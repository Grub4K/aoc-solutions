@echo off
setlocal EnableDelayedExpansion



set "inputFile=..\input\04.txt"

:: Read draw order and boards as linear arrays
for /F "delims=" %%a in ('type "!inputFile!" ^| find /c /v ""') do (
    set /a "boardCount=%%a/6"
)

<"!inputFile!" (
    set /p "drawOrder="
    for /L %%a in (1 1 !boardCount!) do (
        set "boards[%%a]="
        set "input="
        for /L %%. in (0 1 5) do (
            set /p "input="
            set "boards[%%a]=!boards[%%a]!!input! "
        )
    )
)

:: Prepare board for efficient use
for /L %%a in (1 1 !boardCount!) do (
    set "boards[%%a]=!boards[%%a]:  = '!"
    set "boards[%%a]=!boards[%%a]: =+!"
    set "boards[%%a]=!boards[%%a]:'= !"
)

:: Prepare a macro for helping finding winning boards
set "#winLookup=#"
for /L %%x in (0 1 4) do (
    for /L %%y in (0 1 4) do (
        set /a "position=(%%x*2)+(%%y*10)"
        set "#winLookup=!#winLookup!^!tempBoard:~!position!,2^!"
    )
    set /a "position=%%x*10"
    set "#winLookup=!#winLookup!#^!tempBoard:~!position!,10^!#"
)


:: Execute moves one by one
set "firstWinning="
for %%a in ( !drawOrder! ) do (
    %= Pad current number =%
    set "currentNumber= %%a"
    set "currentNumber=!currentNumber:~-2!"
    for %%b in ("!currentNumber!") do (
        %= Execute move on every board =%
        for /L %%c in (1 1 !boardCount!) do (
            if not "!boards[%%c]!"=="#" (
                set "boards[%%c]=!boards[%%c]:+%%~b+=+XX+!"
                %= Check if winning =%
                set "tempBoard=!boards[%%c]:+=!"
                set "lookup=%#winLookup%"
                if not "!lookup:XXXXXXXXXX=!"=="!lookup!" (
                    %= Found a winning board =%
                    set /a "boardSum=0!boards[%%c]!0, boardValue=boardSum*currentNumber"
                    if not defined firstWinning (
                        set "firstWinning=!boardValue!"
                    )
                    %= Empty board, so it cannot be picked again =%
                    set "boards[%%c]=#"
                )
            )
        )
    )
)
echo !firstWinning!
echo !boardValue!
