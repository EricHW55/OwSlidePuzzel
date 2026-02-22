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
                {/* 링 내경 클리핑 마스크 */}
                <clipPath id={`inner-ring-clip-${uid}`}>
                    <circle cx="50" cy="50" r="33" />
                </clipPath>
            </defs>

            <g clipPath={`url(#inner-ring-clip-${uid})`}>
                {/*
                  ── 왼쪽 날개 (2파트) ──

                  삼각형 (상단 뾰족한 부분):
                      (47,28)
                       / \
                      /   \
                  (36,49)─(47,57)

                  직사각형/평행사변형 (하단 대각선 부분):
                  (36,49)──(47,57)
                    /          /
                   /          /
                  (8,90)──(25,90)
                */}

                {/* 왼쪽 날개 (삼각형+평행사변형 통합) */}
                <polygon
                    points="48,27 37,48 0,76 11,84 48,56"
                    fill={ringColor}
                />

                {/* 오른쪽 날개 (좌우대칭) */}
                <polygon
                    points="52,27 63,48 100,76 89,84 52,56"
                    fill={ringColor}
                />
            </g>

            {/* 하단 흰색 링 */}
            <path
                d="M 74.43 20.89 A 38 38 0 1 1 25.57 20.89"
                stroke={ringColor}
                strokeWidth="11"
                strokeLinecap="butt"
                fill="none"
            />

            {/* 상단 오렌지 아치 */}
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
