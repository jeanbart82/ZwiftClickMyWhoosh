@echo off
cd /d "%~dp0"
python -m pip install --quiet bleak
python zwift_mywhoosh.py %*
pause
