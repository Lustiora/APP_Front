import flet as ft
import components as dogdog
import datetime

def onboarding_top_bar(case=None):
    content = ft.Column(
        spacing=0,
        controls=[
            dogdog.basic_text(value="About your Dog", weight="Bold", size=30),
            dogdog.basic_text(value="반려동물의 기본 정보를 입력하세요", weight="Bold", size=15),
        ],
    )
    if case == 1: content = ft.Column(
        spacing=0,
        controls=[
            dogdog.basic_text(value="Welcome to 똑똑", weight="bold", size=30),
            ft.Container(height=12),
            dogdog.basic_text(
                value="똑똑🚪✊ 우리집 강아지가 마지막 한알을 먹기 전\n문앞에 사료가 도착합니다.", 
                weight="bold", size=14
            )
        ]
    )

    return ft.Container(height=120, padding=ft.Padding.only(top=40), content=content)

def home_top_bar(page, pet_list:dict, pet_profile_image="dogclay.png"):
    first_pet_id = next(iter(pet_list.keys()))
    first_pet_birth_day = pet_list.get(first_pet_id).get("birth_day") # type: ignore
    first_pet_birth_sex = pet_list.get(first_pet_id).get("sex") # type: ignore

    pet_list_name = []
    for row_id , row in pet_list.items():
        pet_list_name.append(ft.DropdownOption(key=f"{row_id}", text=row.get("nickname"), style=dogdog.Style.DropdownOptionStyle))
    
    def select_event(e):
        birth_day = None
        sex = None
        for row_id , row in pet_list.items():
            if int(row_id) == int(e.data):
                birth_day = row.get("birth_day")
                sex = row.get("sex")
        if birth_day and sex:
            pet_dropdown_list.helper_text = pet_dropdown_list_helper_text(birth_day, sex)
            pet_dropdown_list.update()
            select_pet_id = pet_dropdown_list.value
    
    def pet_dropdown_list_helper_text(birth_day, sex):
        birth = datetime.datetime.strptime(birth_day, "%Y-%m-%d")
        now = datetime.datetime.now()
        years = now.year - birth.year
        months = now.month - birth.month
        if now.day < birth.day: months -= 1
        if months < 0:
            years -= 1
            months += 12
        sex_symbol = "♂️" if str(sex) == "1" else "♀️"
        return f"({years}년 {months}개월, {sex_symbol})"

    pet_dropdown_list = ft.Dropdown(
        content_padding=0,
        helper_text=pet_dropdown_list_helper_text(first_pet_birth_day, first_pet_birth_sex),
        on_select=select_event,
        helper_style=dogdog.TextStyle(color=ft.Colors.OUTLINE, size=12),
        height=50,
        text_style=dogdog.TextStyle(),
        trailing_icon=ft.Icons.KEYBOARD_ARROW_DOWN,
        selected_trailing_icon=ft.Icons.KEYBOARD_ARROW_UP,
        value=f"{first_pet_id}",
        menu_style=ft.MenuStyle(bgcolor="#DBD19F", padding=0),
        border_width=0,
        options=pet_list_name
    )
    
    header_controls = [
        ft.Container(content=ft.Row(spacing=10, controls=[
            ft.Image(src=pet_profile_image, height=80),
            ft.Container(padding=0, width=120, height=80, content=pet_dropdown_list)])),
        ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE, icon_color=ft.Colors.OUTLINE, icon_size=30)
    ]

    header_container = ft.Container(
        padding=ft.Padding.only(top=40),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=header_controls
    ))

    return header_container