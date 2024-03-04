@echo off

echo.
echo.
echo.
echo.                       [1]     PS4 controller
echo.
echo.
echo.                       [2]     PS5 controller
echo.
echo.
echo.                       [3]     Xbox controller
echo.
echo.
echo.                       [4]     KBM
echo.
echo.
echo.
echo.
echo.
echo.

:: get choice
set pass=
choice /c 1234 /n /m "Choose the type of script to install . . . "
set pass=%errorlevel%

:: set appropriate script name
if errorlevel 1 set scriptName="PS4_controller_example.py"
if errorlevel 2 set scriptName="PS5_controller_example.py"
if errorlevel 3 set scriptName="Xbox_controller_example.py"
if errorlevel 4 set scriptName="KBM_example.py"
cls

set desktopInstallationFolder="%USERPROFILE%\Desktop\Quickchats Script"
set autoclickerImagesFolder="%USERPROFILE%\Desktop\Quickchats Script\autoclicker images"

:: change current working directory to the repo folder (for when running as admin)
cd %~dp0

:: upgrade pip and install dependecies
python.exe -m pip install --upgrade pip
pip install -r requirements.txt
pip install -U Pillow

:: create folders for installation
2> nul mkdir %desktopInstallationFolder%
2>nul mkdir %autoclickerImagesFolder%

:: copy everything to installation folder on desktop
copy /v /y "example scripts\%scriptName%" %desktopInstallationFolder%
copy /v /y "example scripts\functions.py" %desktopInstallationFolder%
copy /v /y "custom ball texture stuff\autoclicker images\*.png" %autoclickerImagesFolder%

cls

:: display appropriate exit message
if %errorlevel% equ 0 (
    echo.
    echo.
    echo.   Setup complete! Press any key to exit.
    echo.
    echo.
    timeout /t 10 >nul 2>&1
) else (
    echo.
    echo.
    echo.   An error occured during installation!
    echo.   
    echo.   ... maybe try running as administrator?
    echo.   
    echo.   
    echo.   
    echo.   
    echo.   
    echo.   Press any key to exit.
    echo.
    echo.
    timeout /t 10 >nul 2>&1
)
