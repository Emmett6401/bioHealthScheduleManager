# -*- coding: utf-8 -*-
"""
시간표 생성 알고리즘 - 간단 버전
"""

from datetime import timedelta

def create_timetable_simple(subjects, start_date, end_date, holidays):
    """
    간단명확한 시간표 생성 알고리즘
    
    규칙:
    1. 1일 1과목 (오전 4h + 오후 4h)
    2. 다음날은 다른 과목
    3. 금요일은 시수 적은 2개 과목 격주
    4. 오전 완료 시 → 오후는 가장 시수 많이 남은 과목
    5. 금요일 과목도 빈 자리 가능
    """
    timetable = []
    
    # 남은 시수
    remaining = {s['code']: s['hours'] for s in subjects}
    
    # 시수 순 정렬
    sorted_subj = sorted(subjects, key=lambda x: x['hours'])
    
    # 금요일 과목 (시수 적은 2개)
    fri_codes = [sorted_subj[0]['code'], sorted_subj[1]['code']] if len(sorted_subj) >= 2 else []
    fri_idx = 0
    
    # 평일 과목 순서
    weekday_subj = [s for s in sorted_subj if s['code'] not in fri_codes]
    weekday_idx = 0
    
    # 다음날 할 과목 (오후에 시작한 과목)
    next_subject = None
    
    current_date = start_date
    
    while current_date <= end_date and any(h > 0 for h in remaining.values()):
        # 주말/공휴일 스킵
        if current_date.weekday() >= 5 or current_date in holidays:
            current_date += timedelta(days=1)
            continue
        
        am_subj = None
        pm_subj = None
        
        # 케이스 1: 어제 오후에 시작한 과목이 있음 → 오늘 계속
        if next_subject:
            subj_code = next_subject['code']
            if remaining[subj_code] > 0:
                # 오전
                am_h = min(4, remaining[subj_code])
                am_subj = make_subject_entry(next_subject, am_h)
                remaining[subj_code] -= am_h
                
                # 오후
                if remaining[subj_code] >= 4:
                    pm_subj = make_subject_entry(next_subject, 4)
                    remaining[subj_code] -= 4
                    next_subject = None  # 완료, 내일은 다른 과목
                elif remaining[subj_code] > 0:
                    pm_subj = make_subject_entry(next_subject, remaining[subj_code])
                    remaining[subj_code] = 0
                    next_subject = None
                else:
                    # 오전에 완료 → 오후는 가장 시수 많은 과목
                    next_subject = None
                    pm_subj = get_most_remaining_subject(subjects, remaining)
                    if pm_subj:
                        remaining[pm_subj['code']] -= pm_subj['hours']
                        next_subject = find_subject_by_code(subjects, pm_subj['code'])
        
        # 케이스 2: 금요일 (금요일 과목 우선)
        elif current_date.weekday() == 4:
            # 금요일 과목 찾기
            fri_subj = None
            for _ in range(len(fri_codes)):
                code = fri_codes[fri_idx % len(fri_codes)]
                fri_idx += 1
                if remaining.get(code, 0) > 0:
                    fri_subj = find_subject_by_code(subjects, code)
                    break
            
            # 금요일 과목이 없으면 가장 시수 많은 과목
            if not fri_subj:
                fri_subj = find_most_remaining_subject(subjects, remaining)
            
            if fri_subj:
                code = fri_subj['code']
                # 오전
                am_h = min(4, remaining[code])
                am_subj = make_subject_entry(fri_subj, am_h)
                remaining[code] -= am_h
                
                # 오후
                if remaining[code] >= 4:
                    pm_subj = make_subject_entry(fri_subj, 4)
                    remaining[code] -= 4
                elif remaining[code] > 0:
                    pm_subj = make_subject_entry(fri_subj, remaining[code])
                    remaining[code] = 0
                else:
                    # 오전 완료 → 오후는 가장 시수 많은 과목
                    pm_subj = get_most_remaining_subject(subjects, remaining)
                    if pm_subj:
                        remaining[pm_subj['code']] -= pm_subj['hours']
                        next_subject = find_subject_by_code(subjects, pm_subj['code'])
        
        # 케이스 3: 평일 (순서대로)
        else:
            # 다음 평일 과목 찾기
            found = False
            for attempt in range(len(subjects)):
                if weekday_idx >= len(weekday_subj):
                    weekday_idx = 0
                
                subj = weekday_subj[weekday_idx]
                if remaining[subj['code']] > 0:
                    # 오전
                    am_h = min(4, remaining[subj['code']])
                    am_subj = make_subject_entry(subj, am_h)
                    remaining[subj['code']] -= am_h
                    
                    # 오후
                    if remaining[subj['code']] >= 4:
                        pm_subj = make_subject_entry(subj, 4)
                        remaining[subj['code']] -= 4
                        weekday_idx += 1  # 내일은 다른 과목
                    elif remaining[subj['code']] > 0:
                        pm_subj = make_subject_entry(subj, remaining[subj['code']])
                        remaining[subj['code']] = 0
                        weekday_idx += 1
                    else:
                        # 오전 완료 → 오후는 가장 시수 많은 과목
                        weekday_idx += 1
                        pm_subj = get_most_remaining_subject(subjects, remaining)
                        if pm_subj:
                            remaining[pm_subj['code']] -= pm_subj['hours']
                            next_subject = find_subject_by_code(subjects, pm_subj['code'])
                    
                    found = True
                    break
                
                weekday_idx += 1
            
            # 평일 과목이 모두 끝났으면 가장 시수 많은 과목 (금요일 포함)
            if not found:
                best = find_most_remaining_subject(subjects, remaining)
                if best:
                    # 오전
                    am_h = min(4, remaining[best['code']])
                    am_subj = make_subject_entry(best, am_h)
                    remaining[best['code']] -= am_h
                    
                    # 오후
                    if remaining[best['code']] >= 4:
                        pm_subj = make_subject_entry(best, 4)
                        remaining[best['code']] -= 4
                    elif remaining[best['code']] > 0:
                        pm_subj = make_subject_entry(best, remaining[best['code']])
                        remaining[best['code']] = 0
                    else:
                        # 오전 완료 → 오후
                        pm_subj = get_most_remaining_subject(subjects, remaining)
                        if pm_subj:
                            remaining[pm_subj['code']] -= pm_subj['hours']
                            next_subject = find_subject_by_code(subjects, pm_subj['code'])
        
        # 시간표 추가
        if am_subj and pm_subj:
            timetable.append({
                'date': current_date,
                'am_subject': am_subj,
                'pm_subject': pm_subj
            })
        
        current_date += timedelta(days=1)
    
    return timetable


def make_subject_entry(subject, hours):
    """과목 엔트리 생성"""
    return {
        'code': subject['code'],
        'name': subject['name'],
        'total_hours': subject['hours'],
        'main_instructor': subject.get('main_instructor_name', '-'),
        'assistant_instructor': subject.get('assistant_instructor_name', '-'),
        'reserve_instructor': subject.get('reserve_instructor_name', '-'),
        'hours': hours
    }


def find_subject_by_code(subjects, code):
    """코드로 과목 찾기"""
    for s in subjects:
        if s['code'] == code:
            return s
    return None


def find_most_remaining_subject(subjects, remaining):
    """가장 시수가 많이 남은 과목 찾기"""
    max_h = 0
    best = None
    for s in subjects:
        h = remaining.get(s['code'], 0)
        if h > max_h:
            max_h = h
            best = s
    return best


def get_most_remaining_subject(subjects, remaining):
    """가장 시수 많은 과목의 4h 엔트리 반환"""
    subj = find_most_remaining_subject(subjects, remaining)
    if subj:
        h = min(4, remaining[subj['code']])
        return make_subject_entry(subj, h)
    return None
