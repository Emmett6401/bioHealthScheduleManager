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
                    day_of_week INT COMMENT '요일: 0=월, 1=화, 2=수, 3=목, 4=금',
                    is_biweekly BOOLEAN DEFAULT FALSE COMMENT '격주 여부',
                    week_offset INT DEFAULT 0 COMMENT '격주인 경우: 0=1주차, 1=2주차',
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
                    start_date DATE,
                    lecture_end_date DATE,
                    project_end_date DATE,
                    internship_end_date DATE,
                    final_end_date DATE,
                    lecture_hours INT NOT NULL DEFAULT 260,
                    project_hours INT NOT NULL DEFAULT 220,
                    internship_hours INT NOT NULL DEFAULT 120,
                    total_days INT,
                    capacity INT NOT NULL,
                    location VARCHAR(200),
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 6. 과정-과목 매핑 테이블 (다대다 관계)
            cursor.execute("""
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
            """)
            
            # 7. 시간표 테이블
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
            
            # 7. 학생 관리 테이블
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    code VARCHAR(10) UNIQUE COMMENT '학생코드 (S-001)',
                    name VARCHAR(50) NOT NULL,
                    birth_date VARCHAR(20) COMMENT '생년월일',
                    gender VARCHAR(10) COMMENT '성별',
                    phone VARCHAR(20) NOT NULL,
                    email VARCHAR(100),
                    address TEXT,
                    interests TEXT COMMENT '관심 분야',
                    education TEXT COMMENT '최종 학교/학년',
                    introduction TEXT COMMENT '자기소개',
                    campus VARCHAR(100) COMMENT '지원 캠퍼스',
                    course_code VARCHAR(10) COMMENT '배정된 과정',
                    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '등록일',
                    notes TEXT COMMENT '비고',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_code) REFERENCES courses(code) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            
            # 8. 프로젝트 관리 테이블
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
    
    # ==================== 면담 관리 메서드 ====================
    
    def add_consultation(self, consultation_data):
        """면담 정보 추가"""
        try:
            query = """
                INSERT INTO consultations (
                    student_id, consultation_date, location, main_topic, 
                    content, consultant_name, next_consultation_date, 
                    consultation_type, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                consultation_data['student_id'],
                consultation_data['consultation_date'],
                consultation_data.get('location', ''),
                consultation_data.get('main_topic', ''),
                consultation_data.get('content', ''),
                consultation_data.get('consultant_name', ''),
                consultation_data.get('next_consultation_date'),
                consultation_data.get('consultation_type', '정기'),
                consultation_data.get('status', '완료')
            )
            cursor = self.execute_query(query, params)
            if cursor:
                return cursor.lastrowid
            return None
        except Exception as e:
            print(f"면담 추가 오류: {str(e)}")
            return None
    
    def update_consultation(self, consultation_id, consultation_data):
        """면담 정보 수정"""
        try:
            query = """
                UPDATE consultations SET
                    consultation_date = %s,
                    location = %s,
                    main_topic = %s,
                    content = %s,
                    consultant_name = %s,
                    next_consultation_date = %s,
                    consultation_type = %s,
                    status = %s
                WHERE id = %s
            """
            params = (
                consultation_data['consultation_date'],
                consultation_data.get('location', ''),
                consultation_data.get('main_topic', ''),
                consultation_data.get('content', ''),
                consultation_data.get('consultant_name', ''),
                consultation_data.get('next_consultation_date'),
                consultation_data.get('consultation_type', '정기'),
                consultation_data.get('status', '완료'),
                consultation_id
            )
            cursor = self.execute_query(query, params)
            return cursor is not None
        except Exception as e:
            print(f"면담 수정 오류: {str(e)}")
            return False
    
    def delete_consultation(self, consultation_id):
        """면담 정보 삭제"""
        try:
            query = "DELETE FROM consultations WHERE id = %s"
            cursor = self.execute_query(query, (consultation_id,))
            return cursor is not None
        except Exception as e:
            print(f"면담 삭제 오류: {str(e)}")
            return False
    
    def get_consultation(self, consultation_id):
        """특정 면담 정보 조회"""
        try:
            query = """
                SELECT c.*, s.name as student_name, s.code as student_code
                FROM consultations c
                LEFT JOIN students s ON c.student_id = s.id
                WHERE c.id = %s
            """
            return self.fetch_one(query, (consultation_id,))
        except Exception as e:
            print(f"면담 조회 오류: {str(e)}")
            return None
    
    def get_consultations_by_student(self, student_id):
        """특정 학생의 모든 면담 조회"""
        try:
            query = """
                SELECT c.*, s.name as student_name, s.code as student_code
                FROM consultations c
                LEFT JOIN students s ON c.student_id = s.id
                WHERE c.student_id = %s
                ORDER BY c.consultation_date DESC
            """
            return self.fetch_all(query, (student_id,))
        except Exception as e:
            print(f"학생 면담 조회 오류: {str(e)}")
            return []
    
    def get_all_consultations(self):
        """모든 면담 조회"""
        try:
            query = """
                SELECT c.*, s.name as student_name, s.code as student_code
                FROM consultations c
                LEFT JOIN students s ON c.student_id = s.id
                ORDER BY c.consultation_date DESC
            """
            return self.fetch_all(query)
        except Exception as e:
            print(f"면담 목록 조회 오류: {str(e)}")
            return []
    
    def get_upcoming_consultations(self):
        """예정된 면담 조회 (다음 면담일이 있는 경우)"""
        try:
            query = """
                SELECT c.*, s.name as student_name, s.code as student_code
                FROM consultations c
                LEFT JOIN students s ON c.student_id = s.id
                WHERE c.next_consultation_date IS NOT NULL 
                AND c.next_consultation_date >= CURDATE()
                ORDER BY c.next_consultation_date ASC
            """
            return self.fetch_all(query)
        except Exception as e:
            print(f"예정 면담 조회 오류: {str(e)}")
            return []
    
    def add_consultation_photo(self, consultation_id, photo_path, description=''):
        """면담 사진 추가"""
        try:
            query = """
                INSERT INTO consultation_photos (consultation_id, photo_path, photo_description)
                VALUES (%s, %s, %s)
            """
            cursor = self.execute_query(query, (consultation_id, photo_path, description))
            if cursor:
                return cursor.lastrowid
            return None
        except Exception as e:
            print(f"면담 사진 추가 오류: {str(e)}")
            return None
    
    def delete_consultation_photo(self, photo_id):
        """면담 사진 삭제"""
        try:
            query = "DELETE FROM consultation_photos WHERE id = %s"
            cursor = self.execute_query(query, (photo_id,))
            return cursor is not None
        except Exception as e:
            print(f"면담 사진 삭제 오류: {str(e)}")
            return False
    
    def get_consultation_photos(self, consultation_id):
        """특정 면담의 모든 사진 조회"""
        try:
            query = """
                SELECT * FROM consultation_photos
                WHERE consultation_id = %s
                ORDER BY uploaded_at DESC
            """
            return self.fetch_all(query, (consultation_id,))
        except Exception as e:
            print(f"면담 사진 조회 오류: {str(e)}")
            return []
    
    def search_consultations(self, keyword='', consultation_type=None, date_from=None, date_to=None):
        """면담 검색"""
        try:
            query = """
                SELECT c.*, s.name as student_name, s.code as student_code
                FROM consultations c
                LEFT JOIN students s ON c.student_id = s.id
                WHERE 1=1
            """
            params = []
            
            if keyword:
                query += """ AND (s.name LIKE %s OR c.main_topic LIKE %s 
                            OR c.content LIKE %s OR c.consultant_name LIKE %s)"""
                keyword_param = f"%{keyword}%"
                params.extend([keyword_param, keyword_param, keyword_param, keyword_param])
            
            if consultation_type:
                query += " AND c.consultation_type = %s"
                params.append(consultation_type)
            
            if date_from:
                query += " AND c.consultation_date >= %s"
                params.append(date_from)
            
            if date_to:
                query += " AND c.consultation_date <= %s"
                params.append(date_to)
            
            query += " ORDER BY c.consultation_date DESC"
            
            return self.fetch_all(query, tuple(params) if params else None)
        except Exception as e:
            print(f"면담 검색 오류: {str(e)}")
            return []
