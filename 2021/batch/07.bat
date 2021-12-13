@echo off
setlocal EnableDelayedExpansion



:: Get input line
:: Since its longer than 1023 we have to use a different method
set "input_file=..\input\07.txt"
for %%a in ("!input_file!") do set /a "file_size=%%~za"

>nul (
    for /L %%a in (0 1023 !file_size!) do (
        <"!input_file!" (
            for /L %%. in (1 1 %%a) do pause
            set /P "input="
        )
        set "input_line=!input_line!!input!"
    )
)

:: Get range of values in dataset
set "stop=0"
set "start=99999999"
for %%a in (!input_line!) do (
    if %%a lss !start! (
        set "start=%%a"
    )
    if %%a gtr !stop! (
        set "stop=%%a"
    )
)

:: Process distance and fuel usage
set "distMin=99999999"
set "fuelMin=99999999"
for /L %%a in (!start! 1 !stop!) do (
    set /a "distSum=0, fuelSum=0"
    for %%b in (%input_line%) do (
        set /a "x=(%%a-%%b), dist=(x>>31|1)*x, distSum+=dist, fuelSum+=dist*(dist+1)/2"
    )
    if !distSum! lss !distMin! (
        set "distMin=!distSum!"
    )
    if !fuelSum! lss !fuelMin! (
        set "fuelMin=!fuelSum!"
    )
)
echo !distMin!
echo !fuelMin!
