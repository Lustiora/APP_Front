import flet as ft

import pg8000.dbapi as psycopg2
# import psycopg2

from components import build_screen_body , go_next , input_box
from .full_query import Product

import component as dogdog

# ✅ DB 연결 함수
def get_connection():
    return psycopg2.connect(
        host="pg.nas6418.ddns.net",
        port=9934,
        database="Dogdog",
        user="dog_5",
        password="kosmo",
        timeout=3,
    )

def build_view(page: ft.Page):
    # 🟩 현재 선택된 사료 이름 상태값
    selected_food_id = None
    selected_food_text = "현재 급여 중인 사료를 선택해주세요."
    if page.session.store.get("food_name"):
        selected_food_text = page.session.store.get("food_name")


    def on_food_weight_change(e):
        page.session.store.set("food_weight", int(e.control.value))
    selected_food_weight = dogdog.input_textfield(
        hint_text="현재 급여 중인 사료 잔여량을 적어주세요", input_type="int", suffix="g",
        on_change=on_food_weight_change
    )
    if page.session.store.get("food_weight"):
        selected_food_weight.value = page.session.store.get("food_weight") # type: ignore

    # 🟦 DB 연결 객체 / 에러 메시지 상태값
    conn = None
    food_error_text = None

    # 🟩 검색 결과가 들어갈 리스트 영역
    food_list_column = ft.Column(
        spacing=6,
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )

    def on_food_search_change(e):
        update_food_list(e.control.value)

    # 🟩 바텀시트 안 검색창
    food_search_field = dogdog.list_input_textfield(
        hint_text="Search", on_change=on_food_search_change
    )


    # ─────────────────────────────────────────────
    # 🟦 추가: DB 연결 보장 함수
    # 🟦 설명:
    # 🟦 - a 코드에서 쓰던 방식 그대로 적용
    # 🟦 - conn이 살아있으면 재사용
    # 🟦 - 끊겼거나 없으면 get_connection()으로 재연결
    # ─────────────────────────────────────────────
    def ensure_db_connection():
        nonlocal conn, food_error_text

        if conn is not None and getattr(conn, "closed", 1) == 0:
            food_error_text = None
            return True

        try:
            conn = get_connection()
            food_error_text = None
            return True
        except Exception as err:
            food_error_text = f"DB 서버 연결 실패: {err}"
            page.snack_bar = ft.SnackBar( # type: ignore
                content=ft.Text(f"DB 연결 실패: {err}"),
                open=True,
            )
            
            return False

    # ─────────────────────────────────────────────
    # 🟦 추가: 사료 전체 목록 조회
    # 🟦 설명:
    # 🟦 - 기존 가짜 food_items 대신
    # 🟦 - full_query의 food_list_query 실행
    # ─────────────────────────────────────────────
    def load_food_list():
        nonlocal food_error_text

        if not ensure_db_connection():
            return None

        try:
            cursor = conn.cursor() # type: ignore
            cursor.execute(Product.product_list_query)
            rows = cursor.fetchall()
            conn.commit() # type: ignore
            cursor.close()
            food_error_text = None
            return rows
        except Exception as err:
            conn.rollback() # type: ignore
            food_error_text = f"사료 목록 조회 실패: {err}"
            print(f"food_list_query error: {err}")
            return None

    # ─────────────────────────────────────────────
    # 🟦 추가: 사료 검색 조회
    # 🟦 설명:
    # 🟦 - 검색창 입력값을 LIKE 검색으로 전달
    # 🟦 - full_query의 food_search_query 사용
    # ─────────────────────────────────────────────
    def search_food_list(keyword):
        nonlocal food_error_text

        if not ensure_db_connection():
            return None

        try:
            cursor = conn.cursor() # type: ignore
            cursor.execute(Product.product_search_query, (f"%{keyword}%",))
            rows = cursor.fetchall()
            conn.commit() # type: ignore
            cursor.close()
            food_error_text = None
            return rows
        except Exception as err:
            conn.rollback() # type: ignore
            food_error_text = f"사료 검색 실패: {err}"
            print(f"food_search_query error: {err}")
            return None

    # 🟩 사료 1개 행
    # 🟦 수정:
    # 🟦 - 이제 row[0]=food_id, row[1]=food_name 구조를 사용한다고 가정
    def food_item(food_id, food_name):
        is_selected = selected_food_id == food_id

        return ft.Container(
            padding=ft.Padding.symmetric(vertical=14, horizontal=10),
            border_radius=10,
            bgcolor=ft.Colors.OUTLINE_VARIANT if is_selected else ft.Colors.WHITE,
            on_click=lambda e, f_id=food_id, f_name=food_name: select_food(f_id, f_name),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    dogdog.basic_text(value=food_name, weight="bold"),
                    ft.Icon(
                        ft.Icons.CHECK,
                        color=ft.Colors.BLACK if is_selected else ft.Colors.TRANSPARENT,
                        size=18,
                    ),
                ],
            ),
        )

    # ─────────────────────────────────────────────
    # 🟦 수정: 검색 결과 리스트 다시 그리기
    # 🟦 기존:
    # 🟦 - food_items라는 가짜 리스트를 필터링
    # 🟦 변경:
    # 🟦 - DB에서 전체 목록 또는 검색 결과를 받아와서 출력
    # ─────────────────────────────────────────────
    def update_food_list(keyword=""):
        nonlocal food_error_text

        if keyword.strip():
            food_rows = search_food_list(keyword.strip())
        else:
            food_rows = load_food_list()

        if food_rows is None:
            food_list_column.controls = [
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=20),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        food_error_text if food_error_text else "DB 연결 오류가 발생했습니다.",
                        size=14,
                        color=ft.Colors.RED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                )
            ]
        elif food_rows:
            food_list_column.controls = [food_item(row[0], row[1]) for row in food_rows]
        else:
            food_list_column.controls = [
                ft.Container(
                    padding=ft.Padding.symmetric(vertical=20),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Text(
                        "검색 결과가 없습니다.",
                        size=14,
                        color=ft.Colors.GREY_600,
                    ),
                )
            ]

    # 🟩 사료 선택 시 실행
    # 🟦 수정:
    # 🟦 - food_id도 같이 저장
    def select_food(food_id, food_name):
        nonlocal selected_food_id, selected_food_text
        selected_food_id = food_id
        page.session.store.set("food_id", selected_food_id)
        selected_food_text = food_name
        page.session.store.set("food_name", selected_food_text)

        rebuild_body()

        harim_bottom_tip_sheet.open = False
        

    # 🟩 바텀시트
    harim_bottom_tip_sheet = dogdog.bottom_sheet(
        content=[
            dogdog.basic_text(value="사료 검색", size=25, weight="bold"),
            ft.Divider(),
            food_search_field,
            food_list_column
        ]
    )

    if harim_bottom_tip_sheet not in page.overlay:
        page.overlay.append(harim_bottom_tip_sheet)

    # 🟩 바텀시트 열기 함수
    # 🟦 수정:
    # 🟦 - 열릴 때 DB 전체 목록 불러오기
    def open_food_bottom_sheet(e):
        food_search_field.value = ""
        update_food_list("")
        harim_bottom_tip_sheet.open = True

    # 🟩 본문 전용 컬럼
    body_content = ft.Column(
        spacing=12,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        scroll=ft.ScrollMode.AUTO,
    )

    # 🟩 본문 다시 그리기
    def rebuild_body():
        body_content.controls = [
            dogdog.basic_text(value="현재 급여 중인 사료", weight="bold"),
            dogdog.picker_field(
                text=selected_food_text,
                on_click=open_food_bottom_sheet,
                icon=ft.Icons.KEYBOARD_ARROW_DOWN_ROUNDED
            ),
            dogdog.basic_text(value="사료 잔여량", weight="bold"),
            selected_food_weight
        ]

    rebuild_body()

    return build_screen_body([body_content])