# -*- coding: utf-8 -*-
"""
기존 교과목 데이터에 기본값 설정
"""

import pymysql
import sys
import os

# 상위 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_db import DB_CONFIG


def update_existing_subjects():
    """기존 교과목에 기본값 설정"""
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
        
        print("=== 기존 교과목 데이터 업데이트 시작 ===")
        
        # 1. 현재 NULL인 데이터 확인
        cursor.execute("""
            SELECT code, name, day_of_week, is_biweekly, week_offset 
            FROM subjects 
            WHERE day_of_week IS NULL
        """)
        null_subjects = cursor.fetchall()
        
        if not null_subjects:
            print("✓ 모든 교과목에 요일이 설정되어 있습니다.")
            cursor.close()
            connection.close()
            return True
        
        print(f"\n총 {len(null_subjects)}개의 교과목에 기본값을 설정합니다:")
        
        # 2. 기본값 설정 (월요일부터 순차적으로 할당)
        for idx, subject in enumerate(null_subjects):
            day_of_week = idx % 5  # 0=월, 1=화, 2=수, 3=목, 4=금
            is_biweekly = 0  # 기본은 매주
            week_offset = 0  # 기본은 1주차
            
            cursor.execute("""
                UPDATE subjects 
                SET day_of_week = %s, is_biweekly = %s, week_offset = %s
                WHERE code = %s
            """, (day_of_week, is_biweekly, week_offset, subject['code']))
            
            day_names = ["월요일", "화요일", "수요일", "목요일", "금요일"]
            print(f"  {subject['code']} ({subject['name']}): {day_names[day_of_week]}, 매주")
        
        connection.commit()
        
        # 3. 업데이트 결과 확인
        cursor.execute("SELECT code, name, day_of_week, is_biweekly, week_offset FROM subjects")
        all_subjects = cursor.fetchall()
        
        print(f"\n=== 최종 교과목 설정 ===")
        day_names = ["월", "화", "수", "목", "금"]
        for subject in all_subjects:
            day = day_names[subject['day_of_week']] if subject['day_of_week'] is not None else "미설정"
            biweekly = "격주" if subject['is_biweekly'] else "매주"
            week = f"/{subject['week_offset']+1}주차" if subject['is_biweekly'] else ""
            print(f"  {subject['code']} ({subject['name']:<15}): {day}요일, {biweekly}{week}")
        
        print("\n=== 업데이트 완료 ===")
        print("💡 이제 교과목 관리에서 각 과목의 요일을 원하는 대로 수정할 수 있습니다.")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 업데이트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    update_existing_subjects()
