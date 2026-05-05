@echo off
:: Registra o DownloadExcel.exe no Agendador de Tarefas do Windows
:: para rodar automaticamente todo dia ao fazer login.
:: Execute como ADMINISTRADOR.

set NOME_TAREFA=DownloadExcelDiario
set EXE_PATH=%~dp0dist\DownloadExcel.exe

echo === Registrando tarefa no Agendador de Tarefas ===
echo Executável: %EXE_PATH%
echo.

schtasks /Create ^
    /TN "%NOME_TAREFA%" ^
    /TR "\"%EXE_PATH%\"" ^
    /SC ONLOGON ^
    /DELAY 0001:00 ^
    /RL HIGHEST ^
    /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo === Tarefa "%NOME_TAREFA%" criada com sucesso! ===
    echo O Excel será baixado automaticamente 1 minuto após cada login.
) else (
    echo.
    echo ERRO ao criar tarefa. Execute este .bat como Administrador.
)

pause
