"""
슬라이딩 퍼즐 생성 및 최적해 계산 모듈

모드:
- quick/ranked: 기본 역할(tank, dps, support) 기준
- hard: 세부 역할(initiator, bruiser, ...) + 기본역할 1칸 혼합
"""

import random
import uuid
from collections import deque
from typing import Tuple, List, Optional, Dict, Any

from heroes import HEROES, get_random_heroes, get_random_heroes_for_hard


# ══════════════════════════════════════════════
#  공용 유틸
# ══════════════════════════════════════════════

BASIC_ROLES = {"tank", "dps", "support"}


def make_target_roles(layout: str = "random") -> List[str]:
    """목표 역할 배열 생성 (기본 모드용)"""
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
    """3x3 그리드에서 해당 인덱스와 인접한(상하좌우) 인덱스들 반환"""
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


def _get_abstract_neighbors(
    state: Tuple[Optional[str], ...],
) -> List[Tuple[Optional[str], ...]]:
    """추상 상태에서 빈 칸과 인접 타일을 스왑 (기본/하드 공용)"""
    empty_idx = -1
    for i, val in enumerate(state):
        if val is None:
            empty_idx = i
            break
    if empty_idx == -1:
        return []

    neighbors = []
    for adj_idx in get_adjacent_indices(empty_idx):
        state_list = list(state)
        state_list[empty_idx], state_list[adj_idx] = state_list[adj_idx], state_list[empty_idx]
        neighbors.append(tuple(state_list))
    return neighbors


def _abstract_state_is_solved(
    abstract_state: Tuple[Optional[str], ...],
    target_roles: List[str],
) -> bool:
    """추상 상태 정답 판별 (기본/하드 공용)"""
    for i, val in enumerate(abstract_state):
        if val is None:
            continue
        if val != target_roles[i]:
            return False
    return True


# ══════════════════════════════════════════════
#  기본 모드: 역할(role) 기반
# ══════════════════════════════════════════════

def _hero_state_to_role_state(
    state: Tuple[Optional[str], ...],
) -> Tuple[Optional[str], ...]:
    """영웅 ID → 역할 기반 상태"""
    return tuple(
        HEROES[h]["role"] if h is not None else None
        for h in state
    )


def is_solved(state: Tuple[Optional[str], ...], target_roles: List[str]) -> bool:
    """정답 판별 (기본 모드: role 매칭)"""
    for i, hero in enumerate(state):
        if hero is None:
            continue
        if HEROES[hero]["role"] != target_roles[i]:
            return False
    return True


def get_neighbors(state: Tuple[Optional[str], ...]) -> List[Tuple[Tuple[Optional[str], ...], int]]:
    """빈 칸과 인접한 타일을 스왑"""
    neighbors = []
    empty_idx = get_empty_index(state)
    if empty_idx == -1:
        return neighbors
    for adj_idx in get_adjacent_indices(empty_idx):
        state_list = list(state)
        state_list[empty_idx], state_list[adj_idx] = state_list[adj_idx], state_list[empty_idx]
        neighbors.append((tuple(state_list), adj_idx))
    return neighbors


def calculate_optimal_moves(
    initial_state: List[Optional[str]],
    target_roles: List[str],
    depth_limit: int = 50,
) -> Optional[int]:
    """역할 기반 BFS 최적해 (기본 모드)"""
    role_state = _hero_state_to_role_state(tuple(initial_state))

    if _abstract_state_is_solved(role_state, target_roles):
        return 0

    queue = deque([(role_state, 0)])
    visited = {role_state}

    while queue:
        state, moves = queue.popleft()
        if moves >= depth_limit:
            continue
        for new_state in _get_abstract_neighbors(state):
            if new_state in visited:
                continue
            if _abstract_state_is_solved(new_state, target_roles):
                return moves + 1
            visited.add(new_state)
            queue.append((new_state, moves + 1))

    return None


# ══════════════════════════════════════════════
#  하드 모드: 세부역할(sub_role) + 기본역할 혼합
# ══════════════════════════════════════════════

def _hero_state_to_mixed_state(
    state: Tuple[Optional[str], ...],
    target_roles: List[str],
) -> Tuple[Optional[str], ...]:
    """
    영웅 ID → 혼합 상태 변환 (하드 모드 BFS용)

    target_roles 각 칸이 기본역할인지 세부역할인지에 따라:
    - 기본역할 칸(tank/dps/support): 영웅의 role로 변환
    - 세부역할 칸(initiator 등): 영웅의 sub_role로 변환
    """
    result = []
    for i, hero in enumerate(state):
        if hero is None:
            result.append(None)
        elif target_roles[i] in BASIC_ROLES:
            result.append(HEROES[hero]["role"])
        else:
            result.append(HEROES[hero]["sub_role"])
    return tuple(result)


def is_solved_hard(state: Tuple[Optional[str], ...], target_roles: List[str]) -> bool:
    """
    정답 판별 (하드 모드)

    - 세부역할 칸: 영웅의 sub_role == target
    - 기본역할 칸: 영웅의 role == target
    """
    for i, hero in enumerate(state):
        if hero is None:
            continue
        target = target_roles[i]
        if target in BASIC_ROLES:
            if HEROES[hero]["role"] != target:
                return False
        else:
            if HEROES[hero]["sub_role"] != target:
                return False
    return True


def calculate_optimal_moves_hard(
    initial_state: List[Optional[str]],
    target_roles: List[str],
    depth_limit: int = 50,
) -> Optional[int]:
    """세부역할 기반 BFS 최적해 (하드 모드)"""
    abstract_state = _hero_state_to_mixed_state(
        tuple(initial_state), target_roles
    )

    if _abstract_state_is_solved(abstract_state, target_roles):
        return 0

    queue = deque([(abstract_state, 0)])
    visited = {abstract_state}

    while queue:
        state, moves = queue.popleft()
        if moves >= depth_limit:
            continue
        for new_state in _get_abstract_neighbors(state):
            if new_state in visited:
                continue
            if _abstract_state_is_solved(new_state, target_roles):
                return moves + 1
            visited.add(new_state)
            queue.append((new_state, moves + 1))

    return None


# ══════════════════════════════════════════════
#  퍼즐 생성: 기본 모드
# ══════════════════════════════════════════════

def generate_puzzle(
    *,
    min_optimal: int = 5,
    max_optimal: int = 20,
    layout: str = "rows",
    max_attempts: int = 500,
    depth_limit: int = 50,
) -> Dict[str, Any]:
    """기본 모드 퍼즐 생성"""
    target_roles = make_target_roles(layout)

    best_state = None
    best_optimal = -1
    best_heroes = None

    for _ in range(max_attempts):
        selected_heroes = get_random_heroes(8)

        initial_state: List[Optional[str]] = selected_heroes.copy()
        initial_state.append(None)
        random.shuffle(initial_state)

        if is_solved(tuple(initial_state), target_roles):
            continue

        optimal = calculate_optimal_moves(initial_state, target_roles, depth_limit=depth_limit)
        if optimal is None:
            continue

        heroes_info = {h: HEROES[h] for h in selected_heroes}

        if optimal > best_optimal:
            best_optimal = optimal
            best_state = initial_state.copy()
            best_heroes = heroes_info

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


# ══════════════════════════════════════════════
#  퍼즐 생성: 하드 모드
# ══════════════════════════════════════════════

def generate_puzzle_hard(
    *,
    min_optimal: int = 5,
    max_optimal: int = 25,
    max_attempts: int = 500,
    depth_limit: int = 50,
) -> Dict[str, Any]:
    """
    하드 모드 퍼즐 생성

    [생성 방식]
    1) get_random_heroes_for_hard()로:
       - 세부역할 9개 선택 (탱3 + 딜3/4 + 힐3)
       - 1개를 상위 기본역할로 변환
       - 각 역할에서 영웅 1명씩 = 9명
       - 1명 블라인드 → 8명
    2) 8명 + 빈칸 → 셔플
    3) 세부역할 기반 BFS로 최적해
    4) 난이도 범위 체크
    """
    best_state = None
    best_optimal = -1
    best_heroes = None
    best_target = None

    for _ in range(max_attempts):
        hard_data = get_random_heroes_for_hard()

        selected_heroes = hard_data["heroes"]
        target_roles = hard_data["target_sub_roles"]

        initial_state: List[Optional[str]] = selected_heroes.copy()
        initial_state.append(None)
        random.shuffle(initial_state)

        if is_solved_hard(tuple(initial_state), target_roles):
            continue

        optimal = calculate_optimal_moves_hard(
            initial_state, target_roles, depth_limit=depth_limit
        )
        if optimal is None:
            continue

        heroes_info = {h: HEROES[h] for h in selected_heroes}

        if optimal > best_optimal:
            best_optimal = optimal
            best_state = initial_state.copy()
            best_heroes = heroes_info
            best_target = target_roles

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
            "mode": "hard",
        }

    if best_state is not None and best_optimal >= 0:
        empty_idx = best_state.index(None)
        return {
            "puzzle_id": str(uuid.uuid4()),
            "initial_state": best_state,
            "target_roles": best_target,
            "empty_index": empty_idx,
            "heroes": best_heroes,
            "optimal_moves": best_optimal,
            "mode": "hard",
            "warning": f"Could not meet difficulty [{min_optimal}, {max_optimal}]. Returned {best_optimal}.",
        }

    raise RuntimeError("Failed to generate hard puzzle")


# ══════════════════════════════════════════════
#  공용
# ══════════════════════════════════════════════

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
        "grade": grade,
    }


if __name__ == "__main__":
    print("=== 기본 모드 테스트 ===\n")
    p = generate_puzzle(min_optimal=5, max_optimal=15, layout="rows")
    print(f"최적해: {p['optimal_moves']}수")
    print(f"목표: {p['target_roles']}")

    print("\n=== 하드 모드 테스트 ===\n")
    h = generate_puzzle_hard(min_optimal=3, max_optimal=20)
    print(f"최적해: {h['optimal_moves']}수")
    print(f"목표: {h['target_roles']}")
    print(f"영웅: {list(h['heroes'].keys())}")
