# Master Specification & Prompt System - Talk to Data (Vesper x Google Fluid Blue Hybrid Style)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), combinant la structure épurée et la physique de mouvement de **Vesper.ai** avec le design system **Google Fluid Blue** de Gemini et Gemini Live.

---

# 🌌 1. Palette Chromatique & Tokens (Google Fluid Blue)

| Token | Valeur | Rôle dans l'UI |
| :--- | :--- | :--- |
| `--bg` | `radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%)` | Fond de viewport sidéral anti-flash. |
| `--text` | `#f8fafc` (Slate 50) | Texte principal haute lisibilité. |
| `--muted` | `#94a3b8` (Slate 400) | Descriptions, légendes et métadonnées. |
| `--border` | `rgba(56, 189, 248, 0.16)` | Bordures actives des cartes et puces. |
| `--border-soft` | `rgba(99, 102, 241, 0.12)` | Délimiteurs et liserés de repos. |
| `--gemini-glow` | `rgba(56, 189, 248, 0.15)` | Halo de l'Orbe et de la barre de recherche. |
| `--gradient-active`| `linear-gradient(135deg, #38bdf8 0%, #3b82f6 50%, #6366f1 100%)` | Accent Gemini pour les boutons principaux. |

---

# 🔮 2. Effets "Liquid-Glass" & Reflet (Shine Sweep)

Les boutons et les capsules de scénarios utilisent un verre semi-transparent avec flou d'arrière-plan (`backdrop-filter: blur(16px)`), réhaussé par un effet de balayage lumineux (*shine transition*) au survol.

```css
.btn-glass {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 44px;
  padding: 0 18px;
  border-radius: 9999px;
  font-size: 14px;
  font-weight: 500;
  color: #ffffff;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(15, 23, 42, 0.45) 50%, rgba(99, 102, 241, 0.05));
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.btn-glass::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(115deg, transparent 20%, rgba(255, 255, 255, 0.25) 48%, transparent 76%);
  transform: translateX(-130%);
  transition: transform 0.65s ease;
  z-index: -1;
}

.btn-glass:hover::after {
  transform: translateX(130%);
}

.btn-glass:hover {
  border-color: rgba(56, 189, 248, 0.6);
  box-shadow: 0 0 20px rgba(56, 189, 248, 0.25);
}
```

---

# 🔊 3. Purification Vocale Live (`sanitizeForSpeech`)

Toute réponse audio passe par `sanitizeForSpeech()` pour garantir qu'aucun code SQL, JSON brut ou symbole Markdown ne soit lu à haute voix.

---

# 📋 4. Prompt Système de Reconstitution Maître

```text
Tu es Antigravity, un développeur UI senior chez Google Cloud.
Ta mission est de construire l'application web double écran "Talk to Data" en combinant la structure Vesper.ai (single-viewport bloqué, grain et lueurs) et le design system Google Fluid Blue (dégradés bleus profonds, verre liquid-glass, et Orbe Gemini Live central interactif).

CONSIGNES STRICTES :
1. FOND SIDÉRAL : radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%).
2. LIQUID-GLASS : Boutons et puces avec flou de 16px, bordures semi-transparentes et effet de brillance (shine) glissant au survol.
3. TYPOGRAPHIE : Police Inter avec mise en valeur en italique Instrument Serif pour "Data".
4. VOCAL PURIFIÉ : Seul le résumé français naturel est lu par la synthèse vocale.
```
