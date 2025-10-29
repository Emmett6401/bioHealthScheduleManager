# -*- coding: utf-8 -*-
"""
KDT 메인 윈도우 - 전체 기능 통합
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QMessageBox, QFrame,
                             QToolBar, QAction, QFileDialog, QMenu, QTabWidget)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.db_manager import DatabaseManager
from config_db import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT
from utils.excel_manager import ExcelManager

# 다이얼로그 임포트
from ui.instructor_code_dialog import InstructorCodeDialog
from ui.instructor_dialog import InstructorDialog
from ui.subject_dialog import SubjectDialog
from ui.holiday_dialog import HolidayDialog
from ui.course_dialog import CourseDialog
from ui.student_dialog import StudentDialog
from ui.project_dialog import ProjectDialog
from ui.timetable_create_dialog import TimetableCreateDialog


class KDTMainWindowFull(QMainWindow):
    """KDT 메인 윈도우 - 전체 기능 (탭 기반)"""
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()
        self.tab_widget = None  # 탭 위젯
        self.open_tabs = {}  # 열린 탭 추적 {name: widget}
        self.init_ui()
        self.check_database()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        
        # 화면 크기 설정 - 수직 최대화
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().availableGeometry()
        self.resize(1280, screen.height())
        self.center_on_screen()
        
        # 전체 애플리케이션에 고딕 폰트 적용
        from PyQt5.QtGui import QFont
        app_font = QFont("맑은 고딕", 10)
        self.setFont(app_font)
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 헤더
        header = self.create_header()
        layout.addWidget(header)
        
        # 메뉴바 생성
        self.create_menu_bar()
        
        # 메인 컨텐츠
        content = self.create_content()
        layout.addWidget(content)
        
        # 하단 상태바
        self.statusBar().showMessage('준비')
        
        central_widget.setLayout(layout)
    
    def center_on_screen(self):
        """윈도우를 화면 중앙에 배치 (수직은 맨 위부터)"""
        from PyQt5.QtWidgets import QDesktopWidget
        screen = QDesktopWidget().screenGeometry()
        window = self.geometry()
        x = (screen.width() - window.width()) // 2
        y = 0  # 화면 맨 위부터 시작
        self.move(x, y)
        
    def create_header(self):
        """헤더 생성"""
        header = QFrame()
        header.setStyleSheet("""
            QFrame {
                background-color: #2962FF;
                color: white;
                padding: 10px 15px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # 타이틀
        title = QLabel("🏛️ 바이오헬스 올인원테크 이노베이터")
        title.setStyleSheet("""
            color: white;
            font-size: 16px;
            font-weight: bold;
            font-family: '맑은 고딕';
        """)
        layout.addWidget(title)
        
        subtitle = QLabel("for KDT - 교육 관리 시스템")
        subtitle.setStyleSheet("color: white; font-size: 14px; font-family: '맑은 고딕';")
        layout.addWidget(subtitle)
        
        header.setLayout(layout)
        return header
        
    def create_menu_bar(self):
        """메뉴바 생성"""
        menubar = self.menuBar()
        
        # 기본 관리 메뉴
        basic_menu = menubar.addMenu('기본 관리')
        
        instructor_code_action = QAction('강사 코드 관리', self)
        instructor_code_action.triggered.connect(self.show_instructor_code_dialog)
        basic_menu.addAction(instructor_code_action)
        
        instructor_action = QAction('강사 관리', self)
        instructor_action.triggered.connect(self.show_instructor_dialog)
        basic_menu.addAction(instructor_action)
        
        subject_action = QAction('교과목 관리', self)
        subject_action.triggered.connect(self.show_subject_dialog)
        basic_menu.addAction(subject_action)
        
        holiday_action = QAction('공휴일 관리', self)
        holiday_action.triggered.connect(self.show_holiday_dialog)
        basic_menu.addAction(holiday_action)
        
        # 과정 관리 메뉴
        course_menu = menubar.addMenu('과정 관리')
        
        course_action = QAction('과정 관리', self)
        course_action.triggered.connect(self.show_course_dialog)
        course_menu.addAction(course_action)
        
        student_action = QAction('학생 관리', self)
        student_action.triggered.connect(self.show_student_dialog)
        course_menu.addAction(student_action)
        
        project_action = QAction('프로젝트 관리', self)
        project_action.triggered.connect(self.show_project_dialog)
        course_menu.addAction(project_action)
        
        # 시간표 메뉴
        timetable_menu = menubar.addMenu('시간표')
        
        create_timetable_action = QAction('시간표 작성', self)
        create_timetable_action.triggered.connect(self.show_timetable_create_dialog)
        timetable_menu.addAction(create_timetable_action)
        
        view_timetable_action = QAction('시간표 조회', self)
        timetable_menu.addAction(view_timetable_action)
        
        # Excel 메뉴
        excel_menu = menubar.addMenu('Excel')
        
        export_action = QAction('내보내기', self)
        export_action.triggered.connect(self.export_excel)
        excel_menu.addAction(export_action)
        
        import_action = QAction('가져오기', self)
        import_action.triggered.connect(self.import_excel)
        excel_menu.addAction(import_action)
        
        # 도움말 메뉴
        help_menu = menubar.addMenu('도움말')
        
        about_action = QAction('정보', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_toolbar(self):
        """툴바 생성"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #f5f5f5;
                border-bottom: 1px solid #ddd;
                padding: 5px;
            }
            QToolButton {
                padding: 8px;
                margin: 2px;
            }
        """)
        self.addToolBar(toolbar)
        
        # 강사 코드 관리
        toolbar.addAction(QAction('👤 강사 코드', self, triggered=self.show_instructor_code_dialog))
        
        # 강사 관리
        toolbar.addAction(QAction('👨‍🏫 강사 관리', self, triggered=self.show_instructor_dialog))
        
        # 교과목 관리
        toolbar.addAction(QAction('📚 교과목', self, triggered=self.show_subject_dialog))
        
        toolbar.addSeparator()
        
        # 공휴일 관리
        toolbar.addAction(QAction('📅 공휴일', self, triggered=self.show_holiday_dialog))
        
        # 과정 관리
        toolbar.addAction(QAction('🎓 과정', self, triggered=self.show_course_dialog))
        
        # 프로젝트 관리
        toolbar.addAction(QAction('💼 프로젝트', self, triggered=self.show_project_dialog))
        
        toolbar.addSeparator()
        
        # 학생 관리
        toolbar.addAction(QAction('👨‍🎓 학생 관리', self, triggered=self.show_student_dialog))
        
        toolbar.addSeparator()
        
        # Excel
        toolbar.addAction(QAction('📊 Excel 내보내기', self, triggered=self.export_excel))
        
    def create_content(self):
        """컨텐츠 영역 생성 - 탭 위젯"""
        # 탭 위젯 생성
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #ddd;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 10px 20px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: white;
                border-bottom-color: white;
            }
            QTabBar::tab:hover {
                background-color: #e8e8e8;
            }
        """)
        
        # 홈 탭 추가
        home_widget = self.create_home_widget()
        self.tab_widget.addTab(home_widget, "🏠 홈")
        self.tab_widget.tabBar().setTabButton(0, self.tab_widget.tabBar().RightSide, None)  # 홈 탭은 닫기 버튼 없음
        
        return self.tab_widget
    
    def create_home_widget(self):
        """홈 위젯 생성"""
        home = QWidget()
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        # 환영 메시지
        welcome = QLabel("🎓 KDT 교육 관리 시스템에 오신 것을 환영합니다!")
        welcome.setStyleSheet("font-size: 14px; font-weight: bold; color: #333; padding: 20px;")
        welcome.setAlignment(Qt.AlignCenter)
        layout.addWidget(welcome)
        
        # 기능 버튼 그리드
        buttons_layout = QVBoxLayout()
        buttons_layout.setSpacing(10)
        
        # 첫 번째 행
        row1 = QHBoxLayout()
        row1.addWidget(self.create_feature_button("👤 강사 코드 관리", "#9C27B0", self.show_instructor_code_dialog))
        row1.addWidget(self.create_feature_button("👨‍🏫 강사 관리", "#2196F3", self.show_instructor_dialog))
        row1.addWidget(self.create_feature_button("📚 교과목 관리", "#4CAF50", self.show_subject_dialog))
        buttons_layout.addLayout(row1)
        
        # 두 번째 행
        row2 = QHBoxLayout()
        row2.addWidget(self.create_feature_button("📅 공휴일 관리", "#FF9800", self.show_holiday_dialog))
        row2.addWidget(self.create_feature_button("🎓 과정 관리", "#F44336", self.show_course_dialog))
        row2.addWidget(self.create_feature_button("💼 프로젝트 관리", "#00BCD4", self.show_project_dialog))
        buttons_layout.addLayout(row2)
        
        # 세 번째 행
        row3 = QHBoxLayout()
        row3.addWidget(self.create_feature_button("📝 시간표 작성", "#3F51B5", self.show_timetable_create_dialog))
        row3.addWidget(self.create_feature_button("📊 Excel 내보내기", "#795548", self.export_excel))
        row3.addWidget(self.create_feature_button("📥 Excel 가져오기", "#607D8B", self.import_excel))
        buttons_layout.addLayout(row3)
        
        # 네 번째 행
        row4 = QHBoxLayout()
        row4.addWidget(self.create_feature_button("🔧 데이터베이스 초기화", "#9E9E9E", self.init_database))
        row4.addStretch()
        row4.addStretch()
        buttons_layout.addLayout(row4)
        
        layout.addLayout(buttons_layout)
        layout.addStretch()
        
        home.setLayout(layout)
        return home
        
    def create_feature_button(self, text, color, callback):
        """기능 버튼 생성"""
        btn = QPushButton(text)
        btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                padding: 30px;
                border-radius: 10px;
                font-size: 13px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """)
        btn.clicked.connect(callback)
        btn.setMinimumHeight(100)
        return btn
        
    def check_database(self):
        """데이터베이스 연결 확인"""
        if self.db.connect():
            self.statusBar().showMessage('데이터베이스 연결됨')
        else:
            QMessageBox.warning(self, "경고", "데이터베이스 연결에 실패했습니다.")
            
    def init_database(self):
        """데이터베이스 초기화"""
        reply = QMessageBox.question(self, "확인", 
                                     "데이터베이스 테이블을 초기화하시겠습니까?",
                                     QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            if self.db.connect():
                if self.db.create_tables():
                    QMessageBox.information(self, "성공", "데이터베이스 테이블이 생성되었습니다.")
                else:
                    QMessageBox.critical(self, "오류", "테이블 생성 실패")
            else:
                QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
    
    def open_or_focus_tab(self, tab_name, widget_class, icon=""):
        """탭이 이미 열려있으면 포커스, 없으면 새로 생성"""
        # 이미 열린 탭이 있는지 확인
        if tab_name in self.open_tabs:
            # 해당 탭으로 전환
            index = self.tab_widget.indexOf(self.open_tabs[tab_name])
            self.tab_widget.setCurrentIndex(index)
        else:
            # 새 탭 생성
            widget = widget_class(self)
            self.tab_widget.addTab(widget, f"{icon} {tab_name}")
            self.open_tabs[tab_name] = widget
            self.tab_widget.setCurrentWidget(widget)
    
    def close_tab(self, index):
        """탭 닫기"""
        if index == 0:  # 홈 탭은 닫을 수 없음
            return
        
        widget = self.tab_widget.widget(index)
        tab_text = self.tab_widget.tabText(index)
        
        # open_tabs에서 제거
        for name, w in list(self.open_tabs.items()):
            if w == widget:
                del self.open_tabs[name]
                break
        
        # 위젯의 closeEvent 호출 (DB 연결 종료 등)
        if hasattr(widget, 'db'):
            widget.db.disconnect()
        
        self.tab_widget.removeTab(index)
        widget.deleteLater()
    
    def show_instructor_code_dialog(self):
        """강사 코드 관리 탭 표시"""
        self.open_or_focus_tab("강사 코드 관리", InstructorCodeDialog, "👤")
        
    def show_instructor_dialog(self):
        """강사 관리 탭 표시"""
        self.open_or_focus_tab("강사 관리", InstructorDialog, "👨‍🏫")
        
    def show_subject_dialog(self):
        """교과목 관리 탭 표시"""
        self.open_or_focus_tab("교과목 관리", SubjectDialog, "📚")
        
    def show_holiday_dialog(self):
        """공휴일 관리 탭 표시"""
        self.open_or_focus_tab("공휴일 관리", HolidayDialog, "📅")
        
    def show_course_dialog(self):
        """과정 관리 탭 표시"""
        self.open_or_focus_tab("과정 관리", CourseDialog, "🎓")
        
    def show_student_dialog(self):
        """학생 관리 탭 표시"""
        self.open_or_focus_tab("학생 관리", StudentDialog, "👨‍🎓")
        
    def show_project_dialog(self):
        """프로젝트 관리 탭 표시"""
        self.open_or_focus_tab("프로젝트 관리", ProjectDialog, "💼")
    
    def show_student_dialog(self):
        """학생 관리 탭 표시"""
        self.open_or_focus_tab("학생 관리", StudentDialog, "👨‍🎓")
    
    def show_timetable_create_dialog(self):
        """시간표 작성 탭 표시"""
        self.open_or_focus_tab("시간표 작성", TimetableCreateDialog, "📝")
        
    def show_timetable_generate_dialog(self):
        """시간표 자동 생성 다이얼로그 표시"""
        dialog = TimetableGenerateDialog(self)
        dialog.exec_()
        
    def show_timetable_view_dialog(self):
        """시간표 조회/수정 다이얼로그 표시"""
        dialog = TimetableViewDialog(self)
        dialog.exec_()
        
    def show_pdf_report_dialog(self):
        """PDF 보고서 생성 다이얼로그 표시"""
        dialog = PDFReportDialog(self)
        dialog.exec_()
        
    def export_excel(self):
        """Excel 내보내기"""
        menu = QMenu(self)
        menu.addAction("강사 목록", lambda: self.export_data('instructors'))
        menu.addAction("교과목 목록", lambda: self.export_data('subjects'))
        menu.addAction("과정 목록", lambda: self.export_data('courses'))
        menu.addAction("프로젝트 목록", lambda: self.export_data('projects'))
        menu.addAction("공휴일 목록", lambda: self.export_data('holidays'))
        menu.exec_(self.cursor().pos())
        
    def export_data(self, table_name):
        """데이터 내보내기"""
        try:
            if not self.db.connect():
                QMessageBox.critical(self, "오류", "데이터베이스 연결 실패")
                return
            
            query = f"SELECT * FROM {table_name}"
            data = self.db.fetch_all(query)
            
            if not data:
                QMessageBox.warning(self, "경고", "내보낼 데이터가 없습니다.")
                return
            
            filename = ExcelManager.export_to_excel(data, table_name)
            QMessageBox.information(self, "성공", f"파일이 저장되었습니다:\n{filename}")
            self.statusBar().showMessage(f'Excel 내보내기 완료: {filename}')
            
        except Exception as e:
            QMessageBox.critical(self, "오류", f"내보내기 실패: {str(e)}")
        
    def import_excel(self):
        """Excel 가져오기"""
        filename, _ = QFileDialog.getOpenFileName(self, "Excel 파일 선택", "", "Excel Files (*.xlsx *.xls)")
        
        if filename:
            try:
                data = ExcelManager.import_from_excel(filename)
                QMessageBox.information(self, "성공", f"{len(data)}개의 데이터를 가져왔습니다.")
                self.statusBar().showMessage(f'Excel 가져오기 완료: {len(data)}개')
            except Exception as e:
                QMessageBox.critical(self, "오류", f"가져오기 실패: {str(e)}")
        
    def show_about(self):
        """정보 표시"""
        QMessageBox.about(self, "정보", 
                         f"{APP_NAME}\n"
                         f"버전: {APP_VERSION}\n\n"
                         "교육 과정 관리를 위한 통합 시스템\n\n"
                         "기능:\n"
                         "- 강사/교과목/과정/프로젝트 관리\n"
                         "- 공휴일 관리\n"
                         "- 시간표 자동 생성\n"
                         "- Excel 내보내기/가져오기")
        
    def closeEvent(self, event):
        """종료 시"""
        self.db.disconnect()
        event.accept()
