# ⚡ 빠른 클론 가이드 (5분)

## 🎯 로컬 컴퓨터에 클론하기

### 📍 저장소 정보
```
URL: https://github.com/Emmett6401/bioHealthScheduleManager.git
브랜치: student
```

---

## 💻 Windows 사용자

### 1단계: Git Bash 또는 CMD 열기
```bash
# 원하는 폴더로 이동
cd C:\Users\YourName\Documents
```

### 2단계: 클론 및 설정
```bash
# 클론
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager
git checkout student

# 패키지 설치
cd pyqt5_app
pip install -r requirements.txt

# 실행
python main_kdt_full.py
```

---

## 🍎 Mac 사용자

### 1단계: Terminal 열기
```bash
# 원하는 폴더로 이동
cd ~/Documents
```

### 2단계: 클론 및 설정
```bash
# 클론
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager
git checkout student

# 패키지 설치
cd pyqt5_app
pip3 install -r requirements.txt

# 실행
python3 main_kdt_full.py
```

---

## ✅ 설정 확인사항

### 자동으로 설정되어 있는 것들 ✅
- ✅ 데이터베이스 연결 정보 (원격 DB)
- ✅ OpenAI API 키
- ✅ 모든 UI 파일
- ✅ 면담 관리 기능

### 추가로 할 일 (선택)
- 📦 패키지 설치: `pip install -r requirements.txt`
- 🧪 시스템 테스트: `python test_consultation_system.py`

---

## 🚀 프로그램 실행

```bash
cd pyqt5_app
python main_kdt_full.py    # Windows
python3 main_kdt_full.py   # Mac
```

### 면담 관리 사용
1. 프로그램 실행
2. 메뉴: **과정 관리** → **학생 면담 관리**
3. 완료! 🎉

---

## 🆘 문제 발생 시

### Git이 없다면
- **Windows**: https://git-scm.com/download/win
- **Mac**: `brew install git`

### Python이 없다면
- **Windows**: https://www.python.org/downloads/
- **Mac**: `brew install python3`

### 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📚 상세 가이드

더 자세한 설명이 필요하면:
- 📖 **로컬_클론_가이드.md** - 완전 상세 가이드
- 📘 **START_HERE.md** - 새 폴더 시작 가이드
- 🚀 **SETUP_COMPLETE.md** - 전체 설정 가이드

---

## 🎊 끝!

3개 명령어만 입력하면 완료:
```bash
git clone https://github.com/Emmett6401/bioHealthScheduleManager.git
cd bioHealthScheduleManager/pyqt5_app
pip install -r requirements.txt && python main_kdt_full.py
```

**즐거운 학생 상담 되세요!** 🎓✨
