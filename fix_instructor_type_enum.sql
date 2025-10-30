-- 강사 타입 ENUM 컬럼 수정
-- 12가지 타입 지원하도록 변경

USE kdt_schedule;

-- instructors 테이블의 type 컬럼 수정
ALTER TABLE instructors 
MODIFY COLUMN type ENUM(
    '1. 주강사',
    '2. 보조강사', 
    '3. 멘토',
    '4. 행정지원',
    '5. 외부강사',
    '6. 인턴',
    '7. 방문강사',
    '8. 온라인강사',
    '9. 특별강사',
    '10. 객원강사',
    '11. 수석강사',
    '12. 조교'
) DEFAULT '1. 주강사';

-- 변경 확인
SHOW CREATE TABLE instructors;
