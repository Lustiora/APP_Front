# pip install plyer dbus-python

from plyer import notification
import os, flet as ft
def main(page: ft.Page):
    app_name = '애플리케이션'
    title = '알람 제목!'
    message = '알림 메시지'
    ticker = '단문 메시지??'
    app_icon = os.path.join(os.getcwd(),'assets/icon.png')
    cmd_message = []
    def button_event(e):
        cmd_message.append(ft.Text("event"))
        try:
            notification.notify(
                title=title,
                message=message,
                app_name=app_name,
                ticker=ticker,
                app_icon=app_icon,
                # timeout=3,
                toast=True
            ) # type: ignore
        except Exception as err:
            cmd_message.append(ft.Text(str(err)))
    
    page.add(ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(expand=True, alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
            controls=cmd_message)
    ))
    cmd_message.append(ft.TextButton("버튼입니다", on_click=button_event))
    page.update()

import logging, warnings
level=logging.INFO
logging.basicConfig(level=level)
warnings.filterwarnings(action="ignore")
if __name__ == "__main__":
    import webbrowser, os
    if os.getenv(key="FLET_NO_BROWSER"):
        webbrowser.open = lambda *args: None
    ft.run(main=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=34636, web_renderer=ft.WebRenderer.CANVAS_KIT)