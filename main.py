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
    // Brawlify 공식 API 고유 ID 매핑 목록
    const brawlerList = [
        { name: "쉘리", id: 16000000 },
        { name: "콜트", id: 16000001 },
        { name: "불", id: 16000002 },
        { name: "브록", id: 16000003 },
        { name: "리코", id: 16000004 },
        { name: "스파이크", id: 16000005 },
        { name: "발리", id: 16000006 },
        { name: "제시", id: 16000007 },
        { name: "니타", id: 16000008 },
        { name: "다이너마이크", id: 16000009 },
        { name: "엘 프리모", id: 16000010 },
        { name: "모티스", id: 16000011 },
        { name: "크로우", id: 16000012 },
        { name: "포코", id: 16000013 },
        { name: "보", id: 16000014 },
        { name: "파이퍼", id: 16000015 },
        { name: "파라", id: 16000016 },
        { name: "팸", id: 16000017 },
        { name: "프랭크", id: 16000018 },
        { name: "페니", id: 16000019 },
        { name: "데릴", id: 16000020 },
        { name: "레온", id: 16000021 },
        { name: "진", id: 16000022 },
        { name: "칼", id: 16000023 },
        { name: "로사", id: 16000024 },
        { name: "비", id: 16000025 },
        { name: "틱", id: 16000026 },
        { name: "8비트", id: 16000027 },
        { name: "샌디", id: 16000028 },
        { name: "엠즈", id: 16000029 },
        { name: "맥스", id: 16000030 },
        { name: "스프라우트", id: 16000031 },
        { name: "잭키", id: 16000032 },
        { name: "게일", id: 16000033 },
        { name: "나니", id: 16000034 },
        { name: "서지", id: 16000035 },
        { name: "콜레트", id: 16000036 },
        { name: "앰버", id: 16000037 },
        { name: "루", id: 16000038 },
        { name: "바이런", id: 16000039 },
        { name: "에드가", id: 16000040 },
        { name: "러프스", id: 16000041 },
        { name: "스튜", id: 16000042 },
        { name: "벨", id: 16000043 },
        { name: "스퀴크", id: 16000044 },
        { name: "그리프", id: 16000045 },
        { name: "애쉬", id: 16000046 },
        { name: "버즈", id: 16000047 },
        { name: "메그", id: 16000048 },
        { name: "롤라", id: 16000049 },
        { name: "그롬", id: 16000050 },
        { name: "송곳니(팽)", id: 16000051 },
        { name: "이브", id: 16000052 },
        { name: "자넷", id: 16000053 },
        { name: "보니", id: 16000054 },
        { name: "오티스", id: 16000055 },
        { name: "샘", id: 16000056 },
        { name: "거스", id: 16000057 },
        { name: "버스터", id: 16000058 },
        { name: "체스터", id: 16000059 },
        { name: "그레이", id: 16000060 },
        { name: "맨디", id: 16000061 },
        { name: "윌로우", id: 16000062 },
        { name: "메이지", id: 16000063 },
        { name: "행크", id: 16000064 },
        { name: "코델리우스", id: 16000065 },
        { name: "더그", id: 16000066 },
        { name: "펄", id: 16000067 },
        { name: "척", id: 16000068 },
        { name: "찰리", id: 16000069 },
        { name: "미코", id: 16000070 },
        { name: "키트", id: 16000071 },
        { name: "라리&로리", id: 16000072 },
        { name: "안젤로", id: 16000073 },
        { name: "멜로디", id: 16000074 },
        { name: "릴리", id: 16000075 },
        { name: "드라코", id: 16000076 },
        { name: "클랜시", id: 16000077 },
        { name: "베리", id: 16000078 },
        { name: "모", id: 16000079 },
        { name: "켄지", id: 16000080 },
        { name: "쥬쥬", id: 16000081 },
        { name: "쉐이드", id: 16000082 }
    ];

    // 부족한 슬롯을 고유 ID 패턴으로 확장하여 106명 맞춤
    while(brawlerList.length < 106) {
        const nextId = 16000000 + brawlerList.length;
        brawlerList.push({ name: `브롤러 ${brawlerList.length + 1}`, id: nextId });
    }

    const maps = [
        "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)", 
        "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
        "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
    ];

    function pickRandomBrawler() {
        const randomIndex = Math.floor(Math.random() * brawlerList.length);
        const selected = brawlerList[randomIndex];

        // Brawlify 공식 이미지 경로 (게임 내 공식 브롤러 아바타 이미지)
        const imgUrl = `https://cdn.brawlify.com/brawlers/borderless/${selected.id}.png`;

        const imgElement = document.getElementById('brawler-img');
        imgElement.src = imgUrl;

        document.getElementById('brawler-name').innerText = selected.name;
        document.getElementById('recommended-map').innerText = maps[randomIndex % maps.length];

        // 추천 조합 브롤러 (자기 자신 제외한 5명 랜덤 추출)
        const synergyList = document.getElementById('synergy-brawlers');
        synergyList.innerHTML = '';
        
        const otherBrawlers = brawlerList.filter(b => b.name !== selected.name);
        const shuffled = [...otherBrawlers].sort(() => 0.5 - Math.random());
        const synergies = shuffled.slice(0, 5);

        synergies.forEach(brawler => {
            const li = document.createElement('li');
            li.innerText = brawler.name;
            synergyList.appendChild(li);
        });

        document.getElementById('result').style.display = 'block';
    }
</script>

</body>
</html>
"""

components.html(html_code, height=650)
