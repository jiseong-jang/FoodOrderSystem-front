#!/bin/bash

# 환경 변수 기본값 설정
export PORT=${PORT:-80}
export SPRING_DATASOURCE_URL=${SPRING_DATASOURCE_URL}
export SPRING_DATASOURCE_USERNAME=${SPRING_DATASOURCE_USERNAME}
export SPRING_DATASOURCE_PASSWORD=${SPRING_DATASOURCE_PASSWORD}
export JWT_SECRET=${JWT_SECRET}
export FRONTEND_URL=${FRONTEND_URL:-http://localhost:${PORT}}

# FastAPI 환경 변수
export VOICE_ORDER_CLIENT_ORIGIN=${VOICE_ORDER_CLIENT_ORIGIN:-http://localhost:${PORT}}
export VOICE_ORDER_MODEL_PRESET=${VOICE_ORDER_MODEL_PRESET:-openai}
export OPENAI_API_KEY=${OPENAI_API_KEY}
export VOICE_ORDER_CHAT_MODEL=${VOICE_ORDER_CHAT_MODEL:-gpt-4o-mini}
export VOICE_ORDER_HF_ENDPOINT=${VOICE_ORDER_HF_ENDPOINT}
export VOICE_ORDER_HF_MODEL=${VOICE_ORDER_HF_MODEL}
export VOICE_ORDER_HF_TOKEN=${VOICE_ORDER_HF_TOKEN}

# Nginx 설정 파일에서 PORT 변수 치환
sed -i "s/__PORT__/${PORT}/g" /etc/nginx/conf.d/default.conf

# Supervisor 시작
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf

