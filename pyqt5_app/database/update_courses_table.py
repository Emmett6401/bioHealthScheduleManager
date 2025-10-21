# -*- coding: utf-8 -*-
"""
courses 테이블 업데이트 스크립트
기존 테이블에 없는 컬럼들을 추가합니다.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager

def update_courses_table():
    """courses 테이블 컬럼 추가"""
    db = DatabaseManager()
    
    if not db.connect():
        print("❌ 데이터베이스 연결 실패")
        return False
    
    print("📊 courses 테이블 업데이트 시작...")
    
    try:
        cursor = db.connection.cursor()
        
        # 기존 테이블 구조 확인
        cursor.execute("DESCRIBE courses")
        existing_columns = [row['Field'] for row in cursor.fetchall()]
        print(f"\n현재 컬럼: {existing_columns}")
        
        # 추가할 컬럼 목록
        columns_to_add = [
            ("start_date", "DATE", "시작일"),
            ("lecture_end_date", "DATE", "강의 종료일"),
            ("project_end_date", "DATE", "프로젝트 종료일"),
            ("internship_end_date", "DATE", "인턴십 종료일"),
            ("final_end_date", "DATE", "최종 종료일"),
            ("lecture_hours", "INT NOT NULL DEFAULT 260", "강의 시간"),
            ("project_hours", "INT NOT NULL DEFAULT 220", "프로젝트 시간"),
            ("internship_hours", "INT NOT NULL DEFAULT 120", "인턴십 시간"),
            ("total_days", "INT", "총 일수"),
        ]
        
        added_count = 0
        
        for col_name, col_type, description in columns_to_add:
            if col_name not in existing_columns:
                try:
                    # 컬럼 추가
                    alter_query = f"ALTER TABLE courses ADD COLUMN {col_name} {col_type}"
                    cursor.execute(alter_query)
                    db.connection.commit()
                    print(f"✅ {col_name} 컬럼 추가 완료 ({description})")
                    added_count += 1
                except Exception as e:
                    print(f"⚠️  {col_name} 컬럼 추가 실패: {str(e)}")
            else:
                print(f"ℹ️  {col_name} 컬럼은 이미 존재합니다")
        
        # 최종 구조 확인
        cursor.execute("DESCRIBE courses")
        final_columns = cursor.fetchall()
        
        print("\n" + "="*60)
        print("📋 최종 테이블 구조:")
        print("="*60)
        for col in final_columns:
            print(f"  {col['Field']:25s} {col['Type']:20s} {col['Null']:5s} {col['Key']:5s} {col['Default'] or ''}")
        print("="*60)
        
        if added_count > 0:
            print(f"\n✨ {added_count}개 컬럼이 추가되었습니다!")
        else:
            print("\n✅ 테이블이 이미 최신 상태입니다!")
        
        db.disconnect()
        return True
        
    except Exception as e:
        print(f"\n❌ 업데이트 실패: {str(e)}")
        db.connection.rollback()
        db.disconnect()
        return False

if __name__ == "__main__":
    print("="*60)
    print("🔧 과정 관리 테이블 업데이트 도구")
    print("="*60)
    print("\n⚠️  주의: 이 스크립트는 courses 테이블에 새로운 컬럼을 추가합니다.")
    print("        기존 데이터는 유지됩니다.\n")
    
    response = input("계속하시겠습니까? (y/n): ")
    
    if response.lower() == 'y':
        if update_courses_table():
            print("\n✅ 업데이트 완료!")
            print("\n이제 프로그램을 실행하세요:")
            print("  python pyqt5_app/ui/kdt_main_window_full.py")
        else:
            print("\n❌ 업데이트 실패")
    else:
        print("\n취소되었습니다.")
