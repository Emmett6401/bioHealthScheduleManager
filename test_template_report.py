#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
템플릿 기반 면담일지 생성 테스트
"""

from datetime import datetime

# 테스트용 면담 데이터
test_data = {
    'student_name': '김철수',
    'student_code': 'S2024001',
    'consultation_date': datetime(2024, 10, 29, 14, 30),
    'location': '상담실',
    'consultation_type': '정기 면담',
    'consultant_name': '박선생',
    'main_topic': '진로 및 학업 계획',
    'content': '학생이 컴퓨터공학 분야에 관심이 있으며, Python 프로그래밍을 독학하고 있습니다. 최근 프로젝트 경험을 통해 자신감을 얻었으나, 수학 과목에서 어려움을 겪고 있어 추가 지도가 필요합니다.'
}

# ReportTemplateGenerator 임포트
import sys
sys.path.append('/home/user/webapp')
from pyqt5_app.ui.consultation_report_dialog import ReportTemplateGenerator

def test_template_generation():
    """템플릿 생성 테스트"""
    print("=" * 60)
    print("템플릿 기반 면담일지 생성 테스트")
    print("=" * 60)
    print()
    
    styles = {
        'formal': '공식적',
        'friendly': '친근함',
        'detailed': '상세분석'
    }
    
    for style_key, style_name in styles.items():
        print(f"\n📝 {style_name} 스타일 테스트 중...")
        print("-" * 60)
        
        try:
            if style_key == 'formal':
                report = ReportTemplateGenerator.generate_formal_report(test_data)
            elif style_key == 'friendly':
                report = ReportTemplateGenerator.generate_friendly_report(test_data)
            elif style_key == 'detailed':
                report = ReportTemplateGenerator.generate_detailed_report(test_data)
            
            # 보고서 길이 확인
            lines = report.split('\n')
            print(f"✅ 생성 성공!")
            print(f"   - 총 라인 수: {len(lines)}")
            print(f"   - 총 글자 수: {len(report)}")
            
            # 첫 100자 미리보기
            preview = report[:100].replace('\n', ' ')
            print(f"   - 미리보기: {preview}...")
            
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("=" * 60)

if __name__ == '__main__':
    test_template_generation()
