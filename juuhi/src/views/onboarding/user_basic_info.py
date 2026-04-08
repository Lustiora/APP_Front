import flet as ft

# 상단 바
def top_bar_back():
    return ft.Column(
        controls=[
            ft.Container(
                # padding=ft.padding.only(top=55),
                # height=100,
                # width=float("inf"),
                content=ft.Row(
                    [
                        ft.Container(
                            alignment=ft.Alignment(1, 0),
                            content=ft.IconButton(icon=ft.Icons.ARROW_BACK, 
                                                icon_color=ft.Colors.GREY_700, 
                                                icon_size=30, 
                                                # on_click=lambda e: e.page.pop_dialog()
                                                ),
                        ),
                        ft.Text(  # 빈칸
                            size=20,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            ),
        ],
    )

# 하단 컨티뉴 버튼
def bottom_button():
    return ft.Container(
    bgcolor=ft.Colors.YELLOW_600,
    content=ft.Text("Continue", color=ft.Colors.WHITE),
)

def user_basic_info_view(page: ft.Page, on_continue=None):
    # body
    title = ft.Column(
        controls=[
            ft.Text("Welcome to 똑똑", size=20, weight=ft.FontWeight.BOLD),
            ft.Text("똑똑🚪✊ 우리집 강아지가 마지막 한알을 먹기 전"),
            ft.Text("문앞에 사료가 도착합니다🔔")
        ]
    )

    def input_box(title):
        return ft.Column(
                controls=[ 
                    ft.Text(title),
                    ft.TextField(
                                hint_text=title,  # 앞페이지에서 받아온 email
                                # read_only=True,
                                border_radius=9,
                                expand=True,
                                border_color=ft.Colors.GREY_400,
                            ),
                ]
            )
    
    get_detail = ft.Column(
        controls=[
            ft.Text("프로필을 완성하세요.", size=20, weight=ft.FontWeight.BOLD),
            ft.Column(
                controls=[ 
                    ft.Text("이메일"),
                    ft.TextField(
                                hint_text="이메일",  # 앞페이지에서 받아온 email
                                # read_only=True,
                                border_radius=9,
                                expand=True,
                                border_color=ft.Colors.GREY_400,
                            ),
                ]
            ),
            ft.Column(
                    controls=[
                    ft.Text("닉네임"),
                    ft.TextField(
                                hint_text="닉네임",
                                border_radius=9,
                                expand=True,
                                border_color=ft.Colors.GREY_400,
                            ),
                ]
            ),
            ft.Column(
                    controls=[
                    ft.Text("비밀번호"),
                    ft.TextField(
                                hint_text="비밀번호",
                                border_radius=9,
                                expand=True,
                                border_color=ft.Colors.GREY_400,
                            ),
                ]
            ),
        ]   
    )

    # return ft.Column(
    #     expand=True,
    #     spacing=0,
    #     controls=[
    #         top_bar_back,  # 상단바
    #         # 바디
    #         title,
    #         get_detail,  
    #         bottom_button,  # 하단바
    #     ],
    # )

    return ft.Column(
        expand=True,
        spacing=40,
        controls=[
            top_bar_back(),  # 상단바
            # 바디
            title,
            get_detail,  
        ],
    )
    

    # render_page(0)


# if __name__ == "__main__":
#     import webbrowser
#     import os

#     if os.getenv("FLET_NO_BROWSER"):
#         webbrowser.open = lambda *args, **kwargs: None

#     ft.run(
#         user_basic_info_view,
#         assets_dir="assets",
#         view=ft.AppView.WEB_BROWSER,
#         port=34636,
#     )
    