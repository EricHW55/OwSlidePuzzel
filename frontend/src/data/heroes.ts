import { Hero, HeroesData, RolesData, Role, RoleInfo } from '../types';

// 오버워치 영웅 데이터
export const HEROES: HeroesData = {
  // 탱커 14명
  dva: { name_ko: "디바", role: "tank" },
  doomfist: { name_ko: "둠피스트", role: "tank" },
  junker_queen: { name_ko: "정커퀸", role: "tank" },
  mauga: { name_ko: "마우가", role: "tank" },
  orisa: { name_ko: "오리사", role: "tank" },
  ramattra: { name_ko: "라마트라", role: "tank" },
  reinhardt: { name_ko: "라인하르트", role: "tank" },
  roadhog: { name_ko: "로드호그", role: "tank" },
  sigma: { name_ko: "시그마", role: "tank" },
  winston: { name_ko: "윈스턴", role: "tank" },
  wrecking_ball: { name_ko: "레킹볼", role: "tank" },
  zarya: { name_ko: "자리야", role: "tank" },
  hazard: { name_ko: "해저드", role: "tank" },
  domina: { name_ko: "도미나", role: "tank" },
  // 딜러 22명
  ashe: { name_ko: "애쉬", role: "dps" },
  bastion: { name_ko: "바스티온", role: "dps" },
  cassidy: { name_ko: "캐서디", role: "dps" },
  echo: { name_ko: "에코", role: "dps" },
  genji: { name_ko: "겐지", role: "dps" },
  hanzo: { name_ko: "한조", role: "dps" },
  junkrat: { name_ko: "정크랫", role: "dps" },
  mei: { name_ko: "메이", role: "dps" },
  pharah: { name_ko: "파라", role: "dps" },
  reaper: { name_ko: "리퍼", role: "dps" },
  sojourn: { name_ko: "소전", role: "dps" },
  soldier_76: { name_ko: "솔저: 76", role: "dps" },
  sombra: { name_ko: "솜브라", role: "dps" },
  symmetra: { name_ko: "시메트라", role: "dps" },
  torbjorn: { name_ko: "토르비욘", role: "dps" },
  tracer: { name_ko: "트레이서", role: "dps" },
  venture: { name_ko: "벤처", role: "dps" },
  widowmaker: { name_ko: "위도우메이커", role: "dps" },
  freja: { name_ko: "프레야", role: "dps" },
  vendetta: { name_ko: "벤데타", role: "dps" },
  anran: { name_ko: "안란", role: "dps" },
  emre: { name_ko: "엠레", role: "dps" },
  // 서포터 14명
  ana: { name_ko: "아나", role: "support" },
  baptiste: { name_ko: "바티스트", role: "support" },
  brigitte: { name_ko: "브리기테", role: "support" },
  illari: { name_ko: "일리아리", role: "support" },
  juno: { name_ko: "주노", role: "support" },
  kiriko: { name_ko: "키리코", role: "support" },
  lifeweaver: { name_ko: "라이프위버", role: "support" },
  lucio: { name_ko: "루시우", role: "support" },
  mercy: { name_ko: "메르시", role: "support" },
  moira: { name_ko: "모이라", role: "support" },
  zenyatta: { name_ko: "젠야타", role: "support" },
  wuyang: { name_ko: "우양", role: "support" },
  mizuki: { name_ko: "미즈키", role: "support" },
  jetpack_cat: { name_ko: "제트팩 캣", role: "support" },
};

export const ROLES: RolesData = {
  tank: { name: '탱커', color: '#5A7E8A' },
  dps: { name: '딜러', color: '#9E4A4A' },
  support: { name: '서포터', color: '#5A8A5A' }
};

// 역할별 영웅 ID 목록
export const HERO_IDS: Record<Role, string[]> = {
  tank: Object.keys(HEROES).filter(h => HEROES[h].role === 'tank'),
  dps: Object.keys(HEROES).filter(h => HEROES[h].role === 'dps'),
  support: Object.keys(HEROES).filter(h => HEROES[h].role === 'support')
};

// 유틸리티 함수
export const shuffle = <T>(arr: T[]): T[] => {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
};

// 영웅 정보 가져오기
export const getHero = (heroId: string): Hero | undefined => {
  return HEROES[heroId];
};

// 역할 정보 가져오기
export const getRole = (role: Role): RoleInfo => {
  return ROLES[role];
};
