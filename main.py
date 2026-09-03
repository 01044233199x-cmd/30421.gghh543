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
        padding: 25px;
        margin-top: 20px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# 전체 브롤러 한글 이름 데이터베이스
BRAWLERS_DATABASE = [
    "쉘리", "콜트", "불", "브록", "리코", "스파이크", "발리", "제시", "니타", "다이너마이크",
    "엘 프리모", "모티스", "크로우", "포코", "보", "파이퍼", "타라", "팸", "프랭크", "페니",
    "데릴", "레온", "진", "칼", "로사", "비비", "틱", "8비트", "샌디", "엠즈",
    "비", "맥스", "미스터 P", "스프라우트", "잭키", "게일", "나니", "서지", "콜레트", "앰버",
    "루", "바이런", "에드가", "러프스", "스튜", "벨", "스퀴크", "그롬", "버즈", "그리프",
    "애쉬", "메그", "롤라", "팽", "이브", "자넷", "보니", "오티스", "샘", "거스",
    "버스터", "체스터", "그레이", "맨디", "윌로우", "메이지", "행크", "코델리우스", "더그", "펄",
    "척", "찰리", "미코", "키트", "라리 & 로리", "안젤로", "멜로디", "릴리", "드라코", "클랜시",
    "베리", "모", "켄지", "쥬쥬", "쉐이드"
]

MAPS_DATABASE = [
    "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)",
    "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
    "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
]

st.title("🥊 랜덤 브롤 추천")
st.write("버튼을 눌러 추천 브롤러와 최적의 조합을 확인하세요!")

# 세션 상태 초기화
if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

# 뽑기 버튼
if st.button("🎲 브롤러 뽑기!", use_container_width=True):
    target_name = random.choice(BRAWLERS_DATABASE)
    rec_map = random.choice(MAPS_DATABASE)
    
    # 추천 브롤러를 제외한 5명 무작위 선정
    other_names = [b for b in BRAWLERS_DATABASE if b != target_name]
    synergy_list = random.sample(other_names, 5)
    
    st.session_state.selected_result = {
        "name": target_name,
        "map": rec_map,
        "synergy": synergy_list
    }

# 결과 화면
if st.session_state.selected_result:
    res = st.session_state.selected_result
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
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
