@echo off
rem Double-click to open the root manifest review app.
rem Uses the Python in ME295_PYTHON if set, else the me295 conda env, else python on PATH.
cd /d "%~dp0..\.."
start "" http://localhost:8295
if defined ME295_PYTHON (
  "%ME295_PYTHON%" scripts\manifest\review_server.py
) else (
  where conda >nul 2>nul && (
    conda run --no-capture-output -n me295 python scripts\manifest\review_server.py
  ) || (
    python scripts\manifest\review_server.py
  )
)
