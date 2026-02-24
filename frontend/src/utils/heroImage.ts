export function getHeroImageSrc(heroId: string) {
    const id = heroId.trim().toLowerCase();
    return `/heroes/${id}.png`;
}

/**
 * 역할 아이콘 SVG 경로 반환
 *
 * 기본역할: tank.svg, damage.svg, support.svg
 * 세부역할: initiator.svg, bruiser.svg, stalwart.svg, ...
 *
 * 파일 위치: public/roles/
 */
export function getRoleIconSrc(role: string): string {
    // dps → damage.svg 매핑 (파일명이 damage.svg)
    const mapped = role === 'dps' ? 'damage' : role;
    return `/roles/${mapped}.svg`;
}
