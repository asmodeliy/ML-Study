# ML Study - MLOps 학습 로드맵

MLOps를 위한 단계별 학습 프로젝트입니다.

## 학습 로드맵

### 1단계: Python 기초 (2-3주)
- **NumPy**: 배열 연산, 선형대수
- **Pandas**: 데이터 처리, 전처리
- **Matplotlib/Seaborn**: 데이터 시각화

### 2단계: ML 기초 (2-3주)
- **Scikit-learn**: 지도/비지도학습
- **모델 파이프라인**: 학습→평가→최적화

### 3단계: MLOps 도구 (3-4주)
- **Docker**: 모델 컨테이너화
- **FastAPI**: REST API 서버
- **MLflow**: 실험 관리

### 4단계: GCP 배포 (2-3주)
- **Vertex AI**: 모델 학습/배포
- **Cloud Run**: 서버리스 배포

### 5단계: 모니터링 (1-2주)
- 모델 성능 모니터링
- 데이터 드리프트 감지

## 폴더 구조

```
ML-Study/
├── 01-python-basics/      # Python 기초
├── 02-ml-basics/          # ML 기초
├── 03-mlops-tools/        # MLOps 도구
├── 04-gcp-deployment/     # GCP 배포
└── 05-monitoring/         # 모니터링
```

## 환경 설정

```bash
# 가상환경 생성
python -m venv venv
venv\Scripts\activate  # Windows

# 필요 패키지 설치
pip install numpy pandas matplotlib scikit-learn jupyter
```

## 시작하기

각 폴더의 `.ipynb` 파일을 Jupyter Notebook으로 열어서 학습하세요.

```bash
jupyter notebook
```
