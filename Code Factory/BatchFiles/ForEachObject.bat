@Echo Off
rem CD \Work

rem For Each File
ECHO List Files:
FOR %%G IN ("S*") DO Echo We found %%~nxG

ECHO List Directories:
rem For Each Directory
FOR /D /r %%G IN ("S*") DO Echo We found %%~nxG



