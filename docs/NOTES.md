# Fletアプリケーション開発の注意点

## 非推奨API対応

### ウィンドウサイズ設定
```python
# 非推奨
page.window_width = 800
page.window_height = 600

# 推奨
page.window.width = 800
page.window.height = 600
```

### カスタムコントロール
```python
# 非推奨
class MyView(ft.UserControl):
    pass

# 推奨
class MyView(ft.Control):
    def _get_control_name(self):
        # 返すべき値は、buildメソッドで返すコントロールの種類に応じて変更
        return "container"  # ft.Containerを返す場合
        # return "column"   # ft.Columnを返す場合
        # return "row"      # ft.Rowを返す場合
```

### 色の指定
```python
# 非推奨
ft.Colors.WHITE
ft.Colors.with_opacity(0.1, ft.Colors.WHITE)  # この形式はまだ使用可能

# 推奨（ただし現在は問題あり）
ft.Colors.WHITE
ft.Colors.WHITE.with_opacity(0.1)  # この形式は現在バグがあるため使用不可
```

### コンテナの画像設定
```python
# 非推奨
ft.Container(
    image_src="path/to/image.png",
    image_fit=ft.ImageFit.COVER
)

# 推奨
ft.Container(
    image=ft.Image(
        src="path/to/image.png",
        fit=ft.ImageFit.COVER
    )
)
```

### イベントハンドラ
```python
# 非推奨（二回クリックが必要）
ft.TextButton("編集", on_click=lambda e: on_edit(memo.id))

# 推奨（一回クリックで反応）
def edit_memo(self, e):
    self.on_edit(self.memo.id)

ft.TextButton("編集", on_click=self.edit_memo)
```

### アイコンの指定
```python
# 非推奨
ft.icons.EDIT

# 推奨
ft.Icons.EDIT
```

### ウィンドウサイズの設定
```python
# 非推奨
page.window_width = 1000
page.window_height = 800

# 推奨
page.window.width = 1000
page.window.height = 800
```

### データベース接続
```python
# 非推奨（スレッドセーフでない）
class DatabaseConnection:
    def __init__(self):
        self.connection = sqlite3.connect("memos.db")

# 推奨（スレッドセーフ）
class DatabaseConnection:
    _thread_local = local()

    @classmethod
    def get_connection(cls):
        if not hasattr(cls._thread_local, "connection"):
            cls._thread_local.connection = sqlite3.connect("memos.db")
        return cls._thread_local.connection
```

### テスト
```python
# 推奨プラクティス
- 機能実装前にテストを書く（TDD）
- データベース操作を含むテストは独立した環境で実行
- セットアップとクリーンアップを適切に行う
- 境界値や異常系のテストも含める
```

## バージョン情報
- Flet 0.25.0以降では`colors`は`Colors`に変更（ただし`with_opacity`は古い形式を使用）
- Flet 0.24.0以降では`Container`の画像関連プロパティが変更
- Flet 0.23.0以降では`window_width`/`window_height`が`window.width`/`window.height`に変更
- Flet 0.21.0以降では`UserControl`が`Control`に変更

## 既知の問題
- `Colors.with_opacity()`メソッドには現在バグがあり、代わりに`colors.with_opacity(opacity, color)`を使用する必要がある
- 画像パスは相対パスではなく、絶対パスを使用することを推奨
- `Control`クラスを継承する場合は、`_get_control_name`メソッドを必ず実装する必要がある。返す値は`build`メソッドで返すコントロールの種類に応じて変更する

UserControlをControlに変更しました。
Controlを継承することで、buildメソッドをオーバーライドしてUIを構築します。

LoginViewの実装を更新：
- UserControlは非推奨（deprecated）となったため、ft.Columnを継承する形に変更
- 複合カスタムコントロール（Composite Control）として実装
- self.isolated = Trueを設定し、独立したコントロールとして動作するように変更
  - これにより、self.update()を使用する際の適切な更新処理を実現
- UIの構造はColumnを直接継承することでシンプルに

colorsはwarningが出るので使わず、Colorsを使用すること

### テストデータベース
```python
# 非推奨（本番DBを使用）
def setUp(self):
    self.conn = DatabaseConnection.get_connection()

# 推奨（テスト用の別DBを使用）
@classmethod
def setUpClass(cls):
    cls.test_db_path = "test_memos.db"
    # テストDB作成とテーブル設定

def setUp(self):
    DatabaseConnection._thread_local.connection = sqlite3.connect(self.test_db_path)
```