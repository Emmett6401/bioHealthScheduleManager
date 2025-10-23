#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
시간표 생성 알고리즘 테스트
"""

import os
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

from PyQt5.QtWidgets import QApplication
import sys
from ui.timetable_create_dialog import TimetableCreateDialog
from datetime import date, timedelta

# QApplication 생성
app = QApplication(sys.argv)

# 테스트 과목 데이터 (총 156시간)
subjects = [
    {'code': 'S001', 'name': '파이썬 기초', 'hours': 24, 
     'main_instructor_name': '김강사', 'assistant_instructor_name': '이조교', 'reserve_instructor_name': '박예비'},
    {'code': 'S002', 'name': '데이터베이스', 'hours': 20,
     'main_instructor_name': '최강사', 'assistant_instructor_name': '정조교', 'reserve_instructor_name': '한예비'},
    {'code': 'S003', 'name': '웹 개발', 'hours': 64,
     'main_instructor_name': '강강사', 'assistant_instructor_name': '송조교', 'reserve_instructor_name': '유예비'},
    {'code': 'S004', 'name': '머신러닝', 'hours': 48,
     'main_instructor_name': '임강사', 'assistant_instructor_name': '오조교', 'reserve_instructor_name': '전예비'},
]

# 테스트 실행
dialog = TimetableCreateDialog()
dialog.subjects = subjects
dialog.holidays = set()

start_date = date(2025, 1, 6)  # 월요일
end_date = start_date + timedelta(days=100)

print("=" * 70)
print("시간표 생성 알고리즘 테스트")
print("=" * 70)
print()

timetable = dialog.create_timetable(start_date, end_date)

print(f'\n총 {len(timetable)}일 생성됨')
print()

# 1일 1과목 원칙 검증
print("=" * 70)
print("1일 1과목 원칙 검증 (처음 25일)")
print("=" * 70)

violations = []
for i, entry in enumerate(timetable[:25], 1):
    am = entry['am_subject']
    pm = entry['pm_subject']
    date_str = entry['date'].strftime('%Y-%m-%d (%a)')
    
    if am['code'] == pm['code']:
        status = '✓'
    elif pm['name'] == '휴강' or am['name'] == '휴강':
        # 휴강(no class)은 위반으로 보지 않음 (마지막 과목 완료 시)
        status = '✓ (휴강)'
    else:
        status = f'⚠️'
        violations.append({
            'day': i,
            'date': date_str,
            'am': am['name'],
            'pm': pm['name']
        })
    
    print(f'{i:2}. {date_str} {status}')
    print(f'    AM: {am["name"]:20} {am["hours"]}h')
    print(f'    PM: {pm["name"]:20} {pm["hours"]}h')

# 총 시수 확인
total_used = {}
for entry in timetable:
    am = entry['am_subject']
    pm = entry['pm_subject']
    
    if am['code'] not in total_used:
        total_used[am['code']] = 0
    total_used[am['code']] += am['hours']
    
    if pm['code'] not in total_used:
        total_used[pm['code']] = 0
    total_used[pm['code']] += pm['hours']

print()
print("=" * 70)
print("총 시수 사용 현황")
print("=" * 70)

total_expected = 0
total_actual = 0
for subject in subjects:
    used = total_used.get(subject['code'], 0)
    expected = subject['hours']
    total_expected += expected
    total_actual += used
    
    if used == expected:
        status = '✓'
    else:
        status = f'✗ (부족: {expected - used}h)'
    
    print(f'{subject["name"]:15} {used:3}h / {expected:3}h  {status}')

print()
print(f'총계: {total_actual}h / {total_expected}h')

# 위반 사항 요약
if violations:
    print()
    print("=" * 70)
    print("⚠️  1일 1과목 원칙 위반 사항")
    print("=" * 70)
    for v in violations:
        print(f'{v["day"]:2}일차 ({v["date"]}): {v["am"][:10]} → {v["pm"][:10]}')
    print()
    print("설명: 오전에 과목이 끝나고 오후에 다른 과목이 시작됨")
    print("      → 다음날은 오후에 시작한 과목으로 계속되어야 함")
else:
    print()
    print("=" * 70)
    print("✓ 1일 1과목 원칙 모두 준수!")
    print("=" * 70)

# 결과 요약
print()
print("=" * 70)
print("테스트 결과 요약")
print("=" * 70)
print(f'총 일수: {len(timetable)}일')
print(f'총 시수: {total_actual}h / {total_expected}h')
print(f'원칙 위반: {len(violations)}건')

if total_actual == total_expected and len(violations) == 0:
    print()
    print("🎉 모든 테스트 통과!")
elif total_actual == total_expected:
    print()
    print("✓ 모든 시수 소진 완료")
    print("⚠️  하지만 1일 1과목 원칙 위반 존재")
else:
    print()
    print("❌ 테스트 실패:")
    if total_actual < total_expected:
        print(f"   - 시수 미달: {total_expected - total_actual}h 남음")
    if len(violations) > 0:
        print(f"   - 1일 1과목 원칙 위반: {len(violations)}건")

print("=" * 70)
