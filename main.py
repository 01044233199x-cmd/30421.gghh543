import streamlit as st
import requests

st.set_page_config(page_title="랜덤 브롤 추천", page_icon="🥊", layout="centered")

# 한글 이름 매핑 사전
KOREAN_NAMES = {
    "Shelly": "쉘리", "Colt": "콜트", "Bull": "불", "Brock": "브록", "Rico": "리코",
    "Spike": "스파이크", "Barley": "발리", "Jessie": "제시", "Nita": "니타", "Dynamike": "다이너마이크",
    "El Primo": "엘 프리모", "Mortis": "모티스", "Crow": "크로우", "Poco": "포코", "Bo": "보",
    "Piper": "파이퍼", "Tara": "타라", "Pam": "팸", "Frank": "프랭크", "Penny": "페니",
    "Darryl": "데릴", "Leon": "레온", "Gene": "진", "Carl": "칼", "Rosa": "로사",
    "Bibi": "비비", "Tick": "틱", "8-Bit": "8비트", "Sandy": "샌디", "Emz": "엠즈",
    "Bea": "비", "Max": "맥스", "Mr. P": "미스터 P", "Sprout": "스프라우트", "Jacky": "잭키",
    "Gale": "게일", "Nani": "나니", "Surge": "서지", "Colette": "콜레트", "Amber": "앰버",
    "Lou": "루", "Byron": "바이런", "Edgar": "에드가", "Ruffs": "러프스", "Stu": "스튜",
    "Belle": "벨", "Squeak": "스퀴크", "Grom": "그롬", "Buzz": "버즈", "Griff": "그리프", "Ash": "애쉬",
    "Meg": "메그", "Lola": "롤라", "Fang": "팽", "Eve": "이브", "Janet": "자넷",
    "Bonnie": "보니", "Otis": "오티스", "Sam": "샘", "Gus": "거스", "Buster": "버스터",
    "Chester": "체스터", "Gray": "그레이", "Mandy": "맨디", "Willow": "윌로우", "Maisie": "메이지",
    "Hank": "행크", "Cordelius": "코델리우스", "Doug": "더그", "Pearl": "펄", "Chuck": "척",
    "Charlie": "찰리", "Mico": "미코", "Kit": "키트", "Larry & Lawrie": "라리 & 로리", "Angelo": "안젤로",
    "Melodie": "멜로디", "Lily": "릴리", "Draco": "드라코", "Clancy": "클랜시", "Berry": "베리",
    "Moe": "모", "Kenji": "켄지", "Juju": "쥬쥬", "Shade": "쉐이드"
}

RECOMMENDED_MAPS = [
    "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)", 
    "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
    "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
]

@st.cache_data
def load_brawlers():
    try:
        res = requests.get("https://api.brawlify.com/v1/brawlers", timeout=10)
        data = res.json()
        brawlers = []
        for item in data.get("list", []):
            eng_name = item.get("name")
            kor_name = KOREAN_NAMES.get(eng_name, eng_name)
            img_url = item.get("imageUrl") or f"https://cdn.brawlify.com/brawlers/borderless/{item.get('id')}.png"
            brawlers.append({"name": kor_name, "image": img_url})
        return brawlers
    except Exception:
        return []

brawlers = load_brawlers()

st.title("🥊 랜덤 브롤 추천")

if not brawlers:
    st.error("브롤러 데이터를 불러오지 못했습니다. 네트워크 상태를 확인해주세요.")
else:
    if "selected_brawler" not in st.session_state:
        st.session_state.selected_brawler = None

    if st.button("🎲 브롤러 뽑기!", use_container_width=True):
        import random
        selected = random.choice(brawlers)
        
        # 조합 브롤러 5명 무작위 선정
        other_brawlers = [b["name"] for b in brawlers if b["name"] != selected["name"]]
        synergy = random.sample(other_brawlers, min(5, len(other_brawlers)))
        rec_map = random.choice(RECOMMENDED_MAPS)
        
        st.session_state.selected_brawler = {
            "name": selected["name"],
            "image": selected["image"],
            "map": rec_map,
            "synergy": synergy
        }

    if st.session_state.selected_brawler:
        res = st.session_state.selected_brawler
        
        st.divider()
        st.image(res["image"], width=120)
        st.subheader(f"✨ 추천 브롤러: {res['name']}")
        
        st.markdown(f"**🗺️ 추천 맵:** {res['map']}")
        
        st.markdown("**🤝 추천 조합 브롤러 (5명):**")
        for member in res["synergy"]:
            st.markdown(f"- {member}")
