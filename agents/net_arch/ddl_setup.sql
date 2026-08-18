-- ============================================================================
-- Schema DDL for NetArch - Architecture, Couverture ARCEP & Clientèle Télécom
-- Dataset: telecom_network_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Official ARCEP "Mon Réseau Mobile" Data,
-- 2G/3G/4G/5G Towers, QoS Telemetry, Equipment Incidents, B2B/B2C Subscribers,
-- User Incident Alerts, FttH Fiber Coverage, and Data Consumption Forecasting.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `telecom_network_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset NetArch : Intelligence réseau télécom français, antennes ARCEP, débits, pannes, abonnés B2B/B2C, appareils 5G, hors-forfait, churn et prédictions de consommation.'
);

-- 1. Table: arcep_sites_mobiles_metropole (Official ARCEP Mobile Towers & 5G Band Master)
CREATE OR REPLACE TABLE `telecom_network_ds.arcep_sites_mobiles_metropole` (
  id_station_anfr STRING OPTIONS(description="Identifiant unique de la station antenne enregistré à l'ANFR"),
  num_site STRING OPTIONS(description="Identifiant technique du site chez l'opérateur"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur mobile (Orange, SFR, Bouygues Telecom, Free Mobile)"),
  commune STRING OPTIONS(description="Nom de la commune d'implantation du pylône"),
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
  type_equipement STRING OPTIONS(description="Équipement défaillant : Antenne 5G, Antenne 4G, Routeur B2B Quartier, PBO Fibre Optique, NRO Central"),
  severite_incident STRING OPTIONS(description="Niveau de gravité : Majeur - Micro-Coupures Répétées, Moyen - Dégradation, Mineur"),
  nombre_abonnes_impactes INT64 OPTIONS(description="Nombre d'abonnés mobiles ou fixes impactés par l'interruption"),
  statut_resolution STRING OPTIONS(description="Statut : EN_COURS, RESOLU, INTERVENTION_EQUIPE")
)
OPTIONS (
  description = "Supervision des pannes d'équipement réseau télécom, micro-coupures de routeurs B2B et temps de rétablissement."
);

-- 5. Table: abonnes_clients_b2b_b2c (Subscribers Master: Churn B2B, Smart 5G Upsell & Data Consumpt)
CREATE OR REPLACE TABLE `telecom_network_ds.abonnes_clients_b2b_b2c` (
  id_client STRING OPTIONS(description="Identifiant unique de l'abonné (ex: CLI-90012)"),
  nom_client STRING OPTIONS(description="Raison sociale entreprise B2B ou nom du client B2C"),
  type_client STRING OPTIONS(description="Type d'abonné : B2B_PROFESSIONNEL ou B2C_PARTICULIER"),
  smartphone_modele_appareil STRING OPTIONS(description="Modèle de smartphone ou routeur détenu par le client (ex: iPhone 15 Pro 5G, Samsung S24 5G)"),
  appareil_compatible_5g BOOL OPTIONS(description="TRUE si le smartphone ou routeur du client est compatible 5G"),
  forfait_actuel_nom STRING OPTIONS(description="Nom de l'abonnement actuel (ex: Forfait 4G LTE 100 Go, Forfait 4G Pro 150 Go, Forfait 5G Max 250 Go)"),
  forfait_actuel_5g BOOL OPTIONS(description="TRUE si la souscription active inclut l'accès au réseau 5G"),
  technologie_actuelle STRING OPTIONS(description="Raccordement actuel : CUIVRE_ADSL, FIBRE_FTTH, 4G_MOBILE, 5G_MOBILE"),
  consommation_donnees_mensuelle_gb NUMERIC OPTIONS(description="Volume de données consommé en Gigaoctets (Go) sur le mois de Mars"),
  quota_donnees_mensuel_gb NUMERIC OPTIONS(description="Quota mensuel de données inclus dans l'abonnement actuel en Go"),
  taux_utilisation_quota_mars_pct NUMERIC OPTIONS(description="Taux de consommation du quota sur le mois de Mars (%)"),
  frais_hors_forfait_eur NUMERIC OPTIONS(description="Frais de dépassement / hors-forfait facturés en Euros (€)"),
  arpu_mensuel_actuel_eur NUMERIC OPTIONS(description="Revenu moyen mensuel actuel (ARPU) facturé au client (€)"),
  arpu_potentiel_5g_max_eur NUMERIC OPTIONS(description="ARPU potentiel estimé après migration vers le Forfait 5G Max / Fibre Pro (€)"),
  gain_arpu_potentiel_eur NUMERIC OPTIONS(description="Gain moyen de chiffre d'affaires ARPU mensuel généré par la migration 5G Max (€)"),
  commune STRING OPTIONS(description="Commune d'implantation de l'abonné"),
  code_departement STRING OPTIONS(description="Département de résidence"),
  nom_region STRING OPTIONS(description="Région administrative"),
  nb_micro_coupures_reseau_30j INT64 OPTIONS(description="Nombre de micro-coupures subies sur le routeur de quartier sur 30 jours"),
  risque_churn_pct NUMERIC OPTIONS(description="Score de risque de résiliation / Churn calculé (%)")
)
OPTIONS (
  description = "Base abonnés B2B et B2C : modèles de smartphones, compatibilité 5G, forfaits 4G/5G, consommation Go, hors-forfait, ARPU et risque de résiliation."
);

-- 6. Table: signalements_dysfonctionnements_utilisateurs (User Alerts vs 100% Theoretical Coverage)
CREATE OR REPLACE TABLE `telecom_network_ds.signalements_dysfonctionnements_utilisateurs` (
  id_signalement STRING OPTIONS(description="Identifiant du signalement client ou alerte application"),
  commune STRING OPTIONS(description="Commune concernée par l'alerte utilisateur"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  couverture_5g_theorique_pct NUMERIC OPTIONS(description="Taux de couverture 5G théorique déclaré à l'ARCEP (ex: 100 %)"),
  nombre_signalements_panne INT64 OPTIONS(description="Nombre total de signalements d'utilisateurs pour dysfonctionnement"),
  type_dysfonctionnement STRING OPTIONS(description="Motif : Micro-coupures quotidiennes, Débit nul malgré 5G, Absence de signal indoor"),
  statut_investigation_technique STRING OPTIONS(description="Statut : AUDIT_EN_COURS, ANOMALIE_CONFIRMEE, CORRIGE")
)
OPTIONS (
  description = "Signalements de pannes et dysfonctionnements réseau remontés dans les communes déclarées à 100 % de couverture 5G."
);

-- 7. Table: deploiement_fibre_ftth_departements (FttH Fiber Deployment Progress vs National Plan)
CREATE OR REPLACE TABLE `telecom_network_ds.deploiement_fibre_ftth_departements` (
  code_departement STRING OPTIONS(description="Code département (ex: 75 - Paris, 23 - Creuse)"),
  nom_departement STRING OPTIONS(description="Nom du département"),
  nom_region STRING OPTIONS(description="Région administrative"),
  locaux_raccordables_ftth INT64 OPTIONS(description="Nombre de logements et locaux professionnels raccordables à la Fibre"),
  locaux_totaux_departement INT64 OPTIONS(description="Nombre total de locaux du département"),
  taux_couverture_ftth_actuel_pct NUMERIC OPTIONS(description="Taux de couverture effective FttH (%)"),
  objectif_plan_france_thd_pct NUMERIC OPTIONS(description="Objectif national du Plan France Très Haut Débit (100 %)"),
  retard_deploiement_pct NUMERIC OPTIONS(description="Écart / Retard de déploiement en points de pourcentage par rapport à l'objectif")
)
OPTIONS (
  description = "Suivi départemental du retard de déploiement de la fibre optique FttH par rapport au Plan France Très Haut Débit."
);

-- 8. Table: consommation_historique_trimestrielle_previsions (Q1 Data Consumption & Q2 Forecasting)
CREATE OR REPLACE TABLE `telecom_network_ds.consommation_historique_trimestrielle_previsions` (
  periode_id STRING OPTIONS(description="Identifiant de période (ex: PER-2025-01)"),
  mois_label STRING OPTIONS(description="Mois d'observation ou de prévision (ex: Janvier 2025, Avril 2025 (Prévision))"),
  trimestre STRING OPTIONS(description="Trimestre comptable (ex: Q1 2025, Q2 2025)"),
  est_prevision BOOL OPTIONS(description="FALSE pour les données historiques réelles Q1, TRUE pour les prévisions Q2"),
  consommation_moyenne_par_abonne_go NUMERIC OPTIONS(description="Consommation moyenne de données mensuelle par abonné (Go)"),
  consommation_totale_reseau_tb NUMERIC OPTIONS(description="Consommation totale cumulée sur le réseau en Téraoctets (TB)"),
  taux_croissance_mensuel_pct NUMERIC OPTIONS(description="Taux de croissance mensuel du trafic de données (%)")
)
OPTIONS (
  description = "Historique réel du 1er trimestre et prévisions de consommation de données pour le 2ème trimestre."
);
