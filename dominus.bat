@echo off
where python3 >nul 2>nul
IF %ERRORLEVEL% EQU 0 (
    SET PYTHON_CMD=python3
) ELSE (
    SET PYTHON_CMD=python
)

%PYTHON_CMD% -m pip install -q -r .\requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo pip install failed. Exiting.
    exit /b %ERRORLEVEL%
)

%PYTHON_CMD% .\dominus_cli\run.py