import flet as ft

class Popup:
    def __init__(self, page: ft.Page):
        self.page = page
        self.api_insert_dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.TRANSPARENT,
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                width=20, controls=[ft.ProgressRing(color=ft.Colors.BLUE_400)])
        )
        page.overlay.append(self.api_insert_dialog)
        self.time = 0.1

    async def show_open(self, e): 
        self.page.show_dialog(self.api_insert_dialog)
        self.page.update()

    async def show_close(self, e): 
        self.page.pop_dialog()
        self.page.update()