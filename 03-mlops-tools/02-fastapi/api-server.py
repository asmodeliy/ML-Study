from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd

app = FastAPI(title="ML Model API")

# 모델 로딩
model = None

class PredictionRequest(BaseModel):
    features: list

class PredictionResponse(BaseModel):
    prediction: int
    probability: list

@app.on_event("startup")
async def load_model():
    global model
    try:
        model = joblib.load("model.pkl")
        print("모델 로딩 완료!")
    except Exception as e:
        print(f"모델 로딩 실패: {e}")

@app.get("/")
async def root():
    return {"message": "ML Model API에 오신 것을 환영합니다!"}

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    if model is None:
        return {"error": "모델이 로딩되지 않았습니다."}
    
    features = np.array(request.features).reshape(1, -1)
    prediction = model.predict(features)[0]
    probability = model.predict_proba(features)[0].tolist()
    
    return PredictionResponse(
        prediction=int(prediction),
        probability=probability
    )

@app.post("/batch_predict")
async def batch_predict(requests: list[PredictionRequest]):
    if model is None:
        return {"error": "모델이 로딩되지 않았습니다."}
    
    results = []
    for request in requests:
        features = np.array(request.features).reshape(1, -1)
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0].tolist()
        results.append({
            "prediction": int(prediction),
            "probability": probability
        })
    
    return {"predictions": results}
