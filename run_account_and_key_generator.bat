@echo off
setlocal

python "%~dp0run_account_and_key_generator.py" %*
exit /b %ERRORLEVEL%

