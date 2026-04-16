# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
import api.full_query as full_query
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
    main_container_content = []
    home_background , top_banner = dogdog.home_layout(page=page, view="feeding") # type: ignore
    def appbar_on_change(e, on_change_page):
        change_page_callback(f"/{on_change_page}") # type: ignore
    appbar_status = [
        # Icon , Text , On_click
        (ft.Icons.HOME, "Home", lambda e:appbar_on_change(e, "home")),
        (ft.Icons.CALENDAR_MONTH, "Log", lambda e:appbar_on_change(e, "log")),
        (None, None, None),
        (ft.Icons.MESSENGER_OUTLINE_ROUNDED, "Contents", lambda e:appbar_on_change(e, "contents")),
        (ft.Icons.PERSON_OUTLINE, "MyPage", lambda e:appbar_on_change(e, "mypage")),
    ]
    # ---------------------------------------------------------------------------------------------------
    # On Boarding Tile Link
    # ---------------------------------------------------------------------------------------------------
    if content_page == "/home":
        home_background , top_banner , body_column = dogdog.home_layout( # type: ignore
            page=page, pet_list=full_query.Home.pet_list, view="home") # type: ignore
        main_container_content.append(top_banner)
        main_container_content.append(body_column)
        body_column.controls.append(
        dogdog.content_container(
            content_list=domains.now_history(page=page),
            on_click=lambda e:appbar_on_change(e, "history")
        ))
        body_column.controls.append(
            dogdog.content_container(
                content_list=domains.feeding_food_count(page=page),
                on_click=lambda e:appbar_on_change(e, "feeding")
        ))
        body_column.controls.append(domains.fast_menu_grid(page=page))
    elif content_page == "/feeding":
        home_background , top_banner = dogdog.home_layout(page=page, view="feeding")  # type: ignore
        main_container_content.append(top_banner)
        main_container_content.append(
            domains.feeding_tabs_view(
                page=page, customer_food_detail=full_query.Home.customer_food_detail))
    return home_background , main_container_content , appbar_status