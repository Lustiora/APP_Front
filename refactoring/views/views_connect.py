# -------------------------------------------------------------------------------------------------------
import flet as ft
import refactoring.views as views
import refactoring.component as dogdog
import re, hashlib
from datetime import date
from dateutil.relativedelta import relativedelta
# -------------------------------------------------------------------------------------------------------
class Api_push_Data:
    data = {}
# -------------------------------------------------------------------------------------------------------
def on_boarding_tile(page, content_page:str="signup", change_page_callback=None):
    # ---------------------------------------------------------------------------------------------------
    # Default Value
    # ---------------------------------------------------------------------------------------------------
    storage = page.session.store.get
    def show_error(text:str):
        page.show_dialog(ft.SnackBar(content=ft.Text(value=text), open=True))
    top = ft.Row(controls=[dogdog.about_dog()])
    focus_field = ft.TextField(
            border_color=ft.Colors.TRANSPARENT, height=0, opacity=0,
            focus_color=ft.Colors.TRANSPARENT, read_only=True
    )
    regex_email = re.compile(
        pattern=r"^[a-zA-Z0-9][a-zA-Z0-9._]+[@][a-zA-Z][A-Za-z.]+[.]\w{2,}"
    )
    # ---------------------------------------------------------------------------------------------------
    # On Boarding Tile Link
    # ---------------------------------------------------------------------------------------------------
    if content_page == "sign_up":
        def sign_up_next(e):
            if storage("user_email") and storage("user_name") and storage("user_password"):
                if not re.fullmatch(pattern=regex_email, storage("user_email")): # type: ignore
                    show_error(text="유효한 이메일 형식이 아닙니다.")
                    return
                hash_pw = hashlib.sha256(data=storage("user_password").encode()).hexdigest() # type: ignore
                Api_push_Data.data.update({
                    "user_email": storage("user_email"), 
                    "user_name": storage("user_name"), 
                    "user_password": hash_pw
                })
                change_page_callback("pet_info") # type: ignore
            else:
                show_error(text="이메일, 닉네임, 비밀번호를 모두 입력해주세요.")
                return
        top = ft.Row(controls=[dogdog.about_dog(case=1)])
        content = views.sign_up_view(page=page)
        bottom = ft.Row(controls=[
            dogdog.continue_button(on_click=sign_up_next) 
        ])
    # ---------------------------------------------------------------------------------------------------
    elif content_page == "pet_info":
        def pet_info_next(e):
            if (storage("breed_text") and
                storage("pet_name") and
                storage("pet_weight")):
                if storage("pet_birth_day"):
                    birth = str(storage("pet_birth_day")) # type: ignore
                elif storage("pet_age_year") and storage("pet_age_month"):
                    age_month = int(storage("pet_age_month").split()[0]) # type: ignore
                    age_year = int(storage("pet_age_year").split()[0]) # type: ignore
                    birth = str(date.today() - relativedelta(months=age_month, years=age_year))
                else: return
                if int(storage("pet_weight")) >= 120: # type: ignore
                    show_error("정상적인 무게를 입력해주세요.")
                try:
                    pet_weight_str = str(storage("pet_weight"))
                    weight_val = float(pet_weight_str)
                    if weight_val <= 0 or weight_val >= 120:
                        show_error(text="정상적인 무게를 입력해주세요.")
                        return
                    if "." in pet_weight_str and len(pet_weight_str.split(".")[1]) > 2:
                        show_error(text="무게는 소수점 두 자리까지만 입력 가능합니다.")
                        return
                except ValueError:
                    show_error(text="올바른 숫자 형식으로 무게를 입력해주세요.")
                    return
                gender = storage("pet_gender")
                if gender == "수컷":
                    sex = 1
                    is_neutered = False
                elif gender == "암컷":
                    sex = 2
                    is_neutered = False
                elif gender == "수컷 (중성화)":
                    sex = 1
                    is_neutered = True
                elif gender == "암컷 (중성화)":
                    sex = 2
                    is_neutered = True
                else: return
                Api_push_Data.data.update({
                    "nickname": storage("pet_name"), "image_path": storage("image_path"),
                    "breed_id": storage("breed_id"), "birth": birth,
                    "sex": sex, "is_neutered": is_neutered, "weight": storage("pet_weight")
                })
                change_page_callback("pet_obesity") # type: ignore
            else:
                show_error(text="이름, 품종, 생년월일, 성별, 무게를 모두 입력해주세요.")
                return
        content = views.pet_info_view(page=page)
        bottom = ft.Row(controls=[
            dogdog.arrow_back(on_click=lambda e: change_page_callback("sign_up")), # type: ignore
            dogdog.continue_button(on_click=pet_info_next),
        ])
    # ---------------------------------------------------------------------------------------------------
    elif content_page == "pet_obesity":
        def pet_obesity_next(e):
            if storage("body_score"):
                Api_push_Data.data.update({"bcs": storage("body_score")})
                change_page_callback("pet_activity") # type: ignore
            else:
                show_error(text="체형을 선택해주세요.")
                return
        content = views.pet_obesity_view(page=page)
        bottom = ft.Row(controls=[
            dogdog.arrow_back(on_click=lambda e: change_page_callback("pet_info")), # type: ignore
            dogdog.continue_button(on_click=pet_obesity_next),
        ])
    # ---------------------------------------------------------------------------------------------------
    elif content_page == "pet_activity":
        def pet_activity_next(e):
            meals = [storage("breakfast"), storage("lunch"), storage("dinner")]
            has_meals = any(meals)
            if storage("radio_time") and has_meals:
                feeding_count = sum(1 for meal in meals if meal)
                Api_push_Data.data.update({
                    "feeding_count": feeding_count, "daily_walks": int(storage("radio_time"))
                })
                change_page_callback("pet_health") # type: ignore
            else:
                show_error(text="급여 시간(최소 1개)과 산책 시간을 선택해주세요.")
                return
        content = views.pet_activity_view(page=page)
        bottom = ft.Row(controls=[
            dogdog.arrow_back(on_click=lambda e: change_page_callback("pet_obesity")), # type: ignore
            dogdog.continue_button(on_click=pet_activity_next),
        ])
    # ---------------------------------------------------------------------------------------------------
    elif content_page == "pet_health":
        def pet_health_next(e):
            if storage("allergy"): Api_push_Data.data.update({"allergy": storage("allergy")})
            if storage("disease"): Api_push_Data.data.update({"disease": storage("disease")})
            change_page_callback("pet_food") # type: ignore
        content = views.pet_health_view(page=page)
        bottom = ft.Row(controls=[
            dogdog.arrow_back(on_click=lambda e: change_page_callback("pet_activity")), # type: ignore
            dogdog.continue_button(on_click=pet_health_next),
        ])
    # ---------------------------------------------------------------------------------------------------
    elif content_page == "pet_food":
        def pet_food_next(e):
            if storage("product_id") and storage("food_weight"):
                if storage("food_weight") > storage("product_weight"): # type: ignore
                    show_error(text="정상적인 잔여량을 입력해주세요.")
                    return
                Api_push_Data.data.update({
                    "product_id": int(storage("product_id")), 
                    "food_weight": storage("food_weight")})
                # print("Final API Push Data:", Api_push_Data.data)
                page.session.store.set("api_push", Api_push_Data.data)
                change_page_callback("sign_up_success") # type: ignore
            else:
                show_error(text="현재 급여 중인 사료와 용량, 잔여량을 선택/입력해주세요.")
                return
        content = views.pet_food_view(page=page)
        bottom = ft.Row(controls=[
            dogdog.arrow_back(on_click=lambda e: change_page_callback("pet_health")), # type: ignore
            dogdog.continue_button(on_click=pet_food_next), # type: ignore
        ])
    # ---------------------------------------------------------------------------------------------------
    elif content_page == "sign_up_success":
        basic_content = ft.Row(
            expand=True,
            controls=[
                ft.Column(
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=views.signup_success_view(page=page)
        )])
        focus_field = None
        return basic_content, focus_field
    # ---------------------------------------------------------------------------------------------------
    # On Boarding Content and Dummy Focus Field Change
    # ---------------------------------------------------------------------------------------------------
    basic_content = [
        top,
        ft.Container(
            expand=True,
            padding=ft.Padding.only(top=20),
            content=ft.Column(
                scroll=ft.ScrollMode.HIDDEN,
                expand=True,
                spacing=10,
                controls=content if isinstance(content, list) else [content] # type: ignore
            )
        ),
        focus_field,
        bottom
    ]
    return basic_content, focus_field