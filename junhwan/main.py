import asyncio
import flet as ft
import views
import re, hashlib
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from components import about_dog, arrow_back, bottom_continue_button

# ─────────────────────────────────────────────
# 🟦 화면 이동 순서표
# ─────────────────────────────────────────────
ROUTES = [
    "/signup",
    "/pet_info",
    "/pet_info_obesity",
    "/pet_info_activity",
    "/pet_info_health",
    "/pet_info_food",
    "/signup_success",
]


# ─────────────────────────────────────────────
# 🟦 route별 실제 화면 생성 함수 연결표
# ─────────────────────────────────────────────
ROUTE_BUILDERS = {
    "/signup": views.signup_view,
    "/pet_info": views.pet_basic_info_view,
    "/pet_info_obesity": views.pet_info_obesity_view,
    "/pet_info_activity": views.pet_info_activity_view,
    "/pet_info_health": views.pet_info_health_view,
    "/pet_info_food": views.pet_info_food_view,
    "/signup_success": views.signup_success_view,
}


# ─────────────────────────────────────────────
# 🟨 슬라이드 애니메이션 설정
# ─────────────────────────────────────────────
ANIMATION_MS = 340
ANIMATION_CURVE = ft.AnimationCurve.EASE_IN_OUT

# ✅ 모바일에서 첫 프레임이 씹히지 않도록 여유 시간
PRE_ANIMATION_DELAY = 0.08
POST_ANIMATION_BUFFER = 0.08


def main(page: ft.Page):
    page.title = "Dog Dog"
    page.bgcolor = ft.Colors.WHITE
    page.padding = 0
    page.spacing = 0
    page.scroll = ft.ScrollMode.HIDDEN
    page.theme_mode = ft.ThemeMode.LIGHT

    # ─────────────────────────────────────────────
    # 🟪 FilePicker 초기화
    # ─────────────────────────────────────────────
    page.profile_image_picker = ft.FilePicker()
    page.overlay.append(page.profile_image_picker)

    # ─────────────────────────────────────────────
    # 🟦 현재 보고 있는 페이지 번호 저장
    # ─────────────────────────────────────────────
    current_index = 0

    # ─────────────────────────────────────────────
    # 🟦 route 동기화 중복 방지 플래그
    # ─────────────────────────────────────────────
    route_sync_in_progress = False

    # ─────────────────────────────────────────────
    # ✅ 이동 중복/연타 방지 플래그
    # ─────────────────────────────────────────────
    is_navigating = False

    # ─────────────────────────────────────────────
    # 🟩 route 문자열 → index 번호 변환
    # ─────────────────────────────────────────────
    def route_to_index(route_name: str) -> int:
        try:
            return ROUTES.index(route_name)
        except ValueError:
            return 0

    # ─────────────────────────────────────────────
    # 🟩 각 화면을 공통 껍데기 안에 넣는 함수
    # ─────────────────────────────────────────────
    def build_page_shell(route_name: str):
        builder = ROUTE_BUILDERS[route_name]

        # 회원가입 완료 페이지는 예외 처리
        if route_name == "/signup_success":
            return builder(page)

        return ft.Container(
            expand=True,
            content=ft.Container(
                expand=True,
                padding=ft.Padding.only(left=16, right=16),
                content=builder(page),
            ),
        )

    # ─────────────────────────────────────────────
    # 🟦 상단 고정 영역
    # ─────────────────────────────────────────────
    top_appbar = ft.Container(
        width=float("inf"),
        padding=ft.Padding.only(left=16, right=16, top=12, bottom=12),
    )

    # ─────────────────────────────────────────────
    # 🟦 하단 고정 영역
    # ─────────────────────────────────────────────
    fixed_button = ft.Container(
        width=float("inf"),
        padding=ft.Padding.only(left=16, right=16, top=10, bottom=20),
    )

    # ─────────────────────────────────────────────
    # 🟦 본문 스택
    # ─────────────────────────────────────────────
    body_stack = ft.Stack(
        expand=True,
        fit=ft.StackFit.EXPAND,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        controls=[],
    )

    # ─────────────────────────────────────────────
    # 🟦 현재/들어오는 레이어 변수
    # ─────────────────────────────────────────────
    current_layer = ft.Container(
        expand=True,
        animate_offset=ft.Animation(ANIMATION_MS, ANIMATION_CURVE),
        content=None,
    )

    incoming_layer = None

    # ─────────────────────────────────────────────
    # 🟨 현재 화면과 브라우저 URL 동기화
    # ─────────────────────────────────────────────
    async def sync_route_to_current_index():
        nonlocal route_sync_in_progress
        route_sync_in_progress = True
        try:
            await page.push_route(ROUTES[current_index])
        finally:
            route_sync_in_progress = False

    # ─────────────────────────────────────────────
    # 🟩 현재 페이지에 맞게 상단/하단 고정 UI 바꾸기
    # ─────────────────────────────────────────────
    def apply_shell_by_index(index: int):
        # print(f"ROUTES: {ROUTES[index]}")

        if ROUTES[index] == "/signup_success":
            top_appbar.content = None
            fixed_button.content = None
            return

        if ROUTES[index] == "/signup":
            top_appbar.content = about_dog(1)
            fixed_button.content = ft.Row(
                controls=[
                    bottom_continue_button(on_click=on_continue_click),
                ]
            )
        else:
            top_appbar.content = about_dog()
            top_appbar.padding = ft.Padding.only(left=16, right=16, top=12, bottom=12)
            fixed_button.padding = ft.Padding.only(left=16, right=16, top=10, bottom=20)
            fixed_button.content = ft.Row(
                controls=[
                    arrow_back(on_click=on_back_click),
                    bottom_continue_button(on_click=on_continue_click),
                ]
            )

    # ─────────────────────────────────────────────
    # 🟩 현재 화면 즉시 표시
    # ─────────────────────────────────────────────
    def show_index_immediately(index: int):
        nonlocal current_layer, incoming_layer

        if ROUTES[index] == "/signup_success":
            current_layer = ft.Container(
                expand=True,
                content=build_page_shell(ROUTES[index]),
            )
        else:
            current_layer = ft.Container(
                expand=True,
                animate_offset=ft.Animation(ANIMATION_MS, ANIMATION_CURVE),
                content=build_page_shell(ROUTES[index]),
            )

            incoming_layer = None
            body_stack.controls.clear()
            body_stack.controls.append(current_layer)

            apply_shell_by_index(index)

    # ─────────────────────────────────────────────
    # 🟥 핵심 1: 버튼 전용 슬라이드 애니메이션 이동
    # ─────────────────────────────────────────────
    async def go_to_index(index: int, direction: int):
        nonlocal current_index, is_navigating, current_layer, incoming_layer

        if is_navigating:
            return

        index = max(0, min(index, len(ROUTES) - 1))
        if index == current_index:
            return

        is_navigating = True

        try:
            next_route = ROUTES[index]

            # ✅ 다음 화면은 딱 한 번만 생성
            next_layer = ft.Container(
                expand=True,
                bgcolor=ft.Colors.WHITE,
                offset=ft.Offset(direction, 0),
                animate_offset=ft.Animation(ANIMATION_MS, ANIMATION_CURVE),
                content=build_page_shell(next_route),
            )

            incoming_layer = next_layer

            # ✅ 현재 화면 + 다음 화면을 스택에 올림
            body_stack.controls.clear()
            body_stack.controls.append(current_layer)
            body_stack.controls.append(next_layer)

            # ✅ 버튼/상단 UI는 도착 페이지 기준으로 먼저 바꿈
            current_index = index
            apply_shell_by_index(current_index)
            page.update()


            # ✅ 모바일에서 첫 프레임을 확실히 그릴 시간 확보
            await asyncio.sleep(PRE_ANIMATION_DELAY)

            # ✅ 새 화면만 슬라이드 인
            next_layer.offset = ft.Offset(0, 0)
            page.update()

            # ✅ 애니메이션 완료까지 충분히 대기
            await asyncio.sleep((ANIMATION_MS / 1000) + POST_ANIMATION_BUFFER)

            # ✅ 새 레이어를 현재 레이어로 확정
            current_layer = next_layer
            incoming_layer = None
            current_layer.offset = ft.Offset(0, 0)

            body_stack.controls.clear()
            body_stack.controls.append(current_layer)

            page.update()
            await sync_route_to_current_index()

        finally:
            is_navigating = False

    # ─────────────────────────────────────────────
    # 🟥 핵심 2: Continue 버튼 클릭 시 다음 화면
    # ─────────────────────────────────────────────
    api_push = {
        "email": None,
        "name": None,
        "password": None,
        "nickname": None,
        "image_path": None,
        "breed_id": None,
        "birth": None,
        "sex": None,
        "weight": None,
        "bcs": None,
        "feeding_count": None,
        "daily_walks": None,
        "allergies": None,
        "medical_history": None,
        "food_id": None,
        "food_weight": None
    }

    async def on_continue_click(e):
        ####################################################################################################
        ### Null Check and API Push
        ####################################################################################################
        storage = page.session.store.get

        if ROUTES[current_index] == "/signup":
            if not (storage("email")
                and storage("name")
                and storage("password")
            ):
                print(f"Null Check {ROUTES[current_index]}")
                return
            else:
                regex_email = re.compile(r'^[a-zA-Z0-9][a-zA-Z0-9._]+[@][a-zA-Z][A-Za-z.]+[.]\w{2,}')
                if not re.fullmatch(regex_email, storage("email")):
                    print("email 필터링됨")
                    return
                hash_pw = hashlib.sha256(storage("password").encode()).hexdigest()
                print(f"Check {ROUTES[current_index]}")
                api_push.update({"email": storage("email"), "name": storage("name"), "password": hash_pw})
        elif ROUTES[current_index] == "/pet_info":
            birth = None
            if storage("selected_birth"):
                birth = str(storage("selected_birth"))
            elif storage("pet_age_year") and storage("pet_age_month"):
                age_month = int(storage("pet_age_month").split()[0])
                age_year = int(storage("pet_age_year").split()[0])
                birth = str(date.today() - relativedelta(months=age_month, years=age_year))
            if not (storage("pet_name")
                and storage("breed_id")
                and birth
                and storage("pet_gender")
                and storage("pet_weight")
            ):
                print(f"Null Check {ROUTES[current_index]}")
                return
            else:
                print(f"Check {ROUTES[current_index]}")
                api_push.update({"nickname": storage("pet_name"), "image_path": storage("image_path"),
                                 "breed_id": storage("breed_id"), "birth": birth,
                                 "sex": storage("pet_gender"), "weight": storage("pet_weight")})
        elif ROUTES[current_index] == "/pet_info_obesity":
            if not storage("body_score"):
                print(f"Null Check {ROUTES[current_index]}")
                return
            else:
                print(f"Check {ROUTES[current_index]}")
                api_push.update({"bcs": storage('body_score')})
        elif ROUTES[current_index] == "/pet_info_activity":
            # Ensure activity time is selected and at least one meal is checked
            meals = [storage("breakfast"), storage("lunch"), storage("dinner")]
            has_meals = any(meals)
            if not (storage("radio_time") and has_meals):
                print(f"Null Check {ROUTES[current_index]}")
                return
            else:
                feeding_count = sum(1 for meal in meals if meal)
                print(f"Check {ROUTES[current_index]}")
                daily_walks = str(timedelta(minutes=int(storage("radio_time"))))
                api_push.update({"feeding_count": feeding_count, "daily_walks": daily_walks})
        elif ROUTES[current_index] == "/pet_info_health":
            # Store health/allergy info if available in session
            print(f"Check {ROUTES[current_index]}")
            api_push.update({
                "allergies": storage("allergies") if storage("allergies") else [],
                "medical_history": storage("medical_history") if storage("medical_history") else []
            })
        elif ROUTES[current_index] == "/pet_info_food":
            if not (storage("food_id")
                    and storage("food_weight")):
                print(f"Null Check {ROUTES[current_index]}")
                return
            else:
                print(f"Check {ROUTES[current_index]}")
                api_push.update({"food_id": storage('food_id'), "food_weight": storage('food_weight')})
                
                # result = await register_user_and_pet(api_push)
                print("Final API Push Data:", api_push)
                
                # Navigate to success page
                await go_to_index(ROUTES.index("/signup_success"), direction=1)
                return

        if current_index >= len(ROUTES) - 1 or is_navigating:
            return
        await go_to_index(current_index + 1, direction=1)
        # print(f"session keys: {page.session.store.get_keys()}")
        # print(f"Change ROUTES: {ROUTES[current_index]}")

    # ─────────────────────────────────────────────
    # 🟥 핵심 3: 뒤로가기 클릭 시 이전 화면
    # ─────────────────────────────────────────────
    async def on_back_click(e):
        if current_index <= 0 or is_navigating:
            return
        await go_to_index(current_index - 1, direction=-1)
        # print(f"session keys: {page.session.store.get_keys()}")

    # ─────────────────────────────────────────────
    # 🟨 브라우저 route가 바뀌었을 때 화면도 맞춰주기
    # ─────────────────────────────────────────────
    def route_change(e: ft.RouteChangeEvent):
        nonlocal current_index

        if route_sync_in_progress:
            return

        target_index = route_to_index(page.route)
        if target_index != current_index:
            current_index = target_index
            show_index_immediately(current_index)

    # ─────────────────────────────────────────────
    # 🟦 전체 앱 껍데기 View
    # ─────────────────────────────────────────────
    page.views.append(ft.View(
        route="/app_shell",
        padding=0,
        spacing=0,
        bgcolor=ft.Colors.WHITE,
        controls=[ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                spacing=0,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(height=20),
                    top_appbar,
                    ft.Container(expand=True, content=body_stack),
                    fixed_button,
            ])
        )]
    ))

    page.on_route_change = route_change

    # ─────────────────────────────────────────────
    # ✅ 시작 route 보정
    # ─────────────────────────────────────────────
    initial_route = page.route or "/signup"

    if initial_route == "/signup_success":
        initial_route = "/signup"

    current_index = route_to_index(initial_route)
    show_index_immediately(current_index)

    page.run_task(page.push_route, ROUTES[current_index])


# build test
# flet build apk ./junhwan --verbose --arch arm64-v8a
# app name = project name

# if __name__ == "__main__":
#     ft.app(target=main, assets_dir="assets")


import logging, warnings
level=logging.INFO
logging.basicConfig(level=level)
warnings.filterwarnings("ignore")
if __name__ == "__main__":
    import webbrowser, os
    if os.getenv("FLET_NO_BROWSER"):
        webbrowser.open = lambda *args, **kwargs: None
    ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, port=34636) # test