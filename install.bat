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

:: create destination folder (to avoid xcopy prompt)
2> nul mkdir %desktopInstallationFolder%

:: copy everything to installation folder on desktop
xcopy "example scripts\%scriptName%" %desktopInstallationFolder% /y /c
xcopy "example scripts\functions.py" %desktopInstallationFolder% /y /c
xcopy "custom ball texture stuff\autoclicker images\*.png" %autoclickerImagesFolder% /y /c /i

cls
echo.
echo.
echo.   Setup complete! Press any key to exit.
echo.
echo.
timeout /t 10 >nul 2>&1