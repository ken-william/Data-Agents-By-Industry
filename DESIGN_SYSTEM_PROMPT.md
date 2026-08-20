# Master Specification & Prompt System - Talk to Data (Official Google Gemini AI Visual Design)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** fondé sur le manifeste officiel de Google Design : *"Illustrating the Gemini App: How dynamic cues help users discover, learn, and master our AI assistant’s evolving features"*.

---

# 🎨 1. Les 4 Piliers du Design Visuel Google Gemini AI

### 1. La Directionnalité des Dégradés & Momentum d'Énergie (Gradient Physics)
* **Vecteurs de Transfert d'Énergie** : Les dégradés possèdent un bord d'attaque net et lumineux qui se diffuse vers l'arrière-plan. Ils agissent comme un **pointeur visuel directionnel** canalisant l'énergie de l'utilisateur vers la barre de recherche et l'Orbe Live.
* **Le Sparkle & les 4 Couleurs Optimistes Google** : Référence directe aux 4 couleurs emblématiques de Google (Bleu `#4285F4`, Rouge `#EA4335`, Jaune `#FBBC05`, Vert `#34A853`) déclinées en dégradés dynamiques.

### 2. La Symbolique des Formes Circulaires (Foundational Circles)
* **Cercles, Puces et Formes Spheriques** : La géométrie du cercle transmet simplicité, harmonie et sérénité. Le logo Gemini lui-même est sculpté à partir de l'espace négatif de 4 cercles adjacents.
* **Boutons, Puces & Dock (`rounded-full` / `border-radius: 9999px`)** : Les capsules de scénarios (`md-menu-item` Material 3) et la barre de recherche adoptent des courbes circulaires ultra-douces.

### 3. Le Mouvement Intentionnel & Réactivité Active (Intentional Motion)
* **Mouvement comme Guide Visuel** : Chaque animation possède un point de départ et d'arrivée défini pour refléter les actions de l'utilisateur.
* **Reflet du Raisonnement IA** : La pulsation de l'Orbe et les halos lumineux (`search-bar-glow`) visualisent l'état de réflexion, d'écoute et de synthèse de Gemini.

### 4. La Douceur Éthérée & la Clarté (Embracing Softness)
* **Surfaces Floues et Spatialisées (`backdrop-blur`)** : Des surfaces dépolies et des lueurs adoucies créent un espace sécurisant et chaleureux, rendant l'IA immédiatement abordable et conviviale.

---

# 🖥️ 2. Spécification Technique Material 3 & Luminous UI

```css
body {
  font-family: "Google Sans Flex", "Google Sans", Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  color: rgb(31, 31, 31); /* #1F1F1F Noir adouci Google */
  background-color: #ffffff;
  background-image: radial-gradient(circle at 50% -20%, #eff6ff 0%, #ffffff 100%);
}

.greeting {
  font-size: 36px;
  font-weight: 400;
  color: #757575;
}

.search-bar-container {
  background-color: #f0f4f9;
  border-radius: 28px;
  padding: 12px 20px;
  font-size: 16px;
}

.bubble {
  height: 48px;
  padding: 0 12px;
  border-radius: 12px;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
```

---

# 🔊 3. Purification de la Synthèse Vocale Live (`sanitizeForSpeech`)

Toute réponse orale est filtrée par `sanitizeForSpeech()` pour exclure le code SQL, les objets JSON et la syntaxe Markdown, afin d'offrir une conversation naturelle en français.

---

# 📋 4. Master Specification & Prompt de Reconstitution (Prompt Maître)

```text
Tu me codes l'application web double écran "Talk to Data" connectée aux Vertex AI Data Agents selon le manifeste officiel Google Gemini AI Visual Design.

CONSIGNES STRICTES DE DESIGN :
1. Dégradés directionnels d'énergie et formes circulaires arrondies.
2. Interface épurée Material 3 Luminous (#1F1F1F texte, #F0F4F9 barre de recherche, #0B57D0 accent bleu).
3. Synthèse vocale live purifiée (résumé français naturel sans SQL ni JSON).
```
