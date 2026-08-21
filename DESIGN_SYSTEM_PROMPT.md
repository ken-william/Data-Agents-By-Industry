# Master Specification & Prompt System - Talk to Data (Google Light Colored Theme & Google Sans Typography)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée selon le design system **Google Light Colored Theme** avec polices exclusives Google Sans.

---

# 🎨 1. Palette Chromatique "Google Light Colored Theme"

| Élément UI | Spécification Visuelle |
| :--- | :--- |
| **Fond Global** | Fond clair coloré officiel Gemini (`radial-gradient(circle at 50% 45%, #E2F0FD 0%, #F4F8FD 50%, #FFFFFF 90%)`). |
| **Typographies Exclusives Google** | `font-family: "Google Sans Flex", "Google Sans", "Product Sans", Roboto, sans-serif;` |
| **Navbar Verre Translucide** | `background: rgba(255, 255, 255, 0.75); border-bottom: 1px solid rgba(226, 232, 240, 0.8); backdrop-filter: blur(24px);` |
| **Puces d'Agents Auto-Adaptatives** | `width: auto; shrink: 0; padding: 0 20px; height: 48px; border-radius: 9999px;` (S'adapte automatiquement à la longueur du texte). |

```css
body {
  font-family: "Google Sans Flex", "Google Sans", Roboto, sans-serif;
  background: radial-gradient(circle at 50% 45%, #E2F0FD 0%, #F4F8FD 50%, #FFFFFF 90%) !important;
  color: #1F1F1F;
}
```

---

# 📝 2. Accroche et Typographie Hero

- **Titre Principal H1** : *"Talk to Data live using conversational AI agents."*
- **Sous-titre H2** : *"Interagissez en langage naturel avec 11 copilotes décisionnels sectoriels directement connectés à vos tables BigQuery."*

---

# 📋 3. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" avec le thème Google Light Coloré et les polices Google Sans.

CONSIGNES STRICTES :
1. POLICES EXCLUSIVEMENT GOOGLE : Google Sans Flex, Google Sans, Roboto.
2. BOUTONS AUTO-ADAPTATIFS : Les puces d'agents ont une largeur automatique (width: auto) qui s'adapte à la taille du texte.
3. FOND CLAIR COLORÉ GEMINI : radial-gradient(circle at 50% 45%, #E2F0FD 0%, #F4F8FD 50%, #FFFFFF 90%).
4. ACCROCHE HERO : "Talk to Data live using conversational AI agents. Interagissez en langage naturel avec 11 copilotes décisionnels sectoriels directement connectés à vos tables BigQuery."
```
