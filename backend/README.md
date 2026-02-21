# 오버워치 슬라이딩 퍼즐 - 백엔드

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 서버 실행
python main.py

# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버 실행 후 http://localhost:8000/docs 에서 Swagger UI로 API 테스트 가능

---

## API 엔드포인트

### 1. 새 퍼즐 생성
```
GET /api/puzzle/new
```

**응답 예시:**
```json
{
  "puzzle_id": "abc123...",
  "initial_state": ["reinhardt", "tracer", "ana", ...],
  "target_roles": ["tank", "tank", "tank", "dps", "dps", "dps", "support", "support", "support"],
  "heroes": {
    "reinhardt": {"name": "Reinhardt", "name_ko": "라인하르트", "role": "tank"},
    ...
  }
}
```

### 2. 결과 제출 (닉네임 없이)
```
POST /api/puzzle/submit
```

**요청:**
```json
{
  "puzzle_id": "abc123...",
  "time_ms": 15230,
  "moves": 12
}
```

**응답:**
```json
{
  "success": true,
  "time_ms": 15230,
  "time_display": "00:15.230",
  "moves": 12,
  "optimal_moves": 8,
  "move_difference": 4,
  "grade": "GOOD",
  "is_rank_worthy": true,
  "current_rank": 3,
  "needs_nickname": true
}
```

### 3. 랭킹 등록 (닉네임 포함)
```
POST /api/ranking/submit
```

**요청:**
```json
{
  "puzzle_id": "abc123...",
  "time_ms": 15230,
  "moves": 12,
  "nickname": "김오버"
}
```

### 4. 랭킹 조회
```
GET /api/ranking?limit=10
```

**응답:**
```json
{
  "total_records": 15,
  "rankings": [
    {
      "rank": 1,
      "nickname": "이트레",
      "time_ms": 12100,
      "time_display": "00:12.100",
      "moves": 9,
      "optimal_moves": 7,
      "move_diff": 2
    },
    ...
  ]
}
```

---

## 파일 구조

| 파일 | 설명 |
|------|------|
| `main.py` | FastAPI 앱 + API 엔드포인트 |
| `puzzle.py` | 퍼즐 생성 + BFS 최적해 계산 |
| `database.py` | SQLite 랭킹 시스템 |
| `heroes.py` | 오버워치 영웅 데이터 (44명) |
| `requirements.txt` | Python 의존성 |

---

## 퍼즐 규칙

- 3x3 그리드, 인접한 타일 스왑 방식
- 목표: 1열=탱커, 2열=딜러, 3열=서포터 배치
- 난이도: 최적해 5~15수로 자동 조절
- 점수: 순수 시간 기준, 최적해 대비 오차는 참고용 표시

---

## 등급 기준 (최적해 대비)

| 오차 | 등급 |
|------|------|
| 0 | PERFECT |
| 1~2 | EXCELLENT |
| 3~5 | GOOD |
| 6~10 | NORMAL |
| 11+ | KEEP TRYING |
