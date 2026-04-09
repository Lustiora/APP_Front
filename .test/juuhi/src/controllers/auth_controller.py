import requests

# 백엔드 서버 기본 주소
BASE_URL = "http://127.0.0.1:8000"


def create_user_profile(email: str, nickname: str, password: str):
    """
    사용자 정보를 백엔드 API로 전송하는 함수

    매개변수:
    - email: 사용자가 입력한 이메일
    - nickname: 사용자가 입력한 닉네임
    - password: 사용자가 입력한 비밀번호

    반환값:
    - 백엔드 응답 JSON(dict)

    예외:
    - 실패 시 Exception 발생
    """

    # 최종 요청 URL
    url = f"{BASE_URL}/app/user"

    # 백엔드에 보낼 JSON 데이터
    payload = {
        "email": email,
        "nickname": nickname,
        "password": password
    }

    try:
        # POST 요청 전송
        response = requests.post(
            url,
            json=payload,
            timeout=5
        )

        # 200번대가 아니어도 일단 응답은 올 수 있으므로 직접 분기 처리
        if response.status_code == 200:
            return response.json()

        # 에러 응답 처리
        try:
            error_data = response.json()
            message = error_data.get("detail", "요청에 실패했습니다.")
        except Exception:
            message = "서버 응답을 해석할 수 없습니다."

        raise Exception(message)

    except requests.exceptions.ConnectionError:
        raise Exception("백엔드 서버에 연결할 수 없습니다.")

    except requests.exceptions.Timeout:
        raise Exception("요청 시간이 초과되었습니다.")

    except Exception as e:
        raise Exception(str(e))