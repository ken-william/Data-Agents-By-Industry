# Master Specification & Prompt System - Talk to Data (Google Fluid Blue Minimalist Landing Page)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** pour les événements B2B (BigData Paris 2026, Google Cloud Next).

---

# 🎨 1. Le Design System "Google Fluid Blue" (Minimalist Landing Page)

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
```

---

# 🖥️ 2. Architecture Double Écran & Landing Page Simplifiée

### Phase 1 : Landing Page Épurée Gemini (Page 1)
La première vue est entièrement centrée, aérée et minimale :
1. **Logo Sparkle Aurora & Titre Dégradé** : Logo Gemini + "Talk to Data" (dégradé bleu/rose) + "Let's get some work done!".
2. **Barre de Recherche Centrale & Bouton Rond Bleu** :
   - Champ de recherche avec halo lumineux radial (`search-bar-glow`).
   - Bouton rond bleu à droite de la barre pour lancer l'expérience Live (`Rocket` icon).
3. **Rangée de Capsules Scénarios (`ScenarioChips`)** :
   - Rangée horizontale de puces capsules compactes (`rounded-full`) servant de sélecteur d'agent direct.

### Phase 2 : Live Experience (Page 2 - Dual Screen)
- **ÉCRAN A (Showcase Public)** : Orbe Gemini Live à vagues physiques (Centre) + Data Canvas 70% largeur + SQLFlipCard 3D (Looker KPI vs SQL néon BigQuery).
- **ÉCRAN B (Contrôleur Tactile)** : Dock d'entrée fixe anti-bruit + Push-to-Talk + Smart Chips.

---

# 📋 3. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur Full-Stack Google Cloud et un Designer UX/UI d'exception.
Ta mission est de coder l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE DESIGN POUR LA LANDING PAGE (Phase 1) :

1. SUPPRESSION DU CATALOGUE EN BAS :
   - Supprime la grille des 11 cartes d'agents et le panneau latéral de connexion.
   - La sélection d'agent se fait exclusivement via les bulles de scénarios horizontales compactes (ScenarioChips).

2. COMPOSITION CENTRÉE ÉPURÉE :
   - Centrage vertical et horizontal complet de la page 1.
   - Logo Gemini Sparkle Aurora + Titre dégradé "Talk to Data" + "Let's get some work done!".
   - Barre de recherche avec halo lumineux et bouton rond bleu à droite pour déclencher l'expérience Live.
   - Rangée de capsules scénarios juste en-dessous.
```
