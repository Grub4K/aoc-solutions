@echo off
setlocal EnableDelayedExpansion

set "input="
set "counter=0"
for /F "usebackq delims=" %%a in (
    "..\input\01.txt"
) do (
    if defined input (
        if %%a geq !input! (
            set /a "counter+=1"
        )
    )
    set "input=%%a"
)
echo !counter!

set "skip=#"
set "counter=0"
set "last3=0+0+0"
set "processInput="

for /F "usebackq delims=" %%a in (
    "..\input\01.txt"
) do (
    if defined processInput (
        set /a "first=!last3!, second=!last3:*+=!+%%a, counter+=(first-second)>>31&1"
    ) else (
        set "skip=+!skip!"
        if "!skip:~3!"=="#" (
            set "processInput=1"
        )
    )
    set "last3=!last3:*+=!+%%a"
)
echo !counter!
