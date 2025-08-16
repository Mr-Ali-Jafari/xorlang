@echo off
REM XorLang v2.0.0 Windows Build Script
REM This script builds XorLang and creates installers on Windows

echo ==========================================
echo XorLang v2.0.0 Windows Build Script
echo ==========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again
    pause
    exit /b 1
)

echo Python found. Checking dependencies...

REM Check if PyInstaller is available
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install PyInstaller
    if errorlevel 1 (
        echo Error: Failed to install PyInstaller
        pause
        exit /b 1
    )
)

REM Check if NSIS is available for installer creation
makensis --version >nul 2>&1
if errorlevel 1 (
    echo Warning: NSIS (makensis) not found
    echo Windows installer creation will be skipped
    echo To create installers, install NSIS from: https://nsis.sourceforge.io/
    echo.
)

echo Dependencies check completed.
echo.

REM Run the build script
echo Starting build process...
python build_with_installers.py

if errorlevel 1 (
    echo.
    echo Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Build completed successfully!
echo ==========================================
echo.
echo Generated files:
echo   - CLI executable: dist\xorlang.exe
echo   - IDE executable: dist\xorlang-ide.exe
if exist "installer\windows\XorLang-2.0.0-Setup.exe" (
    echo   - Windows installer: installer\windows\XorLang-2.0.0-Setup.exe
)
echo.
echo You can now distribute these files to users.
pause
