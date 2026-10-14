# 파이썬 공식 가벼운 이미지 사용
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 패키지 목록 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 클라우드 런 기본 포트(8080) 설정 및 Gunicorn 실행
ENV PORT=8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
