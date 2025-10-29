#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
학생 면담 관리 시스템 테스트 스크립트
"""

import sys
import os

# 경로 추가
sys.path.append(os.path.join(os.path.dirname(__file__), 'pyqt5_app'))

def test_database_connection():
    """데이터베이스 연결 테스트"""
    print("=" * 60)
    print("1. 데이터베이스 연결 테스트")
    print("=" * 60)
    
    try:
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        if db.connect():
            print("✅ 데이터베이스 연결 성공")
            db.disconnect()
            return True
        else:
            print("❌ 데이터베이스 연결 실패")
            return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def test_consultation_table_exists():
    """면담 테이블 존재 확인"""
    print("\n" + "=" * 60)
    print("2. 면담 테이블 존재 확인")
    print("=" * 60)
    
    try:
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        db.connect()
        
        # consultations 테이블 확인
        result = db.fetch_one("SHOW TABLES LIKE 'consultations'")
        if result:
            print("✅ consultations 테이블 존재")
        else:
            print("⚠️  consultations 테이블 없음 - create_consultation_tables.py를 실행하세요")
        
        # consultation_photos 테이블 확인
        result = db.fetch_one("SHOW TABLES LIKE 'consultation_photos'")
        if result:
            print("✅ consultation_photos 테이블 존재")
        else:
            print("⚠️  consultation_photos 테이블 없음 - create_consultation_tables.py를 실행하세요")
        
        db.disconnect()
        return True
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def test_consultation_methods():
    """면담 관리 메서드 테스트"""
    print("\n" + "=" * 60)
    print("3. 면담 관리 메서드 테스트")
    print("=" * 60)
    
    try:
        from database.db_manager import DatabaseManager
        
        db = DatabaseManager()
        db.connect()
        
        # 메서드 존재 확인
        methods = [
            'add_consultation',
            'update_consultation',
            'delete_consultation',
            'get_consultation',
            'get_consultations_by_student',
            'get_all_consultations',
            'get_upcoming_consultations',
            'add_consultation_photo',
            'delete_consultation_photo',
            'get_consultation_photos',
            'search_consultations'
        ]
        
        all_exist = True
        for method in methods:
            if hasattr(db, method):
                print(f"✅ {method} 메서드 존재")
            else:
                print(f"❌ {method} 메서드 없음")
                all_exist = False
        
        db.disconnect()
        return all_exist
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False

def test_ui_files():
    """UI 파일 존재 확인"""
    print("\n" + "=" * 60)
    print("4. UI 파일 존재 확인")
    print("=" * 60)
    
    files = [
        'pyqt5_app/ui/consultation_dialog.py',
        'pyqt5_app/ui/consultation_report_dialog.py'
    ]
    
    all_exist = True
    for file_path in files:
        full_path = os.path.join(os.path.dirname(__file__), file_path)
        if os.path.exists(full_path):
            print(f"✅ {file_path} 존재")
        else:
            print(f"❌ {file_path} 없음")
            all_exist = False
    
    return all_exist

def test_openai_import():
    """OpenAI 패키지 설치 확인"""
    print("\n" + "=" * 60)
    print("5. OpenAI 패키지 설치 확인")
    print("=" * 60)
    
    try:
        import openai
        print(f"✅ OpenAI 패키지 설치됨 (버전: {openai.__version__})")
        return True
    except ImportError:
        print("⚠️  OpenAI 패키지 미설치 - 'pip install openai' 실행 필요")
        print("   (AI 면담일지 생성 기능 사용 시 필요)")
        return False

def test_config():
    """설정 파일 확인"""
    print("\n" + "=" * 60)
    print("6. 설정 파일 확인")
    print("=" * 60)
    
    try:
        from config import OPENAI_API_KEY
        
        if OPENAI_API_KEY and OPENAI_API_KEY != "your-openai-api-key-here":
            print("✅ OpenAI API 키 설정됨")
        else:
            print("⚠️  OpenAI API 키 미설정")
            print("   config.py 또는 환경 변수 OPENAI_API_KEY 설정 필요")
            print("   (AI 면담일지 생성 기능 사용 시 필요)")
        
        return True
    except Exception as e:
        print(f"⚠️  설정 확인 중 오류: {e}")
        return False

def run_all_tests():
    """모든 테스트 실행"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 12 + "학생 면담 관리 시스템 테스트" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    results = []
    
    results.append(("데이터베이스 연결", test_database_connection()))
    results.append(("면담 테이블", test_consultation_table_exists()))
    results.append(("면담 메서드", test_consultation_methods()))
    results.append(("UI 파일", test_ui_files()))
    results.append(("OpenAI 패키지", test_openai_import()))
    results.append(("설정 파일", test_config()))
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("테스트 결과 요약")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ 통과" if result else "❌ 실패"
        print(f"{name:20s} : {status}")
    
    print("=" * 60)
    print(f"총 {total}개 테스트 중 {passed}개 통과 ({passed/total*100:.1f}%)")
    print("=" * 60)
    
    if passed == total:
        print("\n🎉 모든 테스트 통과! 시스템 사용 준비 완료")
    elif passed >= total - 2:
        print("\n⚠️  일부 선택적 기능 미설정 (기본 기능은 사용 가능)")
    else:
        print("\n❌ 필수 설정이 완료되지 않았습니다")
        print("   - 데이터베이스 테이블: create_consultation_tables.py 실행")
        print("   - 필요 패키지: pip install -r requirements.txt")
    
    print("\n📖 자세한 사용 방법은 CONSULTATION_MANAGEMENT_README.md를 참고하세요\n")

if __name__ == "__main__":
    run_all_tests()
