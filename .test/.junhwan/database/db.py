import pg8000.dbapi as psycopg2


# ============================================================
# ✅ DB 연결
# - PostgreSQL 연결 생성 함수
# ============================================================
def get_connection():
    return psycopg2.connect(
        host="pg.nas6418.ddns.net",
        port=9934,
        database="Dogdog",
        user="dog_5",
        password="kosmo",
        timeout=3,
    )
