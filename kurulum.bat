@echo off
title Modül Kurulumu
echo Modüller kuruluyor, lütfen bekleyin...

set "commands=pip install requests"

echo Set shell = CreateObject("WScript.Shell") > temp.vbs
echo shell.Run "cmd /c %commands%", 0, True >> temp.vbs

cscript //nologo temp.vbs >nul
del temp.vbs

echo Kurulum tamamlandı!
timeout /t 2 >nul
exit