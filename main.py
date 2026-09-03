import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="랜덤 브롤 추천", page_icon="🥊", layout="centered")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1a1a2e;
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 10px;
        }
        .container {
            background-color: #16213e;
            border-radius: 15px;
            padding: 25px;
            max-width: 450px;
            width: 100%;
            text-align: center;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
            border: 2px solid #0f3460;
            box-sizing: border-box;
        }
        h1 {
            color: #e94560;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }
        button {
            background-color: #e94560;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 1rem;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background-color 0.2s, transform 0.1s;
            width: 100%;
        }
        button:hover {
            background-color: #ff6b81;
        }
        button:disabled {
            background-color: #555;
            cursor: not-allowed;
        }
        .result-card {
            margin-top: 20px;
            display: none;
            background-color: #0f3460;
            border-radius: 10px;
            padding: 15px;
            text-align: left;
        }
        .brawler-image {
            width: 120px;
            height: 120px;
            object-fit: contain;
            border-radius: 12px;
            display: block;
            margin: 0 auto 10px auto;
            border: 3px solid #e94560;
            background-color: #1a1a2e;
        }
        .brawler-name {
            font-size: 1.5rem;
            text-align: center;
            color: #f9d342;
            margin-bottom: 15px;
            font-weight: bold;
        }
        .info-section {
            margin-bottom: 10px;
        }
        .info-title {
            font-weight: bold;
            color: #e94560;
            margin-bottom: 5px;
            font-size: 0.95rem;
        }
        .info-content {
            background-color: #16213e;
            padding: 8px 12px;
            border-radius: 5px;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        .synergy-list {
            margin: 0;
            padding-left: 20px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>랜덤 브롤 추천</h1>
    <button id="draw-btn" onclick="pickRandomBrawler()" disabled>데이터 불러오는 중...</button>

    <div id="result" class="result-card">
        <img id="brawler-img" class="brawler-image" src="" alt="브롤러 이미지">
        <div id="brawler-name" class="brawler-name"></div>
        
        <div class="info-section">
            <div class="info-title">🗺️ 추천 맵</div>
            <div id="recommended-map" class="info-content"></div>
        </div>

        <div class="info-section">
            <div class="info-title">🤝 추천 조합 브롤러 (5명)</div>
            <div class="info-content">
                <ul id="synergy-brawlers" class="synergy-list"></ul>
            </div>
        </div>
    </div>
</div>

<script>
    let brawlersData = [];

    // 한글 이름 매핑 dictionary
    const koreanNames = {
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
    };

    const maps = [
        "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)", 
        "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
        "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
    ];

    // Brawlify 공식 API에서 실제 브롤러 목록과 매칭되는 정확한 이미지 URL 로드
    async function initBrawlerData() {
        try
