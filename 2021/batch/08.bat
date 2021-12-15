@echo off
setlocal EnableDelayedExpansion



set "input_file=..\input\08.txt"

set "sum="
set "unique_count="
for /F "usebackq tokens=1-2 delims=|" %%1 in ("!input_file!") do (
    for %%a in (%%1) do (
        set "data=%%a"
        set "wires= "
        for %%a in ( a b c d e f g ) do (
            if "!data:%%a=!"=="!data!" (
                set "wires=!wires!  "
            ) else set "wires=!wires!%%a "
        )
        set "wire_count=!wires: =!9876543210"
        set "wire_count=!wire_count:~9,1!"
        if !wire_count!==2 (
            set "one=!wires!"
            set "lookup[!wires: =!]=1"
        ) else if !wire_count!==4 (
            set "four=!wires!"
            set "lookup[!wires: =!]=4"
        ) else if !wire_count!==3 (
            set "lookup[!wires: =!]=7"
        ) else if !wire_count!==7 (
            set "lookup[!wires: =!]=8"
        )
    )

    for %%a in (%%1) do (
        set "data=%%a"
        set "wires= "
        for %%a in ( a b c d e f g ) do (
            if "!data:%%a=!"=="!data!" (
                set "wires=!wires!  "
            ) else set "wires=!wires!%%a "
        )
        set "has_one=1"
        set "has_four=1"
        set "has_four_without_one=1"
        set "four_without_one=!four!"
        for %%b in (!one!) do (
            if "!wires: %%b =!"=="!wires!" set "has_one=0"
            set "four_without_one=!four_without_one: %%b =   !"
        )
        for %%b in (!four!) do (
            if "!wires: %%b =!"=="!wires!" set "has_four=0"
        )

        set "wire_count=!wires: =!9876543210"
        set "wire_count=!wire_count:~9,1!"
        if !wire_count!==5 (
            if !has_one!==1 (
                set "lookup[!wires: =!]=3"
            ) else (
                for %%b in (!four_without_one!) do (
                    if "!wires: %%b =!"=="!wires!" set "has_four_without_one=0"
                )
                if !has_four_without_one!==1 (
                    set "lookup[!wires: =!]=5"
                ) else set "lookup[!wires: =!]=2"
            )
        ) else if !wire_count!==6 (
            if !has_one!==1 (
                if !has_four!==1 (
                    set "lookup[!wires: =!]=9"
                ) else set "lookup[!wires: =!]=0"
            ) else set "lookup[!wires: =!]=6"
        )
    )

    set "result="
    for %%a in (%%2) do (
        set "data=%%a"
        set "wires="
        for %%a in ( a b c d e f g ) do (
            if not "!data:%%a=!"=="!data!" (
                set "wires=!wires!%%a"
            )
        )
        for %%b in (!wires!) do set "result=!result!!lookup[%%b]!"
    )
    set /a "sum+=1!result!-10000"
    set "result=!result:1=!"
    set "result=!result:4=!"
    set "result=!result:7=!"
    set "result=!result:8=!01234"
    set /a "unique_count+=!result:~4,1!"
)
echo !unique_count!
echo !sum!
