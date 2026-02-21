import React from "react";

type Props = {
    size?: number;
    ringColor?: string;    // 링 + 심볼 색상
    accentColor?: string;  // 오렌지 아치 색상
    className?: string;
};

export default function OverwatchLogoIcon({
                                              size = 140,
                                              ringColor = "#EDEDED",
                                              accentColor = "#F06414",
                                              className,
                                          }: Props) {
    // 고유 ID 생성
    const uid = React.useId().replace(/:/g, "");

    return (
        <svg
            width={size}
            height={size}
            viewBox="0 0 100 100"
            xmlns="http://www.w3.org/2000/svg"
            className={className}
            aria-label="Overwatch Logo"
            role="img"
        >
            <defs>
                {/* 링 내경 클리핑 마스크 (기존 유지) */}
                <clipPath id={`inner-ring-clip-${uid}`}>
                    <circle cx="50" cy="50" r="32.5" />
                </clipPath>
            </defs>

            {/* 1. 내부 심볼 (요청하신 대로 아래로 이동) */}
            {/* 내경 클리핑을 적용하여 튀어나오는 부분만 제거 */}
            <g clipPath={`url(#inner-ring-clip-${uid})`}>
                {/* 왼쪽 날개:
                   - 상단 꼭짓점을 y=21에서 y=28로 낮춰 주황색 아치와 거리 확보
                   - 나머지 y좌표도 비례하게 낮춰(42->49, 85->90) 전체적인 형태 유지하며 아래로 이동
                */}
                <polygon
                    points="47,28 36,49 8,90 25,90 47,57"
                    fill={ringColor}
                />
                {/* 오른쪽 날개 (x축 대칭 적용 및 동일한 y좌표 이동) */}
                <polygon
                    points="53,28 64,49 92,90 75,90 53,57"
                    fill={ringColor}
                />
            </g>

            {/* 2. 하단 흰색 링 (기존 유지) */}
            <path
                d="M 74.43 20.89 A 38 38 0 1 1 25.57 20.89"
                stroke={ringColor}
                strokeWidth="11"
                strokeLinecap="butt"
                fill="none"
            />

            {/* 3. 상단 오렌지 아치 (기존 유지) */}
            <path
                d="M 29.87 17.80 A 38 38 0 0 1 70.13 17.80"
                stroke={accentColor}
                strokeWidth="11"
                strokeLinecap="butt"
                fill="none"
            />
        </svg>
    );
}