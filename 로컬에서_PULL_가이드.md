# 🔄 로컬 컴퓨터에서 Pull 하기

## ✅ 원격 푸시 완료!

student 브랜치가 성공적으로 GitHub에 푸시되었습니다! 🎉

```
✅ 원격 저장소: https://github.com/Emmett6401/bioHealthScheduleManager.git
✅ 브랜치: student
✅ 커밋: 81b6eb3
✅ API 키: 모두 제거됨 (안전)
```

---

## 💻 로컬 컴퓨터에서 클론/Pull 하기

### 🆕 처음 클론하는 경우

#### Windows
```cmd
:: 원하는 폴더로 이동
cd C:\Users\YourName\Documents

:: 클론
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git

:: 폴더 이동
cd bioHealthScheduleManager

:: student 브랜치로 전환
git checkout student

:: 확인
git branch
git log --oneline -3
```

#### Mac/Linux
```bash
# 원하는 폴더로 이동
cd ~/Documents

# 클론
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git

# 폴더 이동
cd bioHealthScheduleManager

# student 브랜치로 전환
git checkout student

# 확인
git branch
git log --oneline -3
```

---

### 🔄 이미 클론되어 있는 경우 (Pull)

#### Windows
```cmd
:: 프로젝트 폴더로 이동
cd C:\Users\YourName\Documents\bioHealthScheduleManager

:: student 브랜치로 전환
git checkout student

:: 최신 코드 받기
git pull origin student

:: 확인
git log --oneline -3
```

#### Mac/Linux
```bash
# 프로젝트 폴더로 이동
cd ~/Documents/bioHealthScheduleManager

# student 브랜치로 전환
git checkout student

# 최신 코드 받기
git pull origin student

# 확인
git log --oneline -3
```

---

## 🔑 API 키 설정 (필수)

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="your-actual-api-key-here"
```

### Windows (CMD)
```cmd
set OPENAI_API_KEY=your-actual-api-key-here
```

### Mac/Linux
```bash
export OPENAI_API_KEY=your-actual-api-key-here
```

### 영구 설정 (Mac/Linux)
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'export OPENAI_API_KEY=your-actual-api-key-here' >> ~/.bashrc
source ~/.bashrc
```

### 영구 설정 (Windows)
1. **시스템 속성** → **환경 변수**
2. **새로 만들기**
3. 변수 이름: `OPENAI_API_KEY`
4. 변수 값: `your-actual-api-key-here`

---

## 📦 패키지 설치

```bash
# 프로젝트 폴더에서
cd pyqt5_app
pip install -r requirements.txt
```

**설치되는 패키지:**
- PyQt5
- pymysql
- pandas
- openpyxl
- openai
- reportlab

---

## 🗄️ 데이터베이스 테이블 생성

### 원격 DB 사용 (이미 설정됨)
```bash
# 프로젝트 루트에서
python create_consultation_tables.py
```

**참고:** 테이블이 이미 있으면 "이미 존재합니다" 메시지가 나옵니다. 정상입니다!

---

## 🧪 시스템 테스트

```bash
# 프로젝트 루트에서
python test_consultation_system.py
```

**예상 결과:**
```
✅ 데이터베이스 연결     : 통과
✅ 면담 테이블          : 통과
✅ 면담 메서드          : 통과
✅ UI 파일            : 통과
✅ OpenAI 패키지       : 통과
✅ 설정 파일           : 통과

🎉 모든 테스트 통과! (100%)
```

---

## ▶️ 프로그램 실행

```bash
cd pyqt5_app
python main_kdt_full.py
```

**메뉴 위치:**
```
상단 메뉴바 → 과정 관리 → 학생 면담 관리
```

---

## 📋 전체 명령어 한눈에 보기

### 처음 설치 (Windows)
```cmd
cd C:\Users\YourName\Documents
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager
git checkout student
set OPENAI_API_KEY=your-key-here
cd pyqt5_app
pip install -r requirements.txt
cd ..
python create_consultation_tables.py
python test_consultation_system.py
cd pyqt5_app
python main_kdt_full.py
```

### 처음 설치 (Mac/Linux)
```bash
cd ~/Documents
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager
git checkout student
export OPENAI_API_KEY=your-key-here
cd pyqt5_app
pip install -r requirements.txt
cd ..
python create_consultation_tables.py
python test_consultation_system.py
cd pyqt5_app
python main_kdt_full.py
```

---

## 🔄 업데이트 받기

나중에 새로운 기능이 추가되면:

```bash
cd bioHealthScheduleManager
git checkout student
git pull origin student
pip install -r pyqt5_app/requirements.txt
python test_consultation_system.py
cd pyqt5_app && python main_kdt_full.py
```

---

## 🆘 문제 해결

### "git: command not found"
- Windows: https://git-scm.com/download/win
- Mac: `brew install git`

### "python: command not found" (Mac)
```bash
python3 main_kdt_full.py
```

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 데이터베이스 연결 오류
```bash
# config_db.py 확인
cat pyqt5_app/config_db.py
```

### API 키 오류
```bash
# 환경 변수 확인
echo $OPENAI_API_KEY  # Mac/Linux
echo %OPENAI_API_KEY%  # Windows

# 설정
export OPENAI_API_KEY=your-key  # Mac/Linux
set OPENAI_API_KEY=your-key     # Windows
```

---

## ✅ 체크리스트

```
□ Git 클론 완료
□ student 브랜치 체크아웃
□ API 키 환경 변수 설정
□ 패키지 설치 완료
□ 데이터베이스 테이블 생성
□ 시스템 테스트 통과
□ 프로그램 실행 성공
□ 면담 관리 메뉴 확인
```

---

## 📚 도움말 문서

프로젝트에 포함된 문서들:

| 문서 | 설명 |
|------|------|
| **START_HERE.md** | 시작 가이드 |
| **QUICK_CLONE_GUIDE.md** | 5분 빠른 클론 |
| **로컬_클론_가이드.md** | 상세 클론 방법 |
| **SETUP_COMPLETE.md** | 설정 완료 가이드 |
| **API_KEY_설정_가이드.md** | API 키 보안 설정 |
| **CONSULTATION_QUICK_START.md** | 면담 관리 빠른 시작 |
| **CONSULTATION_MANAGEMENT_README.md** | 면담 관리 상세 매뉴얼 |
| **메뉴_찾기_가이드.md** | 메뉴 위치 안내 |

---

## 🎊 완료!

이제 로컬 컴퓨터에서 **학생 면담 관리 시스템**을 사용할 수 있습니다!

**저장소**: https://github.com/Emmett6401/bioHealthScheduleManager.git  
**브랜치**: student  
**최신 커밋**: 81b6eb3

---

**즐거운 학생 상담 되세요!** 🎓✨
