import random
import requests
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="랜덤 브롤 추천",
    page_icon="🥊",
    layout="centered"
)

# 커스텀 CSS (스타일링)
st.markdown("""
    <style>
    .main {
        background-color: #1a1a2e;
    }
    .stApp {
        background-color: #1a1a2e;
        color: #ffffff;
    }
    div.stButton > button {
        background-color: #e94560;
        color: white;
        font-size: 18px;
        font-weight: bold;
        border-radius: 10px;
        border: none;
        padding: 12px 20px;
        width: 100%;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #ff6b81;
        color: white;
    }
    .result-box {
        background-color: #16213e;
        border: 2px solid #0f3460;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 1. 브롤러 영문-한글 명칭 1:1 매핑 사전 (전체 브롤러 포함)
BRAWLER_KOREAN_NAMES = {
    "Shelly": "쉘리", "Nita": "니타", "Colt": "콜트", "Bull": "불", "Brock": "브록",
    "El Primo": "엘 프리모", "Barley": "발리", "Poco": "포코", "Rosa": "로사", "Rico": "리코",
    "Darryl": "데릴", "Penny": "페니", "Carl": "칼", "Jacky": "잭키", "Gus": "거스",
    "Bo": "보", "Emz": "엠즈", "Stu": "스튜", "Piper": "파이퍼", "Pam": "팸",
    "Frank": "프랭크", "Bibi": "비비", "Bea": "비", "Nani": "나니", "Edgar": "에드가",
    "Griff": "그리프", "Grom": "그롬", "Bonnie": "보니", "Gale": "게일", "Colette": "콜레트",
    "Belle": "벨", "Ash": "애쉬", "Lola": "롤라", "Sam": "샘", "Mandy": "맨디",
    "Maisie": "메이지", "Pearl": "펄", "Larry & Lawrie": "라리 & 로리", "Mortis": "모티스", "Tara": "타라",
    "Gene": "진", "Max": "맥스", "Mr. P": "미스터 P", "Sprout": "스프라우트", "Byron": "바이런",
    "Squeak": "스퀴크", "Lou": "루", "Ruffs": "러프스", "Buzz": "버즈", "Eve": "이브",
    "Janet": "자넷", "Otis": "오티스", "Buster": "버스터", "Gray": "그레이", "Willow": "윌로우",
    "Hank": "행크", "Chuck": "척", "Charlie": "찰리", "Mico": "미코", "Spike": "스파이크",
    "Crow": "크로우", "Leon": "레온", "Sandy": "샌디", "Amber": "앰버", "Meg": "메그",
    "Chester": "체스터", "Cordelius": "코델리우스", "Kit": "키트", "Draco": "드라코", "Clancy": "클랜시",
    "Berry": "베리", "Moe": "모", "Kenji": "켄지", "Angelo": "안젤로", "Melodie": "멜로디",
    "Lily": "릴리", "Juju": "쥬쥬", "Shade": "쉐이드", "Tick": "틱", "8-Bit": "8비트",
    "Dynamike": "다이너마이크", "Doug": "더그"
}

# 2. 추천 맵 데이터베이스
MAPS_DATABASE = [
    "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)",
    "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
    "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)",
    "운하 성채 (바운티)", "좌우 대칭 (잼 그랩)", "우두머리 전투 (녹아웃)"
]

# 3. Brawlify API를 통해 최신 공식 브롤러 데이터 연동
@st.cache_data(show_spinner=False)
def fetch_official_brawlers():
    try:
        url = "https://api.brawlify.com/v1/brawlers"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            brawlers_list = []
            
            for item in data.get("list", []):
                eng_name = item.get("name")
                kor_name = BRAWLER_KOREAN_NAMES.get(eng_name, eng_name)
                
                # API에서 고유 ID를 기반으로 이미지 URL 추출 (1:1 매칭 보장)
                brawler_id = item.get("id")
                img_url = f"https://cdn.brawlify.com/brawlers/borderless/{brawler_id}.png"
                
                brawlers_list.append({
                    "id": brawler_id,
                    "kor_name": kor_name,
                    "eng_name": eng_name,
                    "image": img_url
                })
            return brawlers_list
    except Exception as e:
        pass
    return []

# 타이틀 출력
st.title("🥊 랜덤 브롤 추천")
st.write("버튼을 누르면 106명의 브롤러 중 한 명과 조합 정보가 출력됩니다!")

# 데이터 로딩
brawlers = fetch_official_brawlers()

if not brawlers:
    st.error("데이터를 불러오는데 실패했습니다. 네트워크 연결 상태를 확인 후 페이지를 새로고침 해주세요.")
else:
    # 세션 상태 초기화
    if "selected_result" not in st.session_state:
        st.session_state.selected_result = None

    # 추천 뽑기 버튼
    if st.button("🎲 브롤러 뽑기!"):
        # 1. 메인 브롤러 무작위 선택
        main_brawler = random.choice(brawlers)
        
        # 2. 추천 맵 무작위 선택
        recommended_map = random.choice(MAPS_DATABASE)
        
        # 3. 조합이 좋은 브롤러 5명 추출 (자기 자신 제외)
        other_brawlers = [b["kor_name"] for b in brawlers if b["id"] != main_brawler["id"]]
        synergy_team = random.sample(other_brawlers, min(5, len(other_brawlers)))
        
        # 결과 저장
        st.session_state.selected_result = {
            "name": main_brawler["kor_name"],
            "image": main_brawler["image"],
            "map": recommended_map,
            "synergy": synergy_team
        }

    # 결과 표시 영역
    if st.session_state.selected_result:
        res = st.session_state.selected_result
        
        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        
        # 브롤러 고유 이미지 출력
        st.image(res["image"], width=130)
        st.header(f"✨ {res['name']}")
        
        st.write("---")
        
        # 추천 맵 및 시너지 조합
        st.subheader("🗺️ 추천 맵")
        st.info(res["map"])
        
        st.subheader("🤝 추천 조합 브롤러 (5명)")
        cols = st.columns(5)
        for idx, member in enumerate(res["synergy"]):
            with cols[idx % 5]:
                st.success(f"**{member}**")
                
        st.markdown("</div>", unsafe_allow_html=True)
