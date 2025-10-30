# -*- coding: utf-8 -*-
"""
강사 코드 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QComboBox, QMessageBox, QHeaderView, QGroupBox)
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager


class InstructorCodeDialog(QWidget):
    """강사 코드 관리 위젯 (탭용)"""
    
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
        form_group = QGroupBox("강사 코드 등록")
        form_layout = QHBoxLayout()
        
        # 코드
        form_layout.addWidget(QLabel("코드:"))
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("자동 생성")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(100)
        form_layout.addWidget(self.code_input)
        
        # 강사명칭
        form_layout.addWidget(QLabel("강사명칭:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 주강사")
        form_layout.addWidget(self.name_input)
        
        # 구분
        form_layout.addWidget(QLabel("구분:"))
        self.type_combo = QComboBox()
        self.type_combo.addItems(["1. 주강사", "2. 보조강사", "3. 멘토", "4. 기타", "5. 외부강사", "6. 인턴", "7. 방문강사", "8. 온라인강사", "9. 특별강사", "10. 객원강사"])
        form_layout.addWidget(self.type_combo)
        
        # 버튼
        self.add_btn = QPushButton("추가")
        self.add_btn.clicked.connect(self.add_code)
        form_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.clicked.connect(self.update_code)
        form_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_code)
        form_layout.addWidget(self.delete_btn)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["코드", "강사명칭", "구분"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼 (탭으로 사용되므로 닫기 버튼 불필요)
        
        self.setLayout(layout)
        
    def load_data(self):
        """데이터 로드"""
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        try:
            query = "SELECT * FROM instructor_codes ORDER BY code"
            rows = self.db.fetch_all(query)
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                type_text = {"1": "1. 주강사", "2": "2. 보조강사", "3": "3. 멘토"}
                
                self.table.setItem(row_position, 0, QTableWidgetItem(row['code']))
                self.table.setItem(row_position, 1, QTableWidgetItem(row['name']))
                self.table.setItem(row_position, 2, QTableWidgetItem(type_text.get(row['type'], row['type'])))
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 로드 실패: {str(e)}")
        
    def on_row_selected(self, row, column):
        """행 선택 시"""
        code = self.table.item(row, 0).text()
        name = self.table.item(row, 1).text()
        type_text = self.table.item(row, 2).text()
        
        self.code_input.setText(code)
        self.name_input.setText(name)
        
        # 구분 선택
        for i in range(self.type_combo.count()):
            if self.type_combo.itemText(i) == type_text:
                self.type_combo.setCurrentIndex(i)
                break
        
    def add_code(self):
        """코드 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "강사명칭을 입력하세요.")
            return
        
        type_value = str(self.type_combo.currentIndex() + 1)
        
        try:
            # 다음 코드 생성
            code = self.db.get_next_code('instructor_codes', 'IC-')
            
            query = """
                INSERT INTO instructor_codes (code, name, type) 
                VALUES (%s, %s, %s)
            """
            self.db.execute_query(query, (code, name, type_value))
            
            QMessageBox.information(self, "성공", f"강사 코드 {code}가 추가되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")
    
    def update_code(self):
        """코드 수정"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "경고", "코드와 강사명칭을 입력하세요.")
            return
        
        type_value = str(self.type_combo.currentIndex() + 1)
        
        try:
            query = """
                UPDATE instructor_codes 
                SET name = %s, type = %s 
                WHERE code = %s
            """
            self.db.execute_query(query, (name, type_value, code))
            
            QMessageBox.information(self, "성공", "강사 코드가 수정되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")
    
    def delete_code(self):
        """코드 삭제"""
        code = self.code_input.text().strip()
        
        if not code:
            QMessageBox.warning(self, "경고", "삭제할 코드를 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"코드 {code}를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM instructor_codes WHERE code = %s"
                self.db.execute_query(query, (code,))
                
                QMessageBox.information(self, "성공", "강사 코드가 삭제되었습니다.")
                self.clear_form()
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def clear_form(self):
        """폼 초기화"""
        self.code_input.clear()
        self.name_input.clear()
        self.type_combo.setCurrentIndex(0)
