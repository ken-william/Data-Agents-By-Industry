# TalkToData - Plateforme Multi-Agents d'Analyse de Données Entreprise

TalkToData est une plateforme d'agents décisionnels IA déployée sur Google Cloud Platform (GCP). Elle s'appuie sur Vertex AI Data Agents, BigQuery, Cloud Storage et le Knowledge Catalog Dataplex pour répondre aux questions stratégiques et opérationnelles en langage naturel.

La plateforme couvre 11 secteurs d'activité stratégiques en exploitant directement les données officielles Open Data (France Travail, SNCF, Enedis, ARCEP, Ministère des Sports, Banque de France, ADEME, CNC, Open Food Facts, ESA Sentinel-2).

---

## Les 11 Agents Métiers

| Agent | Domaine | Cas d'Usage Principal | Dataset BigQuery |
| :--- | :--- | :--- | :--- |
| **Sully** | Emploi & RH | Analyse des tensions de recrutement BMO 2025, de la taxonomie ROME 4.0, matching candidats et suivi des 300 CVs PDF sur GCS. | `public_sector_employment_ds` |
| **PulseChecker** | Santé & Hôpitaux | Détection des déserts médicaux RPPS, prévention des ruptures de stock de médicaments critiques et régulation des urgences hospitalières. | `public_sector_healthcare_ds` |
| **ShelfOptimizer** | Retail & Grande Distribution | Audit de conformité des planogrammes, réduction de la casse sur le rayon Frais à 14 jours et optimisation du panier moyen MDD. | `retail_cpg_optimization_ds` |
| **EarthIntel** | Imagerie Satellitaire | Surveillance des risques inondation/incendie, stress hydrique agricole NDVI, surcroissance sous lignes HT et conformité Zéro Déforestation CSRD via Sentinel-2. | `skywatch_aerospace_ds` |
| **TransitNavigator** | Transports & Mobilité | Analyse de fréquentation de 3 000 gares SNCF, régularité des lignes TGV/TER, badgeages usagers et restitution des objets perdus. | `transport_mobility_ds` |
| **ArenaManager** | Sport & Stades | Maximisation des recettes de billetterie et buvettes, audit énergétique du recensement des équipements sportifs (RES) et impact des subventions ANS. | `sports_infrastructure_ds` |
| **Helios** | Énergie & Bornes IRVE | Cartographie des 10 000 bornes de recharge Enedis, télémesure des transformateurs, injection d'énergies renouvelables et flexibilité d'effacement B2B. | `energy_utilities_ds` |
| **NetArch** | Télécoms ARCEP | Suivi de la couverture 4G/5G sur 10 000 antennes relais (Orange, SFR, Bouygues, Free), fréquences 3.5 GHz et qualité de service QoS. | `telecom_network_ds` |
| **CreditAdvisor** | Risque Crédit & Finance | Détection préventive des faillites PME, critères d'octroi de crédit Banque de France, provisionnement IFRS 9 et upsell commercial B2B. | `financial_banking_ds` |
| **Ceres** | Transition Agroécologique | Prévision des rendements agricoles, empreinte carbone ADEME Agribalyse 3.1, Label Bas-Carbone et rapports de performance ESG. | `agriculture_rural_ds` |
| **CineAnalyst** | Cinéma & Box-Office | Analyse des séries historiques du CNC, fréquentation des salles, prix des billets, répartition des genres et rentabilité des sorties. | `cinema_boxoffice_ds` |

---

## Installation et Déploiement

### Prérequis
- Python 3.10 ou supérieur.
- Google Cloud SDK (`gcloud`) installé et configuré.
- Un projet GCP avec les APIs BigQuery, Cloud Storage et Vertex AI Data Analytics activées.

### Étapes Rapides

```bash
# 1. Cloner le dépôt
git clone https://github.com/ken-william/Data-Agents-By-Industry.git
cd Data-Agents-By-Industry

# 2. Configurer le projet GCP
export GOOGLE_CLOUD_PROJECT="votre-projet-gcp"

# 3. S'authentifier sur GCP
gcloud auth login
gcloud auth application-default login

# 4. Installer l'environnement Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 5. Déployer l'ensemble des données et des agents en une commande
python deploy_all.py
```

---

## Structure du Projet

- `agents/` : Dossier contenant l'architecture DDL, les pipelines de données et les payloads des 11 agents.
- `download_authentic_opendata.py` : Script de téléchargement automatique des jeux de données Open Data officiels.
- `deploy_all.py` : Script maître de création des tables, d'ingestion et de déploiement des agents sur Vertex AI.
- `requirements.txt` : Dépendances Python nécessaires.

---

## Documentation Complémentaire

- [agents/README.md](agents/README.md) : Spécifications techniques et guide de création d'un nouvel agent.
- [ARCHITECTURE.md](ARCHITECTURE.md) : Détail des schémas relationnels et provenance des données.
- [DEPLOYMENT.md](DEPLOYMENT.md) : Guide détaillé des tests et du déploiement.
