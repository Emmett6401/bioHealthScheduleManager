# -*- coding: utf-8 -*-
"""
KDT 애플리케이션 메인 실행 파일
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.kdt_main_window import KDTMainWindow


def main():
    """메인 함수"""
    app = QApplication(sys.argv)
    
    # 애플리케이션 스타일 설정
    app.setStyle('Fusion')
    
    # 메인 윈도우 생성 및 표시
    window = KDTMainWindow()
    window.show()
    
    # 이벤트 루프 실행
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
