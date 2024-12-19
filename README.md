# memolet

このmemoletは、Fletで開発されました。コード管理ツールです。

![image](https://github.com/user-attachments/assets/e11219bc-09c3-4175-9b79-a4350b98c669)

![image](https://github.com/user-attachments/assets/12af8618-7124-4af9-8d07-4b6532195748)

![image](https://github.com/user-attachments/assets/2f70acba-dd01-4d62-8b98-b6d88117efe1)


## 特徴

- **ログイン機能**: ユーザーはアカウントを作成し、ログインすることができます。
- **シンプルなUI**: 使いやすいインターフェースで、直感的に操作できます。
- **開発環境の即時起動**: メモに記録したプロジェクトパスとコマンドで、ワンクリックで開発環境を起動できます。
  - 関連するコマンド（code .など）を実行を指定すると、そのコマンドを実行してくれます。

## 使用方法

1 ログイン
2 メモに記録したプロジェクトパスとコマンドで、ワンクリックで開発環境を起動できます。


## Fletのインストール方法

### 開発環境構築 & 基礎準備

#### Windows

1. Python 3.13.0をダウンロードしてインストールします。
    - 公式サイトからPython 3.13.0をダウンロード: https://www.python.org/downloads/release/python-3130/
    - インストール時に「Add Python to PATH」にチェックを入れる。

#### 仮想環境の設定

1. インストールしたPython 3.13.0のパスを確認します。例: `C:\Python313\python.exe`
2. 以下のコマンドで仮想環境を作成します。 `C:\Python313\python.exe -m venv venv`
3. 仮想環境を有効化します。 `venv\Scripts\activate`

#### 複数バージョンのPythonがインストールされている場合

1. 使用したいPythonのバージョンを指定して仮想環境を作成します。例: Python 3.13を使用する場合 `py -3.13 -m venv venv`

#### Mac

1. Python 3.13.0をインストールします。
    - 公式サイトからPython 3.13.0のインストーラーをダウンロード: https://www.python.org/downloads/release/python-3130/
    - またはHomebrewを使用してインストール: `brew install python@3.13`

#### 仮想環境の設定

1. Python 3.13.0のパスを確認します。 `which python3.13`
2. 仮想環境を作成します。 `/usr/local/bin/python3.13 -m venv venv`
3. 仮想環境を有効化します。 `source venv/bin/activate`

#### 補足

既存のPythonが別バージョンでも3.13.0を使いたい場合
- WindowsではインストールしたPythonのパスを直接指定する方法が確実です。
- Macではbrewを使う場合、以下のようにバージョンを指定できます: `brew link --overwrite python@3.13` これで、確実にPython 3.13.0の仮想環境を作成できます！
