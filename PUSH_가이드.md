# 🚀 Git Push 가이드

## ⚠️ 현재 상황

GitHub가 **OpenAI API 키**를 감지하여 푸시를 차단했습니다.

```
remote: - Push cannot contain secrets
remote: - OpenAI API Key
```

---

## ✅ 해결 완료

1. ✅ config.py에서 API 키 제거
2. ✅ 모든 문서에서 API 키 제거
3. ✅ API 키 설정 가이드 추가
4. ✅ 보안 커밋 생성

---

## 🔄 이제 해야 할 일

### 방법 1: 이전 커밋 수정 (권장)

Git 히스토리에서 API 키를 완전히 제거:

```bash
cd /home/user/webapp_consultation

# 1. API 키가 처음 추가된 커밋부터 rebase
git rebase -i b8b87a3

# 2. 에디터에서 '2b909ee' 커밋을 'edit'로 변경
# pick 2b909ee config: OpenAI API 키 설정 완료
# ↓
# edit 2b909ee config: OpenAI API 키 설정 완료

# 3. config.py 수정 (API 키 제거)
vi pyqt5_app/config.py
# OPENAI_API_KEY = None 으로 변경

# 4. 수정 사항 적용
git add pyqt5_app/config.py
git commit --amend --no-edit

# 5. rebase 계속
git rebase --continue

# 6. force push
git push --force origin student
```

### 방법 2: 새 브랜치로 시작 (간단)

깨끗한 브랜치로 다시 시작:

```bash
cd /home/user/webapp_consultation

# 1. 현재 상태 백업
git branch student_backup

# 2. main에서 새 브랜치 생성
git checkout main
git pull origin main
git checkout -b student_clean

# 3. student 브랜치의 변경사항 cherry-pick
git cherry-pick b8b87a3..6d8d284

# 4. 푸시
git push -u origin student_clean

# 5. GitHub에서 student 브랜치 삭제 후 student_clean을 student로 이름 변경
```

### 방법 3: 현재 커밋만 유지 (가장 간단)

API 키가 없는 현재 상태만 푸시:

```bash
cd /home/user/webapp_consultation

# 1. 현재 브랜치 이름 변경
git branch -m student student_old

# 2. main에서 새 student 브랜치
git checkout main
git checkout -b student

# 3. 현재 작업 내용만 복사
git restore --source=student_old --worktree .

# 4. 커밋
git add .
git commit -m "feat: 학생 면담 관리 시스템 완전판

- 면담 정보 저장 및 관리
- AI 면담일지 생성 (GPT-4)
- 사진 첨부 기능
- 검색 및 필터링
- 모든 문서 포함
- 보안: API 키는 환경 변수 사용"

# 5. 푸시
git push --force origin student
```

---

## 💡 권장 방법

**방법 3 (현재 커밋만 유지)**를 추천합니다:

### 실행 단계

```bash
cd /home/user/webapp_consultation

# 1. 백업
git branch student_backup_$(date +%Y%m%d)

# 2. main 기준으로 새 student 브랜치
git fetch origin main
git checkout main
git pull origin main
git branch -D student 2>/dev/null
git checkout -b student

# 3. student_backup의 파일들 복사
git checkout student_backup_$(date +%Y%m%d) -- .

# 4. 모든 변경사항 확인
git status

# 5. API 키 확인
grep -r "sk-proj" . 2>/dev/null | grep -v ".git"
# 아무것도 나오지 않아야 함!

# 6. 커밋 및 푸시
git add .
git commit -m "feat: 학생 면담 관리 시스템

모든 기능 완료:
- 면담 정보 관리
- AI 면담일지 생성
- 사진 첨부
- 검색/필터링
- 완전한 문서화

보안: API 키는 환경 변수로 설정"

git push --force origin student
```

---

## 🧪 푸시 전 확인

```bash
# 1. API 키가 없는지 확인
grep -r "sk-proj" . 2>/dev/null | grep -v ".git"
# 결과 없음 = 안전

# 2. 파일 확인
cat pyqt5_app/config.py | grep OPENAI_API_KEY
# OPENAI_API_KEY = None 이어야 함

# 3. Git 상태 확인
git status
git log --oneline -3
```

---

## 📞 푸시 후

### 성공하면
```bash
# 로컬 컴퓨터에서 클론
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager
git checkout student

# API 키 설정
export OPENAI_API_KEY=your-key-here

# 실행
cd pyqt5_app
pip install -r requirements.txt
python main_kdt_full.py
```

### 여전히 실패하면
GitHub URL에서 직접 허용:
```
https://github.com/Emmett6401/bioHealthScheduleManager/security/secret-scanning/unblock-secret/34joGgXLy2qbBVlQGRApUnHC6LB
```

---

## 🎯 다음 단계

1. ✅ 위의 **방법 3** 실행
2. ✅ 푸시 성공 확인
3. ✅ 로컬 컴퓨터에서 클론
4. ✅ 환경 변수로 API 키 설정
5. ✅ 프로그램 실행 테스트

---

**준비되셨나요? 방법 3을 실행하시겠습니까?**
