import flet as ft
from src.ui.views.login_view import LoginView
from src.ui.views.memo_view import MemoView

def main(page: ft.Page):
    page.title = "memolet"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1000
    page.window.height = 800
    page.padding = 0
    
    def route_change(e):
        page.clean()
        if page.route == "/login":
            page.add(LoginView(show_memo_view))
        elif page.route == "/":
            if hasattr(page, "user"):
                page.add(MemoView(page.user))
            else:
                page.go("/login")
    
    def show_memo_view(user):
        page.user = user  # ユーザー情報をページに保存
        page.go("/")

    page.on_route_change = route_change
    page.go("/login")

ft.app(target=main) 