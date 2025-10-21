# PyQt5 애플리케이션

이 프로젝트는 PyQt5를 사용한 데스크톱 애플리케이션입니다.

## 설치 방법 (Windows)

### 1. Conda 가상환경 생성 및 활성화
```bash
conda create -n pyqt5_app python=3.10
conda activate pyqt5_app
```

### 2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법
```bash
python main.py
```

## 프로젝트 구조
```
pyqt5_app/
├── main.py              # 메인 실행 파일
├── ui/                  # UI 관련 파일
│   ├── main_window.py   # 메인 윈도우
│   └── dialogs.py       # 다이얼로그들
├── models/              # 데이터 모델
│   └── database.py      # DB 연결 및 모델
├── utils/               # 유틸리티 함수
│   └── helpers.py       # 헬퍼 함수들
└── resources/           # 리소스 파일 (아이콘, 이미지 등)
```

## 데이터베이스 설정

`config.py` 파일에서 데이터베이스 연결 정보를 수정하세요:
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}
```
