-- ============================================================================
-- Dataset and Table DDL for CreditAdvisor 360° Executive Copilot (FSI Banque & Assurance)
-- Triple Volume Macroeconomic & Microeconomic Data Engine (2018-2026 Time Series)
-- Supports Q1 to Q11: CRO Risk, CFO Margins & RAROC, Sales Growth & Retention
-- Dataset Name: fsi_creditadvisor_dataset
-- ============================================================================

-- 1. Create Schema / Dataset
CREATE SCHEMA IF NOT EXISTS `fsi_creditadvisor_dataset`
OPTIONS (
  location = 'EU',
  description = 'Dataset 360° FSI Banque & Assurance pour CreditAdvisor : 9 ans de séries temporelles Banque de France (2018-2026), bilans financiers enrichis, IFRS 9 ECL, stress-tests, RAROC, LTV et signaux faibles.'
);

-- ----------------------------------------------------------------------------
-- MICRO-ECONOMIC TABLES (Portefeuilles, Bilans, RAROC, LTV, Signaux Faibles)
-- ----------------------------------------------------------------------------

-- 2. Table: entreprises (Companies Master & Supply Chain Anchors)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.entreprises` (
  id_entreprise STRING OPTIONS(description="Identifiant unique de l'entreprise (ex: ENT_100042 / UUID)"),
  nom_entreprise STRING OPTIONS(description="Raison sociale ou nom commercial officiel"),
  siren STRING OPTIONS(description="Numéro SIREN à 9 chiffres de l'entreprise"),
  categorie_entreprise STRING OPTIONS(description="Catégorie d'entreprise : PME, ETI, Grande Entreprise, Micro-entreprise"),
  secteur_activite STRING OPTIONS(description="Secteur d'activité principal : Commerce, Industrie, BTP, Technologies, Agroalimentaire, Transport, Immobilier, Aéronautique, Automobile"),
  code_naf STRING OPTIONS(description="Code NAF/APE officiel (ex: 4120A, 6201Z, 3030Z)"),
  code_region STRING OPTIONS(description="Code administratif de la région (ex: OCC, IDF, PACA, ARA, NAQ)"),
  nom_region STRING OPTIONS(description="Nom complet de la région administrative française (ex: Occitanie, Île-de-France, PACA, Auvergne-Rhône-Alpes)"),
  ville STRING OPTIONS(description="Ville du siège social de l'entreprise"),
  code_postal STRING OPTIONS(description="Code postal français du siège social"),
  effectif INT64 OPTIONS(description="Nombre total de salariés de l'entreprise"),
  donneur_ordre_principal STRING OPTIONS(description="Grand donneur d'ordre ou client ancrage filière/supply chain (ex: AIRBUS_GROUP, SAFRAN, RENAULT_GROUP, STELLANTIS, THALES, AUCUN)"),
  date_creation DATE OPTIONS(description="Date d'immatriculation légale de l'entreprise")
)
OPTIONS (
  description = "Master entreprises avec typologie filière/supply chain pour l'analyse des risques de concentration (Q6)."
);

-- 3. Table: bilans_financiers (Multi-Year Balance Sheets, Weak Signals & Ratings)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.bilans_financiers` (
  id_bilan STRING OPTIONS(description="Identifiant unique du bilan financier"),
  id_entreprise STRING OPTIONS(description="Clé étrangère vers entreprises.id_entreprise"),
  annee_exercice INT64 OPTIONS(description="Année comptable de l'exercice (2021, 2022, 2023, 2024, 2025)"),
  chiffre_affaires_eur NUMERIC OPTIONS(description="Chiffre d'affaires annuel comptable en Euros (€)"),
  ebe_ebitda_eur NUMERIC OPTIONS(description="Excédent Brut d'Exploitation (EBITDA) en Euros (€)"),
  resultat_net_eur NUMERIC OPTIONS(description="Résultat net comptable après impôts en Euros (€)"),
  fonds_propres_eur NUMERIC OPTIONS(description="Capitaux propres / Fonds propres comptables en Euros (€)"),
  dette_financiere_brute_eur NUMERIC OPTIONS(description="Dette financière brute totale en Euros (€)"),
  tresorerie_nette_eur NUMERIC OPTIONS(description="Trésorerie disponible et équivalents de trésorerie en Euros (€)"),
  bfr_eur NUMERIC OPTIONS(description="Besoin en Fonds de Roulement (BFR) en Euros (€)"),
  ratio_dscr NUMERIC OPTIONS(description="Debt Service Coverage Ratio (EBE / Service de la dette annuel). DSCR < 1.15 = alerte risque."),
  ratio_icr NUMERIC OPTIONS(description="Interest Coverage Ratio (EBE / Charges d'intérêts). ICR < 1.5 = sensibilité aux taux."),
  ratio_endettement NUMERIC OPTIONS(description="Ratio d'endettement net (Dette Nette / Fonds Propres)."),
  notation_interne STRING OPTIONS(description="Notation interne de crédit de la banque : A (Excellente), B (Bonne), C (Vigilance), D (Défaillante)"),
  variation_flux_tresorerie_6m_pct NUMERIC OPTIONS(description="Variation relative du flux de trésorerie sur 6 mois en % (signal faible si < -20%)"),
  delai_paiement_clients_jours INT64 OPTIONS(description="Délai moyen de paiement des clients en jours (signal faible d'asymptomatique si > 60 jours)"),
  score_sante_financiere INT64 OPTIONS(description="Score global de 0 à 100. Score >= 75 indique une PME très solide.")
)
OPTIONS (
  description = "Bilans financiers enrichis avec signaux faibles (flux trésorerie, délais de paiement) et notation interne (Q5, Q7)."
);

-- 4. Table: encours_credit (Credit Lines, RAROC, LTV, Securitization & Churn)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.encours_credit` (
  id_credit STRING OPTIONS(description="Identifiant unique du contrat ou de la ligne de crédit"),
  id_entreprise STRING OPTIONS(description="Clé étrangère vers entreprises.id_entreprise"),
  type_credit STRING OPTIONS(description="Type de crédit : Crédit d'investissement, Crédit bail, Prêt de trésorerie, Crédit revolving, Prêt immobilier pro"),
  montant_initial_eur NUMERIC OPTIONS(description="Capital initial accordé en Euros (€)"),
  montant_encours_eur NUMERIC OPTIONS(description="Encours restant dû (EAD - Exposure at Default) en Euros (€)"),
  taux_interet_actuel NUMERIC OPTIONS(description="Taux d'intérêt effectif annuel en % (ex: 4.50 pour 4.50%)"),
  marge_banque_bps NUMERIC OPTIONS(description="Marge commerciale nette attribuée à la banque en points de base (ex: 180 bps = 1.80%)"),
  raroc_pct NUMERIC OPTIONS(description="Risk-Adjusted Return on Capital (RAROC) en % pour l'optimisation de la rentabilité (Q7)"),
  taux_variable BOOL OPTIONS(description="TRUE si le taux est variable indexé sur Euribor"),
  date_debut DATE OPTIONS(description="Date de déblocage du prêt"),
  date_echeance DATE OPTIONS(description="Date d'échéance finale du contrat"),
  stage_ifrs9 INT64 OPTIONS(description="Classification IFRS 9 : Stage 1 (Performant), Stage 2 (Sous-performant / Dégradation du risque), Stage 3 (Défaillant / NPL)"),
  probabilite_defaillance_6m NUMERIC OPTIONS(description="Probabilité prédictive de défaillance à 6 mois (PD 6m)"),
  probabilite_defaillance_12m NUMERIC OPTIONS(description="Probabilité prédictive de défaillance à 12 mois (PD 12m)"),
  lgd_pct NUMERIC OPTIONS(description="Loss Given Default (Taux de perte en cas de défaut estimé) en %"),
  valeur_garantie_hypothecaire_eur NUMERIC OPTIONS(description="Valeur estimée des garanties et sûretés immobilisées/hypothécaires en Euros (€)"),
  ratio_ltv_pct NUMERIC OPTIONS(description="Ratio Loan-to-Value (Encours / Valeur Garantie en %). LTV > 85% indique un déficit de collatéral (Q8)"),
  montant_ecl_ifrs9_eur NUMERIC OPTIONS(description="Montant de provision IFRS 9 pour Perte de Crédit Attendue (ECL = EAD * PD * LGD) en Euros (€)"),
  taux_utilisation_ligne_pct NUMERIC OPTIONS(description="Taux d'utilisation effectif de la ligne de crédit autorisée en % (signal d'inactivité si < 20% - Q11)"),
  marge_nette_interet_eur NUMERIC OPTIONS(description="Contribution annuelle à la Marge Nette d'Intérêt (MNI) en Euros (€)"),
  eligibilite_titrisation BOOL OPTIONS(description="Indicateur d'éligibilité du prêt à la titrisation / cession pour libérer du capital réglementaire (Q9)"),
  eligibilite_pret_vert BOOL OPTIONS(description="Indicateur d'éligibilité du financement aux critères de prêt vert RSE (Q9)"),
  risque_attrition_churn STRING OPTIONS(description="Risque de départ/churn du client vers un concurrent : HIGH, MEDIUM, LOW (Q10)"),
  statut_restructuration STRING OPTIONS(description="Statut restructuration commerciale/empathique : AUCUN, RESTRUCTURATION_EN_COURS, RACHAT_PROPOSÉ")
)
OPTIONS (
  description = "Table principale des encours de crédit intégrant RAROC, LTV, IFRS 9 ECL, éligibilité à la titrisation et risque de churn (Q1-Q11)."
);

-- 5. Table: produits_bancaires (Product Catalog)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.produits_bancaires` (
  id_produit STRING OPTIONS(description="Identifiant unique du produit bancaire"),
  nom_produit STRING OPTIONS(description="Nom commercial officiel du produit"),
  code_produit STRING OPTIONS(description="Code mnémonique interne (ex: TRES_AUTO, RACHAT_RESTRUCTUR, PRET_VERT_RSE, TECH_DYNAMIC_PRICING)"),
  description STRING OPTIONS(description="Description fonctionnelle du produit et éligibilité"),
  categorie_produit STRING OPTIONS(description="Famille de produit : Trésorerie, Restructuration, Investissement, Titrisation")
)
OPTIONS (
  description = "Catalogue de référence des solutions financières et offres ciblées B2B."
);

-- 6. Table: souscriptions_produits (Active Subscriptions)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.souscriptions_produits` (
  id_souscription STRING OPTIONS(description="Identifiant unique de la souscription"),
  id_entreprise STRING OPTIONS(description="Clé étrangère vers entreprises.id_entreprise"),
  id_produit STRING OPTIONS(description="Clé étrangère vers produits_bancaires.id_produit"),
  code_produit STRING OPTIONS(description="Code mnémonique produit (ex: TRES_AUTO, RACHAT_RESTRUCTUR)"),
  statut_souscription STRING OPTIONS(description="Statut : ACTIF, RESILIE, PROPOSE"),
  date_souscription DATE OPTIONS(description="Date d'effet du contrat")
)
OPTIONS (
  description = "Suivi des souscriptions effectives par les entreprises."
);

-- ----------------------------------------------------------------------------
-- MACRO-ECONOMIC TABLES (9 Years 2018-2026 Banque de France / Webstat Time Series)
-- ----------------------------------------------------------------------------

-- 7. Table: bdf_taux_marche (9-Year Monthly Market & Macro Rates)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.bdf_taux_marche` (
  date_observation DATE OPTIONS(description="Date mensuelle de l'observation (108 mois : de 2018-01-01 à 2026-12-01)"),
  taux_directeur_bce NUMERIC OPTIONS(description="Taux de refinancement principal de la BCE en %"),
  euribor_3m NUMERIC OPTIONS(description="Taux interbancaire Euribor 3 mois en %"),
  euribor_12m NUMERIC OPTIONS(description="Taux interbancaire Euribor 12 mois en %"),
  taux_moyen_credit_pme NUMERIC OPTIONS(description="Taux d'intérêt moyen national accordé aux PME (source Banque de France Webstat) en %"),
  taux_moyen_credit_eti NUMERIC OPTIONS(description="Taux d'intérêt moyen national accordé aux ETI (source Banque de France Webstat) en %"),
  inflation_ipc_pct NUMERIC OPTIONS(description="Taux d'inflation annuel Indice des Prix à la Consommation (IPC) en % (Q4)"),
  pib_croissance_pct NUMERIC OPTIONS(description="Taux de croissance du PIB réel de la France en % (Q4)")
)
OPTIONS (
  description = "Séries temporelles mensuelles sur 9 ans (2018-2026) des taux d'intérêt, Euribor, inflation et PIB pour les prédictions et stress-tests (Q4)."
);

-- 8. Table: bdf_enquete_octroi_bls (Bank Lending Survey)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.bdf_enquete_octroi_bls` (
  trimestre STRING OPTIONS(description="Trimestre d'observation (36 trimestres : de 2018-Q1 à 2026-Q4)"),
  indice_criteres_octroi_pme NUMERIC OPTIONS(description="Indice d'assouplissement/durcissement des critères d'octroi de crédit aux PME (> 0 durcissement, < 0 assouplissement)"),
  indice_demande_credit_pme NUMERIC OPTIONS(description="Indice de la demande nette de crédit formulée par les PME (source BdF BLS)"),
  perception_risque_sectoriel STRING OPTIONS(description="Niveau de perception globale du risque par le régulateur : ELEVE, MODERE, FAIBLE")
)
OPTIONS (
  description = "Séries trimestrielles sur 9 ans de l'Enquête d'Octroi de Crédit (BLS) Banque de France."
);

-- 9. Table: bdf_defaillances_sectorielles_diren (DIREN Sectorial Defaults)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.bdf_defaillances_sectorielles_diren` (
  annee_mois STRING OPTIONS(description="Période mensuelle au format AAAA-MM (2018-01 à 2026-12)"),
  secteur_activite STRING OPTIONS(description="Secteur d'activité économique (Commerce, Industrie, BTP, Tech, Transport, Immobilier, Aéronautique, Automobile)"),
  nom_region STRING OPTIONS(description="Région administrative française"),
  taux_defaillance_annuel_pct NUMERIC OPTIONS(description="Taux de défaillance des entreprises cumulé sur 12 mois glissants en % (source DIREN / BdF)"),
  variation_trimestrielle_pct NUMERIC OPTIONS(description="Variation relative du taux de défaillance sur 3 mois en %")
)
OPTIONS (
  description = "Séries temporelles mensuelles sur 9 ans des taux de défaillances sectoriels et régionaux (DIREN / BdF)."
);

-- 10. Table: bdf_indices_immobiliers_rpp (Real Estate Price Index - RPP)
CREATE OR REPLACE TABLE `fsi_creditadvisor_dataset.bdf_indices_immobiliers_rpp` (
  trimestre STRING OPTIONS(description="Trimestre d'observation (36 trimestres : de 2018-Q1 à 2026-Q4)"),
  nom_region STRING OPTIONS(description="Région administrative française (ex: Occitanie, Île-de-France, PACA, Nouvelle-Aquitaine)"),
  indice_prix_immo_commercial NUMERIC OPTIONS(description="Indice des prix de l'immobilier commercial et de bureaux (Base 100 en 2020)"),
  indice_prix_immo_residentiel NUMERIC OPTIONS(description="Indice des prix de l'immobilier résidentiel (Base 100 en 2020)"),
  variation_annuelle_immo_pct NUMERIC OPTIONS(description="Variation annuelle des prix immobiliers régionaux en % (utilisé pour les stress-tests de collatéraux Q8)")
)
OPTIONS (
  description = "Indices trimestriels des prix de l'immobilier commercial et résidentiel (RPP) sur 9 ans par région."
);
