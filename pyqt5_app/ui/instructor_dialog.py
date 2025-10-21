# -*- coding: utf-8 -*-
"""
강사 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QComboBox, QMessageBox, QHeaderView, QGroupBox,
                             QGridLayout)
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from config_db import CODE_PREFIX


class InstructorDialog(QWidget):
    """강사 관리 위젯 (탭용)"""
    
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
        form_group = QGroupBox("강사 정보 등록")
        form_layout = QGridLayout()
        
        # 코드
        form_layout.addWidget(QLabel("코드:"), 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("T-001 (자동 생성)")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(150)
        form_layout.addWidget(self.code_input, 0, 1)
        
        # 이름
        form_layout.addWidget(QLabel("이름:"), 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("홍길동")
        form_layout.addWidget(self.name_input, 0, 3)
        
        # 연락처
        form_layout.addWidget(QLabel("연락처:"), 0, 4)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("010-1234-5678")
        form_layout.addWidget(self.phone_input, 0, 5)
        
        # 전공
        form_layout.addWidget(QLabel("전공:"), 1, 0)
        self.major_input = QLineEdit()
        self.major_input.setPlaceholderText("컴퓨터공학")
        form_layout.addWidget(self.major_input, 1, 1)
        
        # 강사 구분
        form_layout.addWidget(QLabel("강사 구분:"), 1, 2)
        self.type_combo = QComboBox()
        self.type_combo.setMinimumWidth(150)
        form_layout.addWidget(self.type_combo, 1, 3)
        
        # 이메일
        form_layout.addWidget(QLabel("이메일:"), 1, 4)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("example@email.com")
        form_layout.addWidget(self.email_input, 1, 5)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 버튼 그룹
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px;")
        self.add_btn.clicked.connect(self.add_instructor)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px;")
        self.update_btn.clicked.connect(self.update_instructor)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px;")
        self.delete_btn.clicked.connect(self.delete_instructor)
        btn_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["코드", "이름", "연락처", "전공", "강사구분", "이메일"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼
        # 하단 버튼 (탭으로 사용되므로 닫기 버튼 불필요)
        
        self.setLayout(layout)
        
        # 강사 구분 로드
        self.load_instructor_types()
        
    def load_instructor_types(self):
        """강사 구분 콤보박스 로드"""
        if not self.db.connect():
            return
        
        try:
            query = "SELECT code, name, type FROM instructor_codes ORDER BY type, code"
            rows = self.db.fetch_all(query)
            
            self.type_combo.clear()
            for row in rows:
                type_text = {"1": "주강사", "2": "보조강사", "3": "멘토"}
                display_text = f"{row['name']} ({type_text.get(row['type'], '')})"
                self.type_combo.addItem(display_text, row['code'])
                
        except Exception as e:
            print(f"강사 구분 로드 오류: {str(e)}")
        
    def load_data(self):
        """데이터 로드"""
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        try:
            query = """
                SELECT i.*, ic.name as type_name 
                FROM instructors i
                LEFT JOIN instructor_codes ic ON i.instructor_type = ic.code
                ORDER BY i.code
            """
            rows = self.db.fetch_all(query)
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                self.table.setItem(row_position, 0, QTableWidgetItem(row['code'] or ''))
                self.table.setItem(row_position, 1, QTableWidgetItem(row['name'] or ''))
                self.table.setItem(row_position, 2, QTableWidgetItem(row['phone'] or ''))
                self.table.setItem(row_position, 3, QTableWidgetItem(row['major'] or ''))
                self.table.setItem(row_position, 4, QTableWidgetItem(row['type_name'] or ''))
                self.table.setItem(row_position, 5, QTableWidgetItem(row['email'] or ''))
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 로드 실패: {str(e)}")
        
    def on_row_selected(self, row, column):
        """행 선택 시"""
        self.code_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        self.phone_input.setText(self.table.item(row, 2).text())
        self.major_input.setText(self.table.item(row, 3).text())
        self.email_input.setText(self.table.item(row, 5).text())
        
        # 강사 구분 찾기
        type_name = self.table.item(row, 4).text()
        for i in range(self.type_combo.count()):
            if type_name in self.type_combo.itemText(i):
                self.type_combo.setCurrentIndex(i)
                break
        
    def add_instructor(self):
        """강사 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "이름을 입력하세요.")
            return
        
        phone = self.phone_input.text().strip()
        major = self.major_input.text().strip()
        email = self.email_input.text().strip()
        instructor_type = self.type_combo.currentData()
        
        if not instructor_type:
            QMessageBox.warning(self, "경고", "강사 구분을 선택하세요.")
            return
        
        try:
            # 다음 코드 생성
            code = self.db.get_next_code('instructors', CODE_PREFIX['instructor'])
            
            query = """
                INSERT INTO instructors (code, name, phone, major, instructor_type, email) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (code, name, phone, major, instructor_type, email))
            
            QMessageBox.information(self, "성공", f"강사 {code}가 추가되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")
    
    def update_instructor(self):
        """강사 수정"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "경고", "코드와 이름을 입력하세요.")
            return
        
        phone = self.phone_input.text().strip()
        major = self.major_input.text().strip()
        email = self.email_input.text().strip()
        instructor_type = self.type_combo.currentData()
        
        try:
            query = """
                UPDATE instructors 
                SET name = %s, phone = %s, major = %s, instructor_type = %s, email = %s 
                WHERE code = %s
            """
            self.db.execute_query(query, (name, phone, major, instructor_type, email, code))
            
            QMessageBox.information(self, "성공", "강사 정보가 수정되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")
    
    def delete_instructor(self):
        """강사 삭제"""
        code = self.code_input.text().strip()
        
        if not code:
            QMessageBox.warning(self, "경고", "삭제할 강사를 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"강사 {code}를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM instructors WHERE code = %s"
                self.db.execute_query(query, (code,))
                
                QMessageBox.information(self, "성공", "강사가 삭제되었습니다.")
                self.clear_form()
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def clear_form(self):
        """폼 초기화"""
        self.code_input.clear()
        self.name_input.clear()
        self.phone_input.clear()
        self.major_input.clear()
        self.email_input.clear()
        self.type_combo.setCurrentIndex(0)

