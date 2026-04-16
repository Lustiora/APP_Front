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
    # Customer Data
    # ---------------------------------------------------------------------------------------------------
    pet_list = {
        # pet_id : {nickname, birth_day, sex},
        1:{"nickname":"바둑이테", "birth_day":"2023-01-01", "sex":"1"},
        2:{"nickname":"누렁", "birth_day":"2022-01-01", "sex":"2"},
    }

    customer_food_detail = {
        # customer_food_id : product_detail
        4: {"thumbnail": "test_product_4.jpg",                  # 상품 이미지
            "total_weight": 5800,                               # 상품 총 무게 g
            "brand": "더리얼 독",                                 # 브랜드
            "product_name": "그레인프리 오븐베이크드 닭고기 시니어",  # 상품명
            "left_food_count": 24,                              # 남은 급여 횟수(현재 날짜로 환산 / 1회 : 1일)
            "left_intake": 800},                                # 남은 사료 무게 g
        14: {"thumbnail": "test_product_14.jpg",
            "total_weight": 1600,
            "brand": "더리얼 독",
            "product_name": "그레인프리 오븐베이크드 돼지 어덜트",
            "left_food_count": 12,
            "left_intake": 600},
        44: {"thumbnail": "test_product_44.jpg",
            "total_weight": 1600,
            "brand": "더리얼 독",
            "product_name": "그레인프리 크런치 소고기 시니어",
            "left_food_count": 17,
            "left_intake": 160},
        70: {"thumbnail": "test_product_70.jpg",
            "total_weight": 50,
            "brand": "더리얼 독",
            "product_name": "로우 돼지고기 어덜트",
            "left_food_count": 1,
            "left_intake": 25},
    }
    # ---------------------------------------------------------------------------------------------------
    # Page Top Banner
    # ---------------------------------------------------------------------------------------------------
    # home_background , top_banner , body_column = dogdog.main_top_bar(
    #     page=page, pet_list=pet_list, view="home") # + pet_profile_image
    home_background , top_banner = dogdog.main_top_bar(page=page, view="feeding")  # type: ignore
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
    main_container_content.append(domains.feeding_tabs_view(page=page, customer_food_detail=customer_food_detail))
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
    new_view = ft.View(
        padding=0, spacing=0, bgcolor="#FFFFFF", controls=[
            ft.Stack(controls=[home_background, main_container], expand=True)])
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
    appbar_button_list = [dogdog.appbar_button(
        icon=icon, text=text, on_click=on_click) for icon, text, on_click in appbar_status]
    new_view.bottom_appbar = dogdog.bottom_appbar(appbar_button_list=appbar_button_list)
    new_view.floating_action_button = dogdog.appbar_floating_button(
        icon="skeleton.png", on_click=lambda _: print("shop"))
    new_view.floating_action_button_location = (ft.FloatingActionButtonLocation.CENTER_DOCKED)
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