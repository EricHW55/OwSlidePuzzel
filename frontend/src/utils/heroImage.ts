export function getHeroImageSrc(heroId: string) {
    const id = heroId.trim().toLowerCase();
    return `/heroes/${id}.png`;
}