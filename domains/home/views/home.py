# -------------------------------------------------------------------------------------------------------
import flet as ft
import components as dogdog
import datetime
from api.full_query import Home
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

def fast_menu_grid(page :ft.Page, customer_detail:dict=None): # type: ignore
    storage = page.session.store
    def bottom_sheet(e, call):
        grid_bottom_sheet = dogdog.bottom_sheet(
            content=[
                dogdog.basic_text(value=call, size=25, weight="bold"),
                ft.Divider(),
            ]
        )
        bottom_sheet_contents = grid_bottom_sheet.content.content.controls # type: ignore
        if call == "밥주기":
            if customer_detail:
                food = [dogdog.dropdown_menu_option(
                    key=customer_food_id, text=f"{detail.get("brand")} {detail.get("product_name")}"
                        ) for customer_food_id , detail in customer_detail.items()]
                feeding_food_list = ft.Row(margin=ft.margin.only(bottom=14),
                    controls=[dogdog.dropdown_menu(label="사료를 선택해주세요.", event=None, options=food)])
                
                def on_food_weight_change(e):
                    try: storage.set("feeding_weight", int(e.control.value))
                    except ValueError: pass
                feeding_weight = dogdog.input_textfield(
                    hint_text="급여량을 적어주세요.", input_type="int", suffix="g", on_change=on_food_weight_change)
                if storage.get("feeding_weight"):
                    feeding_weight.value = storage.get("feeding_weight") # type: ignore
                
                def on_memo_change(e):
                    try: storage.set("feeding_memo", e.control.value)
                    except ValueError: pass
                feeding_memo = dogdog.input_textfield(
                    hint_text="메모 (선택)", text_filter=None, max_length=None, on_change=on_memo_change) # type: ignore
                if storage.get("feeding_memo"):
                    feeding_memo.value = storage.get("feeding_memo") # type: ignore
                
                def feeding_date_open(e):
                    date_picker.open = True
                feeding_date = ft.Container(
                    ink=True,
                    border_radius=ft.border_radius.all(10),
                    padding=4,
                    on_click=feeding_date_open,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Icon(icon=ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREY_600, size=16),
                            dogdog.basic_text(value=datetime.datetime.now().strftime("%Y.%m.%d"), color=ft.Colors.GREY_600),
                        ]
                    )
                )

                def feeding_time_open(e):
                    time_picker.open = True
                feeding_time = ft.Container(
                    ink=True,
                    border_radius=ft.border_radius.all(10),
                    padding=4,
                    on_click=feeding_time_open,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5,
                        controls=[
                            ft.Icon(icon=ft.Icons.ACCESS_TIME, color=ft.Colors.GREY_600, size=16),
                            dogdog.basic_text(value="오전 08:00", color=ft.Colors.GREY_600),
                        ]
                    )
                )

                feeding_timestamp = ft.Row(
                    margin=ft.margin.only(top=14),
                    spacing=30,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        feeding_date,
                        feeding_time
                    ]
                )

                def on_date_change(e):
                    if e.control.value:
                        feeding_day = (e.control.value + datetime.timedelta(hours=9)).strftime("%Y.%m.%d")
                        storage.set(key="feeding_date", value=feeding_day)
                        feeding_date.content.controls[1].value = feeding_day # type: ignore

                date_picker = ft.DatePicker(
                    first_date=datetime.datetime.now() - datetime.timedelta(days=7),
                    last_date=datetime.datetime.now(),
                    on_change=on_date_change,
                )
                if date_picker not in page.overlay:
                    page.overlay.append(date_picker)
                
                def on_time_change(e):
                    if e.control.value:
                        feeding_timez = e.control.value.strftime("%p %H:%M").replace("AM", "오전").replace("PM", "오후")
                        storage.set(key="feeding_time", value=feeding_timez)
                        feeding_time.content.controls[1].value = feeding_timez # type: ignore
                
                time_picker = ft.TimePicker(
                    entry_mode=ft.TimePickerEntryMode.DIAL_ONLY,
                    on_change=on_time_change,
                )
                if time_picker not in page.overlay:
                    page.overlay.append(time_picker)
                
                feeding_setting_content = [
                    dogdog.flat_button("수정", scale=1, bgcolor="#FEF3B9"), # type: ignore
                    dogdog.flat_button("삭제", scale=1, bgcolor="#FEF3B9"), # type: ignore
                    dogdog.flat_button("저장", scale=1)
                ]

                feeding_setting = ft.Row(
                    margin=ft.margin.only(top=10),
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=feeding_setting_content # type: ignore
                )

                bottom_sheet_contents.append(feeding_food_list)
                bottom_sheet_contents.append(feeding_weight)
                bottom_sheet_contents.append(feeding_memo)
                bottom_sheet_contents.append(feeding_timestamp)
                bottom_sheet_contents.append(feeding_setting)
            
            else: pass
        elif call == "물주기": pass
        elif call == "활동기록": pass
        elif call == "위생/배변": pass
        elif call == "건강기록": pass
        elif call == "상태기록": pass
        if grid_bottom_sheet not in page.overlay:
            page.overlay.append(grid_bottom_sheet)
        else:
            page.overlay.clear()
            page.overlay.append(grid_bottom_sheet)
        grid_bottom_sheet.open = True
        page.update()
    
    content_list_top = [
        ("밥주기", "dogbowl.png", lambda e, call="밥주기":bottom_sheet(e, call)),
        ("물주기", "waterdrop.png", lambda e, call="물주기":bottom_sheet(e, call)),
        ("활동기록", "dogwalking.png", lambda e, call="활동기록":bottom_sheet(e, call)),
    ]
    content_list_bottom = [
        ("위생/배변", "poop.png", lambda e, call="위생/배변":bottom_sheet(e, call)),
        ("건강기록", "injection.png", lambda e, call="건강기록":bottom_sheet(e, call)),
        ("상태기록", "note.png", lambda e, call="상태기록":bottom_sheet(e, call)),
    ]

    content_column = [
        ft.Row(controls=[
            dogdog.icon_flat_button(text=text, icon=icon, on_click=on_click) for text, icon, on_click in content_list_top
        ]),
        ft.Row(controls=[
            dogdog.icon_flat_button(text=text, icon=icon, on_click=on_click) for text, icon, on_click in content_list_bottom
        ]),
    ]
    return ft.Container(
        padding=ft.Padding.only(left=20, right=20),
        bgcolor="#ffffff",
        content=ft.Column(controls=content_column) # type: ignore
    )