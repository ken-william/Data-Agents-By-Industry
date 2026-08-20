# Master Specification & Prompt System - Talk to Data (Google Fluid Blue + Compact Capsule Chips)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** pour les événements B2B (BigData Paris 2026, Google Cloud Next).

---

# 🎨 1. Le Design System "Google Fluid Blue" (Compact Capsule Chips)

```css
:root {
  /* Palette Chromatique - Google Fluid Blue */
  --bg-gradient: radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%);
  --bento-bg: rgba(15, 23, 42, 0.45);
  --bento-border: rgba(51, 65, 85, 0.5);
  --bento-border-active: rgba(56, 189, 248, 0.55);
  --gemini-gradient: linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #6366f1 100%);
  
  /* Typographie Premium */
  --font-family-google: "Google Sans Flex", "Google Sans", "Inter", sans-serif;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-dark: #0f172a;

  /* Formes et Animations */
  --radius-card: 16px;
  --radius-pill: 9999px; /* Forme capsule officielle Gemini */
  --glow-active: 0 0 25px rgba(56, 189, 248, 0.15);
}

/* Extension Chips (Bulles Capsules Compactes Gemini) */
.extension-chips-container {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  margin-bottom: 12px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: none;
}

.chip {
  display: flex;
  align-items: center;
  white-space: nowrap;
  padding: 6px 14px;
  background-color: rgba(15, 23, 42, 0.55);
  border: 1px solid rgba(148, 163, 184, 0.2);
  border-radius: 9999px; /* Capsule pleine */
  cursor: pointer;
  transition: all 0.2s ease-in-out;
}

.chip.active {
  background-color: rgba(56, 189, 248, 0.15);
  border-color: rgba(56, 189, 248, 0.6);
  box-shadow: 0 0 14px rgba(56, 189, 248, 0.25);
}

.chip:hover {
  background-color: rgba(30, 41, 59, 0.85);
  border-color: rgba(56, 189, 248, 0.4);
  transform: translateY(-1px);
}
```

---

# 🖥️ 2. Architecture Double Écran (Dual-Screen Setup)

```text
+------------------------------------------------------------------------------------------------+
|                                     DUAL-SCREEN ARCHITECTURE                                   |
+------------------------------------------------------------------------------------------------+
|  ÉCRAN A : LE GRAND ÉCRAN (SHOWCASE / PUBLIC)      |  ÉCRAN B : LE PC CONTRÔLEUR (TACTILE)         |
|  - Orbe Gemini Live & Vagues Wave-1/2/3 (Centre)   |  - Capsules Horizontales Compactes (Pills)    |
|  - Visualisation des Données (70% Largeur)         |  - Barre de Saisie Hybride Fixe (Bas d'écran)  |
|  - SQLFlipCard Recto/Verso (Looker vs Neon SQL)    |  - Push-to-Talk Mic + Smart Chips anti-bruit   |
|  - KPI Scores & Graphiques Épurés                  |  - Console de Log & Switcher Écran A/B        |
+------------------------------------------------------------------------------------------------+
```

---

# 🛠️ 3. Les 11 Capsules Sectorielles (Format Compact Single-Row)

1. **`RH & Emploi`** (`sully`)
2. **`Risque Crédit`** (`credit_advisor`)
3. **`Télécoms 5G`** (`net_arch`)
4. **`Spatial & Sat`** (`earth_intel`)
5. **`Transports`** (`transit_navigator`)
6. **`Santé Publique`** (`pulse_checker`)
7. **`CPG Retail`** (`shelf_optimizer`)
8. **`Sport & Stades`** (`arena_manager`)
9. **`Énergie IRVE`** (`helios`)
10. **`Agriculture`** (`ceres`)
11. **`Cinéma & Médias`** (`cine_analyst`)

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE STYLE & CAPSULES ("Google Fluid Blue + Compact Pills") :

1. CAPSULES HORIZONTALES COMPACTES (NotebookLM / Gemini Bar) :
   - Forme : rounded-full (border-radius: 9999px), padding: 6px 14px, display: flex, align-items: center.
   - Conteneur : rangée horizontale compacte avec overflow-x-auto pour éviter de prendre trop d'espace vertical.
```
