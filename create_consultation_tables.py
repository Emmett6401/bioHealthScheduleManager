#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql
import sys
import os

# config_db 모듈에서 DB 설정 가져오기
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyqt5_app'))
from config_db import DB_CONFIG

def create_consultation_tables():
    """면담 관리를 위한 데이터베이스 테이블 생성"""
    try:
        # 데이터베이스 연결
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['passwd'],
            db=DB_CONFIG['db'],
            charset=DB_CONFIG.get('charset', 'utf8mb4'),
            port=DB_CONFIG.get('port', 3306),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        with connection.cursor() as cursor:
            # SQL 파일 읽기
            with open('create_consultation_tables.sql', 'r', encoding='utf-8') as f:
                sql_script = f.read()
            
            # SQL 문을 세미콜론으로 분리하여 실행
            sql_commands = sql_script.split(';')
            
            for command in sql_commands:
                command = command.strip()
                if command:
                    print(f"실행 중: {command[:50]}...")
                    cursor.execute(command)
            
            connection.commit()
            print("\n✅ 면담 관리 테이블이 성공적으로 생성되었습니다!")
            print("   - consultations (면담 정보)")
            print("   - consultation_photos (면담 사진)")
            
    except pymysql.Error as e:
        print(f"❌ 데이터베이스 오류: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ create_consultation_tables.sql 파일을 찾을 수 없습니다.")
        sys.exit(1)
    finally:
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    create_consultation_tables()
