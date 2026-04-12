import os

import requests
# .env 파일과 연결됨.
from dotenv import load_dotenv
# 🚨 DB완 연결됨.
from app.db import get_connection

load_dotenv()

# ==========================================
# 1. 환경 변수 세팅( 필요한 정보를 소셜에서 빼내오기 위해서 필요함.)
# ==========================================
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
# 현재 구글 http 포트는 보안 문제로 연결이 불가능함 -> So localhost로 연결하면 실제 사용이 가능하며 이는 비즈니스용으로 사전 확인된 계정 외에도 로그인이 가능하다.
GOOGLE_DIRECT_URI = os.getenv("GOOGLE_DIRECT_URI2").strip()
#GOOGLE_DIRECT_URI = os.getenv("GOOGLE_DIRECT_URI", "").strip() # 포트가 연결된 URI => 현재 연결 안됨.

KAKAO_CLIENT_ID = os.getenv("KAKAO_CLIENT_ID")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
KAKAO_CLIENT_URI = os.getenv("KAKAO_CLIENT_URI", "").strip()

NAVER_CLIENT_ID = os.getenv("NAVER_CLIENT_ID")
NAVER_CLIENT_SECRET = os.getenv("NAVER_CLIENT_SECRET")
NAVER_STATE = os.getenv("NAVER_STATE")

# ==========================================
# 2. 💡 [통합 진입점] API 라우터가 호출하는 단 하나의 함수
#       목적: 소셜과 서버의 통신 => 유저 정보 획득하기(email) => 소셜 통신
#            DB에서 유저 조회 및 저장하기 => 회원 가입
# ==========================================
def process_social_login(auth_type: str, code: str):

 
 # 1단계: 소셜 서버와 통신하여 유저 정보 획득 (하단의 각 user_info를 를 가져오는 로직 확인(code를 통해 가져옴)
 if auth_type == "google":
     user_info = get_google_user_info(code)
 elif auth_type == "kakao":
     user_info = get_kakao_user_info(code)
 elif auth_type == "naver":
     user_info = get_naver_user_info(code)
 else:
     return {"status": "error", "message": "지원하지 않는 소셜 로그인입니다."}

 # 통신 에러 발생 시 즉시 중단
 if user_info.get("status") == "error":
     return user_info

 email = user_info.get("email")
 name = user_info.get("name", "새로운친구") # DB의 nickname(NOT NULL) 컬럼에 들어갈 값
 auth_type = user_info.get("auth_type")

 # 2단계: DB에서 유저 조회 및 저장 (Repository 로직)
 existing_user = find_user_by_email(email)
 
 if existing_user:
     return {"status": "success", "message": f"[{auth_type}] 기존 회원 로그인 성공", "user": existing_user}
 else:
     new_id = save_new_user(email, name, auth_type)
     if new_id:
         return {"status": "success", "message": f"[{auth_type}] 신규 회원 가입 성공", "user_id": new_id}
     else:
         return {"status": "error", "message": "DB 저장 중 오류가 발생했습니다."}


# ==========================================
# 3. 🌐 [Service 로직] 소셜사별 외부 API 통신 -> 외부 API와 통신해서 필요한 자료(email)을 출력함
# ==========================================
## 1. 구글 API 통신하기 => 이하 카카오/네이버도 방식은 동일하다.
def get_google_user_info(code: str) -> dict:
 try:
     ### 1단계) code 를 실제 token으로 변경하기(상단 환경변수를 이곳에서 사용
     token_res = requests.post(
         "https://oauth2.googleapis.com/token",
         data={
             "code": code, "client_id": GOOGLE_CLIENT_ID, "client_secret": GOOGLE_CLIENT_SECRET,
             "redirect_uri": GOOGLE_DIRECT_URI, "grant_type": "authorization_code"
         }
     ).json()

     ### 2단계) data가 맞다면 access_token을 발급해줌
     if "access_token" not in token_res:
         return {"status": "error", "message": f"구글 토큰 발급 실패: {token_res}"}

     ### 3단계) access_token을 기반으로 유저의 데이터를 추출해줌
     user_res = requests.get(
         "https://www.googleapis.com/oauth2/v3/userinfo",
         headers={"Authorization": f"Bearer {token_res['access_token']}"}
     ).json()

     ### 4단계) 최종 return (성공여부, auth_type, 이메일)
     print(user_res)
     return {"status": "success", "auth_type": "google", "email": user_res.get("email")}
 except Exception as e:
     return {"status": "error", "message": str(e)}

def get_kakao_user_info(code: str) -> dict:
 try:
     token_res = requests.post(
         "https://kauth.kakao.com/oauth/token",
         headers={"Content-type": "application/x-www-form-urlencoded;charset=utf-8"},
         data={
             "grant_type": "authorization_code", "client_id": KAKAO_CLIENT_ID,
             "client_secret": KAKAO_CLIENT_SECRET, "redirect_uri": KAKAO_CLIENT_URI, "code": code
         }
     ).json()
     
     if "access_token" not in token_res:
         return {"status": "error", "message": f"카카오 토큰 발급 실패: {token_res}"}
         
     user_res = requests.get(
         "https://kapi.kakao.com/v2/user/me",
         headers={"Authorization": f"Bearer {token_res['access_token']}"}
     ).json()
     
     kakao_account = user_res.get('kakao_account', {})
     print(user_res)
     return {
         "status": "success", "auth_type": "kakao",
         "email": kakao_account.get("email"),
     }
 except Exception as e:
     return {"status": "error", "message": str(e)}

def get_naver_user_info(code: str) -> dict:
 try:
     token_res = requests.post(
         "https://nid.naver.com/oauth2.0/token",
         data={
             "grant_type": "authorization_code", "client_id": NAVER_CLIENT_ID,
             "client_secret": NAVER_CLIENT_SECRET, "code": code, "state": NAVER_STATE
         }
     ).json()
     
     if "access_token" not in token_res:
         return {"status": "error", "message": f"네이버 토큰 발급 실패: {token_res}"}
         
     user_res = requests.get(
         "https://openapi.naver.com/v1/nid/me",
         headers={"Authorization": f"Bearer {token_res['access_token']}"}
     ).json()
     
     res = user_res.get('response', {})
     print(user_res)
     print(res)
     return {"status": "success", "auth_type": "naver", "email": res.get("email")}
 except Exception as e:
     return {"status": "error", "message": str(e)}

## 2. 신규 기존 회원 =>


# ==========================================
# 4. 🗄️ [Repository 로직] DB 접근 -> 이곳에서 최종적으로 DB와 접촉하며 INSERT, SELECT 역할을 수행함
#    이곳에서 현재 사용중인 dumi 데이터 대신에 실제로 input 한 값을 INSERT 하면 된다.
# ==========================================
## 1-1단계) 회원 여부 확인하기
def find_user_by_email(email: str):
 conn = get_connection() # DB 열쇠를 conn으로 챙김
 cursor = conn.cursor() # 열쇠를 통해 활동할 커서 선언
 try:
     ## 1-2단계) 가지고 온 이메일을 customer_detail에서 같은 이메일을 찾음
     ### tip) 스키마를 잘 찾은면 문제가 없지만, 못찾는다면 "Compainon"처럼 작성을 해줘야함 => 대소문자가 섞인 경우여서 ""로 감쌈
     cursor.execute('SELECT * FROM "Companion".customer_detail WHERE email = %s', (email,))
     return cursor.fetchone() # 있으면 관련한 정보를 가지고 옴
 except Exception as e:
     print(f"DB 조회 중 오류: {e}")
     return None
 finally:
     cursor.close() # 커서 닫기
     conn.close() # DB 종료

## 2-1단계) 새로운 회원 등록하고 번호표 주기
def save_new_user(email: str, nickname: str, oauth_type: str):
 conn = get_connection()
 cursor = conn.cursor()
 try:
     # 1. 실제 테이블 컬럼에 맞춰 INSERT (password에는 더미값 추가)
     # 2. RETURNING customer_id 로 실제 ID 컬럼명 지정
     ## tip) 실제 sql을 작성하는 부분은 """ 로 감싸주어여 하며, VALUES 값에 구멍을 뚫어주고 연결을 해야 함.

     ### 1번) 먼저 customer 테이블에서 새로운 회원을 등록하는 것이 먼저이다.(이후에 외래키로 이어진 customer_detail 이 연결 가능함.
     ### 기본적인 값을 얻고 싶다면 => DEFAULT VALUES로 작성...
     print("DB1")
     cursor.execute(
         """
         INSERT INTO "Companion".customer DEFAULT VALUES
             RETURNING customer_id
         """
     )
     ### 2번) 이후 생성된 진짜 회원번호 가져오기
     print("DB2")
     result = cursor.fetchone()
     new_customer_id = result['customer_id'] ## customer 테이블에서 가져온 진짜 customer_id

    ### 3번) 가져온 customer_id를 기반으로 자식 테이블에 이를 저장함.
     print("DB3")
     sql_query = """
    INSERT INTO "Companion".customer_detail 
        (customer_id, email, oauth_type, password, nickname, phone) 
            VALUES (%s, %s, %s, %s, %s, %s)
     """
     insert_data = (
         new_customer_id,
         email,
         oauth_type,
         "social_dumi_pw2",
         "호빵이",
         "010-5896-7975"
     )
     ### 4번) 실행하기
     cursor.execute(sql_query, insert_data)
    ### 5번) 작업 수행 완료 => 최종 저장하기
     conn.commit()

     return new_customer_id

 except Exception as e:
     conn.rollback()
     print(f"❌ DB 저장 중 에러: {e}")
     return None
 finally:
     cursor.close()
     conn.close()


     
