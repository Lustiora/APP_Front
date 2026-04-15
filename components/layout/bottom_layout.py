import flet as ft

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
        margin=ft.margin.only(top=-5),
        bgcolor="#FFFFFF",
        content=ft.Column(
            controls=[
                ft.Divider(height=1),
                ft.Row(controls=appbar_button_list)
    ]))