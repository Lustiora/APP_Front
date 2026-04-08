@echo off
set "RULE_NAME=APP Test"
set "PORT=34636"

:: 관리자 권한 체크
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [오류] 관리자 권한으로 실행해야 합니다. 
    echo 파일을 우클릭하여 '관리자 권한으로 실행'을 선택해주세요.
    pause
    exit /b
)

echo [%RULE_NAME%] 인바운드 및 아웃바운드 규칙 생성 중...

:: 인바운드 규칙 추가 (TCP)
netsh advfirewall firewall add rule name="%RULE_NAME%" dir=in action=allow protocol=TCP localport=%PORT%

:: 아웃바운드 규칙 추가 (TCP)
netsh advfirewall firewall add rule name="%RULE_NAME%" dir=out action=allow protocol=TCP localport=%PORT%

echo.
echo --------------------------------------------------
echo 설정이 완료되었습니다!
echo 포트: %PORT%
echo 규칙 이름: %RULE_NAME%
echo --------------------------------------------------
pause