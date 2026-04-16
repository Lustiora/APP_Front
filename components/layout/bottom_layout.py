import flet as ft
import components as dogdog

def continue_button(on_click=None):
    return ft.Container(
        expand=9,
        height=50,
        on_click=on_click,
        bgcolor=ft.Colors.YELLOW,
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=10,
        alignment=ft.Alignment.CENTER,
        content=ft.Text(
            value="Continue",
            size=14,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.BLACK,
        )
    )

def arrow_back(on_click=None):
    return ft.Container(
        expand=1,
        on_click=on_click,
        content=ft.Icon(
            icon=ft.Icons.ARROW_BACK_IOS,
            size=22,
        ),
    )

def bottom_appbar(appbar_button_list:list):
    return ft.BottomAppBar(
        padding=0,
        height=80,
        bgcolor="#FFFFFF",
        content=ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Divider(height=1),
                ft.Row(controls=appbar_button_list, expand=True, spacing=0)
    ]))

def home_bottom_appbar(new_view, appbar_status, floating_btn_event):
    def appbar_button(icon, text, on_click):
        if icon is None and text is None:
            return ft.Container(expand=True)
        return ft.Container(
            padding=0,
            expand=True,
            ink=True,
            on_click=on_click,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
                controls=[
                    ft.Icon(icon=icon, color=ft.Colors.GREY_400, size=22),
                    dogdog.basic_text(value=text, size=12, color=ft.Colors.GREY_400),
                ],
            ),
        )

    def appbar_floating_button(icon, on_click):
        return ft.FloatingActionButton(
            offset=ft.Offset(0, 0.2),
            scale=1.3,
            content=ft.Image(
                src=icon,
                fit=ft.BoxFit.COVER,
            ),
            bgcolor=ft.Colors.TRANSPARENT,
            shape=ft.CircleBorder(),
            elevation=0,
            hover_elevation=0,
            highlight_elevation=0,
            focus_elevation=0,
            splash_color=ft.Colors.TRANSPARENT,
            hover_color=ft.Colors.TRANSPARENT,
            focus_color=ft.Colors.TRANSPARENT,
            on_click=on_click,
        )
    
    def appbar_on_change(e, on_change_page):
        floating_btn_event(f"/{on_change_page}") # type: ignore

    appbar_button_list = [appbar_button(
        icon=icon, text=text, on_click=on_click) for icon, text, on_click in appbar_status]
    new_view.bottom_appbar = bottom_appbar(appbar_button_list=appbar_button_list)
    new_view.floating_action_button = appbar_floating_button(
        icon="skeleton.png", on_click=lambda e: appbar_on_change(e, "shop"))
    new_view.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED