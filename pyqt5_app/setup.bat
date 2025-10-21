@echo off
echo ========================================
echo PyQt5 App 설치 스크립트
echo ========================================
echo.

echo [1/3] Conda 환경 생성 중...
call conda create -n pyqt5_app python=3.10 -y

echo.
echo [2/3] Conda 환경 활성화...
call conda activate pyqt5_app

echo.
echo [3/3] 필요한 패키지 설치 중...
pip install -r requirements.txt

echo.
echo ========================================
echo 설치가 완료되었습니다!
echo 실행하려면 run.bat 파일을 실행하세요.
echo ========================================
pause
