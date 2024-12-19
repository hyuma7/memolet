import flet as ft
import subprocess
import os
from ...entities.memo import Memo

class MemoCard(ft.Card):
    def __init__(self, memo: Memo, on_delete, on_edit):
        super().__init__()
        self.memo = memo
        self.on_delete = on_delete
        self.on_edit = on_edit
        
        # カードのスタイル設定
        self.elevation = 3
        self.surface_tint_color = ft.Colors.BLUE_700
        self.color = ft.Colors.WHITE
        
        # オプション情報のコントロールを作成
        optional_controls = []
        if memo.project_path:
            optional_controls.append(
                ft.Text(
                    f"プロジェクトパス: {memo.project_path}",
                    size=12,
                    color=ft.Colors.GREY_700
                )
            )
        if memo.command:
            optional_controls.append(
                ft.Text(
                    f"コマンド: {memo.command}",
                    size=12,
                    color=ft.Colors.GREY_700
                )
            )
        
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.ListTile(
                        title=ft.Text(
                            memo.title,
                            size=20,
                            weight=ft.FontWeight.W_500,
                            color=ft.Colors.BLUE_700
                        ),
                        subtitle=ft.Text(
                            memo.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                            size=12,
                            color=ft.Colors.GREY_600
                        ),
                    ),
                    ft.Container(
                        content=ft.Text(
                            memo.content[:100] + "..." if len(memo.content) > 100 else memo.content,
                            size=14,
                            color=ft.Colors.GREY_800
                        ),
                        padding=ft.padding.only(left=16, right=16, bottom=10)
                    ),
                    # オプション情報の表示
                    ft.Container(
                        content=ft.Column(
                            controls=optional_controls,
                            spacing=5
                        ),
                        padding=ft.padding.only(left=16, right=16, bottom=10)
                    ) if optional_controls else None,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    icon_color=ft.Colors.BLUE_700,
                                    tooltip="編集",
                                    on_click=lambda e: self.on_edit(self.memo.id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED_700,
                                    tooltip="削除",
                                    on_click=lambda e: self.on_delete(self.memo.id)
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.PLAY_ARROW,
                                    icon_color=ft.Colors.GREEN_700,
                                    tooltip="コマンド実行",
                                    on_click=self.execute_command,
                                    visible=bool(memo.command)
                                )
                            ],
                            alignment=ft.MainAxisAlignment.END
                        ),
                        padding=ft.padding.only(right=8, bottom=8)
                    )
                ]
            ),
            padding=10
        )

    def execute_command(self, e):
        if self.memo.project_path and self.memo.command:
            try:
                subprocess.Popen(
                    self.memo.command,
                    cwd=self.memo.project_path,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            except Exception as ex:
                print(f"コマンド実行エラー: {ex}") 