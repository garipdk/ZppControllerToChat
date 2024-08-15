@ECHO OFF
SET mypath0=%~dp0
SET mypath=%mypath0:~0,-1%
ECHO %mypath%
%mypath%\python-3.10.0-embed-amd64\python.exe %mypath%\src\zppControllerToChat.py
PAUSE