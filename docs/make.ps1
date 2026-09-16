<#
.SYNOPSIS
    Sphinx documentation build script for PowerShell.
#>

# スクリプトがあるディレクトリに移動（pushd %~dp0 の代わり）
Push-Location $PSScriptRoot

# Strawberry Perl や Git Perl を PATH に追加（LaTeX/PDF ビルド用）
$perlPaths = @(
    "C:\Strawberry\perl\bin",
    "C:\Users\ykomi\AppData\Local\Programs\StrawberryPerl\perl\bin",
    "C:\Program Files\Git\usr\bin"
)
foreach ($p in $perlPaths) {
    if ((Test-Path $p) -and ($env:PATH -notlike "*$p*")) {
        $env:PATH = "$p;$env:PATH"
    }
}

# SPHINXBUILD の決定
$sphinxBuild = $env:SPHINXBUILD
if ([string]::IsNullOrEmpty($sphinxBuild)) {
    if (Get-Command uv -ErrorAction SilentlyContinue) {
        $sphinxBuild = "uv run sphinx-build"
    } else {
        $sphinxBuild = "sphinx-build"
    }
} elseif ($sphinxBuild -eq "sphinx-build" -and -not (Get-Command sphinx-build -ErrorAction SilentlyContinue) -and (Get-Command uv -ErrorAction SilentlyContinue)) {
    $sphinxBuild = "uv run sphinx-build"
}

$SOURCEDIR = "."
$BUILDDIR = "_build"

# コマンドと引数の分割
$cmdParts = $sphinxBuild -split " "
$cmd = $cmdParts[0]
$cmdPrefixArgs = if ($cmdParts.Length -gt 1) { $cmdParts[1..($cmdParts.Length - 1)] } else { @() }

# コマンドが存在するかチェック
if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
    Write-Host ""
    Write-Host "The '$cmd' command was not found. Make sure you have Sphinx or uv"
    Write-Host "installed, then set the SPHINXBUILD environment variable to point"
    Write-Host "to the full path of the executable. Alternatively you"
    Write-Host "may add the directory to PATH."
    Write-Host ""
    Write-Host "If you don't have Sphinx installed, grab it from"
    Write-Host "http://sphinx-doc.org/"
    
    Pop-Location
    exit 1
}

# 引数（ターゲット）がない場合はヘルプを表示
if ($args.Count -eq 0) {
    $helpArgs = @()
    if ($cmdPrefixArgs.Length -gt 0) { $helpArgs += $cmdPrefixArgs }
    $helpArgs += @("-M", "help", $SOURCEDIR, $BUILDDIR)
    if ($env:SPHINXOPTS) { $helpArgs += $env:SPHINXOPTS -split " " }

    & $cmd @helpArgs
    Pop-Location
    exit 0
}

$target = $args[0]

# pdf / latexpdfja / latexpdf の特別処理
if ($target -in @("pdf", "latexpdfja", "latexpdf")) {
    $sphinxArgs = @()
    if ($cmdPrefixArgs.Length -gt 0) { $sphinxArgs += $cmdPrefixArgs }
    $sphinxArgs += @("-M", "latex", $SOURCEDIR, $BUILDDIR)
    if ($env:SPHINXOPTS) { $sphinxArgs += $env:SPHINXOPTS -split " " }

    & $cmd @sphinxArgs
    if ($LASTEXITCODE -ne 0) {
        Pop-Location
        exit $LASTEXITCODE
    }

    $latexDir = Join-Path $BUILDDIR "latex"
    if (Test-Path $latexDir) {
        Push-Location $latexDir
        
        $latexmkPl = (Get-ChildItem -Path "C:\Users\ykomi\AppData\Local\Programs\MiKTeX\scripts\latexmk\latexmk.pl", "C:\Program Files\MiKTeX\scripts\latexmk\latexmk.pl" -ErrorAction SilentlyContinue | Select-Object -First 1)?.FullName
        $perlExe = (Get-Command perl -ErrorAction SilentlyContinue)?.Source
        if (-not $perlExe) {
            $perlExe = "C:\Strawberry\perl\bin\perl.exe"
        }

        if ($perlExe -and (Test-Path $perlExe) -and $latexmkPl -and (Test-Path $latexmkPl)) {
            Write-Host "Compiling LaTeX to PDF with latexmk.pl..."
            & $perlExe $latexmkPl -r latexmkjarc -pdfdvi -dvi- -ps- -interaction=nonstopmode TECS.tex
        } else {
            Write-Host "Compiling LaTeX to PDF with uplatex & dvipdfmx..."
            & uplatex -kanji=utf8 -interaction=nonstopmode TECS.tex
            & uplatex -kanji=utf8 -interaction=nonstopmode TECS.tex
            & dvipdfmx TECS.dvi
        }
        Pop-Location
    }
} else {
    $sphinxArgs = @()
    if ($cmdPrefixArgs.Length -gt 0) { $sphinxArgs += $cmdPrefixArgs }
    $sphinxArgs += @("-M", $target, $SOURCEDIR, $BUILDDIR)
    if ($env:SPHINXOPTS) {
        $sphinxArgs += $env:SPHINXOPTS -split " "
    }

    & $cmd @sphinxArgs
}

# 元のディレクトリに戻る（popd の代わり）
Pop-Location