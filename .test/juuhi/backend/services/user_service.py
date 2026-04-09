import hashlib
from database.repositories.user_repository import UserRepository

class UserService:
    """
    사용자 관련 비즈니스 로직을 처리하는 서비스 클래스
    """

    @staticmethod
    def create_user_profile(email, nickname, password):
        """
        사용자 프로필 저장 로직

        1. 이메일 중복 확인
        2. 비밀번호를 해시로 변환
        3. DB에 저장
        4. 저장 결과 반환
        """

        # 2) 비밀번호 원문을 바로 저장하면 안 되므로 해시 처리
        # 실제 서비스에서는 bcrypt를 더 많이 사용
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # 3) repository에 저장 요청
        # # 고객
        # customer_id = UserRepository.create_customer()

        # 고객 디테일 - 인증관련
        customer = UserRepository.create_customer(  #email, nickname, password_hash
            email=email,
            nickname=nickname,
            password_hash=password_hash
        )

        # 4) 저장 결과 반환
        return customer