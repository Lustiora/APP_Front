import sys

import flet


# pip install watchfiles "flet==0.81.0"
# flet build apk --split-per-abi
# test address http://ip:port

# flet icon search page https://examples.flet.dev/icons_browser/

class Default:
    if sys.platform == "ios":
        view_width = 375
    elif sys.platform == "android" or "linux":
        view_width = 360
    elif sys.platform == "win32": # Hot Reload Test
        view_width = 360
    else:
        view_width = 380

    image_size = view_width / 1.8 # Width, Height

    data_width = view_width / 2.1
    data_height = data_width / 2

    history_width = view_width
    history_height = view_width / 10

    side_width = view_width / 3
    side_height = view_width / 10

    tail_btn_size = view_width / 3.3 # Width, Height

    text_size = 20
    text_weight = "bold"

    container_border = flet.Border.all(color=flet.Colors.BLACK)

def image_container(event, src:str, size=Default.image_size):
    return flet.Container(
        width=size,
        height=size,
        bgcolor=flet.Colors.BLACK,
        shape=flet.BoxShape.CIRCLE, # 원형 1
        on_click=event,
        image=flet.DecorationImage( # 컨테이너에 이미지를 추가하기위한 옵션
            src=src,
            fit=flet.BoxFit.COVER # 원형 2
        ),
    )

def side_container(text, event, width=Default.side_width, height=Default.side_height):
    return flet.Container(
        content=flet.Text(text, size=Default.text_size, weight=Default.text_weight),
        alignment=flet.Alignment.CENTER,
        on_click=event,
        width=width,
        height=height,
        border_radius=10,
        border = Default.container_border,
    )

def data_container(text, event, width=Default.data_width, height=Default.data_height):
    return flet.Container(
        width=width,
        height=height,
        padding=15,
        content=flet.Column(
            horizontal_alignment=flet.MainAxisAlignment.CENTER,
            controls=[
            flet.Text(text, size=Default.text_size, weight=Default.text_weight),
            flet.Container(width=width/1.5, height=height/10, border_radius=10, border=Default.container_border)
        ]),
        alignment=flet.Alignment.CENTER,
        border_radius=10,
        on_click=event,
        border=Default.container_border,
    )

def history_container(text, event, width=Default.history_width, height=Default.history_height):
    return flet.Container(
        content=flet.Text(text, size=Default.text_size, weight=Default.text_weight),
        alignment=flet.Alignment.CENTER,
        on_click=event,
        width=width,
        height=height,
        border_radius=10,
        border = Default.container_border,
    )

def tail_btn_container(text, event, size=Default.tail_btn_size):
    return flet.Container(
        content=flet.Text(text, size=Default.text_size, weight=Default.text_weight),
        width=size,
        height=size,
        alignment=flet.Alignment.CENTER,
        on_click=event,
        border_radius=10,
        border = Default.container_border,
    )


def main(page: flet.Page):
    print(page.width)
    Default.view_width = page.width if page.width > 0 else 360
    if Default.view_width > 360:
        Default.view_width = 360
    print(Default.view_width)

    page.theme_mode = flet.ThemeMode.SYSTEM
    page.horizontal_alignment = flet.CrossAxisAlignment.CENTER

    def click_print(e, index=None):
        if not index:
            index = f"Nav Bar Page: {e.control.selected_index}"
        print(index)
        if page.appbar.page:
            page.appbar.title.content = index

    page.appbar = flet.AppBar(
        leading=flet.IconButton(flet.Icons.MENU, on_click=lambda e: click_print(e,"Menu")), # 좌측 메뉴
        title=flet.TextButton("DogDog!", on_click=lambda e: click_print(e,"LOGO")),
        center_title=True,
        actions=[flet.IconButton(flet.Icons.SETTINGS, on_click=lambda e: click_print(e,"Settings"))] # 우측 메뉴
    )

    test = flet.Column(
        scroll=flet.ScrollMode.AUTO,
        horizontal_alignment=flet.MainAxisAlignment.CENTER,
        expand=True,
        controls=[
            flet.Container(height=5),
            flet.Row(
                controls=[
                    image_container(
                        event=lambda e: click_print(e,"Images"),
                        src="https://content.lyka.com.au/f/1016262/1104x676/e36872ce32/beagle.png"
                    ),
                    flet.Column(
                        horizontal_alignment=flet.MainAxisAlignment.CENTER,
                        expand=True,
                        controls=[
                            side_container("뽀찌", event=lambda e: click_print(e, "이름")),
                            side_container("살쪘어요..", event=lambda e: click_print(e, "상태값")),
                            side_container("3짤", event=lambda e: click_print(e, "나이")),
                        ]
                    )
                ]
            ),
            flet.Container(height=10),
            flet.Row(
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    data_container(text="섭취량", event=lambda e: click_print(e,"섭취량")),
                    data_container(text="음수량", event=lambda e: click_print(e,"음수량")),
                ]
            ),
            flet.Row(
                alignment=flet.MainAxisAlignment.CENTER,
                controls=[
                    history_container(text=f"OS: {sys.platform}",  event=lambda e: click_print(e,"기록요약")),
                ]
            ),
            flet.Container(height=10),
            flet.Row(
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    tail_btn_container(text="밥주기", event=lambda e: click_print(e,"밥주기")),
                    tail_btn_container(text="물주기", event=lambda e: click_print(e,"물주기")),
                    tail_btn_container(text="약먹이기", event=lambda e: click_print(e,"약먹이기")),
                ]
            ),
            flet.Row(
                alignment=flet.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    tail_btn_container(text="대소변기록", event=lambda e: click_print(e,"대소변기록")),
                    tail_btn_container(text="체중기록", event=lambda e: click_print(e,"체중기록")),
                    tail_btn_container(text="관찰기록", event=lambda e: click_print(e,"관찰기록")),
                ]
            ),
        ]
    )

    content = flet.Row(
        width=Default.view_width,
        expand=True,
        controls=[
            flet.Container(
                # bgcolor=flet.Colors.BROWN,
                expand=True,
                content=test
            ),
        ]
    )

    page.floating_action_button = flet.FloatingActionButton(
        icon=flet.Icons.ADD,
        on_click=lambda _: print("Nyang!"),
    )

    page.navigation_bar=flet.NavigationBar(
        on_change=lambda e: click_print(e),
        destinations=[
            flet.NavigationBarDestination(label="Home", icon=flet.Icons.HOME),
            flet.NavigationBarDestination(label="log", icon=flet.Icons.HISTORY),
            flet.NavigationBarDestination(label="SHOP", icon=flet.Icons.SHOP),
            flet.NavigationBarDestination(label="AI", icon=flet.Icons.STARS_SHARP),
            flet.NavigationBarDestination(label="My Page", icon=flet.Icons.EMOJI_EMOTIONS),
        ]
    )

    page.add(content)

# build test
# app name = project name
# if __name__ == "__main__":
#     flet.app(target=main, assets_dir="assets")

if __name__ == "__main__":
    import webbrowser, os
    if os.getenv("FLET_NO_BROWSER"):
        webbrowser.open = lambda *args, **kwargs: None
    flet.run(main, assets_dir="assets", view=flet.AppView.WEB_BROWSER, port=34636) # test