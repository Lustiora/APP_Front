import flet as ft
import urllib.parse
import os
from dotenv import load_dotenv

# 🚨 이따가 우리가 만들 Service 파일에서 '통합 처리 함수'를 가져옵니다.
from backend.app.domains.auth.service.oauth_service import process_social_login

load_dotenv()

# ==========================================
# 1. 환경변수 및 소셜 인증 URL 세팅 (UI 버튼용)
# ==========================================
NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_DIRECT_URI = os.getenv("NAVER_DIRECT_URI", "").strip()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
# 현재 구글 http 포트는 보안 문제로 연결이 불가능함 -> So localhost로 연결하면 실제 사용이 가능하며 이는 비즈니스용으로 사전 확인된 계정 외에도 로그인이 가능하다.
GOOGLE_DIRECT_URI = os.getenv("GOOGLE_DIRECT_URI2","").strip()
#GOOGLE_DIRECT_URI = os.getenv("GOOGLE_DIRECT_URI", "").strip() # 포트가 연결된 URI => 현재 연결 안됨.
KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_URI = os.getenv("KAKAO_CLIENT_URI", "").strip()

# 각 소셜 서버 인증 주소 생성
google_params = {"client_id": GOOGLE_CLIENT_ID, "redirect_uri": GOOGLE_DIRECT_URI, "response_type": "code", "scope": "openid email profile"}
google_auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(google_params)}"

kakao_params = {"client_id": KAKAO_CLIENT_ID, "redirect_uri": KAKAO_CLIENT_URI, "response_type": "code", "prompt": "consent"}
kakao_auth_url = f"https://kauth.kakao.com/oauth/authorize?{urllib.parse.urlencode(kakao_params)}"

naver_state = 'flet_login_test_state_1234'
naver_params = {"response_type": "code", "client_id": NAVER_CLIENT_ID, "redirect_uri": NAVER_DIRECT_URI, "state": naver_state}
naver_auth_url = f"https://nid.naver.com/oauth2.0/authorize?{urllib.parse.urlencode(naver_params)}"

# ==========================================
# 2. UI에 그릴 소셜 로그인 버튼 데이터
# ==========================================
social_providers = [
    { "text": "Continue with Google", "text_color": ft.Colors.BLACK, "logo": 'http://localhost:9000/logo/web_neutral_rd_na@3x.png', "icon_size": 24, "url": google_auth_url },
    { "text": "Continue with Naver", "text_color": ft.Colors.BLACK, "logo": 'http://localhost:9000/logo/NAVER_login_Light_KR_white_icon_H56.png', "icon_size": 24, "url": naver_auth_url },
    { "text": "Continue with Kakao", "text_color": ft.Colors.BLACK, "logo": 'http://localhost:9000/logo/kakaotalk_sharing_btn_small.png', "icon_size": 18, "url": kakao_auth_url },
]

# ==========================================
# 3. 핵심 라우터 매니저
#      목적: 소셜 로그인을 시도 -> 로그인 후 다시 돌아는 순간(callback)을 감시하고 처리하는 역할을 수행
# ==========================================
async def master_route_handler(e: ft.RouteChangeEvent):
    page = e.page 
    current_route = e.route # 이벤트가 발생한 주소 선언

    print(f"📍 라우터 도착: {current_route}")
    parsed_url = urllib.parse.urlparse(current_route) # 주소가 바뀌면 urllib.parse 기능을 통해 인터넷 주소 => 파이썬 언어로 변경
    query_params = urllib.parse.parse_qs(parsed_url.query)  # 파이썬 언어를 쪼갬

    ## 변환한 URL에(query_params에 'code' [서버 정보 추출을 위한 임시 토큰']이 없는 경우? => 그냥 종료
    if 'code' not in query_params:
        return
    code = query_params['code'][0] 
    
    ## 새로고침으로 인해 같은 코드가 두 번 중복으로 반복되는 것을 방지하는 조건식
    if page.session.store.get('last_code') == code: # 마지막에 세션에 보관된 code가 동일하면 => 동일한 코드라 알리고 종료
        print('⚠️ 이미 처리된 코드입니다.')
        return
    page.session.store.set('last_code', code) # => 세션(사용자 메모리)에 방금 처리된 정보를 저장해둠...

    # 1. 사용자의 주소를 확인 후 auth_type을 판별하는 작업(Redirect URL에 적어둔 내역임...) ++++++++++++++++++++++++++
    auth_type = None
    if parsed_url.path == "/callback/google":
        auth_type = "google"
    elif parsed_url.path == '/callback/kakao':
        auth_type = "kakao"
    elif parsed_url.path == "/callback/naver":
        auth_type = "naver"

    if not auth_type: # auth_type 이 없으면 => 종료
        return

    print(f'🚀 [{auth_type}] 로그인 처리 Service로 전달 (Code: {code})')

    # 2. 통신 및 DB 저장은 Service에게 일괄 위임! => 여기분터 oauth_service.py에 넘겨짐
    result = process_social_login(auth_type, code)

    # 3(임시): 필요에 따라 페이지를 이동하는 기능을 구현했지만 일단 Onboarding으로 이동시키는 로직으로 고정한다...
    if result.get("status") == "success":
        print(f"테스트 로그인 성공(신규기존 구분 안함 >> {result}")
        is_new = result.get("is_new_user", False)
        page.go("/onboarding_1")


    # 3. oauth_service.py의 테스트를 성공? => 성공 출력(실패면 실패를 출력) 추후에 onboarding & main 페이지가 생기면 이곳에 연결하면 됨. =====
    # if result.get("status") == "success":
    #     print(f"✅ 로그인 성공: {result}")
    #     is_new = result.get("is_new_user", False)
    #
    #     if is_new:
    #         print("신규회원, onboarding_1으로 이동")
    #         page.go("/onboarding_1")
    #     else:
    #         print("기존회원, 메인으로 이동")
    #         page.go("/main")
    # else:
    #     print(f"❌ 로그인 실패: {result.get('message')}")
    # ==========================================================================================================================