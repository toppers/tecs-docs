# tecs-docs

TECS (TOPPERS Embedded Component System) の日本語リファレンスマニュアルを [Sphinx](https://www.sphinx-doc.org/) で生成するドキュメントリポジトリです。

対象システム:

- ASP3+TECS
- ATK2+TECS
- mruby-on-ev3rt+tecs
- mruby-on-gr-peach+tecs
- tinet+tecs
- tlsf+tecs

## セットアップ

Python は `>=3.9,<3.10` に固定されています（`.python-version` / `pyproject.toml`）。依存関係は `uv.lock` と `Pipfile.lock` のどちらでも管理されており、好きな方でセットアップできます。

```bash
# uv を使う場合
uv sync

# Pipenv を使う場合
pipenv install
pipenv shell
```

## ビルド方法

すべて `docs/` ディレクトリ内で実行します。

```bash
cd docs

# HTML ビルド
make html

# ライブプレビュー（ファイル変更を監視して自動ビルド）
make livehtml

# PDF ビルド（platex が必要）
make latexpdfja
```

出力先: `docs/_build/html/`（PDF は `docs/_build/latex/`）。

### Windows でのビルド

Windows では GNU `make` が使えないため、代わりに以下のスクリプトを使います。

- リポジトリルートの `make.bat` / `make.ps1`: `docs/` へ移動して `html` と `latexpdfja` のビルドを実行するラッパー。
- `docs/make.ps1`: `make.bat` 相当の PowerShell 版。`uv` があれば自動的に `uv run sphinx-build` を使用する。
- `docs/makex.bat`: `html` / `latexpdfja` 専用のビルドスクリプト。Sphinx が生成する `_build/latex/make.bat` は Unix 系コマンドに依存し素の Windows では実行できないため、代わりに `platex → upmendex（または mendex）→ platex → dvipdfmx` のパイプラインを直接実行する。

```powershell
# リポジトリルートから
.\make.bat
```

## ドキュメント構造

```
docs/
├── conf.py              # Sphinx 設定（言語: ja_jp、テーマ: sphinx_rtd_theme）
├── index.rst            # ルート toctree
├── _extensions/
│   ├── tecs.py          # TECS CDL Sphinx ドメイン
│   └── tecslexer.py     # TECS CDL Pygments レクサー
├── _static/style.css    # カスタム CSS（no-alt-color クラス等）
├── tecs/                # TECS リファレンス（CDL仕様、コマンド、プラグイン等）
├── asp3/                # ASP3+TECS カーネル API
├── atk2+tecs/           # ATK2+TECS
├── mruby-on-ev3rt+tecs/ # mruby EV3RT バインディング
├── mruby-on-gr-peach+tecs/
├── tinet+tecs/          # TINET+TECS
└── tlsf+tecs/           # TLSF+TECS
```

## TECS 固有マークアップ

### シンタックスハイライト

`tecs-cdl` を言語として指定すると TECS CDL のハイライトが適用されます。

```rst
.. code-block:: tecs-cdl

   celltype tTask { ... };
```

### TECS ドメインディレクティブ

`conf.py` で `primary_domain = 'tecs'`、`default_role = 'any'` に設定されているため、ドメイン省略で参照できます。

```rst
.. tecs:celltype:: nNamespace::tCellTypeName

   .. tecs:attr:: Type attributeName
   .. tecs:var:: Type variableName
   .. tecs:entry:: sSignature eEntryPortName
   .. tecs:call:: sSignature cCallPortName

.. tecs:signature:: sSignatureName

   .. tecs:sigfunction:: ReturnType functionName(int param)
```

クロスリファレンス:

```rst
:tecs:attr:`tCellTypeName::attributeName`   # フルネーム表示
:tecs:attr:`~tCellTypeName::attributeName`  # 末尾要素のみ表示
```

### 日本語インラインマークアップ

分かち書きなし言語では両側バックスラッシュでスペースをエスケープします。

```rst
使用方法として\ :ref:`タスクを通知先とする場合 <label>`\ を例として…
```

### 表の縞模様を無効化

```rst
.. rst-class:: no-alt-color

+---------+---------+
| column1 | column2 |
+=========+=========+
```

## Read the Docs

`.readthedocs.yaml` が `docs/conf.py` を Sphinx 設定として参照し、依存関係はルートの `requirements.txt`（`uv.lock` / `Pipfile.lock` とは別管理）からインストールされます。依存関係を追加した場合は `requirements.txt` も合わせて更新してください。
