# -------------------------------------------------------------------------------------------------------
import flet as ft
import components as dogdog
import domains.onboarding.views.pet_food_view as pet_food_view
# -------------------------------------------------------------------------------------------------------
def feeding_add_edit(page: ft.Page, view):
    # ---------------------------------------------------------------------------------------------------
    # Default Value
    # ---------------------------------------------------------------------------------------------------
    storage = page.session.store
    if storage.get("food_text"): storage.remove("food_text")
    if storage.get("product_id"): storage.remove("product_id")
    if storage.get("food_id"): storage.remove("food_id")
    feeding_data:dict = (
        storage.get("select_feeding_data") if storage.get("select_feeding_data") else {}
    ) # type: ignore
    # ---------------------------------------------------------------------------------------------------
    # Test Dialog
    # ---------------------------------------------------------------------------------------------------
    def show_error(text:str): page.show_dialog(ft.SnackBar(content=ft.Text(value=text), open=True))
    # ---------------------------------------------------------------------------------------------------
    # Input Field Change Event
    # ---------------------------------------------------------------------------------------------------    
    def on_food_weight_change(e):
        try: storage.set("food_weight", int(e.control.value))
        except ValueError: pass
    # ---------------------------------------------------------------------------------------------------
    # View Page
    # ---------------------------------------------------------------------------------------------------    
    if view =="edit":
        if not (storage.get("select_customer_food_id" or storage.get("select_feeding_data"))):
            page.go("/feeding")
            show_error("정상적이지 않은 접근입니다.")
            return ft.Container(padding=ft.Padding.only(left=20, right=20, top=20), bgcolor="#ffffff")
        customer_food_id = storage.get("select_customer_food_id")
        storage.set(key="food_text", value=f"{feeding_data["brand"]} {feeding_data["product_name"]}")
        storage.set(key="product_id", value=feeding_data["product_id"])
        storage.set(key="food_id", value=feeding_data["product_detail_id"])
        feeding_start_date = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=5,
            controls=[
                ft.Icon(icon=ft.Icons.CALENDAR_MONTH, color=ft.Colors.GREY_600, size=16),
                dogdog.basic_text(value=f"급여 시작일 : {feeding_data['feeding_start']}", color=ft.Colors.GREY_600),
            ]
        )
    # ---------------------------------------------------------------------------------------------------
    pet_food_controller = pet_food_view.PetfoodController(page=page)
    food_select_field = pet_food_controller.food_picker_field.content.controls[0] # type: ignore
    product_weight_field = pet_food_controller.product_weight_list
    # ---------------------------------------------------------------------------------------------------
    # View Page
    # ---------------------------------------------------------------------------------------------------    
    if view =="edit":
        column_text = "현재 급여 중인 사료"
        feeding_setting_content = [
            dogdog.flat_button("수정", scale=1, bgcolor="#FEF3B9"), # type: ignore
            dogdog.flat_button("삭제", scale=1, bgcolor="#FEF3B9"), # type: ignore
            dogdog.flat_button("저장", scale=1)
        ]
        food_select_field.color = ft.Colors.BLACK
        product_weight_field.label = f"{feeding_data["total_weight"]}g"
    # ---------------------------------------------------------------------------------------------------
    elif view == "add":
        column_text = "신규 등록 사료"
        feeding_setting_content = [dogdog.flat_button("저장", scale=1)]
        food_select_field.value = "사료를 선택해주세요."
    selected_food_weight = dogdog.input_textfield(
        hint_text="사료의 잔여량을 적어주세요", input_type="int", suffix="g",
        on_change=on_food_weight_change)
    feeding_setting = ft.Row(
        margin=ft.margin.only(top=10),
        alignment=ft.MainAxisAlignment.CENTER,
        controls=feeding_setting_content) # type: ignore
    # ---------------------------------------------------------------------------------------------------
    # Feeding Edit Page
    # ---------------------------------------------------------------------------------------------------
    content_column = [
        dogdog.basic_text(value=column_text, weight="bold"),
        pet_food_controller.food_picker_field,
        pet_food_controller.product_weight_list,
        ft.Container(height=10),
        dogdog.basic_text(value="사료 잔여량", weight="bold"),
        selected_food_weight,
    ]
    if view =="edit": content_column.append(feeding_start_date)
    content_column.append(feeding_setting)
    return ft.Container(
        padding=ft.Padding.only(left=20, right=20, top=20),
        bgcolor="#ffffff",
        content=ft.Column(
            controls=content_column # type: ignore
        )
    )