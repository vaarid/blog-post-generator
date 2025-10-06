@echo off
chcp 65001 >nul
title Blog Post Generator - Update

if exist venv (
    call venv\Scripts\activate
) else (
    python -m venv venv
    call venv\Scripts\activate
)
pip install --upgrade pip
pip install -r requirements.txt
pause
