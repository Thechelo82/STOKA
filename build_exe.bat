@echo off
REM ============================================================
REM  STOKA — generar STOKA.exe con PyInstaller (Windows)
REM  No hace falta Visual Studio. Sí hace falta Python SOLO
REM  en la máquina donde se genera el .exe.
REM ============================================================

cd /d "%~dp0"

echo [1/3] Instalando dependencias...
py -3 -m pip install -r requirements.txt
if errorlevel 1 (
    python -m pip install -r requirements.txt
)

echo [2/3] Generando icono...
py -3 tools\generate_logo.py
if errorlevel 1 (
    python tools\generate_logo.py
)

echo [3/3] Empaquetando con PyInstaller...
py -3 -m PyInstaller --noconfirm --onefile --windowed --name STOKA --icon assets\logo.ico --add-data "assets\logo.png;assets" --add-data "assets\logo.ico;assets" --hidden-import PIL._tkinter_finder main.py
if errorlevel 1 (
    python -m PyInstaller --noconfirm --onefile --windowed --name STOKA --icon assets\logo.ico --add-data "assets\logo.png;assets" --add-data "assets\logo.ico;assets" --hidden-import PIL._tkinter_finder main.py
)

echo.
echo Listo. El ejecutable está en: dist\STOKA.exe
pause
