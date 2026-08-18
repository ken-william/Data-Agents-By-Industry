-- ============================================================================
-- Schema DDL for CineAnalyst - Box-Office, Fréquentation & Salles de Cinéma
-- Dataset: entertainment_cinema_ds (Project: data-agents-by-industry)
-- Relational Architecture linking CNC Official Open Data, Nationalities, 
-- Genres, Box Office Performance, and Theater Circuits.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `entertainment_cinema_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset CineAnalyst : Données réelles CNC de fréquentation du cinéma français, recettes box-office, genres, nationalités et parcs de salles.'
);

-- 1. Table: cnc_frequentation_historique (Real CNC Attendance & Revenue History)
CREATE OR REPLACE TABLE `entertainment_cinema_ds.cnc_frequentation_historique` (
  annee INT64 OPTIONS(description="Année d'observation statistique CNC"),
  entrees_totales INT64 OPTIONS(description="Nombre total d'entrées en salles de cinéma en France"),
  recette_totale_eur NUMERIC OPTIONS(description="Recette brute totale hors TSA en Euros (€)"),
  prix_moyen_ticket_eur NUMERIC OPTIONS(description="Prix moyen du billet de cinéma par entrée en Euros (€)")
)
OPTIONS (
  description = "Séries temporelles historiques CNC de fréquentation annuelle, recettes box-office et prix moyen des billets."
);

-- 2. Table: cnc_films_exploitation_nationalite (Real CNC Films by Origin)
CREATE OR REPLACE TABLE `entertainment_cinema_ds.cnc_films_exploitation_nationalite` (
  annee INT64 OPTIONS(description="Année d'exploitation en salles"),
  films_francais NUMERIC OPTIONS(description="Nombre de films français exploités ou entrées associées"),
  films_americains NUMERIC OPTIONS(description="Nombre de films américains exploités ou entrées associées"),
  films_europeens NUMERIC OPTIONS(description="Nombre de films européens hors France exploités"),
  autres_films NUMERIC OPTIONS(description="Nombre de films d'autres nationalités"),
  total_films NUMERIC OPTIONS(description="Volume total de films exploités en salles sur l'année")
)
OPTIONS (
  description = "Statistiques officielles CNC de répartition de l'offre de films en salles selon la nationalité d'origine."
);

-- 3. Table: cnc_films_nouveautes_genres (Real CNC First-Run Releases by Genre)
CREATE OR REPLACE TABLE `entertainment_cinema_ds.cnc_films_nouveautes_genres` (
  annee INT64 OPTIONS(description="Année de première exclusivité en salles"),
  films_fiction NUMERIC OPTIONS(description="Nombre de films de fiction sortis en première exclusivité"),
  films_documentaire NUMERIC OPTIONS(description="Nombre de films documentaires sortis"),
  films_animation NUMERIC OPTIONS(description="Nombre de films d'animation sortis en salles"),
  total_nouveautes NUMERIC OPTIONS(description="Nombre total de nouveaux films sortis en première exclusivité")
)
OPTIONS (
  description = "Volume annuel des nouveautés sorties en salles ventilé par genre (Fiction, Documentaire, Animation)."
);

-- 4. Table: cnc_performance_box_office_tops (Real CNC Box Office Performance Tiers)
CREATE OR REPLACE TABLE `entertainment_cinema_ds.cnc_performance_box_office_tops` (
  annee INT64 OPTIONS(description="Année du bilan de performance box-office"),
  top_10_entrees INT64 OPTIONS(description="Cumul des entrées réalisées par les 10 plus grands succès de l'année"),
  top_20_entrees INT64 OPTIONS(description="Cumul des entrées réalisées par le Top 20 des films"),
  top_30_entrees INT64 OPTIONS(description="Cumul des entrées réalisées par le Top 30 des films"),
  top_100_entrees INT64 OPTIONS(description="Cumul des entrées réalisées par le Top 100 des films")
)
OPTIONS (
  description = "Concentration des entrées et performance au box-office par paliers (Top 10, 20, 30, 100)."
);

-- 5. Table: salles_cinema_etablissements (Cinema Theater Master & Multiplex Circuits)
CREATE OR REPLACE TABLE `entertainment_cinema_ds.salles_cinema_etablissements` (
  id_salle STRING OPTIONS(description="Identifiant unique du cinéma ou multiplexe (ex: CIN_75001)"),
  nom_etablissement STRING OPTIONS(description="Nom du cinéma (ex: Pathé Alésia, UGC Ciné Cité Les Halles, CGR Torcy, MK2 Bibliothèque)"),
  circuit_cinema STRING OPTIONS(description="Circuit / Réseau : Pathé Gaumont, UGC, CGR, MK2, Kinepolis, Cinéma Indépendant"),
  commune STRING OPTIONS(description="Commune d'implantation du cinéma"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  nombre_ecrans INT64 OPTIONS(description="Nombre de salles / écrans dans l'établissement"),
  nombre_fauteuils INT64 OPTIONS(description="Capacité totale en nombre de fauteuils"),
  classification_art_et_essai BOOL OPTIONS(description="Indicateur d'art et d'essai agréé CNC")
)
OPTIONS (
  description = "Parc des salles de cinéma françaises, capacités en écrans/fauteuils et réseaux d'exploitation."
);
