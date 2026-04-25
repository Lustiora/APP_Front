import flet as ft
import components as dogdog
import datetime

def now_log(page: ft.Page, popup, now_history):
    storage = page.session.store
    def history_event(e):
        popup.show_popup_close(e)
        if storage.get("select_log_date"):
            storage.remove("select_log_date")
        page.go("/history")

    now_history_content = now_history.content.content.controls # type: ignore
    now_history_content.clear()
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    history_title = dogdog.basic_text(f"오늘의 기록 : {now}", size=18, weight="bold")
    now_history_content.append(history_title)
    now_history_content.append(ft.Divider())
    for pet_log_numeric_id , details in list(storage.get("history").items()): # type: ignore
        if details["log_date"].split()[0] == now:
            now_history_content.append(dogdog.log_container(page, pet_log_numeric_id, details=details))

    if len(now_history_content) - 2 <= 0:
        now_history_content.append(ft.Container(
            padding=ft.Padding.only(right=10, left=10),
            width=3000,
            ink=True,
            height=50,
            border_radius=10,
            border=ft.Border.all(width=1, color=ft.Colors.GREY_300),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                dogdog.basic_text("오늘의 기록이 없어요 ㅠㅠ", size=14, color=ft.Colors.GREY_700),
        ])))
    history_page = ft.Row(alignment=ft.MainAxisAlignment.CENTER, controls=[
        ft.TextButton(content=dogdog.basic_text("더보기", size=14,color=ft.Colors.GREY_500), on_click=lambda e:history_event(e))
    ])
    now_history_content.append(history_page)