# Master Specification & Prompt System - Talk to Data (Pure Black Spectral Cosmic Space Design)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), repensée selon un style **Pure Black Spectral Cosmic Space** avec formes Googley fluo animées dans l'espace.

---

# 🌌 1. Tokens & Design System "Pure Black Spectral Space"

| Token | Valeur | Usage dans l'UI |
| :--- | :--- | :--- |
| `--bg` | `#000000` (Noir Absolu) | Fond de viewport noir pur anti-flash. |
| `--text` | `#F8FAFC` (Slate 50) | Texte principal haute lisibilité. |
| `--muted` | `#94A3B8` (Slate 400) | Sous-titres et légendes. |
| `--fluo-cyan` | `#38BDF8` | Accent fluo principal et lueurs. |
| `--fluo-purple` | `#C084FC` | Gradient secondaire et Orbe. |
| `--fluo-amber` | `#FBBC05` | Touche de couleur Google. |

---

# 🔮 2. Animations Spectrales Googley (Cosmic Spectral Orbs)

Formes organiques flottantes aux couleurs Google (Bleu Ciel `#38BDF8`, Violet `#818CF8`, Rose `#EC4899`, Jaune `#FBBC05`) qui bougent doucement en arrière-plan comme des nébuleuses cosmiques.

```css
@keyframes floatSpectral {
  0%, 100% {
    transform: translate(0px, 0px) scale(1);
    opacity: 0.25;
  }
  50% {
    transform: translate(60px, -40px) scale(1.15);
    opacity: 0.45;
  }
}

.spectral-orb {
  position: fixed;
  border-radius: 9999px;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
  animation: floatSpectral 18s ease-in-out infinite alternate;
}
```

---

# 💊 3. Bulles Scénarios Agrandies (Large Fluo Capsules)

Les bulles de scénarios sont agrandies pour une lisibilité optimale sur grand écran et PC de contrôle :
- `height: 52px; padding: 0 22px; gap: 12px; border-radius: 9999px;`
- Texte clair `font-size: 15px; font-weight: 600;`
- Icône lumineuse `20px`

---

# 🗑️ 4. Éléments Supprimés (Deletions)

- ❌ Supprimé : Le footer des 3 statistiques (`4.2M+ workflows automated`, etc.).
- ❌ Supprimé : Les boutons "Start for Free" et "See it in action".
- ❌ Supprimé : Le badge discret "Copilote Sélectionné : ArenaManager".
- ❌ Supprimé : Les tags informatiques du Header (`data-agents-by-industry`, `Copilotes Sectoriels (11)`).

---

# 📋 5. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" selon le style Pure Black Spectral Cosmic Space.

CONSIGNES STRICTES :
1. FOND NOIR ABSOLU #000000 avec formes spectrales Googley animées fluo.
2. TYPOGRAPHIE : Inter + Instrument Serif en italique avec dégradés de texte.
3. HEADER FLUO GLASS : Barre flottante dépolie en verre fluo.
4. BULLES SCÉNARIOS AGRANDIES : Capsules fluo de 52px de hauteur avec texte clair et défilement horizontal.
5. AUCUN FOOTER DE STATS NI BOUTONS INUTILES.
```
