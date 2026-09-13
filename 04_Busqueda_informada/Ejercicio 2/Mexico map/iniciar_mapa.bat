@echo off
REM Doble clic en este archivo: entra a la carpeta donde esta el .bat
REM y corre run_map.py, que levanta el servidor y abre el navegador.

cd /d "%~dp0"
python run_map.py

REM Deja la ventana abierta si algo falla, para poder leer el error.
pause
