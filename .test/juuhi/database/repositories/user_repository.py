from database.db import get_connection

class UserRepository:
    """
    users 테이블에 대한 DB 작업을 담당하는 클래스

    1) 이메일 중복 확인
    2) 사용자 저장

    """

    @staticmethod
    def create_customer(email, nickname, password_hash):
        conn = get_connection()  # DB 연결 열기

        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    with sign_up as (insert into "Companion".customer default values returning customer_id)
                    insert into "Companion".customer_detail (customer_id, email, nickname, password)
                    values ((select customer_id from sign_up), %s, %s, %s)
                    RETURNING customer_id, email, nickname, create_date;
                    """,
                    (email, nickname, password_hash)
                )

                # INSERT 후 RETURNING으로 방금 저장된 행 받기
                user = cur.fetchone()

                # INSERT/UPDATE/DELETE는 commit 해야 진짜 반영됨
                conn.commit()

                return user

        except Exception:
            # 오류가 나면 DB 반영 취소
            conn.rollback()
            raise

        finally:
            # 연결 닫기
            conn.close()