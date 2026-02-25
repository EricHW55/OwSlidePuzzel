import { Hero, HeroesData, RolesData, Role, RoleInfo, SubRole } from '../types';

// 오버워치 영웅 데이터
export const HEROES: HeroesData = {
  // 탱커 14명
  dva: { name_ko: "디바", role: "tank", sub_role: "initiator" },
  doomfist: { name_ko: "둠피스트", role: "tank", sub_role: "initiator" },
  wrecking_ball: { name_ko: "레킹볼", role: "tank", sub_role: "initiator" },
  winston: { name_ko: "윈스턴", role: "tank", sub_role: "initiator" },
  mauga: { name_ko: "마우가", role: "tank", sub_role: "bruiser" },
  orisa: { name_ko: "오리사", role: "tank", sub_role: "bruiser" },
  zarya: { name_ko: "자리야", role: "tank", sub_role: "bruiser" },
  roadhog: { name_ko: "로드호그", role: "tank", sub_role: "bruiser" },
  junker_queen: { name_ko: "정커퀸", role: "tank", sub_role: "stalwart" },
  domina: { name_ko: "도미나", role: "tank", sub_role: "stalwart" },
  hazard: { name_ko: "해저드", role: "tank", sub_role: "stalwart" },
  ramattra: { name_ko: "라마트라", role: "tank", sub_role: "stalwart" },
  reinhardt: { name_ko: "라인하르트", role: "tank", sub_role: "stalwart" },
  sigma: { name_ko: "시그마", role: "tank", sub_role: "stalwart" },
  // 딜러 22명
  mei: { name_ko: "메이", role: "dps", sub_role: "specialist" },
  bastion: { name_ko: "바스티온", role: "dps", sub_role: "specialist" },
  soldier_76: { name_ko: "솔저: 76", role: "dps", sub_role: "specialist" },
  symmetra: { name_ko: "시메트라", role: "dps", sub_role: "specialist" },
  junkrat: { name_ko: "정크랫", role: "dps", sub_role: "specialist" },
  torbjorn: { name_ko: "토르비욘", role: "dps", sub_role: "specialist" },
  emre: { name_ko: "엠레", role: "dps", sub_role: "specialist" },
  sombra: { name_ko: "솜브라", role: "dps", sub_role: "recon" },
  echo: { name_ko: "에코", role: "dps", sub_role: "recon" },
  freja: { name_ko: "프레야", role: "dps", sub_role: "recon" },
  pharah: { name_ko: "파라", role: "dps", sub_role: "recon" },
  genji: { name_ko: "겐지", role: "dps", sub_role: "flanker" },
  reaper: { name_ko: "리퍼", role: "dps", sub_role: "flanker" },
  vendetta: { name_ko: "벤데타", role: "dps", sub_role: "flanker" },
  venture: { name_ko: "벤처", role: "dps", sub_role: "flanker" },
  tracer: { name_ko: "트레이서", role: "dps", sub_role: "flanker" },
  anran: { name_ko: "안란", role: "dps", sub_role: "flanker" },
  sojourn: { name_ko: "소전", role: "dps", sub_role: "sharpshooter" },
  ashe: { name_ko: "애쉬", role: "dps", sub_role: "sharpshooter" },
  widowmaker: { name_ko: "위도우메이커", role: "dps", sub_role: "sharpshooter" },
  cassidy: { name_ko: "캐서디", role: "dps", sub_role: "sharpshooter" },
  hanzo: { name_ko: "한조", role: "dps", sub_role: "sharpshooter" },
  // 서포터 14명
  lucio: { name_ko: "루시우", role: "support", sub_role: "tactician" },
  baptiste: { name_ko: "바티스트", role: "support", sub_role: "tactician" },
  ana: { name_ko: "아나", role: "support", sub_role: "tactician" },
  zenyatta: { name_ko: "젠야타", role: "support", sub_role: "tactician" },
  jetpack_cat: { name_ko: "제트팩 캣", role: "support", sub_role: "tactician" },
  lifeweaver: { name_ko: "라이프위버", role: "support", sub_role: "medic" },
  mercy: { name_ko: "메르시", role: "support", sub_role: "medic" },
  moira: { name_ko: "모이라", role: "support", sub_role: "medic" },
  kiriko: { name_ko: "키리코", role: "support", sub_role: "medic" },
  juno: { name_ko: "주노", role: "support", sub_role: "survivor" },
  brigitte: { name_ko: "브리기테", role: "support", sub_role: "survivor" },
  illari: { name_ko: "일리아리", role: "support", sub_role: "survivor" },
  wuyang: { name_ko: "우양", role: "support", sub_role: "survivor" },
  mizuki: { name_ko: "미즈키", role: "support", sub_role: "survivor" },
};

// 기본 역할 데이터
export const ROLES: RolesData = {
  tank: { name: '탱커', color: '#5A7E8A' },
  dps: { name: '딜러', color: '#9E4A4A' },
  support: { name: '서포터', color: '#5A8A5A' },
};

// 세부 역할 데이터
export const SUB_ROLES: RolesData = {
  // 탱커
  initiator: { name: '개시자', color: '#4A8A9E' },
  bruiser: { name: '투사', color: '#6E7A5A' },
  stalwart: { name: '강건한 자', color: '#5A7E8A' },
  // 딜러
  specialist: { name: '전문가', color: '#8A6A4A' },
  recon: { name: '수색가', color: '#7A5A8A' },
  flanker: { name: '측면 공격가', color: '#9E4A4A' },
  sharpshooter: { name: '명사수', color: '#8A4A6A' },
  // 힐러
  tactician: { name: '전술가', color: '#4A7A5A' },
  medic: { name: '의무관', color: '#5A8A5A' },
  survivor: { name: '생존왕', color: '#6A8A4A' },
};

// 모든 역할 데이터 (기본 + 세부) — 통합 조회용
export const ALL_ROLES: RolesData = { ...ROLES, ...SUB_ROLES };

// 세부역할 → 상위 기본역할 매핑
export const SUB_ROLE_PARENT: Record<SubRole, Role> = {
  initiator: 'tank',
  bruiser: 'tank',
  stalwart: 'tank',
  specialist: 'dps',
  recon: 'dps',
  flanker: 'dps',
  sharpshooter: 'dps',
  tactician: 'support',
  medic: 'support',
  survivor: 'support',
};

// 기본 역할인지 확인
export const isBasicRole = (role: string): role is Role => {
  return role === 'tank' || role === 'dps' || role === 'support';
};

// 역할별 영웅 ID 목록
export const HERO_IDS: Record<Role, string[]> = {
  tank: Object.keys(HEROES).filter(h => HEROES[h].role === 'tank'),
  dps: Object.keys(HEROES).filter(h => HEROES[h].role === 'dps'),
  support: Object.keys(HEROES).filter(h => HEROES[h].role === 'support'),
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

export const getHero = (heroId: string): Hero | undefined => {
  return HEROES[heroId];
};

export const getRole = (role: Role): RoleInfo => {
  return ROLES[role];
};

// 세부역할별 영웅 목록 (사전 모달용)
export const SUB_ROLE_GROUPS: { parent: Role; subRole: string; name: string; heroes: string[] }[] = [
  // 탱커
  { parent: 'tank', subRole: 'initiator', name: '개시자', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'initiator') },
  { parent: 'tank', subRole: 'bruiser', name: '투사', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'bruiser') },
  { parent: 'tank', subRole: 'stalwart', name: '강건한 자', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'stalwart') },
  // 딜러
  { parent: 'dps', subRole: 'specialist', name: '전문가', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'specialist') },
  { parent: 'dps', subRole: 'recon', name: '수색가', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'recon') },
  { parent: 'dps', subRole: 'flanker', name: '측면 공격가', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'flanker') },
  { parent: 'dps', subRole: 'sharpshooter', name: '명사수', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'sharpshooter') },
  // 힐러
  { parent: 'support', subRole: 'tactician', name: '전술가', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'tactician') },
  { parent: 'support', subRole: 'medic', name: '의무관', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'medic') },
  { parent: 'support', subRole: 'survivor', name: '생존왕', heroes: Object.keys(HEROES).filter(h => HEROES[h].sub_role === 'survivor') },
];
