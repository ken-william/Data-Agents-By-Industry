# Master Specification & Prompt System - Talk to Data (Master AI Host & Speech Sanitizer)

Ce document constitue la **Spécification Maître Complète** de la plateforme **"Talk to Data"** (BigData Paris 2026), rédigée pour orchestrer l'Agent Hôte Virtuel ("Maître de Jeu"), le filtre de nettoyage vocal (**Speech Sanitizer**), le storytelling actif durant l'exécution BigQuery, et le contrôle hybride voix/tactile (**Gemini Live Always-On**).

---

# 🎭 1. Fonctionnalités de l'Agent Hôte & Sanitizer

| Module | Rôle & Comportement Système |
| :--- | :--- |
| **Speech Sanitizer (Filtre Vocal)** | Intercepte toutes les réponses brutes de Conversational Analytics. **Élimine totalement les JSON, accolades, requêtes SQL, identifiants GCP et balises Markdown à la synthèse vocale (TTS)**. |
| **Storytelling Actif (Attente BQ)** | Durant les 2 à 3 secondes d'exécution de requêtes BigQuery, l'Hôte meuble l'attente à voix haute : *"Je consulte à l'instant vos tables BigQuery... Synthèse immédiate des métriques clés."* |
| **Contrôle Vocale Continu (Gemini Live)** | L'orbe écoute en continu (mode Always-On) dès l'arrivée sur l'écran. |
| **Bouton Mute & Secours Tactile** | Un clic sur le bouton Mute permet de couper le micro en environnement bruyant et de piloter l'interface via les puces de suggestion ou le clavier. |

---

# 📋 2. Prompt Système de Reconstitution Maître

```text
Tu me codes l'application web double écran "Talk to Data" avec l'Agent Hôte Traducteur, le Speech Sanitizer vocal et l'écoute continue Gemini Live.

CONSIGNES STRICTES :
1. SPEECH SANITATION STRICTE : Aucun JSON, code SQL, ou timestamp ne doit être lu par la synthèse vocale TTS.
2. STORYTELLING PENDANT L'ATTENTE : Pendant le chargement BigQuery (2-3s), l'Agent Hôte émet un message de storytelling à voix haute.
3. ÉCOUTE CONTINU ALWAYS-ON : Activation automatique du micro en continu avec bouton Mute de secours.
```
