// 역할 타입
export type Role = 'tank' | 'dps' | 'support';

// 영웅 데이터 타입
export interface Hero {
    name_ko: string;
    role: Role;
}

// 영웅 딕셔너리 타입
export type HeroesData = Record<string, Hero>;

// 역할 정보 타입
export interface RoleInfo {
    name: string;
    color: string;
}

export type RolesData = Record<Role, RoleInfo>;

// 게임 상태 타입
export type GameState = 'idle' | 'playing' | 'completed';
export type GameMode = 'quick' | 'ranked';
export type Screen = 'menu' | 'game' | 'loading';

// 백엔드 퍼즐 응답 타입
export interface PuzzleResponse {
    puzzle_id: string;
    initial_state: (string | null)[];
    target_roles: Role[];
    empty_index: number;
    heroes: Record<string, Hero>;
}

// API 응답 타입
export interface SubmitResult {
    success: boolean;
    time_ms: number;
    time_display: string;
    moves: number;
    optimal_moves: number;
    move_difference: number;
    grade: string;
    is_rank_worthy: boolean;
    current_rank: number | null;
    needs_nickname: boolean;
}

export interface RankingRecord {
    id: number;
    rank: number;
    nickname: string;
    time_ms: number;
    time_display: string;
    moves: number;
    optimal_moves: number;
    move_diff: number;
    created_at: string;
}

export interface RankingResponse {
    total_records: number;
    rankings: RankingRecord[];
}

// 삼각형 타입 (배경용)
export interface Triangle {
    x: number;
    y: number;
    size: number;
    pointing: 'up' | 'down';
    baseAlpha: number;
    alpha: number;
    targetAlpha: number;
    twinkleSpeed: number;
    color: { r: number; g: number; b: number };
}
