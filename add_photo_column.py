#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
학생 테이블에 사진 경로 컬럼 추가 스크립트
"""

import sys
import os

# 프로젝트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pyqt5_app'))

from pyqt5_app.database.db_manager import DatabaseManager

def add_photo_column():
    """학생 테이블에 photo_path 컬럼 추가"""
    db = DatabaseManager()
    
    try:
        if not db.connect():
            print("❌ 데이터베이스 연결 실패")
            return False
        
        print("📊 학생 테이블에 사진 경로 컬럼 추가 중...")
        
        # photo_path 컬럼 추가 (이미 있으면 무시됨)
        alter_query = """
            ALTER TABLE students 
            ADD COLUMN photo_path VARCHAR(500) COMMENT '학생 사진 파일 경로'
        """
        
        try:
            db.execute_query(alter_query)
            print("✅ photo_path 컬럼이 추가되었습니다.")
        except Exception as e:
            if 'Duplicate column name' in str(e):
                print("ℹ️  photo_path 컬럼이 이미 존재합니다.")
            else:
                print(f"⚠️  컬럼 추가 중 오류: {str(e)}")
        
        # 인덱스 추가
        try:
            index_query = "CREATE INDEX idx_students_photo ON students(photo_path)"
            db.execute_query(index_query)
            print("✅ 인덱스가 추가되었습니다.")
        except Exception as e:
            if 'Duplicate key name' in str(e):
                print("ℹ️  인덱스가 이미 존재합니다.")
            else:
                print(f"⚠️  인덱스 추가 중 오류: {str(e)}")
        
        # 현재 테이블 구조 확인
        print("\n📋 현재 students 테이블 구조:")
        desc_query = "DESCRIBE students"
        columns = db.fetch_all(desc_query)
        
        if columns:
            for col in columns:
                col_name = col.get('Field', '')
                col_type = col.get('Type', '')
                col_null = col.get('Null', '')
                col_key = col.get('Key', '')
                col_default = col.get('Default', '')
                
                print(f"  - {col_name}: {col_type} (NULL: {col_null}, KEY: {col_key}, DEFAULT: {col_default})")
        
        print("\n✅ 작업 완료!")
        print("\n💡 이제 학생 관리 화면에서 사진을 등록할 수 있습니다:")
        print("   1. python main_kdt_full.py 실행")
        print("   2. 학생 관리 탭 열기")
        print("   3. 학생 정보 입력 후 '📷 사진 등록' 버튼 클릭")
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.disconnect()

if __name__ == '__main__':
    print("=" * 60)
    print("학생 사진 경로 컬럼 추가 스크립트")
    print("=" * 60)
    print()
    
    success = add_photo_column()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ 모든 작업이 완료되었습니다!")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 작업 중 오류가 발생했습니다.")
        print("=" * 60)
        sys.exit(1)
