<#
.SYNOPSIS
    Sphinx documentation build script for PowerShell.
#>

# スクリプトがあるディレクトリに移動（pushd %~dp0 の代わり）
Push-Location $PSScriptRoot

# 環境変数や変数の初期設定
if ([string]::IsNullOrEmpty($env:SPHINXBUILD)) {
    # $env:SPHINXBUILD = "uv run sphinx-build"
    $env:SPHINXBUILD = "sphinx-build"
}
$SOURCEDIR = "."
$BUILDDIR = "_build"

# 引数（ターゲット）がない場合はヘルプを表示
if ($args.Count -eq 0) {
    & $env:SPHINXBUILD -M help $SOURCEDIR $BUILDDIR $env:SPHINXOPTS
    Pop-Location
    exit 0
}

$target = $args[0]

# 'sphinx-build' コマンドが存在するかチェック（errorlevel 9009 の代わり）
if (-not (Get-Command $env:SPHINXBUILD -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "The '$env:SPHINXBUILD' command was not found. Make sure you have Sphinx"
    Write-Host "installed, then set the SPHINXBUILD environment variable to point"
    Write-Host "to the full path of the '$env:SPHINXBUILD' executable. Alternatively you"
    Write-Host "may add the Sphinx directory to PATH."
    Write-Host ""
    Write-Host "If you don't have Sphinx installed, grab it from"
    Write-Host "http://sphinx-doc.org/"
    
    Pop-Location
    exit 1
}

# Sphinxビルドの実行
# $env:SPHINXOPTS が未定義でもエラーにならないよう、配列として引数を渡す
$sphinxArgs = @("-M", $target, $SOURCEDIR, $BUILDDIR)
if ($env:SPHINXOPTS) {
    $sphinxArgs += $env:SPHINXOPTS -split " "
}

& $env:SPHINXBUILD $sphinxArgs

# 元のディレクトリに戻る（popd の代わり）
Pop-Location