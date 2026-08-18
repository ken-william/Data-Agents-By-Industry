-- ============================================================================
-- Schema DDL for Earth Intel - Imagerie Satellitaire & Intelligence Géospatiale
-- Dataset: skywatch_aerospace_ds (Project: data-agents-by-industry)
-- Relational & Multimodal Architecture unifying Sentinel-2 / Copernicus Satellite
-- Scenes, Industrial Assets with GEOGRAPHY, Flood/Fire Risk Alerts, CSRD Deforestation
-- Verification, and GCS Cloud Storage Object Tables for Direct Image Analysis.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `skywatch_aerospace_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Earth Intel : Imagerie satellitaire ESA Sentinel-2, indices géospatiaux (NDVI, NDWI), audits d\'actifs industriels et table d\'objets Cloud Storage.'
);

-- Drop legacy view if exists
DROP VIEW IF EXISTS `skywatch_aerospace_ds.sentinel_2_index`;
DROP TABLE IF EXISTS `skywatch_aerospace_ds.sentinel_2_index`;

-- 1. Table: company_assets (Industrial & Enterprise Assets with GEOGRAPHY & Risk Scores)
CREATE OR REPLACE TABLE `skywatch_aerospace_ds.company_assets` (
  asset_id STRING OPTIONS(description="Identifiant unique de l'actif industriel ou site d'exploitation (ex: AST-FSI-01)"),
  company_name STRING OPTIONS(description="Nom de l'entreprise ou du groupe propriétaire (ex: AXA Assurances, Sanofi, Agrial, EDF)"),
  industry_sector STRING OPTIONS(description="Secteur d'activité entreprise (Banque & Assurance, Santé & Pharma, Agriculture, Transports, Énergie, Retail, Secteur Public, Télécoms, Divertissement, Sport)"),
  asset_name STRING OPTIONS(description="Nom du site ou complexe (ex: Portefeuille Immobilier Côte d'Azur, Usine Vaccins Marcy-l'Étoile)"),
  asset_type STRING OPTIONS(description="Typologie d'infrastructures (Immobilier commercial, Usine bioproduction, Réseau HT, Hub portuaire)"),
  mgrs_tile STRING OPTIONS(description="Code Tuile MGRS Sentinel-2 rattaché (ex: 31TDF, 31TFL, 30TYQ)"),
  latitude NUMERIC OPTIONS(description="Latitude GPS du centre de l'actif"),
  longitude NUMERIC OPTIONS(description="Longitude GPS du centre de l'actif"),
  location_geo GEOGRAPHY OPTIONS(description="Point spatial ST_GEOGPOINT des coordonnées précises"),
  city STRING OPTIONS(description="Ville ou commune d'implantation"),
  region STRING OPTIONS(description="Région administrative"),
  country STRING OPTIONS(description="Pays"),
  criticality_score NUMERIC OPTIONS(description="Score de criticité de l'actif (0.0 à 1.0)"),
  annual_revenue_impact_eur NUMERIC OPTIONS(description="Chiffre d'affaires ou valeur d'exposition financière (€)"),
  csrd_compliance_status STRING OPTIONS(description="Statut de conformité réglementaire CSRD Zéro Déforestation"),
  flood_risk_score NUMERIC OPTIONS(description="Score de risque d'inondation (0.0 à 1.0)"),
  fire_risk_score NUMERIC OPTIONS(description="Score de risque d'incendie de forêt (0.0 à 1.0)"),
  stagnant_water_km2 NUMERIC OPTIONS(description="Surface d'eaux stagnantes détectée dans un rayon de 5km (km²)"),
  mosquito_outbreak_risk STRING OPTIONS(description="Risque épidémiologique moustiques vecteurs (Nul, Faible, Modéré, Élevé)"),
  ndvi_vegetation_index NUMERIC OPTIONS(description="Indice de végétation moyen NDVI (0.0 à 1.0)"),
  port_container_ships_waiting INT64 OPTIONS(description="Nombre de navires en attente observés aux terminaux portuaires"),
  powerline_tree_encroachment_m NUMERIC OPTIONS(description="Distance minimale mesurée entre frondaison d'arbres et ligne haute tension (m)"),
  deforestation_rate_pct_5y NUMERIC OPTIONS(description="Taux de déforestation mesuré sur 5 ans sur le bassin de sourcing (%)"),
  urban_heat_island_celsius NUMERIC OPTIONS(description="Anomalie de température d'îlot de chaleur urbain (°C)"),
  canopy_density_5g_obstacle_pct NUMERIC OPTIONS(description="Densité de canopée formant obstacle à la propagation des ondes 5G (%)"),
  snow_cover_historical_pct NUMERIC OPTIONS(description="Taux moyen d'enneigement mesuré pour les sites de montagne (%)"),
  stadium_green_cooling_canopy_pct NUMERIC OPTIONS(description="Taux d'ombrage et de canopée rafraîchissante autour des grands stades (%)")
)
OPTIONS (
  description = "Inventaire des sites et actifs industriels des entreprises avec indicateurs géospatiaux et scores de résilience."
);

-- 2. Table: sentinel_2_index (Sentinel-2 Satellite Imagery Scenes & Quicklook Links)
CREATE OR REPLACE TABLE `skywatch_aerospace_ds.sentinel_2_index` (
  scene_id STRING OPTIONS(description="Identifiant unique du cliché satellitaire ESA Sentinel-2 (ex: S2B_MSIL2A_20260815T104021)"),
  mgrs_tile STRING OPTIONS(description="Code Tuile MGRS (ex: 31TDF, 31TFL)"),
  acquisition_date DATE OPTIONS(description="Date d'acquisition du cliché par le satellite"),
  cloud_cover_pct NUMERIC OPTIONS(description="Taux de couverture nuageuse du cliché (%)"),
  constellation_satellite STRING OPTIONS(description="Nom du satellite (Sentinel-2A, Sentinel-2B)"),
  ndvi_mean NUMERIC OPTIONS(description="Indice de végétation moyen (Normalized Difference Vegetation Index)"),
  ndwi_water_mean NUMERIC OPTIONS(description="Indice d'eau moyen (Normalized Difference Water Index)"),
  quicklook_image_url STRING OPTIONS(description="URI Cloud Storage GCS du cliché image Quicklook PNG (ex: gs://talktodata-earth-intel-raw-data/satellite_imagery/s2_31TDF_quicklook.png)")
)
OPTIONS (
  description = "Catalogue d'indexation des scènes et métadonnées d'imagerie satellitaire ESA Sentinel-2."
);

-- 3. Table: satellites_constellations_metadonnees (Satellite Constellations Specs)
CREATE OR REPLACE TABLE `skywatch_aerospace_ds.satellites_constellations_metadonnees` (
  satellite_id STRING OPTIONS(description="Identifiant du satellite (ex: SENTINEL-2A, SENTINEL-2B, LANDSAT-9)"),
  operator STRING OPTIONS(description="Opérateur spatial (ESA / Copernicus, NASA / USGS)"),
  spatial_resolution_m NUMERIC OPTIONS(description="Résolution spatiale au sol en mètres (ex: 10.0 m)"),
  revisit_time_days INT64 OPTIONS(description="Temps de relecture / revisite sur le même point (en jours)"),
  spectral_bands_count INT64 OPTIONS(description="Nombre de bandes spectrales (Bandes Optiques, NIR, SWIR, Thermique)"),
  orbit_type STRING OPTIONS(description="Type d'orbite (Orbite Héliosynchrone Basse LEO)")
)
OPTIONS (
  description = "Répertoire des caractéristiques techniques des constellations satellitaires de télédétection."
);

-- 4. Table: inondations_incendies_alertes (Flood, Fire & Natural Hazards Alerts)
CREATE OR REPLACE TABLE `skywatch_aerospace_ds.inondations_incendies_alertes` (
  alert_id STRING OPTIONS(description="Identifiant de l'alerte de risque naturel (ex: ALR-2026-001)"),
  asset_id STRING OPTIONS(description="Identifiant de l'actif menacé (FK -> company_assets)"),
  scene_id STRING OPTIONS(description="Identifiant du cliché satellitaire de confirmation (FK -> sentinel_2_index)"),
  alert_type STRING OPTIONS(description="Type d'aléa naturel (Inondation Majeure, Départ de Feu de Forêt, Canicule & Îlot de Chaleur, Risque Sanitaire Moustique)"),
  severity_level STRING OPTIONS(description="Niveau de sévérité (Faible, Modéré, Critique, Urgence Majeure)"),
  alert_date TIMESTAMP OPTIONS(description="Horodatage du déclenchement de l'alerte"),
  financial_loss_risk_eur NUMERIC OPTIONS(description="Montant du risque financier d'exposition (€)")
)
OPTIONS (
  description = "Registre des alertes d'incendies, inondations et risques environnementaux confirmées par imagerie spatiale."
);

-- 5. Table: deforestation_csrd_verification (CSRD Zero Deforestation Certification)
CREATE OR REPLACE TABLE `skywatch_aerospace_ds.deforestation_csrd_verification` (
  verification_id STRING OPTIONS(description="Identifiant du certificat de conformité CSRD (ex: CSRD-2026-001)"),
  asset_id STRING OPTIONS(description="Actif ou bassin d'approvisionnement (FK -> company_assets)"),
  commodity_type STRING OPTIONS(description="Matière première suivie (Soja, Cacao, Huile de Palme, Bois / Pâte à papier)"),
  sourcing_country STRING OPTIONS(description="Pays de provenance du sourcing"),
  verified_deforestation_free BOOLEAN OPTIONS(description="Certification attestant l'absence de déforestation après la date butoir réglementaire"),
  canopy_loss_hectares NUMERIC OPTIONS(description="Perte de couvert forestier mesurée par satellite (en hectares)"),
  audit_date DATE OPTIONS(description="Date du dernier audit d'imagerie spatiale")
)
OPTIONS (
  description = "Certificats de conformité à la directive européenne CSRD et au règlement contre la déforestation (RDUE)."
);
