import flet as ft
from ...services.memo_service import MemoService
from ..components.memo_card import MemoCard

class CommandInput(ft.Container):
    def __init__(self, on_delete=None):
        super().__init__()
        self.name_field = ft.TextField(
            label="コマンド名",
            border_radius=10,
            text_size=16,
            expand=True,
            height=40
        )
        self.command_field = ft.TextField(
            label="実行コマンド",
            border_radius=10,
            text_size=16,
            expand=True,
            height=40
        )
        self.delete_button = ft.IconButton(
            icon=ft.Icons.DELETE_OUTLINE,
            icon_color=ft.Colors.RED_700,
            tooltip="削除",
            on_click=lambda _: on_delete(self) if on_delete else None,
            visible=bool(on_delete)
        )
        
        self.content = ft.Row(
            controls=[
                self.name_field,
                self.command_field,
                self.delete_button
            ],
            spacing=10
        )
        self.padding = ft.padding.only(bottom=10)

    def get_command(self):
        return {
            'name': self.name_field.value,
            'command': self.command_field.value
        }

    def set_command(self, name: str, command: str):
        self.name_field.value = name
        self.command_field.value = command

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
        
        # コマンド入力フィールドのコンテナ
        self.commands_container = ft.Column(spacing=0)
        self.commands_container.controls.append(CommandInput())
        
        # メモ作成フォーム
        self.memo_form = ft.Container(
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
                ft.Column([
                    ft.Text(
                        "実行コマンド（オプション）",
                        size=16,
                        weight=ft.FontWeight.W_500,
                        color=ft.Colors.BLUE_700
                    ),
                    self.commands_container,
                    ft.TextButton(
                        "コマンドを追加",
                        icon=ft.Icons.ADD,
                        on_click=self.add_command_input
                    )
                ]),
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
        )
        
        # メモ一覧
        self.memo_list = ft.Container(
            content=ft.Column(
                controls=self.get_memo_cards(),
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
            ),
            expand=True,
            padding=10
        )
        
        # タブの設定
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="新規作成",
                    icon=ft.Icons.CREATE,
                    content=self.memo_form
                ),
                ft.Tab(
                    text="メモ一覧",
                    icon=ft.Icons.LIST_ALT,
                    content=self.memo_list
                ),
            ],
            expand=True
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
                content=self.tabs,
                width=800,
                expand=True
            )
        ]

    def add_command_input(self, e=None):
        self.commands_container.controls.append(
            CommandInput(on_delete=self.remove_command_input)
        )
        if self.page:  # ページに追加された後のみ更新
            self.update()

    def remove_command_input(self, command_input):
        if command_input in self.commands_container.controls:
            self.commands_container.controls.remove(command_input)
            if not self.commands_container.controls:
                self.commands_container.controls.append(CommandInput())
            self.update()

    def get_memo_cards(self):
        memos = self.memo_service.get_user_memos(self.user.id)
        return [MemoCard(memo, self.delete_memo, self.edit_memo) for memo in memos]

    def create_memo(self, e):
        if not self.title_field.value or not self.content_field.value:
            return

        # コマンドの収集
        commands = []
        for cmd_input in self.commands_container.controls:
            if cmd_input.name_field.value and cmd_input.command_field.value:
                commands.append(cmd_input.get_command())

        if self.memo_service.create_memo(
            self.user.id,
            self.title_field.value,
            self.content_field.value,
            self.project_path_field.value or "",
            commands
        ):
            self.title_field.value = ""
            self.content_field.value = ""
            self.project_path_field.value = ""
            self.commands_container.controls = [CommandInput()]
            self.refresh_memos()
            # メモ作成後にメモ一覧タブに切り替え
            self.tabs.selected_index = 1
            self.update()

    def delete_memo(self, memo_id):
        if self.memo_service.delete_memo(memo_id, self.user.id):
            self.refresh_memos()

    def edit_memo(self, memo_id):
        memo = self.memo_service.get_memo(memo_id, self.user.id)
        if memo:
            self.title_field.value = memo.title
            self.content_field.value = memo.content
            self.project_path_field.value = memo.project_path
            
            # コマンドの設定
            self.commands_container.controls = []
            if memo.commands:
                for cmd in memo.commands:
                    command_input = CommandInput(on_delete=self.remove_command_input)
                    command_input.set_command(cmd.name, cmd.command)
                    self.commands_container.controls.append(command_input)
            else:
                self.commands_container.controls.append(CommandInput())
            
            # 編集時は新規作成タブに切り替え
            self.tabs.selected_index = 0
            self.update()

    def refresh_memos(self):
        self.memo_list.content.controls = self.get_memo_cards()
        self.update()

    def logout(self, e):
        self.page.client_storage.remove("user_id")
        self.page.go("/") 