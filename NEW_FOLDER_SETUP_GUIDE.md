# 🔄 새 폴더에서 프로젝트 클론 및 설정 가이드

## 📋 개요

새로운 폴더에서 깨끗하게 시작하고, student 브랜치의 면담 관리 기능을 사용하는 방법입니다.

---

## ⚠️ 현재 상황

### 현재 student 브랜치 커밋 내역
```
d2f6ba9 - docs: 설치 완료 안내 문서 추가
ab34798 - fix: DB 설정 키 이름 수정 (password -> passwd)
2b909ee - config: OpenAI API 키 설정 완료
18b52b1 - docs: 면담 관리 시스템 파일 요약 문서 추가
5855272 - docs: 면담 관리 시스템 테스트 스크립트 및 퀵스타트 가이드 추가
b8b87a3 - feat: 학생 면담 관리 시스템 추가
b93f0d1 - feat: Add student photo infrastructure (hybrid approach)
```

### 원격 저장소
- **URL**: https://github.com/Emmett6401/bioHealthScheduleManager.git
- **현재 브랜치**: student (로컬에만 존재, 아직 푸시 안됨)

---

## 🚀 방법 1: 원격 푸시 후 클론 (권장)

### 1-1. 현재 위치에서 student 브랜치 푸시
```bash
cd /home/user/webapp

# GitHub 토큰이 필요합니다
# 방법 A: SSH 사용 (추천)
git remote set-url origin git@github.com:Emmett6401/bioHealthScheduleManager.git
git push -u origin student

# 방법 B: Personal Access Token 사용
git push -u origin student
# Username: Emmett6401
# Password: [GitHub Personal Access Token 입력]
```

### 1-2. 새 폴더에서 클론
```bash
# 새 폴더로 이동 (원하는 위치)
cd /home/user
mkdir webapp_new
cd webapp_new

# 저장소 클론
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git .

# student 브랜치로 체크아웃
git checkout student

# 확인
git branch
git log --oneline -5
```

---

## 🔄 방법 2: 로컬에서 직접 복사 (빠른 방법)

원격 푸시가 어려운 경우, 로컬에서 직접 복사할 수 있습니다.

### 2-1. 새 폴더 생성 및 Git 초기화
```bash
# 새 폴더 생성
cd /home/user
mkdir webapp_new
cd webapp_new

# 기존 저장소의 .git을 제외한 모든 파일 복사
rsync -av --exclude='.git' /home/user/webapp/ /home/user/webapp_new/

# Git 초기화
git init
git remote add origin https://github.com/Emmett6401/bioHealthScheduleManager.git

# 원격의 student 브랜치 가져오기 (있는 경우)
git fetch origin
```

### 2-2. 기존 student 브랜치 커밋 가져오기
```bash
cd /home/user/webapp_new

# 기존 저장소의 .git 폴더를 임시로 복사
cp -r /home/user/webapp/.git /home/user/webapp_new/.git_backup

# student 브랜치 정보 복사
cd /home/user/webapp_new
rm -rf .git
mv .git_backup .git

# student 브랜치 확인
git branch
git log --oneline -5
```

---

## 🎯 방법 3: 패치 파일 사용 (가장 안전)

### 3-1. 현재 위치에서 패치 파일 생성
```bash
cd /home/user/webapp

# student 브랜치의 모든 변경사항을 패치로 저장
# main 브랜치와의 차이를 패치로 생성
git format-patch main..student -o /home/user/student_patches

# 또는 특정 커밋부터의 패치 생성
git format-patch b93f0d1^..HEAD -o /home/user/student_patches
```

### 3-2. 새 폴더에서 저장소 클론 및 패치 적용
```bash
# 새 폴더에서 저장소 클론
cd /home/user
mkdir webapp_new
cd webapp_new
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git .

# main 브랜치에서 새 브랜치 생성
git checkout -b student_new

# 패치 적용
git am /home/user/student_patches/*.patch

# 확인
git log --oneline -5
```

---

## ✅ 새 폴더에서 설정 완료 후 할 일

### 1. 데이터베이스 테이블 생성
```bash
cd /home/user/webapp_new
python create_consultation_tables.py
```

### 2. 패키지 설치
```bash
cd /home/user/webapp_new/pyqt5_app
pip install -r requirements.txt
```

### 3. OpenAI API 키 설정
```bash
# 방법 A: 환경 변수
export OPENAI_API_KEY=your-openai-api-key-here

# 방법 B: config.py 수정
# pyqt5_app/config.py 파일에서 API 키 확인/수정
```

### 4. 시스템 테스트
```bash
cd /home/user/webapp_new
python test_consultation_system.py
```

### 5. 프로그램 실행
```bash
cd /home/user/webapp_new/pyqt5_app
python main_kdt_full.py
```

---

## 🔐 GitHub Personal Access Token 생성 방법

원격 푸시를 위해 토큰이 필요한 경우:

1. GitHub 로그인
2. Settings → Developer settings → Personal access tokens → Tokens (classic)
3. "Generate new token" 클릭
4. 권한 선택:
   - ✅ repo (전체)
   - ✅ workflow
5. 생성된 토큰 복사
6. Git 푸시 시 Password에 토큰 입력

---

## 📊 각 방법의 장단점

| 방법 | 장점 | 단점 | 추천 상황 |
|------|------|------|----------|
| **방법 1: 원격 푸시 후 클론** | ✅ 가장 깨끗함<br>✅ 팀 공유 가능 | ❌ 인증 필요 | 정식 배포 시 |
| **방법 2: 로컬 복사** | ✅ 가장 빠름<br>✅ 인증 불필요 | ❌ 원격 미반영 | 빠른 테스트 |
| **방법 3: 패치 사용** | ✅ 안전함<br>✅ 이력 보존 | ❌ 단계 많음 | 변경사항 관리 |

---

## 💡 추천 작업 순서

### 즉시 사용하고 싶다면 (5분)
```bash
# 방법 2 사용
cd /home/user
cp -r webapp webapp_new
cd webapp_new
rm -rf .git
git init
git add .
git commit -m "Initial commit from student branch"
python create_consultation_tables.py
cd pyqt5_app && python main_kdt_full.py
```

### 제대로 설정하고 싶다면 (10분)
```bash
# 방법 1 사용 (GitHub 토큰 필요)
# 1. 현재 폴더에서 푸시
cd /home/user/webapp
git push -u origin student

# 2. 새 폴더에서 클론
cd /home/user
mkdir webapp_new && cd webapp_new
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git .
git checkout student

# 3. 설정
python create_consultation_tables.py
cd pyqt5_app && pip install -r requirements.txt
python main_kdt_full.py
```

---

## 🆘 문제 해결

### Q: git push 시 인증 오류
```bash
# SSH 키 사용으로 변경
git remote set-url origin git@github.com:Emmett6401/bioHealthScheduleManager.git

# 또는 토큰 사용
# Username: Emmett6401
# Password: [GitHub Personal Access Token]
```

### Q: 패치 적용 실패
```bash
# 충돌 발생 시
git am --abort
git am --3way /home/user/student_patches/*.patch
```

### Q: 데이터베이스 연결 오류
```bash
# config_db.py 확인
cat pyqt5_app/config_db.py
# DB 설정이 올바른지 확인
```

---

## 📞 다음 단계

새 폴더 설정 완료 후:

1. ✅ 프로그램 실행 확인
2. ✅ 면담 관리 기능 테스트
3. ✅ 팀원들과 공유 (원격 푸시 완료 시)
4. ✅ 기존 /home/user/webapp 폴더 백업 또는 삭제

---

**어떤 방법을 사용하시겠습니까?**

1. **방법 1**: 원격 푸시 후 클론 (GitHub 토큰 필요)
2. **방법 2**: 로컬 복사 (가장 빠름)
3. **방법 3**: 패치 파일 사용 (가장 안전)

알려주시면 해당 방법으로 진행하겠습니다!
