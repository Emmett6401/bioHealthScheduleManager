# -*- coding: utf-8 -*-
"""
데이터베이스 설정 파일
"""

# MySQL 데이터베이스 설정
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'user': 'iyrc',
    'passwd': 'Dodan1004!',
    'db': 'bh2025',
    'charset': 'utf8',
    'port': 3307,
}

# 애플리케이션 설정
APP_NAME = "바이오헬스 올인원테크 이노베이터 for KDT"
APP_VERSION = "2.0.0"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900

# 코드 접두사 설정
CODE_PREFIX = {
    'instructor': 'T-',      # 강사 코드
    'subject': 'G-',         # 교과목 코드
    'course': 'C-',          # 과정 코드
    'project': 'P-',         # 프로젝트 코드
}
