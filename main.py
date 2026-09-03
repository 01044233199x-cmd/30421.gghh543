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
    {"name": "크로우", "image": "
