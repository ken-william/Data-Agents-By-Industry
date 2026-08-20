# Master Specification & Prompt System - Talk to Data (Official Vesper.ai Operational AI Infrastructure Style)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée selon l'architecture et le design system exacts de **Vesper.ai — Operational AI Infrastructure**.

---

# 🌌 1. Tokens & Design System Vesper.ai

| Token | Valeur | Usage dans l'UI |
| :--- | :--- | :--- |
| `--bg` | `#000000` / `radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%)` | Fond de viewport sidéral anti-flash. |
| `--text` | `#ffffff` | Texte principal haute lisibilité. |
| `--muted` | `#9a9a9a` (Slate 400) | Descriptions, légendes et métadonnées. |
| `--stat` | `#d8d8d8` | Valeurs et libellés des statistiques. |
| `--border` | `rgba(255, 255, 255, 0.16)` | Bordures nettes des cartes et boutons. |
| `--border-soft` | `rgba(255, 255, 255, 0.12)` | Délimiteurs et liserés de repos. |

---

# 🎨 2. Typographie & Piles de Polices (Exact)

- **UI / Logo / Nav / Boutons / Badge / Lede / Stats** : `"Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`
- **Mots d'Accent du H1 (*AI agents*)** : `"Instrument Serif", "Times New Roman", Times, serif` (Italique)

```css
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@1&family=Inter:wght@400;500;600;700&display=swap');

body {
  font-family: "Inter", sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: #000000;
  color: #ffffff;
}

h1 em {
  font-family: "Instrument Serif", serif;
  font-style: italic;
  font-weight: 400;
  color: #9a9a9a;
}
```

---

# 🔮 3. Boutons & Puces Liquid-Metal / Liquid-Glass

### Boutons Liquid-Metal Nav (`.btn-nav`)
- `height: 40px; padding: 0 18px; border-radius: 7px;`
- `border: 1px solid rgba(198,198,198,0.55);`
- `background: linear-gradient(105deg, #050505 0%, #2a2a2a 48%, #4a4a4a 100%);`
- Reflet `::before` qui glisse au survol (`translateX(-120%)` ➔ `translateX(120%)`).

### Boutons Liquid-Glass (`.btn-glass` / `.btn-solid`)
- `position: relative; isolation: isolate; overflow: hidden; height: 42px; border-radius: 6px;`
- Reflet `::after` en balayage `linear-gradient(115deg, transparent 20%, rgba(255,255,255,0.45) 48%, transparent 76%)`.

---

# 📊 4. Pied de Page Statistiques (Stats Footer)

1. `4.2M+ workflows automated` (Icone workflow dual-pill)
2. `92% reduction in manual operations` (Icone carre arrondi blanc avec fleche)
3. `180+ operational teams onboarded` (Icone 3 avatars)

---

# 🔊 5. Purification Vocale Live (`sanitizeForSpeech`)

Toute réponse audio passe par `sanitizeForSpeech()` pour garantir qu'aucun code SQL, JSON brut ou symbole Markdown ne soit lu à haute voix.

---

# 📋 6. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu es Antigravity, un développeur UI senior chez Google Cloud.
Ta mission est de construire l'application web double écran "Talk to Data" selon le design exact Vesper.ai — Operational AI Infrastructure.

CONSIGNES STRICTES DE DESIGN :
1. FOND BLACK ANTI-FLASH : html, body { background: #000000 !important; color: #ffffff; }.
2. TYPOGRAPHIE : Inter pour tout l'UI et Instrument Serif en italique pour les mots clés h1 em.
3. BOUTONS LIQUID-METAL & LIQUID-GLASS : Effet de balayage lumineux (shine sweep) au survol.
4. FOOTER STATS : 3 métriques clés avec icônes SVG custom.
```
