import flet as ft
from components import build_screen_body
import component as dogdog


def build_view(page: ft.Page):
    ####################################################################################################
    ### 알레르기
    ####################################################################################################
    def on_allergy_change(e):
        if allergy.visible:
            page.session.store.set("allergy", e.control.value)
        else:
            if page.session.store.get("allergy"):
                page.session.store.remove("allergy")

    allergy = dogdog.input_textfield(hint_text="반려동물의 알레르기를 적어주세요", max_length=None, on_change=on_allergy_change) # type: ignore
    allergy.visible = False

    def on_allergy_radio_change(e):
        if e.control.value == "yes":
            allergy.visible = True
        else:
            allergy.visible = False
            if page.session.store.get("allergy"):
                page.session.store.remove("allergy")

    allergy_radio = dogdog.radio_group(
        value="no",
        on_change=on_allergy_radio_change,
        contents=[
            ft.Radio(value="yes", label="있어요"),
            ft.Radio(value="no", label="없어요"),
        ]
    )

    if page.session.store.get("allergy"):
        allergy.visible = True
        allergy_radio.value = "yes"
        allergy.value = page.session.store.get("allergy") # type: ignore

    ####################################################################################################
    ### 질병
    ####################################################################################################
    def on_disease_change(e):
        if allergy.visible:
            page.session.store.set("disease", e.control.value)
        else:
            if page.session.store.get("disease"):
                page.session.store.remove("disease")

    disease = dogdog.input_textfield(hint_text="반려동물의 질병을 적어주세요", max_length=None, on_change=on_disease_change) # type: ignore
    disease.visible = False

    def on_disease_radio_change(e):
        if e.control.value == "yes":
            disease.visible = True
        else:
            disease.visible = False
            if page.session.store.get("disease"):
                page.session.store.remove("disease")

    disease_radio = dogdog.radio_group(
        value="no",
        on_change=on_disease_radio_change,
        contents=[
            ft.Radio(value="yes", label="있어요"),
            ft.Radio(value="no", label="없어요"),
        ]
    )

    if page.session.store.get("disease"):
        disease.visible = True
        disease_radio.value = "yes"
        disease.value = page.session.store.get("disease") # type: ignore

    body_controls = [
        dogdog.basic_text(value="알레르기", weight="bold"),
        allergy_radio,
        allergy,

        dogdog.basic_text(value="질병", weight="bold"),
        disease_radio,
        disease
    ]

    # ─────────────────────────────────────────────
    # 🟦 체크: 본문만 반환
    # ─────────────────────────────────────────────
    return build_screen_body(body_controls)