@echo off
rem Arranca SABIA (sitio + asistente) en http://127.0.0.1:8800/
title SABIA
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0rag\iniciar.ps1"
pause
