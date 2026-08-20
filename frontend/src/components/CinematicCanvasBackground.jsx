import React, { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';

/**
 * 3D Luminous Google Wave Canvas Component
 * Renders a high-performance 60FPS 3D Undulating Wave Grid using Google's iconic bright colors
 * (Blue #4285F4, Red #EA4335, Yellow #FBBC05, Green #34A853) against a bright luminous backdrop.
 */
export function CinematicCanvasBackground() {
  const canvasRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);

  const scrollFractionRef = useRef(0);
  const mouseRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    // 1. Simulate Preloading for 3D Canvas Scene
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setLoadProgress(Math.min(progress, 100));
      if (progress >= 100) {
        clearInterval(interval);
        setIsLoaded(true);
      }
    }, 35);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let animationFrameId;
    const ZOOM_FACTOR = 1.25;

    // Google Luminous 4 Colors
    const googleColors = [
      'rgba(66, 133, 244, 0.75)',  // Google Blue
      'rgba(234, 67, 53, 0.75)',   // Google Red
      'rgba(251, 188, 5, 0.75)',   // Google Yellow
      'rgba(52, 168, 83, 0.75)'    // Google Green
    ];

    // Canvas Resize
    const resizeCanvas = () => {
      const dpr = window.devicePixelRatio || 1;
      canvas.width = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      ctx.scale(dpr, dpr);
    };

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // GSAP Mouse Parallax Listener
    const handleMouseMove = (e) => {
      const mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      const mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
      mouseRef.current = { x: mouseX, y: mouseY };

      gsap.to(canvas, {
        x: -mouseX * 25,
        y: -mouseY * 25,
        duration: 1.2,
        ease: 'power2.out'
      });
    };

    window.addEventListener('mousemove', handleMouseMove);

    // Scroll Listener
    const handleScroll = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const currentScroll = window.scrollY;
      scrollFractionRef.current = scrollHeight > 0 ? Math.min(Math.max(currentScroll / scrollHeight, 0), 1) : 0;
    };

    window.addEventListener('scroll', handleScroll);

    // 3D Wave Calculation Parameters
    const numLines = 28;
    const pointsPerLine = 45;
    const spacing = 35;
    const fov = 350;

    let time = 0;

    // Main 60FPS 3D Wave Render Loop
    const drawFrame = () => {
      time += 0.015;
      const scrollFrac = scrollFractionRef.current;
      const width = window.innerWidth;
      const height = window.innerHeight;

      // Bright Luminous Backdrop (#F8FAFC -> #EFF6FF)
      const bgGrad = ctx.createLinearGradient(0, 0, width, height);
      bgGrad.addColorStop(0, '#F8FAFC');
      bgGrad.addColorStop(0.5, '#EFF6FF');
      bgGrad.addColorStop(1, '#EEF2FF');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      ctx.save();
      // Apply Manual Cover Zoom Math
      ctx.translate(width / 2, height / 2);
      ctx.scale(ZOOM_FACTOR, ZOOM_FACTOR);
      ctx.translate(-width / 2, -height / 2);

      // Draw 3D Undulating Wave Grid Lines
      for (let i = 0; i < numLines; i++) {
        const lineProgress = i / numLines;
        const color = googleColors[i % googleColors.length];

        ctx.beginPath();
        ctx.strokeStyle = color;
        ctx.lineWidth = 2.5 - lineProgress * 1.2;

        for (let j = 0; j < pointsPerLine; j++) {
          const colProgress = j / pointsPerLine;

          // 3D Coordinates
          const x3d = (j - pointsPerLine / 2) * spacing;
          const z3d = (i + 1) * spacing + 120;
          
          // 3D Wave Height Equation (Undulating Sine/Cos Physics)
          const wave1 = Math.sin(colProgress * Math.PI * 3 + time * 1.8 + scrollFrac * Math.PI) * 45;
          const wave2 = Math.cos(lineProgress * Math.PI * 4 - time * 1.2) * 25;
          const mouseTilt = mouseRef.current.y * 30;
          const y3d = wave1 + wave2 + mouseTilt;

          // 3D Perspective Projection
          const scale = fov / (fov + z3d);
          const x2d = width / 2 + x3d * scale + (mouseRef.current.x * 40 * scale);
          const y2d = height / 2 + y3d * scale + 60;

          if (j === 0) {
            ctx.moveTo(x2d, y2d);
          } else {
            ctx.lineTo(x2d, y2d);
          }
        }
        ctx.stroke();
      }

      ctx.restore();
      animationFrameId = requestAnimationFrame(drawFrame);
    };

    drawFrame();

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('scroll', handleScroll);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <>
      {/* Loading Overlay */}
      {!isLoaded && (
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-[#F8FAFC] text-slate-800 font-sans transition-opacity duration-500">
          <div className="w-12 h-12 rounded-full border-3 border-blue-500 border-t-transparent animate-spin mb-4" />
          <div className="text-sm font-semibold tracking-wider text-slate-600">
            CHARGEMENT VAGUES 3D GOOGLE ({loadProgress}%)
          </div>
        </div>
      )}

      {/* Fullscreen 3D Wave Canvas */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 w-full h-full pointer-events-none -z-10 transform scale-[1.05] transition-transform"
      />
    </>
  );
}
