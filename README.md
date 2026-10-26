# Zwift Click → MyWhoosh

Zet knoppen van een Zwift Click (ook Play / Ride / Click v2) om in toetsaanslagen voor MyWhoosh.

## Gebruik
1. Koppel je trainer (Zwift Hub + Cog) gewoon in MyWhoosh en zet daar **virtueel schakelen** aan.
2. Zorg dat de Click **niet** verbonden is met Zwift/Companion en **niet** gekoppeld in Windows Bluetooth.
3. Dubbelklik `start.bat` en druk op een knop van de Click.
4. Wacht op "handshake OK" en zet MyWhoosh op de voorgrond.

## Instellen (`config.json`)
- `buttons`: knop → toets. Standaard `plus` = `i` (zwaarder), `minus` = `k` (lichter).
  Kijk in MyWhoosh bij de toetsenbordinstellingen welke toetsen schakelen en pas ze hier aan als dat nodig is.
- Komt er een knop voorbij die nog niet gekoppeld is, dan toont het programma de naam ervan. Zet die naam in `buttons`.
- `focus_window_title`: bijv. `"MyWhoosh"` om dat venster voor elke toetsaanslag naar voren te halen.
- `debug` of `start.bat --debug`: toont de ruwe Bluetooth-data.
