from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from backend.services.user_service import UserService

# APIRouter:
# 여러 API를 묶어서 관리하기 위한 FastAPI 라우터 객체입니다.
router = APIRouter()

class UserProfileCreateRequest(BaseModel):
    """
    프론트에서 받을 요청 바디 형식,
    프론트가 JSON으로 보내는 값이 이 구조와 맞는지 검사
    """
    email: EmailStr   # 이메일 형식 검사까지 해줌
    nickname: str
    password: str

# 프론트가 보낸 JSON을 자동으로 파싱
@router.post("/user")
def create_user_profile(payload: UserProfileCreateRequest):
    """
    사용자 정보 저장 API

    프론트가 보낸 JSON 예시:
    {
        "email": "test@test.com",
        "nickname": "주희",
        "password": "1234"
    }
    """

    try:
        # service에게 실제 처리 맡기기
        user = UserService.create_user_profile(
            email=payload.email,
            nickname=payload.nickname,
            password=payload.password
        )

        # 프론트에 성공 응답 반환
        return {
            "success": True,
            "message": "사용자 정보가 저장되었습니다.",
            "data": user
        }

    except ValueError as e:
        # 이메일 중복 같은 "예상 가능한 오류"
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        print("!!! 실제 에러:", e)
        raise HTTPException(status_code=500, detail=str(e))