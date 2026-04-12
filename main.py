# -------------------------------------------------------------------------------------------------------
import flet as ft
import views as views
test_page = ""
# -------------------------------------------------------------------------------------------------------
# flet build apk --verbose --compile-app --compile-packages --arch arm64-v8a
# -------------------------------------------------------------------------------------------------------
test_page = "Browser" # APP Test 시 주석 처리
# -------------------------------------------------------------------------------------------------------
class Front_dogdog:
    def __init__(self, page):
        # -----------------------------------------------------------------------------------------------
        # Default Page Value
        # -----------------------------------------------------------------------------------------------
        self.page = page
        page.bgcolor = "#FFFFFF"
        page.title = "Dog Dog"
        page.spacing = 0
        page.padding = 20
        page.theme_mode = ft.ThemeMode.LIGHT
        page.fonts = {"Pretendard": "fonts/Pretendard-Regular.otf"}
        page.theme = ft.Theme(
            font_family="Pretendard",
            color_scheme=ft.ColorScheme(
                primary=ft.Colors.BLACK,
                on_primary=ft.Colors.WHITE,
                surface=ft.Colors.WHITE,
                on_surface=ft.Colors.BLACK,
                on_surface_variant=ft.Colors.BLACK,
        ))
        # -----------------------------------------------------------------------------------------------
        # Front Page
        # -----------------------------------------------------------------------------------------------
        self.main_column = ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
        self.layout = ft.Container(expand=True, on_click=self.page_click, content=self.main_column)
        page.add(self.layout)
        # -----------------------------------------------------------------------------------------------
        # Dummy Focus Field
        # -----------------------------------------------------------------------------------------------        
        self.focus_field = ft.TextField(
            border_color=ft.Colors.TRANSPARENT, height=0, opacity=0,
            focus_color=ft.Colors.TRANSPARENT, read_only=True
        )
        # -----------------------------------------------------------------------------------------------
        # First Page
        # -----------------------------------------------------------------------------------------------
        self.load_page(page_name="sign_up")
    # ---------------------------------------------------------------------------------------------------
    # Dummy Focus Field Event
    # ---------------------------------------------------------------------------------------------------  
    async def page_click(self, e):
        if self.focus_field:
            await self.focus_field.focus()
            self.page.update()
    # ---------------------------------------------------------------------------------------------------
    # Page Load
    # ---------------------------------------------------------------------------------------------------
    def load_page(self, page_name):
        basic_content , self.focus_field = views.on_boarding_tile(
            page=self.page, content_page=page_name, change_page_callback=self.load_page
        )
        self.main_column.controls = basic_content # type: ignore
        self.page.update()
# -------------------------------------------------------------------------------------------------------
def main(page: ft.Page):
    front_end = Front_dogdog(page=page)
# -------------------------------------------------------------------------------------------------------
if test_page == "Browser":
    import logging, warnings
    level=logging.INFO
    logging.basicConfig(level=level)
    warnings.filterwarnings(action="ignore")
    if __name__ == "__main__":
            import webbrowser, os
            if os.getenv(key="FLET_NO_BROWSER"):
                webbrowser.open = lambda *args: None
            ft.run(main=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=34636)
else:
    if __name__ == "__main__":
        ft.run(main=main, assets_dir="assets")