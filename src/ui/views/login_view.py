import flet as ft
from ...services.user_service import UserService

class LoginView(ft.Column):
    def __init__(self, on_login_success):
        super().__init__()
        self.user_service = UserService()
        self.on_login_success = on_login_success
        self.isolated = True
        self.expand = True
        
        # コントロールの初期化
        self.username_field = ft.TextField(
            label="ユーザー名",
            width=300,
            border_radius=10,
            text_size=16
        )
        self.password_field = ft.TextField(
            label="パスワード",
            password=True,
            width=300,
            border_radius=10,
            text_size=16
        )
        self.message = ft.Text("", color="red", size=14)
        
        # レイアウトの設定
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.vertical_alignment = ft.MainAxisAlignment.CENTER
        self.spacing = 20
        
        self.controls = [
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "memolet",
                            size=40,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700
                        ),
                        ft.Text(
                            "ログインまたは新規登録",
                            size=16,
                            color=ft.Colors.BLUE_700
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5
                ),
                margin=ft.margin.only(bottom=30)
            ),
            self.username_field,
            self.password_field,
            self.message,
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "ログイン",
                        on_click=self.login,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                            padding=ft.padding.all(15),
                            shape=ft.RoundedRectangleBorder(radius=10),
                        ),
                        width=140
                    ),
                    ft.ElevatedButton(
                        "新規登録",
                        on_click=self.register,
                        style=ft.ButtonStyle(
                            color=ft.Colors.BLUE_700,
                            bgcolor=ft.Colors.WHITE,
                            padding=ft.padding.all(15),
                            shape=ft.RoundedRectangleBorder(radius=10),
                            side=ft.BorderSide(1, ft.Colors.BLUE_700),
                        ),
                        width=140
                    ),
                ],
                spacing=20,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ]

    def login(self, e):
        user = self.user_service.authenticate_user(
            self.username_field.value,
            self.password_field.value
        )
        if user:
            self.on_login_success(user)
        else:
            self.message.value = "ユーザー名またはパスワードが間違っています"
            self.update()

    def register(self, e):
        if not self.username_field.value or not self.password_field.value:
            self.message.value = "ユーザー名とパスワードを入力してください"
            self.update()
            return

        if self.user_service.register_user(
            self.username_field.value,
            self.password_field.value
        ):
            self.message.value = "登録が完了しました。ログインしてください。"
        else:
            self.message.value = "このユーザー名は既に使用されています"
        self.update() 