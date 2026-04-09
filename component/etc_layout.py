import flet as ft
import component as dogdog

def arrow_back(on_click=None):
    return ft.Container(
        expand=1,
        on_click=on_click,
        content=ft.Icon(
            ft.Icons.ARROW_BACK_IOS,
            size=22,
        ),
    )


def about_dog(case=None):
    content = ft.Column(
        spacing=0,
        controls=[
            dogdog.basic_text(value="About your Dog", weight="Bold", size=30),
            dogdog.basic_text(value="반려동물의 기본 정보를 입력하세요", weight="Bold", size=15),
        ],
    )
    if case == 1:
        content = ft.Column(
            spacing=0,
            controls=[
                dogdog.basic_text("Welcome to 똑똑", weight="bold", size=30),
                ft.Container(height=12),
                dogdog.basic_text("똑똑🚪✊ 우리집 강아지가 마지막 한알을 먹기 전\n문앞에 사료가 도착합니다.", weight="bold", size=14)
            ],
        )
    return ft.Container(
        height=140,
        alignment=ft.Alignment.BOTTOM_CENTER,
        content=content
    )

def long_box(
    text,
    bgcolor=ft.Colors.WHITE,
    text_color=ft.Colors.BLACK,
    border_color=ft.Colors.GREY_300,
    on_click=None,
    icon=None,
):
    controls = []

    if icon:
        controls.append(ft.Icon(icon, size=18, color=text_color))

    controls.append(
        ft.Text(
            text,
            size=14,
            weight=ft.FontWeight.W_500,
            color=text_color,
        )
    )

    return ft.Container(
        width=350,
        height=50,
        bgcolor=bgcolor,
        border=ft.Border.all(1, border_color),
        border_radius=10,
        padding=10,
        alignment=ft.Alignment(0, 0),
        on_click=on_click,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            controls=controls,
        ),
    )


def bottom_continue_button(on_click=None):
    return ft.Container(
        expand=9,
        content=long_box(
            "Continue",
            bgcolor=ft.Colors.YELLOW,
            text_color=ft.Colors.BLACK,
            on_click=on_click,
        ),
    )
