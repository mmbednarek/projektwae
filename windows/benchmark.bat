setlocal
cd %~dp0..
\.wae_venv\Scripts\Activate
set PYTHONPATH=%PYTHONPATH%;%~dp0..\..
python benchmarks\coco.py %1

