# -*- coding: utf-8 -*-
"""
교과목 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QComboBox, QMessageBox, QHeaderView, QGroupBox,
                             QGridLayout, QSpinBox)
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from config_db import CODE_PREFIX


class SubjectDialog(QWidget):
    """교과목 관리 위젯 (탭용)"""
    
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
        form_group = QGroupBox("교과목 정보 등록")
        form_layout = QGridLayout()
        
        # 코드
        form_layout.addWidget(QLabel("코드:"), 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("G-001 (자동 생성)")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(150)
        form_layout.addWidget(self.code_input, 0, 1)
        
        # 과목명
        form_layout.addWidget(QLabel("과목명:"), 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Python 프로그래밍")
        form_layout.addWidget(self.name_input, 0, 3)
        
        # 수업시수
        form_layout.addWidget(QLabel("수업시수:"), 0, 4)
        self.hours_input = QSpinBox()
        self.hours_input.setRange(1, 999)
        self.hours_input.setValue(40)
        self.hours_input.setSuffix(" 시간")
        form_layout.addWidget(self.hours_input, 0, 5)
        
        # 주강사
        form_layout.addWidget(QLabel("주강사:"), 1, 0)
        self.main_combo = QComboBox()
        self.main_combo.setMinimumWidth(200)
        self.main_combo.setStyleSheet("QComboBox { font-family: 'Courier New', monospace; }")
        form_layout.addWidget(self.main_combo, 1, 1)
        
        # 보조강사
        form_layout.addWidget(QLabel("보조강사:"), 1, 2)
        self.assistant_combo = QComboBox()
        self.assistant_combo.setMinimumWidth(200)
        self.assistant_combo.setStyleSheet("QComboBox { font-family: 'Courier New', monospace; }")
        form_layout.addWidget(self.assistant_combo, 1, 3)
        
        # 예비강사
        form_layout.addWidget(QLabel("예비강사:"), 1, 4)
        self.reserve_combo = QComboBox()
        self.reserve_combo.setMinimumWidth(200)
        self.reserve_combo.setStyleSheet("QComboBox { font-family: 'Courier New', monospace; }")
        form_layout.addWidget(self.reserve_combo, 1, 5)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 버튼 그룹
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px;")
        self.add_btn.clicked.connect(self.add_subject)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px;")
        self.update_btn.clicked.connect(self.update_subject)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px;")
        self.delete_btn.clicked.connect(self.delete_subject)
        btn_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["코드", "과목명", "수업시수", "주강사", "보조강사", "예비강사"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼
        # 하단 버튼 (탭으로 사용되므로 닫기 버튼 불필요)
        
        self.setLayout(layout)
        
        # 강사 목록 로드
        self.load_instructors()
        
    def load_instructors(self):
        """강사 목록 로드 - 유형별 필터링"""
        if not self.db.connect():
            return
        
        try:
            # 주강사용: type='1' (주강사)만
            query_main = """
                SELECT i.code, i.name, ic.type
                FROM instructors i
                LEFT JOIN instructor_codes ic ON i.instructor_type = ic.code
                WHERE ic.type = '1'
                ORDER BY i.code
            """
            main_rows = self.db.fetch_all(query_main)
            
            # 보조강사용: type='2' (보조강사)만
            query_assistant = """
                SELECT i.code, i.name, ic.type
                FROM instructors i
                LEFT JOIN instructor_codes ic ON i.instructor_type = ic.code
                WHERE ic.type = '2'
                ORDER BY i.code
            """
            assistant_rows = self.db.fetch_all(query_assistant)
            
            # 예비강사용: type='1' (주강사) OR type='3' (멘토)
            query_reserve = """
                SELECT i.code, i.name, ic.type
                FROM instructors i
                LEFT JOIN instructor_codes ic ON i.instructor_type = ic.code
                WHERE ic.type IN ('1', '3')
                ORDER BY i.code
            """
            reserve_rows = self.db.fetch_all(query_reserve)
            
            # 주강사 콤보박스
            self.main_combo.clear()
            self.main_combo.addItem("선택 안함", None)
            for row in main_rows:
                # 이름을 10자로 맞춰서 정렬
                name_padded = row['name'].ljust(10)
                display_text = f"{name_padded} - 주강사"
                self.main_combo.addItem(display_text, row['code'])
            
            # 보조강사 콤보박스
            self.assistant_combo.clear()
            self.assistant_combo.addItem("선택 안함", None)
            for row in assistant_rows:
                # 이름을 10자로 맞춰서 정렬
                name_padded = row['name'].ljust(10)
                display_text = f"{name_padded} - 보조강사"
                self.assistant_combo.addItem(display_text, row['code'])
            
            # 예비강사 콤보박스
            self.reserve_combo.clear()
            self.reserve_combo.addItem("선택 안함", None)
            for row in reserve_rows:
                # 이름을 10자로 맞춰서 정렬
                name_padded = row['name'].ljust(10)
                # type에 따라 역할 표시
                role = "주강사" if row['type'] == '1' else "멘토"
                display_text = f"{name_padded} - {role}"
                self.reserve_combo.addItem(display_text, row['code'])
                
        except Exception as e:
            print(f"강사 목록 로드 오류: {str(e)}")
        
    def load_data(self):
        """데이터 로드"""
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        try:
            query = """
                SELECT s.*, 
                       i1.name as main_name,
                       i2.name as assistant_name,
                       i3.name as reserve_name
                FROM subjects s
                LEFT JOIN instructors i1 ON s.main_instructor = i1.code
                LEFT JOIN instructors i2 ON s.assistant_instructor = i2.code
                LEFT JOIN instructors i3 ON s.reserve_instructor = i3.code
                ORDER BY s.code
            """
            rows = self.db.fetch_all(query)
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                self.table.setItem(row_position, 0, QTableWidgetItem(row['code'] or ''))
                self.table.setItem(row_position, 1, QTableWidgetItem(row['name'] or ''))
                self.table.setItem(row_position, 2, QTableWidgetItem(str(row['hours']) + ' 시간'))
                
                # 강사 이름 뒤에 구분 추가
                main_name = f"{row['main_name']}-주강사" if row['main_name'] else '-'
                assistant_name = f"{row['assistant_name']}-보조강사" if row['assistant_name'] else '-'
                reserve_name = f"{row['reserve_name']}-예비강사" if row['reserve_name'] else '-'
                
                self.table.setItem(row_position, 3, QTableWidgetItem(main_name))
                self.table.setItem(row_position, 4, QTableWidgetItem(assistant_name))
                self.table.setItem(row_position, 5, QTableWidgetItem(reserve_name))
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 로드 실패: {str(e)}")
        
    def on_row_selected(self, row, column):
        """행 선택 시"""
        self.code_input.setText(self.table.item(row, 0).text())
        self.name_input.setText(self.table.item(row, 1).text())
        hours_text = self.table.item(row, 2).text().replace(' 시간', '')
        self.hours_input.setValue(int(hours_text))
        
        # 강사 찾기 - 실제 DB에서 다시 조회
        code = self.table.item(row, 0).text()
        query = "SELECT * FROM subjects WHERE code = %s"
        result = self.db.fetch_one(query, (code,))
        
        if result:
            self.set_combo_by_code(self.main_combo, result['main_instructor'])
            self.set_combo_by_code(self.assistant_combo, result['assistant_instructor'])
            self.set_combo_by_code(self.reserve_combo, result['reserve_instructor'])
    
    def set_combo_by_code(self, combo, code):
        """콤보박스를 코드로 설정"""
        if not code:
            combo.setCurrentIndex(0)
            return
        
        for i in range(combo.count()):
            if combo.itemData(i) == code:
                combo.setCurrentIndex(i)
                break
        
    def add_subject(self):
        """교과목 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "과목명을 입력하세요.")
            return
        
        hours = self.hours_input.value()
        main_instructor = self.main_combo.currentData()
        assistant_instructor = self.assistant_combo.currentData()
        reserve_instructor = self.reserve_combo.currentData()
        
        try:
            code = self.db.get_next_code('subjects', CODE_PREFIX['subject'])
            
            query = """
                INSERT INTO subjects (code, name, hours, main_instructor, assistant_instructor, reserve_instructor) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.db.execute_query(query, (code, name, hours, main_instructor, assistant_instructor, reserve_instructor))
            
            QMessageBox.information(self, "성공", f"교과목 {code}가 추가되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")
    
    def update_subject(self):
        """교과목 수정"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "경고", "코드와 과목명을 입력하세요.")
            return
        
        hours = self.hours_input.value()
        main_instructor = self.main_combo.currentData()
        assistant_instructor = self.assistant_combo.currentData()
        reserve_instructor = self.reserve_combo.currentData()
        
        try:
            query = """
                UPDATE subjects 
                SET name = %s, hours = %s, main_instructor = %s, 
                    assistant_instructor = %s, reserve_instructor = %s 
                WHERE code = %s
            """
            self.db.execute_query(query, (name, hours, main_instructor, assistant_instructor, reserve_instructor, code))
            
            QMessageBox.information(self, "성공", "교과목이 수정되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")
    
    def delete_subject(self):
        """교과목 삭제"""
        code = self.code_input.text().strip()
        
        if not code:
            QMessageBox.warning(self, "경고", "삭제할 교과목을 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"교과목 {code}를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM subjects WHERE code = %s"
                self.db.execute_query(query, (code,))
                
                QMessageBox.information(self, "성공", "교과목이 삭제되었습니다.")
                self.clear_form()
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def clear_form(self):
        """폼 초기화"""
        self.code_input.clear()
        self.name_input.clear()
        self.hours_input.setValue(40)
        self.main_combo.setCurrentIndex(0)
        self.assistant_combo.setCurrentIndex(0)
        self.reserve_combo.setCurrentIndex(0)

