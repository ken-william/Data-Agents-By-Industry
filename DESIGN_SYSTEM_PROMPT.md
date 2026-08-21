# Master Specification & Prompt System - Talk to Data (BQ CA Response Formatter & Speech Sanitizer)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour s'assurer que les réponses de BigQuery Conversational Analytics (BQ CA) sont intégralement converties en **tableaux Markdown élégants** et **synthèses d'affaires humaines**, en éliminant tous les blocs JSON bruts et messages systèmes bruts.

---

# 📊 1. Formratage Intelligent des Réponses BQ CA

| Type de Message BQ CA | Traitement Ancien (Aggressif) | Nouveau Formratage Intelligible |
| :--- | :--- | :--- |
| **`result.data` (Lignes de Données)** | Chaîne JSON brute `{"result": {"data": [...]}}`. | **Tableau Markdown Épuré** avec colonnes formatées et lignes lisibles. |
| **`matchedQuery.sqlQuery`** | Affiché en texte brut dans la bulle de chat. | Extrait comme **Pensée/SQL pour la FlipCard 3D**. |
| **`FOLLOWUP_QUESTIONS`** | Affiché en JSON brut. | Converti en **Puces de Suggestions interactives**. |
| **`datasources` / `bigQueryJob`** | Message système brut affiché à l'écran. | Filtré et masqué de la vue principale. |

---

# 📋 2. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" avec un formateur de réponses BQ CA humain et interactif.

CONSIGNES STRICTES :
1. PARSER BQ CA INTELIGENT : Transforme systemMessage.data.result en tableau Markdown élégant.
2. PAS DE JSON BRUT DANS LE CHAT : Élimine totalement les timestamps et structures JSON brutes.
3. EXTRACTEUR SQL : Envoie matchedQuery.sqlQuery dans les thoughts pour la FlipCard 3D.
```
