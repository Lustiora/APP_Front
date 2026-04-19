import flet as ft

class Popup:
    def __init__(self, page: ft.Page):
        self.page = page

        self.main_quit = ft.AlertDialog(
            modal=True,
            title=ft.Text("Quit"),
            content=ft.Text("Exit?"),
            actions_alignment = ft.MainAxisAlignment.END,
            actions=[
                ft.TextButton("OK", on_click=self.exit, autofocus=True),
                ft.TextButton("Cancel", on_click=self.show_exit_close)
            ]
        )
        page.overlay.append(self.main_quit) if self.main_quit in page.overlay else None

        self.api_insert_dialog = ft.AlertDialog(
            modal=True,
            bgcolor=ft.Colors.TRANSPARENT,
            content=ft.Row(alignment=ft.MainAxisAlignment.CENTER,
                width=20, controls=[ft.ProgressRing(color=ft.Colors.BLUE_400)])
        )
        page.overlay.append(self.api_insert_dialog) if self.api_insert_dialog in page.overlay else None

    def show_open(self, e): 
        self.page.show_dialog(self.api_insert_dialog)
        self.page.update()

    def show_close(self, e): 
        self.page.pop_dialog()
        self.page.update()
    
    def show_exit_open(self, e):
        self.page.show_dialog(self.main_quit)
        self.page.update()

    async def exit(self, e):
        await self.page.window.close()
        await self.page.window.destroy()
    
    def show_exit_close(self, e):
        self.page.pop_dialog()
        self.page.go("/home")
        self.page.update()