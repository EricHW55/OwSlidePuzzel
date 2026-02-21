"""
오버워치 슬라이딩 퍼즐 - FastAPI 백엔드

API 엔드포인트:
- GET  /api/puzzle/new       새 퍼즐 생성
- POST /api/puzzle/submit    결과 제출
- GET  /api/ranking          상위 랭킹 조회
- GET  /api/heroes           전체 영웅 목록
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from puzzle import generate_puzzle, calculate_move_difference
from database import (
    add_ranking, 
    get_top_rankings, 
    is_rank_worthy, 
    get_rank_for_time,
    get_total_records
)
from heroes import HEROES

app = FastAPI(
    title="오버워치 슬라이딩 퍼즐",
    description="역할군 맞추기 미니게임 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드 연동용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용. 배포 시 특정 도메인으로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 진행 중인 퍼즐 저장 (메모리)
# 실제 서비스에서는 Redis 등 사용 권장
active_puzzles = {}


# === Request/Response 모델 ===

class SubmitRequest(BaseModel):
    puzzle_id: str
    time_ms: int
    moves: int
    nickname: Optional[str] = None


class SubmitResponse(BaseModel):
    success: bool
    time_ms: int
    time_display: str
    moves: int
    optimal_moves: int
    move_difference: int
    grade: str
    is_rank_worthy: bool
    current_rank: Optional[int] = None
    needs_nickname: bool


class RankingSubmitRequest(BaseModel):
    puzzle_id: str
    time_ms: int
    moves: int
    nickname: str


# === API 엔드포인트 ===

@app.get("/")
def root():
    return {
        "message": "오버워치 슬라이딩 퍼즐 API",
        "endpoints": {
            "새 퍼즐": "GET /api/puzzle/new",
            "결과 제출": "POST /api/puzzle/submit",
            "랭킹 등록": "POST /api/ranking/submit",
            "랭킹 조회": "GET /api/ranking",
            "영웅 목록": "GET /api/heroes"
        }
    }


@app.get("/api/puzzle/new")
def create_puzzle(mode: str = Query("quick", description="quick 또는 ranked")):
    """
    새 퍼즐 생성
    
    Query params:
        - mode: "quick" (일반전, 쉬움) 또는 "ranked" (랭킹전, 어려움)
    
    Returns:
        - puzzle_id: 퍼즐 고유 ID
        - initial_state: 초기 영웅 배치 (9칸, 1개는 null)
        - target_roles: 목표 역할 배치 (9칸)
        - empty_index: 빈 칸 위치
        - heroes: 사용된 영웅 정보 (8명)
    """
    if mode == "ranked":
        # 랭킹전: 어려움 (15~25수)
        puzzle = generate_puzzle(min_optimal=20, max_optimal=25, layout="random")
    else:
        # 일반전: 쉬움 (5~15수)
        puzzle = generate_puzzle(min_optimal=5, max_optimal=18, layout="random")
    
    # 퍼즐 정보 저장 (검증용)
    active_puzzles[puzzle["puzzle_id"]] = {
        "optimal_moves": puzzle["optimal_moves"],
        "initial_state": puzzle["initial_state"],
        "target_roles": puzzle["target_roles"],
        "empty_index": puzzle["empty_index"]
    }
    
    return {
        "puzzle_id": puzzle["puzzle_id"],
        "initial_state": puzzle["initial_state"],
        "target_roles": puzzle["target_roles"],
        "empty_index": puzzle["empty_index"],
        "heroes": puzzle["heroes"]
    }


@app.post("/api/puzzle/submit", response_model=SubmitResponse)
def submit_result(request: SubmitRequest):
    """
    퍼즐 결과 제출 (닉네임 없이)
    
    랭킹권이면 needs_nickname=True 반환
    """
    # 퍼즐 검증
    if request.puzzle_id not in active_puzzles:
        raise HTTPException(status_code=404, detail="퍼즐을 찾을 수 없습니다")
    
    puzzle_info = active_puzzles[request.puzzle_id]
    optimal_moves = puzzle_info["optimal_moves"]
    
    # 이동 횟수 차이 계산
    diff_info = calculate_move_difference(request.moves, optimal_moves)
    
    # 랭킹권 확인
    rank_worthy = is_rank_worthy(request.time_ms, top_n=10)
    current_rank = get_rank_for_time(request.time_ms) if rank_worthy else None
    
    # 시간 포맷
    total_seconds = request.time_ms // 1000
    milliseconds = request.time_ms % 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    time_display = f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    return SubmitResponse(
        success=True,
        time_ms=request.time_ms,
        time_display=time_display,
        moves=request.moves,
        optimal_moves=optimal_moves,
        move_difference=diff_info["difference"],
        grade=diff_info["grade"],
        is_rank_worthy=rank_worthy,
        current_rank=current_rank,
        needs_nickname=rank_worthy
    )


@app.post("/api/ranking/submit")
def submit_ranking(request: RankingSubmitRequest):
    """
    랭킹 등록 (닉네임 포함)
    """
    if request.puzzle_id not in active_puzzles:
        raise HTTPException(status_code=404, detail="퍼즐을 찾을 수 없습니다")
    
    puzzle_info = active_puzzles[request.puzzle_id]
    optimal_moves = puzzle_info["optimal_moves"]
    
    # 닉네임 검증
    if not request.nickname or len(request.nickname.strip()) == 0:
        raise HTTPException(status_code=400, detail="닉네임을 입력해주세요")
    
    if len(request.nickname) > 20:
        raise HTTPException(status_code=400, detail="닉네임은 20자 이하로 입력해주세요")
    
    # 랭킹 등록
    result = add_ranking(
        nickname=request.nickname.strip(),
        time_ms=request.time_ms,
        moves=request.moves,
        optimal_moves=optimal_moves,
        puzzle_id=request.puzzle_id
    )
    
    # 퍼즐 정보 삭제 (재사용 방지)
    del active_puzzles[request.puzzle_id]
    
    return {
        "success": True,
        "rank": result["rank"],
        "message": f"{request.nickname}님, {result['rank']}위로 등록되었습니다!"
    }


@app.get("/api/ranking")
def get_ranking(limit: int = 10):
    """
    상위 랭킹 조회
    
    Query params:
        - limit: 조회할 순위 수 (기본 10)
    """
    if limit < 1 or limit > 100:
        limit = 10
    
    rankings = get_top_rankings(limit)
    total = get_total_records()
    
    return {
        "total_records": total,
        "rankings": rankings
    }


@app.get("/api/heroes")
def get_heroes():
    """
    전체 영웅 목록 반환
    """
    return {
        "total": len(HEROES),
        "heroes": HEROES,
        "by_role": {
            "tank": [h for h, d in HEROES.items() if d["role"] == "tank"],
            "dps": [h for h, d in HEROES.items() if d["role"] == "dps"],
            "support": [h for h, d in HEROES.items() if d["role"] == "support"]
        }
    }


# === 서버 실행 ===
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
