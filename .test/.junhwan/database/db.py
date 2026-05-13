import pg8000.dbapi as psycopg2


# ============================================================
# ✅ DB 연결
# - PostgreSQL 연결 생성 함수
# ============================================================
def get_connection():
    return psycopg2.connect(
        host="",
        port=0000,
        database="",
        user="",
        password="",
        timeout=3,
    )
