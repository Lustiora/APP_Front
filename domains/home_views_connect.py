# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
# -------------------------------------------------------------------------------------------------------
class Api_push_Data:
    data = {}
# -------------------------------------------------------------------------------------------------------
def home_tile(page: ft.Page, content_page:str, change_page_callback=None):
    # ---------------------------------------------------------------------------------------------------
    # Default Value
    # ---------------------------------------------------------------------------------------------------
    popop = dogdog.Popup(page=page)
    storage = page.session.store.get
    def show_error(text:str):
        page.show_dialog(ft.SnackBar(content=ft.Text(value=text), open=True))
    # page.__top_view
    focus_field = ft.TextField(
            border_color=ft.Colors.TRANSPARENT, height=0, opacity=0,
            focus_color=ft.Colors.TRANSPARENT, read_only=True
    )
    # ---------------------------------------------------------------------------------------------------
    # On Boarding Tile Link
    # ---------------------------------------------------------------------------------------------------
    if content_page == "/home":
        content = domains.home(page=page)
    # ---------------------------------------------------------------------------------------------------
    # On Boarding Content and Dummy Focus Field Change
    # ---------------------------------------------------------------------------------------------------
    basic_content = [
        ft.Container(
            expand=True,
            padding=ft.Padding.only(top=20),
            content=ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                spacing=10,
                controls=content if isinstance(content, list) else [content] # type: ignore
            )
        ),
        focus_field
    ]
    return basic_content, focus_field