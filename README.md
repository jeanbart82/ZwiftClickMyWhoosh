# Zwift Click → MyWhoosh

**[Nederlands](#nederlands)** | **[English](#english)**

---

## Nederlands

Gebruik je Zwift Click (ook Zwift Play, Zwift Ride of Click v2) om virtueel te schakelen in MyWhoosh op een Windows-pc.
Het programma maakt via Bluetooth verbinding met de Click en zet elke knopdruk om in een toetsaanslag voor MyWhoosh.

De Zwift Cog heeft geen elektronica en heeft dit programma niet nodig: je koppelt je trainer (bijv. Zwift Hub) gewoon in MyWhoosh.

### Wat heb je nodig
- Windows 10 of 11 met Bluetooth
- MyWhoosh
- Een Zwift Click (of Play / Ride / Click v2)

### Installatie

Kies één van de twee manieren.

#### A. Losse .exe (geen Python nodig)
1. Download `ZwiftClickMyWhoosh-vX.Y.Z.zip` van de [Releases-pagina](https://github.com/jeanbart82/ZwiftClickMyWhoosh/releases/latest).
2. Klik met de rechtermuisknop op de zip → **Eigenschappen** → vink **Blokkering opheffen** aan → **OK**.
3. Pak de zip uit. `ZwiftClickMyWhoosh.exe` en `config.json` moeten samen in één map blijven.
4. Dubbelklik `ZwiftClickMyWhoosh.exe`.

#### B. Met Python (`start.bat`)
1. Installeer Python 3 via [python.org](https://www.python.org/downloads/) of de Microsoft Store.
   Vink bij de installatie **"Add python.exe to PATH"** aan.
2. Dubbelklik `start.bat`. De eerste keer wordt het onderdeel `bleak` gedownload, daarvoor is internet nodig.

Je hebt bij beide manieren **geen beheerdersrechten** nodig.

#### Updaten
Download de nieuwe zip en vervang **zowel `ZwiftClickMyWhoosh.exe` als `config.json`**. Heb je zelf toetsen aangepast, zet die dan daarna opnieuw in de nieuwe `config.json`.

### Gebruik
1. **Click vrijmaken**
   - Sluit de Zwift-app en Zwift Companion, ook op je telefoon. Anders blijft de Click daarmee verbonden.
   - Staat de Click in **Windows-instellingen → Bluetooth en apparaten**? Verwijder hem daar dan. Het programma maakt zelf verbinding.
2. **MyWhoosh klaarzetten**
   - Start MyWhoosh en koppel je trainer.
   - Zet **virtueel schakelen** aan.
   - Kijk bij de toetsenbordinstellingen welke toetsen zwaarder en lichter schakelen. Standaard is dat `K` (zwaarder) en `I` (lichter). Is dat bij jou anders, pas dan `config.json` aan (zie hieronder).
3. **Programma starten**
   - Start de `.exe` of `start.bat`.
   - Druk een paar keer op een knop van de Click om hem wakker te maken.
   - Wacht tot je **"handshake OK"** ziet. Bij een Click v2 (of Play / Ride) verbinden de linker- en rechterhelft apart; je ziet dan beide.
4. **Rijden**
   - Klik in het MyWhoosh-venster zodat het actief is. De toetsen gaan altijd naar het actieve venster.
   - Druk je op + of −, dan zie je in het programmavenster bijvoorbeeld `plus -> toets 'k'`.
5. **Stoppen**: druk op Ctrl+C in het programmavenster, of sluit het venster.

### Instellen (`config.json`)
- `language`: `"nl"` (Nederlands, standaard) of `"en"` (Engels) voor de meldingen van het programma.
- `buttons`: welke knop welke toets geeft. De standaard:

  | Knop | Toets | In MyWhoosh |
  |---|---|---|
  | Click `plus`, alles aan de rechterkant (`shift_up_right`, `shift_down_right`, `paddle_right`, `side_right`, `powerup_right`) | `K` | Zwaarder schakelen |
  | Click `minus`, alles aan de linkerkant (`shift_up_left`, `shift_down_left`, `paddle_left`, `side_left`, `powerup_left`) | `I` | Lichter schakelen |
  | `left` / `right` (richtingskruis) | `A` / `D`, vastgehouden | Sturen |
  | `onoff_left` / `onoff_right` | `H` | Interface verbergen/tonen |
  | `up` / `down` (richtingskruis) | pijltje omhoog / omlaag | Door menu's bladeren |
  | `a` / `b` | `Enter` / `Escape` | Bevestigen / terug |
  | `y`, `z` | – | Niet gekoppeld |

  `Enter` en `Escape` voor de menu's zijn nog niet getest in MyWhoosh. Werken ze niet, kijk dan in MyWhoosh welke toetsen het menu bedienen.

  **Knopnamen per controller**

  | Controller | Knop → naam |
  |---|---|
  | Zwift Click | + → `plus`, − → `minus` |
  | Zwift Click v2, linkerhelft | ▲ → `up`, ▼ → `down`, ◀ → `left`, ▶ → `right`, − → `shift_up_left` |
  | Zwift Click v2, rechterhelft | Y → `y`, Z → `z`, A → `a`, B → `b`, + → `shift_up_right` |
  | Zwift Play | links: `up`, `down`, `left`, `right`, `side_left`, `onoff_left`, `paddle_left` · rechts: `y`, `z`, `a`, `b`, `side_right`, `onoff_right`, `paddle_right` |
  | Zwift Ride | als de Play, plus `shift_up_left`, `shift_down_left`, `shift_up_right`, `shift_down_right`, `powerup_left`, `powerup_right` |

  - Een toets die ingedrukt blijft zolang je de knop vasthoudt, schrijf je zo: `"left": {"key": "a", "hold": true}`. Zonder `hold` wordt het één tik.
  - MyWhoosh heeft ook emotes onder de toetsen `1` tot en met `7`. Je kunt ze aan een vrije knop koppelen, bijv. `"z": "7"`.
  - De Click v2 heeft geen aan/uit-knop. Wil je de interface kunnen verbergen, koppel dan `H` aan een vrije knop: `"y": "h"`.
  - Druk je op een knop die nog niet gekoppeld is, dan toont het programma de naam van die knop. Zet die naam in `buttons` met de gewenste toets.
  - Mogelijke toetsen: letters, cijfers, `space`, `enter`, `escape`, `tab`, `backspace`, `up`, `down`, `left`, `right`, `pageup`, `pagedown`, `home`, `end`, `insert`, `delete`, `f1`–`f12`, `minus`, `plus`, `comma`, `period`. Een lege waarde (`""`) betekent: niet gekoppeld.
- `focus_window_title`: zet hier bijv. `"MyWhoosh"` in. Het programma haalt dan het MyWhoosh-venster naar voren voor elke toetsaanslag.
- `key_hold_ms`: hoe lang een toets ingedrukt blijft (standaard 40 ms). Verhoog dit als MyWhoosh af en toe een schakeling mist.
- `debug`: zet op `true` om de ruwe Bluetooth-data te zien. Je kunt ook `start.bat --debug` gebruiken.

Herstart het programma na een wijziging in `config.json`.

### Waarschuwingen van Windows

**"Windows heeft uw pc beveiligd" (SmartScreen)**
De `.exe` is niet digitaal ondertekend. Windows kan daarom waarschuwen als je hem hebt gedownload, bijvoorbeeld van GitHub, of via e-mail of Teams hebt ontvangen.
Kies dan **Meer info → Toch uitvoeren**.

**Gedownloade zip**
Download je het project als zip van GitHub, klik dan vóór het uitpakken met de rechtermuisknop op de zip → **Eigenschappen** → vink **Blokkering opheffen** aan → **OK**.
Pak de zip daarna pas uit.

**Virusscanner**
Een zelfgebouwde `.exe` wordt soms ten onrechte als verdacht gemeld. Gebruik in dat geval `start.bat` met Python.

**Werklaptop**
Op een laptop van je werk kan het IT-beleid scripts, Bluetooth-apparaten of onbekende programma's blokkeren. Gebruik het bij voorkeur op een privé-pc.

### Problemen oplossen
| Probleem | Oplossing |
|---|---|
| "Geen controller gevonden" | Druk op een knop van de Click. Controleer stap 1 bij Gebruik: Zwift en Companion gesloten, Click niet gekoppeld in Windows. Staat Bluetooth aan? |
| Wel `plus -> toets 'k'` in het venster, maar MyWhoosh reageert niet | Klik eerst in het MyWhoosh-venster, of zet `focus_window_title` op `"MyWhoosh"`. Controleer of de toetsen kloppen met de instellingen van MyWhoosh. |
| MyWhoosh reageert nog steeds niet | Draait MyWhoosh als administrator? Dan blokkeert Windows de toetsaanslagen. Start MyWhoosh normaal, of start dit programma ook als administrator. |
| Knop doet iets anders dan verwacht | Kijk welke knopnaam het programma toont en pas `buttons` in `config.json` aan. |
| + en − schakelen niet op een Click v2 | Gebruik versie 1.2.1 of nieuwer, en vervang ook `config.json`. |
| Click v2 werkt niet | Een Click v2 moet soms eerst een keer met de Zwift-app verbonden zijn geweest. Sluit Zwift daarna weer af. |
| Zwift Ride werkt niet | Firmware nieuwer dan 1.2.0 is door Zwift afgeschermd en werkt niet met andere programma's. |
| Python niet gevonden (`start.bat`) | Installeer Python opnieuw en vink "Add python.exe to PATH" aan. Of gebruik de `.exe`. |

### Zelf de .exe bouwen
Heb je de code aangepast? Dubbelklik dan `build_exe.bat`. Daarvoor is Python nodig.
De nieuwe `ZwiftClickMyWhoosh.exe` verschijnt in dezelfde map.

---

## English

Use your Zwift Click (also Zwift Play, Zwift Ride or Click v2) for virtual shifting in MyWhoosh on a Windows PC.
The program connects to the Click over Bluetooth and turns every button press into a keystroke for MyWhoosh.

The Zwift Cog has no electronics and doesn't need this program: just pair your trainer (e.g. Zwift Hub) in MyWhoosh as usual.

> The program shows its messages in Dutch by default. For English, set `"language": "en"` in `config.json`.

### Requirements
- Windows 10 or 11 with Bluetooth
- MyWhoosh
- A Zwift Click (or Play / Ride / Click v2)

### Installation

Pick one of the two options.

#### A. Standalone .exe (no Python needed)
1. Download `ZwiftClickMyWhoosh-vX.Y.Z.zip` from the [Releases page](https://github.com/jeanbart82/ZwiftClickMyWhoosh/releases/latest).
2. Right-click the zip → **Properties** → tick **Unblock** → **OK**.
3. Extract the zip. Keep `ZwiftClickMyWhoosh.exe` and `config.json` together in the same folder.
4. Double-click `ZwiftClickMyWhoosh.exe`.

#### B. With Python (`start.bat`)
1. Install Python 3 from [python.org](https://www.python.org/downloads/) or the Microsoft Store.
   During installation, tick **"Add python.exe to PATH"**.
2. Double-click `start.bat`. The first run downloads the `bleak` package, so you need an internet connection.

Neither option needs **administrator rights**.

#### Updating
Download the new zip and replace **both `ZwiftClickMyWhoosh.exe` and `config.json`**. If you changed any keys yourself, re-apply them in the new `config.json` afterwards.

### Usage
1. **Free up the Click**
   - Close the Zwift app and Zwift Companion, including on your phone. Otherwise the Click stays connected to them.
   - Is the Click listed under **Windows Settings → Bluetooth & devices**? Remove it there. The program connects to it by itself.
2. **Set up MyWhoosh**
   - Start MyWhoosh and pair your trainer.
   - Turn on **virtual shifting**.
   - Check the keyboard settings for the keys that shift harder and easier. By default they are `K` (harder) and `I` (easier). If yours are different, change them in `config.json` (see below).
3. **Start the program**
   - Run the `.exe` or `start.bat`.
   - Press a button on the Click a few times to wake it up.
   - Wait until you see **"handshake OK"**. A Click v2 (or Play / Ride) connects its left and right halves separately, so you'll see it for both.
4. **Ride**
   - Click in the MyWhoosh window so it's active. Keystrokes always go to the active window.
   - When you press + or −, the program window shows something like `plus -> key 'k'`.
5. **Stop**: press Ctrl+C in the program window, or close the window.

### Configuration (`config.json`)
- `language`: `"nl"` (Dutch, default) or `"en"` (English) for the program's messages.
- `buttons`: which button sends which key. The defaults:

  | Button | Key | In MyWhoosh |
  |---|---|---|
  | Click `plus`, everything on the right (`shift_up_right`, `shift_down_right`, `paddle_right`, `side_right`, `powerup_right`) | `K` | Shift harder |
  | Click `minus`, everything on the left (`shift_up_left`, `shift_down_left`, `paddle_left`, `side_left`, `powerup_left`) | `I` | Shift easier |
  | `left` / `right` (D-pad) | `A` / `D`, held | Steering |
  | `onoff_left` / `onoff_right` | `H` | Hide/show UI |
  | `up` / `down` (D-pad) | arrow up / down | Navigate menus |
  | `a` / `b` | `Enter` / `Escape` | Confirm / back |
  | `y`, `z` | – | Not mapped |

  `Enter` and `Escape` for the menus haven't been tested in MyWhoosh yet. If they don't work, check which keys MyWhoosh uses for its menus.

  **Button names per controller**

  | Controller | Button → name |
  |---|---|
  | Zwift Click | + → `plus`, − → `minus` |
  | Zwift Click v2, left half | ▲ → `up`, ▼ → `down`, ◀ → `left`, ▶ → `right`, − → `shift_up_left` |
  | Zwift Click v2, right half | Y → `y`, Z → `z`, A → `a`, B → `b`, + → `shift_up_right` |
  | Zwift Play | left: `up`, `down`, `left`, `right`, `side_left`, `onoff_left`, `paddle_left` · right: `y`, `z`, `a`, `b`, `side_right`, `onoff_right`, `paddle_right` |
  | Zwift Ride | same as the Play, plus `shift_up_left`, `shift_down_left`, `shift_up_right`, `shift_down_right`, `powerup_left`, `powerup_right` |

  - For a key that stays pressed while you hold the button, write: `"left": {"key": "a", "hold": true}`. Without `hold` it's a single tap.
  - MyWhoosh also has emotes on keys `1` to `7`. You can map them to a free button, e.g. `"z": "7"`.
  - The Click v2 has no on/off button. To be able to hide the UI, map `H` to a free button: `"y": "h"`.
  - When you press a button that isn't mapped yet, the program shows its name. Add that name to `buttons` with the key you want.
  - Available keys: letters, digits, `space`, `enter`, `escape`, `tab`, `backspace`, `up`, `down`, `left`, `right`, `pageup`, `pagedown`, `home`, `end`, `insert`, `delete`, `f1`–`f12`, `minus`, `plus`, `comma`, `period`. An empty value (`""`) means: not mapped.
- `focus_window_title`: set this to e.g. `"MyWhoosh"` and the program brings the MyWhoosh window to the front before every keystroke.
- `key_hold_ms`: how long a key stays pressed (default 40 ms). Increase it if MyWhoosh occasionally misses a shift.
- `debug`: set to `true` to see the raw Bluetooth data. You can also use `start.bat --debug`.

Restart the program after changing `config.json`.

### Windows warnings

**"Windows protected your PC" (SmartScreen)**
The `.exe` isn't digitally signed. Windows may warn you if you downloaded it, for example from GitHub, or received it by e-mail or Teams.
Choose **More info → Run anyway**.

**Downloaded zip**
If you download the project as a zip from GitHub, right-click the zip before extracting → **Properties** → tick **Unblock** → **OK**.
Extract it only after that.

**Antivirus**
A self-built `.exe` is sometimes wrongly flagged as suspicious. In that case, use `start.bat` with Python.

**Work laptop**
On a work laptop, IT policy may block scripts, Bluetooth devices or unknown programs. Preferably use it on a personal PC.

### Troubleshooting
| Problem | Solution |
|---|---|
| "No controller found" | Press a button on the Click. Check step 1 under Usage: Zwift and Companion closed, Click not paired in Windows. Is Bluetooth on? |
| The window shows `plus -> key 'k'`, but MyWhoosh doesn't respond | Click in the MyWhoosh window first, or set `focus_window_title` to `"MyWhoosh"`. Check that the keys match MyWhoosh's settings. |
| MyWhoosh still doesn't respond | Is MyWhoosh running as administrator? Then Windows blocks the keystrokes. Start MyWhoosh normally, or run this program as administrator too. |
| A button does something unexpected | Look at the button name the program shows and adjust `buttons` in `config.json`. |
| + and − don't shift on a Click v2 | Use version 1.2.1 or newer, and replace `config.json` too. |
| Click v2 doesn't work | A Click v2 sometimes needs to have been connected to the Zwift app once first. Close Zwift again afterwards. |
| Zwift Ride doesn't work | Firmware newer than 1.2.0 is locked by Zwift and doesn't work with third-party programs. |
| Python not found (`start.bat`) | Reinstall Python and tick "Add python.exe to PATH". Or use the `.exe`. |

### Building the .exe yourself
Changed the code? Double-click `build_exe.bat`. This requires Python.
The new `ZwiftClickMyWhoosh.exe` appears in the same folder.
