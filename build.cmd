@echo off
cd /d "%~dp0"
python prepare.py
python setup.py -q bdist_wheel --plat-name=win_amd64
