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

def feeding_food_count(page: ft.Page, customer_detail:dict=None): # type: ignore
    left_intake = 0
    g_product_weight = 5
    view_product_weight = "???Kg"
    feeding_food_count = "??"
    last_feeding_food_count = "????.??.??"

    if customer_detail:
        first_customer_detail = customer_detail.get(next(iter(customer_detail.keys())))
        feeding_food_count = first_customer_detail.get("left_food_count") # type: ignore
        now = datetime.datetime.now()
        days = datetime.timedelta(days=feeding_food_count)
        last_feeding_food_count = (now+days).strftime("%Y.%m.%d")
        g_product_weight = first_customer_detail.get("total_weight") # type: ignore
        left_intake = first_customer_detail.get("left_intake") # type: ignore
        kg_product_weight = float(g_product_weight / 1000)
        view_product_weight = (
            f"{kg_product_weight}Kg" if len(str(kg_product_weight).replace(".0", "")) > 2 
                else f"{g_product_weight}g"
        )

    content_column = [
        dogdog.basic_text(value="급여 중인 사료 잔여량", size=17, weight="bold"),
        ft.Row(
            controls=[
                dogdog.basic_text(spans=[
                    ft.TextSpan(f"{left_intake}g", style=dogdog.TextStyle(size=16)),
                    ft.TextSpan(f" / {view_product_weight}")
                ], color=ft.Colors.GREY_400, weight="bold", size=16),
                dogdog.flat_button(f"{feeding_food_count} 일치 남음", scale=0.7),
            ],
        ),
        ft.ProgressBar(
            height=10,
            value=left_intake / g_product_weight if g_product_weight else 0,
            bgcolor=ft.Colors.GREY_300,
            color=ft.Colors.YELLOW_600,
            border_radius=10,
        ),
        dogdog.basic_text(spans=[
            ft.TextSpan("예상 소진일 "),
            ft.TextSpan(last_feeding_food_count)
        ], size=12, color=ft.Colors.GREY_600),
    ]

    return content_column