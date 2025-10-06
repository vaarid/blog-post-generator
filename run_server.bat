@echo off
chcp 65001 >nul
title Blog Post Generator - FastAPI Server

echo ============================================
echo   🚀 Запуск Blog Post Generator API
echo ============================================

:: === Проверка и создание папки logs ===
if not exist logs (
    mkdir logs
    echo [INFO] Папка logs создана.
)

set SERVER_LOG=logs\server.log
set ERROR_LOG=logs\errors.log

echo [START] %date% %time% >> %SERVER_LOG%

:: === Проверка и активация виртуального окружения ===
if exist venv (
    echo [INFO] Активация окружения... >> %SERVER_LOG%
    call venv\Scripts\activate
) else (
    echo [INFO] Создание окружения... >> %SERVER_LOG%
    python -m venv venv
    call venv\Scripts\activate
)

:: === Безопасное обновление pip через python -m pip ===
echo [INFO] Обновление pip... >> %SERVER_LOG%
python -m pip install --upgrade pip >> %SERVER_LOG% 2>> %ERROR_LOG%

:: === Установка зависимостей ===
echo [INFO] Установка зависимостей... >> %SERVER_LOG%
pip install -r requirements.txt >> %SERVER_LOG% 2>> %ERROR_LOG%

:: === Проверка наличия .env ===
if not exist .env (
    echo [WARNING] Файл .env не найден! >> %ERROR_LOG%
)

:: === Запуск FastAPI-сервера ===
echo [INFO] Запуск приложения... >> %SERVER_LOG%
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload >> %SERVER_LOG% 2>> %ERROR_LOG%

echo [STOP] %date% %time% >> %SERVER_LOG%
pause
