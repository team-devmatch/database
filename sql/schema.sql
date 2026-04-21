-- 사용자
CREATE TABLE users (
    user_id BIGSERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL UNIQUE,
    profile_image VARCHAR(500),
    role VARCHAR(20) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 축제행사
CREATE TABLE festival (
    festival_id BIGSERIAL PRIMARY KEY,
    content_id VARCHAR(50) NOT NULL,
    source VARCHAR(100) NOT NULL,
    name VARCHAR(200) NOT NULL,
    address VARCHAR(300),
    start_date VARCHAR(20),
    end_date VARCHAR(20),
    image_url VARCHAR(500),
    theme VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- 축제행사 상세페이지
CREATE TABLE festival_detail (
    detail_id BIGSERIAL PRIMARY KEY,
    festival_id BIGINT NOT NULL UNIQUE,
    description TEXT,
    tel VARCHAR(50),
    homepage VARCHAR(500),
    parking VARCHAR(200),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    sub_image_url VARCHAR(500),
    FOREIGN KEY (festival_id) REFERENCES festival(festival_id) ON DELETE CASCADE
);
-- 축제 후기
CREATE TABLE review (
    review_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    festival_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY(festival_id) REFERENCES festival(festival_id) ON DELETE CASCADE
);
-- 자유게시판
CREATE TABLE post(
    post_id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    category VARCHAR(20) NOT NULL,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    like_count INT DEFAULT 0,
    view_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
-- 자유게시판 상세 페이지
CREATE TABLE comment(
    comment_id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
-- 좋아요 표시
CREATE TABLE post_like(
    like_id BIGSERIAL PRIMARY KEY,
    post_id BIGINT NOT NULL,
    user_id BIGINT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(post_id) REFERENCES post(post_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE(post_id, user_id)
);