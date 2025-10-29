# DeepSeek API 테스트 가이드 🧪

## 🔍 API 키 설정 확인

### 1단계: 환경 변수 확인

**Windows CMD:**
```bash
echo %DEEPSEEK_API_KEY%
```

**Windows PowerShell:**
```powershell
echo $env:DEEPSEEK_API_KEY
```

**출력 예시:**
```
sk-f80c9xxxxxxxxxxxxxxxx08b2
```

✅ 키가 표시되면 설정 완료!  
❌ 아무것도 안 나오면 다시 설정 필요

---

### 2단계: 환경 변수 설정 (필요 시)

#### Windows CMD (현재 세션만)
```bash
set DEEPSEEK_API_KEY=sk-your-deepseek-key-here
```

#### Windows PowerShell (현재 세션만)
```powershell
$env:DEEPSEEK_API_KEY="sk-your-deepseek-key-here"
```

#### Windows 영구 설정
1. **시스템 속성** 열기
   - Win + R → `sysdm.cpl` → Enter

2. **고급** 탭 → **환경 변수** 버튼

3. **사용자 변수** 섹션에서 **새로 만들기**
   - 변수 이름: `DEEPSEEK_API_KEY`
   - 변수 값: `sk-your-deepseek-key-here`

4. **확인** 클릭

5. **터미널 재시작** (중요!)

---

### 3단계: config.py 설정 (대안)

환경 변수 대신 파일에 직접 설정:

```python
# pyqt5_app/config.py 파일 열기

# 이 부분을 수정
DEEPSEEK_API_KEY = "sk-your-deepseek-key-here"  # 여기에 키 입력!
```

⚠️ **주의**: 이 방법은 GitHub에 푸시할 때 키가 노출될 수 있습니다.

---

## 🧪 테스트 방법

### 최신 코드 가져오기
```bash
git pull origin student
```

### 애플리케이션 실행
```bash
python main_kdt_full.py
```

### AI 보고서 생성 테스트
1. **학생 관리** 탭 클릭
2. **학생 면담 관리** 메뉴 선택
3. 면담 기록 작성 또는 선택
   - 학생: 홍길동
   - 주제: 진로 상담
   - 내용: AI 분야 관심, 수학 기초 부족
4. **"AI 면담일지 생성"** 버튼 클릭
5. 15-20초 대기

**예상 결과:**
```
✅ AI 면담일지가 생성되었습니다.
```

---

## 🔧 문제 해결

### 오류 1: "API 키가 설정되어 있지 않습니다"

**원인:** 환경 변수도 config.py도 설정 안 됨

**해결:**
```bash
# 환경 변수 설정
set DEEPSEEK_API_KEY=sk-your-key

# 또는 config.py 수정
```

---

### 오류 2: "Error code: 401 - Incorrect API key"

**원인:** 잘못된 API 키 또는 다른 API 엔드포인트로 요청

**해결:**
1. **DeepSeek 키 확인**
   ```bash
   echo %DEEPSEEK_API_KEY%
   ```
   
2. **올바른 키 형식인지 확인**
   - DeepSeek: `sk-` 로 시작
   - 약 60-70자 길이

3. **최신 코드인지 확인**
   ```bash
   git pull origin student
   git log --oneline -1
   # 출력: 688e2d0 또는 더 최신
   ```

4. **OpenAI 키와 혼동하지 않았는지 확인**
   - DeepSeek 키: https://platform.deepseek.com/
   - OpenAI 키: https://platform.openai.com/

---

### 오류 3: "Error code: 429 - Rate limit"

**원인:** 너무 많은 요청

**해결:**
- 1-2분 기다린 후 다시 시도
- DeepSeek는 무료이지만 초당 요청 수 제한 있음

---

### 오류 4: "Connection error"

**원인:** 네트워크 연결 문제

**해결:**
1. 인터넷 연결 확인
2. 방화벽 설정 확인
3. VPN 사용 시 해제 후 재시도

---

## 📊 API 감지 로직 확인

콘솔 출력을 확인하세요:

### DeepSeek 사용 시
```
✅ DeepSeek API 사용 중 (모델: deepseek-chat)
```

### OpenAI 사용 시
```
ℹ️ OpenAI API 사용 중 (모델: gpt-3.5-turbo)
```

---

## 🎯 올바른 설정 예시

### 환경 변수 (권장)

**CMD:**
```bash
set DEEPSEEK_API_KEY=sk-1234567890abcdef1234567890abcdef1234567890abcdef12345678
python main_kdt_full.py
```

**PowerShell:**
```powershell
$env:DEEPSEEK_API_KEY="sk-1234567890abcdef1234567890abcdef1234567890abcdef12345678"
python main_kdt_full.py
```

---

### config.py 파일

```python
# pyqt5_app/config.py

# DeepSeek API (무료)
DEEPSEEK_API_KEY = "sk-1234567890abcdef1234567890abcdef1234567890abcdef12345678"

# OpenAI API (유료, 대체용)
OPENAI_API_KEY = None
```

---

## ✅ 성공 확인

### 1. API 키 설정 확인
```bash
echo %DEEPSEEK_API_KEY%
# 출력: sk-xxxxxxxxxxxx
```

### 2. 코드 최신 버전 확인
```bash
git log --oneline -1
# 출력: 688e2d0 (또는 더 최신)
```

### 3. 애플리케이션 실행
```bash
python main_kdt_full.py
```

### 4. AI 보고서 생성
- 면담 관리 → AI 생성 버튼
- 콘솔 확인: `✅ DeepSeek API 사용 중`
- 15-20초 대기
- 보고서 생성 완료!

---

## 🎉 모든 것이 정상이면

```
=== AI 생성 학생 면담일지 ===

【기본 정보】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
학생명: 홍길동 (S-001)
면담 일시: 2025년 10월 29일 14:30
면담 장소: 상담실
면담 유형: 정기
상담사: 김선생
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. **면담 개요**
본 면담은 홍길동 학생의 진로 고민을 듣고...

(계속 8개 섹션)
```

---

## 💡 팁

### API 키 관리
- **환경 변수 사용 권장** (보안)
- **config.py는 테스트용으로만** (편의)
- **GitHub에 푸시 전 config.py 확인** (보안)

### 성능 최적화
- 면담 내용을 구체적으로 작성
- 2-3문장 이상 입력
- 핵심 키워드 포함

---

## 🔗 참고 링크

- **DeepSeek 가입**: https://platform.deepseek.com/
- **API 키 관리**: https://platform.deepseek.com/api_keys
- **DeepSeek 문서**: https://platform.deepseek.com/docs

---

**업데이트**: 2025-10-29  
**수정 커밋**: 최신 (API 감지 로직 수정)  
**상태**: ✅ 테스트 준비 완료
