# -------------------------------------------------------------------------------------------------------
import flet as ft
import domains as domains
import components as dogdog
import datetime
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

    menu_style = ft.ButtonStyle(
        bgcolor="#FBEEAC", padding=ft.Padding.only(left=35), text_style=ft.TextStyle(size=14, weight=ft.FontWeight("w600"))
    )

    pet_list = ft.Dropdown(
        height=50,
        text_style=ft.TextStyle(weight=ft.FontWeight("bold")),
        text_align=ft.TextAlign.END,
        trailing_icon=ft.Icons.KEYBOARD_ARROW_DOWN,
        selected_trailing_icon=ft.Icons.KEYBOARD_ARROW_UP,
        value="1",
        menu_style=ft.MenuStyle(bgcolor="#DBD19F", padding=0),
        border_width=0,
        width=105,
        options=[
            ft.DropdownOption(key="1", text="츄츄", style=menu_style),
            ft.DropdownOption(key="2", text="토끼", style=menu_style),                                
        ]
    )

    background = ft.Container(
        bgcolor="#FEF3B9", height=180, border_radius=ft.BorderRadius.only(bottom_left=30, bottom_right=30),
    )

    now_history = ft.Container(
        width=360,
        padding=20,
        border_radius=ft.border_radius.all(10),
        border=ft.Border.all(width=2, color=ft.Colors.GREY_200),
        shadow=ft.BoxShadow(
            blur_radius=2, color=ft.Colors.GREY_100,
            offset=ft.Offset(x=0, y=3)),
        bgcolor="#ffffff",
        content=ft.Column(
            spacing=20,
            controls=[
                ft.Row([
                        dogdog.basic_text(value="오늘의 기록", size=18, weight="bold"),
                        dogdog.basic_text(value=datetime.datetime.now().strftime("%Y.%m.%d"), size=14, weight="bold", color=ft.Colors.GREY_700),
                ]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.TextButton(content=dogdog.basic_text("급여량: 100g", size=12), style=ft.ButtonStyle(bgcolor="#EEEEEE"), width=100),
                        ft.TextButton(content=dogdog.basic_text("음수량: 100ml", size=12), style=ft.ButtonStyle(bgcolor="#EEEEEE"), width=100),
                        ft.TextButton(content=dogdog.basic_text("산책: 60분", size=12), style=ft.ButtonStyle(bgcolor="#EEEEEE"), width=100),
                ]),
                ft.Column(
                    controls=[
                        dogdog.basic_text(value="목표 활동량", size=14, color=ft.Colors.GREY_700, weight="bold"),
                        ft.ProgressBar(
                            height=10,
                            value=0 / 90 if 90 else 0,
                            bgcolor=ft.Colors.GREY_300,
                            color=ft.Colors.YELLOW_600,
                            border_radius=10,
                        ),
                        dogdog.basic_text(
                            value=f"{0}/{90}{"분"}",
                            size=13,
                            color=ft.Colors.GREY_500,
                            weight="bold",
                        ),
                    ],
                ),
                ft.Column(
                    controls=[
                        dogdog.basic_text(value="목표 칼로리", size=14, color=ft.Colors.GREY_700, weight="bold"),
                        ft.ProgressBar(
                            height=10,
                            value=0 / 310 if 310 else 0,
                            bgcolor=ft.Colors.GREY_300,
                            color=ft.Colors.YELLOW_600,
                            border_radius=10,
                        ),
                        dogdog.basic_text(
                            value=f"{0}/{310}{"kcal"}",
                            size=13,
                            color=ft.Colors.GREY_500,
                            weight="bold",
                        ),
                    ],
                ),
            ]
        )
    )
    header_controls = [
        ft.Container(content=ft.Row(spacing=10, controls=[
            ft.Image(src="dogclay.png", width=80),
            ft.Column(spacing=0, controls=[
                ft.Row(controls=[pet_list], margin=ft.margin.only(left=-14, bottom=-10)),
                dogdog.basic_text("(4년 9개월,♀️)", weight="bold", color=ft.Colors.OUTLINE)
        ])])),
        ft.IconButton(icon=ft.Icons.NOTIFICATIONS_NONE, icon_color=ft.Colors.OUTLINE, icon_size=30)
    ]

    header_container = ft.Container(
        padding=ft.Padding.only(top=60, left=20, right=20),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=header_controls
    ))

    body_column = ft.Column(spacing=20, scroll=ft.ScrollMode.HIDDEN, expand=True)
        
    main_container = ft.Container(expand=True, content=ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            header_container,
            body_column
    ]))

    body_column.controls.append(now_history)
    body_column.controls.append(now_history)
    body_column.controls.append(now_history)

    root_stack = ft.Stack(controls=[background, main_container], expand=True)

    new_view = ft.View(padding=0, spacing=0, bgcolor="#FFFFFF", controls=[root_stack])

    def nav_item_rules(icon, label, selected=False, on_click=None):
        return ft.Container(
            expand=True,
            height=74,
            alignment=ft.Alignment(0, 0),
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
        elevation=0,
        padding=0,
        content=ft.Container(
            bgcolor="#FFFFFF",
            height=82,
            padding=ft.padding.only(left=10, right=10, top=0, bottom=2),
            content=ft.Column(
                spacing=0,
                controls=[
                    # 상단 회색 선 전체 표시
                    ft.Container(
                        height=1,
                        bgcolor=ft.Colors.GREY_300,
                    ),
                    ft.Container(
                        expand=True,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=bottom_nav_items(None,None),
                        ),
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