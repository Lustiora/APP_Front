import flet as ft
import components as dogdog
import datetime

def content_container_detail(page: ft.Page, customer_food_id, feeding_data):
    storage = page.session.store
    def feeding_edit_event(e):
        if storage.get("select_customer_food_id"): storage.remove("select_customer_food_id")
        if storage.get("select_feeding_data"): storage.remove("select_feeding_data")
        storage.set("select_customer_food_id", customer_food_id)
        storage.set("select_feeding_data", feeding_data)
        page.go("/feeding_edit")
    
    now = datetime.datetime.now()
    days = datetime.timedelta(days=feeding_data["left_food_count"])
    last_feeding_food_count = (now+days).strftime("%Y.%m.%d")

    feeding_food_weight = feeding_data["left_intake"]
    g_product_weight = feeding_data["total_weight"]
    kg_product_weight = float(g_product_weight / 1000)
    view_product_weight = (
        f"{kg_product_weight}Kg" if len(str(kg_product_weight).replace(".0", "")) > 2 
            else f"{g_product_weight}g"
    )

    detail = [
        ft.Row(height=100, expand=True, controls=[
            ft.Image(src=feeding_data["thumbnail"], fit=ft.BoxFit.CONTAIN, expand=2),
            ft.Column(expand=3, spacing=0, alignment=ft.MainAxisAlignment.CENTER, controls=[
                dogdog.basic_text(value=feeding_data["brand"]),
                dogdog.basic_text(value=feeding_data["product_name"], weight="bold", max_lines=2)
            ]),
            ft.Column(
                controls=[dogdog.flat_button(text="변경", on_click=feeding_edit_event ,disabled=False)]
        )]),
        ft.Divider(height=1),
        ft.Column(expand=True, spacing=5, controls=[
            ft.Row(controls=[
                dogdog.basic_text(spans=[
                    ft.TextSpan(
                        text=f"{feeding_food_weight}g", 
                        style=dogdog.TextStyle(size=16)),
                    ft.TextSpan(text=f" / {view_product_weight}")
                ], color=ft.Colors.GREY_400, weight="bold", size=16),
                dogdog.flat_button(text=f"{feeding_data["left_food_count"]} 일치 남음", scale=0.7),
            ]),
            ft.ProgressBar(
                height=10,
                value=feeding_food_weight / g_product_weight if g_product_weight else 0,
                bgcolor=ft.Colors.GREY_300,
                color=ft.Colors.YELLOW_600,
                border_radius=10,
            ),
            dogdog.basic_text(spans=[
                ft.TextSpan("예상 소진일 "),
                ft.TextSpan(last_feeding_food_count)
            ], size=12, color=ft.Colors.GREY_600),
    ])]

    return detail

def feeding_tabs_view(page: ft.Page, customer_food_detail:dict=None): # type: ignore
    def feeding_view(page, customer_food_detail:dict=None): # type: ignore
        if customer_food_detail:
            content_column = [
                dogdog.content_container(
                    content_list=content_container_detail(
                        page=page, customer_food_id=customer_food_id, feeding_data=detail
                )) for customer_food_id , detail in customer_food_detail.items()
            ]
        else:
            content_column = [
                ft.Row(height=200, alignment=ft.MainAxisAlignment.CENTER, controls=[
                    dogdog.basic_text(value="등록된 제품이 없습니다.", color=ft.Colors.GREY_600, size=14)
                ])
            ]

        return ft.Container(
            bgcolor="#ffffff",
            content=ft.Column(
                margin=ft.margin.only(bottom=10),
                controls=content_column # type: ignore
            )
        )

    feeding_tabs = [
        ft.Tab(label="전체"),
        ft.Tab(label="사료"),
        ft.Tab(label="간식"),
        ft.Tab(label="영양제")
    ]

    def content_column(content):
        return ft.Column(scroll=ft.ScrollMode.HIDDEN, expand=True, controls=[content], margin=ft.margin.only(bottom=10))

    feeding_content = [
        content_column(feeding_view(page=page, customer_food_detail=customer_food_detail)),
        content_column(feeding_view(page=page, customer_food_detail=customer_food_detail)),
        content_column(feeding_view(page=page)),
        content_column(feeding_view(page=page))
    ]
    
    feeding_view = ft.Tabs(
        selected_index=0,
        length=len(feeding_tabs),
        expand=True,
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[
                    ft.TabBar(
                        indicator_size=ft.TabBarIndicatorSize.TAB, divider_height=0,
                        tabs=feeding_tabs, label_text_style=dogdog.TextStyle(size=14), expand=True),  # type: ignore
                    dogdog.flat_button(
                        text="사료 등록", icon=ft.Icons.EDIT, on_click=lambda _: page.go("/feeding_add"), disabled=False)
                ]),
                ft.Divider(height=1),
                ft.TabBarView(expand=True, margin=ft.margin.only(top=10), controls=feeding_content), # type: ignore
    ]))

    return feeding_view