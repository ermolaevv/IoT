@echo off 

CALL run_env.bat
FOR /F %%i in (test_bot_tokens.txt) do (
    start python bots\main.py %%i
)

