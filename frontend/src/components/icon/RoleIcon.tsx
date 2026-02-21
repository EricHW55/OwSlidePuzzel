import React from "react";
import { Role } from "../../types";
// export type RoleType = "support" | "tank" | "damage";

type Props = {
    role: Role;
    size?: number;
    color?: string; // 기본은 currentColor 사용
    className?: string;
};

export default function RoleIcon({
                                     role,
                                     size = 28,
                                     color = "currentColor",
                                     className,
                                 }: Props) {
    const common = {
        width: size,
        height: size,
        viewBox: "0 0 100 100",
        fill: "none",
        xmlns: "http://www.w3.org/2000/svg",
        style: { color } as React.CSSProperties,
        className,
    };

    if (role === "support") {
        // ✅ 힐러(서포터) 아이콘: 이미지처럼 두껍고 묵직한 십자가 형태
        return (
            <svg {...common}>
                <path
                    d="M 38 20 H 62 V 38 H 80 V 62 H 62 V 80 H 38 V 62 H 20 V 38 H 38 Z"
                    fill="currentColor"
                />
            </svg>
        );
    }

    if (role === "tank") {
        // ✅ 탱커 아이콘: 상단이 평평하고 직선으로 떨어지다가 하단이 뾰족해지는 오각형 방패
        return (
            <svg {...common}>
                <path
                    d="M 26 22 H 74 V 55 L 50 84 L 26 55 Z"
                    fill="currentColor"
                />
            </svg>
        );
    }

    // role === "damage" (딜러)
    // ✅ 딜러 아이콘: 윗부분이 곡선(탄두)으로 되어있고, 몸통과 하단 프라이머(네모)가 약간의 간격을 두고 분리된 3발의 탄알
    return (
        <svg {...common}>
            {/* 왼쪽 탄알 */}
            <path
                d="M 22 35 A 6 12 0 0 1 34 35 V 68 H 22 Z M 22 73 H 34 V 82 H 22 Z"
                fill="currentColor"
            />
            {/* 가운데 탄알 */}
            <path
                d="M 44 35 A 6 12 0 0 1 56 35 V 68 H 44 Z M 44 73 H 56 V 82 H 44 Z"
                fill="currentColor"
            />
            {/* 오른쪽 탄알 */}
            <path
                d="M 66 35 A 6 12 0 0 1 78 35 V 68 H 66 Z M 66 73 H 78 V 82 H 66 Z"
                fill="currentColor"
            />
        </svg>
    );
}