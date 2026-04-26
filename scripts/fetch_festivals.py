import requests
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

# API 설정
API_KEY = "3be7613e84638bbf1b77b63b3d03376b87534d6c9a6cea6c3129c59a48d685e0"
BASE_URL = "https://apis.data.go.kr/B551011/KorService2/searchFestival2"

# DB 연결
conn = psycopg2.connect(
    host = os.getenv("DB_HOST", "localhost"),
    port = os.getenv("DB_PORT", 5432),
    database = os.getenv("DB_NAME", "festivaldb"),
    user = os.getenv("DB_USER", "admin"),
    password = os.getenv("DB_PASSWORD", "password")
)
cursor = conn.cursor()

# 키워드 기반 테마 분류
def get_theme(name, description):
    text = f"{name} {description}".lower()
    # 가족과 함께
    family_keywords = [
    "가족", "어린이", "아이", "키즈", "유아",
    "부모", "자녀", "육아", "엄마", "아빠",
    "가정", "초등", "유치", "어른이", "온가족",
    "가족나들이", "가족여행", "아동", "패밀리"
    ]
    # 연인과 함께
    couple_keywords = [
    "연인", "커플", "데이트", "로맨틱", "낭만",
    "사랑", "둘이", "부부", "신혼", "프로포즈",
    "러브", "연애", "달콤", "감성", "야경",
    "불꽃", "야간", "밤", "야외공연"
    ]
    # 친구와 함께
    friend_keywords = [
    "친구", "동반", "단체", "청년", "젊은",
    "대학", "청소년", "또래", "무리", "그룹",
    "동아리", "모임", "파티", "축제즐기기",
    "신나는", "흥겨운", "신명", "흥"
    ]
    # 자연 코스
    nature_keywords = [
    "자연", "숲", "산", "바다", "강", "계곡",
    "꽃", "벚꽃", "단풍", "유채", "해바라기",
    "연꽃", "장미", "매화", "봄꽃", "가을꽃",
    "갯벌", "해변", "해안", "등산", "트레킹",
    "둘레길", "생태", "식물", "나무", "정원",
    "호수", "폭포", "섬", "야생화", "들꽃",
    "청정", "녹색", "초록", "풀밭", "들판"
    ]
    # 힐링 코스
    healing_keywords = [
    "힐링", "치유", "휴식", "명상", "웰빙",
    "힐", "템플", "요가", "치료", "건강",
    "마음", "평화", "고요", "여유", "쉼",
    "온천", "스파", "족욕", "한방", "약초",
    "전통", "느린", "슬로우", "고즈넉", "한적",
    "힐링여행", "자아", "명상", "집중"
    ]
    # 관광두레
    tourism_keywords = [
    "관광두레", "두레", "마을", "지역", "주민",
    "전통마을", "민속", "향토", "지역주민",
    "공동체", "협동", "마을기업", "로컬",
    "지역특산", "농촌", "어촌", "산촌",
    "전통시장", "시장", "5일장", "장터",
    "지역축제", "향토축제", "마을축제"
    ]

    if any(k in text for k in family_keywords):
        return "가족과함께"
    elif any(k in text for k in couple_keywords):
        return "연인과함께"
    elif any(k in text for k in friend_keywords):
        return "친구와함께"
    elif any(k in text for k in nature_keywords):
        return "자연코스"
    elif any(k in text for k in healing_keywords):
        return "힐링코스"
    elif any(k in text for k in tourism_keywords):
        return "관광두레"
    
# 전국 축제 수집 
def fetch_festivals():
    print("\n=== 기본 정보 수집 시작 ===")
    page = 1
    total_saved = 0
    
    while True:
        print(f"페이지 {page} 수집 중..")

        try:
            url = f"{BASE_URL}?serviceKey={API_KEY}&numOfRows=100&pageNo={page}&MobileOS=ETC&MobileApp=FestAI&_type=json&eventStartDate=20260101&arrange=A"
            response = requests.get(url, timeout=10)
            data = response.json()

            body = data["response"]["body"]
            total_count = body["totalCount"]
            items = body["items"]

            if not items:
                print("더 이상 데이터 없음. 수집 완료!")
                break

            item_list = items["item"]

            if isinstance(item_list, dict):
                item_list = [item_list]

            for item in item_list:
                try:
                    name = item.get("title","") or ""
                    description = item.get("overview","") or ""
                    theme = get_theme(name, description)

                    cursor.execute("""
                        INSERT INTO festival(
                            content_id, source, name,
                            address, start_date, end_date,
                            image_url, theme, created_at
                        ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                        ON CONFLICT DO NOTHING
                    """, (
                        item.get("contentid"),
                        "한국관광공사",
                        name,
                        item.get("addr1"),
                        item.get("eventstartdate"),
                        item.get("eventenddate"),
                        item.get("firstimage"),
                        theme
                    ))
                    total_saved += 1
                    print(f"저장: {name} -> {theme}")

                except Exception as e:
                    print(f"저장 오류 ({name}): {e}")
                    continue

            conn.commit()
            print(f"페이지 {page} 완료! (누적: {total_saved}건)")

            if page * 100 >= total_count:
                print(f"\n전체 {total_count}건 수집 완료!")
                break

            page += 1

        except Exception as e:
            print(f"API 오류: {e}")
            break

#상세 정보 수집 + 소개글로 테마 재분류
def fetch_festival_details():
    print("\n=== 상세 정보 수집 시작 ===")

    cursor.execute(
        "SELECT festival_id, content_id, name FROM festival"
    )
    festivals = cursor.fetchall()
    total = len(festivals)
    print(f"총 {total}건 상세 정보 수집 예정")

    for index, (festival_id, content_id, name) in enumerate(festivals, 1):
        try:
            print(f"[{index}/{total}] {name} 상세 수집 중...")

            #공통 정보 조회
            url = f"https://apis.data.go.kr/B551011/KorService2/detailCommon2?serviceKey={API_KEY}&contentId={content_id}&MobileOS=ETC&MobileApp=FestAI&_type=json"
            response = requests.get(url, timeout=10)

            data = response.json()
            item = data["response"]["body"]["items"]["item"]

            if isinstance(item, list):
                item = item[0]

            #소개 정보 조회
            url2 = f"https://apis.data.go.kr/B551011/KorService2/detailIntro2?serviceKey={API_KEY}&contentId={content_id}&contentTypeId=15&MobileOS=ETC&MobileApp=FestAI&_type=json"
            response2 = requests.get(url2, timeout=10)
            data2 = response2.json()
            item2 = data2["response"]["body"]["items"]["item"]

            if isinstance(item2, list):
                item2 = item2[0]

            #소개글로 테마 재분류
            description = item.get("overview", "") or ""
            new_theme = get_theme(name, description)

            #festival_datail 저장
            cursor.execute("""
                INSERT INTO festival_detail (
                    festival_id, description, tel,
                    homepage, parking,
                    latitude, longitude, sub_image_url
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (festival_id) DO NOTHING
            """, (
                festival_id,
                description,
                item.get("tel"),
                item.get("homepage"),
                item2.get("parking") if item2 else None,
                item.get("mapy"),
                item.get("mapx"),
                item.get("firstimage2")
            ))

            #기존 "전체"로 저장된 것만 재분류
            cursor.execute("""
                UPDATE festival
                SET theme = %s
                WHERE festival_id = %s
            """, (new_theme, festival_id))

            conn.commit()
            print(f" -> 상세 저장 완료: {name} / 테마: {new_theme}")

        except Exception as e:
            print(f" -> 상세 오류 ({name}): {e}")
            continue

    print("\n=== 상세 정보 수집 완료 ===")

#분류 결과 확인
def check_theme_stats():
    print("\n=== 테마별 분류 결과 ===")
    cursor.execute("""
        SELECT theme, COUNT(*) as count
        FROM festival
        GROUP BY theme
        ORDER BY count DESC
    """)
    results = cursor.fetchall()
    for theme, count in results:
        print(f"{theme}: {count}건")
    print("========================")

#실행
if __name__ == "__main__":
    print("=============================")
    print("=== 축제 데이터 수집 시작 ===")
    print("=============================")
    fetch_festivals()
    fetch_festival_details()
    check_theme_stats()
    cursor.close()
    conn.close()
    print("\n=== 전체 수집 완료 ===")



