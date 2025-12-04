@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo Python 3.12로 가상환경 재설정
echo ========================================
echo.

REM Python 버전 확인
echo Python 버전 확인 중...
python --version
if errorlevel 1 (
    echo ERROR: Python을 찾을 수 없습니다.
    echo Python 3.12가 설치되어 있고 PATH에 추가되었는지 확인하세요.
    pause
    exit /b 1
)

echo.
echo 기존 가상환경 삭제 중...
if exist ".venv" (
    rmdir /s /q .venv
    echo 기존 가상환경이 삭제되었습니다.
) else (
    echo 기존 가상환경이 없습니다.
)

echo.
echo 새 가상환경 생성 중... (Python 3.12)
python -m venv .venv
if errorlevel 1 (
    echo ERROR: 가상환경 생성 실패
    pause
    exit /b 1
)

echo.
echo 가상환경 활성화 중...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: 가상환경 활성화 실패
    pause
    exit /b 1
)

echo.
echo pip 업그레이드 중...
python -m pip install --upgrade pip setuptools wheel

echo.
echo 필요한 패키지 설치 중...
echo (이 과정은 몇 분이 걸릴 수 있습니다)
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo WARNING: 일부 패키지 설치에 문제가 있었을 수 있습니다.
    echo 하지만 계속 진행합니다...
)

echo.
echo ========================================
echo 설정 완료!
echo ========================================
echo.
echo 이제 다음 명령어로 서버를 시작할 수 있습니다:
echo   start.bat
echo.
echo 또는 수동으로:
echo   call .venv\Scripts\activate.bat
echo   uvicorn app.main:app --reload --host 0.0.0.0 --port 5001
echo.

pause

