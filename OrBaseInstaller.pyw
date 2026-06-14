import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import winreg
import os
import ctypes
import subprocess
import threading

ICON_B64 = "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"

BG = "#1a1a2e"
FG = "#e0e0e0"
ACCENT = "#4a90d9"
BTN_BG = "#16213e"
FONT = ("Segoe UI", 10)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_SUB = ("Segoe UI", 10)

RUNNER_SCRIPT = r"""
@echo off
setlocal enabledelayedexpansion

set "ORB_FILE=%~dp0%~n1.orb"
if not exist "!ORB_FILE!" (
    echo Error: Could not find !ORB_FILE!
    pause
    exit /b 1
)

del /f /q "%TEMP%\orbtemp.*" >nul 2>&1

set "FIRST_LINE="
for /f "usebackq delims=" %%L in ("!ORB_FILE!") do (
    if not defined FIRST_LINE set "FIRST_LINE=%%L"
)

set "LANG="
set "HAS_HEADER="
echo !FIRST_LINE! | findstr /i /r /c:"^-- lang:" /c:"^--lang:" >nul
if %errorlevel%==0 (
    for /f "tokens=2,3 delims=: " %%A in ("!FIRST_LINE!") do (
        if "%%B"=="" (set "LANG=%%A") else set "LANG=%%B"
    )
    set "HAS_HEADER=1"
)

if "!LANG!"=="" set "LANG=bat"

if /i "!LANG!"=="bat" goto run_bat
if /i "!LANG!"=="batch" goto run_bat
if /i "!LANG!"=="cmd" goto run_bat
if /i "!LANG!"=="python" goto run_python
if /i "!LANG!"=="py" goto run_python
if /i "!LANG!"=="powershell" goto run_powershell
if /i "!LANG!"=="ps1" goto run_powershell
if /i "!LANG!"=="node" goto run_node
if /i "!LANG!"=="js" goto run_node
if /i "!LANG!"=="javascript" goto run_node
if /i "!LANG!"=="ruby" goto run_ruby
if /i "!LANG!"=="rb" goto run_ruby
if /i "!LANG!"=="perl" goto run_perl
if /i "!LANG!"=="php" goto run_php
if /i "!LANG!"=="java" goto run_java
if /i "!LANG!"=="lua" goto run_lua
if /i "!LANG!"=="go" goto run_go
if /i "!LANG!"=="rust" goto run_rust
if /i "!LANG!"=="r" goto run_r

echo Unsupported language: !LANG!
echo Orbase does not know how to run "!LANG!" files.
echo Make sure the language is installed and supported.
pause
exit /b 1

:copy_orb
if defined HAS_HEADER (
    more +1 "!ORB_FILE!" > "%~1"
) else (
    copy /y "!ORB_FILE!" "%~1" >nul
)
exit /b 0

:run_bat
set "TMP_FILE=%TEMP%\orbtemp.bat"
call :copy_orb "!TMP_FILE!"
call "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_python
call python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Download it from https://python.org
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.py"
call :copy_orb "!TMP_FILE!"
call python "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_powershell
set "TMP_FILE=%TEMP%\orbtemp.ps1"
call :copy_orb "!TMP_FILE!"
call powershell -ExecutionPolicy Bypass -File "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_node
where node >nul 2>&1
if errorlevel 1 (
    echo Node.js is not installed or not in PATH.
    echo Download it from https://nodejs.org
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.js"
call :copy_orb "!TMP_FILE!"
call node "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_ruby
where ruby >nul 2>&1
if errorlevel 1 (
    echo Ruby is not installed or not in PATH.
    echo Download it from https://rubyinstaller.org
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.rb"
call :copy_orb "!TMP_FILE!"
call ruby "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_perl
where perl >nul 2>&1
if errorlevel 1 (
    echo Perl is not installed or not in PATH.
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.pl"
call :copy_orb "!TMP_FILE!"
call perl "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_php
where php >nul 2>&1
if errorlevel 1 (
    echo PHP is not installed or not in PATH.
    echo Download it from https://php.net
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.php"
call :copy_orb "!TMP_FILE!"
call php "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_java
where javac >nul 2>&1
if errorlevel 1 (
    echo Java JDK is not installed or not in PATH.
    echo Download it from https://adoptium.net
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\OrbTemp.java"
call :copy_orb "!TMP_FILE!"
call javac "!TMP_FILE!"
call java -cp "%TEMP%" OrbTemp
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" "%TEMP%\OrbTemp.class" >nul 2>&1
goto end

:run_lua
where lua >nul 2>&1
if errorlevel 1 (
    echo Lua is not installed or not in PATH.
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.lua"
call :copy_orb "!TMP_FILE!"
call lua "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_go
where go >nul 2>&1
if errorlevel 1 (
    echo Go is not installed or not in PATH.
    echo Download it from https://go.dev
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.go"
call :copy_orb "!TMP_FILE!"
call go run "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_rust
where rustc >nul 2>&1
if errorlevel 1 (
    echo Rust is not installed or not in PATH.
    echo Download it from https://rustup.rs
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.rs"
set "TMP_EXE=%TEMP%\orbtemp.exe"
call :copy_orb "!TMP_FILE!"
call rustc "!TMP_FILE!" -o "!TMP_EXE!"
set "EXITCODE=!errorlevel!"
if exist "!TMP_EXE!" (
    call "!TMP_EXE!"
    set "EXITCODE=!errorlevel!"
    del /f /q "!TMP_EXE!" >nul 2>&1
)
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:run_r
where Rscript >nul 2>&1
if errorlevel 1 (
    echo R is not installed or not in PATH.
    echo Download it from https://cran.r-project.org
    pause
    exit /b 1
)
set "TMP_FILE=%TEMP%\orbtemp.r"
call :copy_orb "!TMP_FILE!"
call Rscript "!TMP_FILE!"
set "EXITCODE=!errorlevel!"
del /f /q "!TMP_FILE!" >nul 2>&1
goto end

:end
if defined EXITCODE if not "!EXITCODE!"=="0" (
    echo.
    echo Script exited with code !EXITCODE!
    pause
)
endlocal
"""

class OrbaseInstaller(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Orbase Installer")
        self.geometry("500x400")
        self.resizable(False, False)
        self.configure(bg=BG)
        try:
            self._icon = tk.PhotoImage(data=ICON_B64)
            self.iconphoto(True, self._icon)
        except Exception:
            pass
        self.orbs_path = tk.StringVar()
        self.frames = {}
        for F in (WelcomePage, FolderPage, InstallingPage, DonePage):
            frame = F(self)
            self.frames[F] = frame
            frame.place(relwidth=1, relheight=1)
        self.show(WelcomePage)

    def show(self, page):
        self.frames[page].tkraise()


class WelcomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="🪐", font=("Segoe UI", 48), bg=BG, fg=FG).pack(pady=(50, 10))
        tk.Label(self, text="Orbase", font=FONT_TITLE, bg=BG, fg=FG).pack()
        tk.Label(self, text="File Association System", font=FONT_SUB, bg=BG, fg="#888").pack(pady=(4, 30))
        tk.Label(self, text="This installer will set up .orb and .orun file types on your system.", font=FONT, bg=BG, fg=FG, wraplength=380, justify="center").pack(pady=(0, 10))
        tk.Label(self, text="Supported languages: batch, python, powershell, javascript,\nruby, perl, php, java, lua, go, rust, r", font=("Segoe UI", 9), bg=BG, fg="#555", justify="center").pack(pady=(0, 30))
        btn = tk.Button(self, text="Get Started →", font=FONT, bg=ACCENT, fg="white", bd=0, padx=20, pady=8, cursor="hand2", command=lambda: master.show(FolderPage))
        btn.pack()


class FolderPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Select Orbs Folder", font=FONT_TITLE, bg=BG, fg=FG).pack(pady=(50, 10))
        tk.Label(self, text="Choose the folder where your .orb files will be in.\nMake sure orBat.ico is inside it too.", font=FONT, bg=BG, fg="#888", justify="center").pack(pady=(0, 30))

        path_frame = tk.Frame(self, bg=BG)
        path_frame.pack(padx=40, fill="x")
        entry = tk.Entry(path_frame, textvariable=master.orbs_path, font=FONT, bg=BTN_BG, fg=FG, insertbackground=FG, bd=0, relief="flat")
        entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        tk.Button(path_frame, text="Browse", font=FONT, bg=ACCENT, fg="white", bd=0, padx=12, pady=6, cursor="hand2",
                  command=lambda: master.orbs_path.set(filedialog.askdirectory(title="Select Orbs Folder") or master.orbs_path.get())).pack(side="right")

        self.err = tk.Label(self, text="", font=FONT, bg=BG, fg="#e05555")
        self.err.pack(pady=(10, 0))

        tk.Button(self, text="Install →", font=FONT, bg=ACCENT, fg="white", bd=0, padx=20, pady=8, cursor="hand2",
                  command=lambda: self.proceed(master)).pack(pady=30)

    def proceed(self, master):
        path = master.orbs_path.get()
        if not path:
            self.err.config(text="Please select a folder.")
            return
        if not os.path.isfile(os.path.join(path, "orBat.ico")):
            self.err.config(text="orBat.ico not found in that folder. Please add it and try again.")
            return
        self.err.config(text="")
        master.show(InstallingPage)
        master.frames[InstallingPage].start(master)


class InstallingPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="Installing...", font=FONT_TITLE, bg=BG, fg=FG).pack(pady=(80, 20))
        self.progress = ttk.Progressbar(self, length=300, mode="determinate")
        self.progress.pack(pady=10)
        self.status = tk.Label(self, text="", font=FONT, bg=BG, fg="#888")
        self.status.pack(pady=10)

    def start(self, master):
        threading.Thread(target=self.install, args=(master,), daemon=True).start()

    def install(self, master):
        path = os.path.normpath(master.orbs_path.get())
        icon = os.path.join(path, "orBat.ico")
        runner = os.path.join(path, "orun_runner.bat")
        steps = [
            ("Getting started", lambda: self.reg_set(winreg.HKEY_CURRENT_USER, r"SOFTWARE\Orbase", "OrbsFolder", path)),
            ("Adding .orb file type...", lambda: self.setup_orb(icon)),
            ("Writing language runner...", lambda: self.write_runner(runner)),
            ("Registering .orun file type...", lambda: self.setup_orun(path, icon, runner)),
            ("Finishing up", self.clear_cache),
        ]
        for i, (msg, fn) in enumerate(steps):
            self.status.config(text=msg)
            self.progress["value"] = (i / len(steps)) * 100
            self.update_idletasks()
            try:
                fn()
            except Exception as e:
                self.status.config(text=f"Error: {e}")
                messagebox.showerror("Install Error", str(e))
                return
        self.progress["value"] = 100
        master.show(DonePage)

    def reg_set(self, hive, key, name, value):
        k = winreg.CreateKeyEx(hive, key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(k)

    def reg_default(self, key, value):
        k = winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, r"Software\Classes" + "\\" + key, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(k, "", 0, winreg.REG_SZ, value)
        winreg.CloseKey(k)

    def write_runner(self, runner_path):
        with open(runner_path, "w", newline="\r\n") as f:
            f.write(RUNNER_SCRIPT)

    def setup_orb(self, icon):
        self.reg_default(r".orb", "Orbfile")
        self.reg_default(r"Orbfile", "Orbfile")
        self.reg_default(r"Orbfile\DefaultIcon", icon)
        vscode = os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\Microsoft VS Code\Code.exe")
        cmd = f'"{vscode}" "%1"' if os.path.exists(vscode) else 'notepad.exe "%1"'
        self.reg_default(r"Orbfile\shell\open\command", cmd)

    def setup_orun(self, orbs_path, icon, runner):
        self.reg_default(r".orun", "Orunfile")
        self.reg_default(r"Orunfile", "Orunfile")
        self.reg_default(r"Orunfile\DefaultIcon", icon)
        self.reg_default(r"Orunfile\shell\open\command", f'cmd.exe /c ""{runner}" "%1""')

    def clear_cache(self):
        ctypes.windll.shell32.SHChangeNotify(0x08000000, 0x0000, None, None)  # SHCNE_ASSOCCHANGED


class DonePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        tk.Label(self, text="✓", font=("Segoe UI", 48), bg=BG, fg="#4caf50").pack(pady=(50, 10))
        tk.Label(self, text="Orbase Installed!", font=FONT_TITLE, bg=BG, fg=FG).pack()
        tk.Label(self, text="Place your .orb files in your Orbs folder\nand double click .orun files to run them.", font=FONT, bg=BG, fg="#888", justify="center").pack(pady=(10, 30))
        tk.Button(self, text="Finish", font=FONT, bg=ACCENT, fg="white", bd=0, padx=20, pady=8, cursor="hand2", command=master.destroy).pack()


if __name__ == "__main__":
    app = OrbaseInstaller()
    app.mainloop()
