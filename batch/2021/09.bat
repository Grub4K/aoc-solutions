@echo off
setlocal EnableDelayedExpansion



set "POINT_MAX=1000"
set "input_file=..\input\09.txt"

:: Read input data
set "y_len=0"
for /F "usebackq delims=" %%a in ("!input_file!") do (
    set "data[!y_len!]=%%a"
    set /a "y_len+=1"
)
set /a "y_len-=1"

:: Get input line length
set "s=!data[0]!"
set "x_len=0"
for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
    if not "!s:~%%P,1!"=="" (
        set /a "x_len+=%%P"
        set "s=!s:~%%P!"
    )
)
set "s="

:: Create a set of points that do not include 9
:: since strings are limited to ~8000, sets are split every POINT_MAX points
set /a "point_counter=-1, point_set[#]=-1"
for /L %%y in (0 1 !y_len!) do (
    for /L %%x in (0 1 !x_len!) do (
        if not "!data[%%y]:~%%x,1!"=="9" (
            set /a "point_counter+=1, prev=point_set[#], point_set[#]=point_counter/%POINT_MAX%"
            if not !point_set[#]!==!prev! (
                set "point_set[!point_set[#]!]=`"
            )
            for %%a in (!point_set[#]!) do (
                set "point_set[%%a]=!point_set[%%a]!%%x,%%y`"
            )
        )
    )
)

:: Reset some values
set /a "highest[0]=highest[1]=highest[2]=risk_value=0, need_new_point=1"

:: We have to loop at most point_counter times
:: since we go over every point at most once
for /L %%. in (0 1 !point_counter!) do (

    %= Check if we have flood filled last basin =%
    if defined need_new_point (
        set "need_new_point="

        %= Reset basin value =%
        set "basin=1"

        %= Get the first point of the list of sets =%
        set "current_point="
        for /L %%a in (0 1 !point_set[#]!) do (
            if not defined current_point if not "!point_set[%%a]!"=="`" (
                for /f "delims=`" %%a in ("!point_set[%%a]!") do (
                    set "current_point=%%a"
                )
                set "point_set[%%a]=!point_set[%%a]:*`=!"
                set "point_set[%%a]=`!point_set[%%a]:*`=!"
            )
        )
        %= Populate the queue with the found new point =%
        set "queue=`!current_point!`"
    )

    %= Get first item in the queue =%
    for /f "tokens=1,2 delims=,`" %%x in ("!queue!") do (
        set "x=%%x"
        set "y=%%y"
        set "value=!data[%%y]:~%%x,1!"
    )
    set "queue=!queue:*`=!"
    set "queue=`!queue:*`=!"
    set "is_risk_point=1"
    %= Loop over all adjacent fields =%
    for %%a in (
        "-1,0"
        "1,0"
        "0,-1"
        "0,1"
    ) do (
        for /F "tokens=1-2 delims=," %%x in ("%%a") do (
            set /a "x_=x+%%x, y_=y+%%y"
        )
        for /F "tokens=1-2 delims=," %%u in ("!x_!,!y_!") do (
            %= If adjacent is bigger it canot be a risk point =%
            if !x_! GEQ 0 if !x_! LEQ !x_len! (
                if !y_! GEQ 0 if !y_! LEQ !y_len! (
                    set /a "test_value=!data[%%v]:~%%u,1!"
                    if !value! GEQ !test_value! (
                        set "is_risk_point=0"
                    )
                )
            )
            %= Put all adjacents into the queue and increment current basin =%
            for /L %%a in (0 1 !point_set[#]!) do (
                if not "!point_set[%%a]:`%%u,%%v`=!"=="!point_set[%%a]!" (
                    set "queue=!queue!%%u,%%v`"
                    set "point_set[%%a]=!point_set[%%a]:`%%u,%%v`=`!"
                    set /a "basin+=1"
                )
            )
        )
    )

    %= Add value to the risk point values =%
    if "!is_risk_point!"=="1" (
        set /a "risk_value+=value+1"
    )

    %= If queue is empty we need a new point from the set =%
    if "!queue!"=="`" (
        set "need_new_point=1"

        %= Check if the current basin places somewhere in the biggest three =%
        if !basin! GTR !highest[2]! (
            set /a "highest[0]=highest[1], highest[1]=highest[2], highest[2]=basin"
        ) else if !basin! GTR !highest[1]! (
            set /a "highest[0]=highest[1], highest[1]=basin"
        ) else if !basin! GTR !highest[0]! (
            set /a "highest[0]=basin"
        )
    )
)

echo !risk_value!


set /a "basin_value=highest[0]*highest[1]*highest[2]"
echo !basin_value!
