import {
  Briefcase,
  TrendingUp,
  Radio,
  Globe,
  Train,
  Activity,
  ShoppingCart,
  Landmark,
  Zap,
  Leaf,
  Film,
  Database
} from 'lucide-react';

export const ICON_MAP = {
  Briefcase,
  TrendingUp,
  Radio,
  Globe,
  Train,
  Activity,
  ShoppingCart,
  Landmark,
  Zap,
  Leaf,
  Film,
  Database
};

export function getIconComponent(iconName) {
  return ICON_MAP[iconName] || Database;
}

// Enterprise B2B Clean & Pro Color Mapping
export const COLOR_THEMES = {
  indigo: {
    category: "Secteur Public & RH",
    badge: "bg-indigo-500/10 text-indigo-300 border-indigo-500/20",
    border: "border-indigo-500/40",
    accentBg: "bg-indigo-600",
    button: "bg-indigo-600 hover:bg-indigo-500 text-white"
  },
  emerald: {
    category: "Banque & Finance B2B",
    badge: "bg-emerald-500/10 text-emerald-300 border-emerald-500/20",
    border: "border-emerald-500/40",
    accentBg: "bg-emerald-600",
    button: "bg-emerald-600 hover:bg-emerald-500 text-white"
  },
  purple: {
    category: "Télécoms & Infrastructures",
    badge: "bg-purple-500/10 text-purple-300 border-purple-500/20",
    border: "border-purple-500/40",
    accentBg: "bg-purple-600",
    button: "bg-purple-600 hover:bg-purple-500 text-white"
  },
  cyan: {
    category: "Spatial & Imagerie Satellite",
    badge: "bg-cyan-500/10 text-cyan-300 border-cyan-500/20",
    border: "border-cyan-500/40",
    accentBg: "bg-cyan-600",
    button: "bg-cyan-600 hover:bg-cyan-500 text-white"
  },
  sky: {
    category: "Transports & Mobilité SNCF",
    badge: "bg-sky-500/10 text-sky-300 border-sky-500/20",
    border: "border-sky-500/40",
    accentBg: "bg-sky-600",
    button: "bg-sky-600 hover:bg-sky-500 text-white"
  },
  teal: {
    category: "Santé & Hôpitaux RPPS",
    badge: "bg-teal-500/10 text-teal-300 border-teal-500/20",
    border: "border-teal-500/40",
    accentBg: "bg-teal-600",
    button: "bg-teal-600 hover:bg-teal-500 text-white"
  },
  amber: {
    category: "Retail & CPG Merchandising",
    badge: "bg-amber-500/10 text-amber-300 border-amber-500/20",
    border: "border-amber-500/40",
    accentBg: "bg-amber-600",
    button: "bg-amber-600 hover:bg-amber-500 text-white"
  },
  rose: {
    category: "Sport & Stades Événementiels",
    badge: "bg-rose-500/10 text-rose-300 border-rose-500/20",
    border: "border-rose-500/40",
    accentBg: "bg-rose-600",
    button: "bg-rose-600 hover:bg-rose-500 text-white"
  },
  yellow: {
    category: "Énergie & Bornes IRVE",
    badge: "bg-yellow-500/10 text-yellow-300 border-yellow-500/20",
    border: "border-yellow-500/40",
    accentBg: "bg-yellow-600",
    button: "bg-yellow-600 hover:bg-yellow-500 text-white"
  },
  green: {
    category: "Agriculture & Agroécologie",
    badge: "bg-green-500/10 text-green-300 border-green-500/20",
    border: "border-green-500/40",
    accentBg: "bg-green-600",
    button: "bg-green-600 hover:bg-green-500 text-white"
  },
  fuchsia: {
    category: "Cinéma & Box-Office CNC",
    badge: "bg-fuchsia-500/10 text-fuchsia-300 border-fuchsia-500/20",
    border: "border-fuchsia-500/40",
    accentBg: "bg-fuchsia-600",
    button: "bg-fuchsia-600 hover:bg-fuchsia-500 text-white"
  }
};
