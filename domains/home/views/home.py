# -------------------------------------------------------------------------------------------------------
import flet as ft
import components as dogdog
import datetime
# -------------------------------------------------------------------------------------------------------
def now_history(page: ft.Page):
    content_column = [
        ft.Row([
                dogdog.basic_text(value="오늘의 기록", size=18, weight="bold"),
                dogdog.basic_text(value=datetime.datetime.now().strftime("%Y.%m.%d"), size=14, weight="bold", color=ft.Colors.GREY_700),
        ]),
        ft.Row(
            spacing=0,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                dogdog.flat_button("급여량: 100g"),
                dogdog.flat_button("음수량: 100ml"),
                dogdog.flat_button("산책: 60분"),
        ]),
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                dogdog.basic_text(value="목표 활동량", size=14, color=ft.Colors.GREY_700, weight="bold"),
                ft.Column(
                    spacing=0,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.ProgressBar(
                            height=20,
                            value=45 / 90 if 90 else 0,
                            bgcolor=ft.Colors.GREY_300,
                            color=ft.Colors.YELLOW_600,
                            border_radius=10,
                        ),
                        dogdog.basic_text(
                            value=f"{45}/{90}{"분"}",
                            size=12,
                            color=ft.Colors.GREY_500,
                            weight="bold",
                        ),
                    ],
                ),
            ]
        ),
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                dogdog.basic_text(value="목표 칼로리", size=14, color=ft.Colors.GREY_700, weight="bold"),
                ft.Column(
                    spacing=0,
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.ProgressBar(
                            height=20,
                            value=150 / 310 if 310 else 0,
                            bgcolor=ft.Colors.GREY_300,
                            color=ft.Colors.YELLOW_600,
                            border_radius=10,
                        ),
                        dogdog.basic_text(
                            value=f"{150}/{310}{"kcal"}",
                            size=12,
                            color=ft.Colors.GREY_500,
                            weight="bold",
                        ),
                    ],
                ),
            ]
        )
    ]
    return content_column

def feeding_food_count(page: ft.Page):
    now = datetime.datetime.now()
    days = datetime.timedelta(days=24)
    last_feeding_food_count = (now+days).strftime("%Y.%m.%d")
    content_column = [
        dogdog.basic_text(value="급여 중인 사료 잔여량", size=17, weight="bold"),
        ft.Row(
            controls=[
                dogdog.basic_text(spans=[
                    ft.TextSpan("800g", style=dogdog.TextStyle(size=16)),
                    ft.TextSpan(" / 2Kg")
                ], color=ft.Colors.GREY_700, weight="bold", size=16),
                dogdog.flat_button("24 일치 남음"),
            ],
        ),
        ft.ProgressBar(
            height=10,
            value=150 / 310 if 310 else 0,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.YELLOW_600,
            border_radius=10,
        ),
        dogdog.basic_text(spans=[
            ft.TextSpan("예상 소진일 "),
            ft.TextSpan(last_feeding_food_count)
        ], size=12, color=ft.Colors.GREY_600, weight="bold"),
    ]

    return content_column

def fast_menu_grid(page :ft.Page):
    content_column = [
        ft.Row(
            controls=[
                dogdog.icon_flat_button(text="밥주기", icon="dogbowl.png"),
                dogdog.icon_flat_button(text="물주기", icon="waterdrop.png"),
                dogdog.icon_flat_button(text="활동기록", icon="dogwalking.png"),
            ]
        ),
        ft.Row(
            controls=[
                dogdog.icon_flat_button(text="위생/배변", icon="poop.png"),
                dogdog.icon_flat_button(text="건강기록", icon="injection.png"),
                dogdog.icon_flat_button(text="상태기록", icon="note.png"),
            ]
        ),
    ]
    return ft.Container(
        padding=ft.Padding.only(left=20, right=20),
        bgcolor="#ffffff",
        content=ft.Column(
            controls=content_column # type: ignore
        )
    )