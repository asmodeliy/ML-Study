# Cloud Run 배포 가이드

ML 모델을 Google Cloud Run에 배포하는 방법입니다.

## 사전 준비

1. Google Cloud 프로젝트 생성
2. Cloud Run API 활성화
3. Docker 설치
4. gcloud CLI 설치 및 설정

## 1. 프로젝트 구조

```
model-serving/
├── Dockerfile
├── requirements.txt
├── main.py
└── model.pkl
```

## 2. Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
```

## 3. requirements.txt

```
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
joblib==1.3.2
```

## 4. main.py

```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

# 모델 로딩
model = joblib.load("model.pkl")

class PredictionRequest(BaseModel):
    features: list

@app.get("/")
async def root():
    return {"message": "ML Model API"}

@app.post("/predict")
async def predict(request: PredictionRequest):
    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].tolist()
    
    return {
        "prediction": int(prediction),
        "probability": probability
    }
```

## 5. Docker 빌드 및 테스트

```bash
# Docker 이미지 빌드
docker build -t ml-model-api .

# 로컬 테스트
docker run -p 8080:8080 ml-model-api

# 테스트 요청
curl -X POST "http://localhost:8080/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
```

## 6. Google Container Registry에 이미지 푸시

```bash
# GCR 로그인
gcloud auth configure-docker

# 이미지 태그
docker tag ml-model-api gcr.io/your-project-id/ml-model-api

# 이미지 푸시
docker push gcr.io/your-project-id/ml-model-api
```

## 7. Cloud Run 배포

```bash
gcloud run deploy ml-model-api \
  --image gcr.io/your-project-id/ml-model-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10
```

## 8. 배포 확인

```bash
# 서비스 목록 조회
gcloud run services list

# 서비스 상세 정보
gcloud run services describe ml-model-api

# 로그 확인
gcloud run services logs read ml-model-api
```

## 9. API 테스트

```bash
# Cloud Run URL 확인 후 테스트
SERVICE_URL=$(gcloud run services describe ml-model-api --platform managed --region us-central1 --format 'value(status.url)')

curl -X POST "$SERVICE_URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, 3.0, 4.0]}'
```

## 주요 설정 옵션

| 옵션 | 설명 | 기본값 |
|------|------|--------|
| `--memory` | 메모리 할당 | 256Mi |
| `--cpu` | CPU 할당 | 1 |
| `--max-instances` | 최대 인스턴스 수 | 100 |
| `--min-instances` | 최소 인스턴스 수 | 0 (스케일 다운) |
| `--concurrency` | 동시 요청 수 | 80 |
| `--timeout` | 요청 타임아웃 | 300s |

## 비용 최적화 팁

1. **최소 인스턴스 0 설정**: 트래픽 없을 때 비용 절감
2. **컨테이너 이미지 최적화**: 이미지 크기 줄이기
3. **적절한 메모리/CPU**: 오버프로비저닝 방지
4. **클라우드 CDN**: 정적 응답 캐싱

## 문제 해결

### 배포 실패 시
```bash
# 빌드 로그 확인
gcloud run services describe ml-model-api --platform managed --region us-central1

# 이벤트 로그 확인
gcloud run services logs read ml-model-api --limit 50
```

### 권한 문제 시
```bash
# 서비스 계정 권한 확인
gcloud projects get-iam-policy your-project-id
```
