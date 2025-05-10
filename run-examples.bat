@echo off
setlocal enabledelayedexpansion

:: Go to examples directorys
cd /d "%~dp0examples"

:: Search for all .py files
for %%f in (*.py) do (
    echo Executings %%f...
    python "%%f"
    if errorlevel 1 (
        echo Error while executing %%f
        exit /b 1
    )
)

echo All examples have been executed succesfully
pause