@echo off
echo Verificando e instalando pacotes do Python...

REM Verifica se o pip está instalado
pip --version >nul 2>nul
IF ERRORLEVEL 1 (
    echo pip não está instalado. Instale o Python com pip e tente novamente.
    exit /b 1
)

REM Atualiza pip para a versão mais recente
echo Atualizando pip...
python -m pip install --upgrade pip

REM Verifica cada pacote listado em requirements.txt
for /f "tokens=*" %%i in (requirements.txt) do (
    echo Verificando %%i...
    python -m pip show %%i >nul 2>nul
    IF ERRORLEVEL 1 (
        echo %%i não está instalado. Instalando...
        python -m pip install %%i
    ) ELSE (
        echo %%i já está instalado. Atualizando...
        python -m pip install --upgrade %%i
    )
)

echo Todos os pacotes foram verificados e instalados/atualizados conforme necessário.

REM Inicia o servidor Django em segundo plano
echo Iniciando o servidor Django...
start cmd /c "python manage.py runserver > server_output.txt"

REM Aguarda um breve momento para o servidor iniciar
timeout /t 5 /nobreak >nul

REM Lê a saída do servidor para capturar a URL
set "url="
for /f "tokens=*" %%l in (server_output.txt) do (
    echo %%l | find "Starting development server at" >nul
    if not errorlevel 1 (
        for /f "tokens=2" %%u in ("%%l") do set "url=%%u"
    )
)

REM Abre a URL do servidor no navegador
if defined url (
    echo Abrindo URL do servidor: %url%
    start %url%
) else (
    echo Não foi possível encontrar a URL do servidor.
)

pause
