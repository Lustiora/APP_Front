from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.app_api import router as app_router

# FastAPI 앱 생성
app = FastAPI(
    title="DogDog Backend",
    description="앱/ERP 공통 백엔드 서버",
    version="1.0.0"
)

# CORS 설정
# 프론트와 백엔드가 서로 다른 주소/포트를 쓸 때 요청 허용을 위한 설정입니다.
# 지금은 테스트 단계이므로 모두 허용(*) 처리합니다.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app_api.py의 라우터를 "/app" prefix와 함께 등록
# 그래서 실제 주소는 "/user"이 아니라 "/app/user"이 됩니다.
app.include_router(app_router, prefix="/app")