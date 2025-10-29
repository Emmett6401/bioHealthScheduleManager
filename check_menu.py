#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
면담 관리 메뉴 확인 스크립트
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'pyqt5_app'))

def check_menu():
    """메뉴 확인"""
    print("=" * 60)
    print("면담 관리 메뉴 확인")
    print("=" * 60)
    
    # 파일 확인
    main_file = 'pyqt5_app/ui/kdt_main_window_full.py'
    if os.path.exists(main_file):
        print(f"✅ {main_file} 존재")
        
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            if '학생 면담 관리' in content:
                print("✅ '학생 면담 관리' 메뉴 텍스트 발견")
            else:
                print("❌ '학생 면담 관리' 메뉴 텍스트 없음")
            
            if 'show_consultation_dialog' in content:
                print("✅ 'show_consultation_dialog' 메서드 발견")
            else:
                print("❌ 'show_consultation_dialog' 메서드 없음")
            
            if 'consultation_action' in content:
                print("✅ 'consultation_action' 액션 발견")
            else:
                print("❌ 'consultation_action' 액션 없음")
    else:
        print(f"❌ {main_file} 없음")
    
    print()
    
    # UI 파일 확인
    dialog_file = 'pyqt5_app/ui/consultation_dialog.py'
    if os.path.exists(dialog_file):
        print(f"✅ {dialog_file} 존재")
        size = os.path.getsize(dialog_file)
        print(f"   파일 크기: {size:,} bytes")
    else:
        print(f"❌ {dialog_file} 없음")
    
    report_file = 'pyqt5_app/ui/consultation_report_dialog.py'
    if os.path.exists(report_file):
        print(f"✅ {report_file} 존재")
        size = os.path.getsize(report_file)
        print(f"   파일 크기: {size:,} bytes")
    else:
        print(f"❌ {report_file} 없음")
    
    print()
    
    # import 테스트
    print("Import 테스트:")
    try:
        from ui.consultation_dialog import ConsultationDialog
        print("✅ ConsultationDialog import 성공")
    except Exception as e:
        print(f"❌ ConsultationDialog import 실패: {e}")
    
    try:
        from ui.consultation_report_dialog import ConsultationReportDialog
        print("✅ ConsultationReportDialog import 성공")
    except Exception as e:
        print(f"❌ ConsultationReportDialog import 실패: {e}")
    
    print()
    print("=" * 60)
    print("실행 방법:")
    print("=" * 60)
    print("cd /home/user/webapp_consultation/pyqt5_app")
    print("python main_kdt_full.py")
    print()
    print("메뉴 위치:")
    print("상단 메뉴바 → 과정 관리 → 학생 면담 관리")
    print("=" * 60)

if __name__ == "__main__":
    check_menu()
