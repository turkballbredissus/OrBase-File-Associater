@echo off
title Orbase Installer
echo ================================
echo        Orbase Installer
echo ================================
echo.

echo Select your Orbs folder...
for /f "delims=" %%I in ('powershell -Command "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.FolderBrowserDialog; $f.Description = 'Select your Orbs folder'; if ($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) { $f.SelectedPath }"') do set "ORBS=%%I"

if "%ORBS%"=="" (
    echo No folder selected. Installation cancelled.
    pause
    exit /b
)

echo Orbs folder set to: %ORBS%
echo.

if not exist "%ORBS%\orBat.ico" (
    echo WARNING: orBat.ico not found in %ORBS%
    echo Please download orBat.ico from GitHub and place it in your Orbs folder, then run the installer again.
    pause
    exit /b
)

echo Icon found. Setting up registry...
echo.

reg add "HKEY_CURRENT_USER\SOFTWARE\Orbase" /v "OrbsFolder" /t REG_SZ /d "%ORBS%" /f >nul

reg add "HKEY_CLASSES_ROOT\.orb" /ve /d "Orbfile" /f >nul
reg add "HKEY_CLASSES_ROOT\Orbfile" /ve /d "Orbfile" /f >nul
reg add "HKEY_CLASSES_ROOT\Orbfile\DefaultIcon" /ve /d "%ORBS%\orBat.ico" /f >nul
reg add "HKEY_CLASSES_ROOT\Orbfile\shell\open\command" /ve /d "\"C:\Windows\System32\cmd.exe\" /c start \"\" \"C:\Users\%USERNAME%\AppData\Local\Programs\Microsoft VS Code\Code.exe\" \"%%1\"" /f >nul

reg add "HKEY_CLASSES_ROOT\.orun" /ve /d "Orunfile" /f >nul
reg add "HKEY_CLASSES_ROOT\Orunfile" /ve /d "Orunfile" /f >nul
reg add "HKEY_CLASSES_ROOT\Orunfile\DefaultIcon" /ve /d "%ORBS%\orBat.ico" /f >nul
reg add "HKEY_CLASSES_ROOT\Orunfile\shell\open\command" /ve /d "powershell.exe -Command \"$n = [IO.Path]::GetFileNameWithoutExtension('%%1'); $path = '%ORBS%\\' + $n + '.orb'; $tmp = $env:TEMP + '\\orbtemp.bat'; Copy-Item $path $tmp; & cmd.exe /c $tmp; Remove-Item $tmp\"" /f >nul

:: Clear icon cache
echo Clearing icon cache...
taskkill /f /im explorer.exe >nul 2>&1
ie4uinit.exe -ClearIconCache >nul 2>&1
del /f /s /q "%localappdata%\Microsoft\Windows\Explorer\iconcache*" >nul 2>&1
start explorer.exe

echo.
echo ================================
echo    Orbase installed successfully!
echo    Place your .orb files in:
echo    %ORBS%
echo ================================
pause
