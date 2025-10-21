# -*- coding: utf-8 -*-
"""
데이터베이스 모델 및 연결 관리
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import sys
import os

# config 파일 import
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG, SQLITE_DB_PATH

Base = declarative_base()


class DatabaseManager:
    """데이터베이스 연결 및 세션 관리"""
    
    def __init__(self, use_sqlite=True):
        """
        Args:
            use_sqlite (bool): True이면 SQLite 사용, False이면 MySQL/PostgreSQL 사용
        """
        self.engine = None
        self.Session = None
        self.use_sqlite = use_sqlite
        
    def connect(self):
        """데이터베이스 연결"""
        try:
            if self.use_sqlite:
                # SQLite 연결
                db_path = os.path.join(os.path.dirname(__file__), '..', SQLITE_DB_PATH)
                connection_string = f'sqlite:///{db_path}'
            else:
                # MySQL/PostgreSQL 연결
                db_type = DB_CONFIG['type']
                user = DB_CONFIG['user']
                password = DB_CONFIG['password']
                host = DB_CONFIG['host']
                port = DB_CONFIG['port']
                database = DB_CONFIG['database']
                
                if db_type == 'mysql':
                    connection_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
                elif db_type == 'postgresql':
                    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
                else:
                    raise ValueError(f"지원하지 않는 데이터베이스 타입: {db_type}")
            
            self.engine = create_engine(connection_string, echo=False)
            self.Session = sessionmaker(bind=self.engine)
            
            # 테이블 생성
            Base.metadata.create_all(self.engine)
            
            return True
        except Exception as e:
            print(f"데이터베이스 연결 오류: {str(e)}")
            return False
    
    def get_session(self):
        """새로운 세션 반환"""
        if self.Session:
            return self.Session()
        return None
    
    def close(self):
        """데이터베이스 연결 종료"""
        if self.engine:
            self.engine.dispose()


# 예제 모델들
class User(Base):
    """사용자 모델"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"


class Note(Base):
    """노트 모델"""
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Note(id={self.id}, title='{self.title}')>"


# 데이터베이스 작업 함수들
def create_user(session, username, email):
    """사용자 생성"""
    try:
        user = User(username=username, email=email)
        session.add(user)
        session.commit()
        return user
    except Exception as e:
        session.rollback()
        print(f"사용자 생성 오류: {str(e)}")
        return None


def get_all_users(session):
    """모든 사용자 조회"""
    return session.query(User).all()


def create_note(session, title, content):
    """노트 생성"""
    try:
        note = Note(title=title, content=content)
        session.add(note)
        session.commit()
        return note
    except Exception as e:
        session.rollback()
        print(f"노트 생성 오류: {str(e)}")
        return None


def get_all_notes(session):
    """모든 노트 조회"""
    return session.query(Note).order_by(Note.updated_at.desc()).all()


def update_note(session, note_id, title=None, content=None):
    """노트 업데이트"""
    try:
        note = session.query(Note).filter(Note.id == note_id).first()
        if note:
            if title:
                note.title = title
            if content:
                note.content = content
            note.updated_at = datetime.now()
            session.commit()
            return note
        return None
    except Exception as e:
        session.rollback()
        print(f"노트 업데이트 오류: {str(e)}")
        return None


def delete_note(session, note_id):
    """노트 삭제"""
    try:
        note = session.query(Note).filter(Note.id == note_id).first()
        if note:
            session.delete(note)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"노트 삭제 오류: {str(e)}")
        return False
