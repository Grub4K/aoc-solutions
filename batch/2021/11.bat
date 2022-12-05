@echo off
setlocal EnableDelayedExpansion



set "input_file=..\input\11.txt"

:: Read data in
set "y_len=-1"
set "data="
for /F "usebackq delims=" %%a in ("!input_file!") do (
    set /a "y_len+=1"
    set "data=!data!%%a"

    if not defined x_len (
        set "s=%%a"
        set "x_len=0"
        for %%P in ( 4096 2048 1024 512 256 128 64 32 16 8 4 2 1 ) do (
            if not "!s:~%%P,1!"=="" (
                set /a "x_len+=%%P"
                set "s=!s:~%%P!"
            )
        )
        set "s="
    )
)
set /a "x_count= x_len + 1 , iter_len= x_count * (y_len + 1) -1"

set "flashes=0"
set "steps="

:: First fixed 100 iterations
set "queue=,"
for /L %%s in (1 1 100) do (
    for /L %%p in (0 1 %iter_len%) do (
        set "queue=!queue!%%p,"
    )
    call :process_queue
    set "data=!data:#=0!"
    if "!data:0=!"=="" (
        set "steps=%%s"
    )
)
echo !flashes!

:: Find the sync steps if not already found
if defined steps (
    echo !steps!
    exit /B
)

set /a "steps=100"
:find_steps
for /L %%s in (1 1 100) do (
    set /a "steps+= 1 "
    for /L %%p in (0 1 %iter_len%) do (
        set "queue=!queue!%%p,"
    )
    call :process_queue
    if "!data:#=!"=="" (
        echo !steps!
        exit /B
    )
    set "data=!data:#=0!"
)
goto :find_steps

exit /B

:process_queue
(
    set "queue=,"
    for %%p in (%queue%) do (
        set "current_value=!data:~%%p,1!"
        if not "!current_value!"=="#" (
            if "!current_value!"=="9" (
                set /a "flashes+= 1 , x= %%p %% %x_count% , y= %%p / %x_count% "
                set "current_value=#"
                for %%s in (
                    "-1'-1" "-1' 0" "-1' 1"
                    " 0'-1"         " 0' 1"
                    " 1'-1" " 1' 0" " 1' 1"
                ) do (
                    for /F "tokens=1-2 delims='" %%x in ("%%s") do (
                        set /a "x_= x + %%x , y_= y + %%y "
                        if !x_! geq 0 if !x_! leq %x_len% (
                            if !y_! geq 0 if !y_! leq %y_len% (
                                set /a "pos= x_count * y_ + x_"
                                set "queue=!queue!!pos!,"
                            )
                        )
                    )
                )
            ) else (
                set /a "current_value+= 1 "
            )
            set "remainder=!data:~%%p!"
            set "data=!data:~0,%%p!!current_value!!remainder:~1!"
        )
    )
)
if "!queue!"=="," exit /B
goto :process_queue
