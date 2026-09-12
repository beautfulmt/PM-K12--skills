@echo off
rem ---------------------------------------------------------------------------
rem  Double-click to start the prototype export service, then KEEP THIS WINDOW
rem  OPEN. Then open any prototype .html page and click the export button.
rem
rem  This file MUST stay pure ASCII: cmd.exe decodes batch text using the
rem  console OEM codepage, so non-ASCII characters here would be mojibake or
rem  break parsing. The filename itself may be Chinese (NTFS is Unicode).
rem  All real logic lives in scripts\start_service.py, shared with macOS.
rem ---------------------------------------------------------------------------
chcp 65001 >nul
pushd "%~dp0"

rem Probe for a usable interpreter. We require printed sentinel output rather
rem than trusting the exit code: the Microsoft Store "python" execution alias
rem is a stub that opens the Store and may still exit 0.
set "PMPY="
py -3 -c "print('PMPYOK')" 2>nul | findstr /C:"PMPYOK" >nul && set "PMPY=py -3"
if not defined PMPY (
  python -c "print('PMPYOK')" 2>nul | findstr /C:"PMPYOK" >nul && set "PMPY=python"
)
if not defined PMPY (
  python3 -c "print('PMPYOK')" 2>nul | findstr /C:"PMPYOK" >nul && set "PMPY=python3"
)
if not defined PMPY goto nopython

%PMPY% scripts\start_service.py --serve
if errorlevel 1 goto failed
popd
exit /b 0

:failed
echo.
echo The service stopped with an error. Press any key to close this window.
pause >nul
popd
exit /b 1

:nopython
echo.
echo Python 3.9 or newer was not found.
echo.
echo   1. Install it from https://www.python.org/downloads/
echo   2. During setup, CHECK the box "Add python.exe to PATH"
echo   3. Double-click this file again
echo.
echo Press any key to close this window.
pause >nul
popd
exit /b 1
