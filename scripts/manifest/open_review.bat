@echo off
rem Double-click to open the root manifest review app.
cd /d "%~dp0..\.."
start "" http://localhost:8295
"D:\miniforge3\envs\me295\python.exe" scripts\manifest\review_server.py
