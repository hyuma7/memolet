import flet as ft
from ...services.memo_service import MemoService
from ..components.memo_card import MemoCard

class MemoView(ft.Column):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.memo_service = MemoService()
        self.isolated = True
        self.expand = True
        self.spacing = 20
        
        # 入力フィールドの初期化
        self.title_field = ft.TextField(
            label="タイトル",
            border_radius=10,
            text_size=16,
            expand=True
        )
        self.content_field = ft.TextField(
            label="メモの内容",
            multiline=True,
            min_lines=3,
            max_lines=3,
            border_radius=10,
            text_size=16,
            expand=True
        )
        self.project_path_field = ft.TextField(
            label="プロジェクトパス（オプション）",
            border_radius=10,
            text_size=16,
            expand=True,
            hint_text="例: C:\\Projects\\my-project"
        )
        self.command_field = ft.TextField(
            label="実行コマンド（オプション）",
            border_radius=10,
            text_size=16,
            expand=True,
            hint_text="例: npm run dev"
        )
        
        # レイアウトの設定
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.controls = [
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            f"ようこそ、{user.username}さん",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700
                        ),
                        ft.IconButton(
                            icon=ft.Icons.LOGOUT,
                            icon_color=ft.Colors.BLUE_700,
                            tooltip="ログアウト",
                            on_click=self.logout
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=1, color=ft.Colors.BLUE_100)
                ]),
                padding=ft.padding.only(left=20, right=20),
                width=800
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "新規メモ作成",
                        size=20,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.BLUE_700
                    ),
                    self.title_field,
                    self.content_field,
                    self.project_path_field,
                    self.command_field,
                    ft.Row([
                        ft.ElevatedButton(
                            "作成",
                            on_click=self.create_memo,
                            style=ft.ButtonStyle(
                                color=ft.Colors.WHITE,
                                bgcolor=ft.Colors.BLUE_700,
                                padding=ft.padding.all(15),
                                shape=ft.RoundedRectangleBorder(radius=10),
                            ),
                        )
                    ], alignment=ft.MainAxisAlignment.END)
                ], spacing=20),
                padding=20,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=15,
                width=800
            ),
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "メモ一覧",
                            size=20,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.BLUE_700
                        ),
                        ft.Column(
                            controls=self.get_memo_cards(),
                            spacing=10,
                            scroll=ft.ScrollMode.AUTO,
                            height=400
                        )
                    ],
                    spacing=20
                ),
                width=800,
                padding=20
            )
        ]

    def get_memo_cards(self):
        memos = self.memo_service.get_user_memos(self.user.id)
        return [MemoCard(memo, self.delete_memo, self.edit_memo) for memo in memos]

    def create_memo(self, e):
        if not self.title_field.value or not self.content_field.value:
            return

        if self.memo_service.create_memo(
            self.user.id,
            self.title_field.value,
            self.content_field.value,
            self.project_path_field.value or "",
            self.command_field.value or ""
        ):
            self.title_field.value = ""
            self.content_field.value = ""
            self.project_path_field.value = ""
            self.command_field.value = ""
            self.refresh_memos()

    def delete_memo(self, memo_id):
        if self.memo_service.delete_memo(memo_id, self.user.id):
            self.refresh_memos()

    def edit_memo(self, memo_id):
        memo = self.memo_service.get_memo(memo_id, self.user.id)
        if memo:
            self.title_field.value = memo.title
            self.content_field.value = memo.content
            self.project_path_field.value = memo.project_path
            self.command_field.value = memo.command
            self.update()

    def refresh_memos(self):
        memo_column = self.controls[-1].content.controls[-1]
        memo_column.controls = self.get_memo_cards()
        self.update()

    def logout(self, e):
        self.page.go("/login") 