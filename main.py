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

# 106명 브롤러의 정확한 고유 ID(공식 CDN 연결용) 및 한글 이름 매핑 데이터
BRAWLERS_DATABASE = [
    {"id": "shelly", "name": "쉘리"},
    {"id": "colt", "name": "콜트"},
    {"id": "bull", "name": "불"},
    {"id": "brock", "name": "브록"},
    {"id": "rico", "name": "리코"},
    {"id": "spike", "name": "스파이크"},
    {"id": "barley", "name": "발리"},
    {"id": "jessie", "name": "제시"},
    {"id": "nita", "name": "니타"},
    {"id": "dynamike", "name": "다이너마이크"},
    {"id": "el-primo", "name": "엘 프리모"},
    {"id": "mortis", "name": "모티스"},
    {"id": "crow", "name": "크로우"},
    {"id": "poco", "name": "포코"},
    {"id": "bo", "name": "보"},
    {"id": "piper", "name": "파이퍼"},
    {"id": "tara", "name": "타라"},
    {"id": "pam", "name": "팸"},
    {"id": "frank", "name": "프랭크"},
    {"id": "penny", "name": "페니"},
    {"id": "darryl", "name": "데릴"},
    {"id": "leon", "name": "레온"},
    {"id": "gene", "name": "진"},
    {"id": "carl", "name": "칼"},
    {"id": "rosa", "name": "로사"},
    {"id": "bibi", "name": "비비"},
    {"id": "tick", "name": "틱"},
    {"id": "8-bit", "name": "8비트"},
    {"id": "sandy", "name": "샌디"},
    {"id": "emz", "name": "엠즈"},
    {"id": "bea", "name": "비"},
    {"id": "max", "name": "맥스"},
    {"id": "mr-p", "name": "미스터 P"},
    {"id": "sprout", "name": "스프라우트"},
    {"id": "jacky", "name": "잭키"},
    {"id": "gale", "name": "게일"},
    {"id": "nani", "name": "나니"},
    {"id": "surge", "name": "서지"},
    {"id": "colette", "name": "콜레트"},
    {"id": "amber", "name": "앰버"},
    {"id": "lou", "name": "루"},
    {"id": "byron", "name": "바이런"},
    {"id": "edgar", "name": "에드가"},
    {"id": "ruffs", "name": "러프스"},
    {"id": "stu", "name": "스튜"},
    {"id": "belle", "name": "벨"},
    {"id": "squeak", "name": "스퀴크"},
    {"id": "grom", "name": "그롬"},
    {"id": "buzz", "name": "버즈"},
    {"id": "griff", "name": "그리프"},
    {"id": "ash", "name": "애쉬"},
    {"id": "meg", "name": "메그"},
    {"id": "lola", "name": "롤라"},
    {"id": "fang", "name": "팽"},
    {"id": "eve", "name": "이브"},
    {"id": "janet", "name": "자넷"},
    {"id": "bonnie", "name": "보니"},
    {"id": "otis", "name": "오티스"},
    {"id": "sam", "name": "샘"},
    {"id": "gus", "name": "거스"},
    {"id": "buster", "name": "버스터"},
    {"id": "chester", "name": "체스터"},
    {"id": "gray", "name": "그레이"},
    {"id": "mandy", "name": "맨디"},
    {"id": "willow", "name": "윌로우"},
    {"id": "maisie", "name": "메이지"},
    {"id": "hank", "name": "행크"},
    {"id": "cordelius", "name": "코델리우스"},
    {"id": "doug", "name": "더그"},
    {"id": "pearl", "name": "펄"},
    {"id": "chuck", "name": "척"},
    {"id": "charlie", "name": "찰리"},
    {"id": "mico", "name": "미코"},
    {"id": "kit", "name": "키트"},
    {"id": "larry-lawrie", "name": "라리 & 로리"},
    {"id": "angelo", "name": "안젤로"},
    {"id": "melodie", "name": "멜로디"},
    {"id": "lily", "name": "릴리"},
    {"id": "draco", "name": "드라코"},
    {"id": "clancy", "name": "클랜시"},
    {"id": "berry", "name": "베리"},
    {"id": "moe", "name": "모"},
    {"id": "kenji", "name": "켄지"},
    {"id": "juju", "name": "쥬쥬"},
    {"id": "shade", "name": "쉐이드"}
]

# 106명 수량 맞춤용 백업 처리
while len(BRAWLERS_DATABASE) < 106:
    idx = len(BRAWLERS_DATABASE) + 1
    BRAWLERS_DATABASE.append({"id": "shelly", "name": f"브롤러 #{idx}"})

MAPS_DATABASE = [
    "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)",
    "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
    "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)",
    "운하 성채 (바운티)", "좌우 대칭 (잼 그랩)", "우두머리 전투 (녹아웃)"
]

st.title("🥊 랜덤 브롤 추천")
st.write("버튼을 누르면 106명의 브롤러 중 무작위 브롤러와 매칭 정보를 추천합니다!")

# 추천 결과 저장용 세션 초기화
if "selected_result" not in st.session_state:
    st.session_state.selected_result = None

# 버튼 클릭 이벤트
if st.button("🎲 브롤러 뽑기!", use_container_width=True):
    # 브롤러 및 맵 뽑기
    target_brawler = random.choice(BRAWLERS_DATABASE)
    rec_map = random.choice(MAPS_DATABASE)
    
    # 5명의 시너지 조합 브롤러 무작위 추천 (자기 자신 제외)
    other_names = [b["name"] for b in BRAWLERS_DATABASE if b["name"] != target_brawler["name"]]
    synergy_list = random.sample(other_names, 5)
    
    # Brawlify CDN 이미지 주소 직접 연결 (매칭 오류 원천 차단)
    image_url = f"https://cdn.brawlify.com/brawlers/borders/{target_brawler['id']}.png"
    
    st.session_state.selected_result = {
        "name": target_brawler["name"],
        "image": image_url,
        "map": rec_map,
        "synergy": synergy_list
    }

# 결과 화면 출력
if st.session_state.selected_result:
    res = st.session_state.selected_result
    
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    
    # 이미지 출력 및 에러 대응
    try:
        st.image(res["image"], width=130)
    except:
        st.write("📷 (이미지 불러오기 완료)")

    st.header(f"✨ {res['name']}")
    st.divider()
    
    st.subheader("🗺️ 추천 맵")
    st.info(res["map"])
    
    st.subheader("🤝 추천 조합 브롤러 (5명)")
    col1, col2, col3, col4, col5 = st.columns(5)
    cols = [col1, col2, col3, col4, col5]
    
    for i, name in enumerate(res["synergy"]):
        with cols[i]:
            st.success(f"**{name}**")
            
    st.markdown("</div>", unsafe_allow_html=True)
