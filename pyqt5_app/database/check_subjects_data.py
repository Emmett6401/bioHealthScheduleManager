# -*- coding: utf-8 -*-
"""
교과목 데이터 확인 스크립트
"""

import pymysql
import sys
import os

# 상위 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_db import DB_CONFIG


def check_subjects_data():
    """교과목 데이터 상태 확인"""
    try:
        # 데이터베이스 연결
        connection = pymysql.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['passwd'],
            db=DB_CONFIG['db'],
            charset=DB_CONFIG['charset'],
            port=DB_CONFIG['port'],
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        print("=== 교과목 테이블 구조 ===")
        cursor.execute("DESCRIBE subjects")
        columns = cursor.fetchall()
        for col in columns:
            null_str = "NULL 가능" if col['Null'] == 'YES' else "NOT NULL"
            default = f"기본값: {col['Default']}" if col['Default'] is not None else "기본값 없음"
            print(f"  {col['Field']:<20} {col['Type']:<20} {null_str:<15} {default}")
        
        print("\n=== 교과목 데이터 ===")
        cursor.execute("SELECT * FROM subjects")
        subjects = cursor.fetchall()
        
        if not subjects:
            print("  교과목 데이터가 없습니다.")
        else:
            day_names = ["월", "화", "수", "목", "금"]
            for subject in subjects:
                print(f"\n코드: {subject['code']}")
                print(f"  과목명: {subject['name']}")
                print(f"  시수: {subject['hours']}")
                print(f"  요일: {subject.get('day_of_week')} ({day_names[subject['day_of_week']] if subject.get('day_of_week') is not None else '미설정'})")
                print(f"  격주: {subject.get('is_biweekly')} ({'격주' if subject.get('is_biweekly') else '매주'})")
                print(f"  주차: {subject.get('week_offset')}")
                print(f"  주강사: {subject.get('main_instructor', 'NULL')}")
                print(f"  보조강사: {subject.get('assistant_instructor', 'NULL')}")
                print(f"  예비강사: {subject.get('reserve_instructor', 'NULL')}")
        
        # NULL 값 확인
        print("\n=== NULL 값 체크 ===")
        cursor.execute("""
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN day_of_week IS NULL THEN 1 ELSE 0 END) as null_day,
                SUM(CASE WHEN is_biweekly IS NULL THEN 1 ELSE 0 END) as null_biweekly,
                SUM(CASE WHEN week_offset IS NULL THEN 1 ELSE 0 END) as null_week_offset
            FROM subjects
        """)
        result = cursor.fetchone()
        print(f"  총 교과목 수: {result['total']}")
        print(f"  day_of_week NULL: {result['null_day']}")
        print(f"  is_biweekly NULL: {result['null_biweekly']}")
        print(f"  week_offset NULL: {result['null_week_offset']}")
        
        if result['null_day'] > 0 or result['null_biweekly'] > 0 or result['null_week_offset'] > 0:
            print("\n⚠️  NULL 값이 존재합니다! update_existing_subjects.py를 실행하세요.")
        else:
            print("\n✅ 모든 필수 값이 설정되어 있습니다.")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_subjects_data()
