-- ============================================================================
-- Schema DDL for Ceres - Agriculture, Ruralité & Transition Agroécologique
-- Dataset: agriculture_rurality_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Cooperatives, Farms, Parcels, ADEME Agribalyse ACV, 
-- Harvests, Weather Forecast Anomalies (Q1), and ESG Reports (Q3).
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `agriculture_rurality_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Ceres : Intelligence environnementale, transition agroécologique, prévisions météo d\'été, coopératives et rapports ESG.'
);

-- 1. Table: ademe_agribalyse_31_synthese (Real ADEME Agribalyse 3.1 ACV Product Catalog)

-- 2. Table: cooperatives_agricoles (Agricultural Cooperatives Master - Q1)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.cooperatives_agricoles` (
  id_cooperative STRING OPTIONS(description="Identifiant unique de la coopérative agricole (ex: COO_4001)"),
  nom_cooperative STRING OPTIONS(description="Nom officiel de la coopérative (ex: Arterris, Tereos, Euralis, Lur Berri, Axereal, Agrial, Vivescia, Cristal Union)"),
  siren STRING OPTIONS(description="Numéro SIREN à 9 chiffres de la coopérative"),
  nom_region STRING OPTIONS(description="Région principale d'implantation (ex: Occitanie, Nouvelle-Aquitaine, Grand Est)"),
  code_departement STRING OPTIONS(description="Département du siège de la coopérative"),
  capacite_stockage_tonnes NUMERIC OPTIONS(description="Capacité totale des silos et infrastructures de stockage en tonnes"),
  filiere_principale STRING OPTIONS(description="Filière dominante : Grandes cultures, Viticulture, Arboriculture, Elevage, Maraichage")
)
OPTIONS (
  description = "Répertoire des coopératives agricoles régionales et capacité de stockage."
);

-- 3. Table: exploitations_agricoles (Farm Master Table)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.exploitations_agricoles` (
  id_exploitation STRING OPTIONS(description="Identifiant unique de l'exploitation agricole (ex: EXP_310042)"),
  id_cooperative STRING OPTIONS(description="Clé étrangère vers cooperatives_agricoles.id_cooperative"),
  nom_exploitation STRING OPTIONS(description="Raison sociale ou nom du domaine / de la ferme"),
  siren STRING OPTIONS(description="Numéro SIREN à 9 chiffres de l'exploitation"),
  nom_exploitant STRING OPTIONS(description="Nom et prénom du chef d'exploitation principal"),
  code_region STRING OPTIONS(description="Code de la région administrative (ex: OCC, NAQ, ARA)"),
  nom_region STRING OPTIONS(description="Nom de la région (ex: Occitanie, Nouvelle-Aquitaine, Auvergne-Rhône-Alpes)"),
  code_departement STRING OPTIONS(description="Numéro et nom du département (ex: 31 - Haute-Garonne, 32 - Gers)"),
  commune STRING OPTIONS(description="Commune d'implantation du siège de l'exploitation"),
  code_postal STRING OPTIONS(description="Code postal français"),
  surface_totale_ha NUMERIC OPTIONS(description="Surface Agricole Utile (SAU) totale en hectares (ha)"),
  mode_production STRING OPTIONS(description="Mode de conduite : Conventionnel, Bio / Agriculture Biologique, Conversion Bio, HVE - Haute Valeur Environnementale"),
  filiere_principale STRING OPTIONS(description="Filière agricole principale : Grandes cultures, Viticulture, Élevage bovin, Arboriculture, Maraîchage"),
  date_creation DATE OPTIONS(description="Date de création ou de reprise de l'exploitation"),
  certification_bas_carbone BOOL OPTIONS(description="Indicateur d'obtention du Label Bas-Carbone ministère de la Transition Écologique")
)
OPTIONS (
  description = "Répertoire master des exploitations agricoles affiliées aux coopératives et leur niveau d'engagement agroécologique."
);

-- 4. Table: parcelles_agricoles (Field Parcels & Crop Mapping)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.parcelles_agricoles` (
  id_parcelle STRING OPTIONS(description="Identifiant unique de la parcelle cadastrale (ex: PAR_700142)"),
  id_exploitation STRING OPTIONS(description="Clé étrangère vers exploitations_agricoles.id_exploitation"),
  nom_parcelle STRING OPTIONS(description="Nom usuel du champ ou numéro d'îlot RPG"),
  surface_ha NUMERIC OPTIONS(description="Surface spécifique de la parcelle en hectares (ha)"),
  culture_actuelle STRING OPTIONS(description="Culture principale implantée (ex: Blé tendre, Maïs grain, Colza, Vigne, Pomme de terre, Tournesol, Soja)"),
  code_ciqual INT64 OPTIONS(description="Clé étrangère vers ademe_agribalyse_31_synthese.code_ciqual pour l'ACV produit"),
  type_sol STRING OPTIONS(description="Nature pédologique du sol : Argilo-calcaire, Limoneux, Sableux, Granitique, Alluvial"),
  irrigation_active BOOL OPTIONS(description="Indicateur de présence d'un système d'irrigation actif"),
  score_sante_sol INT64 OPTIONS(description="Score de santé biologique et de taux de matière organique du sol (0 à 100)"),
  annee_plantation INT64 OPTIONS(description="Année d'implantation de la culture ou de la vigne")
)
OPTIONS (
  description = "Cartographie détaillée des parcelles, types de sols et liaison avec le catalogue d'impact ACV Agribalyse."
);

-- 5. Table: previsions_anomalies_meteo_ete (Summer Weather Forecast Anomalies - Q1)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.previsions_anomalies_meteo_ete` (
  id_prevision STRING OPTIONS(description="Identifiant unique de la prévision météo saisonnière"),
  annee_saison STRING OPTIONS(description="Saison cible des prédictions (ex: 2026-ETE)"),
  code_departement STRING OPTIONS(description="Département concerné par la prévision météo"),
  nom_region STRING OPTIONS(description="Région administrative"),
  temperature_anomalie_c NUMERIC OPTIONS(description="Écart thermique prévisionnel moyen par rapport aux normales de saison en °C (ex: +3.4 pour +3.4°C)"),
  precipitations_anomalie_pct NUMERIC OPTIONS(description="Déficit de précipitations prévisionnel en % (ex: -38.5 pour -38.5% de pluie)"),
  indice_secheresse_evapotranspiration_prevu NUMERIC OPTIONS(description="Indice de stress hydrique prévisionnel d'été (0.0 à 1.0)"),
  baisse_rendement_predite_pct NUMERIC OPTIONS(description="Baisse de rendement estimée sur les récoltes d'été en % (Q1: filtre > 20%)")
)
OPTIONS (
  description = "Prévisions d'anomalies météorologiques climatiques pour l'été et baisse prédictive des rendements (Q1)."
);

-- 6. Table: recoltes_rendements (Harvests, Yields & Carbon Footprint)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.recoltes_rendements` (
  id_recolte STRING OPTIONS(description="Identifiant unique du lot de récolte"),
  id_parcelle STRING OPTIONS(description="Clé étrangère vers parcelles_agricoles.id_parcelle"),
  id_exploitation STRING OPTIONS(description="Clé étrangère vers exploitations_agricoles.id_exploitation"),
  annee_campagne INT64 OPTIONS(description="Année de la campagne agricole (2021, 2022, 2023, 2024, 2025)"),
  quantite_recoltee_tonnes NUMERIC OPTIONS(description="Volume total récolté en tonnes"),
  rendement_ha_tonnes NUMERIC OPTIONS(description="Rendement calculé à l'hectare en tonnes/ha"),
  taux_humidite_pct NUMERIC OPTIONS(description="Taux d'humidité moyen du grain/récolte en %"),
  score_ef_total_lot NUMERIC OPTIONS(description="Score d'empreinte environnementale total calculé sur le lot (ACV Agribalyse)"),
  emissions_co2_kg_eq NUMERIC OPTIONS(description="Émissions équivalent CO2 totales générées par le lot en kg CO2 eq"),
  prix_vente_tonne_eur NUMERIC OPTIONS(description="Prix de vente moyen départ ferme par tonne en Euros (€)"),
  statut_commercialisation STRING OPTIONS(description="Statut : VENDU_COOPERATIVE, STOCKE_FERME, VALORISE_BAS_CARBONE")
)
OPTIONS (
  description = "Historique multi-annuel des récoltes, rendements à l'hectare et empreinte carbone calculée via Agribalyse."
);

-- 7. Table: capteurs_iot_sols_meteo (IoT Sensors & Climate Risk)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.capteurs_iot_sols_meteo` (
  id_capteur STRING OPTIONS(description="Identifiant unique du capteur IoT ou de la station météo champ"),
  id_parcelle STRING OPTIONS(description="Clé étrangère vers parcelles_agricoles.id_parcelle"),
  date_releve DATE OPTIONS(description="Date du relevé journalier de télémesure"),
  humidite_sol_pct NUMERIC OPTIONS(description="Taux d'humidité volumétrique du sol en %"),
  temperature_sol_c NUMERIC OPTIONS(description="Température du sol à -10cm en °C"),
  niveau_stress_hydrique STRING OPTIONS(description="Indice de stress hydrique : FAIBLE, MODERE, SEVERE, CRITIQUE"),
  precipitations_mm NUMERIC OPTIONS(description="Hauteur de pluie cumulée en millimètres (mm)"),
  evapotranspiration_mm NUMERIC OPTIONS(description="Évapotranspiration potentielle (ET0) en mm"),
  indice_vegetation_ndvi NUMERIC OPTIONS(description="Indice de végétation satellite NDVI (0.15 à 0.85)")
)
OPTIONS (
  description = "Relevés quotidiens des capteurs connectés aux champs et indices satellitaires de santé végétale."
);

-- 8. Table: bilans_carbone_subventions_hve (Agroecological Transition & Carbon Credits - Q2)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.bilans_carbone_subventions_hve` (
  id_bilan STRING OPTIONS(description="Identifiant unique du bilan environnemental annuel"),
  id_exploitation STRING OPTIONS(description="Clé étrangère vers exploitations_agricoles.id_exploitation"),
  annee_exercice INT64 OPTIONS(description="Année comptable et environnementale"),
  bilan_co2_tonnes_evitees NUMERIC OPTIONS(description="Volume de CO2 séquestré ou évité grâce aux pratiques régénératives en tonnes"),
  montant_subvention_pac_eur NUMERIC OPTIONS(description="Aides et éco-régimes PAC perçus en Euros (€)"),
  montant_credits_carbone_eur NUMERIC OPTIONS(description="Revenus générés par la vente de crédits carbone certifiés en Euros (€)"),
  label_obtenu STRING OPTIONS(description="Certifications actives : HVE_NIVEAU_3, LABEL_BAS_CARBONE, AB_BIOLOGIQUE, EN_CONVERSION")
)
OPTIONS (
  description = "Suivi de la valeur économique créée par la transition écologiquement performante et le label bas-carbone (Q2)."
);

-- 9. Table: rapports_performance_esg_chaine (Executive ESG Supply Chain Performance Report - Q3)
CREATE OR REPLACE TABLE `agriculture_rurality_ds.rapports_performance_esg_chaine` (
  id_rapport STRING OPTIONS(description="Identifiant unique du rapport de performance ESG"),
  annee_exercice INT64 OPTIONS(description="Année d'exercice du rapport ESG (2025, 2026)"),
  filiere_principale STRING OPTIONS(description="Filière évaluée : Grandes cultures, Viticulture, Arboriculture, Elevage, Maraichage"),
  taux_exploitations_certifiees_pct NUMERIC OPTIONS(description="Taux d'exploitations partenaires certifiées HVE/Bio/Bas-Carbone en %"),
  empreinte_carbone_chaine_co2_kg_par_kg NUMERIC OPTIONS(description="Empreinte carbone moyenne globale de la chaîne d'approvisionnement en kg CO2 eq / kg de produit"),
  reduction_pesticides_pct NUMERIC OPTIONS(description="Taux de réduction d'utilisation des produits phytosanitaires (IFT) en %"),
  score_performance_esg_global INT64 OPTIONS(description="Score de maturité ESG global de la chaîne d'approvisionnement (0 à 100)"),
  synthise_investisseurs STRING OPTIONS(description="Synthèse et faits marquants pour la présentation aux investisseurs institutionnels (Q3)")
)
OPTIONS (
  description = "Rapports consolidés de performance ESG de la chaîne d'approvisionnement destinés aux investisseurs institutionnels (Q3)."
);
