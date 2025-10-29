# -*- coding: utf-8 -*-
"""
학생 면담 관리 다이얼로그
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QTextEdit, QPushButton, QTableWidget,
                             QTableWidgetItem, QComboBox, QDateTimeEdit, QDateEdit,
                             QMessageBox, QFileDialog, QGroupBox, QGridLayout,
                             QHeaderView, QSplitter, QListWidget, QListWidgetItem,
                             QAbstractItemView)
from PyQt5.QtCore import Qt, QDateTime, QDate
from PyQt5.QtGui import QPixmap, QIcon
from datetime import datetime, timedelta
import os
import shutil


class ConsultationDialog(QDialog):
    """면담 관리 다이얼로그"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # parent가 KDTMainWindowFull인 경우 db_manager 가져오기
        if hasattr(parent, 'db'):
            self.db_manager = parent.db
        else:
            # 직접 db_manager를 전달받은 경우 (하위 호환성)
            from database.db_manager import DatabaseManager
            self.db_manager = DatabaseManager()
            self.db_manager.connect()
        
        self.current_consultation_id = None
        self.photo_paths = []  # 추가된 사진 경로 목록
        self.init_ui()
        self.load_consultations()
        
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("학생 면담 관리")
        self.setGeometry(100, 100, 1400, 800)
        
        # 메인 레이아웃
        main_layout = QHBoxLayout()
        
        # 스플리터로 좌우 분할
        splitter = QSplitter(Qt.Horizontal)
        
        # 왼쪽: 면담 목록
        left_widget = self.create_list_section()
        splitter.addWidget(left_widget)
        
        # 오른쪽: 면담 상세/입력
        right_widget = self.create_detail_section()
        splitter.addWidget(right_widget)
        
        # 비율 설정 (왼쪽 40%, 오른쪽 60%)
        splitter.setSizes([560, 840])
        
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
    
    def create_list_section(self):
        """면담 목록 섹션 생성"""
        widget = QGroupBox("면담 목록")
        layout = QVBoxLayout()
        
        # 검색 및 필터
        filter_layout = QHBoxLayout()
        
        # 학생 이름 검색
        filter_layout.addWidget(QLabel("검색:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("학생 이름, 주제, 상담사...")
        self.search_input.textChanged.connect(self.search_consultations)
        filter_layout.addWidget(self.search_input)
        
        # 면담 유형 필터
        self.type_filter = QComboBox()
        self.type_filter.addItems(['전체', '정기', '수시', '긴급', '학부모'])
        self.type_filter.currentTextChanged.connect(self.search_consultations)
        filter_layout.addWidget(self.type_filter)
        
        layout.addLayout(filter_layout)
        
        # 기간 필터
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("기간:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-6))
        self.date_from.setCalendarPopup(True)
        self.date_from.dateChanged.connect(self.search_consultations)
        date_layout.addWidget(self.date_from)
        
        date_layout.addWidget(QLabel("~"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.dateChanged.connect(self.search_consultations)
        date_layout.addWidget(self.date_to)
        
        layout.addLayout(date_layout)
        
        # 면담 목록 테이블
        self.consultation_table = QTableWidget()
        self.consultation_table.setColumnCount(5)
        self.consultation_table.setHorizontalHeaderLabels(['ID', '학생명', '면담일시', '유형', '주제'])
        self.consultation_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.consultation_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.consultation_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # 컬럼 너비 설정
        header = self.consultation_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.Stretch)
        
        # ID 컬럼 숨기기
        self.consultation_table.setColumnHidden(0, True)
        
        self.consultation_table.cellClicked.connect(self.on_consultation_selected)
        layout.addWidget(self.consultation_table)
        
        # 버튼
        button_layout = QHBoxLayout()
        
        self.new_btn = QPushButton("새 면담")
        self.new_btn.clicked.connect(self.new_consultation)
        button_layout.addWidget(self.new_btn)
        
        self.delete_btn = QPushButton("삭제")
        self.delete_btn.clicked.connect(self.delete_consultation)
        button_layout.addWidget(self.delete_btn)
        
        self.upcoming_btn = QPushButton("예정 면담")
        self.upcoming_btn.clicked.connect(self.show_upcoming_consultations)
        button_layout.addWidget(self.upcoming_btn)
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def create_detail_section(self):
        """면담 상세 섹션 생성"""
        widget = QGroupBox("면담 상세 정보")
        layout = QVBoxLayout()
        
        # 스크롤 가능한 영역으로 변경 가능
        form_layout = QGridLayout()
        row = 0
        
        # 학생 선택
        form_layout.addWidget(QLabel("학생 선택:"), row, 0)
        self.student_combo = QComboBox()
        self.load_students()
        form_layout.addWidget(self.student_combo, row, 1, 1, 2)
        row += 1
        
        # 면담 일시
        form_layout.addWidget(QLabel("면담 일시:"), row, 0)
        self.consultation_datetime = QDateTimeEdit()
        self.consultation_datetime.setDateTime(QDateTime.currentDateTime())
        self.consultation_datetime.setCalendarPopup(True)
        form_layout.addWidget(self.consultation_datetime, row, 1, 1, 2)
        row += 1
        
        # 면담 장소
        form_layout.addWidget(QLabel("면담 장소:"), row, 0)
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("예: 상담실, 교실, 온라인 등")
        form_layout.addWidget(self.location_input, row, 1, 1, 2)
        row += 1
        
        # 면담 유형
        form_layout.addWidget(QLabel("면담 유형:"), row, 0)
        self.consultation_type_combo = QComboBox()
        self.consultation_type_combo.addItems(['정기', '수시', '긴급', '학부모'])
        form_layout.addWidget(self.consultation_type_combo, row, 1)
        
        # 면담 상태
        form_layout.addWidget(QLabel("상태:"), row, 2)
        self.status_combo = QComboBox()
        self.status_combo.addItems(['예정', '완료', '취소'])
        self.status_combo.setCurrentText('완료')
        form_layout.addWidget(self.status_combo, row, 3)
        row += 1
        
        # 상담사
        form_layout.addWidget(QLabel("상담사:"), row, 0)
        self.consultant_input = QLineEdit()
        form_layout.addWidget(self.consultant_input, row, 1, 1, 2)
        row += 1
        
        # 주요 주제
        form_layout.addWidget(QLabel("주요 주제:"), row, 0)
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("면담 주요 주제를 입력하세요")
        form_layout.addWidget(self.topic_input, row, 1, 1, 2)
        row += 1
        
        layout.addLayout(form_layout)
        
        # 면담 내용
        layout.addWidget(QLabel("면담 내용:"))
        self.content_text = QTextEdit()
        self.content_text.setPlaceholderText("상세한 면담 내용을 입력하세요...")
        layout.addWidget(self.content_text)
        
        # 다음 면담 예정일
        next_layout = QHBoxLayout()
        self.next_consultation_check = QPushButton("다음 면담 예정일 설정")
        self.next_consultation_check.setCheckable(True)
        self.next_consultation_check.toggled.connect(self.toggle_next_consultation)
        next_layout.addWidget(self.next_consultation_check)
        
        self.next_consultation_date = QDateTimeEdit()
        self.next_consultation_date.setDateTime(QDateTime.currentDateTime().addDays(30))
        self.next_consultation_date.setCalendarPopup(True)
        self.next_consultation_date.setEnabled(False)
        next_layout.addWidget(self.next_consultation_date)
        
        layout.addLayout(next_layout)
        
        # 사진 첨부
        photo_group = QGroupBox("첨부 사진")
        photo_layout = QVBoxLayout()
        
        photo_btn_layout = QHBoxLayout()
        self.add_photo_btn = QPushButton("사진 추가")
        self.add_photo_btn.clicked.connect(self.add_photos)
        photo_btn_layout.addWidget(self.add_photo_btn)
        
        self.remove_photo_btn = QPushButton("사진 삭제")
        self.remove_photo_btn.clicked.connect(self.remove_photo)
        photo_btn_layout.addWidget(self.remove_photo_btn)
        
        photo_layout.addLayout(photo_btn_layout)
        
        # 사진 목록
        self.photo_list = QListWidget()
        self.photo_list.setMaximumHeight(120)
        photo_layout.addWidget(self.photo_list)
        
        photo_group.setLayout(photo_layout)
        layout.addWidget(photo_group)
        
        # 저장/취소 버튼
        button_layout = QHBoxLayout()
        
        self.save_btn = QPushButton("저장")
        self.save_btn.clicked.connect(self.save_consultation)
        button_layout.addWidget(self.save_btn)
        
        self.report_btn = QPushButton("면담일지 출력")
        self.report_btn.clicked.connect(self.generate_report)
        button_layout.addWidget(self.report_btn)
        
        self.cancel_btn = QPushButton("취소")
        self.cancel_btn.clicked.connect(self.clear_form)
        button_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(button_layout)
        
        widget.setLayout(layout)
        return widget
    
    def load_students(self):
        """학생 목록 로드"""
        self.student_combo.clear()
        self.student_combo.addItem("학생을 선택하세요", None)
        
        students = self.db_manager.fetch_all("SELECT id, code, name FROM students ORDER BY name")
        for student in students:
            display_text = f"{student['code']} - {student['name']}"
            self.student_combo.addItem(display_text, student['id'])
    
    def load_consultations(self):
        """면담 목록 로드"""
        consultations = self.db_manager.get_all_consultations()
        self.populate_table(consultations)
    
    def populate_table(self, consultations):
        """테이블에 면담 목록 표시"""
        self.consultation_table.setRowCount(0)
        
        for consultation in consultations:
            row = self.consultation_table.rowCount()
            self.consultation_table.insertRow(row)
            
            # ID (숨김)
            self.consultation_table.setItem(row, 0, QTableWidgetItem(str(consultation['id'])))
            
            # 학생명
            self.consultation_table.setItem(row, 1, QTableWidgetItem(consultation.get('student_name', '')))
            
            # 면담 일시
            date_str = consultation['consultation_date'].strftime('%Y-%m-%d %H:%M') if consultation['consultation_date'] else ''
            self.consultation_table.setItem(row, 2, QTableWidgetItem(date_str))
            
            # 유형
            self.consultation_table.setItem(row, 3, QTableWidgetItem(consultation.get('consultation_type', '')))
            
            # 주제
            topic = consultation.get('main_topic', '')
            if len(topic) > 30:
                topic = topic[:30] + '...'
            self.consultation_table.setItem(row, 4, QTableWidgetItem(topic))
    
    def search_consultations(self):
        """면담 검색"""
        keyword = self.search_input.text()
        consultation_type = self.type_filter.currentText()
        if consultation_type == '전체':
            consultation_type = None
        
        date_from = self.date_from.date().toString('yyyy-MM-dd')
        date_to = self.date_to.date().toString('yyyy-MM-dd')
        
        consultations = self.db_manager.search_consultations(
            keyword=keyword,
            consultation_type=consultation_type,
            date_from=date_from,
            date_to=date_to
        )
        self.populate_table(consultations)
    
    def on_consultation_selected(self, row, col):
        """면담 선택 시"""
        consultation_id = int(self.consultation_table.item(row, 0).text())
        self.load_consultation_detail(consultation_id)
    
    def load_consultation_detail(self, consultation_id):
        """면담 상세 정보 로드"""
        consultation = self.db_manager.get_consultation(consultation_id)
        if not consultation:
            return
        
        self.current_consultation_id = consultation_id
        
        # 학생 선택
        index = self.student_combo.findData(consultation['student_id'])
        if index >= 0:
            self.student_combo.setCurrentIndex(index)
        
        # 면담 일시
        if consultation['consultation_date']:
            self.consultation_datetime.setDateTime(QDateTime(consultation['consultation_date']))
        
        # 장소
        self.location_input.setText(consultation.get('location', ''))
        
        # 유형
        self.consultation_type_combo.setCurrentText(consultation.get('consultation_type', '정기'))
        
        # 상태
        self.status_combo.setCurrentText(consultation.get('status', '완료'))
        
        # 상담사
        self.consultant_input.setText(consultation.get('consultant_name', ''))
        
        # 주제
        self.topic_input.setText(consultation.get('main_topic', ''))
        
        # 내용
        self.content_text.setText(consultation.get('content', ''))
        
        # 다음 면담 예정일
        if consultation.get('next_consultation_date'):
            self.next_consultation_check.setChecked(True)
            self.next_consultation_date.setDateTime(QDateTime(consultation['next_consultation_date']))
        else:
            self.next_consultation_check.setChecked(False)
        
        # 사진 로드
        self.load_consultation_photos(consultation_id)
    
    def load_consultation_photos(self, consultation_id):
        """면담 사진 로드"""
        self.photo_list.clear()
        self.photo_paths = []
        
        photos = self.db_manager.get_consultation_photos(consultation_id)
        for photo in photos:
            item = QListWidgetItem(os.path.basename(photo['photo_path']))
            item.setData(Qt.UserRole, photo['id'])
            item.setData(Qt.UserRole + 1, photo['photo_path'])
            self.photo_list.addItem(item)
            self.photo_paths.append(photo['photo_path'])
    
    def new_consultation(self):
        """새 면담 작성"""
        self.clear_form()
    
    def clear_form(self):
        """입력 폼 초기화"""
        self.current_consultation_id = None
        self.student_combo.setCurrentIndex(0)
        self.consultation_datetime.setDateTime(QDateTime.currentDateTime())
        self.location_input.clear()
        self.consultation_type_combo.setCurrentIndex(0)
        self.status_combo.setCurrentText('완료')
        self.consultant_input.clear()
        self.topic_input.clear()
        self.content_text.clear()
        self.next_consultation_check.setChecked(False)
        self.photo_list.clear()
        self.photo_paths = []
    
    def toggle_next_consultation(self, checked):
        """다음 면담 예정일 토글"""
        self.next_consultation_date.setEnabled(checked)
    
    def add_photos(self):
        """사진 추가"""
        files, _ = QFileDialog.getOpenFileNames(
            self, "면담 사진 선택", "",
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        
        if files:
            for file_path in files:
                # 파일명만 표시
                item = QListWidgetItem(os.path.basename(file_path))
                item.setData(Qt.UserRole, None)  # 새 사진은 DB ID 없음
                item.setData(Qt.UserRole + 1, file_path)
                self.photo_list.addItem(item)
                self.photo_paths.append(file_path)
    
    def remove_photo(self):
        """사진 삭제"""
        current_item = self.photo_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "경고", "삭제할 사진을 선택하세요.")
            return
        
        reply = QMessageBox.question(
            self, "확인", "선택한 사진을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            photo_id = current_item.data(Qt.UserRole)
            photo_path = current_item.data(Qt.UserRole + 1)
            
            # DB에서 삭제 (이미 저장된 경우)
            if photo_id:
                self.db_manager.delete_consultation_photo(photo_id)
            
            # 목록에서 제거
            if photo_path in self.photo_paths:
                self.photo_paths.remove(photo_path)
            
            self.photo_list.takeItem(self.photo_list.row(current_item))
    
    def save_consultation(self):
        """면담 정보 저장"""
        # 유효성 검사
        student_id = self.student_combo.currentData()
        if not student_id:
            QMessageBox.warning(self, "경고", "학생을 선택하세요.")
            return
        
        if not self.topic_input.text().strip():
            QMessageBox.warning(self, "경고", "면담 주제를 입력하세요.")
            return
        
        # 면담 데이터 준비
        consultation_data = {
            'student_id': student_id,
            'consultation_date': self.consultation_datetime.dateTime().toPyDateTime(),
            'location': self.location_input.text(),
            'main_topic': self.topic_input.text(),
            'content': self.content_text.toPlainText(),
            'consultant_name': self.consultant_input.text(),
            'consultation_type': self.consultation_type_combo.currentText(),
            'status': self.status_combo.currentText(),
            'next_consultation_date': None
        }
        
        # 다음 면담 예정일
        if self.next_consultation_check.isChecked():
            consultation_data['next_consultation_date'] = self.next_consultation_date.dateTime().toPyDateTime()
        
        try:
            # 저장 또는 업데이트
            if self.current_consultation_id:
                # 업데이트
                success = self.db_manager.update_consultation(
                    self.current_consultation_id, consultation_data
                )
                consultation_id = self.current_consultation_id
            else:
                # 새로 추가
                consultation_id = self.db_manager.add_consultation(consultation_data)
                success = consultation_id is not None
            
            if success:
                # 사진 저장
                self.save_photos(consultation_id)
                
                QMessageBox.information(self, "성공", "면담 정보가 저장되었습니다.")
                self.load_consultations()
                self.clear_form()
            else:
                QMessageBox.critical(self, "오류", "면담 정보 저장에 실패했습니다.")
                
        except Exception as e:
            QMessageBox.critical(self, "오류", f"저장 중 오류 발생: {str(e)}")
    
    def save_photos(self, consultation_id):
        """사진 파일 저장"""
        # 저장 디렉토리 생성
        photo_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                                 'consultation_photos')
        os.makedirs(photo_dir, exist_ok=True)
        
        # 새로 추가된 사진만 저장
        for i in range(self.photo_list.count()):
            item = self.photo_list.item(i)
            photo_id = item.data(Qt.UserRole)
            photo_path = item.data(Qt.UserRole + 1)
            
            # 이미 DB에 저장된 사진은 건너뛰기
            if photo_id:
                continue
            
            # 파일 복사
            filename = f"consultation_{consultation_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(photo_path)}"
            dest_path = os.path.join(photo_dir, filename)
            
            try:
                shutil.copy2(photo_path, dest_path)
                # DB에 저장
                self.db_manager.add_consultation_photo(consultation_id, dest_path)
            except Exception as e:
                print(f"사진 저장 오류: {e}")
    
    def delete_consultation(self):
        """면담 삭제"""
        current_row = self.consultation_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "경고", "삭제할 면담을 선택하세요.")
            return
        
        consultation_id = int(self.consultation_table.item(current_row, 0).text())
        student_name = self.consultation_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "확인", 
            f"{student_name}의 면담 기록을 삭제하시겠습니까?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.db_manager.delete_consultation(consultation_id):
                QMessageBox.information(self, "성공", "면담 기록이 삭제되었습니다.")
                self.load_consultations()
                self.clear_form()
            else:
                QMessageBox.critical(self, "오류", "면담 기록 삭제에 실패했습니다.")
    
    def show_upcoming_consultations(self):
        """예정된 면담 표시"""
        consultations = self.db_manager.get_upcoming_consultations()
        
        if not consultations:
            QMessageBox.information(self, "알림", "예정된 면담이 없습니다.")
            return
        
        # 예정 면담 표시
        self.populate_table(consultations)
        QMessageBox.information(self, "예정 면담", f"{len(consultations)}건의 예정된 면담이 있습니다.")
    
    def generate_report(self):
        """면담일지 출력 - GPT API 연동"""
        if not self.current_consultation_id:
            QMessageBox.warning(self, "경고", "먼저 면담 기록을 선택하거나 저장하세요.")
            return
        
        # 면담일지 출력 다이얼로그 표시
        from .consultation_report_dialog import ConsultationReportDialog
        dialog = ConsultationReportDialog(self.db_manager, self.current_consultation_id, self)
        dialog.exec_()
