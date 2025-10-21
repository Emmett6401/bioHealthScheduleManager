# -*- coding: utf-8 -*-
"""
시간표 자동 생성 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QMessageBox, QGroupBox,
                             QGridLayout, QDateEdit, QTimeEdit, QTextEdit,
                             QProgressBar)
from PyQt5.QtCore import Qt, QDate, QTime
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from utils.timetable_generator import TimetableGenerator


class TimetableGenerateDialog(QDialog):
    """시간표 자동 생성 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.generator = TimetableGenerator(self.db)
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("시간표 자동 생성")
        self.setGeometry(200, 150, 800, 700)
        
        layout = QVBoxLayout()
        
        # 과정 선택
        form_group = QGroupBox("과정 정보")
        form_layout = QGridLayout()
        
        # 과정 선택
        form_layout.addWidget(QLabel("과정 선택:"), 0, 0)
        self.course_combo = QComboBox()
        self.course_combo.setMinimumWidth(300)
        self.course_combo.currentIndexChanged.connect(self.on_course_selected)
        form_layout.addWidget(self.course_combo, 0, 1, 1, 2)
        
        # 과정 정보 표시
        form_layout.addWidget(QLabel("강의 시수:"), 1, 0)
        self.lecture_hours_label = QLabel("-")
        form_layout.addWidget(self.lecture_hours_label, 1, 1)
        
        form_layout.addWidget(QLabel("프로젝트 시수:"), 1, 2)
        self.project_hours_label = QLabel("-")
        form_layout.addWidget(self.project_hours_label, 1, 3)
        
        form_layout.addWidget(QLabel("인턴쉽 시수:"), 2, 0)
        self.internship_hours_label = QLabel("-")
        form_layout.addWidget(self.internship_hours_label, 2, 1)
        
        form_layout.addWidget(QLabel("총 시수:"), 2, 2)
        self.total_hours_label = QLabel("-")
        self.total_hours_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        form_layout.addWidget(self.total_hours_label, 2, 3)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 시간표 설정
        setting_group = QGroupBox("시간표 설정")
        setting_layout = QGridLayout()
        
        # 시작일
        setting_layout.addWidget(QLabel("수업 시작일:"), 0, 0)
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        setting_layout.addWidget(self.start_date, 0, 1)
        
        # 수업 시작 시간
        setting_layout.addWidget(QLabel("수업 시작 시간:"), 0, 2)
        self.start_time = QTimeEdit()
        self.start_time.setTime(QTime(9, 0))
        self.start_time.setDisplayFormat("HH:mm")
        setting_layout.addWidget(self.start_time, 0, 3)
        
        # 수업 종료 시간
        setting_layout.addWidget(QLabel("수업 종료 시간:"), 1, 0)
        self.end_time = QTimeEdit()
        self.end_time.setTime(QTime(18, 0))
        self.end_time.setDisplayFormat("HH:mm")
        setting_layout.addWidget(self.end_time, 1, 1)
        
        # 하루 수업 시간
        setting_layout.addWidget(QLabel("하루 수업 시간:"), 1, 2)
        hours_label = QLabel("8시간 (점심 1시간 제외)")
        hours_label.setStyleSheet("color: #666;")
        setting_layout.addWidget(hours_label, 1, 3)
        
        setting_group.setLayout(setting_layout)
        layout.addWidget(setting_group)
        
        # 생성 옵션
        option_group = QGroupBox("생성 옵션")
        option_layout = QVBoxLayout()
        
        info_text = QLabel(
            "📌 시간표 생성 규칙:\n"
            "• 공휴일, 토요일, 일요일은 자동으로 제외됩니다\n"
            "• 강의 → 프로젝트 → 인턴쉽 순서로 배치됩니다\n"
            "• 교과목은 등록된 순서대로 배정됩니다\n"
            "• 주강사가 자동으로 배정됩니다"
        )
        info_text.setStyleSheet("""
            background-color: #E3F2FD;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #90CAF9;
        """)
        option_layout.addWidget(info_text)
        
        option_group.setLayout(option_layout)
        layout.addWidget(option_group)
        
        # 진행바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 결과 표시
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMaximumHeight(150)
        self.result_text.setVisible(False)
        layout.addWidget(self.result_text)
        
        # 버튼
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.preview_btn = QPushButton("미리보기")
        self.preview_btn.setStyleSheet("background-color: #9C27B0; color: white; padding: 10px 25px;")
        self.preview_btn.clicked.connect(self.preview_timetable)
        btn_layout.addWidget(self.preview_btn)
        
        self.generate_btn = QPushButton("생성하기")
        self.generate_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 25px;")
        self.generate_btn.clicked.connect(self.generate_timetable)
        btn_layout.addWidget(self.generate_btn)
        
        self.delete_btn = QPushButton("시간표 삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px 25px;")
        self.delete_btn.clicked.connect(self.delete_timetable)
        btn_layout.addWidget(self.delete_btn)
        
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # 과정 목록 로드
        self.load_courses()
        
    def load_courses(self):
        """과정 목록 로드"""
        if not self.db.connect():
            return
        
        try:
            query = "SELECT code, name, lecture_hours, project_hours, internship_hours FROM courses ORDER BY code"
            rows = self.db.fetch_all(query)
            
            self.course_combo.clear()
            self.course_combo.addItem("선택하세요", None)
            
            for row in rows:
                display_text = f"{row['name']} ({row['code']}) - {row['lecture_hours']}h"
                self.course_combo.addItem(display_text, row)
                
        except Exception as e:
            print(f"과정 목록 로드 오류: {str(e)}")
    
    def on_course_selected(self, index):
        """과정 선택 시"""
        course = self.course_combo.currentData()
        
        if course:
            self.lecture_hours_label.setText(f"{course['lecture_hours']} 시간")
            self.project_hours_label.setText(f"{course['project_hours']} 시간")
            self.internship_hours_label.setText(f"{course['internship_hours']} 시간")
            
            total = course['lecture_hours'] + course['project_hours'] + course['internship_hours']
            self.total_hours_label.setText(f"{total} 시간")
        else:
            self.lecture_hours_label.setText("-")
            self.project_hours_label.setText("-")
            self.internship_hours_label.setText("-")
            self.total_hours_label.setText("-")
    
    def preview_timetable(self):
        """시간표 미리보기"""
        course = self.course_combo.currentData()
        
        if not course:
            QMessageBox.warning(self, "경고", "과정을 선택하세요.")
            return
        
        start_date = self.start_date.date().toPyDate()
        
        # 예상 날짜 계산
        holidays = self.generator.get_holidays()
        
        lecture_days = self.generator.calculate_working_days(course['lecture_hours'], 8)
        lecture_dates = self.generator.generate_dates(datetime.combine(start_date, datetime.min.time()), lecture_days, holidays)
        
        project_start = lecture_dates[-1] + timedelta(days=1) if lecture_dates else datetime.combine(start_date, datetime.min.time())
        project_days = self.generator.calculate_working_days(course['project_hours'], 8)
        project_dates = self.generator.generate_dates(project_start, project_days, holidays)
        
        if course['internship_hours'] > 0:
            internship_start = project_dates[-1] + timedelta(days=1) if project_dates else project_start
            internship_days = self.generator.calculate_working_days(course['internship_hours'], 8)
            internship_dates = self.generator.generate_dates(internship_start, internship_days, holidays)
        else:
            internship_dates = []
        
        # 미리보기 텍스트
        preview_text = f"""
📅 시간표 미리보기

과정: {course['name']} ({course['code']})

📚 강의 단계
  • 시작일: {lecture_dates[0].strftime('%Y-%m-%d') if lecture_dates else '-'}
  • 종료일: {lecture_dates[-1].strftime('%Y-%m-%d') if lecture_dates else '-'}
  • 수업일수: {len(lecture_dates)}일
  • 총 시수: {course['lecture_hours']}시간

💼 프로젝트 단계
  • 시작일: {project_dates[0].strftime('%Y-%m-%d') if project_dates else '-'}
  • 종료일: {project_dates[-1].strftime('%Y-%m-%d') if project_dates else '-'}
  • 수업일수: {len(project_dates)}일
  • 총 시수: {course['project_hours']}시간

🏢 인턴쉽 단계
  • 시작일: {internship_dates[0].strftime('%Y-%m-%d') if internship_dates else '없음'}
  • 종료일: {internship_dates[-1].strftime('%Y-%m-%d') if internship_dates else '없음'}
  • 수업일수: {len(internship_dates)}일
  • 총 시수: {course['internship_hours']}시간

📊 전체 요약
  • 전체 기간: {lecture_dates[0].strftime('%Y-%m-%d')} ~ {(internship_dates[-1] if internship_dates else (project_dates[-1] if project_dates else lecture_dates[-1])).strftime('%Y-%m-%d')}
  • 총 수업일수: {len(lecture_dates) + len(project_dates) + len(internship_dates)}일
  • 총 시수: {course['lecture_hours'] + course['project_hours'] + course['internship_hours']}시간
        """
        
        self.result_text.setText(preview_text)
        self.result_text.setVisible(True)
    
    def generate_timetable(self):
        """시간표 생성"""
        course = self.course_combo.currentData()
        
        if not course:
            QMessageBox.warning(self, "경고", "과정을 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"'{course['name']}' 과정의 시간표를 생성하시겠습니까?\n\n"
                                     "기존 시간표가 있다면 삭제됩니다.",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if not self.db.connect():
                QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
                return
            
            # 진행바 표시
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # 무한 진행
            
            # 기존 시간표 삭제
            self.generator.delete_timetable(course['code'])
            
            # 시간표 생성
            start_date = self.start_date.date().toString("yyyy-MM-dd")
            start_time = self.start_time.time().toString("HH:mm")
            end_time = self.end_time.time().toString("HH:mm")
            
            result = self.generator.generate_timetable(
                course['code'],
                start_date,
                start_time,
                end_time
            )
            
            # 진행바 숨기기
            self.progress_bar.setVisible(False)
            
            if result['success']:
                details = result['details']
                result_text = f"""
✅ 시간표 생성 완료!

과정: {course['name']} ({course['code']})
기간: {details['start_date']} ~ {details['end_date']}

📊 생성된 시간표:
  • 강의일수: {details['lecture_days']}일
  • 프로젝트일수: {details['project_days']}일
  • 인턴쉽일수: {details['internship_days']}일
  • 총 수업일수: {details['total_days']}일
  • 총 항목 수: {details['total_entries']}개
                """
                
                self.result_text.setText(result_text)
                self.result_text.setVisible(True)
                
                QMessageBox.information(self, "성공", result['message'])
            else:
                QMessageBox.critical(self, "오류", result['message'])
    
    def delete_timetable(self):
        """시간표 삭제"""
        course = self.course_combo.currentData()
        
        if not course:
            QMessageBox.warning(self, "경고", "과정을 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"'{course['name']}' 과정의 시간표를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if not self.db.connect():
                QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
                return
            
            if self.generator.delete_timetable(course['code']):
                QMessageBox.information(self, "성공", "시간표가 삭제되었습니다.")
                self.result_text.clear()
                self.result_text.setVisible(False)
            else:
                QMessageBox.critical(self, "오류", "시간표 삭제 실패")
    
    def closeEvent(self, event):
        """닫기 이벤트"""
        self.db.disconnect()
        event.accept()
