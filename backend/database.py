"""
SQLite 데이터베이스 모듈 - 랭킹 시스템

테이블:
- rankings: 기본 모드(경쟁전) 랭킹
- rankings_hard: 하드 모드 랭킹
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
        # 기본 모드 랭킹
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
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_time_ms ON rankings(time_ms ASC)
        """)

        # 하드 모드 랭킹
        conn.execute("""
            CREATE TABLE IF NOT EXISTS rankings_hard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nickname TEXT NOT NULL,
                time_ms INTEGER NOT NULL,
                moves INTEGER NOT NULL,
                optimal_moves INTEGER NOT NULL,
                puzzle_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_hard_time_ms ON rankings_hard(time_ms ASC)
        """)

        conn.commit()


def _get_table(mode: str) -> str:
    """모드에 따른 테이블명 반환"""
    return "rankings_hard" if mode == "hard" else "rankings"


def add_ranking(
    nickname: str,
    time_ms: int,
    moves: int,
    optimal_moves: int,
    puzzle_id: str,
    mode: str = "ranked",
) -> dict:
    """
    새 랭킹 기록 추가

    Returns:
        {"id": int, "rank": int}
    """
    table = _get_table(mode)

    with get_db() as conn:
        cursor = conn.execute(f"""
            INSERT INTO {table} (nickname, time_ms, moves, optimal_moves, puzzle_id)
            VALUES (?, ?, ?, ?, ?)
        """, (nickname, time_ms, moves, optimal_moves, puzzle_id))

        record_id = cursor.lastrowid
        conn.commit()

        rank = conn.execute(f"""
            SELECT COUNT(*) + 1 as rank
            FROM {table}
            WHERE time_ms < ?
        """, (time_ms,)).fetchone()["rank"]

        return {"id": record_id, "rank": rank}


def get_top_rankings(limit: int = 10, mode: str = "ranked") -> List[dict]:
    """상위 랭킹 조회"""
    table = _get_table(mode)

    with get_db() as conn:
        rows = conn.execute(f"""
            SELECT 
                id,
                nickname,
                time_ms,
                moves,
                optimal_moves,
                puzzle_id,
                created_at
            FROM {table}
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
                "created_at": row["created_at"],
            }
            for idx, row in enumerate(rows)
        ]


def get_rank_for_time(time_ms: int, mode: str = "ranked") -> int:
    """특정 시간에 대한 예상 순위 반환"""
    table = _get_table(mode)

    with get_db() as conn:
        result = conn.execute(f"""
            SELECT COUNT(*) + 1 as rank
            FROM {table}
            WHERE time_ms < ?
        """, (time_ms,)).fetchone()

        return result["rank"]


def get_total_records(mode: str = "ranked") -> int:
    """전체 기록 수 반환"""
    table = _get_table(mode)

    with get_db() as conn:
        result = conn.execute(f"SELECT COUNT(*) as count FROM {table}").fetchone()
        return result["count"]


def is_rank_worthy(time_ms: int, top_n: int = 10, mode: str = "ranked") -> bool:
    """해당 시간이 상위 N위 안에 드는지 확인"""
    total = get_total_records(mode)

    if total < top_n:
        return True

    rank = get_rank_for_time(time_ms, mode)
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


if __name__ == "__main__":
    print("=== 기본 모드 테스트 ===")
    test_records = [
        ("김오버", 15230, 12, 8, "test-1"),
        ("박겐지", 23450, 18, 10, "test-2"),
        ("이트레", 12100, 9, 7, "test-3"),
    ]
    for nickname, time_ms, moves, optimal, puzzle_id in test_records:
        result = add_ranking(nickname, time_ms, moves, optimal, puzzle_id, mode="ranked")
        print(f"{nickname}: {format_time(time_ms)} - {result['rank']}위")

    print("\n=== 하드 모드 테스트 ===")
    hard_records = [
        ("하드유저1", 30000, 20, 12, "hard-1"),
        ("하드유저2", 25000, 15, 10, "hard-2"),
    ]
    for nickname, time_ms, moves, optimal, puzzle_id in hard_records:
        result = add_ranking(nickname, time_ms, moves, optimal, puzzle_id, mode="hard")
        print(f"{nickname}: {format_time(time_ms)} - {result['rank']}위")

    print("\n=== 기본 랭킹 ===")
    for r in get_top_rankings(10, mode="ranked"):
        print(f"{r['rank']}위: {r['nickname']} - {r['time_display']}")

    print("\n=== 하드 랭킹 ===")
    for r in get_top_rankings(10, mode="hard"):
        print(f"{r['rank']}위: {r['nickname']} - {r['time_display']}")
