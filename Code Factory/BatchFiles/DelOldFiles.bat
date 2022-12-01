@Echo Off
rem Delete all files older than 1 month (31 days).

ECHO Downloads:
forfiles -p "%USERPROFILE%\Downloads" -s -m *.* /D -32 /C "cmd /c del @path"
ECHO Tmp:
forfiles -p "%USERPROFILE%\Tmp" -s -m *.* /D -32 /C "cmd /c del @path"
ECHO OneDrive Tmp:
forfiles -p "%USERPROFILE%\OneDrive\Tmp" -s -m *.* /D -32 /C "cmd /c del @path"


ECHO Clean Manager:
start %windir%\system32\cleanmgr.exe /autoclean /d %systemdrive%



