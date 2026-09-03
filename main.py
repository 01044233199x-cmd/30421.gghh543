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
            width: 110px;
            height: 110px;
            object-fit: contain;
            border-radius: 10px;
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
    // 브롤스타즈 브롤러 목록 데이터
    const brawlerNames = [
        "쉘리", "니타", "콜트", "불", "엘 프리모", "바리", "포코", "로사", "리코", "데릴",
        "페니", "칼", "재키", "거스", "파이퍼", "팸", "프랭크", "비", "나니", "에드가",
        "그리프", "그롬", "보통", "보니", "게일", "콜레트", "벨", "애쉬", "롤라", "샘",
        "메그", "메이지", "펄", "라리&로리", "모티스", "타라", "진", "맥스", "스프라우트", "바이런",
        "스퀴크", "루", "러프스", "버즈", "이브", "자넷", "오티스", "버스터", "그레이", "윌로우",
        "행크", "코드", "더그", "척", "찰리", "밀코", "스파이크", "크로우", "레온", "샌디",
        "앰버", "메구", "체스터", "코델리우스", "키트", "드라코", "클랜시", "베리", "모", "켄지",
        "안젤로", "메이시", "멜로디", "릴리", "쥬쥬", "쉐이드", "피파", "핀", "올리", "피어스",
        "바이론", "8비트", "엠즈", "스튜", "틱", "보", "다이너마이크", "체스터", "게일", "벨",
        "애쉬", "롤라", "샘", "버스터", "메이지", "펄", "찰리", "러프스", "오티스", "윌로우",
        "행크", "더그", "척", "키트", "드라코", "클랜시"
    ];

    const maps = [
        "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)", 
        "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
        "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
    ];

    const brawlers = brawlerNames.map((name, index) => {
        // 실제 공식 렌더링 이미지 경로 규격 적용 (대문자/특수문자 처리)
        const formattedName = name.toLowerCase().replace(/[^a-z0-9]/g, '');
        const imageUrl = `https://cdn.brawlify.com/brawlers/borderless/${index + 1}.png`;

        // 조합 브롤러 5명 추출 (자기 자신 제외)
        const otherBrawlers = brawlerNames.filter(b => b !== name);
        const shuffled = [...otherBrawlers].sort(() => 0.5 - Math.random());
        const synergy = shuffled.slice(0, 5);

        const randomMap = maps[index % maps.length];

        return {
            name: name,
            image: imageUrl,
            map: randomMap,
            synergy: synergy
        };
    });

    function pickRandomBrawler() {
        const randomIndex = Math.floor(Math.random() * brawlers.length);
        const selected = brawlers[randomIndex];

        const imgElement = document.getElementById('brawler-img');
        imgElement.src = selected.image;
        imgElement.onerror = function() {
            // 이미지 로드 실패 시 플레이스홀더 이미지로 대체
            this.src = `https://via.placeholder.com/110/0f3460/ffffff?text=${encodeURIComponent(selected.name)}`;
        };

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
