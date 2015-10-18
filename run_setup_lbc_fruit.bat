@echo off
cls
echo Compiling
if exist build rd /s /q build
if exist dist rd /s /q dist
python -OO setup_lbc_fruit.py py2exe>log.txt
if exist dist\w9xpopen.exe del dist\w9xpopen.exe
echo Done!
