import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="랜덤 브롤 추천",
    page_icon="🥊",
    layout="centered"
)

# UI 스타일 설정
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
    .result-card {
        background-color: #16213e;
        border: 2px solid #0f3460;
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 브롤러 이름과 1:1 검증된 이미지 URL 매핑 데이터
BRAWLERS_DATABASE = [
    {"name": "쉘리", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/0c/Shelly_Portrait.png"},
    {"name": "콜트", "image": "https://static.wikia.nocookie.net/brawlstars/images/5/54/Colt_Portrait.png"},
    {"name": "불", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f6/Bull_Portrait.png"},
    {"name": "브록", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/23/Brock_Portrait.png"},
    {"name": "리코", "image": "https://static.wikia.nocookie.net/brawlstars/images/c/c5/Rico_Portrait.png"},
    {"name": "스파이크", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/1a/Spike_Portrait.png"},
    {"name": "발리", "image": "https://static.wikia.nocookie.net/brawlstars/images/7/77/Barley_Portrait.png"},
    {"name": "제시", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/03/Jessie_Portrait.png"},
    {"name": "니타", "image": "https://static.wikia.nocookie.net/brawlstars/images/4/4b/Nita_Portrait.png"},
    {"name": "다이너마이크", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a2/Dynamike_Portrait.png"},
    {"name": "엘 프리모", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/10/El_Primo_Portrait.png"},
    {"name": "모티스", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f1/Mortis_Portrait.png"},
    {"name": "크로우", "image": "https://static.wikia.nocookie.net/brawlstars/images/5/52/Crow_Portrait.png"},
    {"name": "포코", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b3/Poco_Portrait.png"},
    {"name": "보", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f0/Bo_Portrait.png"},
    {"name": "파이퍼", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f0/Piper_Portrait.png"},
    {"name": "타라", "image": "https://static.wikia.nocookie.net/brawlstars/images/3/30/Tara_Portrait.png"},
    {"name": "팸", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b4/Pam_Portrait.png"},
    {"name": "프랭크", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f4/Frank_Portrait.png"},
    {"name": "페니", "image": "https://static.wikia.nocookie.net/brawlstars/images/9/91/Penny_Portrait.png"},
    {"name": "데릴", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/29/Darryl_Portrait.png"},
    {"name": "레온", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f2/Leon_Portrait.png"},
    {"name": "진", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/00/Gene_Portrait.png"},
    {"name": "칼", "image": "https://static.wikia.nocookie.net/brawlstars/images/7/7b/Carl_Portrait.png"},
    {"name": "로사", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/2a/Rosa_Portrait.png"},
    {"name": "비비", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f2/Bibi_Portrait.png"},
    {"name": "틱", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a9/Tick_Portrait.png"},
    {"name": "8비트", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f8/8-Bit_Portrait.png"},
    {"name": "샌디", "image": "https://static.wikia.nocookie.net/brawlstars/images/4/4e/Sandy_Portrait.png"},
    {"name": "엠즈", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/20/Emz_Portrait.png"},
    {"name": "비", "image": "https://static.wikia.nocookie.net/brawlstars/images/7/73/Bea_Portrait.png"},
    {"name": "맥스", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/23/Max_Portrait.png"},
    {"name": "미스터 P", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/22/Mr._P_Portrait.png"},
    {"name": "스프라우트", "image": "https://static.wikia.nocookie.net/brawlstars/images/4/43/Sprout_Portrait.png"},
    {"name": "잭키", "image": "https://static.wikia.nocookie.net/brawlstars/images/5/52/Jacky_Portrait.png"},
    {"name": "게일", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b8/Gale_Portrait.png"},
    {"name": "나니", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/1a/Nani_Portrait.png"},
    {"name": "서지", "image": "https://static.wikia.nocookie.net/brawlstars/images/8/87/Surge_Portrait.png"},
    {"name": "콜레트", "image": "https://static.wikia.nocookie.net/brawlstars/images/c/c8/Colette_Portrait.png"},
    {"name": "앰버", "image": "https://static.wikia.nocookie.net/brawlstars/images/7/70/Amber_Portrait.png"},
    {"name": "루", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a7/Lou_Portrait.png"},
    {"name": "바이런", "image": "https://static.wikia.nocookie.net/brawlstars/images/d/d4/Byron_Portrait.png"},
    {"name": "에드가", "image": "https://static.wikia.nocookie.net/brawlstars/images/9/90/Edgar_Portrait.png"},
    {"name": "러프스", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f7/Ruffs_Portrait.png"},
    {"name": "스튜", "image": "https://static.wikia.nocookie.net/brawlstars/images/e/e4/Stu_Portrait.png"},
    {"name": "벨", "image": "https://static.wikia.nocookie.net/brawlstars/images/d/d4/Belle_Portrait.png"},
    {"name": "스퀴크", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/07/Squeak_Portrait.png"},
    {"name": "그롬", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/1c/Grom_Portrait.png"},
    {"name": "버즈", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/1b/Buzz_Portrait.png"},
    {"name": "그리프", "image": "https://static.wikia.nocookie.net/brawlstars/images/3/30/Griff_Portrait.png"},
    {"name": "애쉬", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b3/Ash_Portrait.png"},
    {"name": "메그", "image": "https://static.wikia.nocookie.net/brawlstars/images/7/72/Meg_Portrait.png"},
    {"name": "롤라", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b1/Lola_Portrait.png"},
    {"name": "팽", "image": "https://static.wikia.nocookie.net/brawlstars/images/9/96/Fang_Portrait.png"},
    {"name": "이브", "image": "https://static.wikia.nocookie.net/brawlstars/images/3/36/Eve_Portrait.png"},
    {"name": "자넷", "image": "https://static.wikia.nocookie.net/brawlstars/images/8/8b/Janet_Portrait.png"},
    {"name": "보니", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a2/Bonnie_Portrait.png"},
    {"name": "오티스", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f0/Otis_Portrait.png"},
    {"name": "샘", "image": "https://static.wikia.nocookie.net/brawlstars/images/c/c0/Sam_Portrait.png"},
    {"name": "거스", "image": "https://static.wikia.nocookie.net/brawlstars/images/7/7a/Gus_Portrait.png"},
    {"name": "버스터", "image": "https://static.wikia.nocookie.net/brawlstars/images/6/6b/Buster_Portrait.png"},
    {"name": "체스터", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/07/Chester_Portrait.png"},
    {"name": "그레이", "image": "https://static.wikia.nocookie.net/brawlstars/images/2/27/Gray_Portrait.png"},
    {"name": "맨디", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a4/Mandy_Portrait.png"},
    {"name": "윌로우", "image": "https://static.wikia.nocookie.net/brawlstars/images/f/f1/Willow_Portrait.png"},
    {"name": "메이지", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/09/Maisie_Portrait.png"},
    {"name": "행크", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b5/Hank_Portrait.png"},
    {"name": "코델리우스", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/17/Cordelius_Portrait.png"},
    {"name": "더그", "image": "https://static.wikia.nocookie.net/brawlstars/images/8/87/Doug_Portrait.png"},
    {"name": "펄", "image": "https://static.wikia.nocookie.net/brawlstars/images/8/8d/Pearl_Portrait.png"},
    {"name": "척", "image": "https://static.wikia.nocookie.net/brawlstars/images/6/61/Chuck_Portrait.png"},
    {"name": "찰리", "image": "https://static.wikia.nocookie.net/brawlstars/images/b/b0/Charlie_Portrait.png"},
    {"name": "미코", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a2/Mico_Portrait.png"},
    {"name": "키트", "image": "https://static.wikia.nocookie.net/brawlstars/images/e/e0/Kit_Portrait.png"},
    {"name": "안젤로", "image": "https://static.wikia.nocookie.net/brawlstars/images/a/a3/Angelo_Portrait.png"},
    {"name": "멜로디", "image": "https://static.wikia.nocookie.net/brawlstars/images/5/52/Melodie_Portrait.png"},
    {"name": "릴리", "image": "https://static.wikia.nocookie.net/brawlstars/images/c/c2/Lily_Portrait.png"},
    {"name": "드라코", "image": "https://static.wikia.nocookie.net/brawlstars/images/e/e1/Draco_Portrait.png"},
    {"name": "클랜시", "image": "https://static.wikia.nocookie.net/brawlstars/images/0/01/Clancy_Portrait.png"},
    {"name": "베리", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/1a/Berry_Portrait.png"},
    {"name": "모", "image": "https://static.wikia.nocookie.net/brawlstars/images/d/d0/Moe_Portrait.png"},
    {"name": "켄지", "image": "https://static.wikia.nocookie.net/brawlstars/images/1/18/Kenji_Portrait.png"}
]

MAPS_DATABASE = [
    "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)",
    "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
    "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
]

st.title("🥊 랜덤 브롤 추천")

if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

if st.button("🎲 브롤러 뽑기!", use_container_width=True):
    target = random.choice(BRAWLERS_DATABASE)
    rec_map = random.choice(MAPS_DATABASE)
    
    other_names = [b["name"] for b in BRAWLERS_DATABASE if b["name"] != target["name"]]
    synergy_list = random.sample(other_names, 5)
    
    st.session_state.selected_result = {
        "name": target["name"],
        "image": target["image"],
        "map": rec_map,
        "synergy": synergy_list
    }

if st.session_state.selected_result:
    res = st.session_state.selected_result
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    # st.image를 사용해 안심하고 이미지 로딩
    st.image(res["image"], width=130)

    st.header(f"✨ {res['name']}")
    st.divider()
    
    st.subheader("🗺️ 추천 맵")
    st.info(res["map"])
    
    st.subheader("🤝 추천 조합 브롤러 (5명)")
    cols = st.columns(5)
    
    for i, name in enumerate(res["synergy"]):
        with cols[i]:
            st.success(f"**{name}**")
            
    st.markdown("</div>", unsafe_allow_html=True)
