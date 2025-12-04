# 프론트엔드 배포 가이드

이 레포지토리는 프론트엔드(React + Vite)만 포함되어 있습니다.

## Render 배포 방법

### 방법 1: render.yaml 사용 (추천)

1. **GitHub에 레포지토리 푸시**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Render 대시보드에서 배포**
   - [Render](https://render.com/) 접속
   - "New" → "Blueprint" 선택
   - GitHub 레포지토리 연결
   - Render가 자동으로 `render.yaml`을 인식하여 서비스 생성

3. **환경 변수 설정**
   Render 대시보드 → 서비스 → "Environment" 탭에서 다음 변수 설정:
   ```env
   VITE_API_URL=https://[백엔드 URL]/api
   VITE_VOICE_API_URL=https://[음성인식 API URL]
   ```
   
   예시:
   - `VITE_API_URL=https://mrdinner-backend.onrender.com/api`
   - `VITE_VOICE_API_URL=https://mrdinner-voice-api.onrender.com`

### 방법 2: 수동 설정

1. **Render 대시보드 접속**
   - [Render](https://render.com/)에 로그인

2. **새 Static Site 생성**
   - "New" → "Static Site" 선택
   - GitHub 레포지토리 연결
   - 다음 설정 입력:
     - **Name**: `mrdinner-frontend`
     - **Root Directory**: (비워두기 - 루트가 frontend 폴더이므로)
     - **Build Command**: `npm install && npm run build`
     - **Publish Directory**: `dist`

3. **환경 변수 설정** (위와 동일)

## 환경 변수 설명

- `VITE_API_URL`: 백엔드 API URL (빌드 시점에 주입됨)
- `VITE_VOICE_API_URL`: 음성인식 API URL (빌드 시점에 주입됨)

**중요**: Vite 환경 변수는 빌드 시점에 주입되므로, 환경 변수를 변경하면 재배포가 필요합니다.

## 배포 후 확인

- 프론트엔드 URL: `https://[서비스명].onrender.com`
- 브라우저에서 접속하여 정상 작동 확인

