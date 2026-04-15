# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
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
    # Mobile View Scale Update Event
    # ---------------------------------------------------------------------------------------------------
    def update_scale(e):
        base_height = 800.0
        body_scale = 0.92
        body_margin = -80
        top_padding = 40
        if page.height < base_height: # type: ignore
            current_height = page.height if page.height > 0 else base_height # type: ignore
            scale_val = current_height / base_height # type: ignore
            body_column.scale = scale_val * body_scale if scale_val < 1.0 else body_scale
            body_column.margin = ft.margin.only(
                top=body_margin * scale_val if scale_val < 1.0 else body_margin
            )
            top_banner.padding = ft.padding.only(
                top=top_padding * scale_val if scale_val < 1.0 else top_padding
            )
            home_background.height = 160 * scale_val if scale_val < 1.0 else 160
            if e is not None: page.update()
    page.on_resize = update_scale
    # ---------------------------------------------------------------------------------------------------    
    # Page Background
    # ---------------------------------------------------------------------------------------------------
    home_background = ft.Container(
        bgcolor="#FEF3B9", height=150, border_radius=ft.BorderRadius.only(bottom_left=30, bottom_right=30),
    )
    # ---------------------------------------------------------------------------------------------------
    # Page Top Banner
    # ---------------------------------------------------------------------------------------------------
    pet_list = {
        # pet_id : {nickname, birth_day, sex},
        1:{"nickname":"바둑이테", "birth_day":"2023-01-01", "sex":"1"},
        2:{"nickname":"누렁", "birth_day":"2022-01-01", "sex":"2"},
    }
    top_banner = dogdog.home_top_bar(page=page, pet_list=pet_list) # + pet_profile_image
    # ---------------------------------------------------------------------------------------------------
    # Page Body
    # ---------------------------------------------------------------------------------------------------
    body_column = ft.Column(spacing=15, expand=True)
    main_container = ft.Container(expand=True, padding=ft.Padding.only(left=10, right=10), 
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                top_banner,
                body_column
    ]))
    # ---------------------------------------------------------------------------------------------------
    # Page Body List (Home)
    # ---------------------------------------------------------------------------------------------------
    body_column.controls.append(
        dogdog.content_container(
            content_list=domains.now_history(page=page),
            on_click=lambda _:print("history")
    ))
    body_column.controls.append(
        dogdog.content_container(
            content_list=domains.feeding_food_count(page=page),
            on_click=lambda _:print("feeding")
    ))
    body_column.controls.append(domains.fast_menu_grid(page=page))
    # ---------------------------------------------------------------------------------------------------
    # Page View
    # ---------------------------------------------------------------------------------------------------
    new_view = ft.View(
        padding=0, spacing=0, bgcolor="#FFFFFF", controls=[
            ft.Stack(controls=[home_background, main_container], expand=True)
        ]
    )
    page.views.append(new_view)
    # ---------------------------------------------------------------------------------------------------
    # Bottom Appbar
    # ---------------------------------------------------------------------------------------------------
    appbar_status = [
        # Icon , Text , Event
        (ft.Icons.HOME, "Home"),
        (ft.Icons.CALENDAR_MONTH, "Log"),
        (None, None),
        (ft.Icons.MESSENGER_OUTLINE_ROUNDED, "Contents"),
        (ft.Icons.PERSON_OUTLINE, "MyPage"),
    ]
    appbar_button_list = [dogdog.appbar_button(
        icon=icon, text=text, on_click=lambda _:print(text)) for icon, text in appbar_status
    ]
    new_view.bottom_appbar = dogdog.bottom_appbar(appbar_button_list=appbar_button_list)
    new_view.floating_action_button = dogdog.appbar_floating_button(
        icon="skeleton.png", on_click=lambda _: print("shop")
    )
    new_view.floating_action_button_location = (ft.FloatingActionButtonLocation.CENTER_DOCKED)
    # ---------------------------------------------------------------------------------------------------
    update_scale(e=None)
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