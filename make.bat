@ECHO OFF

REM make.bat - top-level build script.
REM Moves into docs\ and runs makex.bat for the html and latexpdfja targets.

setlocal
pushd %~dp0

cd docs

call makex.bat html
if errorlevel 1 goto end

call makex.bat latexpdfja
if errorlevel 1 goto end

:end
popd
endlocal
