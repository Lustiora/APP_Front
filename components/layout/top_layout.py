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

def main_top_bar(page, view=None, pet_list:dict=None, pet_profile_image="dogclay.png"): # type: ignore
    # ---------------------------------------------------------------------------------------------------    
    # Page Background
    # ---------------------------------------------------------------------------------------------------
    background_height = 100
    home_background = ft.Container(
        bgcolor="#FEF3B9", height=background_height, border_radius=ft.BorderRadius.only(bottom_left=30, bottom_right=30),
    )
    case = dogdog.flat_button(
        text="사료 등록", icon=ft.Icons.EDIT, on_click=lambda _: print("사료 등록"), disabled=False
    )
    
    center_header = ft.Container()
    right_header = ft.IconButton(
        icon=ft.Icons.NOTIFICATIONS_NONE, icon_color=ft.Colors.GREY_500, icon_size=26
    )
    
    body_scale = 1
    body_margin = -50
    body_column = ft.Column(spacing=15, expand=True)
    header_container_padding = 40

    if view == "home":
        top_padding = 40
        background_height = 160
        body_scale = 0.92
        body_margin = -80
        first_pet_id = next(iter(pet_list.keys()))
        first_pet_birth_day = pet_list.get(first_pet_id).get("birth_day") # type: ignore
        first_pet_birth_sex = pet_list.get(first_pet_id).get("sex") # type: ignore

        pet_list_name = [
            ft.DropdownOption(
                key=f"{row_id}", text=row.get("nickname"), style=dogdog.Style.DropdownOptionStyle
            ) for row_id , row in pet_list.items()
        ]
        
        def select_event(e):
            birth_day = None
            sex = None
            for row_id , row in pet_list.items():
                if int(row_id) == int(e.data):
                    birth_day = row.get("birth_day")
                    sex = row.get("sex")
            if birth_day and sex:
                pet_dropdown_list.helper_text = pet_dropdown_list_helper_text(
                    birth_day=birth_day, sex=sex
                )
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
            sex_symbol = "♂️" if sex == "1" else "♀️"
            return f"({years}년 {months}개월, {sex_symbol})"

        pet_dropdown_list = ft.Dropdown(
            content_padding=0,
            helper_text=pet_dropdown_list_helper_text(
                birth_day=first_pet_birth_day, sex=first_pet_birth_sex
            ),
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

        left_header = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.END,
            height=80, spacing=10, controls=[
                ft.Image(src=pet_profile_image),
                ft.Container(padding=0, width=120, height=70, content=pet_dropdown_list)]
        )
    elif view == "feeding":
        top_padding = 40
        header_container_padding = 50
        left_header = ft.IconButton(
            icon=ft.Icons.ARROW_BACK_IOS_NEW, icon_color=ft.Colors.GREY_500, icon_size=26
        )
        center_header = dogdog.basic_text(value="급여 중인 제품", weight="bold", size=16)

    header_container = ft.Container(
        padding=ft.Padding.only(top=header_container_padding),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[left_header, center_header, right_header]
    ))

    base_height = 800.0
    if page.height < base_height: # type: ignore
        current_height = page.height if page.height > 0 else base_height # type: ignore
        scale_val = current_height / base_height # type: ignore
        header_container.padding = ft.padding.only(
            top=top_padding * scale_val if scale_val < 1.0 else top_padding
        )
        home_background.height = background_height * scale_val if scale_val < 1.0 else background_height
        body_column.scale = scale_val * body_scale if scale_val < 1.0 else body_scale
        body_column.margin = ft.margin.only(
            top=body_margin * scale_val if scale_val < 1.0 else body_margin
        )
        print('update')
        page.update()

    return (home_background , header_container , body_column) if view == "home" else (home_background , header_container)