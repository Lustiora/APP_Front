

# # 로컬
# # db 연결 코드
# def get_connection():
#     return psycopg2.connect(
#         host="192.168.0.43",
#         database="dogdog",
#         user="postgres",
#         password="tiger",
#         port=9934,
#         cursor_factory=RealDictCursor
#     )


# # 팀장님 서버 - 테스트용
# # db 연결 코드
import psycopg2
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# .env 파일에서 정보를 불러옵니다.
load_dotenv()

def get_connection():
    try:
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
            cursor_factory=RealDictCursor
        )
    except psycopg2.OperationalError as e:
        print(f"❌ DB 연결 실패! 정보가 맞는지 확인하세요: {e}")
        return None