@echo off
setlocal EnableDelayedExpansion



<"..\input\06.txt" set /P "input_line="

for /L %%a in (0 1 8) do set "count[%%a]=0"
for %%a in (!input_line!) do (
    set /a count[%%a]+=1
)

set /a "from=0, to=7"


:: dont worry about overflow in first one
for /L %%. in (1 1 80) do (
    set /a "count[!to!]+=count[!from!], from=(from+1) %% 9, to=(to+1) %% 9"
)

set "fish=0"
for /L %%a in (0 1 8) do (
    set /a fish+=!count[%%a]!
)
echo !fish!


:: Use "addBigInt" function for second, where overflow might occur
for /L %%. in (81 1 256) do (
    %= count[to] += count[from] =%
    for /F "tokens=1-2 delims= " %%a in ("!from! !to!") do (
        call :addBigInt count[!to!] count[!from!]
        set /a "from=(from+1) %% 9, to=(to+1) %% 9"
    )
)

set "fish=0"
for /L %%a in (0 1 8) do (
    call :addBigInt fish count[%%a]
)
echo !fish!

exit /B


:: This function implement integer addition through adding 2 substringed values
:: It does"!%~1! += !%~2!", just for bigger numbers
:addBigInt  <first/output> <second>
set "lower_a=000000000!%~1:~-9!"
set "lower_b=000000000!%~2:~-9!"

set /a "lower=(1!lower_a:~-9!-1000000000) + (1!lower_b:~-9!-1000000000), carry=lower/1000000000*10, upper=carry + !%~1:~0,-9!0 + !%~2:~0,-9!0"

set "lower=000000000!lower:~-9!"
set "%~1=!upper:~0,-1!!lower:~-9!"

exit /B
