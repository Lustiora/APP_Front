# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
import api.full_query as full_query
# -------------------------------------------------------------------------------------------------------
def main(page: ft.Page):
    # ---------------------------------------------------------------------------------------------------
    # Default Page Value
    # ---------------------------------------------------------------------------------------------------
    page.title = "Dog Dog"
    page.spacing = 0
    page.padding = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#ffffff"
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

    # ---------------------------------------------------------------------------------------------------
    # Page Top Banner
    # ---------------------------------------------------------------------------------------------------
    # home_background , top_banner , body_column = dogdog.home_layout( # type: ignore
    #     page=page, pet_list=full_query.Home.pet_list, view="home")
    home_background , top_banner = dogdog.home_layout(page=page, view="feeding")  # type: ignore
    # ---------------------------------------------------------------------------------------------------
    # Page Body
    # ---------------------------------------------------------------------------------------------------
    main_container_content = []
    main_container = ft.Container(expand=True, padding=ft.Padding.only(left=10, right=10), 
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=main_container_content))
    main_container_content.append(top_banner)
    # ---------------------------------------------------------------------------------------------------
    # Page Body List (Exception Home)
    # ---------------------------------------------------------------------------------------------------
    main_container_content.append(domains.feeding_tabs_view(page=page, customer_food_detail=full_query.Home.customer_food_detail))
    # ---------------------------------------------------------------------------------------------------
    # main_container_content.append(body_column)
    # ---------------------------------------------------------------------------------------------------
    # Page Body List (Home)
    # ---------------------------------------------------------------------------------------------------
    # body_column.controls.append(
    #     dogdog.content_container(
    #         content_list=domains.now_history(page=page),
    #         on_click=lambda _:print("history")
    # ))
    # body_column.controls.append(
    #     dogdog.content_container(
    #         content_list=domains.feeding_food_count(page=page),
    #         on_click=lambda _:print("feeding")
    # ))
    # body_column.controls.append(domains.fast_menu_grid(page=page))
    # ---------------------------------------------------------------------------------------------------
    # Page Body List (Exception Home)
    # ---------------------------------------------------------------------------------------------------
    # body_column.controls.append(domains.feeding_view(page=page, customer_food_detail=customer_food_detail))
    # body_column.controls.append(domains.feeding_view(page=page))
    # ---------------------------------------------------------------------------------------------------
    # Page View
    # ---------------------------------------------------------------------------------------------------
    layout = ft.Stack(expand=True, controls=[home_background, main_container])
    new_view = ft.View(padding=0, spacing=0, bgcolor="#FFFFFF", controls=[layout])
    # ---------------------------------------------------------------------------------------------------
    # Bottom Appbar
    # ---------------------------------------------------------------------------------------------------
    appbar_status = [
        # Icon , Text , On_click
        (ft.Icons.HOME, "Home", lambda _:print("Home")),
        (ft.Icons.CALENDAR_MONTH, "Log", lambda _:print("Log")),
        (None, None, None),
        (ft.Icons.MESSENGER_OUTLINE_ROUNDED, "Contents", lambda _:print("Contents")),
        (ft.Icons.PERSON_OUTLINE, "MyPage", lambda _:print("MyPage")),
    ]
    dogdog.home_bottom_appbar(new_view, appbar_status)
    # ---------------------------------------------------------------------------------------------------
    page.views.append(new_view)
    page.update()
# -------------------------------------------------------------------------------------------------------
import logging, warnings
level=logging.INFO
logging.basicConfig(level=level)
warnings.filterwarnings(action="ignore")
if __name__ == "__main__":
    import webbrowser, os
    if os.getenv(key="FLET_NO_BROWSER"):
        webbrowser.open = lambda *args: None
    ft.run(main=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=34636)