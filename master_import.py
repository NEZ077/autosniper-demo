import pandas as pd
import os
import glob
import random
from datetime import datetime

# CONFIGURATION
IMPORT_FOLDER = "imports"   # Dossier où tu mets tes fichiers CSV bruts
OUTPUT_FILE = "annonces.csv" # Fichier final pour l'appli

def clean_price(price_str):
    if pd.isna(price_str): return 0
    clean = str(price_str).replace("€", "").replace(".", "").replace(",", "").replace("-", "").strip()
    try: return int(clean)
    except: return 0

def process_file(filepath):
    """Détecte le type de fichier et extrait les données"""
    try:
        df = pd.read_csv(filepath)
    except:
        print(f"❌ Impossible de lire {filepath}")
        return []

    annonces = []
    source_detected = "Inconnue"
    
    # --- DÉTECTION DU TYPE DE FICHIER ---
    cols = " ".join(df.columns)
    
    # CAS 1 : AUTOSCOUT24 (Structure complexe "pageProps")
    if "pageProps.listings" in cols:
        source_detected = "AutoScout24"
        # On cherche le nombre max de listings
        max_idx = 0
        for c in df.columns:
            if "pageProps.listings." in c:
                try: max_idx = max(max_idx, int(c.split(".")[2]))
                except: pass
        
        for _, row in df.iterrows():
            for i in range(max_idx + 1):
                p = f"pageProps.listings.{i}"
                if f"{p}.id" not in row or pd.isna(row[f"{p}.id"]): continue
                
                # Extraction AS24
                prix = clean_price(row.get(f"{p}.price.priceFormatted", 0))
                url_raw = row.get(f"{p}.url", "")
                lien = f"https://www.autoscout24.fr{url_raw}" if url_raw.startswith("/") else url_raw
                
                annonces.append({
                    "id": f"as-{row.get(f'{p}.id')}",
                    "marque": row.get(f"{p}.vehicle.make", "Inconnue"),
                    "modele": row.get(f"{p}.vehicle.model", "Inconnu"),
                    "titre": f"{row.get(f'{p}.vehicle.make')} {row.get(f'{p}.vehicle.model')} {row.get(f'{p}.vehicle.modelVersionInput', '')}",
                    "prix": prix,
                    "km": row.get(f"{p}.vehicle.mileageInKm", 0),
                    "annee": str(row.get(f"{p}.tracking.firstRegistration", "2020")).split("/")[-1],
                    "img_url": row.get(f"{p}.images.0", ""),
                    "lien_annonce": lien,
                    "description": f"Import AutoScout. {row.get(f'{p}.vehicle.fuel', '')}, {row.get(f'{p}.vehicle.transmission', '')}.",
                    "source": "AutoScout24",
                    "options": "Voir annonce", "carburant": row.get(f"{p}.vehicle.fuel", "N/C"), "boite": row.get(f"{p}.vehicle.transmission", "N/C"), "chevaux": row.get(f"{p}.vehicle.hp", "N/C"), "couleur": "N/C", "ville": row.get(f"{p}.location.city", "Europe")
                })

    # CAS 2 : LEBONCOIN (Structure "subject", "body")
    elif "subject" in df.columns and "body" in df.columns:
        source_detected = "LeBonCoin"
        for _, row in df.iterrows():
            # Extraction Attributs LBC
            attrs = {}
            for col in df.columns:
                if col.startswith("attributes.") and col.endswith(".key"):
                    idx = col.split(".")[1]
                    key = row[col]
                    val = row.get(f"attributes.{idx}.value_label")
                    if pd.isna(val): val = row.get(f"attributes.{idx}.value")
                    attrs[key] = val
            
            # Gestion Image LBC
            img = "https://via.placeholder.com/400x300?text=No+Photo"
            if "images.urls_large.0" in row and pd.notna(row["images.urls_large.0"]): img = row["images.urls_large.0"]
            elif "images.urls.0" in row and pd.notna(row["images.urls.0"]): img = row["images.urls.0"]

            annonces.append({
                "id": f"lbc-{row.get('list_id', random.randint(1000,9999))}",
                "marque": attrs.get("brand", "Inconnue"),
                "modele": attrs.get("model", "Inconnu"),
                "titre": row.get("subject", "Annonce"),
                "prix": int(row.get("price.0", 0)) if pd.notna(row.get("price.0")) else 0,
                "km": str(attrs.get("mileage", "0")).replace(" ", ""),
                "annee": str(attrs.get("regdate", "2020")),
                "img_url": img,
                "lien_annonce": row.get("url", ""),
                "description": str(row.get("body", "")).replace("\n", " ")[:600],
                "source": "LeBonCoin",
                "options": "Voir description", "carburant": attrs.get("fuel", "N/C"), "boite": attrs.get("gearbox", "N/C"), "chevaux": attrs.get("horsepower", "N/C"), "couleur": attrs.get("color", "N/C"), "ville": row.get("location.city", "France")
            })
    
    print(f"   📄 {os.path.basename(filepath)} : {len(annonces)} annonces ({source_detected})")
    return annonces

def run_master_import():
    print("🏭 USINE D'IMPORTATION ACTIVÉE...")
    
    all_files = glob.glob(os.path.join(IMPORT_FOLDER, "*.csv"))
    if not all_files:
        print(f"⚠️ Aucun fichier CSV trouvé dans le dossier '{IMPORT_FOLDER}' !")
        return

    all_data = []
    
    # 1. On traite tous les fichiers
    for f in all_files:
        all_data.extend(process_file(f))
        
    # 2. On transforme en DataFrame pour nettoyer et calculer
    df = pd.DataFrame(all_data)
    
    # 3. Calculs automatiques (Cote, Gain, Status)
    if not df.empty:
        df['prix'] = pd.to_numeric(df['prix'], errors='coerce').fillna(0).astype(int)
        df['cote_argus'] = (df['prix'] * 1.15).astype(int) # Simulation simple
        df['gain'] = df['cote_argus'] - df['prix']
        df['status'] = df.apply(lambda x: "Pépite" if x['gain'] > 3000 else "Clean", axis=1)
        df['temps'] = "1h" # Remplir avec une valeur par défaut
        df['date_scrape'] = datetime.now().strftime("%Y-%m-%d")
        
        # Colonnes obligatoires pour l'App
        required_cols = ["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "status", "source", "temps", "lien_annonce", "description", "date_scrape"]
        for c in required_cols:
            if c not in df.columns: df[c] = ""
        
        # Sauvegarde finale
        df[required_cols].to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n✅ TERMINÉ ! {len(df)} annonces prêtes dans {OUTPUT_FILE}")
    else:
        print("❌ Aucune annonce valide trouvée.")

if __name__ == "__main__":
    run_master_import()