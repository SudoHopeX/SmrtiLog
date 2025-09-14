@REM SmrtiLog by SudoHopeX

@echo off
setlocal enabledelayedexpansion

REM ====== Configuration ======
set "TARGET_HOME=%USERPROFILE%"
set "MODE=%~1"

REM Header
echo.
echo SmrtiLog - A Keystroke Logger Simulation by SudoHopeX
echo.

if "%MODE%"=="" set "MODE=--run"

:dispatch
if /I "%MODE%"=="--help" goto help
if /I "%MODE%"=="-h" goto help
if /I "%MODE%"=="--setup" goto setup
if /I "%MODE%"=="-s" goto setup
if /I "%MODE%"=="--setupRun" goto setupRun
if /I "%MODE%"=="-sr" goto setupRun
if /I "%MODE%"=="--run" goto run
if /I "%MODE%"=="-r" goto run

REM default
goto run

:help
echo Usage:
echo    run.bat [MODE]
echo.
echo MODE:
echo    --help (-h)         Show this help
echo    --setup (-s)        Install safe Python deps globally using pip
echo    --run (-r)          Run the keystroke logger simulator (default)
echo    --setupRun (-sr)    Setup then run
echo.
echo NOTE:
echo    To stop SmrtiLog keystroke logger press 'ESC'
echo    Make sure to run this using an account that can install packages for setup.
goto end

:setup
echo [>] Installing safe Python dependencies globally using pip
echo [!] Make sure you run this using an account that can install packages.
echo.

REM Upgrade pip, then install packages (requests, pynput)
python -m pip install --upgrade pip
if errorlevel 1 (
  echo [!] Failed to run "python -m pip". Ensure Python is on PATH and try again.
  goto end
)

python -m pip install requests pynput cryptography
if errorlevel 1 (
  echo [!] Failed to install 'requests or pynput or cryptography'.
  goto end
)

echo [✔] Safe dependencies installed.
goto end

:setupRun
call :setup
if errorlevel 1 goto end
echo [>] Running the Keystroke logger simulator...
python main.py
goto end

:run
echo [>] Running the Keystroke logger simulator...
python main.py
goto end

:end
endlocal
echo.

echo [*] Thanku for playing with SmrtiLog - SudoHopeX
