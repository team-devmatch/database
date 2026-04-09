# database

ERD 설계 및 DDL 스크립트

## 구성
- erd/ → ERD 이미지 파일
- sql/ → DDL SQL 스크립트

## 기술 스택
- PostgreSQL

## 주요 테이블
- USER → 사용자
- FESTIVAL → 축제 정보
- REGION → 지역
- COURSE → AI 추천 여행코스
- COURSE_ITEM → 코스 항목
- BOOKMARK → 북마크
- REVIEW → 후기

## 브랜치 규칙
- feature/erd-수정내용 → ERD 변경
- feature/ddl-수정내용 → SQL 변경
- main → 최종 확정본
