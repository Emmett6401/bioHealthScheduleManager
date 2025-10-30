#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
강사 타입 ENUM 컬럼 수정 스크립트
12가지 타입을 지원하도록 데이터베이스 업데이트
"""

import sys
import os

# pyqt5_app 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyqt5_app'))

from database.db_manager import DatabaseManager

def fix_instructor_type_enum():
    """강사 타입 ENUM 수정"""
    
    print("=" * 60)
    print("강사 타입 ENUM 컬럼 수정 시작")
    print("=" * 60)
    
    db = DatabaseManager()
    
    try:
        # ENUM 타입 수정 쿼리
        alter_query = """
        ALTER TABLE instructors 
        MODIFY COLUMN type ENUM(
            '1. 주강사',
            '2. 보조강사', 
            '3. 멘토',
            '4. 행정지원',
            '5. 외부강사',
            '6. 인턴',
            '7. 방문강사',
            '8. 온라인강사',
            '9. 특별강사',
            '10. 객원강사',
            '11. 수석강사',
            '12. 조교'
        ) DEFAULT '1. 주강사'
        """
        
        print("\n📝 ENUM 타입 수정 중...")
        db.execute_query(alter_query)
        print("✅ ENUM 타입 수정 완료!")
        
        # 테이블 구조 확인
        print("\n📊 현재 테이블 구조:")
        result = db.execute_query("SHOW CREATE TABLE instructors", fetch=True)
        if result:
            print(result[0][1])
        
        print("\n" + "=" * 60)
        print("✅ 모든 작업이 완료되었습니다!")
        print("=" * 60)
        print("\n이제 강사 코드 관리에서 12가지 타입을 모두 사용할 수 있습니다:")
        print("  1. 주강사")
        print("  2. 보조강사")
        print("  3. 멘토")
        print("  4. 행정지원")
        print("  5. 외부강사")
        print("  6. 인턴")
        print("  7. 방문강사")
        print("  8. 온라인강사")
        print("  9. 특별강사")
        print("  10. 객원강사")
        print("  11. 수석강사")
        print("  12. 조교")
        
    except Exception as e:
        print(f"\n❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    success = fix_instructor_type_enum()
    sys.exit(0 if success else 1)
