# FastAPI 서버 설치 및 실행 가이드

## 문제: Python이 제대로 작동하지 않는 경우

터미널에서 `python --version`이 버전을 출력하지 않고 "Python"만 표시되는 경우,
Windows Store의 Python placeholder가 설치되어 있을 수 있습니다.

## 해결 방법

### 방법 1: Conda 사용 (가장 권장)

1. **Miniconda 설치** (가장 가볍고 빠름)
   - 다운로드: https://docs.conda.io/en/latest/miniconda.html
   - Windows 64-bit 설치 프로그램 다운로드 및 실행
   - 설치 시 "Add Miniconda3 to PATH" 체크

2. **새 CMD 창 열기** (중요!)

3. **FastAPI 서버 설정 및 실행:**
   ```cmd
   cd C:\Users\User\Desktop\wpdbr\voice-order-fastapi
   setup-conda.bat
   start-conda.bat
   ```

### 방법 2: Python 직접 설치

1. **Python 공식 사이트에서 설치**
   - 다운로드: https://www.python.org/downloads/
   - **Python 3.10 이상** 다운로드 (3.11 또는 3.12 권장)
   - 설치 시 **반드시 "Add Python to PATH" 체크박스 선택**

2. **Windows Store Python 제거** (선택사항)
   - Windows 설정 > 앱 > Python 검색 후 제거
   - 또는 PowerShell(관리자 권한)에서:
     ```powershell
     Get-AppxPackage *python* | Remove-AppxPackage
     ```

3. **새 CMD 창 열기** (중요!)

4. **확인:**
   ```cmd
   python --version
   ```
   - 버전이 정상적으로 표시되어야 함 (예: "Python 3.11.5")

5. **FastAPI 서버 설정 및 실행:**
   ```cmd
   cd C:\Users\User\Desktop\wpdbr\voice-order-fastapi
   setup.bat
   start.bat
   ```

### 방법 3: 기존 Python 경로 찾아서 사용

Python이 다른 위치에 설치되어 있을 수 있습니다:

1. **Python 경로 확인:**
   ```cmd
   cd C:\Users\User\Desktop\wpdbr\voice-order-fastapi
   check-python-detail.bat
   ```

2. **경로를 찾았다면 직접 사용:**
   ```cmd
   C:\Python311\python.exe -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 5001
   ```

## 권장사항

**Conda를 사용하는 것을 강력히 권장합니다:**
- Python 버전 관리가 쉬움
- 패키지 설치가 안정적
- 가상환경 관리가 편리
- 다른 프로젝트와 충돌 없음

## 설치 후 확인

서버가 정상적으로 실행되면:
- 브라우저에서 `http://localhost:5001/health` 접속
- `{"status":"ok"}` 응답이 나오면 성공!

## 문제가 계속되면

1. `check-python-detail.bat` 실행 결과 확인
2. Python 설치 경로 확인
3. 환경 변수 PATH 확인

