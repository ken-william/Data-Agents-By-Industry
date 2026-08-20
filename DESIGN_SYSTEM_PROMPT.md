# Master Specification & Prompt System - Talk to Data (AI Quick Builder)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"**. Il peut servir de cahier des charges, de prompt de reconstruction pour une IA, ou de guide de personnalisation pour ajuster l'application à vos attentes exactes.

---

## 1. Vision Globale & Concept "AI Quick Builder"

### 🎯 Objectif Métier & Événementiel
**Talk to Data** est une application web décisionnelle multi-agents déployée sur **Google Cloud Platform (GCP)**. Conçue pour les événements B2B (salons, démos Google Cloud Next, stands interactifs), elle permet à des décideurs d'interagir **en langage naturel à la voix et au texte** avec des données d'entreprise et des bases Open Data via **Vertex AI Data Agents** et **BigQuery**.

### 🎨 Direction Artistique & Style "Gamifié B2B"
1. **Esthétique Modulaire "Soft Corners"** :
   - Coins extrêmement arrondis (`border-radius: 24px` à `32px` / `rounded-3xl`).
   - Style "Bento Grid" épuré inspiré des interfaces Google Cloud modernes.
2. **Gradients & Ambiance Lumineuse Google AI** :
   - Fond sombre haut de gamme (`#030712` / `bg-slate-950`).
   - Accents lumineux et gradients fluides inspirés des couleurs de Gemini (Bleu, Indigo, Violet, Émeraude, Rose, Ambre).
3. **Thématisation Dynamique par Industrie** :
   - Chaque agent possède son propre sous-système de couleurs, d'icônes et de cartes d'arrière-plan adaptées à son secteur d'activité (Santé, Retail, Finance, Télécom, Agriculture, Cinéma, etc.).

---

## 2. Architecture Métier & Données (Track 1)

L'application repose sur **11 Copilotes Décisionnels Sectoriels** interconnectés à BigQuery et Cloud Storage :

| Agent ID | Secteur & Titre | Dataset BigQuery | Source & Spécificités Métiers |
| :--- | :--- | :--- | :--- |
| `sully` | Emploi Public, RH & URSSAF | `public_sector_employment_ds` | Audit santé, vacance des postes hospitaliers (+6m), jointure native Object Table GCS vers les CVs PDF d'origine. |
| `credit_advisor` | Risque Crédit & Finance B2B | `financial_banking_ds` | Scoring de faillite PME/ETI à 6 mois, provisionnement IFRS 9 (ECL), enquêtes BLS Banque de France et upsell trésorerie. |
| `net_arch` | Télécoms & Réseaux ARCEP | `telecom_network_ds` | ARPU abonnés 5G/Fibre, maintenance prédictive IoT des pylônes (température/batterie), débits QoS et SLA NOC. |
| `earth_intel` | Spatial & Imagerie Satellite | `skywatch_aerospace_ds` | Télédétection Sentinel-2 (10m), santé chlorophyllienne NDVI, exposition inondation/incendie, preuve Zéro Déforestation CSRD. |
| `transit_navigator` | Transports Publics & SNCF | `transport_mobility_ds` | Yield Management 1ère classe, diagnostic des retards (Infrastructure vs Matériel), fréquentation 3 000+ gares et objets perdus. |
| `pulse_checker` | Santé & Hôpitaux RPPS | `public_sector_healthcare_ds` | Régulation des urgences (Plan Blanc), prévention des ruptures de stock de médicaments (≤5j) et opportunités cliniques RPPS. |
| `shelf_optimizer` | Retail & Merchandising CPG | `retail_cpg_optimization_ds` | Éradication des Shelf-Out, prédiction anti-gaspillage rayon Frais à 14j, bundles cross-selling Marques Nationales vs MDD. |
| `arena_manager` | Sport & Stades RES | `sports_infrastructure_ds` | Remplissage des loges VIP, panier moyen buvettes/merchandising spectateur, audit énergétique RES des gymnases municipaux. |
| `helios` | Énergie & Bornes IRVE Enedis | `energy_utilities_ds` | Supervision des 10 000 bornes IRVE, télémesure des postes HTA/BT, injection renouvelable et flexibilité d'effacement B2B. |
| `ceres` | Agriculture & Agroécologie | `agriculture_rural_ds` | Pilotage des rendements à l'hectare, valorisation Label Bas-Carbone (crédits CO2e) et bilans ACV ADEME Agribalyse 3.1. |
| `cine_analyst` | Cinéma & Box-Office CNC | `cinema_boxoffice_ds` | Rentabilité Box-Office (ROI), fréquentation des formats immersifs (IMAX/4DX) et part de marché par nationalité. |

---

## 3. Architecture UX/UI en 2 Phases (Track 2)

L'expérience utilisateur est structurée en deux phases distinctes :

```text
+-----------------------------------------------------------------------------------+
|                               TALK TO DATA PLATFORM                               |
+-----------------------------------------------------------------------------------+
|  PHASE 1 : WIZARD BUILDER                 |  PHASE 2 : LIVE EXPERIENCE BENTO GRID  |
|  - Choix du secteur (Cartes Lego 3D)      |  - Orbe Vocal Réactif Gemini           |
|  - Inspection du Dataset & Object Table   |  - Panneau des Défis (Smart Chips)    |
|  - Interrupteur LED "Connecter à BQ"      |  - Dock Hybride (Voix + Clavier)       |
|  - [ 🚀 LANCER L'EXPÉRIENCE ]             |  - Canvas Résultats + SQL Flip Card    |
+-----------------------------------------------------------------------------------+
```

### 🎚️ Phase 1 : Le Wizard Builder
1. **Cartes Sectorielles Soft-Corners** : Grille dynamique des 11 agents avec icônes métiers, description synthétique et badge dataset.
2. **Sélecteur de Connexion** : Toggle switch vert simulant la connexion active avec Vertex AI et BigQuery.
3. **Bouton d'Action** : Un bouton principal lumineux `[ 🚀 LANCER L'EXPÉRIENCE LIVE ]` basculant l'écran vers la Phase 2.

### 🎙️ Phase 2 : Le Plateau de Jeu Live (Bento Grid)
1. **L'Orbe Vocal Réactif Gemini (`GeminiOrb`)** :
   - Avatar sphérique animé réagissant aux 4 états du système :
     - **Calme (Idle)** : Halo bleu/indigo flottant.
     - **À l'écoute (STT)** : Pulsations et onde sonore rose/rouge réactive au micro.
     - **En réflexion (BigQuery)** : Rotation rapide multicolore d'analyse SQL.
     - **S'exprime (TTS)** : Pulsation douce verte/émeraude avec restitution audio.
2. **Panneau des Défis (`ExampleQueries`)** :
   - Cartes cliquables contenant les questions métiers pré-validées par secteur.
3. **Dock d'Entrée Hybride (Voix + Clavier)** :
   - Microphone Web Speech API + Zone de texte multi-lignes.
   - Mode anti-bruit pour les environnements bruyants (salons/démos).
4. **Canvas des Résultats & SQL Inspector (`SQLFlipCard`)** :
   - Rendu Markdown fluide avec tableaux de synthèses de données.
   - Séparation stricte du raisonnement de l'IA (accordéon repliable `Raisonnement & Requête SQL`).
   - Bouton d'inspection sous le capot permettant aux profils techniques de pivoter la carte pour voir la requête SQL BigQuery native.

---

## 4. Stratégie de Résilience & Haute Disponibilité (Failover)

1. **Isolation des Pannes** :
   - Si un agent Vertex AI est temporairement indisponible ou retourne un code HTTP 404/500, l'application ne crashe pas.
   - Le backend FastAPI intercepte l'erreur et envoie un flux SSE d'erreur bienveillant.
2. **Mode Dégradé Gracieux** :
   - Une alerte système s'affiche de manière élégante, proposant au participant de réessayer ou de consulter la synthèse d'exemple.
3. **Chargement Relatif des Assets Vite** :
   - Utilisation de `base: './'` dans `vite.config.js` garantissant le chargement des scripts JS et CSS en chemins relatifs, quel que soit le port, le proxy (Cloud Shell Web Preview, Cloud Run, App Engine).

---

## 5. Comment Modifier et Personnaliser l'Application ?

Si vous souhaitez ajuster la réponse des agents, modifier le style visuel ou ajouter un 12ème agent :

### A. Modifier les Instructions ou Descriptions d'un Agent
Éditez le fichier `agents/<nom_agent>/agent_payload.json` :
- `description` : Texte de présentation de l'agent.
- `systemInstruction` : Prompt système définissant la personnalité, les règles strictes de réponse et l'interdiction du code SQL dans la réponse finale.
- `exampleQueries` : Questions métiers pré-validées.

Puis ré-exécutez le redéploiement :
```bash
python deploy_all_agents.py
```

### B. Ajouter un 12ème Agent Sectoriel
1. Créez le dossier `agents/mon_nouvel_agent/`.
2. Ajoutez les fichiers `ddl_setup.sql`, `generate_data.py`, `agent_payload.json` et `deploy_agent.py`.
3. Ajoutez l'agent au dictionnaire `AGENT_THEMES` dans `backend/agent_manager.py` avec sa couleur et son icône.

### C. Déployer sur Google Cloud Run (us-central1)
Pour obtenir une URL HTTPS publique dans la même région que BigQuery :
```bash
./deploy_cloudrun.sh
```

---

## 6. Prompt d'Instruction Maître (Reconstitution de l'IA)

Le bloc ci-dessous résume le prompt système à transmettre à l'IA pour générer ou modifier cette application :

```text
Tu es Antigravity, un développeur Full-Stack & Lead Data Architect Google Cloud.
Ta mission est de construire une application web nommée "Talk to Data" exposant 11 agents d'intelligence décisionnelle BigQuery via Vertex AI Data Agents.

CONSIGNES UX/UI :
1. Adopte une esthétique "AI Quick Builder" gamifiée avec des coins très arrondis (rounded-3xl), des fonds sombres (bg-slate-950) et des ombres halo colorées.
2. Sépare l'application en 2 phases : Phase 1 (Wizard Configuration Pas-à-Pas avec cartes sectorielles) et Phase 2 (Live Bento Grid Board avec Orbe Vocal réactif).
3. Intègre un avatar vocal Gemini (GeminiOrb) qui change d'animation selon l'état : Idle (bleu), Écoute (rose), Réflexion (multicolore), Parole (vert).
4. Implémente un dock hybride (Bouton Micro STT + Zone texte + Smart Challenge Chips) pour garantir le fonctionnement en environnement bruyant.
5. Intègre la synthèse vocale (Web Speech TTS) et un bouton d'inspection du code SQL sous le capot (SQLFlipCard).
6. Assure une résilience totale : si un agent retourne une erreur, affiche un message d'erreur gracieux sans crasher l'application.
```
