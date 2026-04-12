import flet as ft

def image_circle(event, size, src=None):
    return ft.Container(
        width=size,
        height=size,
        shape=ft.BoxShape.CIRCLE,
        shadow=ft.BoxShadow(
            spread_radius=2,
            blur_radius=20,
            color=ft.Colors.with_opacity(1, ft.Colors.OUTLINE_VARIANT),
            offset=ft.Offset(0, -4),
        ),
        on_click=event,
        image=ft.DecorationImage(src=src, fit=ft.BoxFit.COVER),
    )
