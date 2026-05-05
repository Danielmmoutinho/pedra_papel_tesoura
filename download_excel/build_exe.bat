@echo off
:: Gera o executável .exe com PyInstaller
:: Execute este arquivo UMA VEZ para criar o .exe

echo === Instalando dependências ===
pip install -r requirements.txt

echo.
echo === Gerando executável ===
pyinstaller ^
    --onefile ^
    --noconsole ^
    --name "DownloadExcel" ^
    --add-data "config.json;." ^
    download_excel.py

echo.
echo === Pronto! Executável gerado em: dist\DownloadExcel.exe ===
echo Copie o dist\DownloadExcel.exe e o config.json para a mesma pasta.
pause
