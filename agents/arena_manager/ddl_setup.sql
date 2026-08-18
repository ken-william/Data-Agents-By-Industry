-- ============================================================================
-- Schema DDL for Arena Manager - Sport, Stades & Infrastructures Evénementielles
-- Dataset: sports_infrastructure_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Official RES Sports Census, Federation Licenses,
-- ANS Public Subsidies, Territorial Equipment Deficits, Arena Event Ticketing, and
-- Stadium Concessions & Merchandising Sales.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `sports_infrastructure_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Arena Manager : Recensement national des équipements sportifs (RES), données de licenciés, subventions ANS, billetterie des grands événements et ventes en buvettes/boutiques.'
);

-- 1. Table: ministere_sports_equipements (Official RES Equipment Census & Energy Audit)
CREATE OR REPLACE TABLE `sports_infrastructure_ds.ministere_sports_equipements` (
  id_equipement STRING OPTIONS(description="Identifiant unique de l'équipement sportif (ex: EQ-31500-001)"),
  nom_equipement STRING OPTIONS(description="Nom officiel du complexe ou stade (ex: Stade Ernest-Wallon, Palais des Sports)"),
  type_equipement STRING OPTIONS(description="Type d'infrastructure (Stade omnisports, Piscine olympique, Gymnase, Dojo, Court de tennis)"),
  commune STRING OPTIONS(description="Nom de la commune ou ville d'implantation"),
  departement STRING OPTIONS(description="Code département (ex: 31, 75, 69)"),
  region STRING OPTIONS(description="Région administrative (ex: Occitanie, Île-de-France, Auvergne-Rhône-Alpes)"),
  capacite_accueil_spectateurs INT64 OPTIONS(description="Capacité maximale d'accueil du public / tribunes"),
  surface_m2 NUMERIC OPTIONS(description="Surface totale praticable (en m²)"),
  etat_vetuste STRING OPTIONS(description="Évaluation de l'état du bâtiment (Neuf / Récent, Bon état, À rénover, Vétuste urgent)"),
  consommation_energetique_annuelle_mwh NUMERIC OPTIONS(description="Consommation annuelle d'énergie (en MWh)"),
  gaspillage_kwh_par_m2 NUMERIC OPTIONS(description="Consommation spécifique au m² (kWh/m²/an)"),
  taux_utilisation_semaine_pct NUMERIC OPTIONS(description="Taux moyen d'occupation du creneau en semaine (%)"),
  alerte_gaspillage_energetique BOOLEAN OPTIONS(description="Indicateur de surconsommation énergétique anormale")
)
OPTIONS (
  description = "Recensement national officiel du Ministère des Sports (RES) et diagnostic d'utilisation/performance énergétique des stades et complexes."
);

-- 2. Table: ministere_sports_licencies (Federation Licenses & Membership Growth)
CREATE OR REPLACE TABLE `sports_infrastructure_ds.ministere_sports_licencies` (
  id_licence STRING OPTIONS(description="Identifiant de la licence fédérale régionale (ex: LIC-OCC-001)"),
  region STRING OPTIONS(description="Région administrative"),
  departement STRING OPTIONS(description="Code département"),
  commune STRING OPTIONS(description="Nom de la commune"),
  federation_sportive STRING OPTIONS(description="Fédération sportive (ex: Fédération Française de Football, Rugby, Handball, Tennis, Judo)"),
  nombre_licencies_total INT64 OPTIONS(description="Nombre total d'adhérents et licenciés actifs"),
  part_jeunes_moins_18ans_pct NUMERIC OPTIONS(description="Part des jeunes de moins de 18 ans (%)"),
  croissance_licencies_pct NUMERIC OPTIONS(description="Taux de croissance annuel des adhésions (%)"),
  potentiel_sponsoring_premium_stade STRING OPTIONS(description="Évaluation du potentiel d'attraction des sponsors de stade (Élevé, Très Élevé, Standard)")
)
OPTIONS (
  description = "Suivi du nombre de licenciés par fédération sportive et potentiel de monétisation publicitaire des enceintes."
);

-- 3. Table: ministere_sports_subventions (ANS Public Grants & Renovation Funding)
CREATE OR REPLACE TABLE `sports_infrastructure_ds.ministere_sports_subventions` (
  id_subvention STRING OPTIONS(description="Identifiant unique du dossier d'aide publique (ex: SUB-ANS-2025-001)"),
  commune STRING OPTIONS(description="Commune bénéficiaire"),
  nom_association_club STRING OPTIONS(description="Nom de l'association ou du club sportif bénéficiaire"),
  montant_subvention_ans_eur NUMERIC OPTIONS(description="Montant de la subvention accordée par l'Agence Nationale du Sport (€)"),
  projet_renovation STRING OPTIONS(description="Intitulé du projet financé (Désamiantage, Éclairage LED Stade, Rénovation Thermique Gymnase)"),
  impact_hausse_inscriptions_jeunes_pct NUMERIC OPTIONS(description="Impact mesuré sur l'augmentation des inscriptions jeunes (%)"),
  cout_subvention_par_jeune_inscrit_eur NUMERIC OPTIONS(description="Coût unitaire public par nouveau jeune inscrit (€)")
)
OPTIONS (
  description = "Registres des subventions allouées par l'Agence Nationale du Sport (ANS) et retour sur investissement social/sportif."
);

-- 4. Table: ministere_sports_desequilibre_territoires (Territorial Equipment Shortages)
CREATE OR REPLACE TABLE `sports_infrastructure_ds.ministere_sports_desequilibre_territoires` (
  commune STRING OPTIONS(description="Nom de la commune"),
  departement STRING OPTIONS(description="Code département"),
  region STRING OPTIONS(description="Région administrative"),
  croissance_demographique_annuelle_pct NUMERIC OPTIONS(description="Taux de croissance démographique annuel de la population local (%)"),
  deficit_equipements_homologues_pct NUMERIC OPTIONS(description="Déficit mesuré d'équipements homologués par rapport aux besoins (%)"),
  equipement_manquant_prioritaire STRING OPTIONS(description="Type d'équipement prioritaire manquant (Piscine couverte, Terrain synthétique, Dojo, Court de tennis)")
)
OPTIONS (
  description = "Diagnostic territorial des déséquilibres entre croissance démographique et parc d'équipements sportifs homologués."
);

-- 5. Table: stades_evenements_billetterie (Arena & Stadium Events Ticketing Sales)
CREATE OR REPLACE TABLE `sports_infrastructure_ds.stades_evenements_billetterie` (
  event_id STRING OPTIONS(description="Identifiant unique de l'événement (ex: EVT-STADE-2025-001)"),
  nom_equipement STRING OPTIONS(description="Nom du stade ou arena hôte (FK -> ministere_sports_equipements)"),
  commune STRING OPTIONS(description="Commune où se situe l'enceinte"),
  nom_evenement STRING OPTIONS(description="Intitulé du match ou concert (ex: Stade Toulousain vs La Rochelle, Concert Soprano, Finale Top 14)"),
  categorie_evenement STRING OPTIONS(description="Catégorie (Match Championnat, Rencontre Internationale, Concert / Spectacle, Tournoi Jeunes)"),
  date_heure_evenement TIMESTAMP OPTIONS(description="Date et heure de coup d'envoi ou début du spectacle"),
  capacite_stade INT64 OPTIONS(description="Jauge maximale du stade"),
  billets_vendus_grand_public INT64 OPTIONS(description="Nombre de billets grand public vendus"),
  billets_vip_hospitalite_vendus INT64 OPTIONS(description="Nombre de places VIP / Loges hospitalité vendues"),
  taux_remplissage_pct NUMERIC OPTIONS(description="Taux d'occupation global du stade (%)"),
  recette_billetterie_brute_eur NUMERIC OPTIONS(description="Chiffre d'affaires brut billetterie (€)")
)
OPTIONS (
  description = "Suivi des ventes de billetterie grand public, loges VIP et taux d'occupation lors des événements sportifs et concerts."
);

-- 6. Table: stades_concessions_buvettes (Stadium Food, Beverage & Merchandising Revenues)
CREATE OR REPLACE TABLE `sports_infrastructure_ds.stades_concessions_buvettes` (
  concession_id STRING OPTIONS(description="Identifiant du stand de concession (ex: CNS-BUVETTE-01)"),
  event_id STRING OPTIONS(description="Identifiant de l'événement (FK -> stades_evenements_billetterie)"),
  nom_equipement STRING OPTIONS(description="Nom du stade ou arena"),
  nom_stand STRING OPTIONS(description="Nom du point de vente (ex: Buvette Tribune Nord, Boutique Officielle Club, Stand Snacking Est)"),
  type_stand STRING OPTIONS(description="Type de stand (Restauration / Buvette, Boutique Merchandising, Bar VIP Loges)"),
  recette_nourriture_boisson_eur NUMERIC OPTIONS(description="Recette totale Food & Beverage (€)"),
  recette_merchandising_eur NUMERIC OPTIONS(description="Recette totale maillots et produits dérivés (€)"),
  panier_moyen_par_spectateur_eur NUMERIC OPTIONS(description="Dépense moyenne effectuée par spectateur (€)")
)
OPTIONS (
  description = "Chiffre d'affaires et rentabilité des buvettes, stands de restauration et boutiques officielles de produits dérivés dans les stades."
);
