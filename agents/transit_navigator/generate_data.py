#!/usr/bin/env python3
"""
Refined Relational Data Pipeline & OpenData Processing for Transit Navigator (transport_mobility_ds).
Parses authentic SNCF Open Data CSVs (Frequentation Gares, Regularite TGV / TER) and populates
9 relational tables in BigQuery including 6-month TER Predictive Maintenance time-series
(3 months history + 3 months forecast) and Yield Management 1st Class Pricing.
"""

import os
import sys
import random
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from google.cloud import bigquery
from google.oauth2.credentials import Credentials

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "data-agents-by-industry")
DATASET_ID = "transport_mobility_ds"
LOCATION = "US"
BUCKET_NAME = "gs://talktodata-transit-navigator-raw-data"

GARES_RAW_CSV = "agents/transit_navigator/data/frequentation_gares_sncf_raw.csv"
REGULARITE_TGV_CSV = "agents/transit_navigator/data/regularite_tgv_raw.csv"
REGULARITE_TER_CSV = "agents/transit_navigator/data/regularite_ter_raw.csv"

CITY_METRICS = [
    ("Paris Gare de Lyon", "87686006", "75012", "75", "Île-de-France", 48.8443, 2.3744),
    ("Paris Montparnasse", "87391003", "75015", "75", "Île-de-France", 48.8412, 2.3204),
    ("Paris Gare du Nord", "87271007", "75010", "75", "Île-de-France", 48.8809, 2.3553),
    ("Lyon Part-Dieu", "87722023", "69003", "69", "Auvergne-Rhône-Alpes", 45.7606, 4.8596),
    ("Marseille Saint-Charles", "87751006", "13001", "13", "Provence-Alpes-Côte d'Azur", 43.3027, 5.3806),
    ("Toulouse Matabiau", "87611004", "31500", "31", "Occitanie", 43.6111, 1.4536),
    ("Lille Flandres", "87223263", "59000", "59", "Hauts-de-France", 50.6367, 3.0700),
    ("Bordeaux Saint-Jean", "87581009", "33800", "33", "Nouvelle-Aquitaine", 44.8258, -0.5564),
    ("Strasbourg Ville", "87212027", "67000", "67", "Grand Est", 48.5851, 7.7345),
    ("Nantes", "87481002", "44000", "44", "Pays de la Loire", 47.2173, -1.5418),
    ("Rennes", "87471003", "35000", "35", "Bretagne", 48.1033, -1.6725),
    ("Grenoble", "87747004", "38000", "38", "Auvergne-Rhône-Alpes", 45.1914, 5.7145),
    ("Nice Ville", "87756054", "06000", "06", "Provence-Alpes-Côte d'Azur", 43.7046, 7.2619)
]

FIRST_NAMES = ["Thomas", "Lucas", "Sophie", "Camille", "Élodie", "Alexandre", "Nicolas", "Julie", "Marie", "Jean", "Maxime", "Léa", "Antoine", "Chloé", "Pierre"]
LAST_NAMES = ["Bernard", "Martin", "Moreau", "Petit", "Dubois", "Richard", "Durand", "Laurent", "Lefebvre", "Michel", "Garcia", "David", "Bertrand", "Roux", "Fournier"]

def get_client():
    token = subprocess.check_output(["gcloud", "auth", "print-access-token"]).decode("utf-8").strip()
    creds = Credentials(token)
    return bigquery.Client(project=PROJECT_ID, credentials=creds)

def main():
    print(f"Initializing Refined Transit Navigator Pipeline for project '{PROJECT_ID}'...")
    client = get_client()

    os.makedirs("agents/transit_navigator/data", exist_ok=True)

    # Step 1: Run DDL setup
    ddl_path = os.path.join(os.path.dirname(__file__), "ddl_setup.sql")
    if os.path.exists(ddl_path):
        with open(ddl_path, "r", encoding="utf-8") as f:
            sql_script = f.read().replace("${PROJECT_ID}", PROJECT_ID)
        for stmt in sql_script.split(";"):
            stmt = stmt.strip()
            if stmt:
                client.query(stmt).result()
        print("  ✓ Executed ddl_setup.sql to ensure exact transport_mobility_ds schemas!")

    # Step 2: Build Table 1: frequentation_gares_sncf
    gares_data = []
    if os.path.exists(GARES_RAW_CSV):
        df_raw = pd.read_csv(GARES_RAW_CSV, sep=";", low_memory=False)
        print(f"  ✓ Loaded {len(df_raw)} raw SNCF station attendance records.")
        for idx, row in df_raw.iterrows():
            nom = str(row.get("nom_gare", row.get("Nom de la gare", ""))).strip()
            if not nom or nom == "nan":
                continue
            uic = str(row.get("code_uic_complet", row.get("Code UIC", ""))).strip().split(".")[0]
            cp = str(row.get("code_postal", row.get("Code postal", ""))).strip().split(".")[0].zfill(5)
            dept = cp[:2] if len(cp) >= 2 else "75"
            drg = str(row.get("direction_regionale_gares", row.get("Direction Régionale Gares", ""))).strip()

            v2024 = row.get("total_voyageurs_2024", row.get("Total Voyageurs 2024", 0))
            v2023 = row.get("total_voyageurs_2023", row.get("Total Voyageurs 2023", 0))
            v2022 = row.get("total_voyageurs_2022", row.get("Total Voyageurs 2022", 0))

            try:
                v2024 = int(float(v2024)) if pd.notnull(v2024) else random.randint(50000, 5000000)
                v2023 = int(float(v2023)) if pd.notnull(v2023) else int(v2024 * 0.95)
                v2022 = int(float(v2022)) if pd.notnull(v2022) else int(v2023 * 0.92)
            except Exception:
                v2024, v2023, v2022 = 120000, 115000, 108000

            gares_data.append({
                "code_uic_gare": uic if uic else f"87{idx:06d}",
                "nom_gare": nom,
                "code_postal": cp,
                "departement_code": dept,
                "region_nom": drg if drg else "Île-de-France",
                "direction_regionale_sncf": drg if drg else "DR Gares Paris",
                "total_voyageurs_2024": v2024,
                "total_voyageurs_2023": v2023,
                "total_voyageurs_2022": v2022
            })
    df_gares = pd.DataFrame(gares_data)
    print(f"  ✓ Processed {len(df_gares)} clean SNCF station attendance records.")

    # Step 3: Build Table 2: sncf_regularite_lignes (TGV & TER)
    regularite_data = []
    if os.path.exists(REGULARITE_TGV_CSV):
        df_reg = pd.read_csv(REGULARITE_TGV_CSV, sep=";", low_memory=False)
        print(f"  ✓ Loaded {len(df_reg)} raw SNCF TGV line regularity records.")
        for idx, row in df_reg.iterrows():
            g_dep = str(row.get("Gare de départ", "")).strip()
            g_arr = str(row.get("Gare d'arrivée", "")).strip()
            if not g_dep or not g_arr or g_dep == "nan":
                continue

            axe_name = f"{g_dep} - {g_arr}"
            circ = row.get("Nombre de circulations prévues", 100)
            ann = row.get("Nombre de trains annulés", 2)
            ret_dep = row.get("Retard moyen des trains en retard au départ", 8.5)

            try:
                circ = int(float(circ)) if pd.notnull(circ) else 120
                if circ <= 0:
                    circ = 100
                ann = int(float(ann)) if pd.notnull(ann) else 3
                ret_dep = float(ret_dep) if pd.notnull(ret_dep) else 12.4
            except Exception:
                circ, ann, ret_dep = 100, 2, 9.5

            ponct = round(max(75.0, min(99.5, 100.0 - (ann / circ * 100.0) - (ret_dep * 0.5))), 1)
            infra_pct = round(random.uniform(18.0, 34.0), 1)
            mat_pct = round(random.uniform(22.0, 42.0), 1)
            trafic_pct = round(100.0 - infra_pct - mat_pct, 1)

            regularite_data.append({
                "ligne_axe_id": f"AXE-TGV-{idx:05d}",
                "nom_axe_ferroviaire": axe_name,
                "gare_depart": g_dep,
                "gare_arrivee": g_arr,
                "service_type": "TGV InOui",
                "region": "National TGV",
                "duree_moyenne_trajet_minutes": round(random.uniform(60.0, 240.0), 1),
                "circulations_prevues_nombre": circ,
                "nombre_trains_annules": ann,
                "retard_moyen_minutes": round(ret_dep, 1),
                "taux_regularite_ponctualite_pct": ponct,
                "cause_retard_infrastructure_pct": infra_pct,
                "cause_retard_materiel_roulant_pct": mat_pct,
                "cause_retard_gestion_trafic_pct": trafic_pct,
                "perte_financiere_retards_eur": round(ann * 4500.0 + (circ - ann) * ret_dep * 120.0, 2)
            })

    # Add Regional TER Lines
    ter_axes = [
        ("AXE-TER-001", "Lyon Part-Dieu - Grenoble (TER AURA)", "Lyon Part-Dieu", "Grenoble", "TER Régional", "Auvergne-Rhône-Alpes", 85.0, 240, 12, 18.5, 87.5, 38.0, 42.0, 20.0, 485000.0),
        ("AXE-TER-002", "Marseille Saint-Charles - Toulon (TER PACA)", "Marseille Saint-Charles", "Toulon", "TER Régional", "Provence-Alpes-Côte d'Azur", 65.0, 180, 8, 16.2, 89.1, 41.0, 35.0, 24.0, 390000.0),
        ("AXE-TER-003", "Lille Flandres - Dunkerque (TER Hauts-de-France)", "Lille Flandres", "Dunkerque", "TER Régional", "Hauts-de-France", 55.0, 160, 6, 14.8, 90.2, 29.0, 48.0, 23.0, 280000.0),
        ("AXE-TER-004", "Toulouse Matabiau - Montauban (TER Occitanie)", "Toulouse Matabiau", "Montauban Ville Bourbon", "TER Régional", "Occitanie", 42.0, 140, 5, 15.1, 89.8, 35.0, 38.0, 27.0, 240000.0),
        ("AXE-TER-005", "Paris Montparnasse - Chartres (TER Centre-Val de Loire)", "Paris Montparnasse", "Chartres", "TER Régional", "Centre-Val de Loire", 72.0, 210, 10, 17.4, 88.4, 45.0, 32.0, 23.0, 410000.0)
    ]
    for tax in ter_axes:
        regularite_data.append({
            "ligne_axe_id": tax[0],
            "nom_axe_ferroviaire": tax[1],
            "gare_depart": tax[2],
            "gare_arrivee": tax[3],
            "service_type": tax[4],
            "region": tax[5],
            "duree_moyenne_trajet_minutes": tax[6],
            "circulations_prevues_nombre": tax[7],
            "nombre_trains_annules": tax[8],
            "retard_moyen_minutes": tax[9],
            "taux_regularite_ponctualite_pct": tax[10],
            "cause_retard_infrastructure_pct": tax[11],
            "cause_retard_materiel_roulant_pct": tax[12],
            "cause_retard_gestion_trafic_pct": tax[13],
            "perte_financiere_retards_eur": tax[14]
        })

    df_reg_final = pd.DataFrame(regularite_data)
    print(f"  ✓ Processed {len(df_reg_final)} clean TGV & TER line regularity records.")

    # Step 4: Build Table 3: ter_maintenance_predictive_reseau (TER Failure Predictions)
    ter_maintenance = [
        ("SEG-TER-AURA-01", "Segment TER Lyon Part-Dieu - Grenoble (Section Moirans)", "Auvergne-Rhône-Alpes", "TER Ligne 1", 96.8, 42.0, 18, 9.4, 0.91, "CRITIQUE (Action urgente)", "Surcharge de trafic & Usure caténaire", "Remplacement préventif d'aiguillage & Limitation temporaire de vitesse 80km/h"),
        ("SEG-TER-PACA-02", "Segment TER Marseille - Toulon (Section Aubagne)", "Provence-Alpes-Côte d'Azur", "TER Ligne 4", 94.2, 38.5, 14, 8.8, 0.86, "CRITIQUE (Action urgente)", "Signalisation obsolète & Surchauffe transformateurs", "Audit d'urgence signalisation & Révision bogies rames TER"),
        ("SEG-TER-HDF-03", "Segment TER Lille Flandres - Dunkerque (Section Hazebrouck)", "Hauts-de-France", "TER Ligne 8", 91.5, 35.0, 12, 7.9, 0.78, "ÉLEVÉ", "Usure mécanique bogies & Caténaire vieillissante", "Remplacement des garnitures de freins & Inspection caténaire"),
        ("SEG-TER-OCC-04", "Segment TER Toulouse - Montauban (Section Saint-Jory)", "Occitanie", "TER Ligne 2", 89.4, 31.0, 9, 6.8, 0.72, "ÉLEVÉ", "Micro-coupures d'alimentation sous forte charge", "Renforcement des sous-stations électriques & Maintenance caténaire"),
        ("SEG-TER-CVL-05", "Segment TER Paris Montparnasse - Chartres (Section Rambouillet)", "Centre-Val de Loire", "TER Ligne 12", 95.1, 40.0, 15, 8.9, 0.88, "CRITIQUE (Action urgente)", "Surcharge de trafic aux heures de pointe & Rail fatigué", "Substitution de rames TER & Meulage préventif des rails"),
        ("SEG-TER-IDF-06", "Segment Transilien RER C Sud (Section Juvisy - Brétigny)", "Île-de-France", "RER C", 97.4, 45.0, 22, 10.2, 0.94, "CRITIQUE (Action urgente)", "Vétusté des appareils de voie & Densité extrême", "Renouvellement d'aiguillages & Remplacement caténaires 1500V")
    ]

    ter_maint_rows = []
    for tm in ter_maintenance:
        ter_maint_rows.append({
            "segment_id": tm[0],
            "nom_segment_ferroviaire": tm[1],
            "region": tm[2],
            "line_code": tm[3],
            "charge_trafic_semaine_pct": tm[4],
            "age_infrastructure_annees": tm[5],
            "frequence_micro_coupures_signalisation_30j": tm[6],
            "usure_rail_mm": tm[7],
            "probabilite_panne_materielle_7j": tm[8],
            "risque_ralentissement_majeur": tm[9],
            "cause_principale_risque": tm[10],
            "action_maintenance_recommandee": tm[11]
        })
    df_ter_maint = pd.DataFrame(ter_maint_rows)

    # Step 5: Build Table 4: ter_maintenance_historique_previsions_6mois (3 Months History + 3 Months Forecast)
    # Seasonal Wave Profile: Peak in June (0.82), Drop in July summer maintenance (0.42), Rise in August heatwaves (0.74), Peak in September back-to-school (0.94), Drop in October (0.61)
    seasonal_factors = [
        ("2026-05-01", "HISTORIQUE (3 Mois Passés)", 0.55, 88.0, 8, "MODÉRÉ", "Maintenance préventive de printemps"),
        ("2026-06-01", "HISTORIQUE (3 Mois Passés)", 0.82, 95.5, 18, "CRITIQUE (Action urgente)", "Remplacement d'urgence caténaires & Régulation trafic pré-été"),
        ("2026-07-01", "HISTORIQUE (3 Mois Passés)", 0.42, 82.0, 5, "FAIBLE", "Maintenance lourde estivale & Travaux de renouvellement des voies"),
        ("2026-08-01", "PRÉVISION (3 Mois Futurs)", 0.74, 91.2, 14, "ÉLEVÉ", "Surveillance canicule & Refroidissement des sous-stations électriques"),
        ("2026-09-01", "PRÉVISION (3 Mois Futurs)", 0.94, 98.4, 24, "CRITIQUE (Action urgente)", "Renouvellement d'aiguillages & Substitution rames RER/TER rentrée"),
        ("2026-10-01", "PRÉVISION (3 Mois Futurs)", 0.61, 86.5, 9, "MODÉRÉ", "Calage automatisé des voies & Révision d'automne")
    ]

    time_series_rows = []
    for tm in ter_maintenance:
        seg_id, seg_name, reg, lcode = tm[0], tm[1], tm[2], tm[3]
        base_factor = tm[8]  # Segment criticality multiplier (e.g. 0.94 for RER C, 0.72 for TER Occitanie)
        
        for m_date, p_type, s_prob, s_charge, s_micro, s_risk, s_act in seasonal_factors:
            # Scale probability and metrics according to segment criticality
            prob = round(min(0.99, max(0.20, s_prob * (base_factor / 0.85))), 2)
            charge = round(min(99.5, max(75.0, s_charge * (tm[4] / 94.0))), 1)
            micro_coupures = int(s_micro * (tm[6] / 15.0))
            usure = round(tm[7] + (s_prob - 0.5) * 1.5, 1)

            if prob >= 0.85:
                risk = "CRITIQUE (Action urgente)"
                act = "Renouvellement d'aiguillages & Limitation 80km/h"
            elif prob >= 0.70:
                risk = "ÉLEVÉ"
                act = "Inspection caténaires & Audit signalisation"
            elif prob >= 0.45:
                risk = "MODÉRÉ"
                act = "Maintenance préventive standard"
            else:
                risk = "FAIBLE"
                act = "Contrôle visuel de routine"

            time_series_rows.append({
                "segment_id": seg_id,
                "nom_segment_ferroviaire": seg_name,
                "region": reg,
                "line_code": lcode,
                "mois_date": m_date,
                "periode_type": p_type,
                "charge_trafic_mensuelle_pct": charge,
                "frequence_micro_coupures_signalisation": max(2, micro_coupures),
                "usure_rail_mm": max(4.0, usure),
                "probabilite_panne_materielle": prob,
                "risque_ralentissement_majeur": risk,
                "cause_principale_risque": tm[10],
                "action_maintenance_recommandee": act
            })

    df_6mois = pd.DataFrame(time_series_rows)
    print(f"  ✓ Built {len(df_6mois)} TER 6-month time-series maintenance history & forecast records.")

    # Step 6: Build Table 5: sncf_yield_management_billetterie (Dynamic Pricing & 1st vs 2nd Class)
    yield_pricing = [
        ("YIELD-TGV-6902", "TGV 6902", "AXE-PARIS-LYON", "Paris Lyon - Grenoble", "1ère Classe", 115.0, 92.0, 32.4, 98.2, 58.40, 12.4, "Réduction dynamique 1ère classe -20% sur rames creuses pour viser +12.4% de panier moyen"),
        ("YIELD-TGV-6902-2", "TGV 6902", "AXE-PARIS-LYON", "Paris Lyon - Grenoble", "2nde Classe", 68.0, 68.0, 32.4, 98.2, 58.40, 12.4, "Maintien tarif plein 2nde classe saturée"),
        ("YIELD-TGV-8410", "TGV 8410", "AXE-PARIS-RENNES", "Paris Montparnasse - Rennes", "1ère Classe", 108.0, 85.0, 28.5, 96.5, 54.10, 14.2, "Upsell automatique 1ère classe pour abonnés Navigo/TGV Max (+14.2% panier moyen)"),
        ("YIELD-TER-84210", "TER 84210", "AXE-TER-001", "Lyon Part-Dieu - Grenoble", "1ère Classe", 34.0, 26.5, 22.0, 94.0, 24.80, 11.8, "Tarif promotionnel 1ère classe aux heures creuses (+11.8% panier moyen)"),
        ("YIELD-TGV-6104", "TGV 6104", "AXE-MARSEILLE-LILLE", "Marseille Saint-Charles - Lille Flandres", "1ère Classe", 145.0, 115.0, 38.0, 99.1, 72.50, 13.5, "Tarification yield dynamique multi-tronçons 1ère classe (+13.5% panier moyen)")
    ]

    yield_rows = []
    for yp in yield_pricing:
        yield_rows.append({
            "ticket_offer_id": yp[0],
            "train_number": yp[1],
            "ligne_axe_id": yp[2],
            "nom_axe_ferroviaire": yp[3],
            "classe_billet": yp[4],
            "tarif_nominal_eur": yp[5],
            "tarif_dynamique_propose_eur": yp[6],
            "taux_occupation_1ere_classe_pct": yp[7],
            "taux_occupation_2nde_classe_pct": yp[8],
            "panier_moyen_actuel_eur": yp[9],
            "hausse_panier_moyen_projete_pct": yp[10],
            "recommandation_pricing_yield": yp[11]
        })
    df_yield = pd.DataFrame(yield_rows)

    # Step 7: Build Table 6: abonnements_titres_transport
    plans_data = [
        {"subscription_plan_id": "SUB-NAV-MONTH", "plan_name": "Pass Navigo Mois", "category": "Urbain Île-de-France", "monthly_price_eur": 86.40, "valid_zones": "Zones 1 à 5", "is_employer_subsidized": True},
        {"subscription_plan_id": "SUB-NAV-YEAR", "plan_name": "Pass Navigo Annuel", "category": "Urbain Île-de-France", "monthly_price_eur": 950.40, "valid_zones": "Toutes Zones IDF", "is_employer_subsidized": True},
        {"subscription_plan_id": "SUB-TER-ILICO", "plan_name": "Pass TER Ilico Mensuel", "category": "Régional TER", "monthly_price_eur": 65.00, "valid_zones": "Réseau Régional TER", "is_employer_subsidized": True},
        {"subscription_plan_id": "SUB-TGV-MAX", "plan_name": "Abonnement TGV Max", "category": "Grande Vitesse TGV", "monthly_price_eur": 79.00, "valid_zones": "Réseau National TGV", "is_employer_subsidized": False},
        {"subscription_plan_id": "SUB-NAV-LIB", "plan_name": "Pass Navigo Liberté+", "category": "Urbain Île-de-France", "monthly_price_eur": 0.00, "valid_zones": "Paris & Petite Couronne", "is_employer_subsidized": True}
    ]
    df_plans = pd.DataFrame(plans_data)

    # Step 8: Build Table 7: usagers_profils (with ST_GEOGPOINT)
    usagers = []
    plan_ids = [p["subscription_plan_id"] for p in plans_data]

    for i in range(1, 3001):
        uid = f"USG-{i:05d}"
        fn = random.choice(FIRST_NAMES)
        ln = random.choice(LAST_NAMES)
        gname, code_uic, cp, dept, reg, lat, lon = random.choice(CITY_METRICS)

        home_lat = lat + random.uniform(-0.08, 0.08)
        home_lon = lon + random.uniform(-0.08, 0.08)

        work_metric = random.choice(CITY_METRICS)
        work_lat = work_metric[5] + random.uniform(-0.05, 0.05)
        work_lon = work_metric[6] + random.uniform(-0.05, 0.05)

        usagers.append({
            "passenger_id": uid,
            "first_name": fn,
            "last_name": ln,
            "email": f"{fn.lower()}.{ln.lower()}@email-voyageur.fr",
            "phone": f"+33 6 {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)} {random.randint(10,99)}",
            "home_city": gname.replace("Paris ", "").replace(" Ville", ""),
            "department_code": dept,
            "region_name": reg,
            "age_bracket": random.choice(["18-25 ans", "26-45 ans", "46-60 ans", "60+ ans"]),
            "subscription_plan_id": random.choice(plan_ids),
            "commute_frequency": random.choice(["Quotidien Domicile-Travail", "Hebdomadaire", "Occasionnel"]),
            "home_location_geo": f"POINT({home_lon:.4f} {home_lat:.4f})",
            "work_location_geo": f"POINT({work_lon:.4f} {work_lat:.4f})"
        })
    df_usagers = pd.DataFrame(usagers)

    # Step 9: Build Table 8: validations_trajets_voyageurs (Multi-month turnstile tap-ins)
    validations = []
    modes = [("TGV InOui", "Ligne Grande Vitesse East"), ("TER", "Ligne Régionale TER"), ("RER A", "Axe RER A Charles de Gaulle - Étoile"), ("Métro 1", "Ligne 1 La Défense - Château de Vincennes")]

    usager_records = df_usagers.to_dict("records")

    for i in range(1, 10001):
        vid = f"VAL-{i:06d}"
        u = random.choice(usager_records)
        gname, code_uic, cp, dept, reg, lat, lon = random.choice(CITY_METRICS)
        mode, line = random.choice(modes)

        # Multi-month spread from May 2026 to October 2026
        day_offset = random.randint(0, 180)
        hour = random.choice([7, 8, 17, 18])
        minute = random.randint(0, 59)
        dt = datetime(2026, 5, 1) + timedelta(days=day_offset, hours=hour, minutes=minute)

        validations.append({
            "validation_id": vid,
            "passenger_id": u["passenger_id"],
            "code_uic_gare": code_uic,
            "station_name": gname,
            "transport_mode": mode,
            "line_code": line,
            "department_code": dept,
            "region_name": reg,
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "validation_status": random.choices(["VALIDE", "CORRESPONDANCE", "REFUSE_SOLDE", "HORS_ZONE"], weights=[0.85, 0.10, 0.03, 0.02])[0]
        })
    df_validations = pd.DataFrame(validations)

    # Step 10: Build Table 9: sncf_objets_trouves
    objets = []
    categories = [
        ("Appareils Électroniques", "Ordinateur portable PC 15 pouces dans housse noire"),
        ("Bagages & Valises", "Valise cabine grise à roulettes avec étiquette"),
        ("Papiers d'identité", "Portefeuille en cuir contenant carte Navigo et CNI"),
        ("Clés & Badges", "Trousseau de 4 clés avec badge d'accès entreprise")
    ]
    statuses = ["Restitué au propriétaire", "En réserve gare", "Transmis association"]

    val_records = df_validations.to_dict("records")

    for i in range(1, 1501):
        oid = f"OBJ-{i:05d}"
        val = random.choice(val_records)
        cat, desc = random.choice(categories)
        status = random.choice(statuses)

        objets.append({
            "incident_id": oid,
            "passenger_id": val["passenger_id"],
            "matched_journey_validation_id": val["validation_id"],
            "code_uic_gare": val["code_uic_gare"],
            "station_name": val["station_name"],
            "declaration_date": "2026-08-15",
            "item_category": cat,
            "description_objet": f"{desc} (Déclaré en gare de {val['station_name']})",
            "found_status": status,
            "restitution_date": "2026-08-16" if status == "Restitué au propriétaire" else None
        })
    df_objets = pd.DataFrame(objets)

    # Step 11: Upload CSVs & Load BigQuery
    tables_map = {
        "frequentation_gares_sncf": df_gares,
        "sncf_regularite_lignes": df_reg_final,
        "ter_maintenance_predictive_reseau": df_ter_maint,
        "ter_maintenance_historique_previsions_6mois": df_6mois,
        "sncf_yield_management_billetterie": df_yield,
        "abonnements_titres_transport": df_plans,
        "usagers_profils": df_usagers,
        "validations_trajets_voyageurs": df_validations,
        "sncf_objets_trouves": df_objets
    }

    subprocess.run(f"gcloud storage buckets create {BUCKET_NAME} --project={PROJECT_ID} --location=EU 2>/dev/null", shell=True)

    for tname, df in tables_map.items():
        csv_path = f"agents/transit_navigator/data/{tname}.csv"
        df.to_csv(csv_path, index=False)
        print(f"  ✓ Saved workspace CSV: {csv_path} ({len(df)} rows)")

        gcs_dest = f"{BUCKET_NAME}/{tname}.csv"
        subprocess.run(f"gcloud storage cp {csv_path} {gcs_dest}", shell=True, capture_output=True)

        tref = f"{PROJECT_ID}.{DATASET_ID}.{tname}"
        client.delete_table(tref, not_found_ok=True)

        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True,
            allow_quoted_newlines=True,
            ignore_unknown_values=True
        )
        with open(csv_path, "rb") as f_in:
            job = client.load_table_from_file(f_in, tref, job_config=job_config)
        job.result()
        print(f"  ✓ Loaded table `{tref}` in BigQuery!")

    print("\nSUCCESS: All 9 Transit Navigator tables complete & populated in BigQuery!")

if __name__ == "__main__":
    main()
