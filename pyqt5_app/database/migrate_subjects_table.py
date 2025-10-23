# -*- coding: utf-8 -*-
"""
교과목 테이블 마이그레이션 스크립트
새로운 컬럼 추가: day_of_week, is_biweekly, week_offset
"""

import pymysql
import sys
import os

# 상위 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_db import DB_CONFIG


def migrate_subjects_table():
    """subjects 테이블에 새로운 컬럼 추가"""
    try:
        # 데이터베이스 연결
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['passwd'],
            db=DB_CONFIG['db'],
            charset=DB_CONFIG['charset'],
            port=DB_CONFIG['port']
        )
        
        cursor = connection.cursor()
        
        print("=== 교과목 테이블 마이그레이션 시작 ===")
        
        # 1. day_of_week 컬럼 추가
        try:
            cursor.execute("""
                ALTER TABLE subjects 
                ADD COLUMN day_of_week INT 
                COMMENT '요일: 0=월, 1=화, 2=수, 3=목, 4=금'
                AFTER hours
            """)
            print("✓ day_of_week 컬럼 추가 완료")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("- day_of_week 컬럼이 이미 존재합니다")
            else:
                raise
        
        # 2. is_biweekly 컬럼 추가
        try:
            cursor.execute("""
                ALTER TABLE subjects 
                ADD COLUMN is_biweekly BOOLEAN DEFAULT FALSE 
                COMMENT '격주 여부'
                AFTER day_of_week
            """)
            print("✓ is_biweekly 컬럼 추가 완료")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("- is_biweekly 컬럼이 이미 존재합니다")
            else:
                raise
        
        # 3. week_offset 컬럼 추가
        try:
            cursor.execute("""
                ALTER TABLE subjects 
                ADD COLUMN week_offset INT DEFAULT 0 
                COMMENT '격주인 경우: 0=1주차, 1=2주차'
                AFTER is_biweekly
            """)
            print("✓ week_offset 컬럼 추가 완료")
        except pymysql.err.OperationalError as e:
            if "Duplicate column name" in str(e):
                print("- week_offset 컬럼이 이미 존재합니다")
            else:
                raise
        
        connection.commit()
        
        # 4. 테이블 구조 확인
        cursor.execute("DESCRIBE subjects")
        columns = cursor.fetchall()
        
        print("\n=== 현재 subjects 테이블 구조 ===")
        for col in columns:
            print(f"  {col[0]}: {col[1]}")
        
        print("\n=== 마이그레이션 완료 ===")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 마이그레이션 실패: {str(e)}")
        return False


if __name__ == "__main__":
    migrate_subjects_table()
