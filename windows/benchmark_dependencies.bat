IF %1.==. GOTO No1

CALL .wae_venv\Scripts\activate.bat
python -m easy_install %1
deactivate
GOTO End1

:No1
    ECHO "No first param. Provide location of .egg file generate by compiling coco framework"
:End1