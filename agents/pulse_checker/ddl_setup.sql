-- ============================================================================
-- Schema DDL for PulseChecker - Santé, Urgences Hospitalières, FINESS & Open BIO
-- Dataset: healthcare_medical_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Official FINESS French Hospital Master,
-- Emergency Room Occupancy, Surgical Operating Blocks, Drug Shortages, Medical Staff Plannings,
-- and Official Assurance Maladie Open Bio Medical Biology Expenses.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `healthcare_medical_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset PulseChecker : Operations hospitalieres, urgences, lits, blocs operatoires, medicaments et depenses Open Bio de l Assurance Maladie.'
);

-- 1. Table: finess_etablissements_sante (Official FINESS Master of French Hospitals, CHU & Clinics)
CREATE OR REPLACE TABLE `healthcare_medical_ds.finess_etablissements_sante` (
  id_finess_etablissement STRING OPTIONS(description="Identifiant unique FINESS de l'établissement de santé"),
  nom_etablissement STRING OPTIONS(description="Nom officiel ou raison sociale de l'hôpital/clinique"),
  categorie_etablissement STRING OPTIONS(description="Catégorie : CHU Centre Hospitalier Universitaire, CH Général, Clinique Privée"),
  commune STRING OPTIONS(description="Commune d'implantation de l'établissement"),
  code_postal STRING OPTIONS(description="Code postal français à 5 chiffres"),
  code_departement STRING OPTIONS(description="Département d'implantation (ex: 33 - Gironde, 75 - Paris)"),
  nom_region STRING OPTIONS(description="Région administrative"),
  capacite_totale_lits INT64 OPTIONS(description="Nombre total de lits d'hospitalisation autorisés"),
  capacite_lits_reanimation INT64 OPTIONS(description="Nombre de lits de réanimation et soins intensifs"),
  capacite_lits_urgences INT64 OPTIONS(description="Nombre de lits/brancards d'accueil des urgences"),
  latitude NUMERIC OPTIONS(description="Coordonnée géographique latitude (WGS84)"),
  longitude NUMERIC OPTIONS(description="Coordonnée géographique longitude (WGS84)")
)
OPTIONS (
  description = "Répertoire master FINESS des hôpitaux, CHU, CHR et cliniques privées de France."
);

-- 2. Table: hopitaux_flux_admissions_urgences (Emergency Room Admissions, Wait Times & Plan Blanc)
CREATE OR REPLACE TABLE `healthcare_medical_ds.hopitaux_flux_admissions_urgences` (
  id_releve_urgences STRING OPTIONS(description="Identifiant unique du relevé horaire aux urgences"),
  id_finess_etablissement STRING OPTIONS(description="Clé étrangère vers finess_etablissements_sante.id_finess_etablissement"),
  nom_etablissement STRING OPTIONS(description="Nom du centre hospitalier"),
  commune STRING OPTIONS(description="Commune de l'hôpital"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  horodate_pas_1heure TIMESTAMP OPTIONS(description="Horodate exacte du relevé horaire des urgences"),
  nombre_admissions_heure INT64 OPTIONS(description="Nombre de nouveaux patients enregistrés sur l'heure"),
  temps_attente_moyen_minutes INT64 OPTIONS(description="Temps d'attente moyen avant prise en charge médicale en minutes"),
  taux_occupation_lits_urgences_pct NUMERIC OPTIONS(description="Taux d'occupation des lits et brancards d'urgences (%)"),
  statut_tension_urgences STRING OPTIONS(description="Indicateur de tension : TENSION_EXTREME_PLAN_BLANC, SOUS_TENSION, NORMAL")
)
OPTIONS (
  description = "Suivi horaire de l'affluence aux urgences, temps d'attente et déclenchement des plans blancs hospitaliers."
);

-- 3. Table: hopitaux_blocs_operatoires_chirurgie (Surgical Operating Rooms & ICU Bed Capacity)
CREATE OR REPLACE TABLE `healthcare_medical_ds.hopitaux_blocs_operatoires_chirurgie` (
  id_bloc_operatoire STRING OPTIONS(description="Identifiant du bloc opératoire"),
  id_finess_etablissement STRING OPTIONS(description="Clé étrangère vers finess_etablissements_sante"),
  nom_etablissement STRING OPTIONS(description="Nom de l'établissement hospitalier"),
  specialite_chirurgicale STRING OPTIONS(description="Spécialité : Chirurgie Viscérale, Orthopédie, Neurologie, Cardiologie, Oncologie"),
  nombre_salles_operatoires INT64 OPTIONS(description="Nombre de salles d'opération actives"),
  taux_utilisation_bloc_pct NUMERIC OPTIONS(description="Taux d'occupation moyen du bloc opératoire (%)"),
  nombre_interventions_programmees INT64 OPTIONS(description="Nombre d'interventions chirurgicales programmées sur la semaine"),
  nombre_interventions_urgentes INT64 OPTIONS(description="Nombre d'urgences chirurgicales non programmées déroutées"),
  delai_moyen_attente_chirurgie_jours INT64 OPTIONS(description="Délai moyen d'accès à la chirurgie en jours")
)
OPTIONS (
  description = "Gestion de l'activité des blocs opératoires hospitaliers et programmation chirurgicale."
);

-- 4. Table: pharmacie_stock_medicaments_tension (Hospital Pharmacy Stocks & Critical Drug Shortages)
CREATE OR REPLACE TABLE `healthcare_medical_ds.pharmacie_stock_medicaments_tension` (
  id_medicament STRING OPTIONS(description="Identifiant unique de la référence pharmacie"),
  id_finess_etablissement STRING OPTIONS(description="Clé étrangère vers finess_etablissements_sante"),
  nom_etablissement STRING OPTIONS(description="Nom de l'hôpital"),
  code_cip13 STRING OPTIONS(description="Code CIP13 officiel du médicament ou dispositif médical"),
  nom_substance_active STRING OPTIONS(description="Dénomination Commune Internationale (ex: Amoxicilline, Paracétamol IV, Insuline, Propofol)"),
  quantite_en_stock_doses INT64 OPTIONS(description="Volume de doses/unités actuellement en stock à la pharmacie à usage intérieur (PUI)"),
  jours_autonomie_restants INT64 OPTIONS(description="Nombre de jours d'autonomie estimé avant rupture totale de stock"),
  statut_approvisionnement STRING OPTIONS(description="Statut : RUPTURE_AVEREE_CRITIQUE, REAPPROVISIONNEMENT_TENDU, STOCK_CONFORME")
)
OPTIONS (
  description = "Tensions d'approvisionnement en médicaments essentiels et ruptures de stock à la pharmacie hospitalière (PUI)."
);

-- 5. Table: personnel_medical_garde_planning (Medical Staffing On-Call Plannings & Absenteeism)
CREATE OR REPLACE TABLE `healthcare_medical_ds.personnel_medical_garde_planning` (
  id_planning STRING OPTIONS(description="Identifiant du roulement ou gardes de service"),
  id_finess_etablissement STRING OPTIONS(description="Clé étrangère vers finess_etablissements_sante"),
  nom_etablissement STRING OPTIONS(description="Nom de l'établissement de santé"),
  categorie_personnel STRING OPTIONS(description="Profil : Médecins Urgentistes, Anesthésistes Réanimateurs, Infirmiers IDE, Aides-Soignants"),
  effectif_present INT64 OPTIONS(description="Nombre de soignants effectivement présents de garde"),
  effectif_requis_h24 INT64 OPTIONS(description="Nombre théorique de soignants requis pour la sécurité des soins"),
  taux_absenteisme_pct NUMERIC OPTIONS(description="Taux d'absentéisme constaté dans l'équipe (%)"),
  nombre_heures_supplementaires_semaine NUMERIC OPTIONS(description="Volume moyen d'heures supplémentaires accumulées par soignant"),
  statut_garde STRING OPTIONS(description="Statut : GARDE_CONFORME, SOUS_EFFECTIF_SEVERE")
)
OPTIONS (
  description = "Planning des gardes médicales, suivi des sous-effectifs et absentéisme soignant."
);

-- 6. Table: assurance_maladie_open_bio_depenses (Official Ameli Open Bio Medical Biology Expenses)
CREATE OR REPLACE TABLE `healthcare_medical_ds.assurance_maladie_open_bio_depenses` (
  annee INT64 OPTIONS(description="Année de comptabilisation des actes de biologie médicale"),
  code_groupe_biologie INT64 OPTIONS(description="Code officiel du groupe d'actes de biologie médicale (ex: 1=Hématologie, 2=Biochimie, 4=Microbiologie)"),
  libelle_groupe_biologie STRING OPTIONS(description="Libellé du groupe d'actes (Hématologie courante, Biochimie, Microbiologie, Immunologie)"),
  code_region_beneficiaire STRING OPTIONS(description="Code région du bénéficiaire selon le référentiel INSEE / CNAM"),
  nom_region STRING OPTIONS(description="Région administrative du bénéficiaire"),
  nombre_beneficiaires_consommateurs INT64 OPTIONS(description="Nombre total de patients bénéficiaires consommateurs d'actes sur l'année"),
  nombre_actes_biologie_realises INT64 OPTIONS(description="Dénombrement total des actes de biologie médicale exécutés"),
  montant_base_remboursement_eur NUMERIC OPTIONS(description="Montant total de la base de remboursement en Euros (€)"),
  montant_rembourse_assurance_maladie_eur NUMERIC OPTIONS(description="Montant total pris en charge et remboursé par l'Assurance Maladie (€)")
)
OPTIONS (
  description = "Séries statistiques officielles Open Bio de l'Assurance Maladie sur les dépenses et volumes d'actes de biologie médicale en France."
);
