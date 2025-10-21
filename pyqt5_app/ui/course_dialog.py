# -*- coding: utf-8 -*-
"""
과정 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QGroupBox, QGridLayout,
                             QSpinBox, QTextEdit)
from PyQt5.QtCore import Qt
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
        
        # 입력 폼
        form_group = QGroupBox("과정 정보 등록")
        form_layout = QGridLayout()
        
        # 코드
        form_layout.addWidget(QLabel("코드:"), 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("C-001 (자동 생성)")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(150)
        form_layout.addWidget(self.code_input, 0, 1)
        
        # 반명칭
        form_layout.addWidget(QLabel("반명칭:"), 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 1반")
        form_layout.addWidget(self.name_input, 0, 3)
        
        # 강의 시수
        form_layout.addWidget(QLabel("강의 시수:"), 1, 0)
        self.lecture_hours = QSpinBox()
        self.lecture_hours.setRange(0, 9999)
        self.lecture_hours.setValue(480)
        self.lecture_hours.setSuffix(" 시간")
        form_layout.addWidget(self.lecture_hours, 1, 1)
        
        # 프로젝트 시수
        form_layout.addWidget(QLabel("프로젝트 시수:"), 1, 2)
        self.project_hours = QSpinBox()
        self.project_hours.setRange(0, 9999)
        self.project_hours.setValue(120)
        self.project_hours.setSuffix(" 시간")
        form_layout.addWidget(self.project_hours, 1, 3)
        
        # 인턴쉽 시수
        form_layout.addWidget(QLabel("인턴쉽 시수:"), 2, 0)
        self.internship_hours = QSpinBox()
        self.internship_hours.setRange(0, 9999)
        self.internship_hours.setValue(0)
        self.internship_hours.setSuffix(" 시간")
        form_layout.addWidget(self.internship_hours, 2, 1)
        
        # 인원수
        form_layout.addWidget(QLabel("인원수:"), 2, 2)
        self.capacity = QSpinBox()
        self.capacity.setRange(1, 999)
        self.capacity.setValue(30)
        self.capacity.setSuffix(" 명")
        form_layout.addWidget(self.capacity, 2, 3)
        
        # 강의장소
        form_layout.addWidget(QLabel("강의장소:"), 3, 0)
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("예: 본관 101호")
        form_layout.addWidget(self.location_input, 3, 1, 1, 3)
        
        # 특이사항
        form_layout.addWidget(QLabel("특이사항:"), 4, 0)
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("과정 관련 특이사항을 입력하세요")
        self.notes_input.setMaximumHeight(80)
        form_layout.addWidget(self.notes_input, 4, 1, 1, 3)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 버튼 그룹
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px;")
        self.add_btn.clicked.connect(self.add_course)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px;")
        self.update_btn.clicked.connect(self.update_course)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px;")
        self.delete_btn.clicked.connect(self.delete_course)
        btn_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "코드", "반명칭", "강의시수", "프로젝트시수", 
            "인턴쉽시수", "인원수", "강의장소", "특이사항"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼
        # 하단 버튼 (탭으로 사용되므로 닫기 버튼 불필요)
        
        self.setLayout(layout)
        
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
                self.table.setItem(row_position, 2, QTableWidgetItem(str(row['lecture_hours'])))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(row['project_hours'])))
                self.table.setItem(row_position, 4, QTableWidgetItem(str(row['internship_hours'])))
                self.table.setItem(row_position, 5, QTableWidgetItem(str(row['capacity'])))
                self.table.setItem(row_position, 6, QTableWidgetItem(row['location'] or ''))
                notes = row['notes'] or ''
                self.table.setItem(row_position, 7, QTableWidgetItem(notes[:50] + '...' if len(notes) > 50 else notes))
                
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
            self.lecture_hours.setValue(result['lecture_hours'])
            self.project_hours.setValue(result['project_hours'])
            self.internship_hours.setValue(result['internship_hours'])
            self.capacity.setValue(result['capacity'])
            self.location_input.setText(result['location'] or '')
            self.notes_input.setText(result['notes'] or '')
        
    def add_course(self):
        """과정 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "반명칭을 입력하세요.")
            return
        
        lecture_hrs = self.lecture_hours.value()
        project_hrs = self.project_hours.value()
        internship_hrs = self.internship_hours.value()
        cap = self.capacity.value()
        location = self.location_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        try:
            code = self.db.get_next_code('courses', CODE_PREFIX['course'])
            
            query = """
                INSERT INTO courses (code, name, lecture_hours, project_hours, internship_hours, capacity, location, notes) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (code, name, lecture_hrs, project_hrs, internship_hrs, cap, location, notes))
            
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
        
        lecture_hrs = self.lecture_hours.value()
        project_hrs = self.project_hours.value()
        internship_hrs = self.internship_hours.value()
        cap = self.capacity.value()
        location = self.location_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        try:
            query = """
                UPDATE courses 
                SET name = %s, lecture_hours = %s, project_hours = %s, 
                    internship_hours = %s, capacity = %s, location = %s, notes = %s 
                WHERE code = %s
            """
            self.db.execute_query(query, (name, lecture_hrs, project_hrs, internship_hrs, cap, location, notes, code))
            
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
        self.lecture_hours.setValue(480)
        self.project_hours.setValue(120)
        self.internship_hours.setValue(0)
        self.capacity.setValue(30)
        self.location_input.clear()
        self.notes_input.clear()
    

