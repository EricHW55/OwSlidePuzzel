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
        # 1열=tank(0,3,6), 2열=dps(1,4,7), 3열=support(2,5,8)
        target = [""] * 9
        for idx in (0, 3, 6):
            target[idx] = "tank"
        for idx in (1, 4, 7):
            target[idx] = "dps"
        for idx in (2, 5, 8):
            target[idx] = "support"
        return target

    if layout == "rows":
        # 고정: 탱탱탱딜딜딜힐힐힐
        return ["tank"] * 3 + ["dps"] * 3 + ["support"] * 3
    
    if layout == "shuffle_rows":
        # 행 순서만 랜덤 (예: 딜딜딜탱탱탱힐힐힐)
        rows = [["tank"] * 3, ["dps"] * 3, ["support"] * 3]
        random.shuffle(rows)
        return rows[0] + rows[1] + rows[2]

    # default = random (완전 랜덤)
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
        adjacent.append(index - 3)  # 상
    if row < 2:
        adjacent.append(index + 3)  # 하
    if col > 0:
        adjacent.append(index - 1)  # 좌
    if col < 2:
        adjacent.append(index + 1)  # 우
    
    return adjacent


def is_solved(state: Tuple[Optional[str], ...], target_roles: List[str]) -> bool:
    """현재 상태가 정답인지 확인 (빈 칸 제외하고 역할 매칭)"""
    for i, hero in enumerate(state):
        if hero is None:
            continue  # 빈 칸은 체크 안 함
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


def is_solvable(state: List[Optional[str]], target_roles: List[str]) -> bool:
    """
    슬라이딩 퍼즐이 풀 수 있는지 확인 (inversion count 기반)
    
    3x3 퍼즐에서:
    - 역할 기준으로 inversion 계산
    - 짝수면 풀 수 있음
    """
    tiles = [h for h in state if h is not None]
    role_order = {"tank": 0, "dps": 1, "support": 2}
    
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            role_i = HEROES[tiles[i]]["role"]
            role_j = HEROES[tiles[j]]["role"]
            if role_order[role_i] > role_order[role_j]:
                inversions += 1
    
    return inversions % 2 == 0


def calculate_optimal_moves(
    initial_state: List[Optional[str]],
    target_roles: List[str],
    depth_limit: int = 50,
) -> Optional[int]:
    """BFS로 최적해(최소 이동 횟수) 계산"""
    initial = tuple(initial_state)

    if is_solved(initial, target_roles):
        return 0

    queue = deque([(initial, 0)])
    visited = {initial}

    while queue:
        state, moves = queue.popleft()

        if moves >= depth_limit:
            continue

        for new_state, _ in get_neighbors(state):
            if new_state in visited:
                continue

            if is_solved(new_state, target_roles):
                return moves + 1

            visited.add(new_state)
            queue.append((new_state, moves + 1))

    return None


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
        
        # 풀 수 있는지 확인
        if not is_solvable(initial_state, target_roles):
            continue

        # 최적해 계산
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
