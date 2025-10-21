# -*- coding: utf-8 -*-
"""
메인 윈도우 UI
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, 
                             QTextEdit, QLineEdit, QLabel, QMessageBox,
                             QSplitter, QHeaderView, QMenuBar, QMenu, QAction,
                             QStatusBar, QToolBar)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
import sys
import os

# 상위 디렉토리를 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.database import DatabaseManager, create_note, get_all_notes, update_note, delete_note
from config import APP_NAME, APP_VERSION, WINDOW_WIDTH, WINDOW_HEIGHT


class MainWindow(QMainWindow):
    """메인 윈도우 클래스"""
    
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager(use_sqlite=True)
        self.current_note_id = None
        self.init_ui()
        self.connect_db()
        self.load_notes()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setGeometry(100, 100, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        # 메뉴바 생성
        self.create_menu_bar()
        
        # 툴바 생성
        self.create_tool_bar()
        
        # 중앙 위젯
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 메인 레이아웃
        main_layout = QHBoxLayout()
        
        # 스플리터로 좌우 분할
        splitter = QSplitter(Qt.Horizontal)
        
        # 왼쪽 패널 (노트 목록)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # 오른쪽 패널 (노트 편집)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # 스플리터 비율 설정 (1:2)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        central_widget.setLayout(main_layout)
        
        # 상태바
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage('준비')
        
    def create_menu_bar(self):
        """메뉴바 생성"""
        menubar = self.menuBar()
        
        # 파일 메뉴
        file_menu = menubar.addMenu('파일(&F)')
        
        new_action = QAction('새 노트(&N)', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_note)
        file_menu.addAction(new_action)
        
        save_action = QAction('저장(&S)', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_note)
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('종료(&X)', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 편집 메뉴
        edit_menu = menubar.addMenu('편집(&E)')
        
        delete_action = QAction('삭제(&D)', self)
        delete_action.setShortcut('Delete')
        delete_action.triggered.connect(self.delete_note)
        edit_menu.addAction(delete_action)
        
        # 도움말 메뉴
        help_menu = menubar.addMenu('도움말(&H)')
        
        about_action = QAction('정보(&A)', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def create_tool_bar(self):
        """툴바 생성"""
        toolbar = QToolBar()
        toolbar.setMovable(False)
        self.addToolBar(toolbar)
        
        # 새 노트 버튼
        new_btn = QAction('새 노트', self)
        new_btn.triggered.connect(self.new_note)
        toolbar.addAction(new_btn)
        
        # 저장 버튼
        save_btn = QAction('저장', self)
        save_btn.triggered.connect(self.save_note)
        toolbar.addAction(save_btn)
        
        toolbar.addSeparator()
        
        # 삭제 버튼
        delete_btn = QAction('삭제', self)
        delete_btn.triggered.connect(self.delete_note)
        toolbar.addAction(delete_btn)
        
        toolbar.addSeparator()
        
        # 새로고침 버튼
        refresh_btn = QAction('새로고침', self)
        refresh_btn.triggered.connect(self.load_notes)
        toolbar.addAction(refresh_btn)
        
    def create_left_panel(self):
        """왼쪽 패널 생성 (노트 목록)"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # 제목
        title_label = QLabel('노트 목록')
        title_label.setStyleSheet('font-size: 16px; font-weight: bold; padding: 10px;')
        layout.addWidget(title_label)
        
        # 노트 목록 테이블
        self.notes_table = QTableWidget()
        self.notes_table.setColumnCount(2)
        self.notes_table.setHorizontalHeaderLabels(['ID', '제목'])
        self.notes_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.notes_table.setColumnWidth(0, 50)
        self.notes_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.notes_table.setSelectionMode(QTableWidget.SingleSelection)
        self.notes_table.cellClicked.connect(self.on_note_selected)
        layout.addWidget(self.notes_table)
        
        panel.setLayout(layout)
        return panel
        
    def create_right_panel(self):
        """오른쪽 패널 생성 (노트 편집)"""
        panel = QWidget()
        layout = QVBoxLayout()
        
        # 제목 입력
        title_layout = QHBoxLayout()
        title_label = QLabel('제목:')
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('노트 제목을 입력하세요')
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_input)
        layout.addLayout(title_layout)
        
        # 내용 입력
        content_label = QLabel('내용:')
        layout.addWidget(content_label)
        
        self.content_input = QTextEdit()
        self.content_input.setPlaceholderText('노트 내용을 입력하세요')
        layout.addWidget(self.content_input)
        
        # 버튼 레이아웃
        button_layout = QHBoxLayout()
        
        self.new_btn = QPushButton('새 노트')
        self.new_btn.clicked.connect(self.new_note)
        button_layout.addWidget(self.new_btn)
        
        self.save_btn = QPushButton('저장')
        self.save_btn.clicked.connect(self.save_note)
        button_layout.addWidget(self.save_btn)
        
        self.delete_btn = QPushButton('삭제')
        self.delete_btn.clicked.connect(self.delete_note)
        button_layout.addWidget(self.delete_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        panel.setLayout(layout)
        return panel
        
    def connect_db(self):
        """데이터베이스 연결"""
        if self.db_manager.connect():
            self.statusBar.showMessage('데이터베이스 연결 성공')
        else:
            QMessageBox.critical(self, '오류', '데이터베이스 연결에 실패했습니다.')
            
    def load_notes(self):
        """노트 목록 로드"""
        session = self.db_manager.get_session()
        if session:
            try:
                notes = get_all_notes(session)
                self.notes_table.setRowCount(0)
                
                for note in notes:
                    row = self.notes_table.rowCount()
                    self.notes_table.insertRow(row)
                    self.notes_table.setItem(row, 0, QTableWidgetItem(str(note.id)))
                    self.notes_table.setItem(row, 1, QTableWidgetItem(note.title))
                
                self.statusBar.showMessage(f'{len(notes)}개의 노트를 불러왔습니다.')
            finally:
                session.close()
                
    def on_note_selected(self, row, column):
        """노트 선택 시"""
        note_id = int(self.notes_table.item(row, 0).text())
        session = self.db_manager.get_session()
        
        if session:
            try:
                from models.database import Note
                note = session.query(Note).filter(Note.id == note_id).first()
                if note:
                    self.current_note_id = note_id
                    self.title_input.setText(note.title)
                    self.content_input.setText(note.content or '')
                    self.statusBar.showMessage(f'노트 "{note.title}" 로드됨')
            finally:
                session.close()
                
    def new_note(self):
        """새 노트"""
        self.current_note_id = None
        self.title_input.clear()
        self.content_input.clear()
        self.title_input.setFocus()
        self.statusBar.showMessage('새 노트 작성 중')
        
    def save_note(self):
        """노트 저장"""
        title = self.title_input.text().strip()
        content = self.content_input.toPlainText().strip()
        
        if not title:
            QMessageBox.warning(self, '경고', '제목을 입력해주세요.')
            return
            
        session = self.db_manager.get_session()
        if session:
            try:
                if self.current_note_id:
                    # 업데이트
                    note = update_note(session, self.current_note_id, title, content)
                    if note:
                        QMessageBox.information(self, '성공', '노트가 업데이트되었습니다.')
                        self.statusBar.showMessage('노트 저장 완료')
                else:
                    # 새로 생성
                    note = create_note(session, title, content)
                    if note:
                        self.current_note_id = note.id
                        QMessageBox.information(self, '성공', '노트가 생성되었습니다.')
                        self.statusBar.showMessage('노트 저장 완료')
                
                self.load_notes()
            finally:
                session.close()
                
    def delete_note(self):
        """노트 삭제"""
        if not self.current_note_id:
            QMessageBox.warning(self, '경고', '삭제할 노트를 선택해주세요.')
            return
            
        reply = QMessageBox.question(self, '확인', '정말로 이 노트를 삭제하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            session = self.db_manager.get_session()
            if session:
                try:
                    if delete_note(session, self.current_note_id):
                        QMessageBox.information(self, '성공', '노트가 삭제되었습니다.')
                        self.new_note()
                        self.load_notes()
                        self.statusBar.showMessage('노트 삭제 완료')
                    else:
                        QMessageBox.critical(self, '오류', '노트 삭제에 실패했습니다.')
                finally:
                    session.close()
                    
    def show_about(self):
        """정보 대화상자"""
        QMessageBox.about(self, '정보', 
                         f'{APP_NAME} v{APP_VERSION}\n\n'
                         'PyQt5로 만든 노트 애플리케이션입니다.\n'
                         'SQLAlchemy를 사용하여 데이터베이스를 관리합니다.')
        
    def closeEvent(self, event):
        """종료 시"""
        reply = QMessageBox.question(self, '종료 확인', 
                                     '정말로 종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, 
                                     QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.db_manager.close()
            event.accept()
        else:
            event.ignore()
