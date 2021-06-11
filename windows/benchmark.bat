setlocal
cd %~dp0..
CALL .wae_venv\Scripts\activate.bat
set PYTHONPATH=%PYTHONPATH%;%~dp0..\..
python benchmarks\coco.py %1 %2
deactivate

