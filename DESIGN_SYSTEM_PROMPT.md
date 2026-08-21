# Master Specification & Prompt System - Talk to Data (Google Fluid Blue Master Specification)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée d'après l'architecture **Google Fluid Blue** avec Orbe Vivant à physique des mouvements, Flip Card 3D SQL et fond radial bleu nuit sidéral.

---

# 🎨 1. Palette Chromatique & Tokens (Google Fluid Blue)

| Token CSS | Valeur Hexadécimale / Gradient | Rôle dans l'UI |
| :--- | :--- | :--- |
| **`--bg`** | `radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%)` | Fond de viewport anti-flash blanc. |
| **`--text`** | `#F8FAFC` (Slate 50) | Texte principal haute lisibilité. |
| **`--muted`** | `#94A3B8` (Slate 400) | Sous-titres et métadonnées secondaires. |
| **`--cyan-glow`** | `#38BDF8` (Sky 400) | Lueur supérieure de la barre de recherche et accents néon. |
| **`--blue-vivid`** | `#2563EB` (Blue 600) | Accentuation des icônes et états actifs. |
| **`--emerald-wave`** | `#10B981` (Emerald 500) | Ondes de choc circulaires vocales de l'assistant. |

```css
html, body {
  background: radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%) !important;
  color: #F8FAFC;
  font-family: "Google Sans Flex", "Google Sans", "Inter", sans-serif;
  min-height: 100dvh;
}
```

---

# 🖥️ 2. Page 1 : Portail d'Accueil Gemini Enterprise

1. **Zone Centrale** : Message d'accueil en dégradé pastel fluide, surmonté du logo étincelant Gemini Sparkle.
2. **Barre de Recherche Iconique** : Forme capsule `rounded-full` avec lueur supérieure diffuse cyan (`.search-bar-glow`).
3. **Capsules de Scénarios (11 Pills)** : Puces arrondies compactes aux icônes monochromes s'illuminant au survol.

---

# 🎙️ 3. Page 2 : Espace d'Interaction et d'Analyse (LiveCanvas)

1. **Canvas de Données (Showcase Public)** : Cartes en verre dépoli aux bordures translucides fines et chiffres géants.
2. **Effet de Rotation 3D (SQL Flip Card)** : Carte de données qui pivote à 180° pour afficher les lignes SQL néon au verso.
3. **Orbe Conversationnel Organique (`GeminiOrb`)** :
   * *Écoute* : Vagues de fréquences souples au rythme de la voix de l'utilisateur.
   * *Réflexion* : Anneau multicolore tourbillonnant.
   * *Parole* : Ondes de choc circulaires émeraude & cyan au rythme de l'assistant.

---

# 📋 4. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" selon la spécification Google Fluid Blue.

CONSIGNES STRICTES :
1. FOND DEGRADÉ RADIAL BLEU NUIT : radial-gradient(circle at 50% 30%, #070f2b 0%, #020617 70%, #000000 100%).
2. BARRE DE RECHERCHE GEMINI : Forme capsule avec lueur supérieure diffuse cyan (search-bar-glow).
3. ORBE CONVERSATIONNEL A PHYSIQUE DES ONDES : 3 états (vagues d'écoute, anneau de réflexion, ondes de choc émeraude/cyan de parole).
4. FLIP CARD 3D SQL : Pivotement 3D à 180° de la carte de données pour afficher le SQL néon.
```
