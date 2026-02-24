# 오버워치2 영웅 데이터 (2025년 기준)
# 역할: tank(돌격), dps(공격), support(지원)
# 세부역할: initiator(개시자), bruiser(투사), stalwart(강건한자),
#           specialist(전문가), recon(수색가), flanker(측면공격가), sharpshooter(명사수),
#           tactician(전술가), medic(의무관), survivor(생존왕)

HEROES = {
    # ═══ 돌격 (Tank) - 14명 ═══

    # 개시자 (Initiator) - 4명
    "dva": {"name": "D.Va", "name_ko": "디바", "role": "tank", "sub_role": "initiator"},
    "doomfist": {"name": "Doomfist", "name_ko": "둠피스트", "role": "tank", "sub_role": "initiator"},
    "wrecking_ball": {"name": "Wrecking Ball", "name_ko": "레킹볼", "role": "tank", "sub_role": "initiator"},
    "winston": {"name": "Winston", "name_ko": "윈스턴", "role": "tank", "sub_role": "initiator"},

    # 투사 (Bruiser) - 4명
    "junker_queen": {"name": "Junker Queen", "name_ko": "정커퀸", "role": "tank", "sub_role": "stalwart"},
    "mauga": {"name": "Mauga", "name_ko": "마우가", "role": "tank", "sub_role": "bruiser"},
    "orisa": {"name": "Orisa", "name_ko": "오리사", "role": "tank", "sub_role": "bruiser"},
    "zarya": {"name": "Zarya", "name_ko": "자리야", "role": "tank", "sub_role": "bruiser"},

    # 강건한 자 (Stalwart) - 6명
    "domina": {"name": "Domina", "name_ko": "도미나", "role": "tank", "sub_role": "stalwart"},
    "hazard": {"name": "Hazard", "name_ko": "해저드", "role": "tank", "sub_role": "stalwart"},
    "ramattra": {"name": "Ramattra", "name_ko": "라마트라", "role": "tank", "sub_role": "stalwart"},
    "reinhardt": {"name": "Reinhardt", "name_ko": "라인하르트", "role": "tank", "sub_role": "stalwart"},
    "sigma": {"name": "Sigma", "name_ko": "시그마", "role": "tank", "sub_role": "stalwart"},
    "roadhog": {"name": "Roadhog", "name_ko": "로드호그", "role": "tank", "sub_role": "bruiser"},


    # ═══ 공격 (DPS) - 22명 ═══

    # 전문가 (Specialist) - 7명
    "mei": {"name": "Mei", "name_ko": "메이", "role": "dps", "sub_role": "specialist"},
    "bastion": {"name": "Bastion", "name_ko": "바스티온", "role": "dps", "sub_role": "specialist"},
    "soldier_76": {"name": "Soldier: 76", "name_ko": "솔저: 76", "role": "dps", "sub_role": "specialist"},
    "symmetra": {"name": "Symmetra", "name_ko": "시메트라", "role": "dps", "sub_role": "specialist"},
    "junkrat": {"name": "Junkrat", "name_ko": "정크랫", "role": "dps", "sub_role": "specialist"},
    "torbjorn": {"name": "Torbjörn", "name_ko": "토르비욘", "role": "dps", "sub_role": "specialist"},
    "emre": {"name": "Emre", "name_ko": "엠레", "role": "dps", "sub_role": "specialist"},

    # 수색가 (Recon) - 4명
    "sombra": {"name": "Sombra", "name_ko": "솜브라", "role": "dps", "sub_role": "recon"},
    "echo": {"name": "Echo", "name_ko": "에코", "role": "dps", "sub_role": "recon"},
    "freja": {"name": "Freja", "name_ko": "프레야", "role": "dps", "sub_role": "recon"},
    "anran": {"name": "Anran", "name_ko": "안란", "role": "dps", "sub_role": "flanker"},

    # 측면 공격가 (Flanker) - 6명
    "genji": {"name": "Genji", "name_ko": "겐지", "role": "dps", "sub_role": "flanker"},
    "reaper": {"name": "Reaper", "name_ko": "리퍼", "role": "dps", "sub_role": "flanker"},
    "vendetta": {"name": "Vendetta", "name_ko": "벤데타", "role": "dps", "sub_role": "flanker"},
    "pharah": {"name": "Pharah", "name_ko": "파라", "role": "dps", "sub_role": "recon"},
    "venture": {"name": "Venture", "name_ko": "벤처", "role": "dps", "sub_role": "flanker"},
    "tracer": {"name": "Tracer", "name_ko": "트레이서", "role": "dps", "sub_role": "flanker"},

    # 명사수 (Sharpshooter) - 5명
    "sojourn": {"name": "Sojourn", "name_ko": "소전", "role": "dps", "sub_role": "sharpshooter"},
    "ashe": {"name": "Ashe", "name_ko": "애쉬", "role": "dps", "sub_role": "sharpshooter"},
    "widowmaker": {"name": "Widowmaker", "name_ko": "위도우메이커", "role": "dps", "sub_role": "sharpshooter"},
    "cassidy": {"name": "Cassidy", "name_ko": "캐서디", "role": "dps", "sub_role": "sharpshooter"},
    "hanzo": {"name": "Hanzo", "name_ko": "한조", "role": "dps", "sub_role": "sharpshooter"},


    # ═══ 지원 (Support) - 14명 ═══

    # 전술가 (Tactician) - 5명
    "lucio": {"name": "Lúcio", "name_ko": "루시우", "role": "support", "sub_role": "tactician"},
    "baptiste": {"name": "Baptiste", "name_ko": "바티스트", "role": "support", "sub_role": "tactician"},
    "ana": {"name": "Ana", "name_ko": "아나", "role": "support", "sub_role": "tactician"},
    "zenyatta": {"name": "Zenyatta", "name_ko": "젠야타", "role": "support", "sub_role": "tactician"},
    "jetpack_cat": {"name": "Jetpack_cat", "name_ko": "제트팩 캣", "role": "support", "sub_role": "tactician"},

    # 의무관 (Medic) - 4명
    "lifeweaver": {"name": "Lifeweaver", "name_ko": "라이프위버", "role": "support", "sub_role": "medic"},
    "mercy": {"name": "Mercy", "name_ko": "메르시", "role": "support", "sub_role": "medic"},
    "moira": {"name": "Moira", "name_ko": "모이라", "role": "support", "sub_role": "medic"},
    "kiriko": {"name": "Kiriko", "name_ko": "키리코", "role": "support", "sub_role": "medic"},

    # 생존왕 (Survivor) - 5명
    "juno": {"name": "Juno", "name_ko": "주노", "role": "support", "sub_role": "survivor"},
    "brigitte": {"name": "Brigitte", "name_ko": "브리기테", "role": "support", "sub_role": "survivor"},
    "illari": {"name": "Illari", "name_ko": "일리아리", "role": "support", "sub_role": "survivor"},
    "wuyang": {"name": "Wuyang", "name_ko": "우양", "role": "support", "sub_role": "survivor"},
    "mizuki": {"name": "Mizuki", "name_ko": "미즈키", "role": "support", "sub_role": "survivor"},
}


# ═══ 세부역할 메타데이터 ═══

SUB_ROLES = {
    # 탱커 세부역할
    "initiator":   {"name": "개시자",     "name_en": "Initiator",    "parent_role": "tank"},
    "bruiser":     {"name": "투사",       "name_en": "Bruiser",      "parent_role": "tank"},
    "stalwart":    {"name": "강건한 자",   "name_en": "Stalwart",     "parent_role": "tank"},
    # 딜러 세부역할
    "specialist":  {"name": "전문가",     "name_en": "Specialist",   "parent_role": "dps"},
    "recon":       {"name": "수색가",     "name_en": "Recon",        "parent_role": "dps"},
    "flanker":     {"name": "측면 공격가", "name_en": "Flanker",      "parent_role": "dps"},
    "sharpshooter":{"name": "명사수",     "name_en": "Sharpshooter", "parent_role": "dps"},
    # 힐러 세부역할
    "tactician":   {"name": "전술가",     "name_en": "Tactician",    "parent_role": "support"},
    "medic":       {"name": "의무관",     "name_en": "Medic",        "parent_role": "support"},
    "survivor":    {"name": "생존왕",     "name_en": "Survivor",     "parent_role": "support"},
}


# ═══ 역할별 영웅 ID 리스트 ═══

TANKS = [h for h, data in HEROES.items() if data["role"] == "tank"]
DPS = [h for h, data in HEROES.items() if data["role"] == "dps"]
SUPPORTS = [h for h, data in HEROES.items() if data["role"] == "support"]


def get_heroes_by_role(role: str) -> list:
    """역할별 영웅 ID 리스트 반환"""
    return [h for h, data in HEROES.items() if data["role"] == role]


def get_heroes_by_sub_role(sub_role: str) -> list:
    """세부역할별 영웅 ID 리스트 반환"""
    return [h for h, data in HEROES.items() if data["sub_role"] == sub_role]


def get_hero_role(hero_id: str) -> str:
    """영웅 ID로 역할 반환"""
    return HEROES.get(hero_id, {}).get("role", None)


def get_hero_sub_role(hero_id: str) -> str:
    """영웅 ID로 세부역할 반환"""
    return HEROES.get(hero_id, {}).get("sub_role", None)


def get_random_heroes(count: int = 8) -> list:
    """
    퍼즐용 랜덤 영웅 선택
    
    count=8: 슬라이딩 퍼즐용 (3+3+2 또는 3+2+3 또는 2+3+3)
    count=9: 전체 채움용 (3+3+3)
    """
    import random
    
    if count == 9:
        tanks = random.sample(TANKS, 3)
        dps = random.sample(DPS, 3)
        supports = random.sample(SUPPORTS, 3)
        return tanks + dps + supports
    
    elif count == 8:
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
        all_heroes = list(HEROES.keys())
        return random.sample(all_heroes, min(count, len(all_heroes)))


def get_random_heroes_for_hard() -> dict:
    """
    하드모드용 영웅 선택
    
    1) 세부역할 9개 선택 (탱커3 + 딜러4중3 + 힐러3)
    2) 각 세부역할에서 영웅 1명씩 = 9명
    3) 9명 중 1명 블라인드(제거) → 8명 + 빈칸
    
    Returns:
        {
            "heroes": list[8],           # 퍼즐에 쓸 영웅 8명
            "target_sub_roles": list[9],  # 목표 배치 (세부역할 9개)
            "blinded_hero": str,          # 제거된 영웅
            "blinded_sub_role": str,      # 제거된 영웅의 세부역할
        }
    """
    import random
    
    # 1) 세부역할 9개 선택
    tank_subs = ["initiator", "bruiser", "stalwart"]  # 3개 전부
    dps_subs = random.sample(["specialist", "recon", "flanker", "sharpshooter"], 3)  # 4개 중 3개
    support_subs = ["tactician", "medic", "survivor"]  # 3개 전부
    
    selected_sub_roles = tank_subs + dps_subs + support_subs  # 9개
    random.shuffle(selected_sub_roles)
    
    # 2) 각 세부역할에서 영웅 1명씩 = 9명
    heroes_9 = []
    for sr in selected_sub_roles:
        candidates = get_heroes_by_sub_role(sr)
        heroes_9.append(random.choice(candidates))
    
    # 3) 9명 중 1명 블라인드 → 8명
    blind_idx = random.randint(0, 8)
    blinded_hero = heroes_9[blind_idx]
    blinded_sub_role = selected_sub_roles[blind_idx]
    
    heroes_8 = [h for i, h in enumerate(heroes_9) if i != blind_idx]
    
    return {
        "heroes": heroes_8,
        "target_sub_roles": selected_sub_roles,
        "blinded_hero": blinded_hero,
        "blinded_sub_role": blinded_sub_role,
    }