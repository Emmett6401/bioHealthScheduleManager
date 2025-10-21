# -*- coding: utf-8 -*-
"""
PDF 보고서 생성 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QComboBox, QMessageBox, QGroupBox,
                             QRadioButton, QButtonGroup, QTextEdit, QProgressBar)
from PyQt5.QtCore import Qt
import sys
import os
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from utils.pdf_generator import PDFGenerator


class PDFReportDialog(QDialog):
    """PDF 보고서 생성 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.pdf_gen = PDFGenerator()
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("보고서 생성")
        self.setGeometry(200, 200, 700, 600)
        
        layout = QVBoxLayout()
        
        # 보고서 유형 선택
        type_group = QGroupBox("보고서 유형")
        type_layout = QVBoxLayout()
        
        self.type_group = QButtonGroup()
        
        self.timetable_radio = QRadioButton("📋 시간표 보고서")
        self.timetable_radio.setChecked(True)
        self.type_group.addButton(self.timetable_radio, 1)
        type_layout.addWidget(self.timetable_radio)
        
        self.attendance_radio = QRadioButton("📝 출석부 양식")
        self.type_group.addButton(self.attendance_radio, 2)
        type_layout.addWidget(self.attendance_radio)
        
        self.grade_radio = QRadioButton("📊 성적표 양식")
        self.type_group.addButton(self.grade_radio, 3)
        type_layout.addWidget(self.grade_radio)
        
        self.type_group.buttonClicked.connect(self.on_type_changed)
        
        type_group.setLayout(type_layout)
        layout.addWidget(type_group)
        
        # 과정 선택
        course_group = QGroupBox("과정 선택")
        course_layout = QHBoxLayout()
        
        course_layout.addWidget(QLabel("과정:"))
        self.course_combo = QComboBox()
        self.course_combo.setMinimumWidth(300)
        course_layout.addWidget(self.course_combo)
        course_layout.addStretch()
        
        course_group.setLayout(course_layout)
        layout.addWidget(course_group)
        
        # 보고서 설명
        info_group = QGroupBox("보고서 설명")
        info_layout = QVBoxLayout()
        
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMaximumHeight(150)
        self.update_info_text()
        
        info_layout.addWidget(self.info_text)
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # 진행바
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 결과 메시지
        self.result_label = QLabel("")
        self.result_label.setStyleSheet("color: green; font-weight: bold;")
        self.result_label.setVisible(False)
        layout.addWidget(self.result_label)
        
        layout.addStretch()
        
        # 버튼
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.generate_btn = QPushButton("생성하기")
        self.generate_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px 30px; font-size: 14px;")
        self.generate_btn.clicked.connect(self.generate_report)
        btn_layout.addWidget(self.generate_btn)
        
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
            query = "SELECT * FROM courses ORDER BY code"
            rows = self.db.fetch_all(query)
            
            self.course_combo.clear()
            self.course_combo.addItem("선택하세요", None)
            
            for row in rows:
                display_text = f"{row['name']} ({row['code']})"
                self.course_combo.addItem(display_text, row)
                
        except Exception as e:
            print(f"과정 목록 로드 오류: {str(e)}")
    
    def on_type_changed(self):
        """보고서 유형 변경 시"""
        self.update_info_text()
    
    def update_info_text(self):
        """보고서 설명 업데이트"""
        selected_id = self.type_group.checkedId()
        
        if selected_id == 1:  # 시간표
            text = """
📋 시간표 보고서

선택한 과정의 전체 시간표를 PDF로 생성합니다.

포함 내용:
• 과정 기본 정보 (과정명, 시수, 인원 등)
• 날짜별 상세 시간표
• 교과목 및 강사 정보
• 강의/프로젝트/인턴쉽 구분

활용:
• 과정 안내 자료
• 학생 배포용
• 보고서 제출용
            """
        elif selected_id == 2:  # 출석부
            text = """
📝 출석부 양식

출석 체크를 위한 빈 양식을 생성합니다.

포함 내용:
• 과정명 및 기본 정보
• 학생 명단 (프로젝트 구성원 기준)
• 날짜별 출석 체크 칸 (최대 20일)
• 번호, 이름 포함

활용:
• 일일 출석 체크
• 출석률 관리
• 교육 이수 증빙
            """
        else:  # 성적표
            text = """
📊 성적표 양식

성적 기록을 위한 빈 양식을 생성합니다.

포함 내용:
• 과정명 및 기본 정보
• 학생 명단
• 교과목별 성적 입력 칸
• 평균 및 등급 칸

활용:
• 중간/기말 평가
• 프로젝트 평가
• 수료 증빙
            """
        
        self.info_text.setText(text)
    
    def generate_report(self):
        """보고서 생성"""
        course = self.course_combo.currentData()
        
        if not course:
            QMessageBox.warning(self, "경고", "과정을 선택하세요.")
            return
        
        selected_id = self.type_group.checkedId()
        
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        # 진행바 표시
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        
        try:
            if selected_id == 1:  # 시간표
                filename = self.generate_timetable_report(course)
            elif selected_id == 2:  # 출석부
                filename = self.generate_attendance_report(course)
            else:  # 성적표
                filename = self.generate_grade_report(course)
            
            # 진행바 숨기기
            self.progress_bar.setVisible(False)
            
            # 결과 표시
            self.result_label.setText(f"✅ 생성 완료: {filename}")
            self.result_label.setVisible(True)
            
            QMessageBox.information(self, "성공", 
                                   f"보고서가 생성되었습니다.\n\n파일: {filename}")
            
        except Exception as e:
            self.progress_bar.setVisible(False)
            QMessageBox.critical(self, "오류", f"보고서 생성 실패:\n{str(e)}")
    
    def generate_timetable_report(self, course):
        """시간표 보고서 생성"""
        # 시간표 데이터 조회
        query = """
            SELECT t.*, s.name as subject_name, i.name as instructor_name
            FROM timetables t
            LEFT JOIN subjects s ON t.subject_code = s.code
            LEFT JOIN instructors i ON t.instructor_code = i.code
            WHERE t.course_code = %s
            ORDER BY t.class_date, t.start_time
        """
        
        timetable_data = self.db.fetch_all(query, (course['code'],))
        
        if not timetable_data:
            raise Exception("시간표 데이터가 없습니다. 먼저 시간표를 생성하세요.")
        
        # PDF 생성
        filename = self.pdf_gen.generate_timetable_report(course, timetable_data, f"시간표_{course['name']}")
        
        return filename
    
    def generate_attendance_report(self, course):
        """출석부 양식 생성"""
        # 프로젝트에서 학생 명단 조회
        query = """
            SELECT 
                member1_name as name FROM projects WHERE course_code = %s AND member1_name IS NOT NULL
            UNION
            SELECT member2_name FROM projects WHERE course_code = %s AND member2_name IS NOT NULL
            UNION
            SELECT member3_name FROM projects WHERE course_code = %s AND member3_name IS NOT NULL
            UNION
            SELECT member4_name FROM projects WHERE course_code = %s AND member4_name IS NOT NULL
            UNION
            SELECT member5_name FROM projects WHERE course_code = %s AND member5_name IS NOT NULL
            ORDER BY name
        """
        
        students = self.db.fetch_all(query, (course['code'],) * 5)
        
        if not students:
            # 기본 명단 생성 (과정 정원만큼)
            students = [{'name': f'학생 {i}'} for i in range(1, min(course['capacity'] + 1, 31))]
        
        # 시간표에서 날짜 목록 조회
        date_query = """
            SELECT DISTINCT class_date 
            FROM timetables 
            WHERE course_code = %s 
            ORDER BY class_date 
            LIMIT 20
        """
        
        date_rows = self.db.fetch_all(date_query, (course['code'],))
        
        if date_rows:
            dates = [row['class_date'] for row in date_rows]
        else:
            # 기본 날짜 생성 (오늘부터 20일)
            dates = [(datetime.now() + timedelta(days=i)).date() for i in range(20)]
        
        # PDF 생성
        filename = self.pdf_gen.generate_attendance_sheet(course, students, dates, f"출석부_{course['name']}")
        
        return filename
    
    def generate_grade_report(self, course):
        """성적표 양식 생성"""
        # 학생 명단 조회 (출석부와 동일)
        query = """
            SELECT 
                member1_name as name FROM projects WHERE course_code = %s AND member1_name IS NOT NULL
            UNION
            SELECT member2_name FROM projects WHERE course_code = %s AND member2_name IS NOT NULL
            UNION
            SELECT member3_name FROM projects WHERE course_code = %s AND member3_name IS NOT NULL
            UNION
            SELECT member4_name FROM projects WHERE course_code = %s AND member4_name IS NOT NULL
            UNION
            SELECT member5_name FROM projects WHERE course_code = %s AND member5_name IS NOT NULL
            ORDER BY name
        """
        
        students = self.db.fetch_all(query, (course['code'],) * 5)
        
        if not students:
            students = [{'name': f'학생 {i}'} for i in range(1, min(course['capacity'] + 1, 31))]
        
        # 교과목 목록 조회
        subject_query = "SELECT code, name FROM subjects ORDER BY code LIMIT 10"
        subjects = self.db.fetch_all(subject_query)
        
        if not subjects:
            subjects = [{'name': f'과목{i}'} for i in range(1, 6)]
        
        # PDF 생성
        filename = self.pdf_gen.generate_grade_sheet(course, students, subjects, f"성적표_{course['name']}")
        
        return filename
    
    def closeEvent(self, event):
        """닫기 이벤트"""
        self.db.disconnect()
        event.accept()
