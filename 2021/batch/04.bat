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
        set "boardsCopy[%%a]="
        set "input="
        for /L %%. in (0 1 5) do (
            set /p "input="
            set "boardsCopy[%%a]=!boardsCopy[%%a]!!input! "
        )
    )
)

:: Prepare board for efficient use
for /L %%a in (1 1 !boardCount!) do (
    set "boardsCopy[%%a]=!boardsCopy[%%a]:  = '!"
    set "boardsCopy[%%a]=!boardsCopy[%%a]: =+!"
    set "boardsCopy[%%a]=!boardsCopy[%%a]:'= !"
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

:: Tasks differ only in which board we take, first winning or last
:: Change flag for if to do early exit or not
for %%f in ( "1" "" ) do (
    %= Restore board states from copy =%
    for /L %%a in (1 1 !boardCount!) do (
        set "boards[%%a]=!boardsCopy[%%a]!"
    )

    %= Execute moves one by one =%
    set "foundWinning="
    for %%a in ( !drawOrder! ) do (
        if not defined foundWinning (
            %= Pad current number =%
            set "currentNumber= %%a"
            set "currentNumber=!currentNumber:~-2!"
            for %%b in ("!currentNumber!") do (
                %= Execute move on every board =%
                for /L %%c in (1 1 !boardCount!) do (
                    set "boards[%%c]=!boards[%%c]:+%%~b+=+XX+!"
                    %= Check if winning =%
                    set "tempBoard=!boards[%%c]:+=!"
                    set "lookup=%#winLookup%"
                    if not "!lookup:XXXXXXXXXX=!"=="!lookup!" (
                        %= Found a winning board =%
                        set /a "boardSum=0!boards[%%c]!0, boardValue=boardSum*currentNumber"
                        set "foundWinning=%%~f"
                        %= Empty board, so it cannot be picked again =%
                        set "boards[%%c]=#"
                    )
                )
            )
        )
    )
    echo !boardValue!
)
exit /B
