# Master Specification & Prompt System - Talk to Data (Google Fluid Blue + Extension Chips)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** pour les événements B2B (BigData Paris 2026, Google Cloud Next).

---

# 🎨 1. Le Design System "Google Fluid Blue" (CSS Variables & Chips)

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
  --radius-pill: 16px;
  --glow-active: 0 0 25px rgba(56, 189, 248, 0.15);
}

/* Extension Chips (Bulles de Scénarios Gemini) */
.extension-chips-container {
  display: flex;
  gap: 8px;
  margin-top: 16px;
  flex-wrap: wrap;
  justify-content: center;
}

.chip {
  display: flex;
  align-items: center;
  padding: 6px 12px;
  background-color: rgba(15, 23, 42, 0.45);
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.chip.active {
  background-color: rgba(56, 189, 248, 0.1);
  border-color: rgba(56, 189, 248, 0.45);
  box-shadow: 0 0 12px rgba(56, 189, 248, 0.15);
}

.chip:hover {
  background-color: rgba(30, 41, 59, 0.7);
  border-color: rgba(56, 189, 248, 0.3);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
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
|  - Orbe Gemini Live & Vagues Wave-1/2/3 (Centre)   |  - Extension Chips (Bulles 11 Scénarios)      |
|  - Visualisation des Données (70% Largeur)         |  - Barre de Saisie Hybride Fixe (Bas d'écran)  |
|  - SQLFlipCard Recto/Verso (Looker vs Neon SQL)    |  - Push-to-Talk Mic + Smart Chips anti-bruit   |
|  - KPI Scores & Graphiques Épurés                  |  - Console de Log & Switcher Écran A/B        |
+------------------------------------------------------------------------------------------------+
```

---

# 🛠️ 3. Les 11 Bulles de Scénarios Sectoriels (Chips)

| Agent ID | Intitulé Bulle | Question Type d'Activation |
| :--- | :--- | :--- |
| **sully** | RH & Emploi Public | Affiche la vacance des postes hospitaliers |
| **credit_advisor** | Risque Crédit | Analyse le scoring de faillite IFRS 9 pour ce trimestre |
| **net_arch** | Télécoms & Réseaux | Fais un diagnostic de la QoS réseau sur la zone Sud-Ouest |
| **earth_intel** | Spatial & Satellite | Calcule l'indice de santé chlorophyllienne NDVI du secteur |
| **transit_navigator** | Transports & Logistique | Quelles sont les lignes SNCF ayant subi le plus de retards ? |
| **pulse_checker** | Santé & Hôpitaux | Affiche le taux de rupture des stocks de médicaments |
| **shelf_optimizer** | CPG Retail | Liste des produits en rupture en rayon Frais à 14 jours |
| **arena_manager** | Sport & Stades | Analyse le panier moyen des spectateurs en loge VIP |
| **helios** | Énergie & Bornes | Quelles sont les bornes de recharge IRVE surchargées ? |
| **ceres** | Agriculture & Carbone | Quel est le bilan carbone ACV ADEME pour l'exploitation ? |
| **cine_analyst** | Cinéma & Médias | Calcule la part de marché des cinémas par format immersif |

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE STYLE & STRUCTURE ("Google Fluid Blue + Extension Chips") :

1. PALETTE CHROMATIQUE & BULLES DE SCÉNARIOS :
   - Conteneur de puces : flex-wrap, padding: 6px 12px, border-radius: 16px, background-color: rgba(15, 23, 42, 0.45).
   - Effet hover/active : background-color: rgba(56, 189, 248, 0.1), border-color: rgba(56, 189, 248, 0.45), lueur cyan.

2. ARCHITECTURE D'ÉCRAN DOUBLE :
   - Écran A (Showcase / Public) : Orbe Gemini Live géant avec vagues wave-1/2/3, Data Canvas 70% largeur avec graphiques style Looker et carte 3D SQLFlipCard.
   - Écran B (Contrôleur Tactile) : Extension Chips Container avec les 11 bulles sectorielles, barre de saisie hybride fixe en bas d'écran avec bouton Push-to-Talk.
```
