-- ============================================================================
-- Schema DDL for Sully - France Travail, RH & Urssaf Intelligence Platform
-- Dataset: public_sector_employment_ds (Project: data-agents-by-industry)
-- Relational Architecture linking France Travail BMO 2025 Open Data, ROME 4.0
-- Job Taxonomy, SIRENE/Urssaf Establishments, Job Offers, Job Seekers, Dedicated
-- BigQuery CV Object Reference Table, ATS Applications, and Training Subsidies.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `public_sector_employment_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset Sully : Données réelles France Travail BMO 2025, référentiel ROME 4.0 des métiers, déclarations URSSAF/SIRENE, offres d\'emploi avec coûts de vacance et motifs de rejet, table des candidats, Object Table dédiée des CVs GCS, suivi candidatures ATS et dispositifs d\'aides à l\'embauche.'
);

-- 1. Table: bmo_recrutement_2025 (France Travail Official BMO 2025 Open Data)
CREATE OR REPLACE TABLE `public_sector_employment_ds.bmo_recrutement_2025` (
  code_metier_bmo STRING OPTIONS(description="Code métier BMO officiel France Travail (ex: A0X40, M1801, J1501)"),
  nom_metier_bmo STRING OPTIONS(description="Libellé officiel du métier BMO"),
  famille_metier_libelle STRING OPTIONS(description="Famille professionnelle (ex: Informatique et télécommunications, Santé)"),
  code_region STRING OPTIONS(description="Code région INSEE"),
  nom_region STRING OPTIONS(description="Nom de la région administrative (ex: Île-de-France, Auvergne-Rhône-Alpes, Hauts-de-France)"),
  code_departement STRING OPTIONS(description="Code département (ex: 75, 69, 59)"),
  nom_departement STRING OPTIONS(description="Nom du département"),
  code_bassin_emploi STRING OPTIONS(description="Code du bassin d'emploi France Travail (BE25)"),
  nom_bassin_emploi STRING OPTIONS(description="Nom du bassin d'emploi (ex: Bassin de Paris, Bassin de Lille, Dunkerque)"),
  projets_recrutement_nombre INT64 OPTIONS(description="Nombre total de projets de recrutement prévus"),
  recrutements_difficiles_nombre INT64 OPTIONS(description="Nombre de projets de recrutement jugés difficiles par les employeurs"),
  recrutements_saisonniers_nombre INT64 OPTIONS(description="Nombre de recrutements à caractère saisonnier"),
  part_recrutements_difficiles_pct NUMERIC OPTIONS(description="Taux de tension / difficulté de recrutement (%)")
)
OPTIONS (
  description = "Base officielle Open Data BMO (Besoins en Main d'Œuvre) 2025 de France Travail déclinée par bassin d'emploi et métier."
);

-- 2. Table: rome_arborescence_2024 (France Travail Official ROME 4.0 Taxonomy)
CREATE OR REPLACE TABLE `public_sector_employment_ds.rome_arborescence_2024` (
  code_rome STRING OPTIONS(description="Code ROME 4.0 officiel France Travail (ex: M1801, J1501, A1101)"),
  intitule_rome_appellation STRING OPTIONS(description="Libellé officiel de l'appellation / métier ROME"),
  grand_domaine_code STRING OPTIONS(description="Code de la grande famille de domaines ROME (ex: A, M, J, N)"),
  grand_domaine_libelle STRING OPTIONS(description="Libellé du grand domaine professionnel (ex: Informatique et Télécommunications, Santé)"),
  domaine_prof_code STRING OPTIONS(description="Code du domaine professionnel ROME (ex: A11, M18, J15)"),
  domaine_prof_libelle STRING OPTIONS(description="Libellé du domaine professionnel"),
  code_ogr STRING OPTIONS(description="Identifiant unique OGR France Travail de la fiche métier")
)
OPTIONS (
  description = "Répertoire officiel ROME 4.0 (Répertoire Opérationnel des Métiers et des Emplois) de France Travail avec arborescence principale et 12 255 appellations."
);

-- 3. Table: entreprises_urssaf_declarations (Company Establishments & Payroll Declarations)
CREATE OR REPLACE TABLE `public_sector_employment_ds.entreprises_urssaf_declarations` (
  siret STRING OPTIONS(description="Identifiant unique SIRET (14 chiffres) de l'établissement"),
  company_name STRING OPTIONS(description="Raison sociale / Nom de l'entreprise"),
  sector_naf STRING OPTIONS(description="Code NAF / APE d'activité principale"),
  secteur_activite_libelle STRING OPTIONS(description="Secteur d'activité en clair (Santé & Hôpitaux, Média & TV, Fabrication de Batteries, IT, BTP)"),
  legal_status STRING OPTIONS(description="Statut juridique (SA, SAS, Établissement Public, ETI)"),
  employee_count INT64 OPTIONS(description="Effectif de salariés de l'établissement"),
  total_payroll_eur NUMERIC OPTIONS(description="Masse salariale annuelle brute déclarée URSSAF (€)"),
  oeth_target_deficit_count INT64 OPTIONS(description="Déficit de bénéficiaires OETH par rapport à l'obligation Légale 6 % handicap"),
  postal_code STRING OPTIONS(description="Code postal"),
  department_code STRING OPTIONS(description="Code département (ex: 75, 59, 92)"),
  region_name STRING OPTIONS(description="Région administrative (Île-de-France, Hauts-de-France, etc.)"),
  city_name STRING OPTIONS(description="Ville du siège ou de l'établissement"),
  zone_type STRING OPTIONS(description="Classification de zone géographique (QPV - Quartier Prioritaire, ZRR, Zone Standard)")
)
OPTIONS (
  description = "Répertoire des établissements employeurs SIRENE/URSSAF avec effectifs, masse salariale et obligations OETH handicap."
);

-- 4. Table: offres_emploi_recrutement (Job Vacancies, Vacancy Costs & Candidate Rejection Motifs)
CREATE OR REPLACE TABLE `public_sector_employment_ds.offres_emploi_recrutement` (
  job_offer_id STRING OPTIONS(description="Identifiant unique de l'offre d'emploi (ex: OFFRE-2025-001)"),
  siret STRING OPTIONS(description="Code SIRET de l'entreprise recruteuse (FK -> entreprises_urssaf_declarations)"),
  company_name STRING OPTIONS(description="Nom de l'entreprise recruteuse"),
  secteur_activite_libelle STRING OPTIONS(description="Secteur d'activité en clair (Santé, Média & Télévision, Fabrication de Batteries, IT, Logistique)"),
  code_metier_bmo STRING OPTIONS(description="Code métier BMO cible (FK -> bmo_recrutement_2025)"),
  code_rome STRING OPTIONS(description="Code ROME 4.0 rattaché (FK -> rome_arborescence_2024)"),
  job_title STRING OPTIONS(description="Intitulé du poste à pourvoir"),
  contract_type STRING OPTIONS(description="Type de contrat (CDI, CDD, Alternance, Intérim)"),
  required_experience_months INT64 OPTIONS(description="Expérience minimale exigée (en mois)"),
  annual_salary_brut_eur NUMERIC OPTIONS(description="Rémunération annuelle brute proposée (€)"),
  remote_work_days INT64 OPTIONS(description="Nombre de jours de télétravail hebdomadaire autorisés"),
  department_code STRING OPTIONS(description="Département du lieu de travail"),
  region_name STRING OPTIONS(description="Région administrative du poste"),
  is_hard_to_fill BOOLEAN OPTIONS(description="Indicateur métier en tension / poste difficile à pourvoir"),
  vacance_duree_jours INT64 OPTIONS(description="Durée de vacance du poste en jours (ex: 195j > 6 mois)"),
  cout_vacance_quotidien_eur NUMERIC OPTIONS(description="Coût financier quotidien par poste vacant non pourvu (€/jour)"),
  cout_vacance_cumule_eur NUMERIC OPTIONS(description="Coût de vacance total cumulé (€)"),
  rejet_taux_pct NUMERIC OPTIONS(description="Taux de rejet / d'échec des candidatures sur l'offre (%)"),
  motif_principal_rejet STRING OPTIONS(description="Motif principal de blocage (Salaire insuffisant, Diplômes exigés, Transport/Horaires)"),
  posting_date DATE OPTIONS(description="Date de publication de l'offre"),
  closing_date DATE OPTIONS(description="Date limite de candidature")
)
OPTIONS (
  description = "Offres d'emploi actives, durées de vacance > 6 mois, coûts financiers de vacance quotidiens et motifs de rejet des candidats."
);

-- 5. Table: france_travail_demandeurs (Job Seekers & Talent Profiles)
CREATE OR REPLACE TABLE `public_sector_employment_ds.france_travail_demandeurs` (
  demandeur_id STRING OPTIONS(description="Identifiant unique du demandeur d'emploi France Travail (ex: FT-99720068)"),
  nom_prenom STRING OPTIONS(description="Nom et prénom du candidat"),
  statut_recherche STRING OPTIONS(description="Statut actuel (Recherche Active, En Formation, Emploi Reconversion)"),
  categorie_inscription STRING OPTIONS(description="Catégorie d'inscription France Travail (Catégorie A, B, C, D, E)"),
  anciennete_chomage_mois INT64 OPTIONS(description="Ancienneté d'inscription au chômage (en mois)"),
  code_metier_bmo STRING OPTIONS(description="Code métier BMO recherché (FK -> bmo_recrutement_2025)"),
  code_rome STRING OPTIONS(description="Code ROME 4.0 rattaché (FK -> rome_arborescence_2024)"),
  metier_recherche STRING OPTIONS(description="Intitulé du métier recherché"),
  department_code STRING OPTIONS(description="Code département de résidence"),
  region_name STRING OPTIONS(description="Région de résidence"),
  freins_emploi_detail STRING OPTIONS(description="Freins à l'emploi identifiés (Garde d'enfants, Mobilité sans véhicule, Exigence de rémunération)"),
  competences_actuelles STRING OPTIONS(description="Synthèse des compétences acquises et savoir-faire opérationnels"),
  niveau_etudes STRING OPTIONS(description="Niveau de diplôme (Bac, Bac+2, Bac+3, Bac+5)")
)
OPTIONS (
  description = "Répertoire propre des candidats et demandeurs d'emploi inscrits à France Travail."
);

-- 6. Table: france_travail_cv_object_table (Dedicated Native BigQuery Object Reference Table for Candidate Resumes)
CREATE OR REPLACE TABLE `public_sector_employment_ds.france_travail_cv_object_table` (
  demandeur_id STRING OPTIONS(description="Identifiant du candidat (FK -> france_travail_demandeurs)"),
  uri STRING OPTIONS(description="URI Cloud Storage du CV du candidat (gs://sully-candidate-resumes-data-agents/resumes/cv_*.pdf)"),
  generation INT64 OPTIONS(description="Numéro de génération de l'objet GCS"),
  content_type STRING OPTIONS(description="Type MIME de l'objet (application/pdf)"),
  size INT64 OPTIONS(description="Taille du fichier CV en octets"),
  md5_hash STRING OPTIONS(description="Hash MD5 de vérification d'intégrité de l'objet GCS"),
  updated TIMESTAMP OPTIONS(description="Horodatage de dernière modification du CV sur GCS"),
  metadata ARRAY<STRUCT<name STRING, value STRING>> OPTIONS(description="Métadonnées clés-valeurs associées à l'objet GCS (ex: candidate_name, document_type)")
)
OPTIONS (
  description = "Table d'Objets d'ingestion native BigQuery (Object Table Schema) établissant le lien entre le demandeur d'emploi et son fichier CV hébergé sur GCS."
);

-- 7. Table: candidatures_postulations_suivi (ATS Job Applications & Hiring Funnel)
CREATE OR REPLACE TABLE `public_sector_employment_ds.candidatures_postulations_suivi` (
  application_id STRING OPTIONS(description="Identifiant unique de la candidature ATS (ex: APP-0001)"),
  demandeur_id STRING OPTIONS(description="Identifiant du candidat (FK -> france_travail_demandeurs)"),
  job_offer_id STRING OPTIONS(description="Identifiant de l'offre postulée (FK -> offres_emploi_recrutement)"),
  siret STRING OPTIONS(description="Code SIRET de l'employeur (FK -> entreprises_urssaf_declarations)"),
  company_name STRING OPTIONS(description="Nom de l'entreprise recruteuse"),
  application_date TIMESTAMP OPTIONS(description="Horodatage du dépôt de la candidature"),
  current_status STRING OPTIONS(description="Statut dans le funnel ATS (Candidature Transmise, Entretien RH, Offre d'Embauche, Refusé)"),
  ats_matching_score_pct NUMERIC OPTIONS(description="Score de correspondance algorithmique ATS (%)"),
  motif_refus_detail STRING OPTIONS(description="Raison explicite du refus si statut Refusé"),
  last_status_update TIMESTAMP OPTIONS(description="Horodatage du dernier changement de statut")
)
OPTIONS (
  description = "Suivi dynamique des candidatures et parcours dans le tunnel de recrutement ATS avec motifs de refus."
);

-- 8. Table: france_travail_formations_aides (Vocational Training & Subsidies POEI/AFPR/PMSMP)
CREATE OR REPLACE TABLE `public_sector_employment_ds.france_travail_formations_aides` (
  aide_id STRING OPTIONS(description="Identifiant unique du dossier d'aide ou de formation (ex: AIDE-001)"),
  demandeur_id STRING OPTIONS(description="Identifiant du demandeur bénéficiaire (FK -> france_travail_demandeurs)"),
  siret STRING OPTIONS(description="Code SIRET de l'entreprise d'accueil (FK -> entreprises_urssaf_declarations)"),
  nom_aide_dispositif STRING OPTIONS(description="Dispositif public mobilisé (AFPR, POEI, PMSMP Immersion 15j, Aid'Emploi ZFU, AGEFIPH)"),
  montant_aide_accordee_eur NUMERIC OPTIONS(description="Montant de l'aide ou de la prise en charge formation (€)"),
  date_debut_aide DATE OPTIONS(description="Date de début du dispositif"),
  date_expiration_aide DATE OPTIONS(description="Date de fin / d'échéance du dispositif"),
  statut_aide STRING OPTIONS(description="Statut du dossier (Accordée, En cours de versement, Clôturée)"),
  organisme_financeur STRING OPTIONS(description="Organisme financeur (France Travail, Région, Opco AKTO, Opco Atlas, Agefiph)")
)
OPTIONS (
  description = "Dispositifs d'aide à l'embauche, formations préalables à l'emploi et financements publics mobilisés."
);
