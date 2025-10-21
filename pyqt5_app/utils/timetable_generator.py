# -*- coding: utf-8 -*-
"""
시간표 자동 생성 유틸리티
"""

from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager


class TimetableGenerator:
    """시간표 자동 생성기"""
    
    def __init__(self, db_manager):
        self.db = db_manager
        
    def get_holidays(self):
        """공휴일 목록 조회"""
        try:
            query = "SELECT holiday_date FROM holidays"
            rows = self.db.fetch_all(query)
            return [row['holiday_date'] for row in rows]
        except Exception as e:
            print(f"공휴일 조회 오류: {str(e)}")
            return []
    
    def is_working_day(self, date, holidays):
        """근무일 여부 확인 (월~금, 공휴일 제외)"""
        # 토요일(5) 또는 일요일(6) 체크
        if date.weekday() >= 5:
            return False
        
        # 공휴일 체크
        if date.date() in holidays:
            return False
        
        return True
    
    def calculate_working_days(self, start_date, total_hours, hours_per_day=8):
        """필요한 근무일 수 계산"""
        days_needed = (total_hours + hours_per_day - 1) // hours_per_day  # 올림
        return days_needed
    
    def generate_dates(self, start_date, days_needed, holidays):
        """근무일만 포함한 날짜 리스트 생성"""
        dates = []
        current_date = start_date
        
        while len(dates) < days_needed:
            if self.is_working_day(current_date, holidays):
                dates.append(current_date)
            current_date += timedelta(days=1)
        
        return dates
    
    def generate_timetable(self, course_code, start_date, start_time="09:00", end_time="18:00"):
        """
        시간표 자동 생성
        
        Args:
            course_code: 과정 코드
            start_date: 시작일 (datetime.date)
            start_time: 시작 시간 (HH:MM)
            end_time: 종료 시간 (HH:MM)
        
        Returns:
            dict: 생성된 시간표 정보
        """
        try:
            # 1. 과정 정보 조회
            course_query = "SELECT * FROM courses WHERE code = %s"
            course = self.db.fetch_one(course_query, (course_code,))
            
            if not course:
                return {"success": False, "message": "과정을 찾을 수 없습니다."}
            
            lecture_hours = course['lecture_hours']
            project_hours = course['project_hours']
            internship_hours = course['internship_hours']
            
            # 2. 공휴일 목록 조회
            holidays = self.get_holidays()
            
            # 3. 하루 수업 시간 계산 (예: 09:00-18:00 = 8시간, 점심 1시간 제외)
            hours_per_day = 8
            
            # 4. 각 단계별 날짜 생성
            if isinstance(start_date, str):
                start_date = datetime.strptime(start_date, "%Y-%m-%d")
            
            # 강의 단계
            lecture_days = self.calculate_working_days(lecture_hours, hours_per_day)
            lecture_dates = self.generate_dates(start_date, lecture_days, holidays)
            
            # 프로젝트 단계 (강의 다음)
            project_start = lecture_dates[-1] + timedelta(days=1) if lecture_dates else start_date
            project_days = self.calculate_working_days(project_hours, hours_per_day)
            project_dates = self.generate_dates(project_start, project_days, holidays)
            
            # 인턴쉽 단계 (프로젝트 다음)
            if internship_hours > 0:
                internship_start = project_dates[-1] + timedelta(days=1) if project_dates else project_start
                internship_days = self.calculate_working_days(internship_hours, hours_per_day)
                internship_dates = self.generate_dates(internship_start, internship_days, holidays)
            else:
                internship_dates = []
            
            # 5. 교과목 목록 조회
            subjects_query = "SELECT * FROM subjects ORDER BY code"
            subjects = self.db.fetch_all(subjects_query)
            
            # 6. 시간표 데이터 생성
            timetable_entries = []
            subject_idx = 0
            
            # 강의 시간표 생성
            for date in lecture_dates:
                if subject_idx < len(subjects):
                    subject = subjects[subject_idx % len(subjects)]
                    
                    entry = {
                        'course_code': course_code,
                        'subject_code': subject['code'],
                        'class_date': date.strftime("%Y-%m-%d"),
                        'start_time': start_time,
                        'end_time': end_time,
                        'instructor_code': subject['main_instructor'],
                        'type': 'lecture',
                        'notes': f"{subject['name']} 수업"
                    }
                    timetable_entries.append(entry)
                    subject_idx += 1
            
            # 프로젝트 시간표 생성
            for date in project_dates:
                entry = {
                    'course_code': course_code,
                    'subject_code': None,
                    'class_date': date.strftime("%Y-%m-%d"),
                    'start_time': start_time,
                    'end_time': end_time,
                    'instructor_code': None,
                    'type': 'project',
                    'notes': '프로젝트 실습'
                }
                timetable_entries.append(entry)
            
            # 인턴쉽 시간표 생성
            for date in internship_dates:
                entry = {
                    'course_code': course_code,
                    'subject_code': None,
                    'class_date': date.strftime("%Y-%m-%d"),
                    'start_time': start_time,
                    'end_time': end_time,
                    'instructor_code': None,
                    'type': 'internship',
                    'notes': '인턴쉽'
                }
                timetable_entries.append(entry)
            
            # 7. 데이터베이스에 저장
            insert_query = """
                INSERT INTO timetables 
                (course_code, subject_code, class_date, start_time, end_time, instructor_code, type, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            inserted_count = 0
            for entry in timetable_entries:
                if self.db.execute_query(insert_query, (
                    entry['course_code'],
                    entry['subject_code'],
                    entry['class_date'],
                    entry['start_time'],
                    entry['end_time'],
                    entry['instructor_code'],
                    entry['type'],
                    entry['notes']
                )):
                    inserted_count += 1
            
            # 8. 결과 반환
            end_date = internship_dates[-1] if internship_dates else (project_dates[-1] if project_dates else lecture_dates[-1])
            
            return {
                "success": True,
                "message": f"{inserted_count}개의 시간표가 생성되었습니다.",
                "details": {
                    "course_code": course_code,
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d"),
                    "total_days": len(lecture_dates) + len(project_dates) + len(internship_dates),
                    "lecture_days": len(lecture_dates),
                    "project_days": len(project_dates),
                    "internship_days": len(internship_dates),
                    "total_entries": inserted_count
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"시간표 생성 오류: {str(e)}"
            }
    
    def delete_timetable(self, course_code):
        """특정 과정의 시간표 삭제"""
        try:
            query = "DELETE FROM timetables WHERE course_code = %s"
            self.db.execute_query(query, (course_code,))
            return True
        except Exception as e:
            print(f"시간표 삭제 오류: {str(e)}")
            return False
    
    def get_timetable_summary(self, course_code):
        """시간표 요약 정보 조회"""
        try:
            query = """
                SELECT 
                    type,
                    COUNT(*) as count,
                    MIN(class_date) as start_date,
                    MAX(class_date) as end_date
                FROM timetables
                WHERE course_code = %s
                GROUP BY type
                ORDER BY 
                    CASE type
                        WHEN 'lecture' THEN 1
                        WHEN 'project' THEN 2
                        WHEN 'internship' THEN 3
                    END
            """
            return self.db.fetch_all(query, (course_code,))
        except Exception as e:
            print(f"요약 정보 조회 오류: {str(e)}")
            return []
