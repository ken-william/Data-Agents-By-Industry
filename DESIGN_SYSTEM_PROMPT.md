# Master Specification & Prompt System - Talk to Data (Google Deep Blue Gradient System)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour appliquer fidèlement l'arrière-plan dégradé bleu profond d'après la référence visuelle (`media_1787312920884.png`).

---

# 🎨 1. Palette & Arrière-plan "Google Deep Blue"

| Étape du Dégradé | Code Hexadécimal | Rôle dans l'UI |
| :--- | :--- | :--- |
| **Bleu Ciel Lumineux (Haut-Gauche)** | `#38BDF8` | Touche de lumière angulaire. |
| **Bleu Google Royal (Milieu)** | `#2563EB` | Cœur vibrant de l'arrière-plan. |
| **Bleu Saphir Profond (Centre)** | `#1D4ED8` | Profondeur et transition visuelle. |
| **Bleu Nuit Sidéral (Bas-Droit)** | `#030712` | Ancrage sombre et contraste élevé. |

```css
body {
  background: linear-gradient(135deg, #38bdf8 0%, #2563eb 35%, #1d4ed8 70%, #030712 100%) !important;
  color: #FFFFFF;
  font-family: "Google Sans Flex", "Google Sans", "Inter", sans-serif;
  min-height: 100dvh;
}
```

---

# 🔮 2. Composants & Contrastes Verre Dépoli

- **Navbar Flottante** : Verre dépoli translucide `bg-white/15 border-b border-white/20 backdrop-blur-2xl text-white`.
- **Cartes & Conteneurs** : Verre dépoli blanc argenté `bg-white/95 text-slate-900 rounded-3xl p-6 shadow-2xl border border-white/80`.
- **Boutons d'Action** : Boutons capsules noirs ou bleus vibrants avec surbrillance au survol.

---

# 📋 3. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" avec l'arrière-plan dégradé Google Deep Blue (media_1787312920884.png).

CONSIGNES STRICTES :
1. FOND GOOGLE DEEP BLUE DEGRADÉ : linear-gradient(135deg, #38bdf8 0%, #2563eb 35%, #1d4ed8 70%, #030712 100%).
2. NAVBAR VERRE TRANSLUCIDE : bg-white/15, backdrop-blur-2xl, text-white.
3. CARTES VERRE DÉPOLI : bg-white/95, rounded-3xl, shadow-2xl.
```
