import {
  UserCheck,
  TrendingUp,
  Cpu,
  Globe,
  Navigation,
  Activity,
  Package,
  Award,
  Zap,
  Leaf,
  Film,
  Database
} from 'lucide-react';

export const ICON_MAP = {
  sully: UserCheck,
  credit_advisor: TrendingUp,
  net_arch: Cpu,
  earth_intel: Globe,
  transit_navigator: Navigation,
  pulse_checker: Activity,
  shelf_optimizer: Package,
  arena_manager: Award,
  helios: Zap,
  ceres: Leaf,
  cine_analyst: Film,
  UserCheck,
  TrendingUp,
  Cpu,
  Globe,
  Navigation,
  Activity,
  Package,
  Award,
  Zap,
  Leaf,
  Film,
  Database
};

export function getIconComponent(agentKey) {
  return ICON_MAP[agentKey] || Database;
}

// Google Fluid Blue Theme Badges & Accents
export const COLOR_THEMES = {
  indigo: {
    category: "Secteur Public & RH",
    badge: "bg-blue-500/10 text-blue-300 border-blue-500/20",
    border: "border-blue-500/40 shadow-[0_0_15px_rgba(59,130,246,0.15)]",
    accentBg: "bg-blue-600",
    text: "text-blue-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  emerald: {
    category: "Banque & Finance B2B",
    badge: "bg-sky-500/10 text-sky-300 border-sky-500/20",
    border: "border-sky-500/40 shadow-[0_0_15px_rgba(14,165,233,0.15)]",
    accentBg: "bg-sky-600",
    text: "text-sky-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  purple: {
    category: "Télécoms & IoT 5G",
    badge: "bg-indigo-500/10 text-indigo-300 border-indigo-500/20",
    border: "border-indigo-500/40 shadow-[0_0_15px_rgba(99,102,241,0.15)]",
    accentBg: "bg-indigo-600",
    text: "text-indigo-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  cyan: {
    category: "Spatial & Satellite",
    badge: "bg-teal-500/10 text-teal-300 border-teal-500/20",
    border: "border-teal-500/40 shadow-[0_0_15px_rgba(20,184,166,0.15)]",
    accentBg: "bg-teal-600",
    text: "text-teal-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  sky: {
    category: "Transports & SNCF",
    badge: "bg-cyan-500/10 text-cyan-300 border-cyan-500/20",
    border: "border-cyan-500/40 shadow-[0_0_15px_rgba(6,182,212,0.15)]",
    accentBg: "bg-cyan-600",
    text: "text-cyan-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  teal: {
    category: "Santé & Urgences",
    badge: "bg-emerald-500/10 text-emerald-300 border-emerald-500/20",
    border: "border-emerald-500/40 shadow-[0_0_15px_rgba(16,185,129,0.15)]",
    accentBg: "bg-emerald-600",
    text: "text-emerald-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  amber: {
    category: "Retail & CPG Stocks",
    badge: "bg-blue-500/10 text-blue-300 border-blue-500/20",
    border: "border-blue-500/40 shadow-[0_0_15px_rgba(59,130,246,0.15)]",
    accentBg: "bg-blue-600",
    text: "text-blue-300",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  rose: {
    category: "Sport & Stades RES",
    badge: "bg-indigo-500/10 text-indigo-300 border-indigo-500/20",
    border: "border-indigo-500/40 shadow-[0_0_15px_rgba(99,102,241,0.15)]",
    accentBg: "bg-indigo-600",
    text: "text-indigo-300",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  yellow: {
    category: "Énergie & Bornes IRVE",
    badge: "bg-amber-500/10 text-amber-300 border-amber-500/20",
    border: "border-amber-500/40 shadow-[0_0_15px_rgba(245,158,11,0.15)]",
    accentBg: "bg-amber-600",
    text: "text-amber-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  green: {
    category: "Agriculture & CO2e",
    badge: "bg-green-500/10 text-green-300 border-green-500/20",
    border: "border-green-500/40 shadow-[0_0_15px_rgba(34,197,94,0.15)]",
    accentBg: "bg-green-600",
    text: "text-green-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  },
  fuchsia: {
    category: "Cinéma & CNC Box-Office",
    badge: "bg-violet-500/10 text-violet-300 border-violet-500/20",
    border: "border-violet-500/40 shadow-[0_0_15px_rgba(139,92,246,0.15)]",
    accentBg: "bg-violet-600",
    text: "text-violet-400",
    button: "bg-gradient-to-r from-sky-400 via-blue-500 to-indigo-500 hover:opacity-90 text-white font-semibold"
  }
};

/**
 * Safely resolves an agent's theme object, guaranteeing non-null properties.
 */
export function getAgentTheme(themeObj) {
  const colorKey = typeof themeObj === 'string' ? themeObj : (themeObj?.color || 'indigo');
  const matched = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;

  return {
    category: themeObj?.category || matched.category,
    badge: matched.badge,
    border: matched.border,
    accentBg: matched.accentBg,
    text: matched.text,
    button: matched.button
  };
}
