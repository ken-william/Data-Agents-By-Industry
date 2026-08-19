-- ============================================================================
-- Schema DDL for Transit Navigator - Transports Publics, RATP & SNCF Intelligence Platform
-- Dataset: transport_mobility_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Authentic SNCF Open Data Gares Attendance, TGV/TER
-- Line Punctuality & Cancellations, TER Predictive Maintenance 6-Month Time-Series,
-- Yield Management 1st/2nd Class Pricing, Fare Plans, Passenger Profiles with GEOGRAPHY,
-- Station Turnstile Validations, and Lost & Found Declarations.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `transport_mobility_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Transit Navigator : Données réelles SNCF Open Data de fréquentation des gares, ponctualité/retards TGV/TER, maintenance prédictive 6 mois TER (3m historique + 3m prévisions), tarification dynamique Yield 1ère/2nde classe, abonnements Navigo/Pass, profil usagers et objets trouvés.'
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
  service_type STRING OPTIONS(description="Type de service ferroviaire (TGV InOui, Ouigo, TER Régional, Transilien)"),
  region STRING OPTIONS(description="Région administrative principale rattachée"),
  duree_moyenne_trajet_minutes NUMERIC OPTIONS(description="Durée moyenne nominale du parcours (en minutes)"),
  circulations_prevues_nombre INT64 OPTIONS(description="Nombre total de trains programmés sur la période"),
  nombre_trains_annules INT64 OPTIONS(description="Nombre de trains annulés"),
  retard_moyen_minutes NUMERIC OPTIONS(description="Retard moyen des trains à l'arrivée (en minutes)"),
  taux_regularite_ponctualite_pct NUMERIC OPTIONS(description="Taux de ponctualité à l'arrivée (à moins de 5 min) %"),
  cause_retard_infrastructure_pct NUMERIC OPTIONS(description="Part des retards dus à l'infrastructure et signalisation (%)"),
  cause_retard_materiel_roulant_pct NUMERIC OPTIONS(description="Part des retards dus aux pannes de matériel roulant (%)"),
  cause_retard_gestion_trafic_pct NUMERIC OPTIONS(description="Part des retards dus à la régulation et surcroissance du trafic (%)"),
  perte_financiere_retards_eur NUMERIC OPTIONS(description="Perte financière ou pénalités estimées pour retards/annulations (€)")
)
OPTIONS (
  description = "Suivi de la ponctualité, des retards moyens et des causes d'annulation sur les axes ferroviaires SNCF TGV et TER."
);

-- 3. Table: ter_maintenance_predictive_reseau (TER Network Predictive Maintenance 7-Day & Current Risk)
CREATE OR REPLACE TABLE `transport_mobility_ds.ter_maintenance_predictive_reseau` (
  segment_id STRING OPTIONS(description="Identifiant unique du tronçon ferroviaire (ex: SEG-TER-AURA-01)"),
  nom_segment_ferroviaire STRING OPTIONS(description="Intitulé du segment TER (ex: Segment TER Lyon Part-Dieu - Grenoble Section Moirans)"),
  region STRING OPTIONS(description="Région administrative (Auvergne-Rhône-Alpes, PACA, Hauts-de-France, Occitanie, Île-de-France)"),
  line_code STRING OPTIONS(description="Code de la ligne TER (ex: TER Ligne 1, TER Ligne 4, RER C Sud)"),
  charge_trafic_semaine_pct NUMERIC OPTIONS(description="Taux de charge et sursurcharge de trafic hebdomadaire (%)"),
  age_infrastructure_annees NUMERIC OPTIONS(description="Âge moyen des rails et caténaires (années)"),
  frequence_micro_coupures_signalisation_30j INT64 OPTIONS(description="Nombre de micro-coupures de signalisation relevées sur 30 jours"),
  usure_rail_mm NUMERIC OPTIONS(description="Niveau d'usure mécanique des rails (mm)"),
  probabilite_panne_materielle_7j NUMERIC OPTIONS(description="Probabilité prédite de panne matérielle d'ici la semaine prochaine (0.0 à 1.0)"),
  risque_ralentissement_majeur STRING OPTIONS(description="Statut de risque de ralentissement (CRITIQUE, ÉLEVÉ, MODÉRÉ, FAIBLE)"),
  cause_principale_risque STRING OPTIONS(description="Diagnostic principal (Surcharge de trafic & Usure caténaire, Signalisation obsolète, Usure bogies rames TER)"),
  action_maintenance_recommandee STRING OPTIONS(description="Consigne d'intervention préventive (ex: Remplacement préventif d'aiguillage & Limitation temporaire de vitesse 80km/h)")
)
OPTIONS (
  description = "Module de maintenance prédictive pour anticiper les pannes matérielles et ralentissements majeurs sur le réseau TER."
);

-- 4. Table: ter_maintenance_historique_previsions_6mois (3 Months History + 3 Months Prediction Time-Series)
CREATE OR REPLACE TABLE `transport_mobility_ds.ter_maintenance_historique_previsions_6mois` (
  segment_id STRING OPTIONS(description="Identifiant unique du tronçon ferroviaire TER (ex: SEG-TER-AURA-01)"),
  nom_segment_ferroviaire STRING OPTIONS(description="Nom du segment ferroviaire TER (ex: Segment TER Lyon Part-Dieu - Grenoble)"),
  region STRING OPTIONS(description="Région administrative (Auvergne-Rhône-Alpes, Île-de-France, PACA, etc.)"),
  line_code STRING OPTIONS(description="Code de la ligne TER ou RER (ex: TER Ligne 1, RER C)"),
  mois_date DATE OPTIONS(description="Mois de référence de la mesure ou prévision (du 2026-05-01 au 2026-10-01)"),
  periode_type STRING OPTIONS(description="Type de période (HISTORIQUE 3 Mois Passés, PRÉVISION 3 Mois Futurs)"),
  charge_trafic_mensuelle_pct NUMERIC OPTIONS(description="Taux de charge du trafic ferroviaire mensuel (%)"),
  frequence_micro_coupures_signalisation INT64 OPTIONS(description="Nombre de micro-coupures de signalisation observées ou prédites dans le mois"),
  usure_rail_mm NUMERIC OPTIONS(description="Niveau d'usure mécanique cumulé des rails (mm)"),
  probabilite_panne_materielle NUMERIC OPTIONS(description="Probabilité observée ou prédite de panne matérielle (0.00 à 1.00)"),
  risque_ralentissement_majeur STRING OPTIONS(description="Niveau de risque de ralentissement (CRITIQUE, ÉLEVÉ, MODÉRÉ, FAIBLE)"),
  cause_principale_risque STRING OPTIONS(description="Cause principale du risque (Usure rails, Signalisation obsolète, Surcroissance trafic)"),
  action_maintenance_recommandee STRING OPTIONS(description="Consigne d'intervention préventive préconisée pour le mois")
)
OPTIONS (
  description = "Série temporelle complète sur 6 mois : 3 mois d'historique (Mai - Juillet 2026) et 3 mois de prévisions (Août - Octobre 2026) du risque de pannes TER."
);

-- 5. Table: sncf_yield_management_billetterie (Dynamic Pricing & 1st vs 2nd Class Upsell Optimization)
CREATE OR REPLACE TABLE `transport_mobility_ds.sncf_yield_management_billetterie` (
  ticket_offer_id STRING OPTIONS(description="Identifiant unique de l'offre tarifaire (ex: YIELD-TGV-6902)"),
  train_number STRING OPTIONS(description="Numéro du train (ex: TGV 6902, TER 84210)"),
  ligne_axe_id STRING OPTIONS(description="Identifiant de l'axe rattaché (FK -> sncf_regularite_lignes)"),
  nom_axe_ferroviaire STRING OPTIONS(description="Nom de la ligne ferroviaire"),
  classe_billet STRING OPTIONS(description="Classe de réservation (1ère Classe, 2nde Classe)"),
  tarif_nominal_eur NUMERIC OPTIONS(description="Tarif plein nominal du billet (€)"),
  tarif_dynamique_propose_eur NUMERIC OPTIONS(description="Tarif ajusté par l'algorithme de Yield Management (€)"),
  taux_occupation_1ere_classe_pct NUMERIC OPTIONS(description="Taux de remplissage constaté de la 1ère classe (%)"),
  taux_occupation_2nde_classe_pct NUMERIC OPTIONS(description="Taux de remplissage constaté de la 2nde classe (%)"),
  panier_moyen_actuel_eur NUMERIC OPTIONS(description="Panier moyen constaté par voyageur (€)"),
  hausse_panier_moyen_projete_pct NUMERIC OPTIONS(description="Projection de hausse du panier moyen (% d'augmentation visée)"),
  recommandation_pricing_yield STRING OPTIONS(description="Recommandation d'ajustement tarifaire pour maximiser la marge et le panier moyen (+12%)")
)
OPTIONS (
  description = "Système de tarification dynamique, Yield Management et sous-exploitation de la 1ère classe pour booster le panier moyen."
);

-- 6. Table: abonnements_titres_transport (Transport Fare Subscription Plans)
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

-- 7. Table: usagers_profils (Passenger Profiles with Domicile-Work Commute Coordinates)
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

-- 8. Table: validations_trajets_voyageurs (Passenger Turnstile Validations & Station Tap-Ins)
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

-- 9. Table: sncf_objets_trouves (Station Lost & Found Declarations & Passenger Matching)
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
