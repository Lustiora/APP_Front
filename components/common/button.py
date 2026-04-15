import flet as ft
import components as dogdog
# -------------------------------------------------------------------------------------------------------

def flat_button(text, scale=0.8, size=None, expand=None, on_click=None):
    return ft.Button(
        width=size,
        height=size,
        scale=scale,
        color="#FFFFFF",
        bgcolor=ft.Colors.GREY_100,
        content=dogdog.basic_text(value=text),
        expand=expand,
        on_click=on_click,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREY_300,
            shape=ft.RoundedRectangleBorder(radius=5), 
            padding=ft.Padding.only(left=5, right=5)
        )
    )

def icon_flat_button(text, icon, on_click=None):
    return ft.Container(
        expand=True,
        height=85,
        on_click=lambda _:print(text) if on_click is None else on_click(),
        ink=True,
        border_radius=ft.border_radius.all(10),
        border=ft.Border.all(width=2, color=ft.Colors.GREY_200),
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.GREY_100, offset=ft.Offset(x=0, y=3)),
        bgcolor="#ffffff",
        content=ft.Column(
            spacing=5,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Image(src=icon, width=40, height=40, fit=ft.BoxFit.CONTAIN),
                dogdog.basic_text(value=text, size=16, weight="bold")
            ]
        )
    )