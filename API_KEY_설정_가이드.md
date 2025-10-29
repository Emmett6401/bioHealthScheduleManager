# 🔑 OpenAI API 키 설정 가이드

## ⚠️ 중요: 보안

**API 키는 절대 Git에 커밋하지 마세요!**

GitHub가 자동으로 감지하고 푸시를 차단합니다.

---

## ✅ 올바른 설정 방법

### 방법 1: 환경 변수 사용 (권장) 🌟

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

#### Windows (CMD)
```cmd
set OPENAI_API_KEY=your-api-key-here
```

#### Mac/Linux
```bash
export OPENAI_API_KEY=your-api-key-here
```

#### 영구 설정 (Mac/Linux)
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export OPENAI_API_KEY=your-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

#### 영구 설정 (Windows)
1. **시스템 속성** → **환경 변수**
2. **새로 만들기**
3. 변수 이름: `OPENAI_API_KEY`
4. 변수 값: `your-api-key-here`

---

### 방법 2: config.py 로컬 수정 (권장하지 않음)

```python
# pyqt5_app/config.py
OPENAI_API_KEY = "your-api-key-here"  # 절대 커밋하지 마세요!
```

**주의:**
- ⚠️ 이 파일은 `.gitignore`에 추가해야 합니다
- ⚠️ 실수로 커밋하면 보안 위험

---

### 방법 3: .env 파일 사용 (가장 안전)

#### 1. python-dotenv 설치
```bash
pip install python-dotenv
```

#### 2. .env 파일 생성
```bash
# 프로젝트 루트에 .env 파일 생성
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

#### 3. .gitignore에 추가
```bash
echo ".env" >> .gitignore
```

#### 4. 코드에서 사용
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
```

---

## 🔍 현재 설정 확인

### 환경 변수 확인
```bash
# Windows
echo %OPENAI_API_KEY%

# Mac/Linux
echo $OPENAI_API_KEY
```

### Python에서 확인
```bash
python -c "import os; print(os.environ.get('OPENAI_API_KEY', 'Not Set'))"
```

---

## 🆘 문제 해결

### API 키가 없어도 작동하나요?
✅ **예!** 기본 면담 관리 기능은 모두 사용 가능합니다.
❌ AI 면담일지 자동 생성 기능만 API 키가 필요합니다.

### 프로그램 실행 시 API 키 오류
```
오류: OpenAI API 키가 설정되어 있지 않습니다
```

**해결:**
1. 환경 변수 설정
2. 또는 config.py에 키 추가
3. 프로그램 재시작

### GitHub 푸시 차단
```
remote: - Push cannot contain secrets
remote: - OpenAI API Key
```

**해결:**
1. API 키를 환경 변수로 변경
2. Git 히스토리에서 키 제거 (아래 참고)

---

## 🔧 Git 히스토리에서 API 키 제거

### 방법 1: 최신 커밋만 수정
```bash
# 마지막 커밋 수정
git reset --soft HEAD~1
# API 키 제거 후
git add .
git commit -m "fix: Remove API key from config"
```

### 방법 2: 특정 파일 히스토리 제거 (고급)
```bash
# BFG Repo-Cleaner 사용
git clone --mirror https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager.git
bfg --replace-text passwords.txt
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push --force
```

---

## 📋 권장 워크플로우

### 1. 로컬 개발
```bash
# 환경 변수 설정 (매번 터미널 열 때마다)
export OPENAI_API_KEY=your-key-here

# 또는 .bashrc에 영구 추가
echo 'export OPENAI_API_KEY=your-key-here' >> ~/.bashrc
```

### 2. 프로그램 실행
```bash
cd pyqt5_app
python main_kdt_full.py
```

### 3. Git 작업
```bash
# config.py는 항상 기본값 유지
# API 키는 환경 변수로만 사용
git add .
git commit -m "Update features"
git push origin student
```

---

## 🎯 체크리스트

```
□ 환경 변수로 API 키 설정
□ config.py에 실제 키 없음 확인
□ .env 파일이 .gitignore에 있음
□ git status로 민감한 파일 없음 확인
□ 커밋 전에 한번 더 확인
```

---

## 💡 추가 정보

### API 키 얻기
1. https://platform.openai.com/api-keys
2. "Create new secret key" 클릭
3. 키 복사 (한 번만 보여짐!)
4. 안전한 곳에 저장

### 비용 관리
- GPT-4: 면담일지 1건당 약 $0.02-0.05
- 월별 사용량 제한 설정 권장
- https://platform.openai.com/account/billing/limits

---

**보안을 위해 항상 환경 변수를 사용하세요!** 🔒
