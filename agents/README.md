# TalkToData — Directory Architecture & Data Agent Specifications

Welcome to the `agents/` core directory of **TalkToData**. This folder contains the 11 specialized AI Data Analytics Agents deployed on **Google Cloud Platform (GCP)** using **Vertex AI Data Agents** (`geminidataanalytics.googleapis.com`), **BigQuery**, **Cloud Storage (GCS)**, and **Dataplex Knowledge Catalog**.

---

## 🏛️ Standard Agent Directory Structure

Every Data Agent directory adheres to a strict, standardized production architecture:

```text
agents/<agent_name>/
├── ddl_setup.sql              # BigQuery DDL schema script with exact column types, descriptions & GEOGRAPHY points
├── generate_data.py           # Relational data generator & Open Data ingestion pipeline
├── agent_payload.json         # Vertex AI Data Agent configuration (System prompt, table refs, natural language queries, glossaries)
├── business_catalog_config.json # Dataplex / Knowledge Catalog metadata (Overview, Contacts, Labels, Aspects, Rules, FQN)
├── deploy_agent.py            # Individual deployment script calling geminidataanalytics API
└── data/                      # Local workspace storing authentic Open Data CSV/XLSX files & exports
```

---

## 📊 Summary of the 11 Industry Data Agents

| Agent Folder | Agent ID | Display Name | Industry Domain & Executive ROI | BigQuery Dataset |
| :--- | :--- | :--- | :--- | :--- |
| `pulse_checker` | `pulse-checker-agent` | **PulseChecker - Copilote Santé** | Identifies medical deserts (RPPS), targets private clinic expansion (5-year EBITDA), prevents drug shortages, and regulates ER capacity (Plans Blancs). | `public_sector_healthcare_ds` |
| `shelf_optimizer` | `shelf-optimizer-agent` | **ShelfOptimizer - Merchandising Retail** | Audits planogram compliance, eliminates visual shelf-outs, reduces fresh food waste (14-day prediction), and optimizes national vs private label margins. | `retail_cpg_optimization_ds` |
| `sully` | `sully-agent` | **Sully - France Travail & Emploi Public** | Anticipates hiring tensions (BMO 2025), leverages ROME 4.0 (12,243 occupations), audits URSSAF employers, ATS matching, and tracks 300 clean PDF resumes on GCS. | `public_sector_employment_ds` |
| `transit_navigator` | `transit-navigator-agent` | **TransitNavigator - Transports & Mobilité** | Analyzes traveler volume across 3,000+ SNCF stations, train delays/SLA, tap-in turnstile validations (`ST_GEOGPOINT`), and lost & found item resolution. | `transport_mobility_ds` |
| `arena_manager` | `arena-manager-agent` | **ArenaManager - Sport & Stades RES** | Maximizes stadium ticket sales & VIP hospitality suites, food/beverage concessions, audits sports facility energy waste (RES census), and ANS grants. | `sports_infrastructure_ds` |
| `earth_intel` | `earthintel-agent` | **EarthIntel - Imagerie Satellitaire** | Unifies GCS Object Tables & BigQuery for Sentinel-2 satellite imagery (10m), flood/fire hazard scores, NDVI crop stress, and CSRD zero-deforestation. | `skywatch_aerospace_ds` |
| `helios` | `helios-agent` | **Helios - Énergie & Bornes IRVE Enedis** | Optimizes 10,000 Enedis EV charging stations (IRVE), monitors 30-min transformer load curves, renewable energy injection, and B2B industrial demand response. | `energy_utilities_ds` |
| `net_arch` | `net-arch-agent` | **NetArch - Architecture Réseau Télécom** | Monitors ARCEP 4G/5G mobile coverage across 10,000 cell towers (Orange, SFR, Bouygues, Free), 3.5 GHz spectrum allocation, QoS latency, and NOC incident resolution. | `telecom_network_ds` |
| `credit_advisor` | `credit-advisor-agent` | **CreditAdvisor - Risque Crédit & Finance** | Detects corporate insolvency risks before bankruptcy, aligns credit policies with Banque de France BLS surveys, models IFRS 9 ECL staging, and B2B upsell. | `financial_banking_ds` |
| `ceres` | `ceres-agent` | **Ceres - Transition Agroécologique** | Predicts weather-driven crop yield drops, models ADEME Agribalyse 3.1 ACV lifecycle environmental footprint, Low-Carbon Label credits, and ESG reporting. | `agriculture_rural_ds` |
| `cine_analyst` | `cine-analyst-agent` | **CineAnalyst - Box-Office Cinéma CNC** | Unifies CNC historical box-office series, theater ticket pricing, regional audience distribution, screen capacity, and movie production profitability. | `cinema_boxoffice_ds` |

---

## 🛠️ How to Add a New Industry Data Agent

To add a 12th Data Agent to TalkToData:

1. **Create Directory** : `mkdir agents/my_new_agent`
2. **Define DDL Schema** : Write `agents/my_new_agent/ddl_setup.sql` with strict BigQuery column types and descriptions.
3. **Data Generator** : Create `agents/my_new_agent/generate_data.py` to ingest Open Data CSVs and load BigQuery.
4. **Agent Payload** : Create `agents/my_new_agent/agent_payload.json` with system prompt, table references, high-ROI natural language queries, and glossary terms.
5. **Business Catalog Config** : Write `agents/my_new_agent/business_catalog_config.json` with Overview, Contacts, Labels, Aspects, Data Quality Rules, and FQN.
6. **Deployment Script** : Create `agents/my_new_agent/deploy_agent.py` calling `geminidataanalytics.googleapis.com`.
7. **Register in Master Pipeline** : Add `my_new_agent` to `deploy_all.py` and `download_authentic_opendata.py`.
