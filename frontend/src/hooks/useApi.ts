import { SubmitResult, RankingResponse, PuzzleResponse, GameMode } from '../types';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface SubmitRankingResponse {
  success: boolean;
  rank: number;
  message: string;
}

export const api = {
  // 새 퍼즐 생성
  async createPuzzle(mode: GameMode): Promise<PuzzleResponse | null> {
    try {
      const response = await fetch(`${API_BASE}/api/puzzle/new?mode=${mode}`);
      if (!response.ok) return null;
      return await response.json();
    } catch (error) {
      console.error('퍼즐 생성 실패:', error);
      return null;
    }
  },

  // 결과 제출
  async submitResult(puzzleId: string, timeMs: number, moves: number): Promise<SubmitResult | null> {
    try {
      const response = await fetch(`${API_BASE}/api/puzzle/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          puzzle_id: puzzleId,
          time_ms: timeMs,
          moves: moves,
        }),
      });
      if (!response.ok) return null;
      return await response.json();
    } catch (error) {
      console.error('결과 제출 실패:', error);
      return null;
    }
  },

  // 랭킹 등록
  async submitRanking(
      puzzleId: string,
      timeMs: number,
      moves: number,
      nickname: string,
  ): Promise<SubmitRankingResponse | null> {
    try {
      const response = await fetch(`${API_BASE}/api/ranking/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          puzzle_id: puzzleId,
          time_ms: timeMs,
          moves: moves,
          nickname: nickname,
        }),
      });
      if (!response.ok) return null;
      return await response.json();
    } catch (error) {
      console.error('랭킹 등록 실패:', error);
      return null;
    }
  },

  // 랭킹 조회 (모드별)
  async getRankings(limit: number = 10, mode: string = 'ranked'): Promise<RankingResponse> {
    try {
      const response = await fetch(`${API_BASE}/api/ranking?limit=${limit}&mode=${mode}`);
      if (!response.ok) return { total_records: 0, rankings: [] };
      return await response.json();
    } catch (error) {
      console.error('랭킹 조회 실패:', error);
      return { total_records: 0, rankings: [] };
    }
  },
};

// 로컬 결과 생성 (오프라인용)
export const generateLocalResult = (moves: number, isRanked: boolean): SubmitResult => {
  const optimalMoves = Math.max(5, moves - Math.floor(Math.random() * 5));
  const diff = moves - optimalMoves;

  let grade: string;
  if (diff === 0) grade = 'PERFECT';
  else if (diff <= 2) grade = 'EXCELLENT';
  else if (diff <= 5) grade = 'GOOD';
  else if (diff <= 10) grade = 'NORMAL';
  else grade = 'KEEP TRYING';

  return {
    success: true,
    time_ms: 0,
    time_display: '',
    moves: moves,
    optimal_moves: optimalMoves,
    move_difference: diff,
    grade: grade,
    is_rank_worthy: isRanked,
    current_rank: isRanked ? 1 : null,
    needs_nickname: isRanked,
  };
};
