import flet as ft
import components as dogdog
import domains

def shop_feeding_guide(page: ft.Page):
    storage = page.session.store
    feeding_guide = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=0,
        controls=[
            ft.Row(controls=[
                dogdog.basic_text(
                    value=f"{storage.get('customer_pet_name')}에게 딱 맞춘 하루 권장량",
                    size=18, weight="bold")]),
            ft.Row(margin=ft.margin.only(bottom=10), alignment=ft.MainAxisAlignment.END, controls=[ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.END, spacing=0, controls=[
                ft.Container(scale=0.8,
                    width=25, height=25, ink=True, on_click=None, border_radius=25, bgcolor=ft.Colors.GREY_300,
                    content=ft.Icon(icon=ft.Icons.QUESTION_MARK, color=ft.Colors.WHITE, size=20)),
                    dogdog.basic_text("제품의 열량 4005kcal/kg", weight="bold", size=12, color=ft.Colors.GREY_600)
            ])]),
            ft.Column(horizontal_alignment=ft.CrossAxisAlignment.CENTER, controls=[
                ft.Image(src="speech_bubble.png", height=100, color="#FEF3B9"),
                dogdog.basic_text("40g", weight="bold", size=40),
            ], spacing=-90),
            ft.Image(src="dogbowl.png", height=100, margin=ft.margin.only(top=20)),
            dogdog.basic_text("아침 39g, 저녁 39g", weight="bold", color=ft.Colors.GREY_600),
            dogdog.basic_text("총 310kcal", weight="bold", color=ft.Colors.GREY_600)
    ])

    return ft.Container(
        padding=ft.padding.only(left=20, right=20, top=20),
        bgcolor="#ffffff",
        content=feeding_guide # type: ignore
    )

def product_guide(page: ft.Page):

    guide_container = ft.Container(
        height=300,
        alignment=ft.Alignment.CENTER,
        content=ft.Row([
            
        ])
    )

    content_column = [
        ft.Divider(),
        dogdog.basic_text("추천사료", size=18, weight="bold"),
        guide_container,
        ft.Divider(),
    ]

    return ft.Container(
        padding=ft.Padding.only(left=5, right=5),
        bgcolor="#ffffff",
        content=ft.Column(controls=content_column) # type: ignore
    )