@echo off
setlocal EnableDelayedExpansion

:: This solution assumes that node names are unique
set "input_file=..\input\12.txt"

:: Read data in
set "lower=,"
>nul (
    for /F "usebackq tokens=1-2 delims=-" %%a in ("!input_file!") do (
        for %%n in (%%a %%b) do (
            if not defined paths[%%n] (
                set "paths[%%n]=,"
                for /f "delims=ABCDEFGHIJKLMNOPQRSTUVWXYZ" %%. in ("%%n") do (
                    set "lower=!lower!%%n,"
                )
            )
        )
        set "paths[%%a]=!paths[%%a]!%%b,"
        set "paths[%%b]=!paths[%%b]!%%a,"
    )
)

echo !lower!
exit /B

set "visited=,"
call :walk_path  "start" visited 0
echo !errorlevel!
call :walk_path  "start" visited 1
echo !errorlevel!

exit /B 0

:walk_path  <state:str> <visited:var[set[str]]> <budget:int>
setlocal
if not "!lower:,%~1,=!" == "!lower!" (
    if "!%~2:,%~1,=!" == "!%~2!" (
        set "%~2=!%~2!%~1,"
    )
)

set "accum=0"
for %%s in (!paths[%~1]!) do (
    if %%s == end (
        set /a "accum+= 1 "
    ) else if not %%s == start (
        set "skip="
        set "budget=%~3"
        if not "!%~2:,%%s,=!" == "!%~2!" (
            if !budget! == 0 (
                set "skip=1"
            ) else (
                set /a "budget-=1"
            )
        )
        if not defined skip (
            call :walk_path  "%%s" "%~2" !budget!
            set /a "accum+= !errorlevel! "
        )
    )
)
exit /B !accum!
