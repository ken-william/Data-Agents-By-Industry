-- ============================================================================
-- Schema DDL for Transit Navigator - Transports Publics, RATP & SNCF Intelligence Platform
-- Dataset: transport_mobility_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Authentic SNCF Open Data Gares Attendance, TGV/TER
-- Line Punctuality & Cancellations, Fare Plans, Passenger Profiles with GEOGRAPHY
-- Commute Coordinates, Station Turnstile Validations, and Lost & Found Declarations.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `transport_mobility_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Transit Navigator : Données réelles SNCF Open Data de fréquentation des gares, ponctualité/retards des lignes TGV/TER, abonnements Navigo/Pass, profil usagers et objets trouvés.'
);

-- 1. Table: frequentation_gares_sncf (Authentic SNCF Station Annual Attendance)
CREATE OR REPLACE TABLE `transport_mobility_ds.frequentation_gares_sncf` (
  code_uic_gare STRING OPTIONS(description="Code unique UIC de la gare SNCF (ex: 87743003)"),
  nom_gare STRING OPTIONS(description="Nom officiel de la gare SNCF (ex: Paris Gare de Lyon, Lyon Part-Dieu)"),
  code_postal STRING OPTIONS(description="Code postal de la gare"),
  departement_code STRING OPTIONS(description="Code département (ex: 75, 69, 13)"),
  region_nom STRING OPTIONS(description="Région administrative (ex: Île-de-France, Auvergne-Rhône-Alpes)"),
  direction_regionale_sncf STRING OPTIONS(description="Direction Régionale Gares SNCF"),
  total_voyageurs_2024 INT64 OPTIONS(description="Nombre total de voyageurs enregistrés en 2024"),
  total_voyageurs_2023 INT64 OPTIONS(description="Nombre total de voyageurs enregistrés en 2023"),
  total_voyageurs_2022 INT64 OPTIONS(description="Nombre total de voyageurs enregistrés en 2022")
)
OPTIONS (
  description = "Base officielle SNCF Open Data de la fréquentation annuelle des gares ferroviaires de France."
);

-- 2. Table: sncf_regularite_lignes (Authentic SNCF Line Punctuality & Cancellation Metrics)
CREATE OR REPLACE TABLE `transport_mobility_ds.sncf_regularite_lignes` (
  ligne_axe_id STRING OPTIONS(description="Identifiant de l'axe ferroviaire (ex: AXE-PARIS-LYON)"),
  nom_axe_ferroviaire STRING OPTIONS(description="Nom de la liaison ferroviaire (ex: Paris Lyon - Lyon Part-Dieu)"),
  gare_depart STRING OPTIONS(description="Gare d'origine du trajet"),
  gare_arrivee STRING OPTIONS(description="Gare de destination du trajet"),
  service_type STRING OPTIONS(description="Type de service ferroviaire (TGV InOui, Ouigo, TER)"),
  region STRING OPTIONS(description="Région administrative principale rattachée"),
  duree_moyenne_trajet_minutes NUMERIC OPTIONS(description="Durée moyenne nominale du parcours (en minutes)"),
  circulations_prevues_nombre INT64 OPTIONS(description="Nombre total de trains programmés sur la période"),
  nombre_trains_annules INT64 OPTIONS(description="Nombre de trains annulés"),
  retard_moyen_minutes NUMERIC OPTIONS(description="Retard moyen des trains à l'arrivée (en minutes)"),
  taux_regularite_ponctualite_pct NUMERIC OPTIONS(description="Taux de ponctualité à l'arrivée (à moins de 5 min) %"),
  cause_retard_infrastructure_pct NUMERIC OPTIONS(description="Part des retards dus à l'infrastructure et réseau (%)"),
  cause_retard_materiel_roulant_pct NUMERIC OPTIONS(description="Part des retards dus au matériel roulant (%)"),
  perte_financiere_retards_eur NUMERIC OPTIONS(description="Perte financière ou pénalités estimées pour retards/annulations (€)")
)
OPTIONS (
  description = "Suivi de la ponctualité, des retards moyens et des causes d'annulation sur les axes ferroviaires SNCF TGV et TER."
);

-- 3. Table: abonnements_titres_transport (Transport Fare Subscription Plans)
CREATE OR REPLACE TABLE `transport_mobility_ds.abonnements_titres_transport` (
  subscription_plan_id STRING OPTIONS(description="Identifiant unique du forfait (ex: SUB-NAV-MONTH, SUB-TER-ILICO)"),
  plan_name STRING OPTIONS(description="Nom commercial du forfait (Navigo Mois, Navigo Annuel, Pass TER Ilico, TGV Max, Pass Liberté+)"),
  category STRING OPTIONS(description="Catégorie d'abonnement (Urbain Île-de-France, Régional TER, Grande Vitesse TGV)"),
  monthly_price_eur NUMERIC OPTIONS(description="Prix mensuel de l'abonnement en Euros (€)"),
  valid_zones STRING OPTIONS(description="Zones géographiques autorisées (Zones 1-5, Toutes zones Région, Réseau National)"),
  is_employer_subsidized BOOLEAN OPTIONS(description="Indicateur d'éligibilité au remboursement employeur 50% Obligatoire")
)
OPTIONS (
  description = "Catalogue des forfaits d'abonnements et titres de transport public (RATP, Île-de-France Mobilités, TER, SNCF)."
);

-- 4. Table: usagers_profils (Passenger Profiles with Domicile-Work Commute Coordinates)
CREATE OR REPLACE TABLE `transport_mobility_ds.usagers_profils` (
  passenger_id STRING OPTIONS(description="Identifiant anonymisé de l'usager (ex: USG-00001)"),
  first_name STRING OPTIONS(description="Prénom de l'usager"),
  last_name STRING OPTIONS(description="Nom de l'usager"),
  email STRING OPTIONS(description="Adresse email du voyageur"),
  phone STRING OPTIONS(description="Numéro de téléphone"),
  home_city STRING OPTIONS(description="Ville de résidence"),
  department_code STRING OPTIONS(description="Code département (ex: 75, 69, 13)"),
  region_name STRING OPTIONS(description="Région administrative"),
  age_bracket STRING OPTIONS(description="Tranche d'âge (18-25 ans, 26-45 ans, 46-60 ans, 60+ ans)"),
  subscription_plan_id STRING OPTIONS(description="Forfait souscrit (FK -> abonnements_titres_transport)"),
  commute_frequency STRING OPTIONS(description="Fréquence de déplacement (Quotidien Domicile-Travail, Hebdomadaire, Occasionnel)"),
  home_location_geo GEOGRAPHY OPTIONS(description="Coordonnées GPS POINT du domicile de l'usager"),
  work_location_geo GEOGRAPHY OPTIONS(description="Coordonnées GPS POINT du lieu de travail de l'usager")
)
OPTIONS (
  description = "Répertoire des usagers et abonnés du réseau de transport avec coordonnées spatiales et caractéristiques."
);

-- 5. Table: validations_trajets_voyageurs (Passenger Turnstile Validations & Station Tap-Ins)
CREATE OR REPLACE TABLE `transport_mobility_ds.validations_trajets_voyageurs` (
  validation_id STRING OPTIONS(description="Identifiant unique du badgeage au portillon / validateur (ex: VAL-000001)"),
  passenger_id STRING OPTIONS(description="Identifiant de l'usager (FK -> usagers_profils)"),
  code_uic_gare STRING OPTIONS(description="Code UIC de la gare du badgeage (FK -> frequentation_gares_sncf)"),
  station_name STRING OPTIONS(description="Nom de la gare ou station d'entrée"),
  transport_mode STRING OPTIONS(description="Mode de transport (RER A, Métro 1, TGV InOui, TER, Tramway)"),
  line_code STRING OPTIONS(description="Code ou nom de la ligne rattachée"),
  department_code STRING OPTIONS(description="Département du lieu de validation"),
  region_name STRING OPTIONS(description="Région du lieu de validation"),
  timestamp TIMESTAMP OPTIONS(description="Horodatage exact du badgeage au portillon"),
  validation_status STRING OPTIONS(description="Statut du badgeage (VALIDE, CORRESPONDANCE, REFUSE_SOLDE, HORS_ZONE)")
)
OPTIONS (
  description = "Historique des validations et badgeages aux portillons d'entrée des gares et stations du réseau."
);

-- 6. Table: sncf_objets_trouves (Station Lost & Found Declarations & Passenger Matching)
CREATE OR REPLACE TABLE `transport_mobility_ds.sncf_objets_trouves` (
  incident_id STRING OPTIONS(description="Identifiant unique de la déclaration d'objet trouvé (ex: OBJ-00001)"),
  passenger_id STRING OPTIONS(description="Identifiant de l'usager propriétaire ou déclarant (FK -> usagers_profils)"),
  matched_journey_validation_id STRING OPTIONS(description="Identifiant de la validation de trajet associée (FK -> validations_trajets_voyageurs)"),
  code_uic_gare STRING OPTIONS(description="Code UIC de la gare de découverte ou dépôt (FK -> frequentation_gares_sncf)"),
  station_name STRING OPTIONS(description="Nom de la gare SNCF de découverte"),
  declaration_date DATE OPTIONS(description="Date de la déclaration de perte ou découverte"),
  item_category STRING OPTIONS(description="Catégorie de l'objet (Appareils Électroniques, Bagages & Valises, Papiers d'identité, Clés & Badges)"),
  item_description STRING OPTIONS(description="Description détaillée de l'objet (ex: Sac à dos noir contenant un ordinateur portable)"),
  found_status STRING OPTIONS(description="Statut de restitution (Restitué au propriétaire, En réserve gare, Transmis association)"),
  restitution_date DATE OPTIONS(description="Date de restitution effective à l'usager")
)
OPTIONS (
  description = "Registre des déclarations d'objets trouvés en gare avec rapprochement du parcours et badgeage usager."
);
