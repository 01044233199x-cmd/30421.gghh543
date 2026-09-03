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
    // 브롤러 정보 데이터 (한글 이름, 영문 파일명)
    const brawlerData = [
        { name: "쉘리", id: "shelly" }, { name: "콜트", id: "colt" }, { name: "니타", id: "nita" },
        { name: "불", id: "bull" }, { name: "엘 프리모", id: "el-primo" }, { name: "바리", id: "barley" },
        { name: "포코", id: "poco" }, { name: "로사", id: "rosa" }, { name: "리코", id: "rico" },
        { name: "데릴", id: "darryl" }, { name: "페니", id: "penny" }, { name: "칼", id: "carl" },
        { name: "재키", id: "jacky" }, { name: "거스", id: "gus" }, { name: "파이퍼", id: "piper" },
        { name: "팸", id: "pam" }, { name: "프랭크", id: "frank" }, { name: "비", id: "bea" },
        { name: "나니", id: "nani" }, { name: "에드가", id: "edgar" }, { name: "그리프", id: "griff" },
        { name: "그롬", id: "grom" }, { name: "보니", id: "bonnie" }, { name: "게일", id: "gale" },
        { name: "콜레트", id: "colette" }, { name: "벨", id: "belle" }, { name: "애쉬", id: "ash" },
        { name: "롤라", id: "lola" }, { name: "샘", id: "sam" }, { name: "메그", id: "meg" },
        { name: "메이지", id: "maisie" }, { name: "펄", id: "pearl" }, { name: "모티스", id: "mortis" },
        { name: "타라", id: "tara" }, { name: "진", id: "gene" }, { name: "맥스", id: "max" },
        { name: "스프라우트", id: "sprout" }, { name: "바이런", id: "byron" }, { name: "스퀴크", id: "squeak" },
        { name: "루", id: "lou" }, { name: "러프스", id: "ruffs" }, { name: "버즈", id: "buzz" },
        { name: "이브", id: "eve" }, { name: "자넷", id: "janet" }, { name: "오티스", id: "otis" },
        { name: "버스터", id: "buster" }, { name: "그레이", id: "gray" }, { name: "윌로우", id: "willow" },
        { name: "행크", id: "hank" }, { name: "더그", id: "doug" }, { name: "척", id: "chuck" },
        { name: "찰리", id: "charlie" }, { name: "미코", id: "mico" }, { name: "스파이크", id: "spike" },
        { name: "크로우", id: "crow" }, { name: "레온", id: "leon" }, { name: "샌디", id: "sandy" },
        { name: "앰버", id: "amber" }, { name: "체스터", id: "chester" }, { name: "코델리우스", id: "cordelius" },
        { name: "키트", id: "kit" }, { name: "드라코", id: "draco" }, { name: "클랜시", id: "clancy" },
        { name: "베리", id: "berry" }, { name: "모", id: "moe" }, { name: "켄지", id: "kenji" },
        { name: "안젤로", id: "angelo" }, { name: "멜로디", id: "melody" }, { name: "릴리", id: "lily" },
        { name: "8비트", id: "8-bit" }, { name: "엠즈", id: "emz" }, { name: "스튜", id: "stu" },
        { name: "틱", id: "tick" }, { name: "보", id: "bo" }, { name: "다이너마이크", id: "dynamike" }
    ];

    // 부족한 수량을 자동 채워서 106개 데이터로 세팅
    while(brawlerData.length < 106) {
        const index = brawlerData.length + 1;
        brawlerData.push({ name: `브롤러 ${index}`, id: "shelly" });
    }

    const maps = [
        "뱀의 초원 (바운티)", "우당탕 진흙탕 (쇼다운)", "금암 사막 (하이스트)", 
        "바위 광산 (잼 그랩)", "중앙 구역 (핫 존)", "우주선 정거장 (브롤 볼)",
        "해골 천국 (쇼다운)", "끝없는 야원 (바운티)", "A포인트 (핫 존)"
    ];

    function pickRandomBrawler() {
        const randomIndex = Math.floor(Math.random() * brawlerData.length);
        const selected = brawlerData[randomIndex];

        // 1순위: Brawlify 공식 고화질 렌더링 CDN
        const primaryImg = `https://cdn.brawlify.com/brawlers/borders/${selected.id}.png`;
        
        // 2순위: 로드 실패 시 이름 그래픽 카드
        const fallbackImg = `https://dummyimage.com/110x110/0f3460/ffffff.png&text=${encodeURIComponent(selected.name)}`;

        const imgElement = document.getElementById('brawler-img');
        imgElement.src = primaryImg;
        imgElement.onerror = function() {
            this.src = fallbackImg;
        };

        document.getElementById('brawler-name').innerText = selected.name;
        document.getElementById('recommended-map').innerText = maps[randomIndex % maps.length];

        // 조합 브롤러 추출
        const synergyList = document.getElementById('synergy-brawlers');
        synergyList.innerHTML = '';
        
        const otherBrawlers = brawlerData.filter(b => b.name !== selected.name);
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
