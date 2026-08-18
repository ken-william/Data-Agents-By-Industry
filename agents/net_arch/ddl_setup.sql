-- ============================================================================
-- Schema DDL for NetArch - Enterprise Telecom Architecture (360° Business & Technical)
-- Dataset: telecom_network_ds (Project: data-agents-by-industry)
-- Relational Architecture linking ARCEP Towers, QoS, NOC Outages, Subscribers,
-- Plans Catalog, Hardware IMEI/SIM Tag Codes, Partitioned GEOGRAPHY Network Traffic Flows,
-- Predictive Maintenance, and Data Consumption Forecasts.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `telecom_network_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset NetArch : Intelligence télécom 360°, antennes ARCEP, flux de trafic réseau géolocalisés (GEOGRAPHY), catalogue forfaits, matériel IMEI/SIM, maintenance prédictive et upsell.'
);

-- 1. Table: arcep_sites_mobiles_metropole
CREATE OR REPLACE TABLE `telecom_network_ds.arcep_sites_mobiles_metropole` (
  id_station_anfr STRING OPTIONS(description="Identifiant unique de la station antenne enregistré à l'ANFR"),
  num_site STRING OPTIONS(description="Identifiant technique du site chez l'opérateur"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur mobile (Orange, SFR, Bouygues Telecom, Free Mobile)"),
  commune STRING OPTIONS(description="Nom de la commune d'implantation du pylône"),
  code_insee_commune STRING OPTIONS(description="Code INSEE de la commune"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  latitude NUMERIC OPTIONS(description="Latitude (WGS84)"),
  longitude NUMERIC OPTIONS(description="Longitude (WGS84)"),
  site_2g BOOL OPTIONS(description="Émission 2G"),
  site_3g BOOL OPTIONS(description="Émission 3G"),
  site_4g BOOL OPTIONS(description="Émission 4G"),
  site_5g BOOL OPTIONS(description="Émission 5G NR"),
  site_5g_3500mhz BOOL OPTIONS(description="Émission 5G bande cœur 3.5 GHz"),
  site_zone_blanche_dcc BOOL OPTIONS(description="Dispositif Couverture Ciblée / Zone Blanche")
)
OPTIONS (description = "Répertoire officiel ARCEP des stations d'antennes relais mobiles 2G/3G/4G/5G en France.");

-- 2. Table: arcep_historique_deploiement_5g
CREATE OR REPLACE TABLE `telecom_network_ds.arcep_historique_deploiement_5g` (
  date_observation DATE OPTIONS(description="Date du relevé ARCEP"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur"),
  niveau_geographique STRING OPTIONS(description="Niveau d'agrégation"),
  code_geographique STRING OPTIONS(description="Code INSEE ou de zone"),
  libelle_zone STRING OPTIONS(description="Libellé de la zone"),
  nb_sites_5g_700mhz INT64 OPTIONS(description="Sites 5G 700 MHz"),
  nb_sites_5g_2100mhz INT64 OPTIONS(description="Sites 5G 2100 MHz"),
  nb_sites_5g_3500mhz INT64 OPTIONS(description="Sites 5G 3.5 GHz"),
  nb_sites_5g_total INT64 OPTIONS(description="Total sites 5G")
)
OPTIONS (description = "Historique ARCEP du déploiement 5G par opérateur et fréquence.");

-- 3. Table: telecom_qualite_service_metrique
CREATE OR REPLACE TABLE `telecom_network_ds.telecom_qualite_service_metrique` (
  id_mesure STRING OPTIONS(description="Identifiant mesure QoS"),
  nom_operateur STRING OPTIONS(description="Opérateur"),
  commune STRING OPTIONS(description="Commune"),
  code_departement STRING OPTIONS(description="Département"),
  nom_region STRING OPTIONS(description="Région"),
  technologie_reseau STRING OPTIONS(description="Technologie active"),
  debit_descendant_mbps NUMERIC OPTIONS(description="Débit descendant (Download Mbps)"),
  debit_montant_mbps NUMERIC OPTIONS(description="Débit montant (Upload Mbps)"),
  latence_ms NUMERIC OPTIONS(description="Latence (Ping ms)"),
  taux_couverture_4g_pct NUMERIC OPTIONS(description="Stabilité couverture %")
)
OPTIONS (description = "Télémesures de qualité de service mobile (QoS).");

-- 4. Table: telecom_incidents_equipements_reseau
CREATE OR REPLACE TABLE `telecom_network_ds.telecom_incidents_equipements_reseau` (
  id_incident STRING OPTIONS(description="Ticket incident"),
  nom_operateur STRING OPTIONS(description="Opérateur"),
  commune STRING OPTIONS(description="Commune"),
  code_departement STRING OPTIONS(description="Département"),
  nom_region STRING OPTIONS(description="Région"),
  type_equipement STRING OPTIONS(description="Type d'équipement défaillant"),
  severite_incident STRING OPTIONS(description="Niveau de gravité"),
  nombre_abonnes_impactes INT64 OPTIONS(description="Abonnés impactés"),
  statut_resolution STRING OPTIONS(description="Statut de résolution")
)
OPTIONS (description = "Supervision des pannes d'équipement et respect des SLA.");

-- 5. Table: catalogue_forfaits_abonnements (Enterprise Standard Plan Catalog)
CREATE OR REPLACE TABLE `telecom_network_ds.catalogue_forfaits_abonnements` (
  plan_id STRING OPTIONS(description="Identifiant unique du forfait (ex: bcd0ce84-2380-4b0f-b6b1-8804cfd4c3e2)"),
  plan_name STRING OPTIONS(description="Nom commercial du forfait (eco, student, surf, max, family, pro)"),
  monthly_price_eur NUMERIC OPTIONS(description="Tarif mensuel Hors Taxes (€)"),
  data_quota_gb INT64 OPTIONS(description="Quota de données mensuel en Go (-1 pour illimité)"),
  qos_guaranteed_throughput_mbps INT64 OPTIONS(description="Débit descendant max garanti en Mbps"),
  overage_rate_per_gb NUMERIC OPTIONS(description="Tarif de facturation au Go supplémentaire en hors-forfait (€/Go)"),
  is_5g_enabled BOOL OPTIONS(description="TRUE si l'accès au réseau 5G est activé sur le forfait")
)
OPTIONS (description = "Catalogue officiel des forfaits fixes et mobiles (eco, student, surf, max, family).");

-- 6. Table: abonnes_master_customers
CREATE OR REPLACE TABLE `telecom_network_ds.abonnes_master_customers` (
  id_client STRING OPTIONS(description="Identifiant client unique (ex: CLI-90012)"),
  nom_client STRING OPTIONS(description="Raison sociale entreprise B2B ou nom du client B2C"),
  email_contact STRING OPTIONS(description="Adresse email de contact"),
  telephone_contact STRING OPTIONS(description="Numéro de téléphone principal"),
  type_client STRING OPTIONS(description="B2B_PROFESSIONNEL ou B2C_PARTICULIER"),
  siret_entreprise STRING OPTIONS(description="SIRET pour les clients B2B"),
  plan_id STRING OPTIONS(description="Identifiant du forfait souscrit (ex: d8e5fbf0-1264-43be-b31d-d017a7441f42)"),
  plan_name STRING OPTIONS(description="Nom commercial du forfait (eco, student, surf, max, family)"),
  statut_contrat STRING OPTIONS(description="ACTIF, SUSPENDU, EN_MIGRATION"),
  score_nps_satisfaction INT64 OPTIONS(description="Score de satisfaction Net Promoter Score (0 à 10)"),
  date_souscription DATE OPTIONS(description="Date de première souscription"),
  arpu_mensuel_actuel_eur NUMERIC OPTIONS(description="Revenu mensuel actuel (ARPU €)"),
  arpu_potentiel_5g_max_eur NUMERIC OPTIONS(description="ARPU potentiel 5G Max (€)"),
  gain_arpu_potentiel_eur NUMERIC OPTIONS(description="Gain ARPU potentiel (€)"),
  consommation_donnees_mensuelle_gb NUMERIC OPTIONS(description="Volume consommé en Mars (Go)"),
  quota_donnees_mensuel_gb NUMERIC OPTIONS(description="Quota mensuel inclus (Go)"),
  taux_utilisation_quota_mars_pct NUMERIC OPTIONS(description="Utilisation quota Mars (%)"),
  frais_hors_forfait_eur NUMERIC OPTIONS(description="Frais de dépassement hors-forfait (€)"),
  commune STRING OPTIONS(description="Commune de résidence"),
  code_departement STRING OPTIONS(description="Département"),
  nom_region STRING OPTIONS(description="Région"),
  nb_micro_coupures_reseau_30j INT64 OPTIONS(description="Micro-coupures subies sur 30j"),
  score_risque_churn_pct NUMERIC OPTIONS(description="Risque de résiliation (%)"),
  score_propension_upsell_5g_pct NUMERIC OPTIONS(description="Score de propension à l'upsell 5G Max (%)")
)
OPTIONS (description = "Base centralisée des abonnés B2B/B2C : contrats, consommation, hors-forfait, ARPU et upsell.");

-- 7. Table: parc_equipements_sim_imei
CREATE OR REPLACE TABLE `telecom_network_ds.parc_equipements_sim_imei` (
  id_equipement_client STRING OPTIONS(description="Identifiant matériel (ex: EQP-78001)"),
  id_client STRING OPTIONS(description="Identifiant de l'abonné propriétaire"),
  constructeur STRING OPTIONS(description="Fabricant du terminal (Apple, Samsung, Google, Xiaomi, Cisco)"),
  modele_terminal STRING OPTIONS(description="Modèle exact de l'appareil (ex: iPhone 15 Pro 5G, Routeur Cisco 5G Pro)"),
  imei STRING OPTIONS(description="International Mobile Equipment Identity (IMEI unique 15 chiffres)"),
  imsi_sim_tag_code STRING OPTIONS(description="International Mobile Subscriber Identity (SIM Tag Code)"),
  iccid_sim_card STRING OPTIONS(description="Integrated Circuit Card Identifier (Puce SIM)"),
  type_carte_sim STRING OPTIONS(description="eSIM Virtuelle, Nano-SIM Physique"),
  compatible_5g BOOL OPTIONS(description="TRUE si le matériel supporte la 5G NR"),
  compatible_5g_standalone BOOL OPTIONS(description="TRUE si le matériel supporte le cœur 5G SA"),
  annee_commercialisation INT64 OPTIONS(description="Année de sortie du matériel"),
  date_premiere_connexion_reseau DATE OPTIONS(description="Date d'enregistrement sur le réseau")
)
OPTIONS (description = "Inventaire matériel : IMEI, IMSI SIM Tag Code, ICCID, compatibilité 5G SA & eSIM.");

-- 8. Table: network_traffic_flows (High-Volume Partitioned GEOGRAPHY Traffic Table)
CREATE OR REPLACE TABLE `telecom_network_ds.network_traffic_flows` (
  flow_id STRING OPTIONS(description="Unique identifier for each network traffic flow"),
  imei STRING OPTIONS(description="International Mobile Equipment Identity for mobile devices"),
  antenna_id STRING OPTIONS(description="Identifier for the antenna handling the network traffic (ANFR ID / Tower Num)"),
  timestamp TIMESTAMP OPTIONS(description="Exact date and time when the network traffic flow occurred"),
  application_name STRING OPTIONS(description="Name of the application generating or receiving traffic (Netflix, Teams, TikTok, YouTube, WhatsApp)"),
  traffic_type STRING OPTIONS(description="Classification of traffic (Streaming 4K, Visio Pro, Social Media, Cloud Storage, Gaming, Web Browsing)"),
  volume_mb_uplink NUMERIC OPTIONS(description="Volume of data transmitted to the network in MB"),
  volume_mb_downlink NUMERIC OPTIONS(description="Volume of data received from the network in MB"),
  user_location GEOGRAPHY OPTIONS(description="Geographical coordinates representing the user location during flow"),
  latency_ms INT64 OPTIONS(description="Delay experienced by the network traffic in milliseconds"),
  postal_code STRING OPTIONS(description="Postal code associated with the user location")
)
PARTITION BY DATE(timestamp)
OPTIONS (description = "Table haute performance du trafic réseau géolocalisé (GEOGRAPHY, IMEI, antenne, application, volumes MB).");

-- 9. Table: maintenance_predictive_pylones
CREATE OR REPLACE TABLE `telecom_network_ds.maintenance_predictive_pylones` (
  id_pylone_sensor STRING OPTIONS(description="Identifiant sonde télémétrie"),
  id_station_anfr STRING OPTIONS(description="Identifiant ANFR antenne"),
  nom_operateur STRING OPTIONS(description="Opérateur mobile"),
  commune STRING OPTIONS(description="Commune"),
  temperature_processeur_c NUMERIC OPTIONS(description="Température processeur °C"),
  charge_cpu_pct NUMERIC OPTIONS(description="Charge CPU %"),
  stabilite_tension_volts NUMERIC OPTIONS(description="Tension alimentation Volts"),
  etat_sante_batterie_secours_pct NUMERIC OPTIONS(description="Santé batterie %"),
  vibration_mat_mm NUMERIC OPTIONS(description="Vibration mât mm"),
  probabilite_panne_7j_pct NUMERIC OPTIONS(description="Probabilité de panne 7j %"),
  composant_a_remplacer_prioritaire STRING OPTIONS(description="Composant prioritaire à remplacer")
)
OPTIONS (description = "Télémétrie IoT et maintenance prédictive des pylônes télécoms.");

-- 10. Table: signalements_dysfonctionnements_utilisateurs
CREATE OR REPLACE TABLE `telecom_network_ds.signalements_dysfonctionnements_utilisateurs` (
  id_signalement STRING OPTIONS(description="Identifiant signalement"),
  commune STRING OPTIONS(description="Commune"),
  code_departement STRING OPTIONS(description="Département"),
  nom_region STRING OPTIONS(description="Région"),
  couverture_5g_theorique_pct NUMERIC OPTIONS(description="Couverture 5G théorique déclaré (100 %)"),
  nombre_signalements_panne INT64 OPTIONS(description="Nombre de signalements"),
  type_dysfonctionnement STRING OPTIONS(description="Motif du dysfonctionnement"),
  statut_investigation_technique STRING OPTIONS(description="Statut investigation")
)
OPTIONS (description = "Signalements d'anomalies en zones déclarées 100% 5G.");

-- 11. Table: deploiement_fibre_ftth_departements
CREATE OR REPLACE TABLE `telecom_network_ds.deploiement_fibre_ftth_departements` (
  code_departement STRING OPTIONS(description="Code département"),
  nom_departement STRING OPTIONS(description="Nom département"),
  nom_region STRING OPTIONS(description="Région"),
  locaux_raccordables_ftth INT64 OPTIONS(description="Locaux raccordables Fibre"),
  locaux_totaux_departement INT64 OPTIONS(description="Total locaux"),
  taux_couverture_ftth_actuel_pct NUMERIC OPTIONS(description="Couverture FttH actuelle %"),
  objectif_plan_france_thd_pct NUMERIC OPTIONS(description="Objectif Plan France THD (100 %)"),
  retard_deploiement_pct NUMERIC OPTIONS(description="Retard de déploiement %")
)
OPTIONS (description = "Suivi du déploiement de la fibre optique FttH par département.");

-- 12. Table: consommation_historique_trimestrielle_previsions
CREATE OR REPLACE TABLE `telecom_network_ds.consommation_historique_trimestrielle_previsions` (
  periode_id STRING OPTIONS(description="Identifiant de période"),
  mois_label STRING OPTIONS(description="Mois d'observation ou de prévision"),
  trimestre STRING OPTIONS(description="Trimestre comptable"),
  est_prevision BOOL OPTIONS(description="FALSE pour Q1 réel, TRUE pour Q2 prévision"),
  consommation_moyenne_par_abonne_go NUMERIC OPTIONS(description="Consommation moyenne Go par abonné"),
  consommation_totale_reseau_tb NUMERIC OPTIONS(description="Consommation totale réseau en TB"),
  taux_croissance_mensuel_pct NUMERIC OPTIONS(description="Taux de croissance mensuel %")
)
OPTIONS (description = "Historique réel Q1 et prévisions de consommation de données Q2.");
