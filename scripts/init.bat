@echo off
rem ---------------------------------------------------------------------------
rem  Install PM Workflow into the current directory (Windows).
rem
rem  Usage: from your project folder, run the full path to this file, e.g.
rem     C:\path\to\edu-pm-workflow\scripts\init.bat
rem
rem  Pure ASCII on purpose: cmd.exe decodes batch text with the console OEM
rem  codepage. All real logic lives in scripts\initialize.py.
rem ---------------------------------------------------------------------------
chcp 65001 >nul
setlocal

set "PMPY="
py -3 -c "print('PMPYOK')" 2>nul | findstr /C:"PMPYOK" >nul && set "PMPY=py -3"
if not defined PMPY (
  python -c "print('PMPYOK')" 2>nul | findstr /C:"PMPYOK" >nul && set "PMPY=python"
)
if not defined PMPY (
  python3 -c "print('PMPYOK')" 2>nul | findstr /C:"PMPYOK" >nul && set "PMPY=python3"
)
if not defined PMPY goto nopython

rem %~dp0 is this file's folder; initialize.py sits next to it.
%PMPY% "%~dp0initialize.py" --project "%CD%"
if errorlevel 1 goto failed
endlocal
exit /b 0

:failed
echo.
echo Initialization failed. Press any key to close.
pause >nul
endlocal
exit /b 1

:nopython
echo.
echo Python 3.9 or newer was not found.
echo.
echo   1. Install it from https://www.python.org/downloads/
echo   2. During setup, CHECK the box "Add python.exe to PATH"
echo   3. Run this file again
echo.
pause >nul
endlocal
exit /b 1
