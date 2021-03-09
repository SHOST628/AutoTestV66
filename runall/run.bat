@echo off
set root=%~dp0
set run_path=%root%run.py
call %root%..\venv\Scripts\activate.bat
python %run_path%
rem notice that you have to set  the value of VIRTUAL_ENV  on env/Scripts/activate.bat to %~dp0..  or the root path of env if you want to move env to other machine
rem the best mehtod is to set the value of VIRTUAL_ENV  on env/Scripts/activate.bat to %~dp0.. if  you want to move env to other machine