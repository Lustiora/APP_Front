import flet as ft

def image_circle(event, size, src=None):
    return ft.Container(
        width=size,
        height=size,
        bgcolor=ft.Colors.BLACK,
        shape=ft.BoxShape.CIRCLE, # 원형 1
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(0.2, ft.Colors.OUTLINE_VARIANT),
            offset=ft.Offset(0, -4),
        ),
        on_click=event,
        image=ft.DecorationImage( # 컨테이너에 이미지를 추가하기위한 옵션
            src=src,
            fit=ft.BoxFit.COVER # 원형 2
        ),
    )
