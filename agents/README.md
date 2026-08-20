# Architecture du Dossier `agents/` - Spécifications & Valeur Métier

Bienvenue dans le répertoire cœur `agents/` de **TalkToData**. Ce dossier contient l'ensemble des définitions, schémas DDL, pipelines de données, payloads d'agents et configurations de gouvernance pour les **11 Agents d'Intelligence Décisionnelle** déployés sur **Google Cloud Platform (GCP)** via **Vertex AI Data Agents** (`geminidataanalytics.googleapis.com`), **BigQuery** et **Dataplex Knowledge Catalog**.

---

## Structure Standardisée d'un Agent

Chaque dossier d'agent suit une architecture de niveau production stricte et homogène :

```text
agents/<nom_agent>/
├── ddl_setup.sql              # Script DDL BigQuery (Tables structurées, typage explicite & points GEOGRAPHY)
├── generate_data.py           # Pipeline d'ingestion Open Data & Génération de données métiers relationnelles
├── agent_payload.json         # Payload Vertex AI (Prompts système, tables BQ, requêtes validées & glossaires métiers)
├── business_catalog_config.json # Configuration Dataplex / Knowledge Catalog (Aperçu, contacts, labels, aspects, règles)
├── deploy_agent.py            # Script de déploiement individuel appelant l'API geminidataanalytics
└── data/                      # Stockage des fichiers CSV/XLSX officiels et des tables d'objets GCS
```

---

## Matrice d'Impact & Valeur Métier des 11 Agents Data

| Agent | Domaine | Problématique Métier Cible | Valeur Ajoutée & ROI Concret | Dataset BigQuery |
| :--- | :--- | :--- | :--- | :--- |
| **Sully** | Emploi & RH | Pénuries de compétences & vacance prolongée (+6m) des postes. | **Réduction des coûts de vacance**, captation des subventions POEI/AFPR, et jointure native Object Table GCS vers les CVs PDF d'origine. | `public_sector_employment_ds` |
| **CreditAdvisor** | Banque & Crédit | Risque de défaillance PME/ETI et encours d'impayés. | **Optimisation de la marge d'intérêt (RAROC)**, scoring de faillite prédictif, provisionnement IFRS 9 (ECL) et ciblage d'upsell lignes de trésorerie. | `financial_banking_ds` |
| **NetArch** | Télécoms ARCEP | Saturation des antennes 5G, pannes matérielles & MTTR. | **Maximisation de l'ARPU**, maintenance prédictive IoT des pylônes à 7 jours, supervision QoS et respect des SLA B2B. | `telecom_network_ds` |
| **EarthIntel** | Géospatial & Spatial | Exposition aux risques climatiques et exigences CSRD. | **Évaluation des risques du portefeuille d'actifs** via Sentinel-2 (10m), santé chlorophyllienne NDVI, élagage lignes HT et preuve Zéro Déforestation. | `skywatch_aerospace_ds` |
| **TransitNavigator** | Transports Publics | Retards ferroviaires, pénalités SLA et remplissage 1ère classe. | **Yield Management billetterie**, isolation des causes de retard (Infra vs Matériel) et fréquentation des 3 000+ gares. | `transport_mobility_ds` |
| **PulseChecker** | Santé & Hôpitaux | Saturation des urgences, absentéisme & déserts médicaux. | **Régulation des urgences hospitalières** (Plan Blanc), prévention des ruptures de stock de médicaments (≤5 jours) et EBITDA cliniques RPPS. | `public_sector_healthcare_ds` |
| **ShelfOptimizer** | Retail & CPG | Ruptures visuelles (Shelf-Out) et démarque rayon Frais. | **Éradication des Shelf-Out**, prédiction du gâchis produits frais à 14 jours, et bundles cross-selling Marques Nationales vs MDD. | `retail_cpg_ds` |
| **ArenaManager** | Sport & Stades | Sous-remplissage des loges VIP et gaspillage énergétique. | **Maximisation des recettes de billetterie/buvettes**, audit énergétique des complexes sportifs (RES) et suivi des subventions ANS. | `sports_infrastructure_ds` |
| **Helios** | Énergie & IRVE Enedis | Saturation des transformateurs et raccordement des bornes EV. | **Supervision des 10 000 bornes IRVE**, télémesure des charges HTA/BT, injection d'énergies renouvelables et flexibilité d'effacement B2B. | `power_energy_ds` |
| **Ceres** | Agroécologie | Aléas climatiques sur les récoltes et reporting ESG. | **Pilotage des rendements à l'hectare**, valorisation du Label Bas-Carbone (crédits CO2e) et bilan ACV ADEME Agribalyse 3.1. | `agriculture_rurality_ds` |
| **CineAnalyst** | Cinéma & Box-Office | Arbitrage des sorties de films et rentabilité des salles. | **Analyse de la rentabilité Box-Office (ROI)**, fréquentation des formats immersifs (IMAX/4DX) et part de marché par nationalité. | `cinema_boxoffice_ds` |

---

## Guide de Création d'un Nouvel Agent Métier

Pour ajouter un 12ème Agent d'Intelligence Décisionnelle à la plateforme :

1. **Créer le dossier** : `mkdir agents/nom_de_mon_agent`
2. **Écrire le schéma DDL** : Créer `agents/nom_de_mon_agent/ddl_setup.sql` avec le typage BigQuery et les descriptions de colonnes.
3. **Ingérer les données** : Créer `agents/nom_de_mon_agent/generate_data.py` pour ingérer les bases Open Data et alimenter BigQuery.
4. **Configurer le Payload Vertex AI** : Rédiger `agents/nom_de_mon_agent/agent_payload.json` avec les consignes métier, les requêtes validées (en tête les questions réelles métiers) et les termes du Knowledge Catalog.
5. **Gouvernance Dataplex** : Créer `agents/nom_de_mon_agent/business_catalog_config.json` pour la gouvernance de données.
6. **Script de Déploiement** : Créer `agents/nom_de_mon_agent/deploy_agent.py` interagissant avec l'API `geminidataanalytics.googleapis.com`.
7. **Enregistrer l'Agent** : Ajouter l'agent dans `deploy_all_agents.py`.
