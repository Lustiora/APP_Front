import psycopg2
from psycopg2.extras import RealDictCursor

# db 연결 코드
def get_connection():
    return psycopg2.connect(
        host="192.168.0.43",
        database="dogdog",
        user="postgres",
        password="tiger",
        port=9934,
        cursor_factory=RealDictCursor
    )