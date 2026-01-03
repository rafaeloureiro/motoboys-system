@echo off
echo ========================================
echo  Deploy do Sistema de Motoboys
echo ========================================
echo.

:: Verificar se Git esta instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERRO: Git nao esta instalado!
    echo Instale em: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Inicializando repositorio Git...
git init

echo.
echo [2/5] Adicionando arquivos...
git add .

echo.
echo [3/5] Fazendo commit...
git commit -m "Deploy inicial - Sistema de Motoboys 2026"

echo.
echo [4/5] Configure o remote do GitHub:
echo.
set /p GITHUB_USER="Digite seu usuario do GitHub: "
set /p REPO_NAME="Digite o nome do repositorio (default: sistema-motoboys): "

if "%REPO_NAME%"=="" set REPO_NAME=sistema-motoboys

echo.
echo [5/5] Enviando para GitHub...
git remote add origin https://github.com/%GITHUB_USER%/%REPO_NAME%.git
git branch -M main
git push -u origin main

echo.
echo ========================================
echo  Deploy concluido com sucesso!
echo ========================================
echo.
echo Proximo passo:
echo 1. Acesse: https://share.streamlit.io
echo 2. Conecte seu repositorio: %GITHUB_USER%/%REPO_NAME%
echo 3. Configure os secrets
echo.
pause
