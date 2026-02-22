"""
슬라이딩 퍼즐 생성 및 최적해 계산 모듈

전통적인 슬라이딩 퍼즐 방식:
- 8개 타일 + 1개 빈 칸
- 빈 칸과 인접한 타일만 이동 가능
- 목표: 각 칸의 역할(role)이 target_roles와 일치하도록 만들기
"""

import random
import uuid
from collections import deque
from typing import Tuple, List, Optional, Dict, Any

from heroes import HEROES, get_random_heroes


def make_target_roles(layout: str = "random") -> List[str]:
    """
    목표 역할 배열 생성
    
    3x3 index:
    0 1 2
    3 4 5
    6 7 8
    
    layout:
        - "random": 완전 랜덤 배치 (기본값)
        - "rows": 행 기준 (1행=tank, 2행=dps, 3행=support)
        - "cols": 열 기준 (1열=tank, 2열=dps, 3열=support)
        - "shuffle_rows": 행 순서만 랜덤 (예: 딜딜딜탱탱탱힐힐힐)
    """
    layout = (layout or "random").lower()

    if layout == "cols":
        target = [""] * 9
        for idx in (0, 3, 6):
            target[idx] = "tank"
        for idx in (1, 4, 7):
            target[idx] = "dps"
        for idx in (2, 5, 8):
            target[idx] = "support"
        return target

    if layout == "rows":
        return ["tank"] * 3 + ["dps"] * 3 + ["support"] * 3
    
    if layout == "shuffle_rows":
        rows = [["tank"] * 3, ["dps"] * 3, ["support"] * 3]
        random.shuffle(rows)
        return rows[0] + rows[1] + rows[2]

    # default = random
    target = ["tank"] * 3 + ["dps"] * 3 + ["support"] * 3
    random.shuffle(target)
    return target


def get_empty_index(state: Tuple[Optional[str], ...]) -> int:
    """빈 칸(None)의 인덱스 반환"""
    for i, val in enumerate(state):
        if val is None:
            return i
    return -1


def get_adjacent_indices(index: int) -> List[int]:
    """
    3x3 그리드에서 해당 인덱스와 인접한(상하좌우) 인덱스들 반환
    
    0 1 2
    3 4 5
    6 7 8
    """
    row, col = index // 3, index % 3
    adjacent = []
    
    if row > 0:
        adjacent.append(index - 3)
    if row < 2:
        adjacent.append(index + 3)
    if col > 0:
        adjacent.append(index - 1)
    if col < 2:
        adjacent.append(index + 1)
    
    return adjacent


# ──────────────────────────────────────────────
#  역할 기반 상태 함수 (BFS 최적화용)
# ──────────────────────────────────────────────

def _hero_state_to_role_state(
    state: Tuple[Optional[str], ...],
) -> Tuple[Optional[str], ...]:
    """
    영웅 ID 기반 상태 → 역할 기반 상태로 변환

    같은 역할의 영웅은 서로 교환 가능하므로,
    역할 기반 상태로 축소하면 탐색 공간이 대폭 줄어든다.

    예: ("reinhardt", "genji", None, ...) → ("tank", "dps", None, ...)
    """
    return tuple(
        HEROES[h]["role"] if h is not None else None
        for h in state
    )


def _role_state_is_solved(
    role_state: Tuple[Optional[str], ...],
    target_roles: List[str],
) -> bool:
    """역할 기반 상태가 정답인지 확인 (빈 칸 제외)"""
    for i, role in enumerate(role_state):
        if role is None:
            continue
        if role != target_roles[i]:
            return False
    return True


def _get_role_neighbors(
    role_state: Tuple[Optional[str], ...],
) -> List[Tuple[Optional[str], ...]]:
    """역할 기반 상태에서 빈 칸과 인접 타일을 스왑한 이웃 상태들 반환"""
    empty_idx = -1
    for i, val in enumerate(role_state):
        if val is None:
            empty_idx = i
            break

    if empty_idx == -1:
        return []

    neighbors = []
    for adj_idx in get_adjacent_indices(empty_idx):
        state_list = list(role_state)
        state_list[empty_idx], state_list[adj_idx] = state_list[adj_idx], state_list[empty_idx]
        neighbors.append(tuple(state_list))

    return neighbors


# ──────────────────────────────────────────────
#  영웅 ID 기반 함수 (프론트엔드 정답 판별용 유지)
# ──────────────────────────────────────────────

def is_solved(state: Tuple[Optional[str], ...], target_roles: List[str]) -> bool:
    """현재 상태가 정답인지 확인 (빈 칸 제외하고 역할 매칭)"""
    for i, hero in enumerate(state):
        if hero is None:
            continue
        if HEROES[hero]["role"] != target_roles[i]:
            return False
    return True


def get_neighbors(state: Tuple[Optional[str], ...]) -> List[Tuple[Tuple[Optional[str], ...], int]]:
    """
    빈 칸과 인접한 타일을 스왑하여 도달 가능한 상태들 반환
    
    Returns:
        List of (new_state, moved_tile_index)
    """
    neighbors = []
    empty_idx = get_empty_index(state)
    
    if empty_idx == -1:
        return neighbors
    
    adjacent = get_adjacent_indices(empty_idx)
    
    for adj_idx in adjacent:
        state_list = list(state)
        state_list[empty_idx], state_list[adj_idx] = state_list[adj_idx], state_list[empty_idx]
        neighbors.append((tuple(state_list), adj_idx))
    
    return neighbors


# ──────────────────────────────────────────────
#  최적해 계산 (역할 기반 BFS)
# ──────────────────────────────────────────────

def calculate_optimal_moves(
    initial_state: List[Optional[str]],
    target_roles: List[str],
    depth_limit: int = 50,
) -> Optional[int]:
    """
    역할 기반 BFS로 최적해(최소 이동 횟수) 계산

    [최적화 핵심]
    영웅 ID 대신 역할(role)로 상태를 추상화하여 탐색한다.
    - 영웅 ID 기반: 최대 9! / 2 = 181,440 상태
    - 역할 기반:   9! / (3!×3!×3!) × 빈칸위치 ≈ 5,040 상태

    같은 역할 영웅끼리는 교환해도 정답 여부가 바뀌지 않으므로
    역할 기반 탐색이 정확하면서도 훨씬 빠르다.

    또한 이 함수가 None을 반환하면 "풀 수 없는 배치"이므로,
    별도의 is_solvable 함수가 필요 없다.
    """
    role_state = _hero_state_to_role_state(tuple(initial_state))

    if _role_state_is_solved(role_state, target_roles):
        return 0

    queue = deque([(role_state, 0)])
    visited = {role_state}

    while queue:
        state, moves = queue.popleft()

        if moves >= depth_limit:
            continue

        for new_state in _get_role_neighbors(state):
            if new_state in visited:
                continue

            if _role_state_is_solved(new_state, target_roles):
                return moves + 1

            visited.add(new_state)
            queue.append((new_state, moves + 1))

    return None


# ──────────────────────────────────────────────
#  퍼즐 생성
# ──────────────────────────────────────────────

def generate_puzzle(
    *,
    min_optimal: int = 5,
    max_optimal: int = 20,
    layout: str = "rows",
    max_attempts: int = 500,
    depth_limit: int = 50,
) -> Dict[str, Any]:
    """
    슬라이딩 퍼즐 생성

    [생성 방식]
    1) 목표 역할 배열(target_roles)을 layout에 따라 생성
    2) 최대 max_attempts번 반복하며:
       a) 영웅 8명 랜덤 선택 + 빈 칸 → 9칸 셔플 배치
       b) 이미 정답이면 스킵
       c) 역할 기반 BFS로 최적해 계산 (풀 수 없으면 None → 스킵)
       d) 난이도 범위 [min_optimal, max_optimal]에 맞으면 반환
    3) 범위를 만족하지 못하면 가장 어려웠던 퍼즐을 fallback 반환

    [기존 is_solvable 제거 이유]
    역할 중복이 있는 퍼즐에서 단순 inversion count는 부정확하다.
    역할 기반 BFS의 상태 공간이 ~5,040개로 충분히 작으므로,
    BFS 결과(None 여부)로 풀 수 있는지를 직접 판별한다.
    
    Returns:
        {
            "puzzle_id": str,
            "initial_state": list[9] (1개는 None),
            "target_roles": list[9],
            "empty_index": int,
            "heroes": dict (8명),
            "optimal_moves": int
        }
    """
    target_roles = make_target_roles(layout)
    
    best_state = None
    best_optimal = -1
    best_heroes = None

    for _ in range(max_attempts):
        # 8명 랜덤 선택 (역할당 약 2~3명씩)
        selected_heroes = get_random_heroes(8)
        
        # 9칸에 8명 + 빈 칸 배치
        initial_state: List[Optional[str]] = selected_heroes.copy()
        initial_state.append(None)
        random.shuffle(initial_state)
        
        # 이미 정답이면 스킵
        if is_solved(tuple(initial_state), target_roles):
            continue

        # 역할 기반 BFS로 최적해 계산 (풀 수 없으면 None)
        optimal = calculate_optimal_moves(initial_state, target_roles, depth_limit=depth_limit)
        if optimal is None:
            continue

        heroes_info = {h: HEROES[h] for h in selected_heroes}

        # 최고 후보 저장
        if optimal > best_optimal:
            best_optimal = optimal
            best_state = initial_state.copy()
            best_heroes = heroes_info

        # 난이도 범위 체크
        if optimal < min_optimal:
            continue
        if max_optimal is not None and optimal > max_optimal:
            continue

        empty_idx = initial_state.index(None)

        return {
            "puzzle_id": str(uuid.uuid4()),
            "initial_state": initial_state,
            "target_roles": target_roles,
            "empty_index": empty_idx,
            "heroes": heroes_info,
            "optimal_moves": optimal,
        }

    # 조건 만족 못하면 최고 후보 반환
    if best_state is not None and best_optimal >= 0:
        empty_idx = best_state.index(None)
        return {
            "puzzle_id": str(uuid.uuid4()),
            "initial_state": best_state,
            "target_roles": target_roles,
            "empty_index": empty_idx,
            "heroes": best_heroes,
            "optimal_moves": best_optimal,
            "warning": f"Could not meet difficulty [{min_optimal}, {max_optimal}]. Returned {best_optimal}.",
        }

    raise RuntimeError("Failed to generate puzzle")


def calculate_move_difference(user_moves: int, optimal_moves: int) -> dict:
    """사용자 이동 횟수와 최적해의 차이 계산"""
    difference = user_moves - optimal_moves

    if difference == 0:
        grade = "PERFECT"
    elif difference <= 2:
        grade = "EXCELLENT"
    elif difference <= 5:
        grade = "GOOD"
    elif difference <= 10:
        grade = "NORMAL"
    else:
        grade = "KEEP TRYING"

    return {
        "user_moves": user_moves,
        "optimal_moves": optimal_moves,
        "difference": difference,
        "grade": grade
    }


if __name__ == "__main__":
    print("=== 슬라이딩 퍼즐 생성 테스트 ===\n")
    
    p = generate_puzzle(min_optimal=5, max_optimal=15, layout="rows")
    print(f"최적해: {p['optimal_moves']}수")
    print(f"빈 칸 위치: {p['empty_index']}")
    print(f"초기 배치: {p['initial_state']}")
    print(f"목표 역할: {p['target_roles']}")
    print(f"영웅 수: {len(p['heroes'])}명")
    if "warning" in p:
        print(f"⚠️ 경고: {p['warning']}")
