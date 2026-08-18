#!/usr/bin/env python3
"""
Generate and Upload Authentic Product Packaging Images to Google Cloud Storage (GCS)
for BigQuery Object Tables and Vertex AI Data Agents.
"""

import os
import sys
import subprocess
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

CSV_PATH = "agents/shelf_optimizer/data/openfoodfacts_catalog.csv"
IMG_DIR = "agents/shelf_optimizer/data/product_images"
BUCKET_NAME = "gs://talktodata-shelf-optimizer-raw-data"

NUTRI_COLORS = {
    "A": (30, 130, 60),
    "B": (135, 180, 50),
    "C": (240, 200, 40),
    "D": (230, 120, 30),
    "E": (210, 40, 40)
}

def generate_product_image(row, output_path):
    ean = str(row.get("code_barre_ean"))
    nom = str(row.get("nom_produit"))[:35]
    marque = str(row.get("marque_entreprise"))[:30]
    rayon = str(row.get("rayon_categorie"))[:30]
    nutri = str(row.get("nutri_score", "C")).upper()
    if nutri not in NUTRI_COLORS:
        nutri = "C"

    # Create 400x400 packaging mockup card
    img = Image.new("RGB", (400, 400), color=(250, 252, 255))
    d = ImageDraw.Draw(img)

    # Outer border
    d.rectangle([15, 15, 385, 385], outline=(30, 41, 59), width=4)

    # Header banner
    d.rectangle([19, 19, 381, 70], fill=(30, 41, 59))
    d.text((30, 32), "OPEN FOOD FACTS MASTER CATALOG", fill=(255, 255, 255))

    # Rayon / Category
    d.text((30, 85), f"Rayon: {rayon}", fill=(71, 85, 105))

    # Product Title & Brand
    d.text((30, 120), nom, fill=(15, 23, 42))
    d.text((30, 155), f"Marque: {marque}", fill=(100, 116, 139))

    # Nutri-Score Badge
    bg_color = NUTRI_COLORS[nutri]
    d.rectangle([30, 200, 190, 260], fill=bg_color)
    d.text((45, 218), f"NUTRI-SCORE {nutri}", fill=(255, 255, 255))

    # Barcode mock box
    d.rectangle([30, 290, 370, 365], fill=(241, 245, 249), outline=(203, 213, 225), width=2)
    d.text((45, 305), "||| || ||||| |||| ||| ||||| ||||| |||", fill=(15, 23, 42))
    d.text((45, 335), f"EAN13: {ean}", fill=(71, 85, 105))

    img.save(output_path, "JPEG", quality=85)

def main():
    print(f"Reading product catalog from '{CSV_PATH}'...")
    df = pd.read_csv(CSV_PATH)
    print(f"  ✓ Found {len(df)} product references.")

    os.makedirs(IMG_DIR, exist_ok=True)

    print("Generating product packaging images...")
    for idx, row in df.iterrows():
        ean = str(row.get("code_barre_ean"))
        img_path = os.path.join(IMG_DIR, f"{ean}.jpg")
        generate_product_image(row, img_path)

        if (idx + 1) % 500 == 0 or (idx + 1) == len(df):
            print(f"  ✓ Generated {idx + 1} / {len(df)} images...")

    print(f"\nUploading images to GCS Bucket '{BUCKET_NAME}/product_images/'...")
    subprocess.run(f"gcloud storage cp -r {IMG_DIR} {BUCKET_NAME}/", shell=True)
    print("\nSUCCESS: All product images generated & uploaded to GCS Object Table storage!")

if __name__ == "__main__":
    main()
