import flet as ft
import components as dogdog
import datetime

def flat_icon_text_button(icon, value):
    return ft.Container(
        ink=True,
        border_radius=ft.border_radius.all(10),
        padding=4,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            controls=[
                ft.Icon(icon=icon, color=ft.Colors.GREY_600, size=16),
                dogdog.basic_text(value=value, color=ft.Colors.GREY_600),
            ]
        )
    )

def status_update_menu(page :ft.Page, customer_detail:dict=None): # type: ignore
    storage = page.session.store

    def event_change(e, change, case=None):
        value = e.control.value
        if change == "customer_food_id":
            try: storage.set("customer_food_id", int(value))
            except ValueError: pass
        elif change == "weight":
            try: storage.set("feeding_weight", int(value))
            except ValueError: pass
        elif change == "memo":
            try: storage.set("feeding_memo", value)
            except ValueError: pass
        elif change == "date":
            if value and case:
                now = datetime.timedelta(hours=9)
                storage.set(key="feeding_date", value=(value + now).strftime("%Y-%m-%d"))
                case.content.controls[1].value = (value + now).strftime("%Y.%m.%d")
        elif change == "time":
            if value and case:
                storage.set(key="feeding_time", value=value.strftime("%H:%M"))
                case.content.controls[1].value = (
                    value.strftime("%p %H:%M").replace("AM", "오전").replace("PM", "오후"))
    
    def open_event(e, picker):
        picker.open = True

    def setting_event(e, content):
        if content == "edit":
            print(content)
        elif content == "delete":
            print(content)
        elif content == "save":
            print(content)
            print(storage.get("customer_food_id"))
            print(storage.get("feeding_weight"))
            print(storage.get("feeding_memo"))
            print(storage.get("feeding_date"))
            print(storage.get("feeding_time"))

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
                feeding_food_list = ft.Row(margin=ft.margin.only(bottom=18),
                    controls=[
                        dogdog.dropdown_menu(label="사료를 선택해주세요.", options=food, 
                            event=lambda e, change="customer_food_id": event_change(e, change)
                )])
                
                feeding_weight = dogdog.input_textfield(
                    hint_text="급여량을 적어주세요.", input_type="int", suffix="g", 
                    on_change=lambda e, change="weight": event_change(e, change))
                if storage.get("feeding_weight"): storage.remove("feeding_weight")
                
                feeding_memo = dogdog.input_textfield(
                    hint_text="메모 (선택)", text_filter=None, max_length=None,  # type: ignore
                    on_change=lambda e, change="memo": event_change(e, change))
                if storage.get("feeding_memo"): storage.remove("feeding_memo")
                
                feeding_date = flat_icon_text_button(
                    ft.Icons.CALENDAR_MONTH, datetime.datetime.now().strftime("%Y.%m.%d")
                )

                date_picker = ft.DatePicker(
                    first_date=datetime.datetime.now() - datetime.timedelta(days=7),
                    last_date=datetime.datetime.now(),
                    on_change=lambda e, change="date", case=feeding_date: event_change(e, change, case)
                )
                if date_picker not in page.overlay:
                    page.overlay.append(date_picker)
                storage.set("feeding_date", datetime.datetime.now().strftime("%Y-%m-%d"))
                feeding_date.on_click = lambda e, picker=date_picker: open_event(e, picker)
                
                feeding_time = flat_icon_text_button(
                    ft.Icons.ACCESS_TIME, 
                    datetime.datetime.now().strftime("%p %H:%M").replace("AM", "오전").replace("PM", "오후"))

                time_picker = ft.TimePicker(
                    entry_mode=ft.TimePickerEntryMode.DIAL_ONLY,
                    on_change=lambda e, change="time", case=feeding_time: event_change(e, change, case)
                )
                if time_picker not in page.overlay:
                    page.overlay.append(time_picker)
                storage.set("feeding_time", datetime.datetime.now().strftime("%H:%M"))
                feeding_time.on_click = lambda e, picker=time_picker: open_event(e, picker)
                
                feeding_timestamp = ft.Row(
                    margin=ft.margin.only(top=14),
                    spacing=30,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        feeding_date,
                        feeding_time
                    ]
                )

                feeding_setting_content = [
                    dogdog.flat_button(
                        "수정", disabled=False, scale=1, bgcolor="#FEF3B9",  # type: ignore
                        on_click=lambda e, content="edit": setting_event(e, content)),
                    dogdog.flat_button(
                        "삭제", disabled=False, scale=1, bgcolor="#FEF3B9",  # type: ignore
                        on_click=lambda e, content="delete": setting_event(e, content)),
                    dogdog.flat_button(
                        "저장", disabled=False, scale=1, 
                        on_click=lambda e, content="save": setting_event(e, content)),
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