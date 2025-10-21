# -*- coding: utf-8 -*-
"""
프로젝트 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                             QTableWidget, QTableWidgetItem, QLineEdit, QLabel,
                             QMessageBox, QHeaderView, QGroupBox, QGridLayout,
                             QComboBox, QScrollArea, QWidget)
from PyQt5.QtCore import Qt
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from config_db import CODE_PREFIX


class ProjectDialog(QDialog):
    """프로젝트 관리 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = DatabaseManager()
        self.init_ui()
        self.load_data()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("프로젝트 관리")
        self.setGeometry(100, 100, 1200, 800)
        
        layout = QVBoxLayout()
        
        # 스크롤 영역
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        
        # 입력 폼
        form_group = QGroupBox("프로젝트 정보 등록")
        form_layout = QGridLayout()
        
        # 코드
        form_layout.addWidget(QLabel("코드:"), 0, 0)
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("P-001 (자동 생성)")
        self.code_input.setReadOnly(True)
        self.code_input.setMaximumWidth(150)
        form_layout.addWidget(self.code_input, 0, 1)
        
        # 프로젝트명
        form_layout.addWidget(QLabel("프로젝트명:"), 0, 2)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("예: AI 챗봇 개발")
        form_layout.addWidget(self.name_input, 0, 3, 1, 3)
        
        # 과정
        form_layout.addWidget(QLabel("과정:"), 1, 0)
        self.course_combo = QComboBox()
        self.course_combo.setMinimumWidth(200)
        form_layout.addWidget(self.course_combo, 1, 1, 1, 2)
        
        # 구성원 입력 필드
        self.member_inputs = []
        self.phone_inputs = []
        
        for i in range(5):
            row = 2 + i
            # 구성원 이름
            form_layout.addWidget(QLabel(f"구성원 {i+1}:"), row, 0)
            member_input = QLineEdit()
            member_input.setPlaceholderText(f"이름 {i+1}")
            form_layout.addWidget(member_input, row, 1)
            self.member_inputs.append(member_input)
            
            # 연락처
            form_layout.addWidget(QLabel(f"연락처 {i+1}:"), row, 2)
            phone_input = QLineEdit()
            phone_input.setPlaceholderText("010-0000-0000")
            form_layout.addWidget(phone_input, row, 3)
            self.phone_inputs.append(phone_input)
        
        form_group.setLayout(form_layout)
        scroll_layout.addWidget(form_group)
        
        scroll_widget.setLayout(scroll_layout)
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # 버튼 그룹
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        
        self.add_btn = QPushButton("추가")
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px 20px;")
        self.add_btn.clicked.connect(self.add_project)
        btn_layout.addWidget(self.add_btn)
        
        self.update_btn = QPushButton("수정")
        self.update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px 20px;")
        self.update_btn.clicked.connect(self.update_project)
        btn_layout.addWidget(self.update_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px 20px;")
        self.delete_btn.clicked.connect(self.delete_project)
        btn_layout.addWidget(self.delete_btn)
        
        self.clear_btn = QPushButton("초기화")
        self.clear_btn.clicked.connect(self.clear_form)
        btn_layout.addWidget(self.clear_btn)
        
        layout.addLayout(btn_layout)
        
        # 테이블
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "코드", "프로젝트명", "과정", "구성원1", "구성원2", "구성원3", "구성원4/5"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.cellClicked.connect(self.on_row_selected)
        layout.addWidget(self.table)
        
        # 하단 버튼
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        
        close_btn = QPushButton("닫기")
        close_btn.clicked.connect(self.close)
        bottom_layout.addWidget(close_btn)
        
        layout.addLayout(bottom_layout)
        
        self.setLayout(layout)
        
        # 과정 목록 로드
        self.load_courses()
        
    def load_courses(self):
        """과정 목록 로드"""
        if not self.db.connect():
            return
        
        try:
            query = "SELECT code, name FROM courses ORDER BY code"
            rows = self.db.fetch_all(query)
            
            self.course_combo.clear()
            self.course_combo.addItem("선택 안함", None)
            
            for row in rows:
                display_text = f"{row['name']} ({row['code']})"
                self.course_combo.addItem(display_text, row['code'])
                
        except Exception as e:
            print(f"과정 목록 로드 오류: {str(e)}")
        
    def load_data(self):
        """데이터 로드"""
        if not self.db.connect():
            QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
            return
        
        try:
            query = """
                SELECT p.*, c.name as course_name
                FROM projects p
                LEFT JOIN courses c ON p.course_code = c.code
                ORDER BY p.code
            """
            rows = self.db.fetch_all(query)
            
            self.table.setRowCount(0)
            for row in rows:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                
                self.table.setItem(row_position, 0, QTableWidgetItem(row['code'] or ''))
                self.table.setItem(row_position, 1, QTableWidgetItem(row['name'] or ''))
                self.table.setItem(row_position, 2, QTableWidgetItem(row['course_name'] or '-'))
                self.table.setItem(row_position, 3, QTableWidgetItem(row['member1_name'] or ''))
                self.table.setItem(row_position, 4, QTableWidgetItem(row['member2_name'] or ''))
                self.table.setItem(row_position, 5, QTableWidgetItem(row['member3_name'] or ''))
                
                # 구성원 4, 5
                members_45 = []
                if row['member4_name']:
                    members_45.append(row['member4_name'])
                if row['member5_name']:
                    members_45.append(row['member5_name'])
                self.table.setItem(row_position, 6, QTableWidgetItem(', '.join(members_45)))
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"데이터 로드 실패: {str(e)}")
        
    def on_row_selected(self, row, column):
        """행 선택 시"""
        code = self.table.item(row, 0).text()
        
        # DB에서 전체 데이터 조회
        query = "SELECT * FROM projects WHERE code = %s"
        result = self.db.fetch_one(query, (code,))
        
        if result:
            self.code_input.setText(result['code'])
            self.name_input.setText(result['name'])
            
            # 과정 찾기
            course_code = result['course_code']
            for i in range(self.course_combo.count()):
                if self.course_combo.itemData(i) == course_code:
                    self.course_combo.setCurrentIndex(i)
                    break
            
            # 구성원 정보
            for i in range(5):
                member_name = result.get(f'member{i+1}_name') or ''
                member_phone = result.get(f'member{i+1}_phone') or ''
                self.member_inputs[i].setText(member_name)
                self.phone_inputs[i].setText(member_phone)
        
    def add_project(self):
        """프로젝트 추가"""
        name = self.name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "경고", "프로젝트명을 입력하세요.")
            return
        
        course_code = self.course_combo.currentData()
        
        # 구성원 정보 수집
        members = []
        for i in range(5):
            member_name = self.member_inputs[i].text().strip()
            member_phone = self.phone_inputs[i].text().strip()
            members.append((member_name, member_phone))
        
        try:
            code = self.db.get_next_code('projects', CODE_PREFIX['project'])
            
            query = """
                INSERT INTO projects (
                    code, name, course_code,
                    member1_name, member1_phone,
                    member2_name, member2_phone,
                    member3_name, member3_phone,
                    member4_name, member4_phone,
                    member5_name, member5_phone
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = [code, name, course_code]
            for member_name, member_phone in members:
                params.extend([member_name, member_phone])
            
            self.db.execute_query(query, tuple(params))
            
            QMessageBox.information(self, "성공", f"프로젝트 {code}가 추가되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"추가 실패: {str(e)}")
    
    def update_project(self):
        """프로젝트 수정"""
        code = self.code_input.text().strip()
        name = self.name_input.text().strip()
        
        if not code or not name:
            QMessageBox.warning(self, "경고", "코드와 프로젝트명을 입력하세요.")
            return
        
        course_code = self.course_combo.currentData()
        
        # 구성원 정보 수집
        members = []
        for i in range(5):
            member_name = self.member_inputs[i].text().strip()
            member_phone = self.phone_inputs[i].text().strip()
            members.append((member_name, member_phone))
        
        try:
            query = """
                UPDATE projects 
                SET name = %s, course_code = %s,
                    member1_name = %s, member1_phone = %s,
                    member2_name = %s, member2_phone = %s,
                    member3_name = %s, member3_phone = %s,
                    member4_name = %s, member4_phone = %s,
                    member5_name = %s, member5_phone = %s
                WHERE code = %s
            """
            
            params = [name, course_code]
            for member_name, member_phone in members:
                params.extend([member_name, member_phone])
            params.append(code)
            
            self.db.execute_query(query, tuple(params))
            
            QMessageBox.information(self, "성공", "프로젝트가 수정되었습니다.")
            self.clear_form()
            self.load_data()
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"수정 실패: {str(e)}")
    
    def delete_project(self):
        """프로젝트 삭제"""
        code = self.code_input.text().strip()
        
        if not code:
            QMessageBox.warning(self, "경고", "삭제할 프로젝트를 선택하세요.")
            return
        
        reply = QMessageBox.question(self, "확인", 
                                     f"프로젝트 {code}를 삭제하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                query = "DELETE FROM projects WHERE code = %s"
                self.db.execute_query(query, (code,))
                
                QMessageBox.information(self, "성공", "프로젝트가 삭제되었습니다.")
                self.clear_form()
                self.load_data()
                
            except Exception as e:
                QMessageBox.critical(self, "오류", f"삭제 실패: {str(e)}")
    
    def clear_form(self):
        """폼 초기화"""
        self.code_input.clear()
        self.name_input.clear()
        self.course_combo.setCurrentIndex(0)
        
        for i in range(5):
            self.member_inputs[i].clear()
            self.phone_inputs[i].clear()
    
    def closeEvent(self, event):
        """닫기 이벤트"""
        self.db.disconnect()
        event.accept()
