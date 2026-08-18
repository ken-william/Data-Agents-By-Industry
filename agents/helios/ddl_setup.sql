-- ============================================================================
-- Schema DDL for Helios - Énergie, Réseau Électrique & Bornes IRVE Enedis
-- Dataset: power_energy_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Authentic Enedis IRVE Charging Stations,
-- Grid Transformer Consumption, Renewable Production, and B2B Industrial Clients.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `power_energy_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Helios : Intelligence énergétique Enedis, télémesures 30min, charge des transformateurs, bornes IRVE et production renouvelable.'
);

-- 1. Table: enedis_bornes_irve (Authentic Enedis IRVE EV Charging Hub Master)
CREATE OR REPLACE TABLE `power_energy_ds.enedis_bornes_irve` (
  id_station_itinerance STRING OPTIONS(description="Identifiant unique d'itinérance de la station de recharge IRVE"),
  nom_station STRING OPTIONS(description="Nom commercial de la station de recharge"),
  nom_operateur STRING OPTIONS(description="Nom de l'opérateur de recharge (ex: Freshmile, TotalEnergies, Ionity, Izivia, Enedis)"),
  nom_amenageur STRING OPTIONS(description="Nom de la collectivité ou entreprise aménageuse du site"),
  adresse_station STRING OPTIONS(description="Adresse postale complète de la station"),
  commune STRING OPTIONS(description="Nom de la commune d'implantation"),
  code_postal STRING OPTIONS(description="Code postal français à 5 chiffres"),
  code_departement STRING OPTIONS(description="Département d'implantation (ex: 33 - Gironde, 57 - Moselle, 67 - Bas-Rhin)"),
  nom_region STRING OPTIONS(description="Région administrative"),
  nbre_pdc INT64 OPTIONS(description="Nombre de points de charge (prises) disponibles sur la station"),
  puissance_nominale_kw NUMERIC OPTIONS(description="Puissance nominale maximale délivrée par la station en kW (ex: 22kW, 50kW, 150kW, 350kW)"),
  prise_combo_ccs BOOL OPTIONS(description="Indicateur de présence de connecteur Combo CCS ultra-rapide"),
  prise_type_2 BOOL OPTIONS(description="Indicateur de présence de connecteur Type 2 AC"),
  date_mise_en_service DATE OPTIONS(description="Date officielle de mise en service réseau par Enedis")
)
OPTIONS (
  description = "Répertoire master des 10 000 bornes de recharge pour véhicules électriques réelles Enedis en France."
);

-- 2. Table: enedis_consommation_inf36 (Transformer Load & Grid Stress Telemetry)
CREATE OR REPLACE TABLE `power_energy_ds.enedis_consommation_inf36` (
  id_releve STRING OPTIONS(description="Identifiant unique de la télémesure horodatée"),
  id_station_itinerance STRING OPTIONS(description="Clé étrangère vers enedis_bornes_irve.id_station_itinerance"),
  commune STRING OPTIONS(description="Commune d'implantation du transformateur HTA/BT"),
  code_departement STRING OPTIONS(description="Département du poste source ou transformateur"),
  nom_region STRING OPTIONS(description="Région administrative"),
  nom_transformateur_quartier STRING OPTIONS(description="Identifiant technique Enedis du poste HTA/BT de quartier"),
  horodate_pas30min TIMESTAMP OPTIONS(description="Horodate exacte de la télémesure au pas 30 minutes"),
  consommation_totale_mwh NUMERIC OPTIONS(description="Énergie consommée cumulée sur le pas de temps en MWh"),
  pic_consommation_kw NUMERIC OPTIONS(description="Pic de puissance appelée sur la demi-heure en kW"),
  capacite_max_transformateur_kw NUMERIC OPTIONS(description="Capacité maximale du transformateur Enedis en kW"),
  taux_charge_transformateur_pct NUMERIC OPTIONS(description="Taux de charge calculé en % (Pic / Capacité Max * 100)"),
  risque_tension_reseau STRING OPTIONS(description="Indicateur de risque : Normal, Sous Surveillance Forte, Saturation / Disjonction Imminente 48h")
)
OPTIONS (
  description = "Télémesures de consommation et taux de charge des transformateurs Enedis alimentant les bornes et quartiers."
);

-- 3. Table: enedis_production_renouvelable (Solar, Wind & Biomass Generation)
CREATE OR REPLACE TABLE `power_energy_ds.enedis_production_renouvelable` (
  id_installation STRING OPTIONS(description="Identifiant unique du parc de production Enedis (ex: PROD-ENEDIS-00102)"),
  commune STRING OPTIONS(description="Commune du parc de production"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  filiere_energie STRING OPTIONS(description="Filière : Solaire Photovoltaïque, Éolien Terrestre, Hydraulique, Biomasse / Biogaz"),
  puissance_installee_kw NUMERIC OPTIONS(description="Puissance électrique installée maximale raccordée au réseau en kW"),
  production_journaliere_mwh NUMERIC OPTIONS(description="Énergie totale produite et injectée par jour en MWh"),
  taux_injection_reseau_pct NUMERIC OPTIONS(description="Taux moyen d'injection effective sur le réseau en %")
)
OPTIONS (
  description = "Parcs de production d'énergie renouvelable raccordés au réseau public de distribution Enedis."
);

-- 4. Table: enedis_clients_industriels (High-Voltage B2B Industrial Consumers)
CREATE OR REPLACE TABLE `power_energy_ds.enedis_clients_industriels` (
  id_client_indus STRING OPTIONS(description="Identifiant unique du client industriel HTA/HTB"),
  raison_sociale STRING OPTIONS(description="Raison sociale ou nom du site industriel"),
  secteur_activite STRING OPTIONS(description="Secteur : Chimie & Pharmacie, Métallurgie, Agroalimentaire, Automobile, Data Centers"),
  commune STRING OPTIONS(description="Commune d'implantation de l'usine ou data center"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  consommation_annuelle_mwh NUMERIC OPTIONS(description="Consommation d'électricité annuelle souscrite en MWh"),
  puissance_souscrite_kva NUMERIC OPTIONS(description="Puissance maximale souscrite auprès d'Enedis en kVA"),
  empreinte_carbone_mwh_co2 NUMERIC OPTIONS(description="Émissions équivalent CO2 liées à la consommation en tonnes CO2 eq"),
  optin_flexibilite_effacement BOOL OPTIONS(description="TRUE si le site participe aux mécanismes d'effacement de réseau Enedis")
)
OPTIONS (
  description = "Profils de consommation et potentiel de flexibilité d'effacement des grands clients industriels B2B."
);
