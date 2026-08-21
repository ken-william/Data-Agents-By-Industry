# Master Specification & Prompt System - Talk to Data Live V2 (Gemini Live & Zero-Chat Scroll Architecture)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data Live V2"** (BigData Paris 2026), rédigée pour implémenter l'expérience **Gemini Live**, l'affichage à **État Unique Zero-Chat Scroll**, le **Storytelling pendant les requêtes BigQuery** et la **Purification Vocale Speech-Sanitized**.

---

# 🚀 1. Architecture Visuelle & Principes Directeurs V2

| Module Visuel | Ancienne Approche (V1) | Nouvelle Approche (V2 Gemini Live) |
| :--- | :--- | :--- |
| **Canvas de Restitution** | Historique de chat scrollable vertical accumulant les messages. | **Zero-Chat Scroll (État Unique)** : Affichage exclusif de la question active et du rapport actif avec transition fondue (`fade-in/fade-out`). |
| **Interaction Vocale** | Bouton micro Push-to-Talk (cliquer pour parler). | **Flux Vocal Continu Always-On Gemini Live** avec Orbe Live Chroma à réfraction 4 couleurs. |
| **Temps de Réflexion** | Simple spinner de chargement silencieux. | **Storytelling Narratif Actif** : L'Agent Hôte meuble les 2 secondes d'attente BigQuery avec un schéma lumineux de jointure de tables. |
| **Purification Vocale** | Synthèse vocale risquant de lire le Markdown/SQL. | **Speech-Sanitized Engine** : Filtrage strict éliminant le JSON, les tables Markdown, et les symboles bruts. |

---

# 🖥️ 2. Double-Screen Architecture V2

```
+----------------------------------------------------------------------------------------------------+
|                                  TALK TO DATA LIVE V2 ARCHITECTURE                                 |
+----------------------------------------------------------------------------------------------------+
|  ÉCRAN A (SHOWCASE PUBLIC - GRAND ÉCRAN)             |  ÉCRAN B (TACTILE - CONTRÔLEUR PC)            |
|  - Canvas Actif à État Unique (Zero-Chat Scroll).    |  - Orbe Gemini Live Always-On Audio.          |
|  - Fondu-croisé élégant à chaque nouvelle question.  |  - 11 Floating Scenario Chips ultra-aérés.    |
|  - Schéma lumineux de jointures SQL BigQuery.       |  - Suggestions de secours tactiles instantanées.|
|  - FlipCard 3D SQL phosphorescente sur verre.       |  - Console de diagnostic BigQuery miniature.  |
+----------------------------------------------------------------------------------------------------+
```

---

# 📋 3. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data Live V2" selon l'architecture Gemini Live & Zero-Chat Scroll.

CONSIGNES STRICTES :
1. ZERO-CHAT SCROLL : Élimine le défilement de type chat. Seules la question active et la réponse active s'affichent à tout moment.
2. FLUX VOCAL CONTINU GEMINI LIVE : Orbe Chroma Always-On réagissant à la voix sans besoin de cliquer.
3. STORYTELLING PENDANT LES REQUÊTES : Schéma interactif de jointure de tables BigQuery pendant les 2 secondes d'exécution.
4. SPEECH-SANITIZED VOCAL ENGINE : Purification orale éliminant le JSON, le SQL et le Markdown.
```
