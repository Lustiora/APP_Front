# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
from api.full_query import Home
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
    
    customer_detail = Home.customer_food_detail
    main_container_content = []
    home_background , top_banner = dogdog.home_layout(page=page, view="feeding") # type: ignore
    def appbar_on_change(e, on_change_page):
        change_page_callback(on_change_page) # type: ignore
    # ---------------------------------------------------------------------------------------------------
    # Home Tile Link
    # ---------------------------------------------------------------------------------------------------
    if content_page == "/home":
        home_background , top_banner , body_column = dogdog.home_layout( # type: ignore
            page=page, pet_list=Home.pet_list, view="home") # type: ignore
        main_container_content.append(top_banner)
        main_container_content.append(body_column)
        body_column.controls.append(
            dogdog.content_container(
                content_list=domains.now_history(page=page),
                on_click=lambda e:appbar_on_change(e, "/history")
        ))
        body_column.controls.append(
            dogdog.content_container(
                content_list=domains.feeding_food_count(page=page, customer_detail=customer_detail),
                on_click=lambda e:appbar_on_change(e, "/feeding")
        ))
        body_column.controls.append(domains.fast_menu_grid(page=page, customer_detail=customer_detail))
    elif content_page == "/log":
        home_background , top_banner = dogdog.home_layout(page=page, text="Log")  # type: ignore
        main_container_content.append(top_banner)
    elif content_page == "/shop":
        home_background , top_banner = dogdog.home_layout(page=page, text="Shop Test")  # type: ignore
        main_container_content.append(top_banner)
    elif content_page == "/contents":
        home_background , top_banner = dogdog.home_layout(page=page, text="Content")  # type: ignore
        main_container_content.append(top_banner)
    elif content_page == "/mypage":
        home_background , top_banner = dogdog.home_layout(page=page, text="My Page")  # type: ignore
        main_container_content.append(top_banner)
    elif content_page == "/history":
        home_background , top_banner = dogdog.home_layout(page=page, text="History")  # type: ignore
        main_container_content.append(top_banner)
    elif content_page == "/feeding":
        home_background , top_banner = dogdog.home_layout(page=page, text="급여 중인 제품")  # type: ignore
        main_container_content.append(top_banner)
        main_container_content.append(domains.feeding_tabs_view(
            page=page, customer_food_detail=customer_detail))
    elif content_page == "/feeding_edit":
        home_background , top_banner = dogdog.home_layout(page=page, text="제품 정보 변경")  # type: ignore
        main_container_content.append(top_banner)
        main_container_content.append(domains.feeding_edit_view(page=page, view="edit"))
    elif content_page == "/feeding_add":
        home_background , top_banner = dogdog.home_layout(page=page, text="제품 등록")  # type: ignore
        main_container_content.append(top_banner)
        main_container_content.append(domains.feeding_edit_view(page=page, view="add"))
    elif content_page == "/notification":
        home_background , top_banner = dogdog.home_layout(page=page, text="알림")  # type: ignore
        main_container_content.append(top_banner)

    return home_background , main_container_content