import flet as ft
import requests, urllib.parse
# 클라이언트 키 및 URL 세팅 (기존과 동일) - 추후 env로 하여 보안
naver_client_id ="cL6lf7casYStHBPNomya"
naver_client_secret = "GFftc3MH_7"
naver_direct_url = "http://192.168.0.27:34636/callback/naver".strip()

google_client_id = "896005513797-hvf0hpou20iv5pisattm5u83pfl6bcck.apps.googleusercontent.com"
google_client_secret="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".strip()
## 개발환경에 따른 테스트(구글로그인 테스트를 원하면 true)
use_google_login = True ## True 시 로컬로 연결
if use_google_login:
    google_direct_url="http://localhost:34636/callback/google".strip() # 현재 연결 可
else:
    google_direct_url="http://192.168.0.27:34636/callback/google".strip() # 현재 연결 不可()

kakao_client_id = "37410fe118d9f6cd66429295aad8e850"
kakao_client_secret = "on4CAlsnU57O2YaKXVKFAta03L89OJ0z".strip()
kakao_client_url = "http://192.168.0.27:34636/callback/kakao".strip()


# 각 소셜 서버에 넣을 데이터 likes 방문 키===============================================================================
google_params = {"client_id": google_client_id, 
                "redirect_uri": google_direct_url, # 로그인 완료 후 돌려보낼 주소
                "response_type": "code", # 인증 완료 후 요청사항(code)
                "scope": "openid email profile" # 열람권한 요청(구글은 scope, 네이버는 state) 현재는 이메일, 프로필 요청
                }
google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(google_params)}" # 파이썬의 값을 인터넷이 이해할 수 있게 주소를 인터넷 문법으로 번역

kakao_params = {"client_id": kakao_client_id, "redirect_uri": kakao_client_url, "response_type": "code", "prompt": "consent"}
kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?{urllib.parse.urlencode(kakao_params)}"

naver_state = "flet_login_test_state_1234"
naver_params = {"response_type": "code", "client_id": naver_client_id, "redirect_uri": naver_direct_url, "state": naver_state}
naver_auth_url = f"https://nid.naver.com/oauth2.0/authorize?{urllib.parse.urlencode(naver_params)}"
# ====================================================================================

# 버튼에 집어 넣을 내역을 dictionary 형태로 작성
social_providers = [
 { "text": "Continue with Google", "text_color": ft.Colors.BLACK, "logo": "http://192.168.0.43:9000/logo/web_neutral_rd_na@3x.png", "icon_size": 24, "url": google_auth_url },
 { "text": "Continue with Naver", "text_color": ft.Colors.BLACK, "logo": "http://192.168.0.43:9000/logo/NAVER_login_Light_KR_white_icon_H56.png", "icon_size": 24, "url": naver_auth_url },
 { "text": "Continue with Kakao", "text_color": ft.Colors.BLACK, "logo": "http://192.168.0.43:9000/logo/kakaotalk_sharing_btn_small.png", "icon_size": 18, "url": kakao_auth_url },
]

# 1. 구글 로그인 처리하기
async def process_google_login(code:str):
    print(f"구글 코드 전달: {code}") # 구글 서버에서 google_auth_url을 보내고 response  받은 코드 값
    google_res = requests.post( ## 구글에 대한 응답을 의미
        "https://oauth2.googleapis.com/token",       
        data={
            "code": code, "client_id": google_client_id, "client_secret": google_client_secret, 
            "redirect_uri": google_direct_url, "grant_type": "authorization_code",
        }
    )
    google_token_data = google_res.json() # 구글에 대한 응답을 json 현태로 풀어 token으로 지정
    if "access_token" in google_token_data:
        google_user_res = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {google_token_data["access_token"]}"}                
        ).json() # access_token을 확인 후 정보 
        google_email = google_user_res.get("email")
        google_name = google_user_res.get("name")
        print(f"구글 추출 확인용: {google_user_res}")
        print("★★★ google 출력 결과 ★★★")
        print(f"이름: {google_name} \n이메일: {google_email}")
        ### 구글 데이터를 DB로 전달하기 위해 json 형식으로 포장
        user_data={
            "provider":"google",
            "email":google_email,
            "name":google_name
        }
        print(user_data)
        return True
    else:
        print(f"토큰발급에러: {google_token_data}")
        return False

# 💡 2. 카카오 로그인 처리
async def process_kakao_login(code:str):
    print(f"카카오 코드 전달: {code}") 
    kakao_res = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
        data = {
            "grant_type": "authorization_code", "client_id": kakao_client_id, "client_secret": kakao_client_secret,
            "redirect_uri": kakao_client_url, "code": code,
        }
    )
    kakao_token_data = kakao_res.json()
    if "access_token" in kakao_token_data:
        kakao_user_res = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {kakao_token_data["access_token"]}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
            }
        ).json()
        print(f"카카오 res 데이터: {kakao_user_res}")
        kakao_account = kakao_user_res.get("kakao_account", {})
        kakao_profile = kakao_account.get("profile", {})
        kakao_email = kakao_account.get("email", "이메일 정보 없음")
        kakao_nickname = kakao_profile.get("nickname", "닉네임 정보가 없음")
        kakao_name = kakao_account.get("name", "이름 정보가 없음")
        print(f"카카오 추출 확인용: {kakao_res}")
        print("★★★ 카카오 정보 출력 ★★★")
        print(f"이름: {kakao_name} \n이메일: {kakao_email}")
        user_data={
            "provider": "kakao",
            "email": kakao_email,
            "name": kakao_name
        }
        print(user_data)
        return True
    else:
        print(f"카카오 토큰 에러: {kakao_token_data}")
        return False

# 💡 3. 네이버 로그인 처리
async def process_naver_login(code:str):
    print(f"네이버 코드 전달: {code}")
    naver_res = requests.post(
        "https://nid.naver.com/oauth2.0/token",
        data={
            "grant_type": "authorization_code", "client_id": naver_client_id,
            "client_secret": naver_client_secret, "code": code, "state": naver_state 
        }       
    )
    naver_token_data = naver_res.json()
    if "access_token" in naver_token_data:
        naver_user_res = requests.get(
            "https://openapi.naver.com/v1/nid/me",
            headers={"Authorization": f"Bearer {naver_token_data["access_token"]}"}
        ).json()
        naver_response = naver_user_res.get("response", {})
        naver_email = naver_response.get("email", "이메일 정보가 없음")
        naver_name = naver_response.get("name", "이름 정보가 없음")
        print("★★★ 네이버 정보 출력 ★★★")
        print(f"전체 정보(추출확인용): {naver_res}")
        print(f"이름: {naver_name} \n이메일: {naver_email}")
        user_data={
            "provider": "naver",
            "email": naver_email,
            "name": naver_name            
        }
        print(user_data)
        return True
    else:
        print(f"네이버 토큰 에러: {naver_token_data}")
        return False

# 💡 4. 라우터 핸들러 (프론트엔드에서 가져다 쓸 핵심 매니저)
# 주의: Flet의 on_route_change 이벤트는 핸들러에게 항상 "e(이벤트)" 하나만 넘겨줍니다. 
async def master_route_handler(e: ft.RouteChangeEvent):
    page = e.page 
    current_route = e.route  # 이벤트 발생시 방금 도착한 주소를 가져옴(리다이렉트 등록된 주소)

    print(f"테스트: {current_route} 라우터 감지확인")
    parsed_url = urllib.parse.urlparse(current_route) # 각 소셜 서버(값 요청을 받기 위해 이동)
    query_params = urllib.parse.parse_qs(parsed_url.query) # 소셜 인증을 위해 가지고 오는 코드값

    #if "code" not in query_params:
     #   print(f"코드없음, 무시됨(현재주소: {current_route})")
      #  return
    if "code" in query_params:
        code = query_params["code"][0] # 소셜 인증을 위해 가지고 오는 코드값
    
        if page.session.store.get("last_code") == code: # session.store은 중복 방지 목적으로, 현 code가 이전 번호와 같다면 이미 처리된 코드라는 값을 return 해줌
            print("이미 처리된 코드")
            return
        ## 새로운 코드 시 세션에 저장
        page.session.store.set("last_code", code)
        print(f"새로운 코드 감지 자동 로그인 시작: {code}")

        is_success = False
        # 각 도착 주소(path)에 따라서 알맞은 함수로 전달(google/kakao/naver)
        if parsed_url.path == "/callback/google":
            is_success = await process_google_login(code)
        elif parsed_url.path == "/callback/kakao":
            if page.session.store.get("used_kakao_code") == code:
                return
            page.session.store.set("used_kakao_code", code)
            is_success = await process_kakao_login(code)
        elif parsed_url.path == "/callback/naver":
            is_success = await process_naver_login(code)