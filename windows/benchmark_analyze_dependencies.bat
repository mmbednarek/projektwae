cd %~dp0..
python3 -m pip install virtualenv
python3 -m virtualenv .wae_venv3
CALL .wae_venv3\Scripts\activate.bat
pip install numpy
deactivate
