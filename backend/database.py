"""
SQLite 데이터베이스 모듈 - 랭킹 시스템
"""
import sqlite3
from datetime import datetime
from typing import List, Optional
from contextlib import contextmanager

DATABASE_PATH = "ranking.db"


@contextmanager
def get_db():
    """데이터베이스 연결 컨텍스트 매니저"""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """데이터베이스 초기화 - 테이블 생성"""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rankings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                time_ms INTEGER NOT NULL,
                moves INTEGER NOT NULL,
                optimal_moves INTEGER NOT NULL,
                puzzle_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 인덱스 생성 (시간순 정렬 최적화)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_time_ms ON rankings(time_ms ASC)
        """)
        
        conn.commit()


def add_ranking(
    nickname: str,
    time_ms: int,
    moves: int,
    optimal_moves: int,
    puzzle_id: str
) -> dict:
    """
    새 랭킹 기록 추가
    
    Returns:
        {"id": int, "rank": int}
    """
    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO rankings (nickname, time_ms, moves, optimal_moves, puzzle_id)
            VALUES (?, ?, ?, ?, ?)
        """, (nickname, time_ms, moves, optimal_moves, puzzle_id))
        
        record_id = cursor.lastrowid
        conn.commit()
        
        # 현재 순위 계산
        rank = conn.execute("""
            SELECT COUNT(*) + 1 as rank
            FROM rankings
            WHERE time_ms < ?
        """, (time_ms,)).fetchone()["rank"]
        
        return {"id": record_id, "rank": rank}


def get_top_rankings(limit: int = 10) -> List[dict]:
    """
    상위 랭킹 조회
    """
    with get_db() as conn:
        rows = conn.execute("""
            SELECT 
                id,
                nickname,
                time_ms,
                moves,
                optimal_moves,
                (moves - optimal_moves) AS move_difference,
                puzzle_id,
                created_at
            FROM rankings
            ORDER BY time_ms ASC
            LIMIT ?
        """, (limit,)).fetchall()
        
        return [
            {
                "rank": idx + 1,
                "id": row["id"],
                "nickname": row["nickname"],
                "time_ms": row["time_ms"],
                "time_display": format_time(row["time_ms"]),
                "moves": row["moves"],
                "optimal_moves": row["optimal_moves"],
                "move_diff": row["moves"] - row["optimal_moves"],
                "created_at": row["created_at"]
            }
            for idx, row in enumerate(rows)
        ]


def get_rank_for_time(time_ms: int) -> int:
    """
    특정 시간에 대한 예상 순위 반환
    (게임 종료 시 랭킹권인지 확인용)
    """
    with get_db() as conn:
        result = conn.execute("""
            SELECT COUNT(*) + 1 as rank
            FROM rankings
            WHERE time_ms < ?
        """, (time_ms,)).fetchone()
        
        return result["rank"]


def get_total_records() -> int:
    """전체 기록 수 반환"""
    with get_db() as conn:
        result = conn.execute("SELECT COUNT(*) as count FROM rankings").fetchone()
        return result["count"]


def is_rank_worthy(time_ms: int, top_n: int = 10) -> bool:
    """
    해당 시간이 상위 N위 안에 드는지 확인
    """
    total = get_total_records()
    
    # 기록이 N개 미만이면 무조건 랭킹권
    if total < top_n:
        return True
    
    rank = get_rank_for_time(time_ms)
    return rank <= top_n


def format_time(ms: int) -> str:
    """밀리초를 MM:SS.mmm 형식으로 변환"""
    total_seconds = ms // 1000
    milliseconds = ms % 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


# 초기화 실행
init_db()


# 테스트
if __name__ == "__main__":
    # 테스트 데이터 추가
    test_records = [
        ("김오버", 15230, 12, 8, "test-1"),
        ("박겐지", 23450, 18, 10, "test-2"),
        ("이트레", 12100, 9, 7, "test-3"),
    ]
    
    print("=== 테스트 기록 추가 ===")
    for nickname, time_ms, moves, optimal, puzzle_id in test_records:
        result = add_ranking(nickname, time_ms, moves, optimal, puzzle_id)
        print(f"{nickname}: {format_time(time_ms)} - 순위 {result['rank']}위")
    
    print("\n=== 상위 랭킹 ===")
    for record in get_top_rankings(10):
        diff_str = f"+{record['move_diff']}" if record['move_diff'] > 0 else str(record['move_diff'])
        print(f"{record['rank']}위: {record['nickname']} - {record['time_display']} ({record['moves']}수, 최적해 대비 {diff_str})")
