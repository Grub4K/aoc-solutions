@echo off
setlocal EnableDelayedExpansion

:: reverse macro for later use with default box movement
set "@reverse(?)="
for /L %%a in ( 0 1 100 ) do (
    set "@reverse(?)=^!?:~%%a,1^!!@reverse(?)!"
)
set @reverse(?)=set "?=!@reverse(?)!"


:: Process the *super easy* to read input structure
set "step_one=1"
set "first=1"
set "movements=,"

for /F "usebackq delims=" %%L in ("%~1") do (
    if defined step_one (
        set "line=%%L"
        set /a "control=!line: =!"
        if "!control!"=="!line: =!" (
            set "step_one="
        ) else (
            set /a "boxes[#]=0"
            for /L %%A in (1 4 40) do (
                set "char=!line:~%%A,1!"
                if not "!char!"=="" (
                    set /a "boxes[#]+=1"
                    if defined first (
                        set "boxes[!boxes[#]]="
                    )
                    if not "!char!"==" " (
                        for /f "delims=" %%B in ("boxes[!boxes[#]!]") do (
                            set "%%B=!line:~%%A,1!!%%B!"
                        )
                    )
                )
            )
            set "first="
        )
    ) else (
        for /F "tokens=2,4,6" %%A in ("%%L") do (
            set "movements=!movements!%%A`%%B`%%C,"
        )
    )
)

:: Copy boxes
set "boxes_b[#]=!boxes[#]!"
for /L %%A in (1 1 !boxes[#]!) do (
    set "boxes_b[%%A]=!boxes[%%A]!"
)

:: Apply movements
for %%F in (!movements!) do (
    for /F "tokens=1-3 delims=`" %%A in ("%%F") do (
        set "s=!boxes[%%B]:~-%%A!"
        %@reverse(?):?=s%
        set "boxes[%%C]=!boxes[%%C]!!s!"
        set "boxes[%%B]=!boxes[%%B]:~0,-%%A!"

        set "boxes_b[%%C]=!boxes_b[%%C]!!boxes_b[%%B]:~-%%A!"
        set "boxes_b[%%B]=!boxes_b[%%B]:~0,-%%A!"
    )
)

:: Get result
set "result="
set "result_b="
for /L %%A in (1 1 !boxes[#]!) do (
    set "result=!result!!boxes[%%A]:~-1!"
    set "result_b=!result_b!!boxes_b[%%A]:~-1!"
)
echo !result!
echo !result_b!
