@ECHO OFF
ECHO "This is just a simple line appended  to create a big file. "
ECHO 64x2^24= 1.073.741.824
ECHO "This is just a simple line appended  to create a big file. " > dummy.txt
for /L %%i in (1,1,24) do type dummy.txt >> dummy.txt