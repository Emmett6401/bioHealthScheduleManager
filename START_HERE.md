# 🎉 새로운 폴더에서 시작하기

## 📍 현재 위치
```
/home/user/webapp_consultation
```

이것은 **student 브랜치**의 깨끗한 복사본입니다.
과정 관리 + 학생 면담 관리 기능이 모두 포함되어 있습니다.

---

## ✅ 설정 완료 상태

### 시스템 테스트 결과
```
✅ 데이터베이스 연결     : 통과
✅ 면담 테이블          : 통과
✅ 면담 메서드          : 통과
✅ UI 파일            : 통과
✅ OpenAI 패키지       : 통과 (v2.6.1)
✅ 설정 파일           : 통과

🎉 모든 테스트 통과! (100%)
```

---

## 🚀 바로 시작하기

### 프로그램 실행
```bash
cd /home/user/webapp_consultation/pyqt5_app
python main_kdt_full.py
```

### 면담 관리 사용
1. 프로그램 실행
2. 메뉴: **과정 관리** → **학생 면담 관리**
3. 사용 시작!

---

## 📁 이 폴더의 구조

```
webapp_consultation/
├── pyqt5_app/                          # 메인 애플리케이션
│   ├── main_kdt_full.py               # 실행 파일
│   ├── ui/
│   │   ├── consultation_dialog.py      # 면담 관리 UI
│   │   └── consultation_report_dialog.py  # 면담일지 생성
│   ├── database/
│   │   └── db_manager.py              # DB 관리 (면담 메서드 포함)
│   └── config.py                       # 설정 (OpenAI API 키 포함)
│
├── create_consultation_tables.py       # 테이블 생성 스크립트
├── test_consultation_system.py         # 시스템 테스트
│
└── 📚 문서 파일들
    ├── SETUP_COMPLETE.md              # ⭐ 설치 완료 & 시작 가이드
    ├── CONSULTATION_QUICK_START.md    # 빠른 시작
    ├── CONSULTATION_MANAGEMENT_README.md  # 상세 매뉴얼
    └── CONSULTATION_FILES_SUMMARY.md  # 파일 목록
```

---

## 🎯 주요 기능

### ✨ 포함된 기능
1. **기본 과정 관리**
   - 강사 관리
   - 교과목 관리
   - 과정 관리
   - 학생 관리
   - 프로젝트 관리
   - 시간표 작성

2. **학생 면담 관리** (새로 추가)
   - 면담 정보 저장 및 관리
   - 사진 첨부 기능
   - 검색 및 필터링
   - 다음 면담 예정일 관리
   - **AI 면담일지 자동 생성** (GPT-4)
   - 인쇄/PDF/텍스트 저장

---

## 💡 첫 사용 가이드

### 1️⃣ 첫 번째 면담 기록

```
1. 프로그램 실행
   → cd /home/user/webapp_consultation/pyqt5_app
   → python main_kdt_full.py

2. 면담 관리 열기
   → 메뉴: 과정 관리 → 학생 면담 관리

3. 새 면담 작성
   → "새 면담" 버튼 클릭
   → 학생 선택
   → 면담 정보 입력
   → 저장

4. AI 면담일지 생성 (선택)
   → 저장된 면담 선택
   → "면담일지 출력" 버튼
   → "AI 면담일지 생성" 클릭
   → PDF/인쇄/텍스트 저장
```

---

## 🔧 설정 확인

### OpenAI API 키
```bash
# 확인
cat pyqt5_app/config.py | grep OPENAI_API_KEY

# 현재 설정됨:
OPENAI_API_KEY = "your-openai-api-key-here"
```

### 데이터베이스 설정
```bash
# 확인
cat pyqt5_app/config_db.py

# 현재 설정:
host: bitnmeta2.synology.me
port: 3307
user: iyrc
db: bh2025
```

---

## 📚 도움말 문서

| 문서 | 내용 | 추천 대상 |
|------|------|----------|
| **SETUP_COMPLETE.md** | 설치 완료 & 전체 가이드 | ⭐ 처음 사용자 |
| **CONSULTATION_QUICK_START.md** | 5분 빠른 시작 | 빠르게 시작하고 싶은 사용자 |
| **CONSULTATION_MANAGEMENT_README.md** | 상세 매뉴얼 | 모든 기능을 알고 싶은 사용자 |
| **CONSULTATION_FILES_SUMMARY.md** | 파일 및 코드 설명 | 개발자 |

---

## 🔄 이전 폴더와의 관계

### 이전 폴더
- **위치**: `/home/user/webapp`
- **상태**: 원본 보존 (백업용)
- **브랜치**: student

### 현재 폴더 (새로 만든 곳)
- **위치**: `/home/user/webapp_consultation`
- **상태**: student 브랜치의 깨끗한 복사본
- **브랜치**: student
- **용도**: 실제 작업 및 사용

### 언제든지 원래대로
```bash
# 이전 폴더로 돌아가기
cd /home/user/webapp

# 또는 새 폴더 삭제
rm -rf /home/user/webapp_consultation
```

---

## 🎯 Git 작업 (선택)

### 현재 상태
- 로컬 student 브랜치 복사본
- 원격 저장소에는 아직 푸시 안됨

### 원격에 푸시하고 싶다면
```bash
cd /home/user/webapp_consultation

# SSH 사용 (추천)
git remote set-url origin git@github.com:Emmett6401/bioHealthScheduleManager.git
git push -u origin student

# 또는 HTTPS + Token
git push -u origin student
# Username: Emmett6401
# Password: [GitHub Personal Access Token]
```

### 원격에서 클론하고 싶다면
```bash
# 다른 컴퓨터나 새 폴더에서
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager
git checkout student
```

---

## 🆘 문제 해결

### 프로그램이 실행되지 않을 때
```bash
# 1. 경로 확인
pwd
# /home/user/webapp_consultation/pyqt5_app 이어야 함

# 2. Python 버전 확인
python --version
# Python 3.x 이어야 함

# 3. 패키지 재설치
pip install -r requirements.txt

# 4. 시스템 테스트
cd ..
python test_consultation_system.py
```

### 면담 관리가 보이지 않을 때
```bash
# UI 파일 존재 확인
ls pyqt5_app/ui/consultation_dialog.py
ls pyqt5_app/ui/consultation_report_dialog.py

# 메인 윈도우 확인
grep "consultation" pyqt5_app/ui/kdt_main_window_full.py
```

### AI 면담일지 생성 오류
```bash
# OpenAI 패키지 확인
pip show openai

# API 키 확인
grep OPENAI_API_KEY pyqt5_app/config.py

# 재설치
pip install openai --upgrade
```

---

## ✅ 체크리스트

복사해서 사용하세요:

```
□ 폴더 위치 확인 (/home/user/webapp_consultation)
□ 시스템 테스트 100% 통과 확인
□ 프로그램 실행 테스트
□ 면담 관리 화면 열기 테스트
□ 첫 번째 면담 기록 작성
□ AI 면담일지 생성 테스트
□ 문서 읽기 (SETUP_COMPLETE.md)
□ 팀원들에게 공유 (선택)
```

---

## 🎊 시작하세요!

모든 준비가 완료되었습니다!

```bash
cd /home/user/webapp_consultation/pyqt5_app
python main_kdt_full.py
```

**메뉴: 과정 관리 → 학생 면담 관리**

---

**즐거운 학생 상담 되세요!** 🎓✨

---

**폴더 생성일**: 2024-10-29  
**브랜치**: student  
**테스트 상태**: ✅ 100% 통과
