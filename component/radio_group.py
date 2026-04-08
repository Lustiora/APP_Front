import flet as ft

def radio_group(value, on_change, contents, layout_type=None):
    layout_content = ft.Row(
        spacing=20,
        controls=contents
    )
    if layout_type == "column":
        layout_content = ft.Column(
            spacing=20,
            controls=contents
        )
    return ft.RadioGroup(
        value=value,
        on_change=on_change,
        content=layout_content
    )