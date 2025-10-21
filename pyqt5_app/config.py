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
