#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
학생 테이블에 사진 관련 컬럼 추가 스크립트
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyqt5_app'))

from database.db_manager import DatabaseManager

def add_photo_columns():
    """students 테이블에 photo_path와 thumbnail 컬럼 추가"""
    db = DatabaseManager()
    
    try:
        if not db.connect():
            print("❌ 데이터베이스 연결 실패")
            return False
        
        print("📊 students 테이블에 사진 컬럼 추가 중...")
        
        cursor = db.connection.cursor()
        
        # photo_path 컬럼 추가
        try:
            cursor.execute("""
                ALTER TABLE students 
                ADD COLUMN photo_path VARCHAR(500) COMMENT '원본 사진 파일 경로' AFTER campus
            """)
            print("✅ photo_path 컬럼 추가 완료")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("ℹ️  photo_path 컬럼이 이미 존재합니다")
            else:
                print(f"⚠️  photo_path 컬럼 추가 오류: {str(e)}")
        
        # thumbnail 컬럼 추가
        try:
            cursor.execute("""
                ALTER TABLE students 
                ADD COLUMN thumbnail MEDIUMBLOB COMMENT '썸네일 이미지 (150x150)' AFTER photo_path
            """)
            print("✅ thumbnail 컬럼 추가 완료")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("ℹ️  thumbnail 컬럼이 이미 존재합니다")
            else:
                print(f"⚠️  thumbnail 컬럼 추가 오류: {str(e)}")
        
        db.connection.commit()
        
        # 결과 확인
        print("\n📋 students 테이블 구조:")
        cursor.execute("DESC students")
        results = cursor.fetchall()
        for row in results:
            field = row['Field']
            field_type = row['Type']
            print(f"  - {field}: {field_type}")
        
        print("\n✅ 사진 컬럼 추가 작업 완료!")
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.disconnect()

if __name__ == "__main__":
    print("=" * 60)
    print("학생 테이블 사진 컬럼 추가 스크립트")
    print("=" * 60)
    add_photo_columns()
