import flet as ft

from components import build_screen_body
import component as dogdog

def build_view(page: ft.Page):

    def radio_on_change(e):
        page.session.store.set("radio_time", e.control.value)

    radio_time = dogdog.radio_group(
        value="30",
        on_change=radio_on_change,
        layout_type="column",
        spacing=12,
        contents=[
            ft.Radio(value="30", label="하루 30분 이상"),
            ft.Radio(value="60", label="하루 60분 이상"),
            ft.Radio(value="90", label="하루 90분 이상"),
        ]
    )
    if page.session.store.get("radio_time"):
        radio_time.value = page.session.store.get("radio_time")
    else:
        page.session.store.set("radio_time", "30")

    def breakfast_on_change(e):
        if e.control.value:
            page.session.store.set("breakfast", e.control.value)
        else:
            page.session.store.remove("breakfast")
    breakfast = ft.Checkbox(label="아침", on_change=breakfast_on_change)
    if page.session.store.get("breakfast"):
        breakfast.value = page.session.store.get("breakfast")

    def lunch_on_change(e):
        if e.control.value:
            page.session.store.set("lunch", e.control.value)
        else:
            page.session.store.remove("lunch")
    lunch = ft.Checkbox(label="점심", on_change=lunch_on_change)
    if page.session.store.get("lunch"):
        lunch.value = page.session.store.get("lunch")

    def dinner_on_change(e):
        if e.control.value:
            page.session.store.set("dinner", e.control.value)
        else:
            page.session.store.remove("dinner")
    dinner = ft.Checkbox(label="저녁", on_change=dinner_on_change)
    if page.session.store.get("dinner"):
        dinner.value = page.session.store.get("dinner")

    body_controls = [
        dogdog.basic_text("급여 시간", weight="bold"),
        breakfast,
        lunch,
        dinner,
        dogdog.basic_text("산책 시간", weight="bold"),
        radio_time,
    ]

    return build_screen_body(body_controls)