# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
import os
# -------------------------------------------------------------------------------------------------------
def main(page: ft.Page):
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

    home_background = ft.Container(
        bgcolor="#FEF3B9", height=150, border_radius=ft.BorderRadius.only(bottom_left=30, bottom_right=30),
    )

    now_history = dogdog.content_container(content_list=domains.now_history(page=page))
    feeding_food_count = dogdog.content_container(content_list=domains.feeding_food_count(page=page))
    
    def update_scale(e):
        base_height = 800.0
        body_scale = 0.87
        body_margin = -100
        if page.height < base_height: # type: ignore
            current_height = page.height if page.height > 0 else base_height # type: ignore
            scale_val = current_height / base_height # type: ignore
            body_column.scale = scale_val * body_scale if scale_val < 1.0 else body_scale
            body_column.margin = ft.margin.only(top=body_margin * scale_val if scale_val < 1.0 else body_margin)
            top_banner.padding = ft.padding.only(top=40 * scale_val if scale_val < 1.0 else 40)
            home_background.height = 160 * scale_val if scale_val < 1.0 else 160
            if e is not None: page.update()

    page.on_resize = update_scale
    
    body_column = ft.Column(spacing=15, expand=True)

    pet_list = {
        # pet_id : {nickname, birth_day, sex},
        1:{"nickname":"바둑이테", "birth_day":"2023-01-01", "sex":"1"},
        2:{"nickname":"누렁", "birth_day":"2022-01-01", "sex":"2"},
    }

    top_banner = dogdog.home_top_bar(page=page, pet_list=pet_list)
    
    update_scale(e=None)

    main_container = ft.Container(expand=True, padding=ft.Padding.only(left=10, right=10), 
        content=ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                top_banner,
                body_column
    ]))

    body_column.controls.append(now_history)
    body_column.controls.append(feeding_food_count)
    body_column.controls.append(domains.fast_menu_grid(page=page))


    root_stack = ft.Stack(controls=[home_background, main_container], expand=True)

    new_view = ft.View(padding=0, spacing=0, bgcolor="#FFFFFF", controls=[root_stack])

    def nav_item_rules(icon, label, selected=False, on_click=None):
        return ft.Container(
            expand=True,
            height=74,
            on_click=on_click,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=3,
                controls=[
                    ft.Icon(
                        icon,
                        color=ft.Colors.BLACK if selected else ft.Colors.GREY_400,
                        size=22,
                    ),
                    ft.Text(
                        label,
                        color=ft.Colors.BLACK if selected else ft.Colors.GREY_400,
                        size=10,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER,
                        max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS,
                        no_wrap=True,
                    ),
                ],
            ),
        )
    
    def bottom_nav_items(selected_index, on_tab_change):
        tabs = [
            (ft.Icons.HOME, "Home"),
            (ft.Icons.CALENDAR_MONTH, "Log"),
            (None, None),  # 👉 FAB 자리
            (ft.Icons.MESSENGER_OUTLINE_ROUNDED, "Contents"),
            (ft.Icons.PERSON_OUTLINE, "MyPage"),
        ]

        controls = []

        for i, (icon, label) in enumerate(tabs):
            # 👉 가운데 FAB 자리
            if icon is None:
                controls.append(ft.Container(width=72))
                continue

            # 👉 실제 탭 index 계산
            tab_index = i if i < 2 else i - 1

            controls.append(
                nav_item_rules(
                    icon,
                    label,
                    selected=(selected_index == tab_index),
                    on_click=lambda e, idx=tab_index: on_tab_change(idx)
                    if on_tab_change
                    else None,
                )
            )

        return controls # 👉 이거 없으면 나브 아이템 전멸 
    
    new_view.bottom_appbar = ft.BottomAppBar(
        bgcolor="#FFFFFF",
        padding=0,
        content=ft.Container(
            bgcolor="#FFFFFF",
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Divider(height=1),
                    ft.Row(
                        controls=bottom_nav_items(None,None),
                    ),
                ],
            ),
        ),
    )

    page.views.append(new_view)
    page.update()

import logging, warnings
level=logging.INFO
logging.basicConfig(level=level)
warnings.filterwarnings(action="ignore")
if __name__ == "__main__":
    import webbrowser, os
    if os.getenv(key="FLET_NO_BROWSER"):
        webbrowser.open = lambda *args: None
    ft.run(main=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=34636)