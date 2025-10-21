# -*- coding: utf-8 -*-
"""
PDF 보고서 생성 유틸리티
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import os


class PDFGenerator:
    """PDF 보고서 생성기"""
    
    def __init__(self):
        # 한글 폰트 설정 (시스템에 따라 경로가 다를 수 있음)
        try:
            # Windows
            font_path = "C:/Windows/Fonts/malgun.ttf"
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('MalgunGothic', font_path))
                self.font_name = 'MalgunGothic'
            else:
                self.font_name = 'Helvetica'
        except:
            self.font_name = 'Helvetica'
    
    def generate_timetable_report(self, course_data, timetable_data, filename="시간표"):
        """시간표 보고서 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{filename}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(final_filename, pagesize=A4)
        elements = []
        
        # 스타일 설정
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=self.font_name,
            fontSize=24,
            textColor=colors.HexColor('#2962FF'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName=self.font_name,
            fontSize=14,
            textColor=colors.HexColor('#333333'),
            spaceAfter=12
        )
        
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=self.font_name,
            fontSize=10
        )
        
        # 제목
        title = Paragraph("교육 과정 시간표", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # 과정 정보
        course_info = [
            ["과정명", course_data.get('name', '-')],
            ["과정 코드", course_data.get('code', '-')],
            ["강의 시수", f"{course_data.get('lecture_hours', 0)} 시간"],
            ["프로젝트 시수", f"{course_data.get('project_hours', 0)} 시간"],
            ["인턴쉽 시수", f"{course_data.get('internship_hours', 0)} 시간"],
            ["인원", f"{course_data.get('capacity', 0)} 명"],
            ["장소", course_data.get('location', '-')],
            ["생성일", datetime.now().strftime("%Y-%m-%d %H:%M")]
        ]
        
        info_table = Table(course_info, colWidths=[4*cm, 12*cm])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#E3F2FD')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey)
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 1*cm))
        
        # 시간표 제목
        timetable_heading = Paragraph("상세 시간표", heading_style)
        elements.append(timetable_heading)
        elements.append(Spacer(1, 0.3*cm))
        
        # 시간표 테이블
        table_data = [["날짜", "시작", "종료", "교과목", "강사", "유형", "비고"]]
        
        type_map = {"lecture": "강의", "project": "프로젝트", "internship": "인턴쉽"}
        
        for row in timetable_data:
            table_data.append([
                str(row.get('class_date', '-')),
                str(row.get('start_time', '-'))[:5],
                str(row.get('end_time', '-'))[:5],
                row.get('subject_name', '-') or '-',
                row.get('instructor_name', '-') or '-',
                type_map.get(row.get('type'), row.get('type', '-')),
                row.get('notes', '-') or '-'
            ])
        
        timetable_table = Table(table_data, colWidths=[2.5*cm, 1.5*cm, 1.5*cm, 3.5*cm, 2.5*cm, 2*cm, 3*cm])
        timetable_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2962FF')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 11),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')])
        ]))
        
        elements.append(timetable_table)
        
        # PDF 생성
        doc.build(elements)
        
        return final_filename
    
    def generate_attendance_sheet(self, course_data, students, dates, filename="출석부"):
        """출석부 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{filename}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(final_filename, pagesize=A4, 
                               topMargin=1*cm, bottomMargin=1*cm,
                               leftMargin=1*cm, rightMargin=1*cm)
        elements = []
        
        # 스타일
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontName=self.font_name,
            fontSize=18,
            alignment=TA_CENTER
        )
        
        # 제목
        title = Paragraph(f"출석부 - {course_data.get('name', '')}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # 출석부 테이블
        # 헤더: 이름 + 날짜들
        header = ["번호", "이름"] + [str(d)[-5:] for d in dates[:20]]  # 최대 20일
        table_data = [header]
        
        # 학생 행
        for idx, student in enumerate(students, 1):
            row = [str(idx), student.get('name', '-')]
            row.extend([''] * len(dates[:20]))  # 빈 출석 칸
            table_data.append(row)
        
        # 컬럼 너비
        col_widths = [1*cm, 3*cm] + [0.7*cm] * len(dates[:20])
        
        attendance_table = Table(table_data, colWidths=col_widths)
        attendance_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F1F8E9')])
        ]))
        
        elements.append(attendance_table)
        
        # PDF 생성
        doc.build(elements)
        
        return final_filename
    
    def generate_grade_sheet(self, course_data, students, subjects, filename="성적표"):
        """성적표 생성"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_filename = f"{filename}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(final_filename, pagesize=A4)
        elements = []
        
        # 스타일
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'Title',
            parent=styles['Heading1'],
            fontName=self.font_name,
            fontSize=18,
            alignment=TA_CENTER
        )
        
        # 제목
        title = Paragraph(f"성적표 - {course_data.get('name', '')}", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.5*cm))
        
        # 성적표 테이블
        header = ["번호", "이름"] + [s.get('name', '-')[:6] for s in subjects[:10]] + ["평균", "등급"]
        table_data = [header]
        
        # 학생 행
        for idx, student in enumerate(students, 1):
            row = [str(idx), student.get('name', '-')]
            row.extend([''] * (len(subjects[:10]) + 2))  # 빈 성적 칸
            table_data.append(row)
        
        # 컬럼 너비
        col_widths = [1*cm, 3*cm] + [1.5*cm] * len(subjects[:10]) + [1.5*cm, 1.5*cm]
        
        grade_table = Table(table_data, colWidths=col_widths)
        grade_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#FF9800')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#FFF3E0')])
        ]))
        
        elements.append(grade_table)
        
        # PDF 생성
        doc.build(elements)
        
        return final_filename
