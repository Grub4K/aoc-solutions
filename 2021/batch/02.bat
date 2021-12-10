@echo off
setlocal EnableDelayedExpansion

set "operation[forward]=x+"
set "operation[down]=depth+"
set "operation[up]=depth-"

set /a "x=0, depth=0"
for /F "usebackq tokens=1,2" %%a in (
    "..\input\02.txt"
) do (
    set /a "!operation[%%a]!=%%b"
)
set /a "result=x * depth"
echo !result!


set /a "x=0, depth=0, aim=0"
for /F "usebackq tokens=1,2" %%a in (
    "..\input\02.txt"
) do (
    if "%%a"=="forward" (
        set /a "depth+=aim*%%b, x+=%%b"
    ) else if "%%a"=="down" (
        set /a "aim+=%%b"
    ) else if "%%a"=="up" (
        set /a "aim-=%%b"
    )
)
set /a "result=x * depth"
echo !result!
