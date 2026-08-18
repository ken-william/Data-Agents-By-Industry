-- ============================================================================
-- Schema DDL for ShelfOptimizer - Retail Merchandising, CPG & Planograms
-- Dataset: retail_cpg_ds (Project: data-agents-by-industry)
-- Relational Architecture linking Open Food Facts Master Catalog, Store Footfall,
-- Fresh Produce Expiration Losses, Shelf Stockout Rates, Basket Margins, and Cross-Selling Bundles.
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS `retail_cpg_ds`
OPTIONS (
  location = 'US',
  description = 'Dataset ShelfOptimizer : Merchandising grande distribution, Nutri-Score Open Food Facts, affluence magasins, ruptures de rayon, paniers et cross-selling.'
);

-- 1. Table: openfoodfacts_catalog (Master Product Catalog from Open Food Facts)
CREATE OR REPLACE TABLE `retail_cpg_ds.openfoodfacts_catalog` (
  code_barre_ean STRING OPTIONS(description="Code-barres EAN13 unique du produit de grande consommation"),
  nom_produit STRING OPTIONS(description="Dénomination commerciale exacte du produit"),
  marque_entreprise STRING OPTIONS(description="Marque industrielle ou Marque de Distributeur (MDD)"),
  rayon_categorie STRING OPTIONS(description="Rayon d'implantation : Produits Frais, Épicerie, Boissons, Produits Laitiers, Surgelés, Boulangerie"),
  nutri_score STRING OPTIONS(description="Note nutritionnelle officielle Nutri-Score (A, B, C, D, E)"),
  nova_score INT64 OPTIONS(description="Indice d'ultra-transformation NOVA (1=Peu transformé à 4=Ultra-transformé)"),
  additifs_problematiques STRING OPTIONS(description="Liste des additifs ou conservateurs controversés identifiés"),
  alternatives_saines_recommandees STRING OPTIONS(description="Référence produit alternative mieux notée en Nutri-Score"),
  chiffre_affaires_annuel_eur NUMERIC OPTIONS(description="Chiffre d'affaires annuel généré sur l'enseigne (€)"),
  empreinte_carbone_100g NUMERIC OPTIONS(description="Équivalent gCO2eq pour 100g de produit"),
  produit_image_url STRING OPTIONS(description="URL GCS Object Table de la photographie HD du packaging produit")
)
OPTIONS (
  description = "Catalogue produits master Open Food Facts avec indicateurs nutritionnels, additifs et photos GCS."
);

-- 2. Table: retail_frequentation_magasins (Store Footfall, Traffic & Fresh Produce Loss Prediction)
CREATE OR REPLACE TABLE `retail_cpg_ds.retail_frequentation_magasins` (
  id_magasin STRING OPTIONS(description="Identifiant unique du point de vente"),
  nom_magasin STRING OPTIONS(description="Nom commercial du magasin"),
  enseigne STRING OPTIONS(description="Enseigne : Carrefour Hyper, Auchan Super, Monoprix, E.Leclerc, Intermarché"),
  commune STRING OPTIONS(description="Commune d'implantation du point de vente"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  tranche_horaire STRING OPTIONS(description="Créneau horaire de comptage (ex: 08h-11h, 11h-14h, 14h-17h, 17h-20h)"),
  affluence_clients_jour INT64 OPTIONS(description="Nombre de visiteurs / passage caisses enregistrés"),
  taux_conversion_passage_caisses_pct NUMERIC OPTIONS(description="Taux de conversion visiteurs vers acheteurs (%)"),
  demarque_pertes_produits_frais_14j_eur NUMERIC OPTIONS(description="Pertes financières prédites sur 14 jours par péremption des produits frais (€)"),
  consigne_reassort_automatique STRING OPTIONS(description="Consigne : REASSORT_URGENT_AUTOMATIQUE, CONFORME")
)
OPTIONS (
  description = "Fréquentation des points de vente, taux de conversion et prédiction des pertes par démarque fraîche."
);

-- 3. Table: retail_prix_moyens_panier (Average Basket Price & Category Margins)
CREATE OR REPLACE TABLE `retail_cpg_ds.retail_prix_moyens_panier` (
  id_releve_panier STRING OPTIONS(description="Identifiant du relevé panier moyen"),
  commune STRING OPTIONS(description="Commune de l'analyse"),
  code_departement STRING OPTIONS(description="Département d'implantation"),
  nom_region STRING OPTIONS(description="Région administrative"),
  rayon_categorie STRING OPTIONS(description="Rayon concerné par l'analyse tarifaire"),
  prix_moyen_panier_eur NUMERIC OPTIONS(description="Montant moyen du panier d'achat en Euros (€)"),
  marge_brute_pct NUMERIC OPTIONS(description="Taux de marge brute moyenne réalisée sur le rayon (%)"),
  part_produits_bio_pct NUMERIC OPTIONS(description="Part des produits certifiés Bio dans les ventes du rayon (%)"),
  part_marques_distributeur_pct NUMERIC OPTIONS(description="Part des Marques de Distributeurs (MDD) dans le panier (%)")
)
OPTIONS (
  description = "Analyse des prix moyens par panier, taux de marge brute par rayon et part des marques MDD."
);

-- 4. Table: retail_analyse_lineaire_ruptures (Shelf Stockout & Planogram Compliance)
CREATE OR REPLACE TABLE `retail_cpg_ds.retail_analyse_lineaire_ruptures` (
  id_releve_lineaire STRING OPTIONS(description="Identifiant du relevé merchandising en rayon"),
  id_magasin STRING OPTIONS(description="Clé étrangère vers retail_frequentation_magasins"),
  code_barre_ean STRING OPTIONS(description="Clé étrangère vers openfoodfacts_catalog"),
  rayon_categorie STRING OPTIONS(description="Rayon du linéaire auditations"),
  nombre_facings_theorique INT64 OPTIONS(description="Nombre de facings prescrits sur le planogramme officiel"),
  nombre_facings_constate INT64 OPTIONS(description="Nombre de facings réellement observés en rayon"),
  taux_conformite_planogramme_pct NUMERIC OPTIONS(description="Taux de conformité au planogramme (%)"),
  taux_rupture_lineaire_pct NUMERIC OPTIONS(description="Taux de rupture visuelle en rayon (%)"),
  statut_stock_lineaire STRING OPTIONS(description="Statut : RUPTURE_SHELF_OUT, STOCK_FAIBLE, CONFORME")
)
OPTIONS (
  description = "Audit de conformité des planogrammes de linéaires et détection des ruptures de stock en rayon."
);

-- 5. Table: retail_cross_selling_associations (Affinity Rules & Basket Optimization Bundles)
CREATE OR REPLACE TABLE `retail_cpg_ds.retail_cross_selling_associations` (
  id_association STRING OPTIONS(description="Identifiant unique de la règle d'affinité"),
  code_barre_ean_principal STRING OPTIONS(description="Code-barres du produit pilier à forte notoriété"),
  code_barre_ean_associe_mdd STRING OPTIONS(description="Code-barres du produit MDD complémentaire recommandé"),
  nom_produit_principal STRING OPTIONS(description="Nom du produit pilier"),
  nom_produit_mdd_associe STRING OPTIONS(description="Nom du produit MDD à forte marge associé"),
  indice_confiance_association_pct NUMERIC OPTIONS(description="Indice de confiance de l'association panier (%)"),
  hausse_ticket_moyen_projete_pct NUMERIC OPTIONS(description="Hausse estimée du ticket moyen panier (%)"),
  offre_bundle_recommandee STRING OPTIONS(description="Description de l'offre bundle promotionnelle (ex: -30% sur le 2eme produit MDD)")
)
OPTIONS (
  description = "Règles d'affinité d'achat et recommandations de bundles cross-selling pour augmenter le panier moyen."
);
