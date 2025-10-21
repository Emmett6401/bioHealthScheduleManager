# -*- coding: utf-8 -*-
"""
유틸리티 헬퍼 함수들
"""

from datetime import datetime
import re


def format_datetime(dt, format_str='%Y-%m-%d %H:%M:%S'):
    """
    datetime 객체를 문자열로 포맷팅
    
    Args:
        dt: datetime 객체
        format_str: 포맷 문자열
    
    Returns:
        str: 포맷팅된 날짜 문자열
    """
    if isinstance(dt, datetime):
        return dt.strftime(format_str)
    return str(dt)


def validate_email(email):
    """
    이메일 유효성 검사
    
    Args:
        email: 이메일 주소
    
    Returns:
        bool: 유효하면 True, 아니면 False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def truncate_text(text, max_length=50, suffix='...'):
    """
    텍스트를 지정된 길이로 자르기
    
    Args:
        text: 원본 텍스트
        max_length: 최대 길이
        suffix: 잘린 부분에 추가할 접미사
    
    Returns:
        str: 잘린 텍스트
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def sanitize_filename(filename):
    """
    파일명에서 특수문자 제거
    
    Args:
        filename: 원본 파일명
    
    Returns:
        str: 정제된 파일명
    """
    # Windows에서 사용할 수 없는 문자들 제거
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename


def bytes_to_human_readable(bytes_size):
    """
    바이트 크기를 읽기 쉬운 형식으로 변환
    
    Args:
        bytes_size: 바이트 크기
    
    Returns:
        str: 읽기 쉬운 형식 (예: 1.5 MB)
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"
