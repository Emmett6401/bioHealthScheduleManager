# -*- coding: utf-8 -*-
"""
교과목 데이터 수정 스크립트
day_of_week를 0~4 범위로 강제 설정
"""

import pymysql
import sys
import os

# 상위 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_db import DB_CONFIG


def fix_subjects_data():
    """교과목 데이터 수정"""
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
        
        print("=== 교과목 데이터 수정 시작 ===\n")
        
        # 1. 모든 교과목 조회
        cursor.execute("SELECT code, name, day_of_week, is_biweekly, week_offset FROM subjects")
        subjects = cursor.fetchall()
        
        if not subjects:
            print("교과목 데이터가 없습니다.")
            return
        
        print(f"총 {len(subjects)}개 교과목 확인 중...\n")
        
        day_names = ["월요일", "화요일", "수요일", "목요일", "금요일"]
        fixed_count = 0
        
        # 2. 각 교과목 검사 및 수정
        for idx, subject in enumerate(subjects):
            code = subject['code']
            name = subject['name']
            day = subject.get('day_of_week')
            biweekly = subject.get('is_biweekly')
            week_offset = subject.get('week_offset')
            
            need_fix = False
            new_day = day
            new_biweekly = biweekly if biweekly is not None else 0
            new_week_offset = week_offset if week_offset is not None else 0
            
            # day_of_week 검사
            if day is None or day < 0 or day > 4:
                new_day = idx % 5  # 0~4 순차 할당
                need_fix = True
                print(f"⚠️  {code} ({name})")
                print(f"    day_of_week: {day} → {new_day} ({day_names[new_day]})")
            
            # is_biweekly 검사
            if biweekly is None:
                need_fix = True
                print(f"⚠️  {code} ({name})")
                print(f"    is_biweekly: NULL → 0 (매주)")
            
            # week_offset 검사
            if week_offset is None:
                need_fix = True
                if not biweekly:  # 이미 위에서 출력 안 했으면
                    print(f"⚠️  {code} ({name})")
                print(f"    week_offset: NULL → 0 (1주차)")
            
            # 수정 실행
            if need_fix:
                cursor.execute("""
                    UPDATE subjects 
                    SET day_of_week = %s, is_biweekly = %s, week_offset = %s
                    WHERE code = %s
                """, (new_day, new_biweekly, new_week_offset, code))
                fixed_count += 1
                print(f"    ✅ 수정 완료\n")
        
        connection.commit()
        
        # 3. 최종 결과 확인
        cursor.execute("SELECT code, name, day_of_week, is_biweekly, week_offset FROM subjects ORDER BY code")
        subjects = cursor.fetchall()
        
        print("\n=== 최종 교과목 설정 ===")
        for subject in subjects:
            day = subject['day_of_week']
            day_str = day_names[day] if day is not None and 0 <= day <= 4 else "오류"
            biweekly = "격주" if subject['is_biweekly'] else "매주"
            week_suffix = f" ({subject['week_offset']+1}주차)" if subject['is_biweekly'] else ""
            
            print(f"{subject['code']} - {subject['name']:<30} : {day_str}, {biweekly}{week_suffix}")
        
        print(f"\n=== 수정 완료: {fixed_count}개 교과목 업데이트 ===")
        
        cursor.close()
        connection.close()
        
        return True
        
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    fix_subjects_data()
