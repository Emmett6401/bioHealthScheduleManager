# -*- coding: utf-8 -*-
"""
과정 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QGroupBox, QGridLayout,
                             QSpinBox, QTextEdit, QDateEdit, QFrame, QScrollArea, QCheckBox)
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
        
        # 전체 위젯에 고딕 폰트 적용
        from PyQt5.QtGui import QFont
        gothic_font = QFont("맑은 고딕", 10)  # 기본 폰트 크기 10
        self.setFont(gothic_font)
        
        # 메인 레이아웃
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 스크롤 영역 생성
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        # 스크롤 가능한 컨텐츠 위젯
        scroll_content = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 10, 15, 10)
        
        # 과정 시작일 입력
        date_group = QGroupBox("📅 과정 시작일")
        date_group.setStyleSheet("QGroupBox { font-size: 12px; font-weight: bold; padding-top: 10px; margin-top: 8px; }")
        date_layout = QHBoxLayout()
        date_layout.setSpacing(10)
        date_layout.setContentsMargins(10, 8, 10, 8)
        
        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setDisplayFormat("yyyy-MM-dd")
        self.start_date.dateChanged.connect(self.calculate_dates)
        self.start_date.setMinimumWidth(160)
        self.start_date.setMinimumHeight(30)
        self.start_date.setStyleSheet("font-size: 12px;")
        date_layout.addWidget(self.start_date)
        
        info_label = QLabel("ℹ️ 과정 기간 내 법정공휴일이 있다면 등록해주세요.")
        info_label.setStyleSheet("color: #2196F3; font-size: 12px;")
        date_layout.addWidget(info_label)
        date_layout.addStretch()
        
        date_group.setLayout(date_layout)
        layout.addWidget(date_group)
        
        # 과정 개요 (총 600시간) - 카드 형식
        hours_group = QGroupBox("📚 과정 개요 (총 600시간)")
        hours_group.setStyleSheet("QGroupBox { font-size: 11pt; font-weight: bold; padding-top: 10px; margin-top: 8px; }")
        hours_layout = QHBoxLayout()
        hours_layout.setSpacing(12)
        hours_layout.setContentsMargins(10, 8, 10, 8)
        
        # 강의 시수 카드
        lecture_card = QFrame()
        lecture_card.setStyleSheet("""
            QFrame {
                background-color: #E3F2FD;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        lecture_card_layout = QVBoxLayout()
        lecture_card_layout.setSpacing(3)
        lecture_card_layout.setContentsMargins(6, 6, 6, 6)
        
        lecture_title = QLabel("📘 1단계: 이론")
        lecture_title.setStyleSheet("font-weight: bold; font-size: 11pt; color: #1976D2;")
        lecture_card_layout.addWidget(lecture_title)
        
        self.lecture_hours = QSpinBox()
        self.lecture_hours.setRange(0, 9999)
        self.lecture_hours.setValue(260)
        self.lecture_hours.setSuffix(" 시간")
        self.lecture_hours.valueChanged.connect(self.calculate_dates)
        self.lecture_hours.setStyleSheet("font-size: 11pt; font-weight: bold;")
        self.lecture_hours.setMinimumHeight(32)
        lecture_card_layout.addWidget(self.lecture_hours)
        
        self.lecture_days_label = QLabel("약 33일")
        self.lecture_days_label.setStyleSheet("color: #1976D2; font-size: 11pt; font-weight: bold;")
        lecture_card_layout.addWidget(self.lecture_days_label)
        
        lecture_card.setLayout(lecture_card_layout)
        hours_layout.addWidget(lecture_card)
        
        # 프로젝트 시수 카드
        project_card = QFrame()
        project_card.setStyleSheet("""
            QFrame {
                background-color: #E8F5E9;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        project_card_layout = QVBoxLayout()
        project_card_layout.setSpacing(3)
        project_card_layout.setContentsMargins(6, 6, 6, 6)
        
        project_title = QLabel("📗 2단계: 프로젝트")
        project_title.setStyleSheet("font-weight: bold; font-size: 11pt; color: #388E3C;")
        project_card_layout.addWidget(project_title)
        
        self.project_hours = QSpinBox()
        self.project_hours.setRange(0, 9999)
        self.project_hours.setValue(220)
        self.project_hours.setSuffix(" 시간")
        self.project_hours.valueChanged.connect(self.calculate_dates)
        self.project_hours.setStyleSheet("font-size: 11pt; font-weight: bold;")
        self.project_hours.setMinimumHeight(32)
        project_card_layout.addWidget(self.project_hours)
        
        self.project_days_label = QLabel("약 28일")
        self.project_days_label.setStyleSheet("color: #388E3C; font-size: 11pt; font-weight: bold;")
        project_card_layout.addWidget(self.project_days_label)
        
        project_card.setLayout(project_card_layout)
        hours_layout.addWidget(project_card)
        
        # 인턴쉽 시수 카드
        internship_card = QFrame()
        internship_card.setStyleSheet("""
            QFrame {
                background-color: #FFF3E0;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        internship_card_layout = QVBoxLayout()
        internship_card_layout.setSpacing(3)
        internship_card_layout.setContentsMargins(6, 6, 6, 6)
        
        internship_title = QLabel("📙 3단계: 인턴십")
        internship_title.setStyleSheet("font-weight: bold; font-size: 11pt; color: #F57C00;")
        internship_card_layout.addWidget(internship_title)
        
        self.internship_hours = QSpinBox()
        self.internship_hours.setRange(0, 9999)
        self.internship_hours.setValue(120)
        self.internship_hours.setSuffix(" 시간")
        self.internship_hours.valueChanged.connect(self.calculate_dates)
        self.internship_hours.setStyleSheet("font-size: 11pt; font-weight: bold;")
        self.internship_hours.setMinimumHeight(32)
        internship_card_layout.addWidget(self.internship_hours)
        
        self.internship_days_label = QLabel("약 15일")
        self.internship_days_label.setStyleSheet("color: #F57C00; font-size: 11pt; font-weight: bold;")
        internship_card_layout.addWidget(self.internship_days_label)
        
        internship_card.setLayout(internship_card_layout)
        hours_layout.addWidget(internship_card)
        
        hours_group.setLayout(hours_layout)
        layout.addWidget(hours_group)
        
        # 과정 일정 계산 결과 - 압축 버전
        calc_result_group = QGroupBox("📊 교육 일정 계산 결과")
        calc_result_group.setStyleSheet("QGroupBox { font-size: 11pt; font-weight: bold; padding-top: 10px; margin-top: 8px; }")
        calc_result_layout = QHBoxLayout()
        calc_result_layout.setSpacing(20)
        calc_result_layout.setContentsMargins(10, 8, 10, 8)
        
        # 총 기간
        total_period_layout = QVBoxLayout()
        total_period_layout.setSpacing(5)
        total_period_label = QLabel("총 기간")
        total_period_label.setStyleSheet("font-size: 11pt; color: #666;")
        total_period_layout.addWidget(total_period_label)
        
        self.total_days_label = QLabel("113일")
        self.total_days_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #2196F3;")
        total_period_layout.addWidget(self.total_days_label)
        calc_result_layout.addLayout(total_period_layout)
        
        calc_result_layout.addStretch()
        
        # 근무일 (실제 교육일)
        workdays_layout = QVBoxLayout()
        workdays_layout.setSpacing(5)
        workdays_label = QLabel("근무일 (600시간)")
        workdays_label.setStyleSheet("font-size: 11pt; color: #666;")
        workdays_layout.addWidget(workdays_label)
        
        self.workdays_label = QLabel("76일 (600시간)")
        self.workdays_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #4CAF50;")
        workdays_layout.addWidget(self.workdays_label)
        calc_result_layout.addLayout(workdays_layout)
        
        calc_result_layout.addStretch()
        
        # 제외일 (주말+공휴일)
        excluded_layout = QVBoxLayout()
        excluded_layout.setSpacing(5)
        excluded_label = QLabel("제외일 (주말+공휴일)")
        excluded_label.setStyleSheet("font-size: 11pt; color: #666;")
        excluded_layout.addWidget(excluded_label)
        
        self.excluded_days_label = QLabel("5일")
        self.excluded_days_label.setStyleSheet("font-size: 11pt; font-weight: bold; color: #F44336;")
        excluded_layout.addWidget(self.excluded_days_label)
        
        # 제외일 세부 정보 (주말/공휴일)
        self.excluded_detail_label = QLabel("주말: 0일/공휴일: 0일")
        self.excluded_detail_label.setStyleSheet("font-size: 11pt; color: #999;")
        excluded_layout.addWidget(self.excluded_detail_label)
        
        calc_result_layout.addLayout(excluded_layout)
        
        calc_result_group.setLayout(calc_result_layout)
        layout.addWidget(calc_result_group)
        
        # 공휴일 목록 표시
        holiday_list_group = QGroupBox("🎉 과정 기간 내 공휴일")
        holiday_list_group.setStyleSheet("QGroupBox { font-size: 11pt; font-weight: bold; padding-top: 10px; margin-top: 8px; }")
        holiday_list_layout = QVBoxLayout()
        holiday_list_layout.setSpacing(5)
        holiday_list_layout.setContentsMargins(10, 8, 10, 8)
        
        self.holiday_list_label = QLabel("공휴일이 없습니다.")
        self.holiday_list_label.setStyleSheet("font-size: 11pt; color: #666; padding: 8px;")
        self.holiday_list_label.setWordWrap(True)
        holiday_list_layout.addWidget(self.holiday_list_label)
        
        holiday_list_group.setLayout(holiday_list_layout)
        layout.addWidget(holiday_list_group)
        
        # 기본 정보 입력 폼
        form_group = QGroupBox("📋 기본 정보")
        form_group.setStyleSheet("QGroupBox { font-size: 11pt; font-weight: bold; padding-top: 10px; margin-top: 8px; }")
        form_layout = QGridLayout()
        form_layout.setSpacing(10)
        form_layout.setVerticalSpacing(12)
        form_layout.setContentsMargins(10, 8, 10, 8)
        
        # 코드
        code_label = QLabel("코드:")
        code_label.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(code_label, 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("C-001 (자동 생성)")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(200)
        self.code_input.setMinimumHeight(30)
        self.code_input.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(self.code_input, 0, 1)
        
        # 반명칭
        name_label = QLabel("반명칭:")
        name_label.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(name_label, 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 1반")
        self.name_input.setMinimumHeight(30)
        self.name_input.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(self.name_input, 0, 3)
        
        # 인원수
        capacity_label = QLabel("인원수:")
        capacity_label.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(capacity_label, 1, 0)
        self.capacity = QSpinBox()
        self.capacity.setRange(1, 999)
        self.capacity.setValue(30)
        self.capacity.setSuffix(" 명")
        self.capacity.setMinimumHeight(30)
        self.capacity.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(self.capacity, 1, 1)
        
        # 강의장소
        location_label = QLabel("강의장소:")
        location_label.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(location_label, 1, 2)
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("예: 본관 101호")
        self.location_input.setMinimumHeight(30)
        self.location_input.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(self.location_input, 1, 3)
        
        # 특이사항
        notes_label = QLabel("특이사항:")
        notes_label.setStyleSheet("font-size: 11pt;")
        form_layout.addWidget(notes_label, 2, 0)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("과정 관련 특이사항을 입력하세요")
        self.notes_input.setMinimumHeight(30)  # 15 → 30 (2배)
        self.notes_input.setMaximumHeight(30)  # 최대 높이도 30px
        self.notes_input.setStyleSheet("font-size: 11pt;")
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
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 11pt;")
        self.add_btn.setMinimumHeight(38)
        self.add_btn.clicked.connect(self.add_course)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 10px 20px; font-size: 11pt;")
        self.update_btn.setMinimumHeight(38)
        self.update_btn.clicked.connect(self.update_course)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 10px 20px; font-size: 11pt;")
        self.delete_btn.setMinimumHeight(38)
        self.delete_btn.clicked.connect(self.delete_course)
        btn_layout.addWidget(self.delete_btn)
        
        self.subject_select_btn = QPushButton("📚 과목 선택")
        self.subject_select_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 10px 20px; font-size: 11pt; font-weight: bold;")
        self.subject_select_btn.setMinimumHeight(38)
        self.subject_select_btn.clicked.connect(self.open_subject_selection)
        self.subject_select_btn.setEnabled(False)  # 과정 선택 시 활성화
        btn_layout.addWidget(self.subject_select_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.setStyleSheet("padding: 10px 20px; font-size: 11pt;")
        self.clear_btn.setMinimumHeight(38)
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
        
        # 테이블 폰트 크기 설정
        from PyQt5.QtGui import QFont
        table_font = QFont("맑은 고딕", 10)
        self.table.setFont(table_font)
        
        # 헤더 폰트 크기 설정
        header_font = QFont("맑은 고딕", 11, QFont.Bold)
        self.table.horizontalHeader().setFont(header_font)
        self.table.horizontalHeader().setMinimumHeight(28)
        
        # 행 높이 설정
        self.table.verticalHeader().setDefaultSectionSize(30)
        
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼
        # 하단 버튼 (탭으로 사용되므로 닫기 버튼 불필요)
        
        # 스크롤 컨텐츠 설정
        scroll_content.setLayout(layout)
        scroll_area.setWidget(scroll_content)
        
        # 메인 레이아웃에 스크롤 영역 추가
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
    
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
        
        # 공휴일 조회
        holidays = self.get_holidays()
        
        # 강의 종료일 계산
        lecture_end = self.calculate_end_date(start_date, lecture_days, holidays)
        
        # 프로젝트 종료일 계산 (강의 종료일 다음날부터 시작)
        project_start = lecture_end + timedelta(days=1)
        project_start = self.get_next_workday(project_start, holidays)
        project_end = self.calculate_end_date(project_start, project_days, holidays)
        
        # 인턴쉽 종료일 계산 (프로젝트 종료일 다음날부터 시작)
        internship_start = project_end + timedelta(days=1)
        internship_start = self.get_next_workday(internship_start, holidays)
        internship_end = self.calculate_end_date(internship_start, internship_days, holidays)
        
        # 계산된 날짜를 인스턴스 변수에 저장
        self.calculated_lecture_end = lecture_end
        self.calculated_project_end = project_end
        self.calculated_internship_end = internship_end
        self.calculated_final_end = internship_end
        
        # 일수 라벨 업데이트 (종료일 포함)
        self.lecture_days_label.setText(f"약 {lecture_days}일 ({lecture_end.strftime('%m-%d')} 까지)")
        self.project_days_label.setText(f"약 {project_days}일 ({project_end.strftime('%m-%d')} 까지)")
        self.internship_days_label.setText(f"약 {internship_days}일 ({internship_end.strftime('%m-%d')} 까지)")
        
        # 최종 종료일 (인턴쉽 종료일과 동일)
        self.final_end_date.setText(internship_end.strftime("%Y-%m-%d"))
        
        # 총 기간 계산 (시작일부터 최종 종료일까지)
        total_calendar_days = (internship_end - start_date).days + 1
        total_work_days = lecture_days + project_days + internship_days
        excluded_days = total_calendar_days - total_work_days
        
        # 주말과 공휴일 구분 계산
        weekend_count = 0
        holiday_count = 0
        current = start_date
        
        while current <= internship_end:
            # 주말 체크 (토요일=5, 일요일=6)
            if current.weekday() >= 5:
                weekend_count += 1
            # 공휴일 체크 (주말이 아닌 날 중에서)
            elif current in holidays:
                holiday_count += 1
            current += timedelta(days=1)
        
        # 라벨 업데이트
        self.total_days_label.setText(f"{total_calendar_days}일")
        self.workdays_label.setText(f"{total_work_days}일 (600시간)")
        self.excluded_days_label.setText(f"{excluded_days}일")
        
        # 제외일 세부 정보 업데이트 (계산 결과 섹션)
        self.excluded_detail_label.setText(f"주말: {weekend_count}일/공휴일: {holiday_count}일")
        
        # 공휴일 목록 표시
        self.update_holiday_list(start_date, internship_end, holidays)
    
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
    
    def update_holiday_list(self, start_date, end_date, holidays):
        """과정 기간 내 공휴일 목록 표시"""
        try:
            # 과정 기간 내 공휴일만 필터링
            holidays_in_range = []
            
            # 공휴일 상세 정보 조회
            if self.db.connect():
                query = """
                    SELECT holiday_date, name 
                    FROM holidays 
                    WHERE holiday_date BETWEEN %s AND %s
                    ORDER BY holiday_date
                """
                rows = self.db.fetch_all(query, (start_date, end_date))
                
                for row in rows:
                    holiday_date = row['holiday_date']
                    # 주말이 아닌 공휴일만 표시
                    if holiday_date.weekday() < 5:
                        date_str = holiday_date.strftime("%m-%d")
                        holidays_in_range.append(f"{date_str}({row['name']})")
            
            # 공휴일 목록 텍스트 생성
            if holidays_in_range:
                holiday_text = ", ".join(holidays_in_range)
                self.holiday_list_label.setText(holiday_text)
                self.holiday_list_label.setStyleSheet("font-size: 12px; color: #F44336; padding: 5px; font-weight: bold;")
            else:
                self.holiday_list_label.setText("공휴일이 없습니다.")
                self.holiday_list_label.setStyleSheet("font-size: 12px; color: #666; padding: 5px;")
                
        except Exception as e:
            print(f"공휴일 목록 표시 오류: {str(e)}")
            self.holiday_list_label.setText("공휴일 정보를 불러올 수 없습니다.")
            self.holiday_list_label.setStyleSheet("font-size: 12px; color: #666; padding: 5px;")
        
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
                
                # 시작일 - None 체크 개선
                start_date = ''
                if row.get('start_date') and row['start_date'] is not None:
                    start_date = row['start_date'].strftime("%Y-%m-%d")
                self.table.setItem(row_position, 2, QTableWidgetItem(start_date))
                
                # 강의 종료일 - None 체크 개선
                lecture_end = ''
                if row.get('lecture_end_date') and row['lecture_end_date'] is not None:
                    lecture_end = row['lecture_end_date'].strftime("%m-%d")
                self.table.setItem(row_position, 3, QTableWidgetItem(lecture_end))
                
                # 프로젝트 종료일 - None 체크 개선
                project_end = ''
                if row.get('project_end_date') and row['project_end_date'] is not None:
                    project_end = row['project_end_date'].strftime("%m-%d")
                self.table.setItem(row_position, 4, QTableWidgetItem(project_end))
                
                # 인턴쉽 종료일 - None 체크 개선
                internship_end = ''
                if row.get('internship_end_date') and row['internship_end_date'] is not None:
                    internship_end = row['internship_end_date'].strftime("%m-%d")
                self.table.setItem(row_position, 5, QTableWidgetItem(internship_end))
                
                # 총 기간 - None 체크 개선
                total_days = ''
                if row.get('total_days') and row['total_days'] is not None:
                    total_days = f"{row['total_days']}일"
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
        
        # 과목 선택 버튼 활성화
        self.subject_select_btn.setEnabled(True)
        
        # DB에서 전체 데이터 조회
        query = "SELECT * FROM courses WHERE code = %s"
        result = self.db.fetch_one(query, (code,))
        
        if result:
            self.code_input.setText(result['code'])
            self.name_input.setText(result['name'])
            
            # 시작일 설정 및 원본 저장
            if result.get('start_date') and result['start_date'] is not None:
                q_date = QDate(result['start_date'].year, result['start_date'].month, result['start_date'].day)
                self.start_date.setDate(q_date)
                self.original_start_date = result['start_date']  # 원본 시작일 저장
            
            self.lecture_hours.setValue(result['lecture_hours'])
            self.project_hours.setValue(result['project_hours'])
            self.internship_hours.setValue(result['internship_hours'])
            self.capacity.setValue(result['capacity'])
            self.location_input.setText(result['location'] or '')
            self.notes_input.setText(result['notes'] or '')
            
            # 일수 라벨 업데이트 (종료일 포함)
            lecture_days = (result['lecture_hours'] + 7) // 8
            project_days = (result['project_hours'] + 7) // 8
            internship_days = (result['internship_hours'] + 7) // 8
            
            # 저장된 날짜를 인스턴스 변수에 로드
            if result.get('lecture_end_date') and result['lecture_end_date'] is not None:
                self.calculated_lecture_end = result['lecture_end_date']
                self.lecture_days_label.setText(f"약 {lecture_days}일 ({result['lecture_end_date'].strftime('%m-%d')} 까지)")
            else:
                self.lecture_days_label.setText(f"약 {lecture_days}일")
                
            if result.get('project_end_date') and result['project_end_date'] is not None:
                self.calculated_project_end = result['project_end_date']
                self.project_days_label.setText(f"약 {project_days}일 ({result['project_end_date'].strftime('%m-%d')} 까지)")
            else:
                self.project_days_label.setText(f"약 {project_days}일")
                
            if result.get('internship_end_date') and result['internship_end_date'] is not None:
                self.calculated_internship_end = result['internship_end_date']
                self.calculated_final_end = result['internship_end_date']
                self.internship_days_label.setText(f"약 {internship_days}일 ({result['internship_end_date'].strftime('%m-%d')} 까지)")
            else:
                self.internship_days_label.setText(f"약 {internship_days}일")
            
            # 계산 결과 업데이트
            if result.get('total_days') and result['total_days'] is not None:
                lecture_days = (result['lecture_hours'] + 7) // 8
                project_days = (result['project_hours'] + 7) // 8
                internship_days = (result['internship_hours'] + 7) // 8
                total_work_days = lecture_days + project_days + internship_days
                excluded_days = result['total_days'] - total_work_days
                
                self.total_days_label.setText(f"{result['total_days']}일")
                self.workdays_label.setText(f"{total_work_days}일 (600시간)")
                self.excluded_days_label.setText(f"{excluded_days}일")
                
                # 주말과 공휴일 구분 계산
                if result.get('start_date') and result.get('internship_end_date'):
                    holidays = self.get_holidays()
                    weekend_count = 0
                    holiday_count = 0
                    current = result['start_date']
                    
                    while current <= result['internship_end_date']:
                        if current.weekday() >= 5:
                            weekend_count += 1
                        elif current in holidays:
                            holiday_count += 1
                        current += timedelta(days=1)
                    
                    self.excluded_detail_label.setText(f"주말: {weekend_count}일/공휴일: {holiday_count}일")
                    
                    # 공휴일 목록 업데이트
                    self.update_holiday_list(result['start_date'], result['internship_end_date'], holidays)
                else:
                    self.excluded_detail_label.setText("주말: 0일/공휴일: 0일")
                    self.holiday_list_label.setText("공휴일이 없습니다.")
                    self.holiday_list_label.setStyleSheet("font-size: 12px; color: #666; padding: 5px;")
        
    def add_course(self):
        """과정 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "반명칭을 입력하세요.")
            return
        
        # 날짜 정보
        start_date = self.start_date.date().toPyDate()
        
        # 계산된 날짜 확인
        if not hasattr(self, 'calculated_lecture_end') or not hasattr(self, 'calculated_project_end') or not hasattr(self, 'calculated_internship_end'):
            QMessageBox.warning(self, "경고", "일정 자동계산 버튼을 클릭하여 일정을 먼저 계산하세요.")
            return
        
        lecture_end = self.calculated_lecture_end.strftime("%Y-%m-%d")
        project_end = self.calculated_project_end.strftime("%Y-%m-%d")
        internship_end = self.calculated_internship_end.strftime("%Y-%m-%d")
        final_end = self.calculated_final_end.strftime("%Y-%m-%d")
        
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
        
        # 계산된 날짜 확인
        if not hasattr(self, 'calculated_lecture_end') or not hasattr(self, 'calculated_project_end') or not hasattr(self, 'calculated_internship_end'):
            QMessageBox.warning(self, "경고", "일정 자동계산 버튼을 클릭하여 일정을 먼저 계산하세요.")
            return
        
        # 시작일이 변경되었는지 확인
        if hasattr(self, 'original_start_date'):
            if start_date != self.original_start_date:
                reply = QMessageBox.question(
                    self, "확인",
                    "시작일이 변경되었습니다.\n일정 자동계산을 먼저 수행하시겠습니까?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    self.calculate_dates()  # 올바른 메서드 이름
                    # 재계산 후 다시 날짜 가져오기 (아래 코드에서 사용됨)
                else:
                    QMessageBox.warning(self, "경고", "시작일 변경 시 일정을 다시 계산해야 합니다.")
                    return
        
        lecture_end = self.calculated_lecture_end.strftime("%Y-%m-%d")
        project_end = self.calculated_project_end.strftime("%Y-%m-%d")
        internship_end = self.calculated_internship_end.strftime("%Y-%m-%d")
        final_end = self.calculated_final_end.strftime("%Y-%m-%d")
        
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
        
        # 계산된 날짜 인스턴스 변수 초기화
        if hasattr(self, 'calculated_lecture_end'):
            delattr(self, 'calculated_lecture_end')
        if hasattr(self, 'calculated_project_end'):
            delattr(self, 'calculated_project_end')
        if hasattr(self, 'calculated_internship_end'):
            delattr(self, 'calculated_internship_end')
        if hasattr(self, 'calculated_final_end'):
            delattr(self, 'calculated_final_end')
        
        # 라벨 초기화
        self.lecture_days_label.setText("약 33일")
        self.project_days_label.setText("약 28일")
        self.internship_days_label.setText("약 15일")
        self.total_days_label.setText("계산 필요")
        self.workdays_label.setText("계산 필요")
        self.excluded_days_label.setText("계산 필요")
    
    def open_subject_selection(self):
        """과목 선택 다이얼로그 열기"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "경고", "과정을 먼저 선택하세요.")
            return
        
        # 선택된 과정 코드 가져오기
        course_code_item = self.table.item(selected_row, 0)
        if not course_code_item:
            QMessageBox.warning(self, "경고", "과정 코드를 찾을 수 없습니다.")
            return
        
        course_code = course_code_item.text()
        course_name = self.table.item(selected_row, 1).text() if self.table.item(selected_row, 1) else ""
        
        # 과목 선택 다이얼로그 열기
        dialog = SubjectSelectionDialog(course_code, course_name, self)
        dialog.exec_()


class SubjectSelectionDialog(QDialog):
    """과정별 과목 선택 다이얼로그"""
    
    def __init__(self, course_code, course_name, parent=None):
        super().__init__(parent)
        self.course_code = course_code
        self.course_name = course_name
        self.db = DatabaseManager()
        self.init_ui()
        self.load_subjects()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(f"과목 선택 - {self.course_name} ({self.course_code})")
        self.setMinimumSize(900, 600)
        
        layout = QVBoxLayout()
        
        # 안내 메시지
        info_label = QLabel(
            f"📚 {self.course_name} 과정에 사용할 과목을 선택하세요.\n"
            "체크박스를 선택/해제하여 과목을 추가/제거할 수 있습니다."
        )
        info_label.setStyleSheet("font-size: 11pt; padding: 10px; background-color: #E3F2FD; border-radius: 5px;")
        layout.addWidget(info_label)
        
        # 과목 테이블
        self.subject_table = QTableWidget()
        self.subject_table.setColumnCount(7)
        self.subject_table.setHorizontalHeaderLabels([
            "선택", "과목코드", "과목명", "시수", "요일", "격주", "담당강사"
        ])
        self.subject_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.subject_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.subject_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.subject_table.setStyleSheet("font-size: 11pt;")
        layout.addWidget(self.subject_table)
        
        # 버튼
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        save_btn = QPushButton("💾 저장")
        save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 20px; font-size: 11pt;")
        save_btn.setMinimumHeight(40)
        save_btn.clicked.connect(self.save_selections)
        btn_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("취소")
        cancel_btn.setStyleSheet("padding: 10px 20px; font-size: 11pt;")
        cancel_btn.setMinimumHeight(40)
        cancel_btn.clicked.connect(self.reject)
        btn_layout.addWidget(cancel_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
    
    def load_subjects(self):
        """모든 과목 로드 및 선택 상태 표시"""
        try:
            if not self.db.connect():
                QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
                return
            
            # 모든 과목 조회
            query = """
                SELECT s.code, s.name, s.hours, s.day_of_week, s.is_biweekly,
                       i.name as instructor_name
                FROM subjects s
                LEFT JOIN instructors i ON s.main_instructor = i.code
                ORDER BY s.code
            """
            all_subjects = self.db.fetch_all(query)
            
            # 현재 과정에 선택된 과목 조회
            query_selected = """
                SELECT subject_code
                FROM course_subjects
                WHERE course_code = %s
            """
            selected_subjects = self.db.fetch_all(query_selected, (self.course_code,))
            selected_codes = set([s['subject_code'] for s in selected_subjects])
            
            # 테이블에 표시
            self.subject_table.setRowCount(len(all_subjects))
            
            day_names = ["월", "화", "수", "목", "금"]
            
            for i, subject in enumerate(all_subjects):
                # 체크박스
                from PyQt5.QtWidgets import QCheckBox
                checkbox = QCheckBox()
                checkbox.setChecked(subject['code'] in selected_codes)
                checkbox.setStyleSheet("margin-left: 20px;")
                
                checkbox_widget = QWidget()
                checkbox_layout = QHBoxLayout(checkbox_widget)
                checkbox_layout.addWidget(checkbox)
                checkbox_layout.setAlignment(Qt.AlignCenter)
                checkbox_layout.setContentsMargins(0, 0, 0, 0)
                
                self.subject_table.setCellWidget(i, 0, checkbox_widget)
                
                # 과목 정보
                self.subject_table.setItem(i, 1, QTableWidgetItem(subject['code']))
                self.subject_table.setItem(i, 2, QTableWidgetItem(subject['name']))
                self.subject_table.setItem(i, 3, QTableWidgetItem(f"{subject['hours']}시간"))
                
                # 요일
                day_str = day_names[subject['day_of_week']] if subject.get('day_of_week') is not None and 0 <= subject['day_of_week'] <= 4 else "-"
                self.subject_table.setItem(i, 4, QTableWidgetItem(day_str))
                
                # 격주
                biweekly_str = "격주" if subject.get('is_biweekly') else "매주"
                self.subject_table.setItem(i, 5, QTableWidgetItem(biweekly_str))
                
                # 담당강사
                instructor = subject.get('instructor_name') or '-'
                self.subject_table.setItem(i, 6, QTableWidgetItem(instructor))
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"과목 로드 실패: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def save_selections(self):
        """선택된 과목 저장"""
        try:
            if not self.db.connect():
                QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
                return
            
            # 기존 선택 삭제
            delete_query = "DELETE FROM course_subjects WHERE course_code = %s"
            self.db.execute_query(delete_query, (self.course_code,))
            
            # 새로운 선택 저장
            insert_query = """
                INSERT INTO course_subjects (course_code, subject_code, display_order)
                VALUES (%s, %s, %s)
            """
            
            selected_count = 0
            for i in range(self.subject_table.rowCount()):
                checkbox_widget = self.subject_table.cellWidget(i, 0)
                checkbox = checkbox_widget.findChild(QCheckBox)
                
                if checkbox and checkbox.isChecked():
                    subject_code = self.subject_table.item(i, 1).text()
                    self.db.execute_query(insert_query, (self.course_code, subject_code, i))
                    selected_count += 1
            
            QMessageBox.information(
                self, 
                "완료", 
                f"{selected_count}개 과목이 {self.course_name} 과정에 저장되었습니다."
            )
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 실패: {str(e)}")
            import traceback
            traceback.print_exc()


