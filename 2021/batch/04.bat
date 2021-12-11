@echo off
setlocal EnableDelayedExpansion

:: Read draw order and boards as linear arrays
set "drawOrder="
set "counter=######"
set "boardCount=0"
for /F "usebackq delims=" %%a in (
    "..\input\04.txt"
) do (
    if not defined drawOrder (
        set "drawOrder=%%a"
    ) else (
        if "!counter:~5!"=="#" (
            set /a "boardCount+=1"
            set "boardsCopy[!boardCount!]= "
            set "counter=#"
        )
        for %%b in (!boardCount!) do (
            set "boardsCopy[%%b]=!boardsCopy[%%b]!%%a "
        )
        set "counter=!counter!#"
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
