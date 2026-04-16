import flet as ft
import components as dogdog
# -------------------------------------------------------------------------------------------------------

def flat_button(text, scale=0.8, icon=None, size=None, expand=None, on_click=None, disabled=True):
    return ft.Button(
        icon=icon,
        width=size,
        height=size,
        scale=scale,
        bgcolor=ft.Colors.GREY_100,
        content=dogdog.basic_text(value=text, color=ft.Colors.GREY_600),
        expand=expand,
        on_click=on_click,
        disabled=disabled,
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.GREY_300,
            shape=ft.RoundedRectangleBorder(radius=5), 
            padding=ft.Padding.only(left=10, right=10)
        )
    )

def icon_flat_button(text, icon, on_click=None):
    return ft.Container(
        expand=True,
        height=90,
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


def appbar_button(icon, text, on_click):
    if icon is None and text is None:
        return ft.Container(expand=True)
    return ft.Container(
        padding=0,
        expand=True,
        ink=True,
        on_click=on_click,
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=3,
            controls=[
                ft.Icon(icon=icon, color=ft.Colors.GREY_400, size=22),
                dogdog.basic_text(value=text, size=12, color=ft.Colors.GREY_400),
            ],
        ),
    )

def appbar_floating_button(icon, on_click):
    return ft.FloatingActionButton(
        offset=ft.Offset(0, 0.2),
        scale=1.3,
        content=ft.Image(
            src=icon,
            fit=ft.BoxFit.COVER,
        ),
        bgcolor=ft.Colors.TRANSPARENT,
        shape=ft.CircleBorder(),
        elevation=0,
        hover_elevation=0,
        highlight_elevation=0,
        focus_elevation=0,
        splash_color=ft.Colors.TRANSPARENT,
        hover_color=ft.Colors.TRANSPARENT,
        focus_color=ft.Colors.TRANSPARENT,
        on_click=on_click,
    )

def tap_button(index, value, on_click=None):
    return ft.Container(
        padding=ft.Padding.only(left=20, right=20, top=10, bottom=10),
        expand=True,
        border_radius=ft.border_radius.all(10),
        ink=True,
        on_click=on_click,
        content=dogdog.basic_text(value=value, size=16, weight="bold", color=ft.Colors.GREY_500)
    )