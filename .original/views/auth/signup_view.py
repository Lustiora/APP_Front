import flet as ft
import original.component as dogdog


def build_view(page: ft.Page):

    def email_on_change(e):
        page.session.store.set("email", e.control.value)
    def name_on_change(e):
        page.session.store.set("name", e.control.value)
    def password_on_change(e):
        page.session.store.set("password", e.control.value)

    email_input = dogdog.input_textfield(
        hint_text="example@gmail.com", max_length=None, on_change=email_on_change, input_type="email")
    name_input = dogdog.input_textfield(
        hint_text="닉네임", on_change=name_on_change)
    password_input = dogdog.input_textfield(
        hint_text="비밀번호", max_length=None, on_change=password_on_change, input_type="password")

    if page.session.store.get("email"):
        email_input.value = page.session.store.get("email")

    if page.session.store.get("name"):
        name_input.value = page.session.store.get("name")

    if page.session.store.get("password"):
        password_input.value = page.session.store.get("password")

    body_controls = [
        # ─────────────────────────────────────────────
        # 🟨 기존 주석/구조 유지
        # ─────────────────────────────────────────────
        ft.Container(height=8),
        dogdog.basic_text("이메일", weight="bold"),
        email_input,
        ft.Container(height=8),
        dogdog.basic_text("닉네임", weight="bold"),
        name_input,
        dogdog.basic_text("비밀번호", weight="bold"),
        password_input,
    ]

    # ─────────────────────────────────────────────
    # 🟩 체크: build_screen(...) 제거
    # 이유:
    # - 상단/하단은 main.py 에서 고정 관리
    # - 이 파일은 본문만 반환
    # ─────────────────────────────────────────────
    return dogdog.build_screen_body(body_controls)