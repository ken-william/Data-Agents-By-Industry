# Master Specification & Prompt System - Talk to Data (Google Material 3 / Gemini Luminous Visual Design)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"** selon le Design System officiel **Google Material 3 / Gemini Luminous**.

---

# 🎨 1. Le Design System "Google Material 3 / Gemini Luminous"

### Palette Chromatique Officielle Google Material 3

| Usage | Code Hexadécimal / RGB | Description Visuelle |
| :--- | :--- | :--- |
| **Fond Principal** | `#FFFFFF` + `radial-gradient` | Blanc pur avec dégradé radial subtil de profondeur `radial-gradient(circle at 50% -20%, #eff6ff 0%, #ffffff 100%)`. |
| **Texte Principal** | `#1F1F1F` / `rgb(31,31,31)` | Noir adouci "Google" pour une lisibilité parfaite. |
| **Texte Secondaire** | `#757575` / `rgb(117,117,117)` | Gris neutre pour les métadonnées et sous-titres. |
| **Fond Barre de Recherche** | `#F0F4F9` | Bleu-gris très clair caractéristique de Gemini / Bard. |
| **Accent Bleu Google** | `#0B57D0` | Bleu Material 3 officiel pour les boutons et actions. |
| **Lueur de Recherche (Glow)** | `radial-gradient(100% 100% at 50% 8%, #ffffff 0%, #9dd2ff 50%)` | Halo lumineux filtré à `blur(15px); opacity: 0.5;`. |
| **Ombre Douce** | `0 1px 3px rgba(0,0,0,0.1)` | Ombre discrète et élégante. |

### Typographie Google Sans Flex

```css
body {
  font-family: "Google Sans Flex", "Google Sans", Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  color: rgb(31, 31, 31);
}
```

* **Titres (Greeting)** : `36px`, `font-weight: 400` (Regular Flex)
* **Bulles / Scénarios** : `14px`, `font-weight: 500` (Medium)
* **Barre de recherche** : `16px`, `font-weight: 400`

---

# 🛠️ 2. Le Style des Bulles (Material 3 `md-menu-item`)

```css
.bubble {
  display: flex;
  align-items: center;
  padding: 0 12px;
  height: 48px;
  gap: 12px;
  background: #ffffff;
  border-radius: 12px;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.bubble:hover {
  background-color: rgba(31, 31, 31, 0.08);
}
```

---

# 🔊 3. Synthèse Vocale Live Purifiée (`sanitizeForSpeech`)

Toute réponse audio passe par `sanitizeForSpeech()` pour garantir qu'aucun code SQL, JSON brut ou symbole Markdown ne soit lu à haute voix.

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu me codes l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents.

CONSIGNES STRICTES DE DESIGN (Google Material 3 / Gemini Luminous) :

1. COULEURS & TYPOGRAPHIE :
   - Police : "Google Sans Flex", "Google Sans", Roboto, sans-serif avec -webkit-font-smoothing: antialiased.
   - Texte principal : #1F1F1F (Noir adouci Google).
   - Fond global : #FFFFFF avec radial-gradient(circle at 50% -20%, #eff6ff 0%, #ffffff 100%).
   - Barre de recherche : #F0F4F9 avec accent bleu Google #0B57D0 et halo lumineux.
   - Bulles de scénarios : md-menu-item Material 3 (height: 48px, padding: 0 12px, border-radius: 12px).
```
