# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains
import time
test_page = ""
# -------------------------------------------------------------------------------------------------------
# flet build apk --verbose --compile-app --compile-packages --arch arm64-v8a
# -------------------------------------------------------------------------------------------------------
test_page = "Browser" # APP Build Test 시 주석 처리
# -------------------------------------------------------------------------------------------------------
class Front_dogdog:
    def __init__(self, page: ft.Page):
        # -----------------------------------------------------------------------------------------------
        # Default Page Value
        # -----------------------------------------------------------------------------------------------
        self.page = page
        page.title = "Dog Dog"
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
        page.on_route_change = self.on_route_change
        page.on_view_pop = self.handle_back
        self.is_onboarding_complete = True
        # -----------------------------------------------------------------------------------------------
        # Init First View
        # -----------------------------------------------------------------------------------------------
        page.views.clear()
        if self.is_onboarding_complete == False:
            page.go("/sign_up")
        else:
            page.go("/home")
    # ---------------------------------------------------------------------------------------------------
    # Route Change & Android OnBackPressedCallback Event
    # ---------------------------------------------------------------------------------------------------
    def on_route_change(self, e):
        route = e.route
        if len(self.page.views) > 1 and self.page.views[-2].route == route:
            self.page.views.pop()
            self.page.update()
        elif len(self.page.views) == 0 or self.page.views[-1].route != route:
            self.routing_view(page_name=route)
    def handle_back(self, e=None):
        if len(self.page.views) > 1:
            self.page.views.pop()
            self.page.go(self.page.views[-1].route)
    # ---------------------------------------------------------------------------------------------------
    # View Routing Event
    # ---------------------------------------------------------------------------------------------------  
    def routing_view(self, page_name):
        if self.is_onboarding_complete == False:
            basic_content, focus_field = domains.on_boarding_tile(
                page=self.page, content_page=page_name, change_page_callback=self.page.go
            )
            async def view_click(e):
                if focus_field:
                    await focus_field.focus()
                    self.page.update()
            main_column = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                expand=True, controls=basic_content # type: ignore
            )
            layout = ft.Container(expand=True, padding=20, on_click=view_click, content=main_column)
        else:
            basic_content, focus_field = domains.home_tile(
                page=self.page, content_page=page_name, change_page_callback=self.page.go
            )
            async def view_click(e):
                if focus_field:
                    await focus_field.focus()
                    self.page.update()
            main_column = ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                expand=True, controls=basic_content # type: ignore
            )
            content = ft.Container(expand=True, padding=20, on_click=view_click, content=main_column)
            background = ft.Container(
                bgcolor="#FEF3B9",
                height=200,
                border_radius=ft.BorderRadius.only(bottom_left=50, bottom_right=50),
            )
            layout = ft.Stack(expand=True, controls=[background, content])
        new_view = ft.View(
            route=page_name, padding=0, spacing=0, bgcolor="#FFFFFF", controls=[layout]
        )
        self.page.views.append(new_view)
        if page_name == "/sign_up_success":
            new_view.bgcolor = ft.Colors.YELLOW
            self.page.views.clear()
            self.page.views.append(new_view)
            time.sleep(1)
            self.page.views.clear()
            self.is_onboarding_complete = True
            self.page.go("/home")
        self.page.update()
# -------------------------------------------------------------------------------------------------------
def main(page: ft.Page): front_end = Front_dogdog(page=page)
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
    if __name__ == "__main__": ft.run(main=main, assets_dir="assets")