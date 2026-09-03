import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="랜덤 브롤 추천", page_icon="🥊", layout="centered")

# HTML/CSS/JS 구현
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
        button:active {
            transform: scale(0.98);
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
            width: 110px;
            height: 110px;
            object-fit: cover;
            border-radius: 10px;
            display: block;
            margin: 0 auto 10px auto;
            border: 3px solid #e94560;
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
    <button onclick="pickRandomBrawler()">브롤러 뽑기!</button>

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
    const brawlers = Array.from({ length: 106 }, (_, i) => {
        const id = i + 1;
        
        if (id === 1) {
            return {
                name: "쉘리",
                image: "https://via.placeholder.com/120?text=Shelly",
                map: "우당탕 진흙탕 (쇼다운), 뱀의 초원 (바운티)",
                synergy: ["타라", "진", "스파이크", "버스터", "포코"]
            };
        }
        if (id === 2) {
            return {
                name: "콜트",
                image: "https://via.placeholder.com/120?text=Colt",
                map: "금암 사막 (하이스트), 브롤 볼 오픈 맵",
                synergy: ["브록", "파이퍼", "안젤로", "벨", "엘 프리모"]
            };
        }

        return {
            name: `브롤러 #${id}`,
            image: `https://via.placeholder.com/120?text=Brawler+${id}`,
            map: "우당탕 진흙탕, 우주선 정거장, 해골 천국",
            synergy: [
                `조합 브롤러 A`,
                `조합 브롤러 B`,
                `조합 브롤러 C`,
                `조합 브롤러 D`,
                `조합 브롤러 E`
            ]
        };
    });

    function pickRandomBrawler() {
        const randomIndex = Math.floor(Math.random() * brawlers.length);
        const selected = brawlers[randomIndex];

        document.getElementById('brawler-img').src = selected.image;
        document.getElementById('brawler-name').innerText = selected.name;
        document.getElementById('recommended-map').innerText = selected.map;

        const synergyList = document.getElementById('synergy-brawlers');
        synergyList.innerHTML = '';
        selected.synergy.forEach(brawler => {
            const li = document.createElement('li');
            li.innerText = brawler;
            synergyList.appendChild(li);
        });

        document.getElementById('result').style.display = 'block';
    }
</script>

</body>
</html>
"""

components.html(html_code, height=650)
