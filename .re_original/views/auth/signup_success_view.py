import flet as ft
import component as dogdog


def build_view(page: ft.Page):
    return ft.Container(
        expand=True,
        width=float("inf"),
        bgcolor=ft.Colors.YELLOW,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(
                    src="checkone.png",
                    width=150,
                    height=150,
                ),
                dogdog.basic_text(value="회원 가입이 완료되었습니다.", weight="bold", size=20),
            ],
        ),
    )