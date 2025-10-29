#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""course_subjects 테이블 생성 스크립트"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pyqt5_app.database.db_manager import DatabaseManager

def create_course_subjects_table():
    """course_subjects 테이블 생성"""
    db = DatabaseManager()
    
    try:
        if not db.connect():
            print("❌ 데이터베이스 연결 실패")
            return False
        
        print("✅ 데이터베이스 연결 성공")
        
        # course_subjects 테이블 생성
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS course_subjects (
            id INT AUTO_INCREMENT PRIMARY KEY,
            course_code VARCHAR(10) NOT NULL,
            subject_code VARCHAR(10) NOT NULL,
            display_order INT DEFAULT 0 COMMENT '과목 표시 순서',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            UNIQUE KEY unique_course_subject (course_code, subject_code),
            FOREIGN KEY (course_code) REFERENCES courses(code) ON DELETE CASCADE,
            FOREIGN KEY (subject_code) REFERENCES subjects(code) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        
        print("\n🔨 course_subjects 테이블 생성 중...")
        cursor = db.connection.cursor()
        cursor.execute(create_table_sql)
        db.connection.commit()
        
        print("✅ course_subjects 테이블 생성 완료!")
        
        # 테이블 확인
        cursor.execute("SHOW TABLES LIKE 'course_subjects'")
        result = cursor.fetchone()
        
        if result:
            print("\n📊 테이블 구조 확인:")
            cursor.execute("DESCRIBE course_subjects")
            columns = cursor.fetchall()
            
            print("\n컬럼 목록:")
            for col in columns:
                print(f"  - {col['Field']}: {col['Type']}")
            
            return True
        else:
            print("❌ 테이블 생성 실패")
            return False
            
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("📦 course_subjects 테이블 생성 스크립트")
    print("=" * 60)
    
    success = create_course_subjects_table()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 테이블 생성 완료!")
    else:
        print("❌ 테이블 생성 실패")
    print("=" * 60)
    
    sys.exit(0 if success else 1)
