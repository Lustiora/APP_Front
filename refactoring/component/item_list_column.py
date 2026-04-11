import flet as ft
import refactoring.component as dogdog
import pg8000.dbapi as psycopg2

class DB:
    conn = psycopg2.connect(
        host="pg.nas6418.ddns.net",
        port=9934,
        database="Dogdog",
        user="dog_5",
        password="kosmo",
    )


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
                ),
            ],
        ),
    )

def update_item_list(list_column, query_search, query_list, select_key, select_value, keyword=""):
    rows = None
    try:
        conn = DB.conn
        cursor = conn.cursor()
        if keyword.strip():
            cursor.execute(query_search, (f"%{keyword.strip()}%",))
        else:
            cursor.execute(query_list)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
    except Exception as e:
        conn.rollback()
        print(f"Search or List Query Error.\n{e}")
    try:
        if rows:
            list_column.controls.clear()
            for row in rows:
                list_column.controls.append(
                    item(row[0], row[1], select_key, select_value)
                )
        else:
            list_column.controls = [
                ft.Container(dogdog.basic_text(f"검색 결과가 없습니다.", size=14))
            ]
    except Exception as err:
        list_column.controls = [
            ft.Container(
                alignment=ft.Alignment(0, 0),
                content=dogdog.basic_text(
                    "\n\n서버에 접속할 수 없습니다.\n잠시 후 다시 시도해주세요.", weight="bold", size=14
                )
            )
        ]
        print(err)

def dropdown_list(dropdown_menu, query_list, key):
    try:
        conn = DB.conn
        cursor = conn.cursor()
        cursor.execute(query_list,(key,))
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        if rows:
            dropdown_menu.options.clear()
            for row in rows:
                dropdown_menu.options.append(
                    dogdog.dropdown_menu_option(key=row[0], text=f"{row[1]}g"),
                )
    except:
        conn.rollback()
        print("List Query Error")
        return