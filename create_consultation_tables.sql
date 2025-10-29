-- 면담 정보 테이블
CREATE TABLE IF NOT EXISTS consultations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    consultation_date DATETIME NOT NULL,
    location VARCHAR(200),
    main_topic VARCHAR(500),
    content TEXT,
    consultant_name VARCHAR(100),
    next_consultation_date DATETIME,
    consultation_type ENUM('정기', '수시', '긴급', '학부모') DEFAULT '정기',
    status ENUM('예정', '완료', '취소') DEFAULT '예정',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    INDEX idx_student_id (student_id),
    INDEX idx_consultation_date (consultation_date),
    INDEX idx_next_consultation_date (next_consultation_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 면담 사진 테이블
CREATE TABLE IF NOT EXISTS consultation_photos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    consultation_id INT NOT NULL,
    photo_path VARCHAR(500) NOT NULL,
    photo_description VARCHAR(500),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
    INDEX idx_consultation_id (consultation_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
