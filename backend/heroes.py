# 오버워치2 영웅 데이터 (2025년 기준)
# 역할: tank(돌격), dps(공격), support(지원)

HEROES = {
    # 돌격 (Tank) - 14명
    "dva": {"name": "D.Va", "name_ko": "디바", "role": "tank"},
    "doomfist": {"name": "Doomfist", "name_ko": "둠피스트", "role": "tank"},
    "junker_queen": {"name": "Junker Queen", "name_ko": "정커퀸", "role": "tank"},
    "mauga": {"name": "Mauga", "name_ko": "마우가", "role": "tank"},
    "orisa": {"name": "Orisa", "name_ko": "오리사", "role": "tank"},
    "ramattra": {"name": "Ramattra", "name_ko": "라마트라", "role": "tank"},
    "reinhardt": {"name": "Reinhardt", "name_ko": "라인하르트", "role": "tank"},
    "roadhog": {"name": "Roadhog", "name_ko": "로드호그", "role": "tank"},
    "sigma": {"name": "Sigma", "name_ko": "시그마", "role": "tank"},
    "winston": {"name": "Winston", "name_ko": "윈스턴", "role": "tank"},
    "wrecking_ball": {"name": "Wrecking Ball", "name_ko": "레킹볼", "role": "tank"},
    "zarya": {"name": "Zarya", "name_ko": "자리야", "role": "tank"},
    "hazard": {"name": "Hazard", "name_ko": "해저드", "role": "tank"},
    "domina": {"name": "Domina", "name_ko": "도미나", "role": "tank"},
    
    
    # 공격 (DPS) - 22명
    "ashe": {"name": "Ashe", "name_ko": "애쉬", "role": "dps"},
    "bastion": {"name": "Bastion", "name_ko": "바스티온", "role": "dps"},
    "cassidy": {"name": "Cassidy", "name_ko": "캐서디", "role": "dps"},
    "echo": {"name": "Echo", "name_ko": "에코", "role": "dps"},
    "genji": {"name": "Genji", "name_ko": "겐지", "role": "dps"},
    "hanzo": {"name": "Hanzo", "name_ko": "한조", "role": "dps"},
    "junkrat": {"name": "Junkrat", "name_ko": "정크랫", "role": "dps"},
    "mei": {"name": "Mei", "name_ko": "메이", "role": "dps"},
    "pharah": {"name": "Pharah", "name_ko": "파라", "role": "dps"},
    "reaper": {"name": "Reaper", "name_ko": "리퍼", "role": "dps"},
    "sojourn": {"name": "Sojourn", "name_ko": "소전", "role": "dps"},
    "soldier_76": {"name": "Soldier: 76", "name_ko": "솔저: 76", "role": "dps"},
    "sombra": {"name": "Sombra", "name_ko": "솜브라", "role": "dps"},
    "symmetra": {"name": "Symmetra", "name_ko": "시메트라", "role": "dps"},
    "torbjorn": {"name": "Torbjörn", "name_ko": "토르비욘", "role": "dps"},
    "tracer": {"name": "Tracer", "name_ko": "트레이서", "role": "dps"},
    "venture": {"name": "Venture", "name_ko": "벤처", "role": "dps"},
    "widowmaker": {"name": "Widowmaker", "name_ko": "위도우메이커", "role": "dps"},
    "freja": {"name": "Freja", "name_ko": "프레야", "role": "dps"},
    "vendetta": {"name": "Vendetta", "name_ko": "벤데타", "role": "dps"},
    "anran": {"name": "Anran", "name_ko": "안란", "role": "dps"},
    "emre": {"name": "Emre", "name_ko": "엠레", "role": "dps"},
    
    
    # 지원 (Support) - 14명
    "ana": {"name": "Ana", "name_ko": "아나", "role": "support"},
    "baptiste": {"name": "Baptiste", "name_ko": "바티스트", "role": "support"},
    "brigitte": {"name": "Brigitte", "name_ko": "브리기테", "role": "support"},
    "illari": {"name": "Illari", "name_ko": "일리아리", "role": "support"},
    "juno": {"name": "Juno", "name_ko": "주노", "role": "support"},
    "kiriko": {"name": "Kiriko", "name_ko": "키리코", "role": "support"},
    "lifeweaver": {"name": "Lifeweaver", "name_ko": "라이프위버", "role": "support"},
    "lucio": {"name": "Lúcio", "name_ko": "루시우", "role": "support"},
    "mercy": {"name": "Mercy", "name_ko": "메르시", "role": "support"},
    "moira": {"name": "Moira", "name_ko": "모이라", "role": "support"},
    "zenyatta": {"name": "Zenyatta", "name_ko": "젠야타", "role": "support"},
    "wuyang": {"name": "Wuyang", "name_ko": "우양", "role": "support"},
    "mizuki": {"name": "Mizuki", "name_ko": "미즈키", "role": "support"},
    "jetpack_cat": {"name": "Jetpack_cat", "name_ko": "제트팩 캣", "role": "support"},
}

# 역할별 영웅 ID 리스트
TANKS = [h for h, data in HEROES.items() if data["role"] == "tank"]
DPS = [h for h, data in HEROES.items() if data["role"] == "dps"]
SUPPORTS = [h for h, data in HEROES.items() if data["role"] == "support"]

def get_heroes_by_role(role: str) -> list:
    """역할별 영웅 ID 리스트 반환"""
    return [h for h, data in HEROES.items() if data["role"] == role]

def get_hero_role(hero_id: str) -> str:
    """영웅 ID로 역할 반환"""
    return HEROES.get(hero_id, {}).get("role", None)

def get_random_heroes(count: int = 8) -> list:
    """
    퍼즐용 랜덤 영웅 선택
    
    count=8: 슬라이딩 퍼즐용 (3+3+2 또는 3+2+3 또는 2+3+3)
    count=9: 전체 채움용 (3+3+3)
    """
    import random
    
    if count == 9:
        # 역할당 3명씩
        tanks = random.sample(TANKS, 3)
        dps = random.sample(DPS, 3)
        supports = random.sample(SUPPORTS, 3)
        return tanks + dps + supports
    
    elif count == 8:
        # 한 역할만 2명, 나머지 3명씩
        # 어떤 역할을 2명으로 할지 랜덤 선택
        reduced_role = random.choice(['tank', 'dps', 'support'])
        
        if reduced_role == 'tank':
            tanks = random.sample(TANKS, 2)
            dps = random.sample(DPS, 3)
            supports = random.sample(SUPPORTS, 3)
        elif reduced_role == 'dps':
            tanks = random.sample(TANKS, 3)
            dps = random.sample(DPS, 2)
            supports = random.sample(SUPPORTS, 3)
        else:
            tanks = random.sample(TANKS, 3)
            dps = random.sample(DPS, 3)
            supports = random.sample(SUPPORTS, 2)
        
        return tanks + dps + supports
    
    else:
        # 일반적인 경우: 전체에서 랜덤 선택
        all_heroes = list(HEROES.keys())
        return random.sample(all_heroes, min(count, len(all_heroes)))
