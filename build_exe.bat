@echo off
rem Bouwt ZwiftClickMyWhoosh.exe (los bestand, geen Python nodig om te draaien)
cd /d "%~dp0"
python -m pip install --quiet bleak pyinstaller
python -m PyInstaller --onefile --console --name ZwiftClickMyWhoosh ^
    --distpath . --workpath build --specpath build zwift_mywhoosh.py
pause
