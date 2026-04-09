import flet as ft
from components.layout.top_bar import top_bar
from views.home.home import home_view
from views.logs.log import log_view
from views.onboarding.user_basic_info import user_basic_info_view

def main(page: ft.Page):
    page.bgcolor = ft.Colors.WHITE
    page.padding = 0
    page.spacing = 0

    is_signed_up = False
    current_index = 0

    app_shell = ft.Container(expand=True)

    def get_main_body(index: int):
        if index == 0:
            print("0")
            return home_view(page)
        elif index == 1:
            print("1")
            return log_view(page)
        elif index == 2:
            return ft.Text("샵 페이지 준비 중")
        elif index == 3:
            return ft.Text("콘텐츠 페이지 준비 중")
        elif index == 4:
            return ft.Text("마이페이지 준비 중")
        return ft.Text("페이지 준비 중")

    def handle_signup_success():
        nonlocal is_signed_up
        is_signed_up = True
        render_app()

    # onboarding
    def build_onboarding_layout():
        bottom_button = ft.Container(
            border_radius=9,
            width=float("inf"),
            height=50,
            bgcolor=ft.Colors.YELLOW_600,
            on_click= lambda e:handle_signup_success(),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=ft.Text("Continue", color=ft.Colors.WHITE, size=20))
            )
        return ft.Container(
            expand=True,
            bgcolor=ft.Colors.WHITE,
            alignment=ft.Alignment(0, 1),
            # padding=ft.padding.only(bottom=20),
            padding=20,
            content=ft.Column(
                controls=[
                    user_basic_info_view(page, on_continue=handle_signup_success),
                    bottom_button
                ]
            )
        )

    # main
    def build_main_layout():
        body = ft.Container(
            expand=True,
            content=get_main_body(current_index)
        )

        nav = ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.YELLOW_600,
            inactive_color=ft.Colors.BROWN_200,
            active_color=ft.Colors.BROWN_700,
            selected_index=current_index,
            on_change=lambda e: render_app(e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
                ft.NavigationBarDestination(icon=ft.Icons.CALENDAR_MONTH, label="Log"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.FOOD_BANK_ROUNDED,
                    selected_icon=ft.Icons.SHOPPING_CART,
                    label="Shop",
                ),
                ft.NavigationBarDestination(icon=ft.Icons.MESSENGER_OUTLINE_ROUNDED, label="Contents"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.PERSON_OUTLINE,
                    selected_icon=ft.Icons.PERSON,
                    label="MyPage"
                ),
            ],
        )

        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                top_bar(),
                body,
                nav,
            ],
        )

    def render_app(index=0):
        nonlocal current_index
        current_index = index
        if is_signed_up:
            app_shell.content = build_main_layout()
        else:
            app_shell.content = build_onboarding_layout()

        page.update()

    page.add(app_shell)
    render_app()

if __name__ == "__main__":
    import webbrowser
    import os

    if os.getenv("FLET_NO_BROWSER"):
        webbrowser.open = lambda *args, **kwargs: None

    ft.run(
        main,
        assets_dir="assets",
        view=ft.AppView.WEB_BROWSER,
        port=34636,
    )