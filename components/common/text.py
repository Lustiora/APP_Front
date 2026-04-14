import flet as ft

def basic_text(value, size=None, weight=None, color=None):
    if weight == "bold": weight = ft.FontWeight.BOLD
    return ft.Text(value=value, size=size, weight=weight, color=color, font_family="Pretendard")