# -*- coding: utf-8 -*-
"""
Excel 관리 유틸리티
"""

import pandas as pd
from datetime import datetime
import os


class ExcelManager:
    """Excel 내보내기/가져오기 관리"""
    
    @staticmethod
    def export_to_excel(data, filename, sheet_name='Sheet1'):
        """데이터를 Excel로 내보내기"""
        try:
            df = pd.DataFrame(data)
            
            # 파일명에 타임스탬프 추가
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = os.path.splitext(filename)[0]
            final_filename = f"{base_name}_{timestamp}.xlsx"
            
            # Excel 파일로 저장
            writer = pd.ExcelWriter(final_filename, engine='xlsxwriter')
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # 포맷팅
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]
            
            # 헤더 포맷
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#4472C4',
                'font_color': 'white',
                'border': 1
            })
            
            # 셀 포맷
            cell_format = workbook.add_format({
                'border': 1
            })
            
            # 헤더 스타일 적용
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
            
            # 열 너비 자동 조정
            for idx, col in enumerate(df.columns):
                max_len = max(
                    df[col].astype(str).apply(len).max(),
                    len(str(col))
                ) + 2
                worksheet.set_column(idx, idx, min(max_len, 50))
            
            writer.close()
            
            return final_filename
            
        except Exception as e:
            raise Exception(f"Excel 내보내기 실패: {str(e)}")
    
    @staticmethod
    def import_from_excel(filename, sheet_name=0):
        """Excel에서 데이터 가져오기"""
        try:
            df = pd.read_excel(filename, sheet_name=sheet_name)
            
            # NaN을 빈 문자열로 변환
            df = df.fillna('')
            
            # 딕셔너리 리스트로 변환
            data = df.to_dict('records')
            
            return data
            
        except Exception as e:
            raise Exception(f"Excel 가져오기 실패: {str(e)}")
    
    @staticmethod
    def export_timetable(timetable_data, filename="시간표"):
        """시간표 Excel 내보내기"""
        return ExcelManager.export_to_excel(timetable_data, filename, '시간표')
    
    @staticmethod
    def export_instructors(instructor_data, filename="강사목록"):
        """강사 목록 Excel 내보내기"""
        return ExcelManager.export_to_excel(instructor_data, filename, '강사목록')
    
    @staticmethod
    def export_subjects(subject_data, filename="교과목목록"):
        """교과목 목록 Excel 내보내기"""
        return ExcelManager.export_to_excel(subject_data, filename, '교과목목록')
    
    @staticmethod
    def export_projects(project_data, filename="프로젝트목록"):
        """프로젝트 목록 Excel 내보내기"""
        return ExcelManager.export_to_excel(project_data, filename, '프로젝트목록')
