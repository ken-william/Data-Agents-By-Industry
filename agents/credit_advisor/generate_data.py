#!/usr/bin/env python3
"""
Synthetic Data Generation Script for CreditAdvisor 360° Executive Copilot (FSI Sector - Banque & Assurance)
Generates 9 Years of Macroeconomic Time Series (2018-2026, 108 Monthly Points) & 3,000 Micro-Economic Company Records.
Supports Queries Q1 to Q11: CRO Risk, CFO Margins/RAROC, Sales Retention & Growth.

Dataset: fsi_creditadvisor_dataset
"""

import os
import sys
import uuid
import random
import subprocess
from datetime import datetime, date, timedelta
from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker('fr_FR')
Faker.seed(42)
random.seed(42)

DATASET_ID = os.environ.get("BIGQUERY_DATASET", "fsi_creditadvisor_dataset")
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")

REGIONS = {
    "Occitanie": ["Toulouse", "Montpellier", "Nîmes", "Perpignan", "Béziers", "Tarbes", "Albi", "Carcassonne"],
    "Île-de-France": ["Paris", "Boulogne-Billancourt", "Saint-Denis", "Versailles", "Nanterre"],
    "Provence-Alpes-Côte d'Azur": ["Marseille", "Nice", "Toulon", "Aix-en-Provence", "Cannes"],
    "Auvergne-Rhône-Alpes": ["Lyon", "Saint-Étienne", "Grenoble", "Annecy"],
    "Nouvelle-Aquitaine": ["Bordeaux", "Limoges", "Poitiers", "Pau", "La Rochelle"]
}

REGION_CODES = {
    "Occitanie": "OCC", "Île-de-France": "IDF",
    "Provence-Alpes-Côte d'Azur": "PACA", "Auvergne-Rhône-Alpes": "ARA", "Nouvelle-Aquitaine": "NAQ"
}

SECTORS = ["Commerce", "Industrie", "BTP", "Technologies", "Agroalimentaire", "Transport", "Immobilier", "Aéronautique", "Automobile"]

NAF_CODES = {
    "Commerce": ["4711F", "4690Z"], "Industrie": ["2899B", "1089Z"],
    "BTP": ["4120A", "4321A"], "Technologies": ["6201Z", "6202A"],
    "Agroalimentaire": ["1011Z", "1051A"], "Transport": ["4941A", "5210B"],
    "Immobilier": ["6820B", "6810Z"], "Aéronautique": ["3030Z", "2540Z"],
    "Automobile": ["2910Z", "2932Z"]
}

SUPPLY_CHAIN_ANCHORS = {
    "Aéronautique": ["AIRBUS_GROUP", "SAFRAN", "THALES"],
    "Automobile": ["RENAULT_GROUP", "STELLANTIS"],
    "Industrie": ["SCHNEIDER_ELECTRIC", "ALSTOM"]
}

def generate_siren():
    return "".join([str(random.randint(0, 9)) for _ in range(9)])

def generate_macro_data_9_years():
    print("Generating 9 Years of Banque de France Webstat Macroeconomic Time Series (2018-2026)...")
    
    # 1. bdf_taux_marche (Monthly rates 2018-01-01 to 2026-12-01 = 108 Months)
    taux_marche = []
    current_date = date(2018, 1, 1)
    end_date = date(2026, 12, 1)
    
    # Base rates initial state (Low interest environment 2018-2021, spike 2022-2024, stabilization 2025-2026)
    while current_date <= end_date:
        yr = current_date.year
        mo = current_date.month
        
        if yr < 2022:
            bce_rate = 0.00
            euribor_3m = round(-0.35 + random.uniform(-0.05, 0.05), 2)
            euribor_12m = round(-0.15 + random.uniform(-0.05, 0.05), 2)
            pme_rate = round(1.45 + random.uniform(-0.1, 0.1), 2)
            eti_rate = round(1.15 + random.uniform(-0.08, 0.08), 2)
            inflation = round(1.2 + random.uniform(-0.3, 0.3), 1)
            pib_growth = round(1.8 + random.uniform(-0.4, 0.4), 1) if yr != 2020 else -7.9
        elif yr in [2022, 2023, 2024]:
            # Rate rise & Inflation shock
            progress = ((yr - 2022) * 12 + mo) / 36.0
            bce_rate = round(0.50 + progress * 4.00, 2)
            euribor_3m = round(0.20 + progress * 3.75, 2)
            euribor_12m = round(0.50 + progress * 3.65, 2)
            pme_rate = round(euribor_3m + 1.95, 2)
            eti_rate = round(euribor_3m + 1.35, 2)
            inflation = round(5.2 - progress * 2.5, 1)
            pib_growth = round(0.8 + random.uniform(-0.3, 0.3), 1)
        else:
            # 2025-2026 Adjustment & Stabilization
            bce_rate = 3.25
            euribor_3m = round(3.15 + random.uniform(-0.08, 0.08), 2)
            euribor_12m = round(3.05 + random.uniform(-0.08, 0.08), 2)
            pme_rate = round(euribor_3m + 1.75, 2)
            eti_rate = round(euribor_3m + 1.20, 2)
            inflation = round(2.1 + random.uniform(-0.2, 0.2), 1)
            pib_growth = round(1.2 + random.uniform(-0.2, 0.2), 1)

        taux_marche.append({
            "date_observation": current_date.strftime("%Y-%m-%d"),
            "taux_directeur_bce": bce_rate,
            "euribor_3m": euribor_3m,
            "euribor_12m": euribor_12m,
            "taux_moyen_credit_pme": pme_rate,
            "taux_moyen_credit_eti": eti_rate,
            "inflation_ipc_pct": inflation,
            "pib_croissance_pct": pib_growth
        })
        
        # Advance 1 month
        month = current_date.month + 1
        year = current_date.year
        if month > 12:
            month = 1
            year += 1
        current_date = date(year, month, 1)

    df_taux = pd.DataFrame(taux_marche)

    # 2. bdf_enquete_octroi_bls (36 Quarters: 2018-Q1 to 2026-Q4)
    bls_data = []
    for yr in range(2018, 2027):
        for q in [1, 2, 3, 4]:
            q_str = f"{yr}-Q{q}"
            if yr in [2022, 2023, 2024]:
                criteres = round(random.uniform(15.0, 38.0), 1)
                demande = round(random.uniform(-30.0, -8.0), 1)
                risque = "ELEVE"
            elif yr in [2020]:
                criteres = round(random.uniform(20.0, 45.0), 1)
                demande = round(random.uniform(10.0, 50.0), 1) # PGE demand
                risque = "ELEVE"
            else:
                criteres = round(random.uniform(-8.0, 8.0), 1)
                demande = round(random.uniform(2.0, 18.0), 1)
                risque = "MODERE"

            bls_data.append({
                "trimestre": q_str,
                "indice_criteres_octroi_pme": criteres,
                "indice_demande_credit_pme": demande,
                "perception_risque_sectoriel": risque
            })
    df_bls = pd.DataFrame(bls_data)

    # 3. bdf_defaillances_sectorielles_diren (Monthly DIREN defaults across sectors and regions)
    diren_data = []
    for yr in range(2018, 2027):
        for m in range(1, 13):
            ym = f"{yr}-{m:02d}"
            for sec in SECTORS:
                for reg in REGIONS.keys():
                    base_rate = 9.2 if sec == "BTP" else (7.5 if sec in ["Automobile", "Commerce"] else 4.5)
                    yr_mult = 1.35 if yr in [2023, 2024] else (0.65 if yr in [2021] else 1.0)
                    reg_mult = 1.12 if reg == "Occitanie" else 1.0
                    rate = round(base_rate * yr_mult * reg_mult + random.uniform(-0.6, 0.6), 2)
                    
                    diren_data.append({
                        "annee_mois": ym,
                        "secteur_activite": sec,
                        "nom_region": reg,
                        "taux_defaillance_annuel_pct": rate,
                        "variation_trimestrielle_pct": round(random.uniform(-1.5, 3.2), 2)
                    })
    df_diren = pd.DataFrame(diren_data)

    # 4. bdf_indices_immobiliers_rpp (36 Quarters 2018-2026 RPP indices)
    rpp_data = []
    for yr in range(2018, 2027):
        for q in [1, 2, 3, 4]:
            q_str = f"{yr}-Q{q}"
            for reg in REGIONS.keys():
                if yr < 2022:
                    base_comm = round(95.0 + (yr - 2018) * 3.5, 1)
                    base_res = round(92.0 + (yr - 2018) * 4.0, 1)
                    var_ann = round(random.uniform(2.5, 6.5), 2)
                elif yr in [2023, 2024, 2025]:
                    # Commercial Real Estate contraction
                    base_comm = round(108.0 - (yr - 2022) * 7.5, 1)
                    base_res = round(110.0 - (yr - 2022) * 3.5, 1)
                    var_ann = round(random.uniform(-14.8, -4.2), 2)
                else:
                    base_comm = 86.5
                    base_res = 99.0
                    var_ann = round(random.uniform(-1.5, 1.5), 2)

                rpp_data.append({
                    "trimestre": q_str,
                    "nom_region": reg,
                    "indice_prix_immo_commercial": base_comm,
                    "indice_prix_immo_residentiel": base_res,
                    "variation_annuelle_immo_pct": var_ann
                })
    df_rpp = pd.DataFrame(rpp_data)

    return df_taux, df_bls, df_diren, df_rpp

def generate_micro_data(num_companies=3000):
    print(f"Generating 3,000 Micro-Economic Company Records with Q1-Q11 Attributes...")
    
    # Products Catalog
    df_products = pd.DataFrame([
        {
            "id_produit": "PROD_TRES_AUTO",
            "nom_produit": "Crédit de trésorerie automatisé",
            "code_produit": "TRES_AUTO",
            "description": "Ligne de crédit court terme automatisée pilotée par IA (Q2).",
            "categorie_produit": "Trésorerie"
        },
        {
            "id_produit": "PROD_RACHAT_RESTRUCTUR",
            "nom_produit": "Solution de Rachat & Restructuration Empathique",
            "code_produit": "RACHAT_RESTRUCTUR",
            "description": "Réaménagement de dette court terme en long terme avec rééchelonnement (Q5).",
            "categorie_produit": "Restructuration"
        },
        {
            "id_produit": "PROD_PRET_VERT_RSE",
            "nom_produit": "Prêt Vert Transition Énergétique & RSE",
            "code_produit": "PRET_VERT_RSE",
            "description": "Financement bonifié RSE financé par la titrisation de créances (Q9).",
            "categorie_produit": "Investissement"
        },
        {
            "id_produit": "PROD_TECH_DYNAMIC_PRICING",
            "nom_produit": "Crédit Dynamic Pricing Tech RAROC",
            "code_produit": "TECH_DYNAMIC_PRICING",
            "description": "Crédit sur mesure pour PME Tech à tarification basée sur le risque et le RAROC (Q7).",
            "categorie_produit": "Trésorerie"
        }
    ])

    companies, balance_sheets, credit_lines, subscriptions = [], [], [], []

    for i in range(num_companies):
        company_id = f"ENT_{100000 + i}"
        nom_region = "Occitanie" if i < int(num_companies * 0.35) else random.choice(list(REGIONS.keys()))
        ville = random.choice(REGIONS[nom_region])
        secteur = random.choice(SECTORS)
        code_naf = random.choice(NAF_CODES[secteur])
        
        donneur_ordre = "AUCUN"
        if secteur in SUPPLY_CHAIN_ANCHORS:
            donneur_ordre = random.choice(SUPPLY_CHAIN_ANCHORS[secteur])

        rand_cat = random.random()
        if rand_cat < 0.70:
            categorie = "PME"
            effectif = random.randint(10, 249)
            ca_2025 = round(random.uniform(1_800_000, 48_000_000), 2)
        elif rand_cat < 0.92:
            categorie = "ETI"
            effectif = random.randint(250, 4999)
            ca_2025 = round(random.uniform(50_000_000, 450_000_000), 2)
        else:
            categorie = "Grande Entreprise"
            effectif = random.randint(5000, 25000)
            ca_2025 = round(random.uniform(500_000_000, 2_200_000_000), 2)

        # Company Master
        companies.append({
            "id_entreprise": company_id,
            "nom_entreprise": fake.company() + (" SAS" if random.random() > 0.5 else " SARL"),
            "siren": generate_siren(),
            "categorie_entreprise": categorie,
            "secteur_activite": secteur,
            "code_naf": code_naf,
            "code_region": REGION_CODES[nom_region],
            "nom_region": nom_region,
            "ville": ville,
            "code_postal": f"{random.randint(11, 95):02d}{random.randint(100, 900):03d}",
            "effectif": effectif,
            "donneur_ordre_principal": donneur_ordre,
            "date_creation": (datetime.now() - timedelta(days=random.randint(730, 8000))).strftime("%Y-%m-%d")
        })

        # Financial Health & Ratings
        is_solid_pme = (nom_region == "Occitanie" and categorie == "PME" and random.random() < 0.70)
        is_tech = (secteur == "Technologies" and categorie == "PME")
        
        score_sante = random.randint(78, 98) if (is_solid_pme or is_tech) else random.randint(15, 95)
        
        # Internal Rating
        if score_sante >= 75:
            notation = random.choice(["A", "B"])
        elif score_sante >= 45:
            notation = "B"
        elif score_sante >= 25:
            notation = "C"
        else:
            notation = "D"

        # Multi-Year Balance Sheets (2021 to 2025)
        for yr in [2021, 2022, 2023, 2024, 2025]:
            growth = 1.0 if yr == 2025 else (0.92 if yr == 2024 else 0.85)
            ca_yr = round(ca_2025 * growth, 2)
            ebe_yr = round(ca_yr * random.uniform(0.08, 0.24), 2)
            res_net = round(ebe_yr * random.uniform(0.35, 0.65), 2)
            fonds_propres = round(ca_yr * random.uniform(0.20, 0.45), 2)
            dette_brute = round(ca_yr * random.uniform(0.15, 0.60), 2)
            treso = round(ca_yr * random.uniform(0.04, 0.16), 2)
            bfr = round(ca_yr * random.uniform(0.08, 0.25), 2)

            dscr = round(max(0.4, ebe_yr / max(1.0, (dette_brute * 0.18))), 2)
            icr = round(max(0.5, ebe_yr / max(1.0, (dette_brute * 0.055))), 2)
            ratio_endett = round(max(0.1, (dette_brute - treso) / max(1.0, fonds_propres)), 2)

            # Weak Signals (Q5: Asymptomatic deterioration despite A/B rating)
            if notation in ["A", "B"] and random.random() < 0.15:
                var_flux_treso = round(random.uniform(-35.0, -22.0), 2) # Drop in cash flow
                delai_paiement = random.randint(68, 95) # Extended payment delays
            else:
                var_flux_treso = round(random.uniform(-5.0, 18.0), 2)
                delai_paiement = random.randint(25, 55)

            balance_sheets.append({
                "id_bilan": f"BIL_{company_id}_{yr}",
                "id_entreprise": company_id,
                "annee_exercice": yr,
                "chiffre_affaires_eur": ca_yr,
                "ebe_ebitda_eur": ebe_yr,
                "resultat_net_eur": res_net,
                "fonds_propres_eur": fonds_propres,
                "dette_financiere_brute_eur": dette_brute,
                "tresorerie_nette_eur": treso,
                "bfr_eur": bfr,
                "ratio_dscr": dscr,
                "ratio_icr": icr,
                "ratio_endettement": ratio_endett,
                "notation_interne": notation,
                "variation_flux_tresorerie_6m_pct": var_flux_treso,
                "delai_paiement_clients_jours": delai_paiement,
                "score_sante_financiere": score_sante
            })

        # Product Subscriptions: TRES_AUTO
        if not (nom_region == "Occitanie" and categorie == "PME" and random.random() > 0.25):
            subscriptions.append({
                "id_souscription": f"SUB_{i}_1",
                "id_entreprise": company_id,
                "id_produit": "PROD_TRES_AUTO",
                "code_produit": "TRES_AUTO",
                "statut_souscription": "ACTIF",
                "date_souscription": "2024-03-15"
            })

        # Credit Lines with RAROC, LTV, IFRS 9 ECL, Securitization, Churn & Dormancy (Q1-Q11)
        num_credits = random.randint(1, 2)
        for c_idx in range(num_credits):
            montant_encours = round(ca_2025 * random.uniform(0.08, 0.28), 2)
            taux_actuel = round(random.uniform(3.8, 7.8), 2)
            marge_bps = round(random.uniform(140, 320), 0)
            taux_var = random.choice([True, False])

            # RAROC (Q7: Risk-Adjusted Return on Capital)
            raroc = round(random.uniform(9.5, 18.5) if is_tech else random.uniform(6.0, 14.0), 2)

            # Probabilities of Default & IFRS 9 Staging
            if score_sante < 35 or random.random() < 0.12:
                prob_def_6m = round(random.uniform(0.76, 0.96), 4) # Q1 > 75%
                prob_def_12m = round(prob_def_6m * 1.05, 4)
                stage_ifrs9 = 3 if prob_def_6m > 0.85 else 2
                statut_restruct = "RACHAT_PROPOSÉ" if random.random() > 0.4 else "RESTRUCTURATION_EN_COURS"
            elif score_sante < 60:
                prob_def_6m = round(random.uniform(0.20, 0.65), 4)
                prob_def_12m = round(prob_def_6m * 1.1, 4)
                stage_ifrs9 = 2
                statut_restruct = "AUCUN"
            else:
                prob_def_6m = round(random.uniform(0.002, 0.007), 4) # Q7 < 0.8%
                prob_def_12m = round(prob_def_6m * 1.2, 4)
                stage_ifrs9 = 1
                statut_restruct = "AUCUN"

            lgd_pct = 45.0
            
            # Collateral & LTV (Q8: Loan-to-Value & Commercial Real Estate Shock)
            valeur_garantie = round(montant_encours * random.uniform(0.70, 1.40), 2)
            ratio_ltv = round((montant_encours / max(1.0, valeur_garantie)) * 100.0, 1)

            ecl_ifrs9 = round(montant_encours * prob_def_12m * (lgd_pct / 100.0), 2)

            # Line Utilization Rate (Q11: Dormant Lines < 20%)
            if random.random() < 0.18:
                taux_utilisation = round(random.uniform(5.0, 18.0), 1) # Dormant credit facility
            else:
                taux_utilisation = round(random.uniform(60.0, 95.0), 1)

            # Churn Risk (Q10: Top-tier profitable clients churning)
            if score_sante >= 85 and random.random() < 0.15:
                churn_risk = "HIGH"
            else:
                churn_risk = "LOW"

            # Securitization & Green Loan Eligibility (Q9)
            elig_titrisation = (stage_ifrs9 == 1 and prob_def_12m < 0.05 and random.random() < 0.40)
            elig_pret_vert = (secteur in ["Technologies", "Agroalimentaire", "Industrie"] and random.random() < 0.35)

            mni_eur = round(montant_encours * (marge_bps / 10000.0), 2)

            credit_lines.append({
                "id_credit": f"CRE_{company_id}_{c_idx+1}",
                "id_entreprise": company_id,
                "type_credit": random.choice(["Crédit d'investissement", "Crédit bail", "Prêt de trésorerie", "Prêt immobilier pro"]),
                "montant_initial_eur": round(montant_encours * 1.25, 2),
                "montant_encours_eur": montant_encours,
                "taux_interet_actuel": taux_actuel,
                "marge_banque_bps": marge_bps,
                "raroc_pct": raroc,
                "taux_variable": taux_var,
                "date_debut": "2023-03-15",
                "date_echeance": "2028-03-15",
                "stage_ifrs9": stage_ifrs9,
                "probabilite_defaillance_6m": prob_def_6m,
                "probabilite_defaillance_12m": prob_def_12m,
                "lgd_pct": lgd_pct,
                "valeur_garantie_hypothecaire_eur": valeur_garantie,
                "ratio_ltv_pct": ratio_ltv,
                "montant_ecl_ifrs9_eur": ecl_ifrs9,
                "taux_utilisation_ligne_pct": taux_utilisation,
                "marge_nette_interet_eur": mni_eur,
                "eligibilite_titrisation": elig_titrisation,
                "eligibilite_pret_vert": elig_pret_vert,
                "risque_attrition_churn": churn_risk,
                "statut_restructuration": statut_restruct
            })

    return (df_products, pd.DataFrame(companies), pd.DataFrame(balance_sheets),
            pd.DataFrame(credit_lines), pd.DataFrame(subscriptions))

def save_and_upload_all(project_id, macro_tables, micro_tables):
    all_tables = {**macro_tables, **micro_tables}
    os.makedirs("generated_data", exist_ok=True)
    for name, df in all_tables.items():
        df.to_csv(f"generated_data/{name}.csv", index=False)
        print(f"Saved local CSV: generated_data/{name}.csv ({len(df)} rows)")

    print(f"\nUploading all 9 tables to BigQuery project '{project_id}' via bq load CLI...")
    for table_name in all_tables.keys():
        cmd = f"bq load --source_format=CSV --skip_leading_rows=1 --replace {project_id}:{DATASET_ID}.{table_name} generated_data/{table_name}.csv"
        print(f"Executing: {cmd}")
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Successfully loaded `{DATASET_ID}.{table_name}`.")
        else:
            print(f"Error loading `{DATASET_ID}.{table_name}`: {res.stderr}")

def main():
    print(f"Starting Triple-Volume 360° Data Engine for Project: '{PROJECT_ID}'...")
    df_taux, df_bls, df_diren, df_rpp = generate_macro_data_9_years()
    df_products, df_entreprises, df_bilans, df_credits, df_subscriptions = generate_micro_data(3000)

    macro_tables = {
        "bdf_taux_marche": df_taux,
        "bdf_enquete_octroi_bls": df_bls,
        "bdf_defaillances_sectorielles_diren": df_diren,
        "bdf_indices_immobiliers_rpp": df_rpp
    }

    micro_tables = {
        "produits_bancaires": df_products,
        "entreprises": df_entreprises,
        "bilans_financiers": df_bilans,
        "encours_credit": df_credits,
        "souscriptions_produits": df_subscriptions
    }

    save_and_upload_all(PROJECT_ID, macro_tables, micro_tables)

if __name__ == "__main__":
    main()
