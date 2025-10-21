# 🎓 바이오헬스 융합인재 이노베이터 for KDT
## 교육 관리 시스템 완전판

![Python](https://img.shields.io/badge/Python-3.10-blue)
![PyQt5](https://img.shields.io/badge/PyQt5-5.15-green)
![MySQL](https://img.shields.io/badge/MySQL-8.0-orange)
![License](https://img.shields.io/badge/license-MIT-green)

## 📋 목차
- [개요](#개요)
- [주요 기능](#주요-기능)
- [시스템 요구사항](#시스템-요구사항)
- [설치 방법](#설치-방법)
- [실행 방법](#실행-방법)
- [데이터베이스 구조](#데이터베이스-구조)
- [사용 가이드](#사용-가이드)

## 🎯 개요

KDT(K-Digital Training) 교육 과정을 효율적으로 관리하기 위한 통합 데스크톱 애플리케이션입니다.
강사, 교과목, 과정, 프로젝트 관리부터 시간표 자동 생성까지 교육 운영에 필요한 모든 기능을 제공합니다.

## ✨ 주요 기능

### 1. 📚 기본 관리
- **강사 코드 관리**
  - 코드: IC-001, IC-002...
  - 강사명칭: 주강사, 보조강사, 멘토
  - 구분: 1(주강사), 2(보조강사), 3(멘토)

- **강사 관리**
  - 코드: T-001, T-002...
  - 기본 정보: 이름, 연락처, 전공, 이메일
  - 강사 구분 선택 (강사 코드 기반)

- **교과목 관리**
  - 코드: G-001, G-002...
  - 과목명, 수업시수
  - 주강사, 보조강사, 예비강사 지정

- **공휴일 관리**
  - 법정공휴일 자동 입력 (2025년 기준)
  - 수동 입력 (구정, 추석 등)
  - 날짜, 공휴일명, 법정공휴일 여부

### 2. 🎓 과정 관리
- **과정 관리**
  - 코드: C-001, C-002...
  - 반명칭, 강의장소
  - 강의 시수, 프로젝트 시수, 인턴쉽 시수
  - 인원수, 특이사항

- **시간표 작성** (예정)
  - 수업 시작일 기준 자동 계산
  - 공휴일, 토요일, 일요일 제외
  - 강의/프로젝트/인턴쉽 시수 자동 배분

### 3. 💼 프로젝트 관리
- **프로젝트 관리**
  - 코드: P-001, P-002...
  - 프로젝트명, 과정 연결
  - 구성원 1~5명 (이름, 연락처)

### 4. 📊 Excel 기능
- **내보내기**
  - 강사 목록
  - 교과목 목록
  - 과정 목록
  - 프로젝트 목록
  - 공휴일 목록

- **가져오기**
  - Excel 파일에서 데이터 일괄 가져오기

## 💻 시스템 요구사항

- **OS**: Windows 10/11
- **Python**: 3.10 이상
- **Database**: MySQL 8.0
- **RAM**: 4GB 이상
- **Storage**: 500MB 이상

## 📦 설치 방법

### 1. 필수 프로그램 설치
- Python 3.10
- Anaconda (권장)
- MySQL 8.0

### 2. Conda 환경 생성
```bash
conda create -n pyqt5_app python=3.10 -y
conda activate pyqt5_app
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

또는 자동 설치:
```bash
setup.bat
```

### 4. 데이터베이스 설정
`config_db.py` 파일에서 데이터베이스 연결 정보를 확인하세요:
```python
DB_CONFIG = {
    'host': 'bitnmeta2.synology.me',
    'user': 'iyrc',
    'passwd': 'Dodan1004!',
    'db': 'bh2025',
    'charset': 'utf8',
    'port': 3307,
}
```

## 🚀 실행 방법

### Windows 배치 파일
```bash
run_kdt_full.bat
```

### 직접 실행
```bash
conda activate pyqt5_app
python main_kdt_full.py
```

### 첫 실행 시
1. 애플리케이션 실행
2. 메뉴 또는 버튼에서 "데이터베이스 초기화" 선택
3. 테이블 생성 확인

## 🗄️ 데이터베이스 구조

### 주요 테이블

1. **instructor_codes** - 강사 코드
   - code (PK): VARCHAR(10)
   - name: VARCHAR(50)
   - type: ENUM('1', '2', '3')

2. **instructors** - 강사 정보
   - code (PK): VARCHAR(10)
   - name, phone, major, email
   - instructor_type (FK)

3. **subjects** - 교과목
   - code (PK): VARCHAR(10)
   - name, hours
   - main_instructor, assistant_instructor, reserve_instructor (FK)

4. **holidays** - 공휴일
   - id (PK): INT
   - holiday_date: DATE
   - name, is_legal

5. **courses** - 과정
   - code (PK): VARCHAR(10)
   - name, lecture_hours, project_hours, internship_hours
   - capacity, location, notes

6. **timetables** - 시간표
   - id (PK): INT
   - course_code (FK), subject_code (FK), instructor_code (FK)
   - class_date, start_time, end_time
   - type: ENUM('lecture', 'project', 'internship')

7. **projects** - 프로젝트
   - code (PK): VARCHAR(10)
   - name, course_code (FK)
   - member1~5_name, member1~5_phone

## 📖 사용 가이드

### 강사 등록 순서
1. **강사 코드 관리** → 강사 구분 코드 생성 (IC-001: 주강사 등)
2. **강사 관리** → 강사 정보 등록 (T-001: 홍길동 등)

### 교과목 등록 순서
1. 강사 등록 완료
2. **교과목 관리** → 과목 정보 입력 및 강사 배정

### 과정 생성 순서
1. **공휴일 관리** → 법정공휴일 자동 입력
2. **과정 관리** → 과정 정보 등록
3. **시간표 작성** → 자동 생성 (구현 예정)

### 프로젝트 등록
1. 과정 등록 완료
2. **프로젝트 관리** → 프로젝트 및 팀원 정보 입력

### Excel 활용
1. **내보내기**: 현재 데이터를 Excel로 백업
2. **가져오기**: Excel 파일에서 데이터 일괄 등록

## 📁 프로젝트 구조

```
pyqt5_app/
├── main_kdt_full.py           ⭐ 전체 기능 실행 파일
├── run_kdt_full.bat          ⭐ Windows 실행 스크립트
├── config_db.py              ⭐ DB 설정
├── requirements.txt
│
├── database/
│   ├── __init__.py
│   └── db_manager.py         ⭐ DB 연결 및 관리
│
├── ui/
│   ├── kdt_main_window_full.py    ⭐ 메인 윈도우
│   ├── instructor_code_dialog.py  강사 코드 관리
│   ├── instructor_dialog.py       강사 관리
│   ├── subject_dialog.py          교과목 관리
│   ├── holiday_dialog.py          공휴일 관리
│   ├── course_dialog.py           과정 관리
│   └── project_dialog.py          프로젝트 관리
│
└── utils/
    ├── excel_manager.py      ⭐ Excel 처리
    └── helpers.py
```

## 🎨 화면 구성

### 메인 화면
- 상단: 파란색 헤더 (타이틀)
- 메뉴바: 기본 관리, 과정 관리, 시간표, Excel, 도움말
- 툴바: 빠른 접근 버튼
- 컨텐츠: 9개 기능 버튼 그리드
- 하단: 상태바

### 각 관리 다이얼로그
- 상단: 입력 폼 (GroupBox)
- 중간: CRUD 버튼 (추가, 수정, 삭제, 초기화)
- 하단: 데이터 테이블
- 최하단: 닫기 버튼

## 🔧 문제 해결

### Q: 데이터베이스 연결 실패
```
A: config_db.py에서 연결 정보 확인
   - host, user, passwd, db, port 체크
   - MySQL 서버 실행 상태 확인
```

### Q: 테이블이 없다는 오류
```
A: "데이터베이스 초기화" 기능 실행
   메인 화면 → 데이터베이스 초기화 버튼 클릭
```

### Q: Excel 내보내기/가져오기 오류
```
A: 패키지 재설치
   pip install pandas openpyxl xlsxwriter
```

### Q: 한글이 깨져 보임
```
A: 데이터베이스 charset 확인
   charset='utf8' 또는 'utf8mb4' 사용
```

## 🚧 개발 예정 기능

- [ ] 시간표 자동 생성 로직
- [ ] 시간표 조회 및 인쇄
- [ ] 출석 관리 시스템
- [ ] 성적 관리 시스템
- [ ] 보고서 자동 생성 (PDF)
- [ ] 데이터 시각화 (차트)
- [ ] 사용자 권한 관리
- [ ] 백업/복구 기능

## 📞 지원

문제가 발생하면:
1. README_FULL.md 파일 확인
2. QUICK_START.md 빠른 시작 가이드 참조
3. 데이터베이스 로그 확인

## 📜 라이선스

MIT License

## 👨‍💻 개발 정보

- **프로젝트**: KDT 교육 관리 시스템
- **버전**: 2.0.0
- **개발**: 2025
- **기술 스택**: Python, PyQt5, MySQL, pandas, openpyxl

---

**Happy Managing! 🎉**
