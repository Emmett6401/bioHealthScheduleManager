-- 학생 테이블에 사진 경로 컬럼 추가

USE kdt_management;

-- photo_path 컬럼이 없으면 추가
ALTER TABLE students 
ADD COLUMN IF NOT EXISTS photo_path VARCHAR(500) COMMENT '학생 사진 파일 경로';

-- 인덱스 추가 (검색 성능 향상)
CREATE INDEX IF NOT EXISTS idx_students_photo ON students(photo_path);

SELECT 'photo_path 컬럼 추가 완료' as result;
