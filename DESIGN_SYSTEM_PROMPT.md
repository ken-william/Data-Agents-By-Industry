# Master Specification & Prompt System - Talk to Data (Apple x Emil Kowalski Specification)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour intégrer les principes de purification visuelle et de micro-interactions fluides inspirés du design **Apple** et d'**Emil Kowalski** (Framer Motion spring physics & Shared Layout Morphing).

---

# 🎨 1. Architecture Visuelle Purifiée (Page 2 Layout 70% / 30%)

| Zone / Composant | Composition Visuelle & Comportement |
| :--- | :--- |
| **70% Gauche / Centre (Data Visual Bento Card)** | Panneau central unique en verre dépoli (`rounded-[36px] bg-white/85 backdrop-blur-3xl`). Affiche uniquement la synthèse d'affaires nettoyée et les tableaux Markdown épurés. **Aucun log technique ou JSON brut**. |
| **Bouton d'Inspection Discret `[⚡ Inspecter le SQL]`** | Bouton subtil situé en haut à droite. Déclenche une rotation 3D Apple (`SQLFlipCard`) pour faire pivoter la carte et révéler la requête SQL en néon phosphorescent sous le capot. |
| **30% Droite (L'Agent Compagnon Hôte & Slime Orb)** | L'Orbe Slime 3D Gemini Live en lévitation gravitationnelle fluide (`framer-motion` spring physics) avec sa bulle de storytelling sous l'orbe. |
| **Orbe Slime 3D Gemini Live** | Pure sphère de lumière liquide en fusion (**aucun icône de micro à l'intérieur**). Dégradés chromatiques en mouvement continu (Perlin noise mesh). |
| **Puces de Suggestion Spacieuses** | Capsules aérées flottantes inspirées de Gemini Enterprise (`gap-4`, `padding: 12px 24px`). |

---

# 📋 2. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" avec la refonte visuelle Apple x Emil Kowalski (Purification & Mouvement Fluide).

CONSIGNES STRICTES :
1. LAYOUT 70%/30% PAGE 2 : 70% Bento Card de données unique en verre dépoli, 30% Compagnon Hôte & Orbe Slime 3D.
2. BOUTON DISCRET [⚡ Inspecter le SQL] : Pivote la carte en 3D (Rotation Apple 180deg) pour inspecter le SQL néon.
3. ORBE SLIME SANS MICRO : Sphère liquide 3D avec lévitation gravitationnelle et physique de ressorts framer-motion.
4. SPEECH SANITIZER : Intercepte les JSON bruts et génère une prose d'affaires naturelle en français.
```
