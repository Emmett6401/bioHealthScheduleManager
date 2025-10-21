# -*- coding: utf-8 -*-
"""
바이오헬스 올인원테크 이노베이터 for KDT - 메인 윈도우
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTextEdit,
                             QFrame, QScrollArea, QGridLayout, QDateEdit,
                             QTimeEdit, QGroupBox, QMenuBar, QAction, QToolBar,
                             QMessageBox, QTableWidget, QTableWidgetItem,
                             QHeaderView, QComboBox)
from PyQt5.QtCore import Qt, QDate, QTime
from PyQt5.QtGui import QFont, QIcon
import sys
import os


class CollapsibleSection(QWidget):
    """접을 수 있는 섹션 위젯"""
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.is_collapsed = False
        self.init_ui(title)
        
    def init_ui(self, title):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 헤더
        self.header = QPushButton(f"▼ {title}")
        self.header.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                border: 1px solid #ddd;
                text-align: left;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.header.clicked.connect(self.toggle_collapse)
        layout.addWidget(self.header)
        
        # 컨텐츠 컨테이너
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_widget.setLayout(self.content_layout)
        layout.addWidget(self.content_widget)
        
        self.setLayout(layout)
        
    def toggle_collapse(self):
        """섹션 접기/펼치기"""
        self.is_collapsed = not self.is_collapsed
        self.content_widget.setVisible(not self.is_collapsed)
        
        # 화살표 방향 변경
        title = self.header.text()[2:]  # "▼ " 제거
        if self.is_collapsed:
            self.header.setText(f"▶ {title}")
        else:
            self.header.setText(f"▼ {title}")
    
    def add_widget(self, widget):
        """컨텐츠에 위젯 추가"""
        self.content_layout.addWidget(widget)


class KDTMainWindow(QMainWindow):
    """KDT 메인 윈도우"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("바이오헬스 올인원테크 이노베이터 for KDT")
        self.setGeometry(100, 50, 1400, 900)
        
        # 메인 위젯
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 헤더
        header = self.create_header()
        main_layout.addWidget(header)
        
        # 네비게이션 메뉴
        nav_menu = self.create_nav_menu()
        main_layout.addWidget(nav_menu)
        
        # 컨텐츠 영역 (스크롤 가능)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background-color: #f5f5f5; }")
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # 1반 시간표 타이틀
        title_label = QLabel("🏠 1반 시간표")
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            padding: 10px;
            color: #333;
        """)
        content_layout.addWidget(title_label)
        
        # 교육 세팅 섹션
        edu_setting_section = self.create_edu_setting_section()
        content_layout.addWidget(edu_setting_section)
        
        # 교육 인원 정보 섹션
        edu_info_section = self.create_edu_info_section()
        content_layout.addWidget(edu_info_section)
        
        # 교과 과정 학습 진도 섹션
        progress_section = self.create_progress_section()
        content_layout.addWidget(progress_section)
        
        # 교육 기간 섹션
        period_section = self.create_period_section()
        content_layout.addWidget(period_section)
        
        content_layout.addStretch()
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        
        main_layout.addWidget(scroll_area)
        
        # 하단 버튼 바
        bottom_bar = self.create_bottom_bar()
        main_layout.addWidget(bottom_bar)
        
        main_widget.setLayout(main_layout)
        
    def create_header(self):
        """헤더 생성"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2962FF;
                color: white;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # 타이틀
        title = QLabel("🏛️ 바이오헬스 올인원테크 이노베이터\nfor KDT")
        title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
        """)
        layout.addWidget(title)
        
        layout.addStretch()
        
        # 서브 타이틀
        subtitle = QLabel("실시간 데이터 분석 대응")
        subtitle.setStyleSheet("color: white; font-size: 12px;")
        layout.addWidget(subtitle)
        
        # 메뉴 버튼
        menu_btn = QPushButton("☰ 메뉴 보기")
        menu_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                border: 1px solid white;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(menu_btn)
        
        header.setLayout(layout)
        return header
        
    def create_nav_menu(self):
        """네비게이션 메뉴 생성"""
        nav = QFrame()
        nav.setStyleSheet("""
            QFrame {
                background-color: #1E53E5;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout()
        layout.setSpacing(5)
        
        menu_items = [
            ("🏠 시간표", True),
            ("👨‍🏫 강사 시간표", False),
            ("📊 3개 과정", False),
            ("✅ 출석 현황", False),
            ("📁 프로젝트 관리", False)
        ]
        
        for text, is_active in menu_items:
            btn = QPushButton(text)
            if is_active:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: white;
                        color: #2962FF;
                        border: none;
                        padding: 8px 20px;
                        border-radius: 3px;
                        font-weight: bold;
                    }
                """)
            else:
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        border: none;
                        padding: 8px 20px;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: rgba(255, 255, 255, 0.2);
                    }
                """)
            layout.addWidget(btn)
        
        layout.addStretch()
        nav.setLayout(layout)
        return nav
        
    def create_edu_setting_section(self):
        """교육 세팅 섹션"""
        section = CollapsibleSection("교육 세팅")
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(10)
        
        # 교육 과정 (번호/명)
        layout.addWidget(QLabel("교육 과정 (번호/명):"), 0, 0)
        course_num = QLineEdit("2023-10-27")
        course_num.setPlaceholderText("예: 5기-6차교육산업")
        layout.addWidget(course_num, 0, 1)
        
        # 저장 버튼 추가
        save_btn = QPushButton("저장하기")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(save_btn, 0, 2)
        
        container.setLayout(layout)
        section.add_widget(container)
        
        return section
        
    def create_edu_info_section(self):
        """교육 인원 정보 섹션"""
        section = CollapsibleSection("교과 내용 및 480시간")
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        
        # 첫 번째 행
        layout.addWidget(QLabel("교육 시작일:"), 0, 0)
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate(2023, 10, 27))
        self.start_date.setCalendarPopup(True)
        self.start_date.setStyleSheet("padding: 5px;")
        layout.addWidget(self.start_date, 0, 1)
        
        layout.addWidget(QLabel("수업 시작시간:"), 0, 2)
        start_time = QTimeEdit()
        start_time.setTime(QTime(9, 0))
        start_time.setStyleSheet("padding: 5px;")
        layout.addWidget(start_time, 0, 3)
        
        layout.addWidget(QLabel("교육 정원:"), 0, 4)
        capacity = QLineEdit("26명")
        capacity.setMaximumWidth(100)
        layout.addWidget(capacity, 0, 5)
        
        # 두 번째 행
        layout.addWidget(QLabel("교육 종료일:"), 1, 0)
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate(2024, 3, 1))
        self.end_date.setCalendarPopup(True)
        self.end_date.setStyleSheet("padding: 5px;")
        layout.addWidget(self.end_date, 1, 1)
        
        layout.addWidget(QLabel("수업 종료시간:"), 1, 2)
        end_time = QTimeEdit()
        end_time.setTime(QTime(18, 0))
        end_time.setStyleSheet("padding: 5px;")
        layout.addWidget(end_time, 1, 3)
        
        layout.addWidget(QLabel("교육 인원:"), 1, 4)
        students = QLineEdit("22명")
        students.setMaximumWidth(100)
        layout.addWidget(students, 1, 5)
        
        container.setLayout(layout)
        section.add_widget(container)
        
        return section
        
    def create_progress_section(self):
        """과정 학습 진도 섹션"""
        section = CollapsibleSection("IT 교과 과정 학습 진도 통계")
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        
        # 이론 시간
        theory_label = QLabel("이론:")
        theory_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(theory_label, 0, 0)
        
        theory_input = QLineEdit("260")
        theory_input.setMaximumWidth(100)
        layout.addWidget(theory_input, 0, 1)
        
        theory_total = QLabel("총 시간(이론+실습) 480시간")
        theory_total.setStyleSheet("color: #2196F3; font-weight: bold;")
        layout.addWidget(theory_total, 0, 2)
        
        # 실습 시간
        practice_label = QLabel("실습:")
        practice_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(practice_label, 1, 0)
        
        practice_input = QLineEdit("220")
        practice_input.setMaximumWidth(100)
        layout.addWidget(practice_input, 1, 1)
        
        # 프로젝트 시간
        project_label = QLabel("프로젝트:")
        project_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(project_label, 2, 0)
        
        project_input = QLineEdit("120")
        project_input.setMaximumWidth(100)
        layout.addWidget(project_input, 2, 1)
        
        project_hours = QLabel("최종 프로젝트\n2월")
        project_hours.setStyleSheet("color: #F44336;")
        layout.addWidget(project_hours, 2, 2)
        
        container.setLayout(layout)
        section.add_widget(container)
        
        return section
        
    def create_period_section(self):
        """교육 기간 섹션"""
        section = CollapsibleSection("교육 기간")
        
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 15px;
            }
        """)
        
        layout = QGridLayout()
        layout.setSpacing(15)
        
        # 시작 월일
        layout.addWidget(QLabel("시작 월일:"), 0, 0)
        start_period = QLineEdit("2023-12-28")
        layout.addWidget(start_period, 0, 1)
        
        # 종료 월일
        layout.addWidget(QLabel("종료시 월일:"), 0, 2)
        end_period = QLineEdit("12월01일-3")
        layout.addWidget(end_period, 0, 3)
        
        # 내역표 월일
        layout.addWidget(QLabel("내역표 월일:"), 0, 4)
        report_period = QLineEdit("2023-12-11")
        layout.addWidget(report_period, 0, 5)
        
        container.setLayout(layout)
        section.add_widget(container)
        
        # 교육 안내 정보 박스
        info_box = QWidget()
        info_box.setStyleSheet("""
            QWidget {
                background-color: #E3F2FD;
                border: 1px solid #90CAF9;
                border-radius: 5px;
                padding: 15px;
                margin-top: 10px;
            }
        """)
        
        info_layout = QVBoxLayout()
        
        info_title = QLabel("ℹ️ 교육 과정 안내")
        info_title.setStyleSheet("font-weight: bold; font-size: 14px; color: #1976D2;")
        info_layout.addWidget(info_title)
        
        info_text = QLabel(
            "• 교육 기간: 전체 수업 일정은 해당 과정 종료일까지입니다\n"
            "• 교과내 목표: 실시 이론과 실습과 함께 프로젝트 산학 대인지\n"
            "• 교육 진도: 진행 상태 교육 계획과 진도율 확인이 가능 합니다\n"
            "• 시간표 관리: 강사, 실습 관리, 시간, 교육 기관을 등록할 수 있습니다"
        )
        info_text.setStyleSheet("color: #555; line-height: 1.8;")
        info_layout.addWidget(info_text)
        
        info_box.setLayout(info_layout)
        section.add_widget(info_box)
        
        return section
        
    def create_bottom_bar(self):
        """하단 버튼 바 생성"""
        bottom_bar = QFrame()
        bottom_bar.setStyleSheet("""
            QFrame {
                background-color: white;
                border-top: 1px solid #ddd;
                padding: 15px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # 시간표 저장 완료 버튼
        save_complete_btn = QPushButton("✓ 시간표 저장 완료")
        save_complete_btn.setStyleSheet("""
            QPushButton {
                background-color: #2962FF;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1E53E5;
            }
        """)
        save_complete_btn.clicked.connect(self.save_complete)
        layout.addWidget(save_complete_btn)
        
        # 시간표 가져오기 버튼
        import_btn = QPushButton("📥 시간표 가져오기")
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(import_btn)
        
        # Excel 내려받기 버튼
        excel_btn = QPushButton("📊 Excel 내려받기")
        excel_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7B1FA2;
            }
        """)
        layout.addWidget(excel_btn)
        
        # 초기화 버튼
        reset_btn = QPushButton("🔄 초기화")
        reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #757575;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #616161;
            }
        """)
        reset_btn.clicked.connect(self.reset_form)
        layout.addWidget(reset_btn)
        
        # 관리자 버튼
        admin_btn = QPushButton("⚙️ 관리자-데이터추가")
        admin_btn.setStyleSheet("""
            QPushButton {
                background-color: #00BCD4;
                color: white;
                border: none;
                padding: 10px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #0097A7;
            }
        """)
        layout.addWidget(admin_btn)
        
        layout.addStretch()
        
        bottom_bar.setLayout(layout)
        return bottom_bar
        
    def save_complete(self):
        """시간표 저장 완료"""
        QMessageBox.information(self, "저장 완료", "1반 시간표 저장이 완료되었습니다.")
        
    def reset_form(self):
        """폼 초기화"""
        reply = QMessageBox.question(self, "초기화 확인", 
                                     "정말로 모든 내용을 초기화하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, "초기화", "폼이 초기화되었습니다.")
