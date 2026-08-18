# TalkToData: Architecture & Data Specifications

This document outlines the detailed system design, relational data models, authentic Open Data sources, and Google Cloud Platform integration patterns implemented in TalkToData.

---

## Data Storage Architecture

### 1. BigQuery Datasets & Regional Configuration

All datasets are provisioned in BigQuery under the target GCP Project (`data-agents-by-industry`).

```text
Project: data-agents-by-industry
├── Dataset: fsi_creditadvisor_dataset (EU / US)
├── Dataset: retail_cpg_ds (EU / US)
├── Dataset: public_sector_employment_ds (EU / US)
├── Dataset: transport_mobility_ds (EU / US)
├── Dataset: skywatch_aerospace_ds (EU / US)
├── Dataset: healthcare_pharma_ds (EU / US)
├── Dataset: telco_media_ds (EU / US)
├── Dataset: agriculture_rurality_ds (EU / US)
├── Dataset: entertainment_cinema_ds (EU / US)
├── Dataset: sports_infrastructure_ds (EU / US)
└── Dataset: power_energy_ds (EU / US)
```

### 2. Cloud Storage Dedicated Buckets (1 Bucket per Agent)

To ensure clear tenant separation and governance, raw data files are stored in dedicated Cloud Storage buckets:

```text
gs://talktodata-credit-advisor-raw-data/
gs://talktodata-shelf-optimizer-raw-data/
gs://talktodata-sully-raw-data/
gs://talktodata-transit-navigator-raw-data/
gs://talktodata-earth-intel-raw-data/
gs://talktodata-pulse-checker-raw-data/
gs://talktodata-net-arch-raw-data/
gs://talktodata-ceres-raw-data/
gs://talktodata-cine-analyst-raw-data/
gs://talktodata-arena-manager-raw-data/
gs://talktodata-helios-raw-data/
```

---

## Authentic Open Data Provenance

TalkToData integrates authentic Open Data downloaded directly from official French government APIs and open data repositories:

| Data Domain | Authentic Dataset Name | Provider | Key Attributes |
| :--- | :--- | :--- | :--- |
| **Transport & Mobility** | `frequentation_gares_sncf.csv` | **SNCF Open Data** | 3,021 French train stations, UIC station codes, annual passenger traffic (2015–2024). |
| **Transport & Mobility** | `sncf_regularite_lignes.csv` | **SNCF Open Data** | 12,544 monthly observations of TGV/TER train line punctuality and delays. |
| **Power & Energy** | `enedis_bornes_irve.csv` | **Enedis Open Data** | 3,892 electric vehicle (EV) charging stations, connector types, power capacity in kW. |
| **Retail & CPG** | `openfoodfacts_catalog.csv` | **Open Food Facts** | Real food products sold in France, EAN barcodes, Nutri-Score, ingredient lists. |
| **FSI & Banking** | `bdf_taux_marche.csv` | **Banque de France** | 9-year time series (2018–2026) of Euribor, ECB key rates, and SME market interest rates. |
| **FSI & Banking** | `bdf_defaillances_sectorielles.csv` | **Banque de France / DIREN** | 4,860 sectorial default rate observations across NAF industry divisions. |
| **FSI & Banking** | `bdf_indices_immobiliers_rpp.csv` | **Banque de France / RPP** | Commercial and residential property price indices. |
| **FSI & Banking** | `bdf_enquete_octroi_bls.csv` | **Banque de France / BLS** | Quarterly Bank Lending Survey credit tightness standards. |
| **Agriculture** | `agribalyse-31-synthese.csv` | **ADEME** | 2,452 agricultural products with Environmental Footprint (EF) single scores and CO2 LCA impacts. |

---

## Relational Schema Specifications

### Ceres (Agriculture & Agroecological Transition)

```text
Table: ademe_agribalyse_31_synthese (2,452 rows)
  - code_ciqual (INT64, Primary Key)
  - nom_du_produit_en_francais (STRING)
  - groupe_daliment (STRING)
  - score_unique_ef (NUMERIC)
  - changement_climatique (NUMERIC)
  - epuisement_des_ressources_eau (NUMERIC)

Table: cooperatives_agricoles (8 rows)
  - id_cooperative (STRING, Primary Key)
  - nom_cooperative (STRING)
  - nom_region (STRING)
  - code_departement (STRING)
  - capacite_stockage_tonnes (NUMERIC)

Table: exploitations_agricoles (1,500 rows)
  - id_exploitation (STRING, Primary Key)
  - id_cooperative (STRING, Foreign Key -> cooperatives_agricoles.id_cooperative)
  - nom_exploitation (STRING)
  - mode_production (STRING)
  - certification_bas_carbone (BOOL)

Table: parcelles_agricoles (4,500 rows)
  - id_parcelle (STRING, Primary Key)
  - id_exploitation (STRING, Foreign Key -> exploitations_agricoles.id_exploitation)
  - culture_actuelle (STRING)
  - code_ciqual (INT64, Foreign Key -> ademe_agribalyse_31_synthese.code_ciqual)
  - surface_ha (NUMERIC)

Table: previsions_anomalies_meteo_ete (27 rows)
  - id_prevision (STRING, Primary Key)
  - annee_saison (STRING)
  - code_departement (STRING)
  - temperature_anomalie_c (NUMERIC)
  - precipitations_anomalie_pct (NUMERIC)
  - baisse_rendement_predite_pct (NUMERIC)

Table: rapports_performance_esg_chaine (8 rows)
  - id_rapport (STRING, Primary Key)
  - annee_exercice (INT64)
  - filiere_principale (STRING)
  - taux_exploitations_certifiees_pct (NUMERIC)
  - empreinte_carbone_chaine_co2_kg_par_kg (NUMERIC)
  - score_performance_esg_global (INT64)
```

---

## Data Analytics Agent API Integration

TalkToData deploys agents using HTTP REST calls to the Vertex AI Data Analytics API:

```http
PATCH https://geminidataanalytics.googleapis.com/v1alpha/projects/{PROJECT_ID}/locations/global/dataAgents/{AGENT_ID}?updateMask=displayName,description,dataAnalyticsAgent
Content-Type: application/json
Authorization: Bearer <GCP_ACCESS_TOKEN>

{
  "displayName": "Ceres - Transition Agroecologique",
  "description": "Copilote d'intelligence agroecologique...",
  "dataAnalyticsAgent": {
    "publishedContext": {
      "systemInstruction": "...",
      "datasourceReferences": {
        "bq": {
          "tableReferences": [ ... ]
        }
      },
      "exampleQueries": [ ... ],
      "glossaryTerms": [ ... ]
    }
  }
}
```
