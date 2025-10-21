# -*- coding: utf-8 -*-
"""
시간표 조회/수정 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLabel, QComboBox,
                             QMessageBox, QHeaderView, QGroupBox, QDateEdit,
                             QTimeEdit, QLineEdit, QTextEdit, QCalendarWidget,
                             QTabWidget, QWidget, QGridLayout)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QColor, QTextCharFormat
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager


class TimetableViewDialog(QDialog):
    """시간표 조회/수정 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.current_timetable_id = None
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("시간표 조회/수정")
        self.setGeometry(100, 100, 1400, 800)
        
        layout = QVBoxLayout()
        
        # 탭 위젯
        self.tabs = QTabWidget()
        
        # 탭 1: 테이블 뷰
        self.table_tab = self.create_table_tab()
        self.tabs.addTab(self.table_tab, "📋 테이블 뷰")
        
        # 탭 2: 달력 뷰
        self.calendar_tab = self.create_calendar_tab()
        self.tabs.addTab(self.calendar_tab, "📅 달력 뷰")
        
        # 탭 3: 강사별 스케줄
        self.instructor_tab = self.create_instructor_tab()
        self.tabs.addTab(self.instructor_tab, "👨‍🏫 강사별 스케줄")
        
        layout.addWidget(self.tabs)
        
        # 하단 버튼
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        refresh_btn = QPushButton("새로고침")
        refresh_btn.clicked.connect(self.load_data)
        btn_layout.addWidget(refresh_btn)
        
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)
        
        layout.addLayout(btn_layout)
        
        self.setLayout(layout)
        
        # 데이터 로드
        self.load_courses()
        self.load_data()
        
    def create_table_tab(self):
        """테이블 뷰 탭 생성"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 필터 그룹
        filter_group = QGroupBox("검색 필터")
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("과정:"))
        self.table_course_combo = QComboBox()
        self.table_course_combo.currentIndexChanged.connect(self.filter_table)
        filter_layout.addWidget(self.table_course_combo)
        
        filter_layout.addWidget(QLabel("유형:"))
        self.table_type_combo = QComboBox()
        self.table_type_combo.addItems(["전체", "강의", "프로젝트", "인턴쉽"])
        self.table_type_combo.currentIndexChanged.connect(self.filter_table)
        filter_layout.addWidget(self.table_type_combo)
        
        filter_layout.addWidget(QLabel("날짜:"))
        self.table_date_from = QDateEdit()
        self.table_date_from.setDate(QDate.currentDate().addMonths(-1))
        self.table_date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.table_date_from)
        
        filter_layout.addWidget(QLabel("~"))
        self.table_date_to = QDateEdit()
        self.table_date_to.setDate(QDate.currentDate().addMonths(6))
        self.table_date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.table_date_to)
        
        search_btn = QPushButton("검색")
        search_btn.clicked.connect(self.filter_table)
        filter_layout.addWidget(search_btn)
        
        filter_layout.addStretch()
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # 편집 폼
        edit_group = QGroupBox("시간표 편집")
        edit_layout = QGridLayout()
        
        edit_layout.addWidget(QLabel("ID:"), 0, 0)
        self.edit_id = QLineEdit()
        self.edit_id.setReadOnly(True)
        self.edit_id.setMaximumWidth(100)
        edit_layout.addWidget(self.edit_id, 0, 1)
        
        edit_layout.addWidget(QLabel("날짜:"), 0, 2)
        self.edit_date = QDateEdit()
        self.edit_date.setCalendarPopup(True)
        edit_layout.addWidget(self.edit_date, 0, 3)
        
        edit_layout.addWidget(QLabel("시작 시간:"), 0, 4)
        self.edit_start_time = QTimeEdit()
        edit_layout.addWidget(self.edit_start_time, 0, 5)
        
        edit_layout.addWidget(QLabel("종료 시간:"), 1, 0)
        self.edit_end_time = QTimeEdit()
        edit_layout.addWidget(self.edit_end_time, 1, 1)
        
        edit_layout.addWidget(QLabel("교과목:"), 1, 2)
        self.edit_subject = QComboBox()
        edit_layout.addWidget(self.edit_subject, 1, 3)
        
        edit_layout.addWidget(QLabel("강사:"), 1, 4)
        self.edit_instructor = QComboBox()
        edit_layout.addWidget(self.edit_instructor, 1, 5)
        
        edit_layout.addWidget(QLabel("비고:"), 2, 0)
        self.edit_notes = QLineEdit()
        edit_layout.addWidget(self.edit_notes, 2, 1, 1, 5)
        
        # 편집 버튼
        edit_btn_layout = QHBoxLayout()
        edit_btn_layout.addStretch()
        
        self.save_btn = QPushButton("저장")
        self.save_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px;")
        self.save_btn.clicked.connect(self.save_timetable)
        edit_btn_layout.addWidget(self.save_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px;")
        self.delete_btn.clicked.connect(self.delete_timetable)
        edit_btn_layout.addWidget(self.delete_btn)
        
        edit_layout.addLayout(edit_btn_layout, 3, 0, 1, 6)
        
        edit_group.setLayout(edit_layout)
        layout.addWidget(edit_group)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "과정", "날짜", "시작시간", "종료시간", "교과목", "강사", "유형", "비고"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        self.table.setColumnWidth(0, 50)
        layout.addWidget(self.table)
        
        tab.setLayout(layout)
        return tab
        
    def create_calendar_tab(self):
        """달력 뷰 탭 생성"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 필터
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("과정:"))
        self.calendar_course_combo = QComboBox()
        self.calendar_course_combo.currentIndexChanged.connect(self.load_calendar)
        filter_layout.addWidget(self.calendar_course_combo)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # 달력
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.clicked.connect(self.on_date_clicked)
        layout.addWidget(self.calendar)
        
        # 선택한 날짜의 일정
        self.date_schedule = QTextEdit()
        self.date_schedule.setReadOnly(True)
        self.date_schedule.setMaximumHeight(200)
        layout.addWidget(QLabel("선택한 날짜의 일정:"))
        layout.addWidget(self.date_schedule)
        
        tab.setLayout(layout)
        return tab
        
    def create_instructor_tab(self):
        """강사별 스케줄 탭 생성"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # 강사 선택
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("강사:"))
        self.instructor_combo = QComboBox()
        self.instructor_combo.currentIndexChanged.connect(self.load_instructor_schedule)
        filter_layout.addWidget(self.instructor_combo)
        
        filter_layout.addWidget(QLabel("기간:"))
        self.instructor_date_from = QDateEdit()
        self.instructor_date_from.setDate(QDate.currentDate())
        self.instructor_date_from.setCalendarPopup(True)
        filter_layout.addWidget(self.instructor_date_from)
        
        filter_layout.addWidget(QLabel("~"))
        self.instructor_date_to = QDateEdit()
        self.instructor_date_to.setDate(QDate.currentDate().addMonths(3))
        self.instructor_date_to.setCalendarPopup(True)
        filter_layout.addWidget(self.instructor_date_to)
        
        search_btn = QPushButton("조회")
        search_btn.clicked.connect(self.load_instructor_schedule)
        filter_layout.addWidget(search_btn)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # 강사 스케줄 테이블
        self.instructor_table = QTableWidget()
        self.instructor_table.setColumnCount(6)
        self.instructor_table.setHorizontalHeaderLabels([
            "날짜", "시작시간", "종료시간", "과정", "교과목", "비고"
        ])
        self.instructor_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.instructor_table)
        
        tab.setLayout(layout)
        return tab
        
    def load_courses(self):
        """과정 목록 로드"""
        if not self.db.connect():
            return
        
        try:
            query = "SELECT code, name FROM courses ORDER BY code"
            rows = self.db.fetch_all(query)
            
            # 각 콤보박스에 추가
            for combo in [self.table_course_combo, self.calendar_course_combo]:
                combo.clear()
                combo.addItem("전체", None)
                for row in rows:
                    combo.addItem(f"{row['name']} ({row['code']})", row['code'])
            
            # 교과목 로드
            subject_query = "SELECT code, name FROM subjects ORDER BY code"
            subjects = self.db.fetch_all(subject_query)
            
            self.edit_subject.clear()
            self.edit_subject.addItem("선택 안함", None)
            for subject in subjects:
                self.edit_subject.addItem(f"{subject['name']} ({subject['code']})", subject['code'])
            
            # 강사 로드
            instructor_query = "SELECT code, name FROM instructors ORDER BY name"
            instructors = self.db.fetch_all(instructor_query)
            
            self.edit_instructor.clear()
            self.edit_instructor.addItem("선택 안함", None)
            
            self.instructor_combo.clear()
            self.instructor_combo.addItem("선택하세요", None)
            
            for instructor in instructors:
                display = f"{instructor['name']} ({instructor['code']})"
                self.edit_instructor.addItem(display, instructor['code'])
                self.instructor_combo.addItem(display, instructor['code'])
                
        except Exception as e:
            print(f"목록 로드 오류: {str(e)}")
        
    def load_data(self):
        """데이터 로드"""
        self.filter_table()
        self.load_calendar()
        
    def filter_table(self):
        """테이블 필터링"""
        if not self.db.connect():
            return
        
        try:
            course_code = self.table_course_combo.currentData()
            type_text = self.table_type_combo.currentText()
            date_from = self.table_date_from.date().toString("yyyy-MM-dd")
            date_to = self.table_date_to.date().toString("yyyy-MM-dd")
            
            query = """
                SELECT t.*, c.name as course_name, s.name as subject_name, i.name as instructor_name
                FROM timetables t
                LEFT JOIN courses c ON t.course_code = c.code
                LEFT JOIN subjects s ON t.subject_code = s.code
                LEFT JOIN instructors i ON t.instructor_code = i.code
                WHERE t.class_date BETWEEN %s AND %s
            """
            params = [date_from, date_to]
            
            if course_code:
                query += " AND t.course_code = %s"
                params.append(course_code)
            
            if type_text != "전체":
                type_map = {"강의": "lecture", "프로젝트": "project", "인턴쉽": "internship"}
                query += " AND t.type = %s"
                params.append(type_map[type_text])
            
            query += " ORDER BY t.class_date, t.start_time"
            
            rows = self.db.fetch_all(query, tuple(params))
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                type_map = {"lecture": "강의", "project": "프로젝트", "internship": "인턴쉽"}
                
                self.table.setItem(row_position, 0, QTableWidgetItem(str(row['id'])))
                self.table.setItem(row_position, 1, QTableWidgetItem(row['course_name'] or ''))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(row['class_date'])))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(row['start_time'])))
                self.table.setItem(row_position, 4, QTableWidgetItem(str(row['end_time'])))
                self.table.setItem(row_position, 5, QTableWidgetItem(row['subject_name'] or '-'))
                self.table.setItem(row_position, 6, QTableWidgetItem(row['instructor_name'] or '-'))
                self.table.setItem(row_position, 7, QTableWidgetItem(type_map.get(row['type'], row['type'])))
                self.table.setItem(row_position, 8, QTableWidgetItem(row['notes'] or ''))
                
        except Exception as e:
            print(f"테이블 로드 오류: {str(e)}")
    
    def load_calendar(self):
        """달력에 시간표 표시"""
        if not self.db.connect():
            return
        
        try:
            course_code = self.calendar_course_combo.currentData()
            
            query = "SELECT DISTINCT class_date, type FROM timetables"
            params = []
            
            if course_code:
                query += " WHERE course_code = %s"
                params.append(course_code)
            
            rows = self.db.fetch_all(query, tuple(params) if params else None)
            
            # 달력 포맷 초기화
            self.calendar.setDateTextFormat(QDate(), QTextCharFormat())
            
            # 수업 날짜에 색상 표시
            for row in rows:
                date = QDate(row['class_date'].year, row['class_date'].month, row['class_date'].day)
                format = QTextCharFormat()
                
                if row['type'] == 'lecture':
                    format.setBackground(QColor("#E3F2FD"))  # 파랑
                elif row['type'] == 'project':
                    format.setBackground(QColor("#FFF3E0"))  # 주황
                elif row['type'] == 'internship':
                    format.setBackground(QColor("#E8F5E9"))  # 초록
                
                format.setFontWeight(75)
                self.calendar.setDateTextFormat(date, format)
                
        except Exception as e:
            print(f"달력 로드 오류: {str(e)}")
    
    def on_date_clicked(self, date):
        """달력 날짜 클릭 시"""
        if not self.db.connect():
            return
        
        try:
            date_str = date.toString("yyyy-MM-dd")
            course_code = self.calendar_course_combo.currentData()
            
            query = """
                SELECT t.*, s.name as subject_name, i.name as instructor_name
                FROM timetables t
                LEFT JOIN subjects s ON t.subject_code = s.code
                LEFT JOIN instructors i ON t.instructor_code = i.code
                WHERE t.class_date = %s
            """
            params = [date_str]
            
            if course_code:
                query += " AND t.course_code = %s"
                params.append(course_code)
            
            query += " ORDER BY t.start_time"
            
            rows = self.db.fetch_all(query, tuple(params))
            
            if rows:
                type_map = {"lecture": "강의", "project": "프로젝트", "internship": "인턴쉽"}
                schedule_text = f"📅 {date_str} 일정\n\n"
                
                for row in rows:
                    schedule_text += f"⏰ {row['start_time']} ~ {row['end_time']}\n"
                    schedule_text += f"   유형: {type_map.get(row['type'], row['type'])}\n"
                    if row['subject_name']:
                        schedule_text += f"   교과목: {row['subject_name']}\n"
                    if row['instructor_name']:
                        schedule_text += f"   강사: {row['instructor_name']}\n"
                    if row['notes']:
                        schedule_text += f"   비고: {row['notes']}\n"
                    schedule_text += "\n"
                
                self.date_schedule.setText(schedule_text)
            else:
                self.date_schedule.setText(f"📅 {date_str}\n\n일정이 없습니다.")
                
        except Exception as e:
            print(f"날짜 일정 조회 오류: {str(e)}")
    
    def load_instructor_schedule(self):
        """강사별 스케줄 로드"""
        if not self.db.connect():
            return
        
        instructor_code = self.instructor_combo.currentData()
        if not instructor_code:
            return
        
        try:
            date_from = self.instructor_date_from.date().toString("yyyy-MM-dd")
            date_to = self.instructor_date_to.date().toString("yyyy-MM-dd")
            
            query = """
                SELECT t.*, c.name as course_name, s.name as subject_name
                FROM timetables t
                LEFT JOIN courses c ON t.course_code = c.code
                LEFT JOIN subjects s ON t.subject_code = s.code
                WHERE t.instructor_code = %s
                AND t.class_date BETWEEN %s AND %s
                ORDER BY t.class_date, t.start_time
            """
            
            rows = self.db.fetch_all(query, (instructor_code, date_from, date_to))
            
            self.instructor_table.setRowCount(0)
            for row in rows:
                row_position = self.instructor_table.rowCount()
                self.instructor_table.insertRow(row_position)
                
                self.instructor_table.setItem(row_position, 0, QTableWidgetItem(str(row['class_date'])))
                self.instructor_table.setItem(row_position, 1, QTableWidgetItem(str(row['start_time'])))
                self.instructor_table.setItem(row_position, 2, QTableWidgetItem(str(row['end_time'])))
                self.instructor_table.setItem(row_position, 3, QTableWidgetItem(row['course_name'] or ''))
                self.instructor_table.setItem(row_position, 4, QTableWidgetItem(row['subject_name'] or '-'))
                self.instructor_table.setItem(row_position, 5, QTableWidgetItem(row['notes'] or ''))
                
        except Exception as e:
            print(f"강사 스케줄 로드 오류: {str(e)}")
    
    def on_row_selected(self, row, column):
        """테이블 행 선택 시"""
        timetable_id = int(self.table.item(row, 0).text())
        
        # DB에서 상세 정보 조회
        query = "SELECT * FROM timetables WHERE id = %s"
        result = self.db.fetch_one(query, (timetable_id,))
        
        if result:
            self.current_timetable_id = timetable_id
            self.edit_id.setText(str(result['id']))
            
            date = QDate(result['class_date'].year, result['class_date'].month, result['class_date'].day)
            self.edit_date.setDate(date)
            
            start_time = QTime.fromString(str(result['start_time']), "HH:mm:ss")
            self.edit_start_time.setTime(start_time)
            
            end_time = QTime.fromString(str(result['end_time']), "HH:mm:ss")
            self.edit_end_time.setTime(end_time)
            
            # 교과목 찾기
            for i in range(self.edit_subject.count()):
                if self.edit_subject.itemData(i) == result['subject_code']:
                    self.edit_subject.setCurrentIndex(i)
                    break
            
            # 강사 찾기
            for i in range(self.edit_instructor.count()):
                if self.edit_instructor.itemData(i) == result['instructor_code']:
                    self.edit_instructor.setCurrentIndex(i)
                    break
            
            self.edit_notes.setText(result['notes'] or '')
    
    def save_timetable(self):
        """시간표 저장"""
        if not self.current_timetable_id:
            QMessageBox.warning(self, "경고", "수정할 시간표를 선택하세요.")
            return
        
        try:
            date = self.edit_date.date().toString("yyyy-MM-dd")
            start_time = self.edit_start_time.time().toString("HH:mm")
            end_time = self.edit_end_time.time().toString("HH:mm")
            subject_code = self.edit_subject.currentData()
            instructor_code = self.edit_instructor.currentData()
            notes = self.edit_notes.text().strip()
            
            query = """
                UPDATE timetables 
                SET class_date = %s, start_time = %s, end_time = %s,
                    subject_code = %s, instructor_code = %s, notes = %s
                WHERE id = %s
            """
            
            self.db.execute_query(query, (date, start_time, end_time, subject_code, instructor_code, notes, self.current_timetable_id))
            
            QMessageBox.information(self, "성공", "시간표가 수정되었습니다.")
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 실패: {str(e)}")
    
    def delete_timetable(self):
        """시간표 삭제"""
        if not self.current_timetable_id:
            QMessageBox.warning(self, "경고", "삭제할 시간표를 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     "이 시간표를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM timetables WHERE id = %s"
                self.db.execute_query(query, (self.current_timetable_id,))
                
                QMessageBox.information(self, "성공", "시간표가 삭제되었습니다.")
                self.current_timetable_id = None
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def closeEvent(self, event):
        """닫기 이벤트"""
        self.db.disconnect()
        event.accept()
