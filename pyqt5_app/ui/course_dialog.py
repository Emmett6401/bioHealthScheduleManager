# -*- coding: utf-8 -*-
"""
과정 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QGroupBox, QGridLayout,
                             QSpinBox, QTextEdit, QDateEdit, QFrame)
from PyQt5.QtCore import Qt, QDate
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from config_db import CODE_PREFIX


class CourseDialog(QWidget):
    """과정 관리 위젯 (탭용)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """UI 초기화"""
        # 탭으로 사용되므로 setWindowTitle, setGeometry 불필요
        
        layout = QVBoxLayout()
        layout.setSpacing(5)
        layout.setContentsMargins(8, 5, 8, 8)
        
        # 과정 시작일 입력
        date_group = QGroupBox("📅 과정 시작일")
        date_group.setStyleSheet("QGroupBox { font-size: 10px; font-weight: bold; padding-top: 5px; margin-top: 5px; }")
        date_layout = QHBoxLayout()
        date_layout.setSpacing(6)
        date_layout.setContentsMargins(5, 5, 5, 5)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.dateChanged.connect(self.calculate_dates)
        self.start_date.setMinimumWidth(130)
        self.start_date.setMaximumHeight(26)
        self.start_date.setStyleSheet("font-size: 10px;")
        date_layout.addWidget(self.start_date)
        
        info_label = QLabel("ℹ️ 과정 기간 내 법정공휴일이 있다면 등록해주세요.")
        info_label.setStyleSheet("color: #2196F3; font-size: 9px;")
        date_layout.addWidget(info_label)
        date_layout.addStretch()
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # 과정 과목 (총 600시간) - 카드 형식
        hours_group = QGroupBox("📚 과정 과목 (총 600시간)")
        hours_group.setStyleSheet("QGroupBox { font-size: 10px; font-weight: bold; padding-top: 5px; margin-top: 5px; }")
        hours_layout = QHBoxLayout()
        hours_layout.setSpacing(8)
        hours_layout.setContentsMargins(5, 5, 5, 5)
        
        # 강의 시수 카드
        lecture_card = QFrame()
        lecture_card.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        lecture_card_layout = QVBoxLayout()
        lecture_card_layout.setSpacing(2)
        lecture_card_layout.setContentsMargins(3, 3, 3, 3)
        
        lecture_title = QLabel("📘 1단계: 이론")
        lecture_title.setStyleSheet("font-weight: bold; font-size: 10px; color: #1976D2;")
        lecture_card_layout.addWidget(lecture_title)
        
        self.lecture_hours = QSpinBox()
        self.lecture_hours.setRange(0, 9999)
        self.lecture_hours.setValue(260)
        self.lecture_hours.setSuffix(" 시간")
        self.lecture_hours.valueChanged.connect(self.calculate_dates)
        self.lecture_hours.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.lecture_hours.setMaximumHeight(28)
        lecture_card_layout.addWidget(self.lecture_hours)
        
        self.lecture_days_label = QLabel("약 33일")
        self.lecture_days_label.setStyleSheet("color: #1976D2; font-size: 9px;")
        lecture_card_layout.addWidget(self.lecture_days_label)
        
        lecture_card.setLayout(lecture_card_layout)
        hours_layout.addWidget(lecture_card)
        
        # 프로젝트 시수 카드
        project_card = QFrame()
        project_card.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        project_card_layout = QVBoxLayout()
        project_card_layout.setSpacing(2)
        project_card_layout.setContentsMargins(3, 3, 3, 3)
        
        project_title = QLabel("📗 2단계: 프로젝트")
        project_title.setStyleSheet("font-weight: bold; font-size: 10px; color: #388E3C;")
        project_card_layout.addWidget(project_title)
        
        self.project_hours = QSpinBox()
        self.project_hours.setRange(0, 9999)
        self.project_hours.setValue(220)
        self.project_hours.setSuffix(" 시간")
        self.project_hours.valueChanged.connect(self.calculate_dates)
        self.project_hours.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.project_hours.setMaximumHeight(28)
        project_card_layout.addWidget(self.project_hours)
        
        self.project_days_label = QLabel("약 28일")
        self.project_days_label.setStyleSheet("color: #388E3C; font-size: 9px;")
        project_card_layout.addWidget(self.project_days_label)
        
        project_card.setLayout(project_card_layout)
        hours_layout.addWidget(project_card)
        
        # 인턴쉽 시수 카드
        internship_card = QFrame()
        internship_card.setStyleSheet("""
            QFrame {
                background-color: #FFF3E0;
                border-radius: 6px;
                padding: 5px;
            }
        """)
        internship_card_layout = QVBoxLayout()
        internship_card_layout.setSpacing(2)
        internship_card_layout.setContentsMargins(3, 3, 3, 3)
        
        internship_title = QLabel("📙 3단계: 인턴십")
        internship_title.setStyleSheet("font-weight: bold; font-size: 10px; color: #F57C00;")
        internship_card_layout.addWidget(internship_title)
        
        self.internship_hours = QSpinBox()
        self.internship_hours.setRange(0, 9999)
        self.internship_hours.setValue(120)
        self.internship_hours.setSuffix(" 시간")
        self.internship_hours.valueChanged.connect(self.calculate_dates)
        self.internship_hours.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.internship_hours.setMaximumHeight(28)
        internship_card_layout.addWidget(self.internship_hours)
        
        self.internship_days_label = QLabel("약 15일")
        self.internship_days_label.setStyleSheet("color: #F57C00; font-size: 9px;")
        internship_card_layout.addWidget(self.internship_days_label)
        
        internship_card.setLayout(internship_card_layout)
        hours_layout.addWidget(internship_card)
        
        hours_group.setLayout(hours_layout)
        layout.addWidget(hours_group)
        
        # 과정 종료일 - 카드 형식
        result_group = QGroupBox("📅 과정 종료일")
        result_group.setStyleSheet("QGroupBox { font-size: 10px; font-weight: bold; padding-top: 5px; margin-top: 5px; }")
        result_layout = QHBoxLayout()
        result_layout.setSpacing(8)
        result_layout.setContentsMargins(5, 5, 5, 5)
        
        # 이론 종료
        lecture_end_card = QFrame()
        lecture_end_card.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 5px;
                padding: 4px;
            }
        """)
        lecture_end_layout = QVBoxLayout()
        lecture_end_layout.setSpacing(1)
        lecture_end_layout.setContentsMargins(3, 2, 3, 2)
        lecture_end_title = QLabel("이론 종료")
        lecture_end_title.setStyleSheet("font-size: 9px; color: #666;")
        lecture_end_layout.addWidget(lecture_end_title)
        
        self.lecture_end_date = QLineEdit()
        self.lecture_end_date.setReadOnly(True)
        self.lecture_end_date.setStyleSheet("border: none; background: transparent; font-size: 11px; font-weight: bold;")
        self.lecture_end_date.setMaximumHeight(22)
        lecture_end_layout.addWidget(self.lecture_end_date)
        
        lecture_end_card.setLayout(lecture_end_layout)
        result_layout.addWidget(lecture_end_card)
        
        # 프로젝트 종료
        project_end_card = QFrame()
        project_end_card.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 5px;
                padding: 4px;
            }
        """)
        project_end_layout = QVBoxLayout()
        project_end_layout.setSpacing(1)
        project_end_layout.setContentsMargins(3, 2, 3, 2)
        project_end_title = QLabel("프로젝트 종료")
        project_end_title.setStyleSheet("font-size: 9px; color: #666;")
        project_end_layout.addWidget(project_end_title)
        
        self.project_end_date = QLineEdit()
        self.project_end_date.setReadOnly(True)
        self.project_end_date.setStyleSheet("border: none; background: transparent; font-size: 11px; font-weight: bold;")
        self.project_end_date.setMaximumHeight(22)
        project_end_layout.addWidget(self.project_end_date)
        
        project_end_card.setLayout(project_end_layout)
        result_layout.addWidget(project_end_card)
        
        # 인턴십 종료
        internship_end_card = QFrame()
        internship_end_card.setStyleSheet("""
            QFrame {
                background-color: #FFF3E0;
                border-radius: 5px;
                padding: 4px;
            }
        """)
        internship_end_layout = QVBoxLayout()
        internship_end_layout.setSpacing(1)
        internship_end_layout.setContentsMargins(3, 2, 3, 2)
        internship_end_title = QLabel("인턴십 종료 (최종)")
        internship_end_title.setStyleSheet("font-size: 9px; color: #666;")
        internship_end_layout.addWidget(internship_end_title)
        
        self.internship_end_date = QLineEdit()
        self.internship_end_date.setReadOnly(True)
        self.internship_end_date.setStyleSheet("border: none; background: transparent; font-size: 11px; font-weight: bold;")
        self.internship_end_date.setMaximumHeight(22)
        internship_end_layout.addWidget(self.internship_end_date)
        
        internship_end_card.setLayout(internship_end_layout)
        result_layout.addWidget(internship_end_card)
        
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        # 과정 일정 계산 결과 - 압축 버전
        calc_result_group = QGroupBox("📊 교육 일정 계산 결과")
        calc_result_group.setStyleSheet("QGroupBox { font-size: 11px; font-weight: bold; padding-top: 8px; }")
        calc_result_layout = QHBoxLayout()
        calc_result_layout.setSpacing(15)
        
        # 총 기간
        total_period_layout = QVBoxLayout()
        total_period_layout.setSpacing(2)
        total_period_label = QLabel("총 기간")
        total_period_label.setStyleSheet("font-size: 10px; color: #666;")
        total_period_layout.addWidget(total_period_label)
        
        self.total_days_label = QLabel("113일")
        self.total_days_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2196F3;")
        total_period_layout.addWidget(self.total_days_label)
        calc_result_layout.addLayout(total_period_layout)
        
        calc_result_layout.addStretch()
        
        # 근무일 (실제 교육일)
        workdays_layout = QVBoxLayout()
        workdays_layout.setSpacing(2)
        workdays_label = QLabel("근무일 (600시간)")
        workdays_label.setStyleSheet("font-size: 10px; color: #666;")
        workdays_layout.addWidget(workdays_label)
        
        self.workdays_label = QLabel("76일 (600시간)")
        self.workdays_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #4CAF50;")
        workdays_layout.addWidget(self.workdays_label)
        calc_result_layout.addLayout(workdays_layout)
        
        calc_result_layout.addStretch()
        
        # 제외일 (주말+공휴일)
        excluded_layout = QVBoxLayout()
        excluded_layout.setSpacing(2)
        excluded_label = QLabel("제외일 (주말+공휴일)")
        excluded_label.setStyleSheet("font-size: 10px; color: #666;")
        excluded_layout.addWidget(excluded_label)
        
        self.excluded_days_label = QLabel("5일")
        self.excluded_days_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #F44336;")
        excluded_layout.addWidget(self.excluded_days_label)
        calc_result_layout.addLayout(excluded_layout)
        
        calc_result_group.setLayout(calc_result_layout)
        layout.addWidget(calc_result_group)
        
        # 기본 정보 입력 폼
        form_group = QGroupBox("📋 기본 정보")
        form_group.setStyleSheet("QGroupBox { font-size: 11px; font-weight: bold; padding-top: 8px; }")
        form_layout = QGridLayout()
        form_layout.setSpacing(6)
        form_layout.setVerticalSpacing(8)
        
        # 코드
        code_label = QLabel("코드:")
        code_label.setStyleSheet("font-size: 11px;")
        form_layout.addWidget(code_label, 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("C-001 (자동 생성)")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(150)
        self.code_input.setMaximumHeight(28)
        form_layout.addWidget(self.code_input, 0, 1)
        
        # 반명칭
        name_label = QLabel("반명칭:")
        name_label.setStyleSheet("font-size: 11px;")
        form_layout.addWidget(name_label, 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 1반")
        self.name_input.setMaximumHeight(28)
        form_layout.addWidget(self.name_input, 0, 3)
        
        # 인원수
        capacity_label = QLabel("인원수:")
        capacity_label.setStyleSheet("font-size: 11px;")
        form_layout.addWidget(capacity_label, 1, 0)
        self.capacity = QSpinBox()
        self.capacity.setRange(1, 999)
        self.capacity.setValue(30)
        self.capacity.setSuffix(" 명")
        self.capacity.setMaximumHeight(28)
        form_layout.addWidget(self.capacity, 1, 1)
        
        # 강의장소
        location_label = QLabel("강의장소:")
        location_label.setStyleSheet("font-size: 11px;")
        form_layout.addWidget(location_label, 1, 2)
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("예: 본관 101호")
        self.location_input.setMaximumHeight(28)
        form_layout.addWidget(self.location_input, 1, 3)
        
        # 특이사항
        notes_label = QLabel("특이사항:")
        notes_label.setStyleSheet("font-size: 11px;")
        form_layout.addWidget(notes_label, 2, 0)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("과정 관련 특이사항을 입력하세요")
        self.notes_input.setMaximumHeight(50)
        form_layout.addWidget(self.notes_input, 2, 1, 1, 3)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 최종 종료일은 인턴쉽 종료일과 동일
        self.final_end_date = QLineEdit()
        self.final_end_date.setReadOnly(True)
        self.final_end_date.hide()  # 숨김 (인턴쉽 종료일과 동일)
        
        # 버튼 그룹
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 6px 16px; font-size: 11px;")
        self.add_btn.setMaximumHeight(32)
        self.add_btn.clicked.connect(self.add_course)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 6px 16px; font-size: 11px;")
        self.update_btn.setMaximumHeight(32)
        self.update_btn.clicked.connect(self.update_course)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 6px 16px; font-size: 11px;")
        self.delete_btn.setMaximumHeight(32)
        self.delete_btn.clicked.connect(self.delete_course)
        btn_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.setStyleSheet("padding: 6px 16px; font-size: 11px;")
        self.clear_btn.setMaximumHeight(32)
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            "코드", "반명칭", "시작일", "강의종료", "프로젝트종료", 
            "인턴쉽종료", "총기간", "인원", "장소", "비고"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼
        # 하단 버튼 (탭으로 사용되므로 닫기 버튼 불필요)
        
        self.setLayout(layout)
    
    def calculate_dates(self):
        """과정 일정 자동 계산"""
        start_date = self.start_date.date().toPyDate()
        
        lecture_hours = self.lecture_hours.value()
        project_hours = self.project_hours.value()
        internship_hours = self.internship_hours.value()
        
        # 하루 8시간 기준 일수 계산
        lecture_days = (lecture_hours + 7) // 8  # 올림
        project_days = (project_hours + 7) // 8
        internship_days = (internship_hours + 7) // 8
        
        # 일수 라벨 업데이트
        self.lecture_days_label.setText(f"({lecture_days}일)")
        self.project_days_label.setText(f"({project_days}일)")
        self.internship_days_label.setText(f"({internship_days}일)")
        
        # 공휴일 조회
        holidays = self.get_holidays()
        
        # 강의 종료일 계산
        lecture_end = self.calculate_end_date(start_date, lecture_days, holidays)
        self.lecture_end_date.setText(lecture_end.strftime("%Y-%m-%d"))
        
        # 프로젝트 종료일 계산 (강의 종료일 다음날부터 시작)
        project_start = lecture_end + timedelta(days=1)
        project_start = self.get_next_workday(project_start, holidays)
        project_end = self.calculate_end_date(project_start, project_days, holidays)
        self.project_end_date.setText(project_end.strftime("%Y-%m-%d"))
        
        # 인턴쉽 종료일 계산 (프로젝트 종료일 다음날부터 시작)
        internship_start = project_end + timedelta(days=1)
        internship_start = self.get_next_workday(internship_start, holidays)
        internship_end = self.calculate_end_date(internship_start, internship_days, holidays)
        self.internship_end_date.setText(internship_end.strftime("%Y-%m-%d"))
        
        # 최종 종료일 (인턴쉽 종료일과 동일)
        self.final_end_date.setText(internship_end.strftime("%Y-%m-%d"))
        
        # 총 기간 계산 (시작일부터 최종 종료일까지)
        total_calendar_days = (internship_end - start_date).days + 1
        total_work_days = lecture_days + project_days + internship_days
        excluded_days = total_calendar_days - total_work_days
        
        # 라벨 업데이트
        self.total_days_label.setText(f"{total_calendar_days}일")
        self.workdays_label.setText(f"{total_work_days}일 (600시간)")
        self.excluded_days_label.setText(f"{excluded_days}일")
    
    def get_holidays(self):
        """공휴일 목록 조회"""
        holidays = set()
        try:
            if self.db.connect():
                query = "SELECT holiday_date FROM holidays"
                rows = self.db.fetch_all(query)
                for row in rows:
                    holidays.add(row['holiday_date'])
        except Exception as e:
            print(f"공휴일 조회 오류: {str(e)}")
        return holidays
    
    def is_workday(self, date, holidays):
        """평일 여부 확인 (토요일, 일요일, 공휴일 제외)"""
        # 토요일(5), 일요일(6) 제외
        if date.weekday() >= 5:
            return False
        # 공휴일 제외
        if date in holidays:
            return False
        return True
    
    def get_next_workday(self, date, holidays):
        """다음 평일 찾기"""
        while not self.is_workday(date, holidays):
            date += timedelta(days=1)
        return date
    
    def calculate_end_date(self, start_date, work_days, holidays):
        """종료일 계산 (평일 기준)"""
        current_date = start_date
        days_counted = 0
        
        while days_counted < work_days:
            if self.is_workday(current_date, holidays):
                days_counted += 1
                if days_counted >= work_days:
                    break
            current_date += timedelta(days=1)
        
        return current_date
        
    def load_data(self):
        """데이터 로드"""
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        try:
            query = "SELECT * FROM courses ORDER BY code"
            rows = self.db.fetch_all(query)
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                self.table.setItem(row_position, 0, QTableWidgetItem(row['code'] or ''))
                self.table.setItem(row_position, 1, QTableWidgetItem(row['name'] or ''))
                
                # 시작일
                start_date = row['start_date'].strftime("%Y-%m-%d") if row.get('start_date') else ''
                self.table.setItem(row_position, 2, QTableWidgetItem(start_date))
                
                # 강의 종료일
                lecture_end = row['lecture_end_date'].strftime("%m-%d") if row.get('lecture_end_date') else ''
                self.table.setItem(row_position, 3, QTableWidgetItem(lecture_end))
                
                # 프로젝트 종료일
                project_end = row['project_end_date'].strftime("%m-%d") if row.get('project_end_date') else ''
                self.table.setItem(row_position, 4, QTableWidgetItem(project_end))
                
                # 인턴쉽 종료일
                internship_end = row['internship_end_date'].strftime("%m-%d") if row.get('internship_end_date') else ''
                self.table.setItem(row_position, 5, QTableWidgetItem(internship_end))
                
                # 총 기간
                total_days = f"{row['total_days']}일" if row.get('total_days') else ''
                self.table.setItem(row_position, 6, QTableWidgetItem(total_days))
                
                # 인원
                self.table.setItem(row_position, 7, QTableWidgetItem(str(row['capacity'])))
                
                # 장소
                self.table.setItem(row_position, 8, QTableWidgetItem(row['location'] or ''))
                
                # 비고
                notes = row['notes'] or ''
                self.table.setItem(row_position, 9, QTableWidgetItem(notes[:20] + '...' if len(notes) > 20 else notes))
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 로드 실패: {str(e)}")
        
    def on_row_selected(self, row, column):
        """행 선택 시"""
        code = self.table.item(row, 0).text()
        
        # DB에서 전체 데이터 조회
        query = "SELECT * FROM courses WHERE code = %s"
        result = self.db.fetch_one(query, (code,))
        
        if result:
            self.code_input.setText(result['code'])
            self.name_input.setText(result['name'])
            
            # 시작일 설정
            if result.get('start_date'):
                q_date = QDate(result['start_date'].year, result['start_date'].month, result['start_date'].day)
                self.start_date.setDate(q_date)
            
            self.lecture_hours.setValue(result['lecture_hours'])
            self.project_hours.setValue(result['project_hours'])
            self.internship_hours.setValue(result['internship_hours'])
            self.capacity.setValue(result['capacity'])
            self.location_input.setText(result['location'] or '')
            self.notes_input.setText(result['notes'] or '')
            
            # 계산된 날짜들 표시
            if result.get('lecture_end_date'):
                self.lecture_end_date.setText(result['lecture_end_date'].strftime("%Y-%m-%d"))
            if result.get('project_end_date'):
                self.project_end_date.setText(result['project_end_date'].strftime("%Y-%m-%d"))
            if result.get('internship_end_date'):
                self.internship_end_date.setText(result['internship_end_date'].strftime("%Y-%m-%d"))
            if result.get('final_end_date'):
                self.final_end_date.setText(result['final_end_date'].strftime("%Y-%m-%d"))
        
    def add_course(self):
        """과정 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "반명칭을 입력하세요.")
            return
        
        # 날짜 정보
        start_date = self.start_date.date().toPyDate()
        lecture_end = self.lecture_end_date.text()
        project_end = self.project_end_date.text()
        internship_end = self.internship_end_date.text()
        final_end = self.final_end_date.text()
        
        if not lecture_end or not project_end or not internship_end:
            QMessageBox.warning(self, "경고", "일정 자동계산 버튼을 클릭하여 일정을 먼저 계산하세요.")
            return
        
        lecture_hrs = self.lecture_hours.value()
        project_hrs = self.project_hours.value()
        internship_hrs = self.internship_hours.value()
        cap = self.capacity.value()
        location = self.location_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        # 총 일수 계산
        final_date = datetime.strptime(final_end, "%Y-%m-%d").date()
        total_days = (final_date - start_date).days + 1
        
        try:
            code = self.db.get_next_code('courses', CODE_PREFIX['course'])
            
            query = """
                INSERT INTO courses (
                    code, name, start_date, lecture_end_date, project_end_date, 
                    internship_end_date, final_end_date, lecture_hours, project_hours, 
                    internship_hours, total_days, capacity, location, notes
                ) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (
                code, name, start_date, lecture_end, project_end, 
                internship_end, final_end, lecture_hrs, project_hrs, 
                internship_hrs, total_days, cap, location, notes
            ))
            
            QMessageBox.information(self, "성공", f"과정 {code}가 추가되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")
    
    def update_course(self):
        """과정 수정"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "경고", "코드와 반명칭을 입력하세요.")
            return
        
        # 날짜 정보
        start_date = self.start_date.date().toPyDate()
        lecture_end = self.lecture_end_date.text()
        project_end = self.project_end_date.text()
        internship_end = self.internship_end_date.text()
        final_end = self.final_end_date.text()
        
        if not lecture_end or not project_end or not internship_end:
            QMessageBox.warning(self, "경고", "일정 자동계산 버튼을 클릭하여 일정을 먼저 계산하세요.")
            return
        
        lecture_hrs = self.lecture_hours.value()
        project_hrs = self.project_hours.value()
        internship_hrs = self.internship_hours.value()
        cap = self.capacity.value()
        location = self.location_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        # 총 일수 계산
        final_date = datetime.strptime(final_end, "%Y-%m-%d").date()
        total_days = (final_date - start_date).days + 1
        
        try:
            query = """
                UPDATE courses 
                SET name = %s, start_date = %s, lecture_end_date = %s, project_end_date = %s,
                    internship_end_date = %s, final_end_date = %s, lecture_hours = %s, 
                    project_hours = %s, internship_hours = %s, total_days = %s,
                    capacity = %s, location = %s, notes = %s 
                WHERE code = %s
            """
            self.db.execute_query(query, (
                name, start_date, lecture_end, project_end, internship_end, final_end,
                lecture_hrs, project_hrs, internship_hrs, total_days, cap, location, notes, code
            ))
            
            QMessageBox.information(self, "성공", "과정이 수정되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")
    
    def delete_course(self):
        """과정 삭제"""
        code = self.code_input.text().strip()
        
        if not code:
            QMessageBox.warning(self, "경고", "삭제할 과정을 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"과정 {code}를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM courses WHERE code = %s"
                self.db.execute_query(query, (code,))
                
                QMessageBox.information(self, "성공", "과정이 삭제되었습니다.")
                self.clear_form()
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def clear_form(self):
        """폼 초기화"""
        self.code_input.clear()
        self.name_input.clear()
        self.start_date.setDate(QDate.currentDate())
        self.lecture_hours.setValue(260)
        self.project_hours.setValue(220)
        self.internship_hours.setValue(120)
        self.capacity.setValue(30)
        self.location_input.clear()
        self.notes_input.clear()
        self.lecture_end_date.clear()
        self.project_end_date.clear()
        self.internship_end_date.clear()
        self.final_end_date.clear()
    

