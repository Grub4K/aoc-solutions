@echo off
setlocal EnableDelayedExpansion
for /F "tokens=1 delims==" %%a in ('set "count[" 2^>nul') do set "%%a="


set "length="
for /F "usebackq tokens=1,2" %%a in (
    "..\input\03.txt"
) do (
    set "line=%%a"
    set /a "length+=1"
)
set "numberOfBits=0"
for %%a in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
    if "!line:~%%a,1!" neq "" (
        set /a "numberOfBits+=%%a"
        set "line=!line:~%%a!"
    )
)


for /F "usebackq tokens=1,2" %%a in (
    "..\input\03.txt"
) do (
    set "line=%%a"
    for /L %%b in (0 1 !numberOfBits!) do (
        set /a "count[%%b]+=!line:~%%b,1!"
    )
)

set /a "threshold=length / 2, gamma=0, epsilon=0, additor=1"
for /L %%a in (!numberOfBits! -1 0 ) do (
    if !count[%%a]! gtr !threshold! (
        set /a "gamma+=additor"
    ) else set /a "epsilon+=additor"
    set /a "additor<<=1"
)
set /a "result=gamma*epsilon"

echo !result!


:: create a lookup for each value
for /F "usebackq tokens=1,2" %%a in (
    "..\input\03.txt"
) do (
    set "lookup[%%a]=1"
)

for /L %%a in ( 0 1 !numberOfBits! ) do (
    set "count[0]=0"
    set "count[1]=0"
    %= Count bits at current position =%
    for /F "tokens=1 delims==" %%b in ('set "lookup[!filterA!" 2^>nul') do (
        set "bit=%%b"
        set "bit=!bit:~7!"
        set "bit=!bit:~%%a,1!"
        set /a "count[!bit!]+=1"
    )
    %= Adjust filter based of current position =%
    if !count[1]! geq !count[0]! (
        set "filterA=!filterA!1"
    ) else set "filterA=!filterA!0"
)

set "foundB="
for /L %%a in ( 0 1 !numberOfBits! ) do (
    if not defined foundB (
        set "once="
        set "foundB=1"
        set "count[0]=0"
        set "count[1]=0"
        %= Count bits at current position, exit early to get last found name =%
        for /F "tokens=1 delims==" %%b in ('set "lookup[!filterB!" 2^>nul') do (
            set "bit=%%b"
            set "nameB=!bit:~7,-1!"
            set "bit=!nameB:~%%a,1!"
            set /a "count[!bit!]+=1"
            if defined once set "foundB="
            set "once=1"
        )
        if !count[1]! geq !count[0]! (
            set "filterB=!filterB!0"
        ) else set "filterB=!filterB!1"
    )
)

:: Convert to base 10
set /a "oxygen=0, co2=0, current=1"
for /L %%a in ( !numberOfBits! -1 0 ) do (
    if "!filterA:~%%a,1!"=="1" (
        set /a "oxygen+=current"
    )
    if "!nameB:~%%a,1!"=="1" (
        set /a "co2+=current"
    )
    set /a "current<<=1"
)

set /a "result=oxygen*co2"
echo !result!
