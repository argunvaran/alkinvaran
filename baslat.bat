@echo off
title Alkin Varan Website Sunucusu
color 0A

echo ==============================================================================
echo                      ALKIN VARAN - WEBSITE YONETIM SISTEMI
echo ==============================================================================
echo [BILGI] Sisteme baslatiliyor. Lutfen isiniz bitene kadar bu pencereyi kapatmayin...
echo.

:: Dosyanin bulundugu dizine gec
cd /d "%~dp0"

:: Tarayiciyi baslat
echo [*] Tarayici panel icin aciliyor... (http://localhost:8000)
timeout /t 2 /nobreak > nul
start http://localhost:8000
echo.

:: Django Development Server calistirma
echo [*] Django yerel sunucusu ayaga kaldiriliyor...
echo.
echo ==============================================================================
echo   Sunucuyu durdurmak icin klavyeden CTRL + C tuslarina basabilirsiniz.
echo ==============================================================================

:: Sisteminizde Django zaten global olarak kurulu (Sanal ortam ici bos), o yuzden direkt ana python ile baslatiyoruz:
python manage.py runserver

:: Eger hata verirse kapanmasin, hatayi gorebilelim:
pause
