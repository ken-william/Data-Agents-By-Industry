import React, { useEffect, useRef, useState } from 'react';
import gsap from 'gsap';

/**
 * Cinematic Canvas Background Component
 * Implements Canvas Rendering, Aspect-Ratio Cover (ZOOM_FACTOR=1.35),
 * GSAP Interactive Mouse Parallax, and Scroll-driven animation (Scrollytelling).
 */
export function CinematicCanvasBackground() {
  const canvasRef = useRef(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [loadProgress, setLoadProgress] = useState(0);

  const scrollFractionRef = useRef(0);
  const mouseRef = useRef({ x: 0, y: 0 });

  useEffect(() => {
    // 1. Simulate Preloading State for 60FPS High-Performance Canvas Scene
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      setLoadProgress(Math.min(progress, 100));
      if (progress >= 100) {
        clearInterval(interval);
        setIsLoaded(true);
      }
    }, 40);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let animationFrameId;
    const ZOOM_FACTOR = 1.35;

    // Generate Procedural Google Spectral Nebula Orbs & Particles
    const numParticles = 80;
    const particles = Array.from({ length: numParticles }, () => ({
      x: Math.random(),
      y: Math.random(),
      radius: Math.random() * 3 + 1,
      baseAlpha: Math.random() * 0.7 + 0.3,
      speed: Math.random() * 0.0005 + 0.0002,
      color: ['#38BDF8', '#818CF8', '#C084FC', '#EC4899', '#FBBC05'][Math.floor(Math.random() * 5)]
    }));

    const nebulae = [
      { cx: 0.3, cy: 0.3, r: 0.4, color1: 'rgba(56, 189, 248, 0.35)', color2: 'rgba(99, 102, 241, 0.05)' },
      { cx: 0.7, cy: 0.7, r: 0.45, color1: 'rgba(192, 132, 252, 0.3)', color2: 'rgba(236, 72, 153, 0.05)' },
      { cx: 0.5, cy: 0.2, r: 0.35, color1: 'rgba(251, 188, 5, 0.25)', color2: 'rgba(56, 189, 248, 0.02)' }
    ];

    // Canvas Resize with Aspect Ratio Cover Math & ZOOM_FACTOR
    const resizeCanvas = () => {
      const dpr = window.devicePixelRatio || 1;
      canvas.width = window.innerWidth * dpr;
      canvas.height = window.innerHeight * dpr;
      ctx.scale(dpr, dpr);
    };

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    // 2. Interactive Mouse Parallax using GSAP
    const handleMouseMove = (e) => {
      const mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
      const mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
      mouseRef.current = { x: mouseX, y: mouseY };

      // Smooth GSAP Parallax Offset in opposite direction of mouse movement
      gsap.to(canvas, {
        x: -mouseX * 30,
        y: -mouseY * 30,
        duration: 1.2,
        ease: 'power2.out'
      });
    };

    window.addEventListener('mousemove', handleMouseMove);

    // 3. Scroll-Driven Scrollytelling Fraction
    const handleScroll = () => {
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const currentScroll = window.scrollY;
      scrollFractionRef.current = scrollHeight > 0 ? Math.min(Math.max(currentScroll / scrollHeight, 0), 1) : 0;
    };

    window.addEventListener('scroll', handleScroll);

    // 4. Main 60FPS Draw Loop
    let time = 0;
    const drawFrame = () => {
      time += 0.01;
      const scrollFrac = scrollFractionRef.current;
      const width = window.innerWidth;
      const height = window.innerHeight;

      // Solid Black Cinematic Background
      ctx.fillStyle = '#000000';
      ctx.fillRect(0, 0, width, height);

      ctx.save();
      // Apply Manual object-fit: cover zoom centering math
      ctx.translate(width / 2, height / 2);
      ctx.scale(ZOOM_FACTOR, ZOOM_FACTOR);
      ctx.translate(-width / 2, -height / 2);

      // Draw Morphing Spectral Nebulae
      nebulae.forEach((neb, i) => {
        const offset = Math.sin(time + i + scrollFrac * Math.PI * 2) * 40;
        const x = neb.cx * width + offset;
        const y = neb.cy * height + Math.cos(time * 0.8 + i) * 30;
        const radius = neb.r * Math.min(width, height) * (1 + scrollFrac * 0.2);

        const grad = ctx.createRadialGradient(x, y, 0, x, y, radius);
        grad.addColorStop(0, neb.color1);
        grad.addColorStop(1, neb.color2);

        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(x, y, radius, 0, Math.PI * 2);
        ctx.fill();
      });

      // Draw Floating Particles
      particles.forEach((p) => {
        p.y -= p.speed;
        if (p.y < 0) p.y = 1;

        const px = p.x * width + Math.sin(time + p.x * 10) * 15;
        const py = p.y * height;
        const alpha = p.baseAlpha * (0.6 + Math.sin(time * 2 + p.x * 20) * 0.4);

        ctx.fillStyle = p.color;
        ctx.globalAlpha = alpha;
        ctx.beginPath();
        ctx.arc(px, py, p.radius, 0, Math.PI * 2);
        ctx.fill();
        ctx.globalAlpha = 1.0;
      });

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
        <div className="fixed inset-0 z-50 flex flex-col items-center justify-center bg-black text-white font-sans transition-opacity duration-500">
          <div className="w-12 h-12 rounded-full border-2 border-sky-400 border-t-transparent animate-spin mb-4" />
          <div className="text-sm font-semibold tracking-wider text-slate-300">
            LOADING CINEMATIC CANVAS ({loadProgress}%)
          </div>
        </div>
      )}

      {/* Cinematic Fullscreen Canvas with 1.05 Scale & GSAP Parallax */}
      <canvas
        ref={canvasRef}
        className="fixed inset-0 w-full h-full pointer-events-none -z-10 bg-black transform scale-[1.05] transition-transform"
      />
    </>
  );
}
