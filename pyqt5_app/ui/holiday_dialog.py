# -*- coding: utf-8 -*-
"""
공휴일 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QGroupBox, QDateEdit,
                             QCheckBox, QGridLayout)
from PyQt5.QtCore import Qt, QDate
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager


class HolidayDialog(QDialog):
    """공휴일 관리 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("공휴일 관리")
        self.setGeometry(200, 200, 900, 600)
        
        layout = QVBoxLayout()
        
        # 입력 폼
        form_group = QGroupBox("공휴일 등록")
        form_layout = QGridLayout()
        
        # 날짜
        form_layout.addWidget(QLabel("날짜:"), 0, 0)
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.date_input.setDisplayFormat("yyyy-MM-dd")
        form_layout.addWidget(self.date_input, 0, 1)
        
        # 공휴일명
        form_layout.addWidget(QLabel("공휴일명:"), 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: 설날")
        form_layout.addWidget(self.name_input, 0, 3)
        
        # 법정공휴일 체크박스
        self.legal_checkbox = QCheckBox("법정공휴일")
        form_layout.addWidget(self.legal_checkbox, 0, 4)
        
        form_group.setLayout(form_layout)
        layout.addWidget(form_group)
        
        # 버튼 그룹
        btn_layout = QHBoxLayout()
        
        self.auto_btn = QPushButton("법정공휴일 자동 입력")
        self.auto_btn.setStyleSheet("background-color: #9C27B0; color: white; padding: 8px 20px;")
        self.auto_btn.clicked.connect(self.auto_insert_holidays)
        btn_layout.addWidget(self.auto_btn)
        
        btn_layout.addStretch()
        
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px;")
        self.add_btn.clicked.connect(self.add_holiday)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px;")
        self.update_btn.clicked.connect(self.update_holiday)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px;")
        self.delete_btn.clicked.connect(self.delete_holiday)
        btn_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "날짜", "공휴일명", "법정공휴일"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        self.table.setColumnWidth(0, 50)
        layout.addWidget(self.table)
        
        # 하단 버튼
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        bottom_layout.addWidget(close_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        
    def auto_insert_holidays(self):
        """법정공휴일 자동 입력"""
        reply = QMessageBox.question(self, "확인", 
                                     "2025년 법정공휴일을 자동으로 입력하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                # 2025년 한국 법정공휴일
                holidays = [
                    ('2025-01-01', '신정', True),
                    ('2025-01-28', '설날 연휴', True),
                    ('2025-01-29', '설날', True),
                    ('2025-01-30', '설날 연휴', True),
                    ('2025-03-01', '삼일절', True),
                    ('2025-03-03', '대체공휴일(삼일절)', True),
                    ('2025-05-05', '어린이날', True),
                    ('2025-05-06', '대체공휴일(어린이날)', True),
                    ('2025-06-06', '현충일', True),
                    ('2025-08-15', '광복절', True),
                    ('2025-10-03', '개천절', True),
                    ('2025-10-05', '추석 연휴', True),
                    ('2025-10-06', '추석', True),
                    ('2025-10-07', '추석 연휴', True),
                    ('2025-10-08', '대체공휴일(추석)', True),
                    ('2025-10-09', '한글날', True),
                    ('2025-12-25', '성탄절', True),
                ]
                
                inserted = 0
                for date, name, is_legal in holidays:
                    query = """
                        INSERT IGNORE INTO holidays (holiday_date, name, is_legal) 
                        VALUES (%s, %s, %s)
                    """
                    if self.db.execute_query(query, (date, name, is_legal)):
                        inserted += 1
                
                QMessageBox.information(self, "성공", f"{inserted}개의 법정공휴일이 입력되었습니다.")
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"자동 입력 실패: {str(e)}")
        
    def load_data(self):
        """데이터 로드"""
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        try:
            query = "SELECT * FROM holidays ORDER BY holiday_date"
            rows = self.db.fetch_all(query)
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                self.table.setItem(row_position, 0, QTableWidgetItem(str(row['id'])))
                self.table.setItem(row_position, 1, QTableWidgetItem(str(row['holiday_date'])))
                self.table.setItem(row_position, 2, QTableWidgetItem(row['name']))
                legal_text = "법정" if row['is_legal'] else "수동"
                self.table.setItem(row_position, 3, QTableWidgetItem(legal_text))
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 로드 실패: {str(e)}")
        
    def on_row_selected(self, row, column):
        """행 선택 시"""
        date_str = self.table.item(row, 1).text()
        name = self.table.item(row, 2).text()
        is_legal = self.table.item(row, 3).text() == "법정"
        
        self.date_input.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        self.name_input.setText(name)
        self.legal_checkbox.setChecked(is_legal)
        
    def add_holiday(self):
        """공휴일 추가"""
        date = self.date_input.date().toString("yyyy-MM-dd")
        name = self.name_input.text().strip()
        
        if not name:
            QMessageBox.warning(self, "경고", "공휴일명을 입력하세요.")
            return
        
        is_legal = self.legal_checkbox.isChecked()
        
        try:
            query = """
                INSERT INTO holidays (holiday_date, name, is_legal) 
                VALUES (%s, %s, %s)
            """
            self.db.execute_query(query, (date, name, is_legal))
            
            QMessageBox.information(self, "성공", "공휴일이 추가되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")
    
    def update_holiday(self):
        """공휴일 수정"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "경고", "수정할 공휴일을 선택하세요.")
            return
        
        holiday_id = int(self.table.item(selected_row, 0).text())
        date = self.date_input.date().toString("yyyy-MM-dd")
        name = self.name_input.text().strip()
        is_legal = self.legal_checkbox.isChecked()
        
        if not name:
            QMessageBox.warning(self, "경고", "공휴일명을 입력하세요.")
            return
        
        try:
            query = """
                UPDATE holidays 
                SET holiday_date = %s, name = %s, is_legal = %s 
                WHERE id = %s
            """
            self.db.execute_query(query, (date, name, is_legal, holiday_id))
            
            QMessageBox.information(self, "성공", "공휴일이 수정되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")
    
    def delete_holiday(self):
        """공휴일 삭제"""
        selected_row = self.table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 공휴일을 선택하세요.")
            return
        
        holiday_id = int(self.table.item(selected_row, 0).text())
        name = self.table.item(selected_row, 2).text()
        
        reply = QMessageBox.question(self, "확인", 
                                     f"공휴일 '{name}'을(를) 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM holidays WHERE id = %s"
                self.db.execute_query(query, (holiday_id,))
                
                QMessageBox.information(self, "성공", "공휴일이 삭제되었습니다.")
                self.clear_form()
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def clear_form(self):
        """폼 초기화"""
        self.date_input.setDate(QDate.currentDate())
        self.name_input.clear()
        self.legal_checkbox.setChecked(False)
    
    def closeEvent(self, event):
        """닫기 이벤트"""
        self.db.disconnect()
        event.accept()
