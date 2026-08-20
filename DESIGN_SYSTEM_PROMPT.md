# Master Specification & Prompt System - Talk to Data (Enterprise Grade Dark Mode)

Ce document constitue la **Spécification Complète et le Prompt Système Maître** ayant permis la conception, le design et le développement de la plateforme **"Talk to Data"**. Il définit les consignes strictes d'architecture, d'UX/UI B2B Enterprise et d'intégration Google Cloud.

---

## 1. Vision Globale & Direction Artistique B2B Enterprise

### 🎯 Objectif Métier & Événementiel
**Talk to Data** est une application web décisionnelle multi-agents déployée sur **Google Cloud Platform (GCP)**. Elle permet aux décideurs d'interagir **en langage naturel à la voix et au texte** avec des données d'entreprise et Open Data via **Vertex AI Data Agents** et **BigQuery**.

### 🎨 Consignes Strictes de Design (Enterprise Grade Dark Mode)

1. **Palette & Fond** :
   - Fond d'écran : Gris foncé neutre et épuré `bg-[#09090b]` (Zinc 950). Fini le noir total ou les halos lumineux violents.
   - Cartes (Bento Grid) : Fond légèrement contrasté `bg-[#141417]` avec une bordure fine et sobre `border-[#27272a]`.
   - Suppression des halos lumineux diffus colorés. Utilisation de liserés discrets pour indiquer l'état actif.

2. **Formes & Coins** :
   - Utilisation de `rounded-xl` (12px) pour les cartes principales et `rounded-md` (6px) ou `rounded-lg` (8px) pour les boutons et badges.

3. **Typographie & Hiérarchie** :
   - Titres : Blanc neutre (`text-zinc-50`), taille modérée et graisse semi-bold.
   - Textes secondaires / Descriptions : Gris clair (`text-zinc-400`), taille réduite `text-xs` / `text-sm`.
   - Métadonnées (Datasets, IDs) : Discrètes, `text-zinc-500` et `text-[11px]`.
   - Icônes monocromes (`text-zinc-300`) accompagnées de badges de couleur très légers et discrets pour éliminer l'effet "sapin de Noël".

4. **Layout & Organisation** :
   - **Phase 1 (Builder)** : Grille dense, aérée et très lisible des 11 agents sectoriels.
   - **Phase 2 (Live)** : Le panneau central de résultats prend 70% de l'espace visuel (priorité au contenu et aux tableaux Markdown). L'Orbe Gemini est compact, discret et intégré élégamment.

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

```text
+-----------------------------------------------------------------------------------+
|                        TALK TO DATA PLATFORM (ENTERPRISE)                         |
+-----------------------------------------------------------------------------------+
|  PHASE 1 : WIZARD BUILDER                 |  PHASE 2 : LIVE BENTO GRID BOARD       |
|  - Grille dense d'agents (#141417)        |  - Orbe Gemini discret & compact       |
|  - Icônes monocromes + badges discrets    |  - Smart Challenge Chips (Défis B2B)   |
|  - Toggle BQ Connection + Security Tag    |  - Canvas Résultats (70% Priorité)     |
|  - [ 🚀 LANCER L'EXPÉRIENCE ]             |  - Inspector SQL sous le capot         |
+-----------------------------------------------------------------------------------+
```

---

## 4. Prompt de Reconstitution Corrigé (Clean & Pro)

```text
Tu es un Senior UX/UI Designer et Développeur Front-End spécialisé dans les interfaces Google Cloud (B2B).
Ta mission est de reconstruire l'application "Talk to Data" avec un design moderne, épuré, professionnel et hautement lisible ("Enterprise Grade Dark Mode").

CONSIGNES STRICTES DE DESIGN (Tailwind CSS préférés) :

1. PALETTE & FOND :
   - Fini le noir total. Utilise un fond gris foncé neutre et moderne : `bg-[#09090b]` (Zinc 950).
   - Pour les cartes (Bento), utilise un fond légèrement contrasté : `bg-[#141417]` avec une bordure très fine `border-[#27272a]`.
   - Supprime les halos lumineux colorés trop voyants. Utilise des liserés discrets pour indiquer l'état actif.

2. FORMES & COINS :
   - Réduis les arrondis extrêmes. Utilise `rounded-xl` (12px) pour les cartes principales et `rounded-md` (6px) pour les boutons et badges.

3. TYPOGRAPHIE ET HIÉRARCHIE :
   - Titres : Blanc neutre (`text-zinc-50`), taille modérée.
   - Textes secondaires / Descriptions : Gris clair (`text-zinc-400`), taille réduite `text-sm`.
   - Métadonnées (Datasets, IDs) : Discrètes, `text-zinc-500` et `text-xs`.
   - Réduis la taille des polices globales pour éviter l'effet "gros boutons".

4. LAYOUT ET ORGANISATION :
   - Phase 1 (Builder) : Organise les 11 cartes dans une grille dense mais aérée. Cache les informations superflues (ex: chemin exact du dataset) sous un badge ou en très petit.
   - Phase 2 (Live) : Le panneau central de résultat doit être la priorité visuelle (clair, lisible, fond noir profond). L'Orbe Gemini doit être élégant et petit, pas un avatar géant.

5. ACCESSIBILITÉ :
   - Assure un contraste suffisant entre le texte et le fond des cartes.
   - Les zones cliquables doivent être clairement identifiables sans couleurs flashy.
```
