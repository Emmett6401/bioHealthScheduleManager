# -*- coding: utf-8 -*-
"""
애플리케이션 설정 파일
"""

# 데이터베이스 설정
DB_CONFIG = {
    'type': 'mysql',  # 'mysql', 'postgresql', 'sqlite'
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'your_password',
    'database': 'your_database',
    'charset': 'utf8mb4'
}

# SQLite 사용 시
SQLITE_DB_PATH = 'app_database.db'

# 애플리케이션 설정
APP_NAME = "PyQt5 App"
APP_VERSION = "1.0.0"
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# AI API 설정 (면담일지 생성용)

# 【100% 무료, 영구 무료!】 Hugging Face API 🤗
# 1. https://huggingface.co/ 회원가입 (30초, 완전 무료)
# 2. Settings → Access Tokens → New token
# 3. Read 권한 선택 → Create token
# 4. 아래에 입력 또는 환경 변수 HUGGINGFACE_API_KEY 설정
# 장점: 
# - 100% 무료 (신용카드 불필요)
# - 영구적으로 무료
# - 쿼터 제한 없음
# - 한국어 우수 (Qwen 2.5 모델)
HUGGINGFACE_API_KEY = None  # 여기에 직접 설정: "hf_your-token"
