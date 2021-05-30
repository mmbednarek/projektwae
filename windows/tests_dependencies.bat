cd %~dp0..
python -m pip install virtualenv
python -m virtualenv .wae_venv
CALL .wae_venv\Scripts\activate.bat
pip install numpy
deactivate
