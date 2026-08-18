-- ============================================================================
-- Schema DDL for NetArch - Télécoms, Couverture Mobile & Réseaux ARCEP
-- Dataset: telecom_network_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Official ARCEP "Mon Réseau Mobile" Data,
-- 2G/3G/4G/5G Mobile Towers, 5G Frequencies, QoS Throughputs, and Outage Incidents.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `telecom_network_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset NetArch : Intelligence réseau télécom français, couverture mobile ARCEP, antennes 2G/3G/4G/5G, débits et supervision des incidents d équipement.'
);

-- 1. Table: arcep_sites_mobiles_metropole (Official ARCEP Mobile Towers & 5G Band Master)
CREATE OR REPLACE TABLE `telecom_network_ds.arcep_sites_mobiles_metropole` (
  id_station_anfr STRING OPTIONS(description="Identifiant unique de la station antenne enregistré à l'ANFR"),
  num_site STRING OPTIONS(description="Identifiant technique du site chez l'opérateur"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur mobile (Orange, SFR, Bouygues Telecom, Free Mobile)"),
  commune STRING OPTIONS(description="Nom de la commune d'implantation du pône / pylône"),
  code_insee_commune STRING OPTIONS(description="Code INSEE de la commune à 5 chiffres"),
  code_departement STRING OPTIONS(description="Département d'implantation (ex: 75 - Paris, 33 - Gironde)"),
  nom_region STRING OPTIONS(description="Région administrative"),
  latitude NUMERIC OPTIONS(description="Coordonnée géographique latitude (WGS84)"),
  longitude NUMERIC OPTIONS(description="Coordonnée géographique longitude (WGS84)"),
  site_2g BOOL OPTIONS(description="TRUE si le site émet en technologie 2G / GSM"),
  site_3g BOOL OPTIONS(description="TRUE si le site émet en technologie 3G / UMTS"),
  site_4g BOOL OPTIONS(description="TRUE si le site émet en 4G / LTE"),
  site_5g BOOL OPTIONS(description="TRUE si le site émet en technologie 5G NR"),
  site_5g_3500mhz BOOL OPTIONS(description="TRUE si l'antenne émet sur la bande cœur 3.5 GHz (Ultra Haut Débit)"),
  site_zone_blanche_dcc BOOL OPTIONS(description="TRUE si le site fait partie du Dispositif de Couverture Ciblée (DCC) / Zone Blanche")
)
OPTIONS (
  description = "Répertoire officiel ARCEP des stations d'antennes relais mobiles 2G/3G/4G/5G en France métropolitaine."
);

-- 2. Table: arcep_historique_deploiement_5g (5G Deployment & Frequency History)
CREATE OR REPLACE TABLE `telecom_network_ds.arcep_historique_deploiement_5g` (
  date_observation DATE OPTIONS(description="Date du relevé trimestriel ou mensuel d'ARCEP"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur mobile (Orange, SFR, Bouygues Telecom, Free Mobile)"),
  niveau_geographique STRING OPTIONS(description="Niveau d'agrégation géographique : National, Région, Département"),
  code_geographique STRING OPTIONS(description="Code INSEE ou identifiant de zone"),
  libelle_zone STRING OPTIONS(description="Libellé clair de la zone (ex: Toute France, Île-de-France, Occitanie)"),
  nb_sites_5g_700mhz INT64 OPTIONS(description="Nombre de sites 5G activés sur la bande 700 MHz"),
  nb_sites_5g_2100mhz INT64 OPTIONS(description="Nombre de sites 5G activés sur la bande 2100 MHz"),
  nb_sites_5g_3500mhz INT64 OPTIONS(description="Nombre de sites 5G activés sur la bande cœur 3.5 GHz"),
  nb_sites_5g_total INT64 OPTIONS(description="Volume total de sites 5G ouverts commercialement")
)
OPTIONS (
  description = "Historique ARCEP du déploiement de la 5G en France par opérateur, bandes de fréquences et zones géographiques."
);

-- 3. Table: telecom_qualite_service_metrique (Quality of Service & Throughput Benchmarks)
CREATE OR REPLACE TABLE `telecom_network_ds.telecom_qualite_service_metrique` (
  id_mesure STRING OPTIONS(description="Identifiant unique du test de qualité de service QoS"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur testé"),
  commune STRING OPTIONS(description="Commune de test de débit"),
  code_departement STRING OPTIONS(description="Département de test"),
  nom_region STRING OPTIONS(description="Région administrative"),
  technologie_reseau STRING OPTIONS(description="Technologie active lors du test : 5G 3.5GHz, 5G 700MHz, 4G+ LTE, 4G"),
  debit_descendant_mbps NUMERIC OPTIONS(description="Débit descendant moyen mesuré en Mbps (Download)"),
  debit_montant_mbps NUMERIC OPTIONS(description="Débit montant moyen mesuré en Mbps (Upload)"),
  latence_ms NUMERIC OPTIONS(description="Temps de réponse / Latence réseau mesurée en millisecondes (ms)"),
  taux_couverture_4g_pct NUMERIC OPTIONS(description="Taux d'accès aux services mobile 4G/5G sans coupure (%)")
)
OPTIONS (
  description = "Télémesures de qualité de service (QoS) mobile : débits descendant/montant, latence et stabilité."
);

-- 4. Table: telecom_incidents_equipements_reseau (Network Equipment Outages & Incidents)
CREATE OR REPLACE TABLE `telecom_network_ds.telecom_incidents_equipements_reseau` (
  id_incident STRING OPTIONS(description="Identifiant unique du ticket d'incident équipement"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur concerné"),
  commune STRING OPTIONS(description="Commune touchée par l'incident"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  type_equipement STRING OPTIONS(description="Équipement défaillant : Antenne 5G, Antenne 4G, PBO Fibre, NRO Central, Routeur B2B"),
  severite_incident STRING OPTIONS(description="Niveau de gravité : Majeur - Rupture 48h, Moyen - Dégradation, Mineur"),
  nombre_abonnes_impactes INT64 OPTIONS(description="Nombre d'abonnés mobiles ou fixes impactés par l'interruption"),
  statut_resolution STRING OPTIONS(description="Statut : EN_COURS, RESOLU, INTERVENTION_EQUIPE")
)
OPTIONS (
  description = "Supervision des pannes d'équipement réseau télécom, ruptures de service et temps de rétablissement."
);
