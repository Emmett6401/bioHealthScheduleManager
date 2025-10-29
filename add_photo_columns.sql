-- 학생 테이블에 사진 관련 컬럼 추가
-- photo_path: 원본 이미지 파일 경로
-- thumbnail: 썸네일 이미지 (BLOB)

USE bh2025;

ALTER TABLE students 
ADD COLUMN photo_path VARCHAR(500) COMMENT '원본 사진 파일 경로' AFTER campus,
ADD COLUMN thumbnail MEDIUMBLOB COMMENT '썸네일 이미지 (150x150)' AFTER photo_path;

-- 결과 확인
DESC students;
