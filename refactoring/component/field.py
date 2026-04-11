import flet as ft
import datetime


def picker_field(text, on_click=None, icon=None):
    # print(type(text))

    ### 폰트 색상 및 형식 조정
    font_color = ft.Colors.OUTLINE

    #### datetime.datetime 문자열 형식
    if type(text) == datetime.datetime:
        font_color = None
        text = text.strftime("%Y-%m-%d")
        # 2026-03-31 15:00:00.000Z -> 26-03-31

    ### 아이콘 사용 여부에 따른 레이아웃 조정
    if icon:
        contents = [
            ft.Text(
                value=text, color=font_color, expand=True,
                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS
            ),
            ft.Icon(icon=icon, color=ft.Colors.OUTLINE)
        ]
    else:
        contents = [
            ft.Text(
                value=text, color=font_color, expand=True,
                max_lines=1, overflow=ft.TextOverflow.ELLIPSIS
            )
        ]

    ### 반환 레이아웃
    return ft.Container(
        height=48,
        border=ft.Border.all(color=ft.Colors.OUTLINE_VARIANT),
        border_radius=10,
        padding=ft.Padding.only(left=14, right=14),
        on_click=on_click,
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=contents # type: ignore
        )
    )