import flet as ft
import datetime

import pg8000.dbapi as psycopg2
# import psycopg2

from .full_query import Breed
import component as dogdog


# ✅ DB 연결 함수
def get_connection():
    conn = psycopg2.connect(
        host="pg.nas6418.ddns.net",
        port=9934,
        database="Dogdog",
        user="dog_5",
        password="kosmo",
        timeout=3,
    )
    return conn

def build_view(page: ft.Page):
    conn = None
    breed_error_text = None
    selected_breed_id = None

    # 🟨 키보드 숨김용 투명/더미 입력창 추가
    dummy_input = ft.TextField(width=0, height=0, opacity=0, read_only=True)
    if dummy_input not in page.overlay:
        page.overlay.append(dummy_input)

    async def hide_keyboard():
        await dummy_input.focus()

    ####################################################################################################
    ### 애완동물 이름 입력
    ####################################################################################################
    def petname_on_change(e):
        page.session.store.set("pet_name", e.control.value)
    pet_name_field = dogdog.input_textfield(hint_text="이름을 입력해주세요.", on_change=petname_on_change)
    if page.session.store.get("pet_name"):
        pet_name_field.value = page.session.store.get("pet_name") # type: ignore

    ####################################################################################################
    ### 애완동물 이미지 등록
    ####################################################################################################
    image_container = dogdog.image_circle(event=None, src=None, size=200)
    image_container.visible = False
    selected_profile_image_text = "이미지를 등록해주세요."

    # Image retrieval on initial load
    if page.session.store.get("image_path"): # Check for image_path
        selected_profile_image_text = page.session.store.get("image_name") # Keep displaying the name
        image_container.visible = True
        image_container.image = ft.DecorationImage(src=page.session.store.get("image_path"), fit=ft.BoxFit.COVER)

    file_picker = ft.FilePicker()

    async def pick_profile_image(e):
        nonlocal selected_profile_image_text
        await hide_keyboard()

        files = await file_picker.pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
        )

        if files:
            print(files)
            file = files[0]
            if file.path is None:
                print("Error: file.path is None. Could not get file path from selected file.")
                selected_profile_image_text = "파일 경로를 가져올 수 없습니다."
                rebuild_body()
                page.update()
                return

            # 세션에 로컬 파일 경로와 이름을 직접 저장합니다.
            page.session.store.set("image_path", file.path)
            page.session.store.set("image_name", file.name)
            selected_profile_image_text = file.name

            # 이미지 컨테이너를 업데이트합니다.
            image_container.visible = True
            image_container.image = ft.DecorationImage(src=file.path, fit=ft.BoxFit.COVER)
        else:
            selected_profile_image_text = "프로필 이미지를 등록하세요"
            # 아무것도 선택되지 않은 경우 세션에서 이미지를 지웁니다.
            page.session.store.remove("image_path")
            page.session.store.remove("image_name")
            image_container.visible = False
            image_container.image = None

        rebuild_body()
        page.update() # UI 업데이트를 확인합니다.

    ####################################################################################################
    ### 애완동물 견종 선택
    ####################################################################################################
    selected_breed_text = "반려동물 품종을 선택해주세요."
    if page.session.store.get("breed_text"):
        selected_breed_text = page.session.store.get("breed_text")

    breed_list_column = ft.Column(
        expand=True,
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
    )

    def ensure_db_connection():
        nonlocal conn, breed_error_text

        if conn is not None and getattr(conn, "closed", 1) == 0:
            breed_error_text = None
            return True
        try:
            conn = get_connection()
            breed_error_text = None
            return True
        except Exception as err:
            breed_error_text = f"DB 서버 연결 실패: {err}"
            return False

    def load_breed_list():
        nonlocal breed_error_text

        if not ensure_db_connection():
            return None

        try:
            cursor = conn.cursor() # type: ignore
            cursor.execute(Breed.breed_list_query)
            rows = cursor.fetchall()
            conn.commit() # type: ignore
            cursor.close()
            breed_error_text = None
            return rows
        except Exception as err:
            conn.rollback() # type: ignore
            breed_error_text = f"품종 목록 조회 실패: {err}"
            print(f"breed_list_query error: {err}")
            return None

    def search_breed_list(keyword):
        nonlocal breed_error_text

        if not ensure_db_connection():
            return None

        try:
            cursor = conn.cursor() # type: ignore
            cursor.execute(Breed.breed_search_query, (f"%{keyword}%",))
            rows = cursor.fetchall()
            conn.commit() # type: ignore
            cursor.close()
            breed_error_text = None
            return rows
        except Exception as err:
            conn.rollback() # type: ignore
            breed_error_text = f"품종 검색 실패: {err}"
            print(f"breed_search_query error: {err}")
            return None

    def select_breed(breed_id, breed_name):
        nonlocal selected_breed_id, selected_breed_text
        selected_breed_id = breed_id
        page.session.store.set("breed_id", selected_breed_id)
        selected_breed_text = breed_name
        page.session.store.set("breed_text", selected_breed_text)

        update_breed_list(breed_search_field.value if breed_search_field.value else "")
        rebuild_body()

        breed_bottom_sheet.open = False

    def breed_item(breed_id, breed_name):
        is_checked = selected_breed_id == breed_id

        return ft.Container(
            padding=ft.Padding.symmetric(vertical=14, horizontal=10),
            border_radius=10,
            bgcolor=ft.Colors.OUTLINE_VARIANT if is_checked else ft.Colors.WHITE,
            on_click=lambda e, b_id=breed_id, b_name=breed_name: select_breed(b_id, b_name),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    dogdog.basic_text(value=breed_name, weight="bold"),
                    ft.Icon(
                        ft.Icons.CHECK,
                        color=ft.Colors.BLACK if is_checked else ft.Colors.TRANSPARENT,
                        size=18,
                    ),
                ],
            ),
        )

    def update_breed_list(keyword=""):
        nonlocal breed_error_text

        if keyword.strip():
            breed_rows = search_breed_list(keyword.strip())
        else:
            breed_rows = load_breed_list()

        if breed_rows is None:
            breed_list_column.controls = [
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=20),
                    alignment=ft.Alignment(0, 0),
                    content=dogdog.basic_text(
                        breed_error_text if breed_error_text else "DB 연결 오류가 발생했습니다.",
                        size=14,
                        color=ft.Colors.RED,
                    ),
                )
            ]
        elif breed_rows:
            breed_list_column.controls = [breed_item(row[0], row[1]) for row in breed_rows]
        else:
            breed_list_column.controls = [
                ft.Container(
                    content=dogdog.basic_text(
                        "검색 결과가 없습니다.",
                        size=14,
                    ),
                )
            ]

    def on_breed_search_change(e):
        update_breed_list(e.control.value)

    breed_search_field = dogdog.list_input_textfield(
        hint_text="품종 검색", on_change=on_breed_search_change
    )

    breed_bottom_sheet = dogdog.bottom_sheet(
        content=[
            dogdog.basic_text(value="품종 검색", size=25, weight="bold"),
            ft.Divider(),
            breed_search_field,
            breed_list_column
        ]
    )

    if breed_bottom_sheet not in page.overlay:
        page.overlay.append(breed_bottom_sheet)

    async def open_breed_bottom_sheet(e):
        await hide_keyboard()
        breed_search_field.value = ""
        update_breed_list("")
        breed_bottom_sheet.open = True

    ####################################################################################################
    ### 애완동물 생년월일 선택
    ####################################################################################################
    birth_input_mode = None

    def open_date_picker(e):
        date_picker.open = True
    async def age_year_event(e):
        await hide_keyboard()
        page.session.store.set("pet_age_year", e.control.value)
        if page.session.store.get("selected_birth"):
            page.session.store.remove("selected_birth")
    async def age_month_event(e):
        await hide_keyboard()
        page.session.store.set("pet_age_month", e.control.value)
        if page.session.store.get("selected_birth"):
            page.session.store.remove("selected_birth")
    async def change_birth_mode(e):
        await hide_keyboard()
        nonlocal birth_input_mode
        birth_input_mode = e.control.value
        page.session.store.set("birth_input_mode", birth_input_mode)
        rebuild_body()

    selected_birth_text = "생년월일 선택"
    if page.session.store.get("selected_birth"):
        selected_birth_text = page.session.store.get("selected_birth")

    def on_date_change(e):
        nonlocal selected_birth_text
        if e.control.value:
            selected_birth_text = e.control.value
            page.session.store.set("selected_birth", selected_birth_text)
            if page.session.store.get("pet_age_year") and page.session.store.get("pet_age_month"):
                page.session.store.remove("pet_age_year")
                page.session.store.remove("pet_age_month")
            rebuild_body()

    date_picker = ft.DatePicker(
        first_date=datetime.datetime(2000, 1, 1),
        last_date=datetime.datetime.now(),
        on_change=on_date_change,
    )
    if date_picker not in page.overlay:
        page.overlay.append(date_picker)

    age_year_dropdown = dogdog.dropdown_menu(
        label="년 선택",
        event=age_year_event,
        options=[dogdog.dropdown_menu_option(text=f"{year} 년") for year in range(0, 31)],
    )
    age_month_dropdown = dogdog.dropdown_menu(
        label="개월 선택",
        event=age_month_event,
        options=[dogdog.dropdown_menu_option(text=f"{month} 개월") for month in range(0, 12)],
    )
    if page.session.store.get("pet_age_year") and page.session.store.get("pet_age_month"):
        age_year_dropdown.value = page.session.store.get("pet_age_year")
        age_month_dropdown.value = page.session.store.get("pet_age_month")

    def build_birth_choice():
        choice = ft.Column(
            expand=True,
            controls=[
                dogdog.radio_group(
                    value="birthday_known",
                    on_change=change_birth_mode,
                    layout_type="column",
                    contents=[
                        ft.Radio(value="birthday_known", label="생년월일을 알아요"),
                        ft.Radio(value="age_only", label="대략적인 나이만 알고 있어요")
                    ]
                ),
                dogdog.picker_field(
                    text=selected_birth_text,
                    on_click=open_date_picker,
                    icon=ft.Icons.CALENDAR_MONTH,
                )
            ]
        )
        page.session.store.set("birthday", birth_input_mode)

        if "age_only" in (page.session.store.get("birth_input_mode"), birth_input_mode):
            choice.controls=[
                dogdog.radio_group(
                    value="age_only",
                    on_change=change_birth_mode,
                    layout_type="column",
                    contents=[
                        ft.Radio(value="birthday_known", label="생년월일을 알아요"),
                        ft.Radio(value="age_only", label="대략적인 나이만 알고 있어요")
                    ]
                ),
                ft.Row(
                    height=48,
                    controls=[
                        age_year_dropdown,
                        age_month_dropdown,
                    ],
                )
            ]
            page.session.store.set("birthday", birth_input_mode)

        return choice

    ####################################################################################################
    ### 애완동물 성별 / 중성화 여부 선택
    ####################################################################################################
    async def gender_event(e):
        await hide_keyboard()
        page.session.store.set("pet_gender", e.control.value)
    gender_dropdown = dogdog.dropdown_menu(
        label="성별 / 중성화",
        event=gender_event,
        options=[
            dogdog.dropdown_menu_option(text="수컷", icon=ft.Icons.MALE, icon_color=ft.Colors.BLUE),
            dogdog.dropdown_menu_option(text="수컷 (중성화)", icon=ft.Icons.CUT, icon_color=ft.Colors.BLUE),
            dogdog.dropdown_menu_option(text="암컷", icon=ft.Icons.FEMALE, icon_color=ft.Colors.PINK),
            dogdog.dropdown_menu_option(text="암컷 (중성화)", icon=ft.Icons.CUT, icon_color=ft.Colors.PINK),
        ]
    )
    if page.session.store.get("pet_gender"):
        gender_dropdown.value = page.session.store.get("pet_gender")

    ####################################################################################################
    ### 애완동물 무게 입력
    ####################################################################################################
    def weight_event(e):
        try:
            page.session.store.set("pet_weight", float(e.control.value))
        except ValueError:
            pass
    weight_field = dogdog.input_textfield(hint_text="무게를 입력해주세요.", suffix="Kg", input_type="int", on_change=weight_event)
    if page.session.store.get("pet_weight"):
        weight_field.value = page.session.store.get("pet_weight") # type: ignore

    body_content = ft.Column(
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )

    def rebuild_body():
        body_content.controls = [
            dogdog.basic_text("이름", weight="bold"),
            pet_name_field,
            ft.Container(content=image_container, alignment=ft.Alignment.CENTER),
            dogdog.basic_text("프로필 이미지", weight="bold"),
            dogdog.picker_field(
                text=selected_profile_image_text,
                on_click=pick_profile_image,
                icon=ft.Icons.UPLOAD_FILE,
            ),
            ft.Container(height=8),
            dogdog.basic_text("품종", weight="bold"),
            dogdog.picker_field(
                text=selected_breed_text,
                on_click=open_breed_bottom_sheet,
                icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED,
            ),
            ft.Container(height=8),
            dogdog.basic_text("생년월일", weight="bold"),
            build_birth_choice(),
            ft.Container(height=8),
            dogdog.basic_text("성별", weight="bold"),
            gender_dropdown,
            ft.Container(height=8),
            dogdog.basic_text("무게", weight="bold"),
            weight_field,
        ]

    rebuild_body()

    return dogdog.build_screen_body([body_content])