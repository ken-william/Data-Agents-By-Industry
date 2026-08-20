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

// Google Light Workspace Pastel Themes per Sector
export const COLOR_THEMES = {
  indigo: {
    category: "Secteur Public & RH",
    badge: "bg-blue-50 text-blue-700 border-blue-200",
    topBorder: "border-t-4 border-t-blue-500",
    iconBg: "bg-blue-50 text-blue-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  emerald: {
    category: "Banque & Finance B2B",
    badge: "bg-emerald-50 text-emerald-700 border-emerald-200",
    topBorder: "border-t-4 border-t-emerald-500",
    iconBg: "bg-emerald-50 text-emerald-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  purple: {
    category: "Télécoms & IoT 5G",
    badge: "bg-purple-50 text-purple-700 border-purple-200",
    topBorder: "border-t-4 border-t-purple-500",
    iconBg: "bg-purple-50 text-purple-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  cyan: {
    category: "Spatial & Satellite",
    badge: "bg-cyan-50 text-cyan-700 border-cyan-200",
    topBorder: "border-t-4 border-t-cyan-500",
    iconBg: "bg-cyan-50 text-cyan-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  sky: {
    category: "Transports & SNCF",
    badge: "bg-sky-50 text-sky-700 border-sky-200",
    topBorder: "border-t-4 border-t-sky-500",
    iconBg: "bg-sky-50 text-sky-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  teal: {
    category: "Santé & Urgences",
    badge: "bg-teal-50 text-teal-700 border-teal-200",
    topBorder: "border-t-4 border-t-teal-500",
    iconBg: "bg-teal-50 text-teal-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  amber: {
    category: "Retail & CPG Stocks",
    badge: "bg-amber-50 text-amber-700 border-amber-200",
    topBorder: "border-t-4 border-t-amber-500",
    iconBg: "bg-amber-50 text-amber-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  rose: {
    category: "Sport & Stades RES",
    badge: "bg-rose-50 text-rose-700 border-rose-200",
    topBorder: "border-t-4 border-t-rose-500",
    iconBg: "bg-rose-50 text-rose-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  yellow: {
    category: "Énergie & Bornes IRVE",
    badge: "bg-yellow-50 text-yellow-700 border-yellow-200",
    topBorder: "border-t-4 border-t-yellow-500",
    iconBg: "bg-yellow-50 text-yellow-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  green: {
    category: "Agriculture & CO2e",
    badge: "bg-green-50 text-green-700 border-green-200",
    topBorder: "border-t-4 border-t-green-500",
    iconBg: "bg-green-50 text-green-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  },
  fuchsia: {
    category: "Cinéma & CNC Box-Office",
    badge: "bg-fuchsia-50 text-fuchsia-700 border-fuchsia-200",
    topBorder: "border-t-4 border-t-fuchsia-500",
    iconBg: "bg-fuchsia-50 text-fuchsia-600",
    button: "bg-blue-600 hover:bg-blue-700 text-white font-semibold shadow-sm"
  }
};

export function getAgentTheme(themeObj) {
  const colorKey = typeof themeObj === 'string' ? themeObj : (themeObj?.color || 'indigo');
  const matched = COLOR_THEMES[colorKey] || COLOR_THEMES.indigo;

  return {
    category: themeObj?.category || matched.category,
    badge: matched.badge,
    topBorder: matched.topBorder,
    iconBg: matched.iconBg,
    button: matched.button
  };
}
