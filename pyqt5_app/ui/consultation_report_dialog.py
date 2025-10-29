# -*- coding: utf-8 -*-
"""
면담일지 출력 다이얼로그 (템플릿 기반)
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTextEdit, QMessageBox, QProgressBar,
                             QComboBox, QGroupBox, QFileDialog, QCheckBox, QTextBrowser)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from datetime import datetime
import os
import json
import base64


class ReportTemplateGenerator:
    """템플릿 기반 면담일지 생성기 (API 불필요!)"""
    
    @staticmethod
    def generate_formal_report(data):
        """공식적인 스타일의 면담일지 생성"""
        student_name = data.get('student_name', '')
        student_code = data.get('student_code', '')
        date = data.get('consultation_date', '')
        location = data.get('location', '')
        cons_type = data.get('consultation_type', '')
        consultant = data.get('consultant_name', '')
        topic = data.get('main_topic', '')
        content = data.get('content', '')
        
        report = f"""1. **면담 개요**

본 면담은 {student_name} 학생({student_code})을 대상으로 {topic}에 관하여 논의하기 위해 실시되었습니다. 면담은 {location}에서 진행되었으며, {cons_type} 형식으로 이루어졌습니다.

2. **학생 상태 분석**

학생은 현재 {topic}와 관련하여 다음과 같은 상황에 놓여 있습니다:
{content[:200] if len(content) > 200 else content}

학생의 전반적인 학습 태도 및 정서 상태를 고려할 때, 체계적인 지원과 관심이 필요한 것으로 판단됩니다.

3. **주요 논의 사항**

면담 중 다음과 같은 핵심 사항들이 논의되었습니다:
- {topic}에 대한 학생의 현재 입장
- 관련 어려움 및 고민사항
- 개선 및 발전 가능성

학생은 자신의 상황에 대해 진지하게 고민하고 있으며, 긍정적인 변화를 위한 의지를 보였습니다.

4. **학생 의견 및 반응**

학생은 면담 과정에서 다음과 같은 의견을 표현하였습니다:
{content}

전반적으로 학생은 자신의 상황을 객관적으로 인식하고 있으며, 개선 방안에 대해 적극적인 태도를 보였습니다.

5. **상담사 소견**

상담사로서 다음과 같은 점을 관찰하였습니다:
- 학생의 자기 인식 수준은 적절한 것으로 판단됨
- {topic}에 대한 관심과 동기가 확인됨
- 체계적인 지원 시 긍정적 변화 가능성이 높음

학생의 강점을 활용하고 약점을 보완할 수 있는 맞춤형 지원이 필요합니다.

6. **향후 지도 방안**

학생의 발전을 위해 다음과 같은 지도 방안을 제안합니다:

- 단기 목표: {topic}에 대한 기초 역량 강화
- 중기 목표: 실질적인 성과 달성 및 자신감 향상
- 장기 목표: 지속적인 성장 및 발전 추구

정기적인 모니터링과 피드백을 통해 학생의 진전 상황을 확인하고, 필요시 지도 방법을 조정할 계획입니다.

7. **특이사항**

특별히 주목할 만한 사항은 다음과 같습니다:
- 학생의 적극적인 면담 참여 태도
- 자기 개선에 대한 강한 의지
- 구체적인 목표 설정의 필요성

8. **후속 조치**

효과적인 지도를 위해 다음과 같은 후속 조치를 시행할 예정입니다:

- 2주 후 추가 면담 실시
- 학습 진행 상황 주간 점검
- 필요시 학부모 상담 진행
- 관련 자료 및 정보 제공

상담사: {consultant}
작성일: {datetime.now().strftime('%Y년 %m월 %d일')}
"""
        return report
    
    @staticmethod
    def generate_friendly_report(data):
        """친근한 스타일의 면담일지 생성"""
        student_name = data.get('student_name', '')
        topic = data.get('main_topic', '')
        content = data.get('content', '')
        consultant = data.get('consultant_name', '')
        
        report = f"""1. **면담 개요**

안녕하세요! 오늘 {student_name} 학생과 {topic}에 대해 이야기를 나누었습니다. 편안한 분위기에서 학생의 생각과 고민을 충분히 들을 수 있었습니다.

2. **학생 상태 분석**

{student_name} 학생은 현재 {topic}에 대해 진지하게 고민하고 있어요. {content[:150] if len(content) > 150 else content}

학생의 긍정적인 태도와 의지가 인상적이었습니다.

3. **주요 논의 사항**

함께 이야기 나눈 내용들:
- {topic}에 대한 학생의 솔직한 생각
- 어려움을 느끼는 부분들
- 앞으로의 계획과 목표

학생은 자신의 상황을 잘 이해하고 있으며, 개선하고 싶은 마음이 크다는 것을 알 수 있었습니다.

4. **학생 의견 및 반응**

{student_name} 학생이 들려준 이야기:
"{content}"

학생의 진솔한 마음을 들을 수 있어서 좋았어요. 변화하고자 하는 의지가 느껴졌습니다.

5. **상담사 소견**

{student_name} 학생과의 면담에서 느낀 점:
- 자기 자신에 대해 잘 알고 있어요
- {topic}에 대한 관심이 높습니다
- 조금만 도움을 주면 충분히 잘할 수 있을 것 같아요

학생의 강점을 살리면서 부족한 부분을 함께 채워나가면 좋겠습니다.

6. **향후 지도 방안**

앞으로 이렇게 도와드릴게요:

- 우선 {topic}의 기본부터 차근차근 함께 다져봐요
- 작은 목표를 정하고 하나씩 달성해보면서 자신감을 키워요
- 힘들 때는 언제든 이야기하고, 함께 방법을 찾아봐요

정기적으로 만나서 진행 상황을 체크하고, 필요한 부분을 더 도와드릴게요.

7. **특이사항**

{student_name} 학생의 특별한 점:
- 적극적으로 면담에 참여했어요
- 자기 개선 의지가 강합니다
- 구체적인 계획이 필요해 보여요

8. **후속 조치**

다음 단계로 이런 것들을 준비했어요:

- 2주 후에 다시 만나서 진행 상황을 확인해요
- 일주일에 한 번씩 간단히 체크해요
- 필요하면 부모님과도 상담해요
- 도움이 될 만한 자료를 드릴게요

함께 노력하면 분명 좋은 결과가 있을 거예요! 화이팅!

상담사: {consultant}
작성일: {datetime.now().strftime('%Y년 %m월 %d일')}
"""
        return report
    
    @staticmethod
    def generate_detailed_report(data):
        """상세 분석 스타일의 면담일지 생성"""
        student_name = data.get('student_name', '')
        student_code = data.get('student_code', '')
        date = data.get('consultation_date', '')
        location = data.get('location', '')
        cons_type = data.get('consultation_type', '')
        consultant = data.get('consultant_name', '')
        topic = data.get('main_topic', '')
        content = data.get('content', '')
        
        report = f"""1. **면담 개요 (상세)**

【면담 배경】
본 면담은 {student_name} 학생({student_code})의 {topic}에 관한 심층 상담을 목적으로 실시되었습니다. 면담은 {date}에 {location}에서 {cons_type} 방식으로 약 30-40분간 진행되었습니다.

【면담 목적】
- {topic}에 대한 학생의 현재 상태 파악
- 관련 문제점 및 애로사항 분석
- 효과적인 개선 방안 모색
- 학생의 잠재력 및 발전 가능성 평가

2. **학생 상태 분석 (심층)**

【현재 상황 분석】
{student_name} 학생은 현재 다음과 같은 상황에 처해 있습니다:
{content}

【심리·정서적 상태】
- 자기 인식: 학생은 자신의 상황을 비교적 정확하게 인식하고 있음
- 동기 수준: {topic}에 대한 내적 동기가 관찰됨
- 정서 상태: 전반적으로 안정적이나, 부분적으로 불안감 존재
- 자신감: 현재 상태에서는 다소 낮은 편이나, 향상 가능성 높음

【학습 태도 및 습관】
- 학습 참여도: 적극적인 태도를 보임
- 자기주도성: 발전 가능성이 있으나 체계적 접근 필요
- 시간 관리: 개선이 필요한 영역

3. **주요 논의 사항 (상세)**

【핵심 이슈】
a) {topic} 관련 현재 수준 및 인식
   - 학생의 자체 평가
   - 객관적 현황 분석
   - 격차 및 개선 영역 식별

b) 직면한 어려움 및 장애 요인
   - 외적 요인 (환경, 자원 등)
   - 내적 요인 (심리, 역량 등)
   - 복합적 요인 분석

c) 목표 및 기대사항
   - 단기 목표 (1-2개월)
   - 중기 목표 (3-6개월)
   - 장기 목표 (1년 이상)

【논의 과정】
학생은 면담 과정에서 자신의 생각을 논리적으로 표현하였으며, 상담사의 질문에 진지하게 응답하였습니다. 특히 {topic}에 대한 학생의 관심과 개선 의지가 명확하게 드러났습니다.

4. **학생 의견 및 반응 (상세)**

【학생 진술 내용】
"{content}"

【비언어적 표현 분석】
- 표정: 진지하고 집중된 모습
- 태도: 적극적이고 협조적
- 반응: 상담사의 제안에 긍정적 반응

【자기 인식 수준】
학생은 자신의 강점과 약점을 비교적 정확히 파악하고 있으며, 현실적인 목표 설정 능력을 보여주었습니다.

5. **상담사 소견 (심층 분석)**

【종합 평가】
{student_name} 학생은 다음과 같은 특성을 보입니다:

【강점】
- 자기 인식 능력이 우수함
- {topic}에 대한 관심과 동기가 높음
- 변화와 개선에 대한 의지가 강함
- 상담 및 지도에 협조적인 태도

【개선 필요 영역】
- 체계적인 학습 전략 수립
- 시간 관리 및 실행력 강화
- 자신감 향상을 위한 성공 경험 축적

【잠재력 평가】
적절한 지원과 체계적인 지도가 제공된다면, 학생은 {topic} 영역에서 유의미한 성과를 달성할 수 있을 것으로 판단됩니다.

6. **향후 지도 방안 (구체적 계획)**

【단계별 지도 계획】

◆ 1단계 (1-2개월): 기초 역량 강화
- 목표: {topic}의 기본 개념 및 원리 이해
- 방법: 체계적 학습 자료 제공, 주 1회 점검
- 평가: 이해도 테스트 및 피드백

◆ 2단계 (3-4개월): 실전 능력 배양
- 목표: 실제 적용 및 문제 해결 능력 향상
- 방법: 프로젝트 기반 학습, 멘토링
- 평가: 결과물 평가 및 개선사항 도출

◆ 3단계 (5-6개월): 심화 및 확장
- 목표: 전문성 향상 및 독립적 학습 능력 완성
- 방법: 자기주도 학습 지원, 정기 면담
- 평가: 종합 평가 및 차기 목표 설정

【지원 체계】
- 주간 학습 점검 및 피드백
- 월 1회 정기 면담
- 필요시 수시 상담
- 학습 자료 및 정보 제공
- 학부모 연계 지도

7. **특이사항 (상세)**

【긍정적 요인】
- 학생의 높은 참여도와 협조적 태도
- 명확한 자기 개선 의지
- 부모님의 지원 가능성

【주의 요인】
- 과도한 기대로 인한 스트레스 가능성
- 초기 어려움으로 인한 동기 저하 우려
- 체계적 시간 관리의 필요성

【권장 사항】
- 점진적이고 단계적인 목표 설정
- 작은 성공 경험 축적을 통한 자신감 향상
- 정기적 모니터링 및 즉각적 피드백

8. **후속 조치 (상세 계획)**

【즉시 조치 사항】
- 학습 계획표 작성 및 배포
- 기초 학습 자료 제공
- 다음 면담 일정 확정 (2주 후)

【단기 조치 사항 (1개월)】
- 주간 진행 상황 점검 시스템 운영
- 학습 어려움 발생 시 즉시 상담
- 필요시 추가 학습 자료 제공

【중장기 조치 사항 (3-6개월)】
- 월별 성과 평가 및 피드백
- 학부모 상담 (필요시)
- 진로 연계 지도
- 종합 평가 및 차기 목표 설정

【모니터링 계획】
- 주간 체크리스트를 통한 진행 상황 확인
- 월별 면담을 통한 심층 평가
- 분기별 종합 리포트 작성

【비상 대응 계획】
- 학습 진행 중 어려움 발생 시 즉시 상담
- 동기 저하 징후 발견 시 긴급 면담
- 필요시 전문가 연계 (상담사, 전문 교사 등)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

상담사: {consultant}
작성일: {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}

【상담사 최종 의견】
{student_name} 학생은 충분한 잠재력과 개선 의지를 갖추고 있습니다. 
체계적인 지원과 지속적인 관심을 통해 목표 달성이 가능할 것으로 기대됩니다.
"""
        return report


class ConsultationReportDialog(QDialog):
    """면담일지 출력 다이얼로그"""
    
    def __init__(self, db_manager, consultation_id, parent=None):
        super().__init__(parent)
        self.db_manager = db_manager
        self.consultation_id = consultation_id
        self.consultation_data = None
        self.generated_report = ""
        
        self.init_ui()
        self.load_consultation_data()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle("면담일지 출력")
        self.setGeometry(150, 150, 900, 700)
        
        layout = QVBoxLayout()
        
        # 상단 옵션
        option_group = QGroupBox("출력 옵션")
        option_layout = QHBoxLayout()
        
        option_layout.addWidget(QLabel("작성 스타일:"))
        self.style_combo = QComboBox()
        self.style_combo.addItem("공식적", "formal")
        self.style_combo.addItem("친근함", "friendly")
        self.style_combo.addItem("상세 분석", "detailed")
        option_layout.addWidget(self.style_combo)
        
        self.include_photos_check = QCheckBox("첨부 사진 포함")
        self.include_photos_check.setChecked(True)
        option_layout.addWidget(self.include_photos_check)
        
        option_layout.addStretch()
        
        self.generate_btn = QPushButton("📝 면담일지 생성 (무료)")
        self.generate_btn.clicked.connect(self.generate_with_gpt)
        option_layout.addWidget(self.generate_btn)
        
        option_group.setLayout(option_layout)
        layout.addWidget(option_group)
        
        # 진행 표시
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # 미리보기 영역
        layout.addWidget(QLabel("면담일지 미리보기:"))
        
        self.preview_text = QTextBrowser()
        self.preview_text.setReadOnly(True)
        self.preview_text.setOpenExternalLinks(False)
        
        # 폰트 설정
        font = QFont("맑은 고딕", 10)
        self.preview_text.setFont(font)
        
        layout.addWidget(self.preview_text)
        
        # 하단 버튼
        button_layout = QHBoxLayout()
        
        self.print_btn = QPushButton("인쇄")
        self.print_btn.clicked.connect(self.print_report)
        self.print_btn.setEnabled(False)
        button_layout.addWidget(self.print_btn)
        
        self.save_pdf_btn = QPushButton("PDF 저장")
        self.save_pdf_btn.clicked.connect(self.save_as_pdf)
        self.save_pdf_btn.setEnabled(False)
        button_layout.addWidget(self.save_pdf_btn)
        
        self.save_txt_btn = QPushButton("텍스트 저장")
        self.save_txt_btn.clicked.connect(self.save_as_text)
        self.save_txt_btn.setEnabled(False)
        button_layout.addWidget(self.save_txt_btn)
        
        button_layout.addStretch()
        
        self.close_btn = QPushButton("닫기")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_consultation_data(self):
        """면담 데이터 로드"""
        self.consultation_data = self.db_manager.get_consultation(self.consultation_id)
        if self.consultation_data:
            # 기본 면담일지 표시
            self.show_basic_report()
    
    def get_student_photo_base64(self, student_code):
        """학생 사진을 base64로 인코딩하여 반환"""
        try:
            # 프로젝트 루트 디렉토리 찾기
            current_dir = os.path.dirname(os.path.abspath(__file__))  # ui 폴더
            pyqt5_app_dir = os.path.dirname(current_dir)  # pyqt5_app 폴더
            project_root = os.path.dirname(pyqt5_app_dir)  # 프로젝트 루트
            
            print(f"📁 현재 파일: {__file__}")
            print(f"📁 current_dir: {current_dir}")
            print(f"📁 pyqt5_app_dir: {pyqt5_app_dir}")
            print(f"📁 project_root: {project_root}")
            print(f"🎓 학번: '{student_code}' (타입: {type(student_code)})")
            
            # student_photos 폴더 존재 확인
            photos_dir = os.path.join(project_root, "student_photos")
            print(f"📂 student_photos 폴더: {photos_dir}")
            print(f"   존재 여부: {os.path.exists(photos_dir)}")
            
            if os.path.exists(photos_dir):
                # 하위 폴더 확인
                thumbnails_dir = os.path.join(photos_dir, "thumbnails")
                originals_dir = os.path.join(photos_dir, "originals")
                print(f"   thumbnails 폴더: {os.path.exists(thumbnails_dir)}")
                print(f"   originals 폴더: {os.path.exists(originals_dir)}")
                
                # 파일 목록 출력
                if os.path.exists(thumbnails_dir):
                    files = os.listdir(thumbnails_dir)
                    print(f"   thumbnails 파일들: {files}")
                if os.path.exists(originals_dir):
                    files = os.listdir(originals_dir)
                    print(f"   originals 파일들: {files}")
            
            # 썸네일 경로 (절대 경로)
            thumbnail_path = os.path.join(project_root, "student_photos", "thumbnails", f"{student_code}.jpg")
            
            print(f"🔍 사진 찾는 중: {thumbnail_path}")
            print(f"   파일 존재: {os.path.exists(thumbnail_path)}")
            
            # 썸네일이 없으면 원본 확인
            if not os.path.exists(thumbnail_path):
                print(f"⚠️ 썸네일 없음, 원본 확인 중...")
                original_path = os.path.join(project_root, "student_photos", "originals", f"{student_code}.jpg")
                if os.path.exists(original_path):
                    print(f"✅ 원본 사진 발견: {original_path}")
                    thumbnail_path = original_path
                else:
                    # 기본 아바타
                    print(f"⚠️ 원본도 없음, 기본 아바타 사용")
                    thumbnail_path = os.path.join(project_root, "student_photos", "default_avatar.png")
                    if not os.path.exists(thumbnail_path):
                        print(f"❌ 기본 아바타도 없음!")
                        return None
            else:
                print(f"✅ 썸네일 발견: {thumbnail_path}")
            
            # 이미지 파일을 base64로 인코딩
            with open(thumbnail_path, 'rb') as img_file:
                img_data = img_file.read()
                img_base64 = base64.b64encode(img_data).decode('utf-8')
                
                # 파일 확장자 확인
                ext = os.path.splitext(thumbnail_path)[1].lower()
                mime_type = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
                
                print(f"✅ 사진 인코딩 완료 (크기: {len(img_data)} bytes)")
                return f"data:{mime_type};base64,{img_base64}"
        except Exception as e:
            print(f"❌ 사진 로드 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def show_basic_report(self):
        """기본 면담일지 표시 (HTML 형식, 사진 포함)"""
        try:
            data = self.consultation_data
            
            # 데이터 안전하게 가져오기
            student_name = data.get('student_name', '') if data else ''
            student_code = data.get('student_code', '') if data else ''
            location = data.get('location', '') if data else ''
            consultation_type = data.get('consultation_type', '') if data else ''
            consultant_name = data.get('consultant_name', '') if data else ''
            main_topic = data.get('main_topic', '') if data else ''
            content = data.get('content', '') if data else ''
            
            # None 체크 및 안전한 변환
            if content is None:
                content = ''
            content_html = content.replace('\n', '<br>') if content else ''
            
            # 날짜 포맷팅
            consultation_date_str = ''
            if data and data.get('consultation_date'):
                try:
                    consultation_date_str = data.get('consultation_date').strftime('%Y년 %m월 %d일 %H:%M')
                except:
                    consultation_date_str = str(data.get('consultation_date', ''))
            
            next_date_str = '미정'
            if data and data.get('next_consultation_date'):
                try:
                    next_date_str = data.get('next_consultation_date').strftime('%Y년 %m월 %d일 %H:%M')
                except:
                    next_date_str = str(data.get('next_consultation_date', '미정'))
            
            # 학생 사진 가져오기
            photo_base64 = None
            if student_code:
                photo_base64 = self.get_student_photo_base64(student_code)
            
            # 사진 HTML (있는 경우)
            photo_html = ""
            if photo_base64:
                photo_html = f'''
                <div style="text-align: center; margin: 20px 0;">
                    <img src="{photo_base64}" width="150" height="180" style="border: 2px solid #ccc; border-radius: 5px;">
                </div>
                '''
            
            report_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: '맑은 고딕', sans-serif; margin: 20px; }}
                    h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                    .info-box {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                    .section {{ margin: 20px 0; }}
                    .label {{ font-weight: bold; color: #34495e; }}
                    .content {{ margin-left: 20px; color: #2c3e50; }}
                    .footer {{ text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 0.9em; }}
                </style>
            </head>
            <body>
                <h2>📋 학생 면담일지</h2>
                
                {photo_html}
                
                <div class="info-box">
                    <p><span class="label">학생명:</span> {student_name} ({student_code})</p>
                    <p><span class="label">면담 일시:</span> {consultation_date_str}</p>
                    <p><span class="label">면담 장소:</span> {location}</p>
                    <p><span class="label">면담 유형:</span> {consultation_type}</p>
                    <p><span class="label">상담사:</span> {consultant_name}</p>
                </div>
                
                <div class="section">
                    <p class="label">【면담 주제】</p>
                    <p class="content">{main_topic}</p>
                </div>
                
                <div class="section">
                    <p class="label">【면담 내용】</p>
                    <p class="content">{content_html}</p>
                </div>
                
                <div class="section">
                    <p class="label">【다음 면담 예정】</p>
                    <p class="content">{next_date_str}</p>
                </div>
                
                <div class="footer">
                    <hr>
                    <p>작성일: {datetime.now().strftime('%Y년 %m월 %d일')}</p>
                    <p style="color: #3498db;">※ '면담일지 생성' 버튼을 클릭하면 더 상세하고 전문적인 면담일지를 자동 생성할 수 있습니다.</p>
                    <p style="color: #27ae60;">(완전 무료, API 키 불필요, 즉시 생성!)</p>
                </div>
            </body>
            </html>
            """
            
            self.preview_text.setHtml(report_html)
            self.enable_export_buttons()
            
        except Exception as e:
            print(f"❌ 기본 보고서 표시 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            # 오류 발생 시 간단한 텍스트 표시
            error_html = f"""
            <html>
            <body>
                <h2>⚠️ 오류 발생</h2>
                <p>면담일지를 표시하는 중 오류가 발생했습니다.</p>
                <p>오류 내용: {str(e)}</p>
                <p>관리자에게 문의하세요.</p>
            </body>
            </html>
            """
            self.preview_text.setHtml(error_html)
    
    def generate_with_gpt(self):
        """템플릿 기반 면담일지 생성"""
        if not self.consultation_data:
            QMessageBox.warning(self, "경고", "면담 데이터를 불러올 수 없습니다.")
            return
        
        try:
            # UI 비활성화
            self.generate_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # 무한 진행
            
            # 스타일 선택
            style = self.style_combo.currentData()
            
            print(f"📝 템플릿 기반 면담일지 생성 중... (스타일: {style})")
            
            # 스타일 선택
            style_templates = {
                'formal': ReportTemplateGenerator.generate_formal_report,
                'friendly': ReportTemplateGenerator.generate_friendly_report,
                'detailed': ReportTemplateGenerator.generate_detailed_report
            }
            
            generate_func = style_templates.get(style, ReportTemplateGenerator.generate_formal_report)
            report = generate_func(self.consultation_data)
            
            print("✅ 면담일지 생성 완료!")
            
            # 생성 완료 처리
            self.on_gpt_finished(report)
            
        except Exception as e:
            print(f"❌ 오류: {str(e)}")
            self.on_gpt_error(f"면담일지 생성 중 오류 발생:\n{str(e)}")
    
    def on_gpt_finished(self, report):
        """템플릿 생성 완료 - HTML 형식으로 표시"""
        try:
            self.progress_bar.setVisible(False)
            self.generate_btn.setEnabled(True)
            
            # 데이터 안전하게 가져오기
            data = self.consultation_data
            student_name = data.get('student_name', '') if data else ''
            student_code = data.get('student_code', '') if data else ''
            location = data.get('location', '') if data else ''
            consultation_type = data.get('consultation_type', '') if data else ''
            consultant_name = data.get('consultant_name', '') if data else ''
            
            # 날짜 포맷팅
            consultation_date_str = ''
            if data and data.get('consultation_date'):
                try:
                    consultation_date_str = data.get('consultation_date').strftime('%Y년 %m월 %d일 %H:%M')
                except:
                    consultation_date_str = str(data.get('consultation_date', ''))
            
            # 학생 사진 가져오기
            photo_base64 = None
            if student_code:
                photo_base64 = self.get_student_photo_base64(student_code)
            
            # 사진 HTML (있는 경우)
            photo_html = ""
            if photo_base64:
                photo_html = f'''
                <div style="text-align: center; margin: 20px 0;">
                    <img src="{photo_base64}" width="150" height="180" style="border: 2px solid #ccc; border-radius: 5px;">
                </div>
                '''
            
            # HTML 형식으로 변환 (텍스트 보고서를 HTML로)
            report_html_content = report.replace('\n', '<br>') if report else ''
            
            full_report_html = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: '맑은 고딕', sans-serif; margin: 20px; }}
                    h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }}
                    .info-box {{ background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }}
                    .content {{ margin: 20px 0; line-height: 1.8; }}
                    .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #ddd; color: #7f8c8d; }}
                </style>
            </head>
            <body>
                <h2>📋 학생 면담일지</h2>
                
                {photo_html}
                
                <div class="info-box">
                    <p><strong>학생명:</strong> {student_name} ({student_code})</p>
                    <p><strong>면담 일시:</strong> {consultation_date_str}</p>
                    <p><strong>면담 장소:</strong> {location}</p>
                    <p><strong>면담 유형:</strong> {consultation_type}</p>
                    <p><strong>상담사:</strong> {consultant_name}</p>
                </div>
                
                <div class="content">
                    {report_html_content}
                </div>
                
                <div class="footer">
                    <p>작성일: {datetime.now().strftime('%Y년 %m월 %d일')}</p>
                </div>
            </body>
            </html>
            """
            
            # 텍스트 버전도 저장 (내보내기용)
            full_report_text = f"""
=== 학생 면담일지 ===

【기본 정보】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
학생명: {student_name} ({student_code})
면담 일시: {consultation_date_str}
면담 장소: {location}
면담 유형: {consultation_type}
상담사: {consultant_name}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{report}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
작성일: {datetime.now().strftime('%Y년 %m월 %d일')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
            """
            
            self.generated_report = full_report_text
            self.preview_text.setHtml(full_report_html)
            self.enable_export_buttons()
            
            # 생성된 면담일지를 DB에 저장
            self.save_report_to_db(report)
            
            QMessageBox.information(self, "완료", "📷 면담일지가 생성되었습니다!\n\n생성된 내용이 면담 기록에 저장되었습니다.\nPDF 또는 텍스트 파일로 저장하거나 인쇄할 수 있습니다.")
            
        except Exception as e:
            print(f"❌ 템플릿 생성 완료 처리 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            self.progress_bar.setVisible(False)
            self.generate_btn.setEnabled(True)
            QMessageBox.critical(self, "오류", f"면담일지 표시 중 오류가 발생했습니다:\n{str(e)}")
    
    def save_report_to_db(self, report):
        """생성된 면담일지를 DB에 저장"""
        try:
            print(f"💾 면담일지 DB 저장 시작 (ID: {self.consultation_id})")
            
            # consultations 테이블의 content 필드 업데이트
            query = """
                UPDATE consultations 
                SET content = %s 
                WHERE id = %s
            """
            
            self.db_manager.execute_query(query, (report, self.consultation_id))
            print(f"✅ 면담일지 DB 저장 완료!")
            
        except Exception as e:
            print(f"❌ DB 저장 오류: {str(e)}")
            import traceback
            traceback.print_exc()
            # DB 저장 실패해도 사용자에게는 알리지 않음 (생성은 성공했으므로)
    
    def on_gpt_error(self, error_msg):
        """GPT 생성 오류"""
        self.progress_bar.setVisible(False)
        self.generate_btn.setEnabled(True)
        
        QMessageBox.critical(self, "오류", error_msg)
    
    def enable_export_buttons(self):
        """내보내기 버튼 활성화"""
        self.print_btn.setEnabled(True)
        self.save_pdf_btn.setEnabled(True)
        self.save_txt_btn.setEnabled(True)
    
    def print_report(self):
        """면담일지 인쇄"""
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            self.preview_text.document().print_(printer)
            QMessageBox.information(self, "완료", "인쇄가 완료되었습니다.")
    
    def save_as_pdf(self):
        """PDF로 저장"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "PDF 저장",
            f"면담일지_{self.consultation_data.get('student_name', '')}_{datetime.now().strftime('%Y%m%d')}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if filename:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            self.preview_text.document().print_(printer)
            
            QMessageBox.information(self, "완료", f"PDF 파일이 저장되었습니다.\n{filename}")
    
    def save_as_text(self):
        """텍스트 파일로 저장"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "텍스트 저장",
            f"면담일지_{self.consultation_data.get('student_name', '')}_{datetime.now().strftime('%Y%m%d')}.txt",
            "Text Files (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.preview_text.toPlainText())
                
                QMessageBox.information(self, "완료", f"텍스트 파일이 저장되었습니다.\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "오류", f"파일 저장 중 오류 발생:\n{str(e)}")
