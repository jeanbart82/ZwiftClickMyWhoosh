"""
Zwift Click / Play / Ride -> MyWhoosh bridge voor Windows.

Maakt via Bluetooth LE verbinding met Zwift-controllers en zet knopdrukken om
in toetsaanslagen (bijv. virtueel schakelen in MyWhoosh).

Gebruik:  python zwift_mywhoosh.py            (normaal)
          python zwift_mywhoosh.py --debug    (toon ruwe BLE-data)
"""

import asyncio
import ctypes
import json
import sys
import time
from ctypes import wintypes
from pathlib import Path

from bleak import BleakClient, BleakScanner

# ---------------------------------------------------------------------------
# Meldingen (config.json: "language": "nl" of "en")
# ---------------------------------------------------------------------------

MESSAGES = {
    "nl": {
        "left": "links",
        "right": "rechts",
        "unknown_key": "Onbekende toets in config: '{key}'",
        "unmapped": "[{name}] knop '{button}' ingedrukt (niet gekoppeld in config.json)",
        "pressed": "[{name}] {button} -> toets '{key}'",
        "scanning": "Zoeken naar Zwift-controllers ({timeout:.0f} s)... druk een knop op je Click om hem wakker te maken.",
        "debug_device": "  [debug] Zwift-apparaat: {name} {address} mfr={mfr}",
        "found": "  Gevonden: {label} ({address})",
        "connected": "[{label}] verbonden",
        "battery": "[{label}] batterij: {level}%",
        "handshake": "[{label}] handshake OK - klaar om te schakelen!",
        "disconnected": "[{label}] verbinding verbroken",
        "connect_error": "[{label}] verbindingsfout: {error}",
        "reconnecting": "[{label}] opnieuw verbinden...",
        "none_found": "Geen controller gevonden. Tips: druk op een knop van de Click, zorg dat hij niet\n"
                      "met Zwift/Companion verbonden is en niet gekoppeld is in Windows Bluetooth-instellingen.\n"
                      "Opnieuw zoeken...\n",
        "ready": "\nOpen MyWhoosh en zorg dat het venster actief is. Stoppen met Ctrl+C.\n",
        "stopped": "Gestopt.",
        "error": "\nFout: {error}",
        "press_enter": "Druk op Enter om af te sluiten...",
    },
    "en": {
        "left": "left",
        "right": "right",
        "unknown_key": "Unknown key in config: '{key}'",
        "unmapped": "[{name}] button '{button}' pressed (not mapped in config.json)",
        "pressed": "[{name}] {button} -> key '{key}'",
        "scanning": "Searching for Zwift controllers ({timeout:.0f} s)... press a button on your Click to wake it up.",
        "debug_device": "  [debug] Zwift device: {name} {address} mfr={mfr}",
        "found": "  Found: {label} ({address})",
        "connected": "[{label}] connected",
        "battery": "[{label}] battery: {level}%",
        "handshake": "[{label}] handshake OK - ready to shift!",
        "disconnected": "[{label}] disconnected",
        "connect_error": "[{label}] connection error: {error}",
        "reconnecting": "[{label}] reconnecting...",
        "none_found": "No controller found. Tips: press a button on the Click, make sure it isn't\n"
                      "connected to Zwift/Companion and isn't paired in Windows Bluetooth settings.\n"
                      "Searching again...\n",
        "ready": "\nOpen MyWhoosh and make sure its window is active. Stop with Ctrl+C.\n",
        "stopped": "Stopped.",
        "error": "\nError: {error}",
        "press_enter": "Press Enter to exit...",
    },
}
language = "nl"


def t(message_id: str, /, **kwargs) -> str:
    return MESSAGES[language][message_id].format(**kwargs)

# ---------------------------------------------------------------------------
# Zwift BLE-protocol
# ---------------------------------------------------------------------------

ZWIFT_MANUFACTURER_ID = 0x094A
SERVICE_UUIDS = {
    "00000001-19ca-4651-86e5-fa29dcdd09d1",  # Click v1 / Play
    "0000fc82-0000-1000-8000-00805f9b34fb",  # Ride / Click v2
}
ASYNC_CHAR = "00000002-19ca-4651-86e5-fa29dcdd09d1"    # notify: knopstatus
SYNC_RX_CHAR = "00000003-19ca-4651-86e5-fa29dcdd09d1"  # write: handshake
SYNC_TX_CHAR = "00000004-19ca-4651-86e5-fa29dcdd09d1"  # indicate: antwoorden
RIDE_ON = b"RideOn"

# Eerste byte van de manufacturer data = apparaattype: (naam, kant)
DEVICE_TYPES = {
    0x02: ("Zwift Play", "right"),
    0x03: ("Zwift Play", "left"),
    0x07: ("Zwift Ride", "right"),
    0x08: ("Zwift Ride", "left"),
    0x09: ("Zwift Click", None),
    0x0A: ("Zwift Click v2", "right"),
    0x0B: ("Zwift Click v2", "left"),
}

MSG_PLAY = 0x07
MSG_BATTERY = 0x19
MSG_RIDE = 0x23
MSG_CLICK = 0x37

# Zwift Ride / Click v2: bit = 0 betekent ingedrukt
RIDE_BUTTONS = {
    0x00001: "left",
    0x00002: "up",
    0x00004: "right",
    0x00008: "down",
    0x00010: "a",
    0x00020: "b",
    0x00040: "y",
    0x00100: "z",
    0x00200: "shift_up_left",
    0x00400: "shift_down_left",
    0x00800: "powerup_left",
    0x01000: "onoff_left",
    0x02000: "shift_up_right",
    0x04000: "shift_down_right",
    0x10000: "powerup_right",
    0x20000: "onoff_right",
}

# Zwift Ride / Click v2: analoge peddels (veld 3), locatie 0 = links, 1 = rechts
RIDE_PADDLES = {0: "paddle_left", 1: "paddle_right"}
RIDE_PADDLE_THRESHOLD = 25

# Zwift Play: protobuf-veldnummer -> knopnaam (waarde 0 = ingedrukt).
# De linkerhelft heeft een richtingskruis, de rechterhelft Y/Z/A/B; namen gelijk aan de Ride.
PLAY_FIELDS = {
    "left": {2: "up", 3: "left", 4: "right", 5: "down", 6: "side_left", 7: "onoff_left"},
    "right": {2: "y", 3: "z", 4: "a", 5: "b", 6: "side_right", 7: "onoff_right"},
}
PLAY_PADDLE_THRESHOLD = 100  # analoge peddel (-100..100): alleen helemaal ingeknepen telt


def protobuf_fields(data: bytes) -> list[tuple[int, int | bytes]]:
    """Minimale protobuf-decoder: geeft (veldnummer, waarde) voor varint- en length-delimited velden."""
    fields: list[tuple[int, int | bytes]] = []
    i = 0

    def varint() -> int:
        nonlocal i
        result = shift = 0
        while i < len(data):
            b = data[i]
            i += 1
            result |= (b & 0x7F) << shift
            if not b & 0x80:
                break
            shift += 7
        return result

    while i < len(data):
        key = varint()
        field, wire = key >> 3, key & 0x07
        if wire == 0:
            fields.append((field, varint()))
        elif wire == 2:
            length = varint()
            fields.append((field, data[i:i + length]))
            i += length
        elif wire == 1:
            i += 8
        elif wire == 5:
            i += 4
        else:
            break
    return fields


def parse_protobuf(data: bytes) -> dict[int, int]:
    """Geeft {veldnummer: waarde} voor de varint-velden (eerste voorkomen)."""
    result: dict[int, int] = {}
    for field, value in protobuf_fields(data):
        if isinstance(value, int):
            result.setdefault(field, value)
    return result


def zigzag(n: int) -> int:
    return (n >> 1) ^ -(n & 1)


def decode_buttons(data: bytes) -> set[str] | None:
    """Zet een notificatie om in de set ingedrukte knoppen (None = geen knopbericht)."""
    if not data:
        return None
    msg_type, payload = data[0], data[1:]

    if msg_type == MSG_CLICK:
        f = parse_protobuf(payload)
        pressed = set()
        if f.get(1, 0) == 0:
            pressed.add("plus")
        if f.get(2, 0) == 0:
            pressed.add("minus")
        return pressed

    if msg_type == MSG_PLAY:
        f = parse_protobuf(payload)
        side = "right" if f.get(1, 0) == 0 else "left"
        pressed = {name for num, name in PLAY_FIELDS[side].items() if f.get(num, 0) == 0}
        if abs(zigzag(f.get(8, 0))) >= PLAY_PADDLE_THRESHOLD:
            pressed.add(f"paddle_{side}")
        return pressed

    if msg_type == MSG_RIDE:
        f = parse_protobuf(payload)
        button_map = f.get(1, 0xFFFFFFFF)
        pressed = {name for bit, name in RIDE_BUTTONS.items() if not button_map & bit}
        for field, value in protobuf_fields(payload):
            if field == 3 and isinstance(value, bytes):
                paddle = parse_protobuf(value)
                name = RIDE_PADDLES.get(paddle.get(1, 0))
                if name and abs(zigzag(paddle.get(2, 0))) >= RIDE_PADDLE_THRESHOLD:
                    pressed.add(name)
        return pressed

    return None


# ---------------------------------------------------------------------------
# Toetsaanslagen via Windows SendInput
# ---------------------------------------------------------------------------

user32 = ctypes.WinDLL("user32", use_last_error=True)

INPUT_KEYBOARD = 1
KEYEVENTF_EXTENDEDKEY = 0x0001
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [("wVk", wintypes.WORD), ("wScan", wintypes.WORD), ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.c_size_t)]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG), ("dy", wintypes.LONG), ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD), ("time", wintypes.DWORD), ("dwExtraInfo", ctypes.c_size_t)]


class _INPUTUNION(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT), ("mi", MOUSEINPUT)]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", _INPUTUNION)]


SPECIAL_KEYS = {
    "space": 0x20, "enter": 0x0D, "tab": 0x09, "escape": 0x1B, "backspace": 0x08,
    "up": 0x26, "down": 0x28, "left": 0x25, "right": 0x27,
    "pageup": 0x21, "pagedown": 0x22, "home": 0x24, "end": 0x23,
    "insert": 0x2D, "delete": 0x2E,
    "minus": 0xBD, "plus": 0xBB, "equals": 0xBB, "comma": 0xBC, "period": 0xBE,
    **{f"f{n}": 0x6F + n for n in range(1, 13)},
}
EXTENDED_VKS = {0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x2D, 0x2E}


def key_to_vk(key: str) -> int:
    key = key.lower().strip()
    if key in SPECIAL_KEYS:
        return SPECIAL_KEYS[key]
    if len(key) == 1 and key.isalnum():
        return ord(key.upper())
    raise ValueError(t("unknown_key", key=key))


def _send_key(vk: int, up: bool) -> None:
    scan = user32.MapVirtualKeyW(vk, 0)  # MAPVK_VK_TO_VSC
    flags = KEYEVENTF_SCANCODE | (KEYEVENTF_KEYUP if up else 0)
    if vk in EXTENDED_VKS:
        flags |= KEYEVENTF_EXTENDEDKEY
    inp = INPUT(type=INPUT_KEYBOARD, u=_INPUTUNION(ki=KEYBDINPUT(wVk=0, wScan=scan, dwFlags=flags)))
    user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(INPUT))


async def tap_key(vk: int, hold_ms: int) -> None:
    _send_key(vk, up=False)
    await asyncio.sleep(hold_ms / 1000)
    _send_key(vk, up=True)


def focus_window(title_part: str) -> None:
    """Zet het venster met title_part in de titel op de voorgrond (als dat nog niet zo is)."""
    found = []

    @ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
    def callback(hwnd, _):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buf, length + 1)
            if title_part.lower() in buf.value.lower():
                found.append(hwnd)
                return False
        return True

    user32.EnumWindows(callback, 0)
    if found and user32.GetForegroundWindow() != found[0]:
        user32.SetForegroundWindow(found[0])


# ---------------------------------------------------------------------------
# Controller-verbinding
# ---------------------------------------------------------------------------

class Bridge:
    def __init__(self, config: dict, debug: bool):
        self.debug = debug
        self.hold_ms = int(config.get("key_hold_ms", 40))
        self.focus_title = config.get("focus_window_title") or None
        # Waarde is "k" (tik) of {"key": "a", "hold": true} (ingedrukt zolang de knop ingedrukt is)
        self.mapping: dict[str, tuple[str, int, bool]] = {}
        for button, value in config["buttons"].items():
            key, hold = (value.get("key", ""), bool(value.get("hold"))) if isinstance(value, dict) else (value, False)
            if key:
                self.mapping[button] = (key, key_to_vk(key), hold)

    async def on_buttons(self, name: str, previous: set[str], pressed: set[str]) -> None:
        for button in sorted(previous - pressed):
            if button in self.mapping and self.mapping[button][2]:
                _send_key(self.mapping[button][1], up=True)

        for button in sorted(pressed - previous):
            if button not in self.mapping:
                print(t("unmapped", name=name, button=button))
                continue
            key, vk, hold = self.mapping[button]
            print(t("pressed", name=name, button=button, key=key))
            if self.focus_title:
                focus_window(self.focus_title)
            if hold:
                _send_key(vk, up=False)
            else:
                await tap_key(vk, self.hold_ms)

    def release_all(self, pressed: set[str]) -> None:
        """Laat vastgehouden toetsen los, bijv. als de verbinding wegvalt."""
        for button in pressed:
            if button in self.mapping and self.mapping[button][2]:
                _send_key(self.mapping[button][1], up=True)


def identify(device, adv) -> str | None:
    """Geeft een naam terug als dit een Zwift-controller is (geen trainer)."""
    name = (adv.local_name or device.name or "").strip()
    if any(x in name.lower() for x in ("hub", "kickr", "trainer")):
        return None
    mfr = adv.manufacturer_data.get(ZWIFT_MANUFACTURER_ID)
    if mfr and mfr[0] in DEVICE_TYPES:
        device_name, side = DEVICE_TYPES[mfr[0]]
        return f"{device_name} ({t(side)})" if side else device_name
    if name.lower().startswith("zwift") and any(x in name.lower() for x in ("click", "play", "ride")):
        return name
    return None


async def find_controllers(timeout: float, debug: bool) -> list[tuple[object, str]]:
    print(t("scanning", timeout=timeout))
    found = await BleakScanner.discover(timeout=timeout, return_adv=True)
    controllers = []
    for device, adv in found.values():
        if debug and (ZWIFT_MANUFACTURER_ID in adv.manufacturer_data
                      or SERVICE_UUIDS & {u.lower() for u in adv.service_uuids}):
            mfr = adv.manufacturer_data.get(ZWIFT_MANUFACTURER_ID, b"")
            print(t("debug_device", name=adv.local_name or device.name, address=device.address, mfr=mfr.hex()))
        label = identify(device, adv)
        if label:
            controllers.append((device, label))
            print(t("found", label=label, address=device.address))
    return controllers


async def run_controller(device, label: str, bridge: Bridge) -> None:
    address = device.address
    target = device
    while True:
        disconnected = asyncio.Event()
        pressed: set[str] = set()
        try:
            async with BleakClient(target, disconnected_callback=lambda _: disconnected.set()) as client:
                print(t("connected", label=label))

                async def on_async(_, data: bytearray):
                    nonlocal pressed
                    data = bytes(data)
                    if bridge.debug:
                        print(f"[{label}] [debug] async {data.hex()}")
                    if data and data[0] == MSG_BATTERY and len(data) > 2:
                        print(t("battery", label=label, level=parse_protobuf(data[1:]).get(1, "?")))
                    new = decode_buttons(data)
                    if new is not None:
                        previous, pressed = pressed, new
                        await bridge.on_buttons(label, previous, new)

                def on_sync_tx(_, data: bytearray):
                    data = bytes(data)
                    if data.startswith(RIDE_ON):
                        print(t("handshake", label=label))
                    elif bridge.debug:
                        print(f"[{label}] [debug] sync {data.hex()}")

                await client.start_notify(ASYNC_CHAR, on_async)
                await client.start_notify(SYNC_TX_CHAR, on_sync_tx)
                rx = client.services.get_characteristic(SYNC_RX_CHAR)
                await client.write_gatt_char(rx, RIDE_ON, response="write-without-response" not in rx.properties)

                await disconnected.wait()
                print(t("disconnected", label=label))
        except Exception as e:  # noqa: BLE001 - BLE-fouten zijn divers, gewoon opnieuw proberen
            print(t("connect_error", label=label, error=e))
        finally:
            bridge.release_all(pressed)

        await asyncio.sleep(3)
        print(t("reconnecting", label=label))
        target = await BleakScanner.find_device_by_address(address, timeout=10) or address


def load_config() -> dict:
    path = Path(getattr(sys, "frozen", False) and sys.executable or __file__).parent / "config.json"
    with open(path, encoding="utf-8") as f:
        return json.load(f)


async def main() -> None:
    global language
    debug = "--debug" in sys.argv
    config = load_config()
    if config.get("language") in MESSAGES:
        language = config["language"]
    debug = debug or bool(config.get("debug"))
    bridge = Bridge(config, debug)

    controllers = []
    while not controllers:
        controllers = await find_controllers(float(config.get("scan_seconds", 8)), debug)
        if not controllers:
            print(t("none_found"))

    print(t("ready"))
    await asyncio.gather(*(run_controller(dev, label, bridge) for dev, label in controllers))


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(t("stopped"))
        time.sleep(0.2)
    except Exception as e:  # noqa: BLE001
        print(t("error", error=e))
        if getattr(sys, "frozen", False):  # .exe: venster openhouden zodat de fout leesbaar is
            input(t("press_enter"))
        raise
