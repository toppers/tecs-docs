@ECHO OFF

REM makex.bat - build helper for html and latexpdfja targets.
REM
REM make.bat's latexpdfja target relies on Sphinx invoking an external
REM make(.bat) inside _build\latex, which does not exist as a runnable
REM command on plain Windows. This script instead runs the
REM platex -> upmendex(index) -> platex -> dvipdfmx pipeline directly.

setlocal
pushd %~dp0

set PROJECT_ROOT=%~dp0..

where uv >NUL 2>NUL
if errorlevel 1 goto skip_uv_sync
uv sync --project "%PROJECT_ROOT%"
if errorlevel 1 (
	echo.
	echo.uv sync failed. Aborting.
	goto end
)
:skip_uv_sync

if "%SPHINXBUILD%" == "" goto detect_sphinxbuild
where %SPHINXBUILD% >NUL 2>NUL
if not errorlevel 1 goto have_sphinxbuild
:detect_sphinxbuild
where sphinx-build >NUL 2>NUL
if errorlevel 1 goto use_uv_sphinxbuild
set SPHINXBUILD=sphinx-build
goto have_sphinxbuild
:use_uv_sphinxbuild
set SPHINXBUILD=uv run --project "%PROJECT_ROOT%" sphinx-build
:have_sphinxbuild

set SOURCEDIR=.
set BUILDDIR=_build
set LATEXDIR=%BUILDDIR%\latex

if "%1" == "" goto help
if /I "%1" == "html" goto html
if /I "%1" == "latexpdfja" goto latexpdfja
goto help

:html
%SPHINXBUILD% -M html %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
if errorlevel 1 goto end
echo.
echo.The HTML pages are in %BUILDDIR%\html.
goto end

:latexpdfja
%SPHINXBUILD% -M latex %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
if errorlevel 1 goto end

if not exist "%LATEXDIR%" (
	echo.
	echo.%LATEXDIR% not found. LaTeX sources were not generated.
	goto end
)

pushd "%LATEXDIR%"

for %%f in (*.png *.gif *.jpg *.jpeg) do (
	if exist "%%f" extractbb "%%f"
)

for %%f in (*.tex) do platex -kanji=utf8 -interaction=nonstopmode "%%f"
for %%f in (*.tex) do platex -kanji=utf8 -interaction=nonstopmode "%%f"
for %%f in (*.tex) do platex -kanji=utf8 -interaction=nonstopmode "%%f"

where mendex >NUL 2>NUL
if errorlevel 1 goto use_upmendex
for %%f in (*.idx) do mendex -f -d "%%~nf.dic" -s python.ist "%%f"
goto index_done
:use_upmendex
for %%f in (*.idx) do upmendex -f -d "%%~nf.dic" -s python.ist "%%f"
:index_done

for %%f in (*.tex) do platex -kanji=utf8 -interaction=nonstopmode "%%f"
for %%f in (*.tex) do platex -kanji=utf8 -interaction=nonstopmode "%%f"

for %%f in (*.dvi) do dvipdfmx "%%f"

popd

echo.
echo.The PDF files are in %LATEXDIR%.
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS%
echo.
echo.Usage: makex.bat html ^| latexpdfja

:end
popd
endlocal
