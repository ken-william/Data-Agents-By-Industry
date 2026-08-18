-- ============================================================================
-- Schema DDL for NetArch - Master Telecom Architecture (360° Business & Technical)
-- Dataset: telecom_network_ds (Project: data-agents-by-industry)
-- Relational Architecture linking ARCEP Towers, QoS, NOC Outages, Subscribers,
-- Plans Catalog, SIM/IMEI Technical Hardware, Traffic Sessions, Predictive Maintenance,
-- and Q1/Q2 Data Consumption Forecasts.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `telecom_network_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset NetArch : Vision 360° réseau télécom français, pylônes ARCEP, catalogue forfaits, matériel SIM/IMEI, trafic web agrégé, abonnés B2B/B2C, maintenance prédictive et upsell 5G Max.'
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

-- 5. Table: abonnes_master_customers
CREATE OR REPLACE TABLE `telecom_network_ds.abonnes_master_customers` (
  id_client STRING OPTIONS(description="Identifiant client unique (ex: CLI-90012)"),
  nom_client STRING OPTIONS(description="Raison sociale entreprise B2B ou nom du client B2C"),
  email_contact STRING OPTIONS(description="Adresse email de contact"),
  telephone_contact STRING OPTIONS(description="Numéro de téléphone principal"),
  type_client STRING OPTIONS(description="B2B_PROFESSIONNEL ou B2C_PARTICULIER"),
  siret_entreprise STRING OPTIONS(description="SIRET pour les clients B2B"),
  id_forfait_actuel STRING OPTIONS(description="Identifiant du forfait souscrit (ex: FORF-5G-MAX)"),
  nom_forfait_actuel STRING OPTIONS(description="Nom commercial du forfait souscrit"),
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
OPTIONS (description = "Fichier centralisé des abonnés B2B/B2C : contrat, satisfaction, consommation, hors-forfait, ARPU et prédiction d'upsell.");

-- 6. Table: catalogue_forfaits_abonnements
CREATE OR REPLACE TABLE `telecom_network_ds.catalogue_forfaits_abonnements` (
  id_forfait STRING OPTIONS(description="Identifiant unique du forfait (ex: FORF-5G-MAX)"),
  nom_forfait STRING OPTIONS(description="Nom commercial du forfait"),
  famille_forfait STRING OPTIONS(description="Famille : MOBILE_5G, MOBILE_4G, FIBRE_PRO, CUIVRE_ADSL"),
  cible_client STRING OPTIONS(description="B2B Pro, B2C Grand Public, Enterprise Premium"),
  prix_mensuel_ht_eur NUMERIC OPTIONS(description="Tarif mensuel Hors Taxes (€)"),
  quota_donnees_go INT64 OPTIONS(description="Quota de données mensuel en Go (-1 pour illimité)"),
  debit_max_descendant_mbps INT64 OPTIONS(description="Débit descendant max garanti en Mbps"),
  technologie_reseau_incluse STRING OPTIONS(description="Technologie incluse (5G 3.5GHz, 5G Standalone, 4G+ LTE, Fibre 2Gbps)"),
  services_inclus_liste STRING OPTIONS(description="Description des options incluses (Roaming Monde, Cybersec, IP Fixe)")
)
OPTIONS (description = "Catalogue de référence des forfaits et abonnements fixes & mobiles.");

-- 7. Table: parc_equipements_sim_imei
CREATE OR REPLACE TABLE `telecom_network_ds.parc_equipements_sim_imei` (
  id_equipement_client STRING OPTIONS(description="Identifiant matériel (ex: EQP-78001)"),
  id_client STRING OPTIONS(description="Identifiant de l'abonné propriétaire"),
  constructeur STRING OPTIONS(description="Fabricant du terminal (Apple, Samsung, Google, Xiaomi, Huawei, Cisco, Huawei B2B)"),
  modele_terminal STRING OPTIONS(description="Modèle exact de l'appareil (ex: iPhone 15 Pro 5G, Routeur Cisco 5G Pro)"),
  imei_code STRING OPTIONS(description="Code IMEI unique du terminal à 15 chiffres"),
  imsi_sim_tag_code STRING OPTIONS(description="Code IMSI de la carte SIM (SIM Tag Code)"),
  iccid_sim_card STRING OPTIONS(description="Code ICCID unique de la pucely SIM"),
  type_carte_sim STRING OPTIONS(description="eSIM Virtuelle, Nano-SIM Physique, SIM M2M"),
  compatible_5g BOOL OPTIONS(description="TRUE si le matériel supporte la 5G NR"),
  compatible_5g_standalone BOOL OPTIONS(description="TRUE si le matériel supporte le cœur 5G SA"),
  annee_commercialisation INT64 OPTIONS(description="Année de sortie du matériel"),
  date_premiere_connexion_reseau DATE OPTIONS(description="Date d'enregistrement sur le réseau")
)
OPTIONS (description = "Inventaire technique du parc matériel : codes IMEI, IMSI SIM Tag Code, ICCID, compatibilité 5G SA & eSIM.");

-- 8. Table: sessions_trafic_web_categories
CREATE OR REPLACE TABLE `telecom_network_ds.sessions_trafic_web_categories` (
  id_session STRING OPTIONS(description="Identifiant unique de la session de trafic"),
  id_client STRING OPTIONS(description="Identifiant de l'abonné"),
  imsi_sim_tag_code STRING OPTIONS(description="Code IMSI de la carte SIM"),
  timestamp_session TIMESTAMP OPTIONS(description="Horodatage du début de session"),
  duree_session_minutes INT64 OPTIONS(description="Durée de la session en minutes"),
  volume_download_mb NUMERIC OPTIONS(description="Volume de données téléchargé en Mo"),
  volume_upload_mb NUMERIC OPTIONS(description="Volume de données émis en Mo"),
  categorie_contenu_visite STRING OPTIONS(description="Catégorie agrégée : Streaming Video 4K, Visio Pro Teams/Zoom, Réseaux Sociaux, Cloud Storage, Gaming, Web Browsing"),
  protocole_reseau STRING OPTIONS(description="Protocole : HTTPS, QUIC, SIP_VOIP, UDP_GAMING"),
  id_station_anfr_connectee STRING OPTIONS(description="Identifiant du pylône relais auquel l'appareil était raccordé"),
  qualite_experience_qoe_score NUMERIC OPTIONS(description="Score de qualité d'expérience ressentie QoE (0.0 à 5.0)")
)
OPTIONS (description = "Historique agrégé des sessions de trafic de données : volumes Mo, catégories de contenus consultés et pylône raccordé.");

-- 9. Table: maintenance_predictive_pylones
CREATE OR REPLACE TABLE `telecom_network_ds.maintenance_predictive_pylones` (
  id_pylone_sensor STRING OPTIONS(description="Identifiant de la sonde de télémétrie pylône"),
  id_station_anfr STRING OPTIONS(description="Identifiant ANFR de l'antenne relais"),
  nom_operateur STRING OPTIONS(description="Opérateur mobile"),
  commune STRING OPTIONS(description="Commune d'implantation"),
  temperature_processeur_c NUMERIC OPTIONS(description="Température du processeur de baie en °C"),
  charge_cpu_pct NUMERIC OPTIONS(description="Charge CPU moyenne de la baie (%)"),
  stabilite_tension_volts NUMERIC OPTIONS(description="Tension électrique d'alimentation en Volts"),
  etat_sante_batterie_secours_pct NUMERIC OPTIONS(description="État de santé des batteries de secours (%)"),
  vibration_mat_mm NUMERIC OPTIONS(description="Amplitude de vibration du mât en mm"),
  probabilite_panne_7j_pct NUMERIC OPTIONS(description="Probabilité prédictive d'incident sous 7 jours (%)"),
  composant_a_remplacer_prioritaire STRING OPTIONS(description="Composant critique à remplacer (ex: Carte Alim DC, Ventilateur Baie, Module Optique SFP, Faisceau Hertzien)")
)
OPTIONS (description = "Télémétrie IOT et modèles de maintenance prédictive sur les pylônes télécoms pour prévenir les pannes matérielles.");

-- 10. Table: consommation_historique_trimestrielle_previsions
CREATE OR REPLACE TABLE `telecom_network_ds.consommation_historique_trimestrielle_previsions` (
  periode_id STRING OPTIONS(description="Identifiant de période (ex: PER-2025-01)"),
  mois_label STRING OPTIONS(description="Mois d'observation ou de prévision"),
  trimestre STRING OPTIONS(description="Trimestre comptable"),
  est_prevision BOOL OPTIONS(description="FALSE pour Q1 réel, TRUE pour Q2 prévision"),
  consommation_moyenne_par_abonne_go NUMERIC OPTIONS(description="Consommation moyenne Go par abonné"),
  consommation_totale_reseau_tb NUMERIC OPTIONS(description="Consommation totale réseau en Téraoctets (TB)"),
  taux_croissance_mensuel_pct NUMERIC OPTIONS(description="Taux de croissance mensuel (%)")
)
OPTIONS (description = "Historique réel Q1 et prévisions de consommation de données Q2.");
