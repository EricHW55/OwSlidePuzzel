import React, { useEffect, useRef } from 'react';
import { Triangle } from '../types';

const TriangleBackground: React.FC = () => {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const trianglesRef = useRef<Triangle[]>([]);
  const animationRef = useRef<number>(0);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const getRandomColor = (): { r: number; g: number; b: number } => {
      const colors = [
        { r: 42, g: 69, b: 85 },
        { r: 30, g: 53, b: 69 },
        { r: 37, g: 58, b: 74 },
        { r: 26, g: 42, b: 58 },
        { r: 50, g: 78, b: 95 },
        { r: 35, g: 62, b: 82 },
      ];
      return colors[Math.floor(Math.random() * colors.length)];
    };

    const generateTriangles = (): Triangle[] => {
      const triangles: Triangle[] = [];
      const size = 150;
      const rows = Math.ceil(canvas.height / (size * 0.866)) + 2;
      const cols = Math.ceil(canvas.width / size) + 2;

      for (let row = 0; row < rows; row++) {
        for (let col = 0; col < cols; col++) {
          const x = col * size + (row % 2) * (size / 2);
          const y = row * size * 0.866;

          triangles.push({
            x, y, size, 
            pointing: 'up',
            baseAlpha: 0.04 + Math.random() * 0.06,
            alpha: 0.04 + Math.random() * 0.06,
            targetAlpha: 0.04 + Math.random() * 0.06,
            twinkleSpeed: 0.003 + Math.random() * 0.012,
            color: getRandomColor()
          });

          triangles.push({
            x: x + size / 2, y, size, 
            pointing: 'down',
            baseAlpha: 0.04 + Math.random() * 0.06,
            alpha: 0.04 + Math.random() * 0.06,
            targetAlpha: 0.04 + Math.random() * 0.06,
            twinkleSpeed: 0.003 + Math.random() * 0.012,
            color: getRandomColor()
          });
        }
      }
      return triangles;
    };

    const drawTriangle = (tri: Triangle): void => {
      ctx.beginPath();
      if (tri.pointing === 'up') {
        ctx.moveTo(tri.x, tri.y + tri.size * 0.866);
        ctx.lineTo(tri.x + tri.size / 2, tri.y);
        ctx.lineTo(tri.x + tri.size, tri.y + tri.size * 0.866);
      } else {
        ctx.moveTo(tri.x - tri.size / 2, tri.y);
        ctx.lineTo(tri.x, tri.y + tri.size * 0.866);
        ctx.lineTo(tri.x + tri.size / 2, tri.y);
      }
      ctx.closePath();
      ctx.fillStyle = `rgba(${tri.color.r}, ${tri.color.g}, ${tri.color.b}, ${tri.alpha})`;
      ctx.fill();
      ctx.strokeStyle = `rgba(60, 90, 110, ${tri.alpha * 0.8})`;
      ctx.lineWidth = 1;
      ctx.stroke();
    };

    const resizeCanvas = (): void => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      trianglesRef.current = generateTriangles();
    };

    let lastTime = 0;
    const animate = (currentTime: number): void => {
      const deltaTime = currentTime - lastTime;
      lastTime = currentTime;

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      trianglesRef.current.forEach(tri => {
        if (Math.random() < 0.003) {
          tri.targetAlpha = tri.baseAlpha + Math.random() * 0.18;
        }
        const diff = tri.targetAlpha - tri.alpha;
        tri.alpha += diff * tri.twinkleSpeed * (deltaTime / 16);
        if (Math.abs(diff) < 0.001) tri.targetAlpha = tri.baseAlpha;
        drawTriangle(tri);
      });

      animationRef.current = requestAnimationFrame(animate);
    };

    resizeCanvas();
    animationRef.current = requestAnimationFrame(animate);
    window.addEventListener('resize', resizeCanvas);

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      if (animationRef.current) {
        cancelAnimationFrame(animationRef.current);
      }
    };
  }, []);

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      zIndex: 0,
      background: 'linear-gradient(135deg, #1a2634 0%, #1e3040 50%, #152530 100%)'
    }}>
      <canvas 
        ref={canvasRef} 
        style={{ 
          position: 'absolute', 
          top: 0, 
          left: 0, 
          width: '100%', 
          height: '100%' 
        }} 
      />
    </div>
  );
};

export default TriangleBackground;
