# database

ERD 설계 및 DDL 스크립트

## 구성

- erd/ → ERD 이미지 파일
- sql/ → DDL SQL 스크립트
- scripts/ → 데이터 수집 스크립트

## 기술 스택

- PostgreSQL (메인 DB)

## 주요 테이블

- USER → 사용자
- FESTIVAL → 축제 정보
- FESTIVAL_DETAIL → 축제 상세 정보
- REVIEW → 축제 후기
- POST → 게시판 글
- COMMENT → 댓글
- POST_LIKE → 게시글 좋아요

## 설계 원칙

- ON DELETE CASCADE 적용 (부모 삭제 시 자식 데이터 자동 삭제)
- UNIQUE 제약으로 중복 데이터 방지
- 자동완성 PK (BIGSERIAL) 적용

## 브랜치 규칙

- feature/erd-수정내용 → ERD 변경
- feature/ddl-수정내용 → SQL 변경
- main → 최종 확정본
