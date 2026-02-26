import React, { useState, useCallback, useEffect, useRef } from 'react';
import TriangleBackground from './components/TriangleBackground';
import OverwatchLogoIcon from './components/icon/OverwatchLogoIcon';
import { useTimer } from './hooks/useTimer';
import { api, generateLocalResult } from './hooks/useApi';
import { ROLES, ALL_ROLES, SUB_ROLE_PARENT, isBasicRole, SUB_ROLE_GROUPS, HEROES } from './data/heroes';
import { GameState, GameMode, Screen, Role, SubmitResult, RankingRecord, Hero } from './types';
import './styles/index.css';
import { getHeroImageSrc, getRoleIconSrc } from "./utils/heroImage";


const App: React.FC = () => {
  // 화면 상태
  const [screen, setScreen] = useState<Screen>('menu');
  const [gameMode, setGameMode] = useState<GameMode>('quick');

  // 하드모드 토글
  const [isHardMode, setIsHardMode] = useState<boolean>(false);

  // 로딩 취소 플래그
  const cancelledRef = useRef<boolean>(false);

  // 타일 이동 사운드 (public/sound/clicker.wav)
  const clickSoundsRef = useRef<HTMLAudioElement[]>([]);
  const clickSoundIdxRef = useRef<number>(0);

  useEffect(() => {
    // 개발 환경 StrictMode에서 effect 2번 실행될 수 있어서 방어
    if (clickSoundsRef.current.length) return;

    const POOL_SIZE = 6; // 연속 클릭 시 끊김 방지용
    clickSoundsRef.current = Array.from({ length: POOL_SIZE }, () => {
      const a = new Audio('/sound/clicker.wav'); // public 기준 경로
      a.preload = 'auto';
      a.volume = 0.6;
      return a;
    });
  }, []);

  const playClickSound = useCallback((): void => {
    const pool = clickSoundsRef.current;
    if (!pool.length) return;

    const i = clickSoundIdxRef.current % pool.length;
    clickSoundIdxRef.current += 1;

    const a = pool[i];
    try { a.currentTime = 0; } catch {}
    a.play().catch(() => {
      // 모바일/브라우저 정책으로 막히는 경우 무시 (사용자 제스처 후엔 보통 OK)
    });
  }, []);

  // 게임 상태
  const [gameState, setGameState] = useState<GameState>('idle');
  const [targetRoles, setTargetRoles] = useState<string[]>([]);
  const [puzzleTiles, setPuzzleTiles] = useState<(string | null)[]>([]);
  const [emptyIndex, setEmptyIndex] = useState<number>(8);
  const [moves, setMoves] = useState<number>(0);
  const [puzzleId, setPuzzleId] = useState<string>('');

  // 서버에서 받은 영웅 정보
  const [heroesData, setHeroesData] = useState<Record<string, Hero>>({});

  // 타이머
  const { time, formattedTime, start: startTimer, stop: stopTimer, reset: resetTimer, formatTime } = useTimer();

  // 모달 상태
  const [showResultModal, setShowResultModal] = useState<boolean>(false);
  const [showNicknameModal, setShowNicknameModal] = useState<boolean>(false);
  const [showRankingModal, setShowRankingModal] = useState<boolean>(false);
  const [result, setResult] = useState<SubmitResult | null>(null);
  const [nickname, setNickname] = useState<string>('');
  const [rankings, setRankings] = useState<RankingRecord[]>([]);
  const [showDictModal, setShowDictModal] = useState<boolean>(false);

  // 정답 확인 - 기본 + 하드 모드 통합
  const checkSolved = useCallback((
      tiles: (string | null)[],
      roles: string[],
      heroes: Record<string, Hero>,
  ): boolean => {
    for (let i = 0; i < 9; i++) {
      const tile = tiles[i];
      if (tile === null) continue;

      const hero = heroes[tile];
      if (!hero) continue;

      const target = roles[i];

      if (isBasicRole(target)) {
        // 기본역할 칸: role로 판정
        if (hero.role !== target) return false;
      } else {
        // 세부역할 칸: sub_role로 판정
        if (hero.sub_role !== target) return false;
      }
    }
    return true;
  }, []);

  // 타일이 현재 위치에 맞는지 확인 (녹색 표시용)
  const isTileCorrect = useCallback((heroId: string, targetRole: string): boolean => {
    const hero = heroesData[heroId];
    if (!hero) return false;

    if (isBasicRole(targetRole)) {
      return hero.role === targetRole;
    } else {
      return hero.sub_role === targetRole;
    }
  }, [heroesData]);

  // 퍼즐 초기화
  const initPuzzle = useCallback(async (mode: GameMode): Promise<void> => {
    stopTimer();
    resetTimer();
    setGameState('idle');
    setMoves(0);

    const puzzle = await api.createPuzzle(mode);

    // API 응답 왔을 때 이미 취소됐으면 무시
    if (cancelledRef.current) return;

    if (!puzzle) {
      alert('퍼즐 생성 실패! 백엔드를 확인해주세요.');
      return;
    }

    setPuzzleId(puzzle.puzzle_id);
    setTargetRoles(puzzle.target_roles);
    setPuzzleTiles(puzzle.initial_state);
    setEmptyIndex(puzzle.empty_index);
    setHeroesData(puzzle.heroes);

    setGameState('playing');

    requestAnimationFrame(() => {
      startTimer();
    });
  }, [resetTimer, startTimer, stopTimer]);

  // 인접 확인
  const isAdjacent = (idx1: number, idx2: number): boolean => {
    const r1 = Math.floor(idx1 / 3), c1 = idx1 % 3;
    const r2 = Math.floor(idx2 / 3), c2 = idx2 % 3;
    return (Math.abs(r1 - r2) + Math.abs(c1 - c2)) === 1;
  };

  // 타일 이동
  const moveTile = useCallback((index: number): void => {
    if (!isAdjacent(index, emptyIndex)) return;
    if (gameState === 'completed') return;

    playClickSound();

    const newTiles = [...puzzleTiles];
    newTiles[emptyIndex] = newTiles[index];
    newTiles[index] = null;

    setPuzzleTiles(newTiles);
    setEmptyIndex(index);
    setMoves(prev => prev + 1);

    if (checkSolved(newTiles, targetRoles, heroesData)) {
      setGameState('completed');
      stopTimer();
    }
  }, [puzzleTiles, emptyIndex, gameState, targetRoles, heroesData, startTimer, stopTimer, checkSolved]);

  // 게임 완료 처리
  const handleGameComplete = useCallback(async (): Promise<void> => {
    let resultData: SubmitResult;

    if (gameMode === 'ranked' || gameMode === 'hard') {
      const response = await api.submitResult(puzzleId, time, moves);
      resultData = response || generateLocalResult(moves, true);
    } else {
      resultData = generateLocalResult(moves, false);
    }

    setResult(resultData);
    setShowResultModal(true);

    // 랭킹전/하드모드이고 랭킹권이면 닉네임 입력
    if ((gameMode === 'ranked' || gameMode === 'hard') && resultData.is_rank_worthy) {
      setTimeout(() => {
        setShowResultModal(false);
        setShowNicknameModal(true);
      }, 2000);
    }
  }, [gameMode, puzzleId, time, moves]);

  // 게임 완료 시 결과 처리
  useEffect(() => {
    if (gameState === 'completed') {
      handleGameComplete();
    }
  }, [gameState, handleGameComplete]);

  // 게임 시작
  const startGame = async (mode: GameMode): Promise<void> => {
    cancelledRef.current = false;
    setGameMode(mode);
    setScreen('loading');

    await initPuzzle(mode);
    if (cancelledRef.current) return; // 취소됐으면 게임 화면으로 안 감
    setScreen('game');
  };

  // 메뉴로 돌아가기
  const goToMenu = (): void => {
    cancelledRef.current = true; // 진행 중인 로딩 취소
    stopTimer();
    setShowResultModal(false);
    setShowNicknameModal(false);
    setShowRankingModal(false);
    setShowDictModal(false);
    setScreen('menu');
  };

  // 닉네임 제출
  const submitNickname = async (): Promise<void> => {
    if (!nickname.trim()) return;
    await api.submitRanking(puzzleId, time, moves, nickname.trim());
    setNickname('');
    setShowNicknameModal(false);
    fetchRankings();
    setShowRankingModal(true);
  };

  // 랭킹 조회 (모드별)
  const fetchRankings = async (): Promise<void> => {
    const mode = isHardMode ? 'hard' : 'ranked';
    const data = await api.getRankings(10, mode);
    setRankings(data.rankings || []);
  };

  // 랭킹 모달 열기
  const showRanking = (): void => {
    fetchRankings();
    setShowRankingModal(true);
  };

  // 다시 하기
  const retryGame = async (): Promise<void> => {
    cancelledRef.current = false;
    setShowResultModal(false);
    setScreen('loading');

    await initPuzzle(gameMode);
    if (cancelledRef.current) return;
    setScreen('game');
  };

  // 키보드 이벤트 (닉네임 입력)
  const handleNicknameKeyPress = (e: React.KeyboardEvent<HTMLInputElement>): void => {
    if (e.key === 'Enter') {
      submitNickname();
    }
  };

  // 게임 모드 라벨
  const getGameModeLabel = (): string => {
    if (gameMode === 'hard') return '하드모드';
    if (gameMode === 'ranked') return '경쟁전';
    return '일반전';
  };

  // 역할 이름 가져오기 (기본 + 세부 통합)
  const getRoleName = (role: string): string => {
    return ALL_ROLES[role]?.name || role;
  };

  // 역할의 상위 기본역할 가져오기 (아이콘 표시용)
  const getParentRole = (role: string): Role => {
    if (isBasicRole(role)) return role;
    return SUB_ROLE_PARENT[role as keyof typeof SUB_ROLE_PARENT] || 'tank';
  };

  return (
      <div className={`app ${isHardMode ? 'hard-mode' : ''}`}>
        <TriangleBackground isHardMode={isHardMode} />

        {/* 메인 메뉴 */}
        {screen === 'menu' && (
            <div className="screen active">
              {/* 하드모드 토글 스위치 */}
              <div className="hard-mode-toggle">
                <span className="toggle-label">하드모드</span>
                <label className="toggle-switch">
                  <input
                      type="checkbox"
                      checked={isHardMode}
                      onChange={e => setIsHardMode(e.target.checked)}
                  />
                  <span className="toggle-slider" />
                </label>
              </div>

              <div className="menu-logo">
                {isHardMode ? (
                    <img
                        src="/talon.webp"
                        alt="Talon Logo"
                        className="talon-logo"
                        draggable={false}
                    />
                ) : (
                    <OverwatchLogoIcon size={160} />
                )}
                <div className="menu-title">{isHardMode ? 'TALON' : 'OVERWATCH'}</div>
                <div className="menu-subtitle">
                  {isHardMode ? 'HARD PUZZLE' : 'ROLE PUZZLE'}
                </div>
              </div>
              <div className="menu-buttons">
                {isHardMode ? (
                    <>
                      <button className="menu-btn secondary dict" onClick={() => setShowDictModal(true)}>
                        역할군 보기
                      </button>
                      <button className="menu-btn primary hard" onClick={() => startGame('hard')}>
                        하드모드 시작
                      </button>
                    </>
                ) : (
                    <>
                      <button className="menu-btn primary" onClick={() => startGame('quick')}>
                        일반전
                      </button>
                      <button className="menu-btn primary" onClick={() => startGame('ranked')}>
                        경쟁전
                      </button>
                    </>
                )}
                <button className="menu-btn secondary" onClick={showRanking}>
                  {isHardMode ? '하드 랭킹' : '랭킹 보기'}
                </button>
              </div>
            </div>
        )}

        {/* 로딩 화면 */}
        {screen === "loading" && (
            <div className="screen active">
              <div className="loading-wrap">
                <img
                    src="/icon2.png"
                    alt="앱 아이콘"
                    style={{ width: 160, height: 160 }}
                    draggable={false}
                />
                <div className="loading-title">매칭 중…</div>
                <div className="loading-sub">퍼즐 준비하는 중</div>

                <div className="loading-dots" aria-hidden="true">
                  <span />
                  <span />
                  <span />
                </div>

                <button className="menu-btn secondary" onClick={goToMenu}>
                  취소
                </button>
              </div>
            </div>
        )}

        {/* 게임 화면 */}
        {screen === 'game' && (
            <div className="screen active">
              <div className="game-header">
                <button className="back-btn" onClick={goToMenu}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
                  </svg>
                  나가기
                </button>
                <span className={`game-mode-label ${gameMode === 'hard' ? 'hard' : ''}`}>
                            {getGameModeLabel()}
                        </span>
              </div>

              <div className="game-stats">
                <div className="stat-box">
                  <div className="stat-label">시간</div>
                  <div className="stat-value">{formattedTime}</div>
                </div>
                <div className="stat-box">
                  <div className="stat-label">이동</div>
                  <div className="stat-value">{moves}</div>
                </div>
              </div>

              <div className="puzzle-area">
                {/* 목표 배치 */}
                <div>
                  <div className="puzzle-label">목표 배치</div>
                  <div className="puzzle-grid">
                    {targetRoles.map((role, index) => {
                      const iconSize = isBasicRole(role) ? 44 : 56;
                      return (
                          <div
                              key={index}
                              className={`role-slot ${getParentRole(role)} ${!isBasicRole(role) ? 'sub-role' : ''}`}
                          >
                            <img
                                className="role-icon-img"
                                src={getRoleIconSrc(role)}
                                alt={getRoleName(role)}
                                title={getRoleName(role)}
                                draggable={false}
                                style={{ width: iconSize, height: iconSize }}
                            />
                          </div>
                      );
                    })}
                  </div>
                </div>

                {/* 슬라이딩 퍼즐 */}
                <div>
                  <div className="puzzle-label">슬라이딩 퍼즐</div>
                  <div className="puzzle-grid">
                    {puzzleTiles.map((heroId, index) => {
                      if (heroId === null) {
                        return <div key={index} className="hero-tile empty" />;
                      }

                      const hero = heroesData[heroId];
                      if (!hero) {
                        return <div key={index} className="hero-tile empty" />;
                      }

                      const isCorrect = isTileCorrect(heroId, targetRoles[index]);
                      const isMovable = isAdjacent(index, emptyIndex);

                      return (
                          <div
                              key={index}
                              className={`hero-tile ${isCorrect ? "correct" : ""} ${isMovable ? "movable" : ""}`}
                              onClick={() => isMovable && moveTile(index)}
                          >
                            <img
                                className="hero-img"
                                src={getHeroImageSrc(heroId)}
                                alt={hero.name_ko}
                                draggable={false}
                                onError={(e) => {
                                  (e.currentTarget as HTMLImageElement).src = "/heroes/_unknown.png";
                                }}
                            />
                          </div>
                      );
                    })}
                  </div>
                </div>
              </div>

              <p className="game-hint">빈 칸 옆의 영웅을 클릭하여 이동하세요</p>
            </div>
        )}

        {/* 결과 모달 */}
        {showResultModal && result && (
            <div className="modal-overlay active" onClick={() => setShowResultModal(false)}>
              <div className="modal" onClick={e => e.stopPropagation()}>
                <h2 className="modal-title">🎉 퍼즐 완료!</h2>
                <div className="result-grid">
                  <div className="result-item">
                    <div className="result-label">시간</div>
                    <div className="result-value">{formatTime(time)}</div>
                  </div>
                  <div className="result-item">
                    <div className="result-label">이동 횟수</div>
                    <div className="result-value">{moves}회</div>
                  </div>
                  <div className="result-item">
                    <div className="result-label">최적해</div>
                    <div className="result-value">{result.optimal_moves}회</div>
                  </div>
                  <div className="result-item">
                    <div className="result-label">오차</div>
                    <div className="result-value" style={{ color: result.move_difference === 0 ? '#FFD700' : '#FFA500' }}>
                      +{result.move_difference}
                    </div>
                  </div>
                </div>
                <div className={`grade ${result.grade.toLowerCase().replace(' ', '-')}`}>{result.grade}</div>
                {(gameMode === 'ranked' || gameMode === 'hard') && result.is_rank_worthy && (
                    <div className="rank-badge">🏆 {result.current_rank}위!</div>
                )}
                <div>
                  <button className="modal-btn primary" onClick={retryGame}>다시 도전</button>
                  <button className="modal-btn secondary" onClick={goToMenu}>메뉴로</button>
                </div>
              </div>
            </div>
        )}

        {/* 닉네임 모달 */}
        {showNicknameModal && (
            <div className="modal-overlay active">
              <div className="modal">
                <h2 className="modal-title">🏆 랭킹 등록</h2>
                <p style={{ color: '#7aa2b8', marginBottom: '15px' }}>
                  {result?.current_rank}위에 진입!
                </p>
                <input
                    type="text"
                    className="nickname-input"
                    placeholder="배틀태그 입력"
                    maxLength={20}
                    value={nickname}
                    onChange={e => setNickname(e.target.value)}
                    onKeyPress={handleNicknameKeyPress}
                    autoFocus
                />
                <div>
                  <button className="modal-btn primary" onClick={submitNickname}>등록</button>
                  <button className="modal-btn secondary" onClick={() => setShowNicknameModal(false)}>건너뛰기</button>
                </div>
              </div>
            </div>
        )}

        {/* 랭킹 모달 */}
        {showRankingModal && (
            <div className="modal-overlay active" onClick={() => setShowRankingModal(false)}>
              <div className="modal ranking-modal" onClick={e => e.stopPropagation()}>
                <h2 className="modal-title">
                  🏆 {isHardMode ? 'HARD' : ''} TOP 10
                </h2>
                <div className="ranking-list">
                  {rankings.length === 0 ? (
                      <p className="no-ranking">기록이 없습니다</p>
                  ) : (
                      rankings.map(r => (
                          <div key={r.id} className="ranking-item">
                            <span className="rank-position">#{r.rank}</span>
                            <span className="rank-name">{r.nickname}</span>
                            <span className="rank-time">{r.time_display}</span>
                            <span className="rank-moves">{r.move_diff === 0 ? 'PERFECT' : `+${r.move_diff}`}</span>
                          </div>
                      ))
                  )}
                </div>
                <button className="modal-btn secondary" onClick={() => setShowRankingModal(false)}>닫기</button>
              </div>
            </div>
        )}

        {/* 역할군 사전 모달 */}
        {showDictModal && (
            <div className="modal-overlay active" onClick={() => setShowDictModal(false)}>
              <div className="modal dict-modal" onClick={e => e.stopPropagation()}>
                <h2 className="modal-title">세부 역할군 정보</h2>
                <div className="dict-content">
                  {(['tank', 'dps', 'support'] as const).map(parentRole => (
                      <div key={parentRole} className="dict-section">
                        <div className="dict-parent-header">
                          <img src={getRoleIconSrc(parentRole)} alt="" className="dict-parent-icon" />
                          <span>{ROLES[parentRole].name}</span>
                        </div>
                        {SUB_ROLE_GROUPS
                            .filter(g => g.parent === parentRole)
                            .map(group => (
                                <div key={group.subRole} className="dict-group">
                                  <div className="dict-sub-header">
                                    <img src={getRoleIconSrc(group.subRole)} alt="" className="dict-sub-icon" />
                                    <span>{group.name}</span>
                                  </div>
                                  <div className="dict-heroes">
                                    {group.heroes.map(heroId => (
                                        <div key={heroId} className="dict-hero">
                                          <img
                                              src={getHeroImageSrc(heroId)}
                                              alt={HEROES[heroId]?.name_ko}
                                              className="dict-hero-img"
                                              onError={(e) => {
                                                (e.currentTarget as HTMLImageElement).src = "/heroes/_unknown.png";
                                              }}
                                          />
                                          <span className="dict-hero-name">{HEROES[heroId]?.name_ko}</span>
                                        </div>
                                    ))}
                                  </div>
                                </div>
                            ))
                        }
                      </div>
                  ))}
                </div>
                <button className="modal-btn secondary" onClick={() => setShowDictModal(false)}>닫기</button>
              </div>
            </div>
        )}
      </div>
  );
};

export default App;
