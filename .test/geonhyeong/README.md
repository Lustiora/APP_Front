# .env
 보안관련 시크릿 키 및 DB 연결 관련 정보 보관

 ## 보관위치(구)
  D:\macoding\dogdog-project

# signinup_view
 가장 기초적인 front 내역임(이전과 변화는 거의 없음)

 oauth_api와 연결되어 있음(서버 연결 관련)

 ## 보관위치(구)
 D:\macoding\dogdog-project\app\domains\auth\views

# oauth_api
 소셜 서버와 연결해서 클릭에 따라 필요한 위치로 옮겨주는 안내소 느낌
 **신규/기존 회원에 따른 라우터 설정은 이곳에서 처리**
 *84줄 확인*

 oauth_service와 연결되어 있음(DB와 연결)

 ## 보관위치(구)
 D:\macoding\dogdog-project\backend\app\domains\auth\api

# oauth_service
 실제 소셜에서 데이터를 빼내고(email) DB에 실제로 연결하여 저장하는 역할

 db.py와 연결되어 있음

 ## 보관 위치 (구)
 D:\macoding\dogdog-project\backend\app\domains\auth\service

# db.py
 db와 연결하기 위한 키/포트 등 내역을 정리해놓은 파일

 ## 보관위치(구)
 D:\macoding\dogdog-project\app