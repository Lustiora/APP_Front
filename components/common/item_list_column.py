import flet as ft
import components as dogdog
import pg8000.dbapi as psycopg2

def db_connect():
    try:
        conn = psycopg2.connect(
            host="pg.nas6418.ddns.net", # type: ignore
            port=9934, # type: ignore
            database="Dogdog",
            user="dog_5",
            password="kosmo"
        )
    except psycopg2.OperationalError as Err:
        conn = None
    return conn

def item(list_key, list_value, select_key, select_value):
    is_checked = select_key == list_key
    return ft.Container(
        padding=ft.Padding.symmetric(vertical=14, horizontal=10),
        border_radius=10,
        bgcolor=ft.Colors.OUTLINE_VARIANT if is_checked else ft.Colors.WHITE,
        on_click=lambda e, list_key=list_key, list_value=list_value: select_value(list_key, list_value),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                dogdog.basic_text(value=list_value, weight="bold"),
                ft.Icon(
                    ft.Icons.CHECK,
                    color=ft.Colors.BLACK if is_checked else ft.Colors.TRANSPARENT,
                    size=18,
                )
            ]
        )
    )

def update_item_list(list_column, query_search, query_list, select_key, select_value, keyword=""):
    conn = None
    try:
        conn = db_connect()
        cursor = conn.cursor() # type: ignore
        if keyword.strip():
            cursor.execute(query_search, (f"%{keyword.strip()}%",))
        else:
            cursor.execute(query_list)
        rows = cursor.fetchall()
        conn.commit() # type: ignore
        cursor.close()
        list_column.controls.clear()
        if rows:
            for row in rows:
                list_column.controls.append(
                    item(list_key=row[0], list_value=row[1],
                        select_key=select_key, select_value=select_value)
                )
        else:
            list_column.controls = [
                ft.Container(content=dogdog.basic_text(value=f"검색 결과가 없습니다.", size=14))
            ]
    except Exception as e:
        if conn:
            conn.rollback() # type: ignore
            print(f"Search or List Query Error.\n{e}")
        else:
            list_column.controls = [
                ft.Container(
                    alignment=ft.Alignment(0, 0),
                    content=dogdog.basic_text(
                        value="\n\n서버에 접속할 수 없습니다.\n잠시 후 다시 시도해주세요.", weight="bold", size=14
                    )
                )
            ]

def dropdown_list(dropdown_menu, query_list, key):
    conn = None
    try:
        conn = db_connect()
        cursor = conn.cursor() # type: ignore
        cursor.execute(query_list,(key,))
        rows = cursor.fetchall()
        conn.commit() # type: ignore
        cursor.close()
        dropdown_menu.options.clear()
        if rows:
            for row in rows:
                dropdown_menu.options.append(
                    dogdog.dropdown_menu_option(key=row[0], text=f"{row[1]}g"),
                )
        else:
            dropdown_menu.options.append(
                dogdog.dropdown_menu_option(text="조회되는 내용이 없습니다."),
            )
    except:
        if conn:
            conn.rollback() # type: ignore
        print("List Query Error")
        return