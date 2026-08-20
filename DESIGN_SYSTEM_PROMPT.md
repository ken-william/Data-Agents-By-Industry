# Master Specification & Prompt System - Talk to Data (Google Fluid Blue Aurora)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** pour les événements B2B (BigData Paris 2026, Google Cloud Next).

---

# 🎨 1. Le Design System "Google Fluid Blue Aurora" (CSS Mesh Gradient & Frosted Glass)

```css
:root {
  /* Palette Chromatique - Google Fluid Blue Aurora */
  --bento-bg: rgba(15, 23, 42, 0.55);
  --bento-border: rgba(51, 65, 85, 0.6);
  --bento-border-active: rgba(56, 189, 248, 0.7);
  --gemini-gradient: linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #6366f1 100%);
  
  /* Typographie Google Flex */
  --font-family-google: "Google Sans Flex", "Google Sans", "Inter", sans-serif;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;

  /* Formes et Animations */
  --radius-card: 16px;
  --radius-pill: 9999px;
  --glow-active: 0 0 25px rgba(56, 189, 248, 0.2);
}

/* Animation Mesh Gradient Ultra-Lisse (Aucune ligne de coupure) */
@keyframes aurora-mesh {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

.google-aurora-bg {
  background: linear-gradient(-45deg, #020617, #070F2B, #0F172A, #1E1B4B, #0A192F);
  background-size: 400% 400%;
  animation: aurora-mesh 18s ease infinite;
}
```

---

# 🖥️ 2. Header Épuré & Configuration Écran A / B via Paramètres

### Header Minimaliste sans Boutons d'Écran
Le Header ne contient plus les boutons de basculement Écran A / Écran B :
- Logo + Titre "Talk to Data | BigData Paris 2026".
- Bouton Synthèse Vocale (Voix Active / Muette).
- Bouton Paramètres (Roue Crantée `Settings`).

### Configuration Écran A / Écran B dans le Tiroir Settings
Le choix de l'écran se fait exclusivement dans le panneau **Paramètres** (`SettingsDrawer.jsx`) :
- **Bouton Écran A : Showcase (Grand Écran)** : Bascule la fenêtre courante sur le mode Showcase avec l'Orbe Gemini Live géant et le Data Canvas 70%.
- **Bouton Écran B : Contrôleur Tactile (PC / Tablette)** : Bascule la fenêtre sur la vue console présentateur.
- **Lien Ouvrir dans un nouvel onglet** (`?screen=showcase` ou `?screen=controller`) pour attribuer un écran physique distinct à chaque moniteur.

---

# 🛠️ 3. Navigation par Flèches sur les Capsules Scénarios (`ScenarioChips`)

Le composant `ScenarioChips` intègre des boutons de défilement gauche et droite (`ChevronLeft`, `ChevronRight`) survolants et cliquables pour faire défiler de manière fluide l'ensemble des 11 capsules d'agents sur tous les types d'écrans.

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE DESIGN DE FINITION :

1. ARRIÈRE-PLAN ANIMÉ AURORA SMOOTH :
   - Supprime tout radial-gradient créant une ligne visible au milieu.
   - Utilise un dégradé animé linéaire multi-couches fluide (linear-gradient(-45deg, #020617, #070F2B, #0F172A, #1E1B4B, #0A192F)) avec animation mesh 18s.

2. HEADER & CONFIGURATION DES ÉCRANS :
   - Supprime les boutons Écran A / Écran B du Header.
   - Intègre la sélection d'écran (Écran A Showcase / Écran B Contrôleur) et le lien "Ouvrir dans un nouvel onglet" uniquement dans le panneau Paramètres (SettingsDrawer).

3. SCROLL FLUIDE SUR LES CAPSULES :
   - Ajoute des flèches de défilement gauche et droite sur la barre de puces capsules d'agents.
```
