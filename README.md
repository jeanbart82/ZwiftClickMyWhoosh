# Zwift Click → MyWhoosh

Gebruik je Zwift Click (ook Zwift Play, Zwift Ride of Click v2) om virtueel te schakelen in MyWhoosh op een Windows-pc.
Het programma maakt via Bluetooth verbinding met de Click en zet elke knopdruk om in een toetsaanslag voor MyWhoosh.

De Zwift Cog heeft geen elektronica en heeft dit programma niet nodig: je koppelt je trainer (bijv. Zwift Hub) gewoon in MyWhoosh.

## Wat heb je nodig
- Windows 10 of 11 met Bluetooth
- MyWhoosh
- Een Zwift Click (of Play / Ride / Click v2)

## Installatie

Kies één van de twee manieren.

### A. Losse .exe (geen Python nodig)
1. Download `ZwiftClickMyWhoosh-vX.Y.Z.zip` van de [Releases-pagina](https://github.com/jeanbart82/ZwiftClickMyWhoosh/releases/latest).
2. Klik met de rechtermuisknop op de zip → **Eigenschappen** → vink **Blokkering opheffen** aan → **OK**.
3. Pak de zip uit. `ZwiftClickMyWhoosh.exe` en `config.json` moeten samen in één map blijven.
4. Dubbelklik `ZwiftClickMyWhoosh.exe`.

### B. Met Python (`start.bat`)
1. Installeer Python 3 via [python.org](https://www.python.org/downloads/) of de Microsoft Store.
   Vink bij de installatie **"Add python.exe to PATH"** aan.
2. Dubbelklik `start.bat`. De eerste keer wordt het onderdeel `bleak` gedownload, daarvoor is internet nodig.

Je hebt bij beide manieren **geen beheerdersrechten** nodig.

## Gebruik
1. **Click vrijmaken**
   - Sluit de Zwift-app en Zwift Companion, ook op je telefoon. Anders blijft de Click daarmee verbonden.
   - Staat de Click in **Windows-instellingen → Bluetooth en apparaten**? Verwijder hem daar dan. Het programma maakt zelf verbinding.
2. **MyWhoosh klaarzetten**
   - Start MyWhoosh en koppel je trainer.
   - Zet **virtueel schakelen** aan.
   - Kijk bij de toetsenbordinstellingen welke toetsen zwaarder en lichter schakelen. Zijn dat niet `I` en `K`, pas dan `config.json` aan (zie hieronder).
3. **Programma starten**
   - Start de `.exe` of `start.bat`.
   - Druk een paar keer op een knop van de Click om hem wakker te maken.
   - Wacht tot je **"handshake OK"** ziet.
4. **Rijden**
   - Klik in het MyWhoosh-venster zodat het actief is. De toetsen gaan altijd naar het actieve venster.
   - Druk je op + of −, dan zie je in het programmavenster bijvoorbeeld `plus -> toets 'i'`.
5. **Stoppen**: druk op Ctrl+C in het programmavenster, of sluit het venster.

## Instellen (`config.json`)
- `buttons`: welke knop welke toets geeft. Standaard is `plus` = `i` (zwaarder) en `minus` = `k` (lichter).
  - Druk je op een knop die nog niet gekoppeld is, dan toont het programma de naam van die knop. Zet die naam in `buttons` met de gewenste toets.
  - Mogelijke toetsen: letters, cijfers, `space`, `enter`, `up`, `down`, `left`, `right`, `pageup`, `pagedown`, `f1`–`f12`, `minus`, `plus`, `comma`, `period`.
- `focus_window_title`: zet hier bijv. `"MyWhoosh"` in. Het programma haalt dan het MyWhoosh-venster naar voren voor elke toetsaanslag.
- `key_hold_ms`: hoe lang een toets ingedrukt blijft (standaard 40 ms). Verhoog dit als MyWhoosh af en toe een schakeling mist.
- `debug`: zet op `true` om de ruwe Bluetooth-data te zien. Je kunt ook `start.bat --debug` gebruiken.

Herstart het programma na een wijziging in `config.json`.

## Waarschuwingen van Windows

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

## Problemen oplossen
| Probleem | Oplossing |
|---|---|
| "Geen controller gevonden" | Druk op een knop van de Click. Controleer stap 1 bij Gebruik: Zwift en Companion gesloten, Click niet gekoppeld in Windows. Staat Bluetooth aan? |
| Wel `plus -> toets 'i'` in het venster, maar MyWhoosh reageert niet | Klik eerst in het MyWhoosh-venster, of zet `focus_window_title` op `"MyWhoosh"`. Controleer of de toetsen kloppen met de instellingen van MyWhoosh. |
| MyWhoosh reageert nog steeds niet | Draait MyWhoosh als administrator? Dan blokkeert Windows de toetsaanslagen. Start MyWhoosh normaal, of start dit programma ook als administrator. |
| Knop doet iets anders dan verwacht | Kijk welke knopnaam het programma toont en pas `buttons` in `config.json` aan. |
| Click v2 werkt niet | Een Click v2 moet soms eerst een keer met de Zwift-app verbonden zijn geweest. Sluit Zwift daarna weer af. |
| Python niet gevonden (`start.bat`) | Installeer Python opnieuw en vink "Add python.exe to PATH" aan. Of gebruik de `.exe`. |

## Zelf de .exe bouwen
Heb je de code aangepast? Dubbelklik dan `build_exe.bat`. Daarvoor is Python nodig.
De nieuwe `ZwiftClickMyWhoosh.exe` verschijnt in dezelfde map.
