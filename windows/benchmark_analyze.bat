cd %~dp0..
CALL .wae_venv3\Scripts\Activate
python3 -m cocopp exdata\classic-benchmark-output exdata\dg-benchmark-output
deactivate
