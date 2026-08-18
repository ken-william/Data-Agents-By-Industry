-- ============================================================================
-- Schema DDL for CineAnalyst - Box-Office, Fréquentation & Salles de Cinéma
-- Dataset: cinema_boxoffice_ds (Project: data-agents-by-industry)
-- Relational Architecture linking CNC Official Open Data, Nationalities, 
-- Genres, Individual Movie Titles & Budgets, Flop Risk & Social Buzz, Formats (IMAX/4DX), and Theater Circuits.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `cinema_boxoffice_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset CineAnalyst : Données réelles CNC de fréquentation du cinéma français, recettes box-office, nouveautés par titre, prédictions de flops, formats de salles et parcs de cinémas.'
);

-- 1. Table: cnc_frequentation_historique (Real CNC Attendance & Revenue History)
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.cnc_frequentation_historique` (
  annee INT64 OPTIONS(description="Année d'observation statistique CNC"),
  entrees_totales INT64 OPTIONS(description="Nombre total d'entrées en salles de cinéma en France"),
  recette_totale_eur NUMERIC OPTIONS(description="Recette brute totale hors TSA en Euros (€)"),
  prix_moyen_ticket_eur NUMERIC OPTIONS(description="Prix moyen du billet de cinéma par entrée en Euros (€)")
)
OPTIONS (
  description = "Séries temporelles historiques CNC de fréquentation annuelle, recettes box-office et prix moyen des billets."
);

-- 2. Table: cnc_films_exploitation_nationalite (Real CNC Films by Origin)
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.cnc_films_exploitation_nationalite` (
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
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.cnc_films_nouveautes_genres` (
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
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.cnc_performance_box_office_tops` (
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
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.salles_cinema_etablissements` (
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

-- 6. Table: cnc_films_nouveautes_titres_boxoffice (Individual Movie Titles, Budgets, 1st Week Admissions, Flop Risk & Social Buzz)
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.cnc_films_nouveautes_titres_boxoffice` (
  movie_id STRING OPTIONS(description="Identifiant unique du film (ex: FILM-2025-001)"),
  titre_film STRING OPTIONS(description="Titre officiel du film en salles"),
  genre STRING OPTIONS(description="Genre du film (Fiction, Animation, Documentaire)"),
  nationalite STRING OPTIONS(description="Nationalité principale de production (Français, Américain, Européen)"),
  budget_production_eur NUMERIC OPTIONS(description="Budget de production officiel en Euros (€)"),
  date_sortie_salles DATE OPTIONS(description="Date de première sortie nationale en salles"),
  entrees_premiere_semaine INT64 OPTIONS(description="Nombre d'entrées réalisées en 1ère semaine d'exploitation"),
  entrees_cumulees_total INT64 OPTIONS(description="Nombre total d'entrées cumulées en fin d'exploitation"),
  semaines_affiche INT64 OPTIONS(description="Nombre de semaines de maintien à l'affiche"),
  coefficient_maintien_semaine2 NUMERIC OPTIONS(description="Ratio de maintien d'entrées entre semaine 2 et semaine 1 (>0.75 = excellent)"),
  index_buzz_reseaux_sociaux NUMERIC OPTIONS(description="Indice de sentiment et volume de mentions réseaux sociaux (0.0 à 100.0)"),
  risque_flop_box_office_pct NUMERIC OPTIONS(description="Score de risque de flop au box-office en pourcentage (%)")
)
OPTIONS (
  description = "Fiche détaillée des films nouveautés : entrées 1ère semaine, budget, maintien à l'affiche, buzz réseaux sociaux et prédiction de flop."
);

-- 7. Table: salles_formats_projection_frequentation (IMAX 3D, 4DX Immersif, Dolby Cinema vs Standard)
CREATE OR REPLACE TABLE `cinema_boxoffice_ds.salles_formats_projection_frequentation` (
  format_id STRING OPTIONS(description="Identifiant du format (ex: FMT-001)"),
  nom_format_projection STRING OPTIONS(description="Format de salle (Standard 2D, IMAX 3D, 4DX Immersif, Dolby Cinema, ScreenX 270°)"),
  taux_occupation_moyen_seance_pct NUMERIC OPTIONS(description="Taux d'occupation moyen des fauteuils par séance (%)"),
  prix_moyen_billet_format_eur NUMERIC OPTIONS(description="Prix moyen du ticket d'entrée pour ce format (€)"),
  surcout_prix_billet_pct NUMERIC OPTIONS(description="Surcoût tarifaire appliqué par rapport au tarif standard (%)"),
  recette_annuelle_par_fauteuil_eur NUMERIC OPTIONS(description="Recette brute générée par fauteuil par an (€)")
)
OPTIONS (
  description = "Comparatif de performance des formats de projection premium (IMAX, 4DX, Dolby Cinema) vs Standard : taux d'occupation des fauteuils par séance et prix du billet."
);
