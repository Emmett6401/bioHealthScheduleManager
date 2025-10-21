# -*- coding: utf-8 -*-
"""
데이터베이스 매니저
"""

import pymysql
import sys
import os
from datetime import datetime

# 상위 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config_db import DB_CONFIG


class DatabaseManager:
    """MySQL 데이터베이스 연결 및 관리"""
    
    def __init__(self):
        self.connection = None
        
    def connect(self):
        """데이터베이스 연결"""
        try:
            self.connection = pymysql.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                passwd=DB_CONFIG['passwd'],
                db=DB_CONFIG['db'],
                charset=DB_CONFIG['charset'],
                port=DB_CONFIG['port'],
                cursorclass=pymysql.cursors.DictCursor
            )
            return True
        except Exception as e:
            print(f"데이터베이스 연결 오류: {str(e)}")
            return False
    
    def disconnect(self):
        """데이터베이스 연결 종료"""
        if self.connection:
            self.connection.close()
            
    def create_tables(self):
        """필요한 테이블 생성"""
        try:
            cursor = self.connection.cursor()
            
            # 1. 강사 코드 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS instructor_codes (
                    code VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    type ENUM('1', '2', '3') NOT NULL COMMENT '1:주강사, 2:보조강사, 3:멘토',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 2. 강사 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS instructors (
                    code VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(50) NOT NULL,
                    phone VARCHAR(20),
                    major VARCHAR(100),
                    instructor_type VARCHAR(10),
                    email VARCHAR(100),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (instructor_type) REFERENCES instructor_codes(code)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 3. 교과목 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    code VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    hours INT NOT NULL,
                    main_instructor VARCHAR(10),
                    assistant_instructor VARCHAR(10),
                    reserve_instructor VARCHAR(10),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (main_instructor) REFERENCES instructors(code),
                    FOREIGN KEY (assistant_instructor) REFERENCES instructors(code),
                    FOREIGN KEY (reserve_instructor) REFERENCES instructors(code)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 4. 공휴일 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS holidays (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    holiday_date DATE NOT NULL UNIQUE,
                    name VARCHAR(100) NOT NULL,
                    is_legal BOOLEAN DEFAULT FALSE COMMENT '법정공휴일 여부',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 5. 과정 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS courses (
                    code VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    lecture_hours INT NOT NULL,
                    project_hours INT NOT NULL,
                    internship_hours INT NOT NULL,
                    capacity INT NOT NULL,
                    location VARCHAR(200),
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 6. 시간표 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS timetables (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    course_code VARCHAR(10) NOT NULL,
                    subject_code VARCHAR(10),
                    class_date DATE NOT NULL,
                    start_time TIME NOT NULL,
                    end_time TIME NOT NULL,
                    instructor_code VARCHAR(10),
                    type ENUM('lecture', 'project', 'internship') NOT NULL,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_code) REFERENCES courses(code),
                    FOREIGN KEY (subject_code) REFERENCES subjects(code),
                    FOREIGN KEY (instructor_code) REFERENCES instructors(code)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 7. 프로젝트 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    code VARCHAR(10) PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    member1_name VARCHAR(50),
                    member1_phone VARCHAR(20),
                    member2_name VARCHAR(50),
                    member2_phone VARCHAR(20),
                    member3_name VARCHAR(50),
                    member3_phone VARCHAR(20),
                    member4_name VARCHAR(50),
                    member4_phone VARCHAR(20),
                    member5_name VARCHAR(50),
                    member5_phone VARCHAR(20),
                    course_code VARCHAR(10),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_code) REFERENCES courses(code)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            self.connection.commit()
            print("테이블이 성공적으로 생성되었습니다.")
            return True
            
        except Exception as e:
            print(f"테이블 생성 오류: {str(e)}")
            self.connection.rollback()
            return False
    
    def execute_query(self, query, params=None):
        """쿼리 실행"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Exception as e:
            print(f"쿼리 실행 오류: {str(e)}")
            self.connection.rollback()
            return None
    
    def fetch_all(self, query, params=None):
        """모든 결과 조회"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"조회 오류: {str(e)}")
            return []
    
    def fetch_one(self, query, params=None):
        """단일 결과 조회"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchone()
        except Exception as e:
            print(f"조회 오류: {str(e)}")
            return None
    
    def get_next_code(self, table_name, prefix):
        """다음 코드 번호 생성"""
        try:
            query = f"SELECT code FROM {table_name} WHERE code LIKE %s ORDER BY code DESC LIMIT 1"
            result = self.fetch_one(query, (f"{prefix}%",))
            
            if result:
                last_code = result['code']
                # 숫자 부분 추출
                num = int(last_code.replace(prefix, ''))
                next_num = num + 1
            else:
                next_num = 1
            
            # 3자리 숫자로 포맷팅
            return f"{prefix}{next_num:03d}"
        except Exception as e:
            print(f"코드 생성 오류: {str(e)}")
            return f"{prefix}001"
