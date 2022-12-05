@echo off
setlocal EnableDelayedExpansion



set /a "boardSize=1000"
:: board building, line based
set "emptyLine="
for /L %%a in (0 1 %boardSize%) do (
    set "emptyLine=!emptyLine! "
)
for /L %%a in (0 1 %boardSize%) do (
    set "board[%%a]=!emptyLine!"
)

set "diagonals[#]=0"
for /F "usebackq tokens=1-4 delims=,-> " %%a in (
    "..\input\05.txt"
) do (
    set "isDiagonal="
    if not "%%a"=="%%c" if not "%%b"=="%%d" (
        set /a "diagonals[#]+=1, isDiagonal=1"
        set "diagonals[!diagonals[#]!]=%%a`%%b`%%c`%%d"
    )
    set /a "count=0, counter+=1"
    if not defined isDiagonal (
        if %%a lss %%c (
            set /a "x_step=1, count=%%c-%%a"
        ) else if %%c lss %%a (
            set /a "x_step=-1, count=%%a-%%c"
        ) else set /a "x_step=0"

        if %%b lss %%d (
            set /a "y_step=1, count=%%d-%%b"
        ) else if %%d lss %%b (
            set /a "y_step=-1, count=%%b-%%d"
        ) else set /a "y_step=0"
        for /L %%s in (0 1 !count!) do (
            set /a "x=%%a+(x_step*%%s), xb=x+1, y=%%b+(y_step*%%s)"
            for /F "tokens=1-3 delims= " %%x in ("!x! !y! !xb!") do (
                set /a "r=!board[%%y]:~%%x,1!+1"
                set "board[%%y]=!board[%%y]:~0,%%x!!r!!board[%%y]:~%%z!"
                if !r!==2 (
                    set /a "intersections+=1"
                )
            )
        )
    )
)
echo !intersections!


for /L %%i in (1 1 %diagonals[#]%) do (
    set /a "count=0, counter+=1"
    for /F "tokens=1-4 delims=`" %%a in ("!diagonals[%%i]!") do (
        if %%a lss %%c (
            set /a "x_step=1, count=%%c-%%a"
        ) else if %%c lss %%a (
            set /a "x_step=-1, count=%%a-%%c"
        ) else set /a "x_step=0"

        if %%b lss %%d (
            set /a "y_step=1, count=%%d-%%b"
        ) else if %%d lss %%b (
            set /a "y_step=-1, count=%%b-%%d"
        ) else set /a "y_step=0"
        for /L %%s in (0 1 !count!) do (
            set /a "x=%%a+(x_step*%%s), xb=x+1, y=%%b+(y_step*%%s)"
            for /F "tokens=1-3 delims= " %%x in ("!x! !y! !xb!") do (
                set /a "r=!board[%%y]:~%%x,1!+1"
                set "board[%%y]=!board[%%y]:~0,%%x!!r!!board[%%y]:~%%z!"
                if !r!==2 (
                    set /a "intersections+=1"
                )
            )
        )
    )
)
echo !intersections!
exit /B
