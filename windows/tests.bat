setlocal
cd %~dp0..

del /Q logs\*

CALL .wae_venv\Scripts\activate.bat
set PYTHONPATH=%PYTHONPATH%;%~dp0..\..
python tests\test.py %1
deactivate
