@echo off
setlocal EnableDelayedExpansion



set "input_file=..\input\10.txt"

:: Read data in
set "y_len=-1"
for /F "usebackq delims=" %%a in ("!input_file!") do (
    set /a "y_len+=1"
    set "data[!y_len!]=%%a"
)

:: Create some lookups
set "lookup=<({["

set "lookup[(]=)"
set "lookup[[]=]"
set "lookup[{]=}"
set "lookup[<]=>"

set "syntax_error_lookup[)]=3"
set "syntax_error_lookup[]]=57"
set "syntax_error_lookup[}]=1197"
set "syntax_error_lookup[>]=25137"

set "c=1000000000"
set "autocorrect_lookup[)]=%c:~1%%c:~2%1"
set "autocorrect_lookup[]]=%c:~1%%c:~2%2"
set "autocorrect_lookup[}]=%c:~1%%c:~2%3"
set "autocorrect_lookup[>]=%c:~1%%c:~2%4"

set "syntax_error_score=0"

set "autocorrect_scores=,"
set "autocorrect_score_count=0"

:: Iterate over all lines
for /L %%y in (0 1 !y_len!) do (
    %= Get length of current line =%
    set "s=!data[%%y]!"
    set "x_len=0"
    for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
        if not "!s:~%%P,1!"=="" (
            set /a "x_len+=%%P"
            set "s=!s:~%%P!"
        )
    )
    set "s="

    %= Stack, growing to the front =%
    set "stack="
    set "illegal_score="

    %=Iterate over current line =%
    for /L %%x in (0 1 !x_len!) do (
        for %%c in ("!data[%%y]:~%%x,1!") do (
            %= Add character to stack if we have opening brace =%
            if not "!lookup:%%~c=!"=="!lookup!" (
                set "stack=!lookup[%%~c]!!stack!"
            ) else (
                %= Skip if line is corrupted =%
                if not defined illegal_score (
                    set "expected=!stack:~0,1!"
                    set "stack=!stack:~1!"
                    %= Check if we have an unexpected char =%
                    if not "%%~c"=="!expected!" (
                        %= Add to the syntax score =%
                        set "illegal_score=!syntax_error_lookup[%%~c]!"
                        set /a "syntax_error_score+=illegal_score"
                    )
                )
            )
        )
    )
    %= Calculate autocomplete score if its not a corrupted line =%
    %= and we have an unfinished line =%
    if defined stack if not defined illegal_score (
        %= Get length of remaining stack items =%
        set "s=!stack!"
        set "stack_len=0"
        for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
            if not "!s:~%%P,1!"=="" (
                set /a "stack_len+=%%P"
                set "s=!s:~%%P!"
            )
        )
        set "s="

        set "accum=%c:~1%%c:~1%"
        for /L %%x in (0 1 !stack_len!) do (
            set "autocorrect_score=!accum!"
            for %%c in ("!stack:~%%x,1!") do (
                %= Implement bigger addition by using substrings again =%
                %= Multiply by adding 4 times, then add the new value =%
                for %%v in (
                    "!autocorrect_score!"
                    "!autocorrect_score!"
                    "!autocorrect_score!"
                    "!autocorrect_score!"
                    "!autocorrect_lookup[%%~c]!"
                ) do (
                    set "summand=%%~v"
                    set /a "lower=(1!accum:~-9!-%c%) + (1!summand:~-9!-%c%), carry=lower/%c%, lower-=carry*%c%, upper=(1!accum:~0,9!-%c%)+(1!summand:~0,9!-%c%)+carry"
                    set "upper=%c:~1%!upper!"
                    set "lower=%c:~1%!lower!"
                    set "accum=!upper:~-9!!lower:~-9!"
                )
            )
        )
        %= Add items to the stack =%
        set "autocorrect_scores=!autocorrect_scores!!accum!,"
        set /a "autocorrect_score_count+=1"
    )
)
echo !syntax_error_score!

:: Sort the array and take the middle entry
:: We sort by piping the array to the sort command
set "middle_score="
set /a "position=0, middle_position=(autocorrect_score_count+1)/2"
for /F "delims=" %%a in (
    '(for %%b in (!autocorrect_scores!^) do @echo %%b^)^|sort'
) do (
    set /a "position+=1"
    if !position!==%middle_position% (
        %= Strip leading zeroes and set to variable =%
        set "middle_score=%%a"
        set "middle_score=!middle_score:~0,-1!"
        set "first_number=!middle_score:0=!"
        for %%b in ("!first_number:~0,1!") do (
            set "middle_score=%%~b!middle_score:*%%~b=!"
        )
    )
)
echo !middle_score!
