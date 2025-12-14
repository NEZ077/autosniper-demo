import pandas as pd
import os
import glob
import random
from datetime import datetime
import re

# --- CONFIGURATION ---
# Mets tous tes fichiers CSV (LBC, AutoScout...) dans ce dossier
IMPORT_FOLDER = "imports"   
OUTPUT_FILE = "annonces.csv"

def clean_power(valeur):
    if pd.isna(valeur): return 0
    s = str(valeur).lower().replace(',', '.')
    # On extrait le chiffre
    match = re.search(r"(\d+[\.]?\d*)", s)
    if not match: return 0
    num = float(match.group(1))
    
    # Si c'est des kW (souvent le cas sur AutoScout), on convertit
    if "kw" in s:
        return int(num * 1.36)
    
    # Sinon on retourne le chiffre tel quel (supposé être des ch)
    return int(num)

def clean_price(price_str):
    """Nettoie les prix (enlève €, les points, les virgules...)"""
    if pd.isna(price_str): return 0
    clean = str(price_str).replace("€", "").replace(".", "").replace(",", "").replace("-", "").strip()
    try: return int(clean)
    except: return 0

def detecter_et_convertir(filepath):
    """Lit un CSV et devine si c'est Leboncoin ou AutoScout"""
    try:
        # On essaie de lire avec différents encodages pour éviter les erreurs
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
        except:
            df = pd.read_csv(filepath, encoding='latin-1')
    except Exception as e:
        print(f"❌ Erreur lecture {filepath}: {e}")
        return []

    annonces = []
    cols = " ".join(df.columns)
    filename = os.path.basename(filepath)

    # --- CAS 1 : AUTOSCOUT24 (Format 'pageProps') ---
    if "pageProps.listings" in cols:
        print(f"   🔹 {filename} : Format AUTOSCOUT24 détecté")
        
        # Trouver le nombre max de colonnes listings
        max_idx = 0
        for c in df.columns:
            if "pageProps.listings." in c:
                try: max_idx = max(max_idx, int(c.split(".")[2]))
                except: pass
        
        for _, row in df.iterrows():
            for i in range(max_idx + 1):
                p = f"pageProps.listings.{i}"
                if f"{p}.id" not in row or pd.isna(row[f"{p}.id"]): continue
                
                # Extraction
                prix = clean_price(row.get(f"{p}.price.priceFormatted", 0))
                url_raw = row.get(f"{p}.url", "")
                # Correction lien relatif AS24
                lien = f"https://www.autoscout24.fr{url_raw}" if str(url_raw).startswith("/") else url_raw
                
                marque = row.get(f"{p}.vehicle.make", "Inconnue")
                modele = row.get(f"{p}.vehicle.model", "Inconnu")
                version = row.get(f"{p}.vehicle.modelVersionInput", "")
                
                # Image
                img = row.get(f"{p}.images.0", "")
                if pd.isna(img): img = "https://via.placeholder.com/400x300?text=No+Image"

                annonces.append({
                    "id": f"as-{row.get(f'{p}.id')}",
                    "marque": marque,
                    "modele": modele,
                    "titre": f"{marque} {modele} {version}".strip(),
                    "prix": prix,
                    "km": row.get(f"{p}.vehicle.mileageInKm", 0),
                    "annee": str(row.get(f"{p}.tracking.firstRegistration", "2020")).split("/")[-1],
                    "img_url": img,
                    "lien_annonce": lien,
                    "description": f"Import AutoScout. {row.get(f'{p}.vehicle.fuel', '')}, {row.get(f'{p}.vehicle.transmission', '')}. {version}",
                    "source": "AutoScout24",
                    "options": "Voir annonce détaillée", 
                    "carburant": row.get(f"{p}.vehicle.fuel", "N/C"), 
                    "boite": row.get(f"{p}.vehicle.transmission", "N/C"), 
                    "chevaux": clean_power(row.get(f"{p}.vehicle.hp") or row.get(f"{p}.vehicle.rawPower")), 
                    "couleur": "N/C", 
                    "ville": row.get(f"{p}.location.city", "Europe"),
                    "temps": f"{random.randint(1, 12)}h"
                })

    # --- CAS 2 : LEBONCOIN (Format 'subject' + 'attributes') ---
    elif "subject" in df.columns: # Verification simplifiée
        print(f"   🔸 {filename} : Format LEBONCOIN détecté")
        
        for index, row in df.iterrows():
            attrs = {}
            # Extraction dynamique des attributs LBC (attributes.X.key / value)
            for col in df.columns:
                if col.startswith("attributes.") and col.endswith(".key"):
                    try:
                        idx = col.split(".")[1]
                        key = row[col]
                        # On cherche la valeur lisible (label) ou la valeur brute
                        val = row.get(f"attributes.{idx}.value_label")
                        if pd.isna(val): val = row.get(f"attributes.{idx}.value")
                        attrs[key] = val
                    except: pass
            
            # Image LBC
            img = "https://via.placeholder.com/400x300?text=No+Photo"
            if "images.urls_large.0" in row and pd.notna(row["images.urls_large.0"]): img = row["images.urls_large.0"]
            elif "images.urls.0" in row and pd.notna(row["images.urls.0"]): img = row["images.urls.0"]

            annonces.append({
                "id": f"lbc-{row.get('list_id', random.randint(10000,99999))}",
                "marque": attrs.get("brand", "Inconnue"),
                "modele": attrs.get("model", "Inconnu"),
                "titre": row.get("subject", "Annonce LBC"),
                "prix": int(row.get("price.0", 0)) if pd.notna(row.get("price.0")) else 0,
                "km": str(attrs.get("mileage", "0")).replace(" ", ""),
                "annee": str(attrs.get("regdate", "2020")),
                "img_url": img,
                "lien_annonce": row.get("url", ""),
                "description": str(row.get("body", "")).replace("\n", " ")[:800],
                "source": "LeBonCoin",
                "options": "Voir description", 
                "carburant": attrs.get("fuel", "N/C"), 
                "boite": attrs.get("gearbox", "N/C"), 
                "chevaux": clean_power(attrs.get("horsepower") or attrs.get("fiscal_power")), 
                "couleur": attrs.get("color", "N/C"), 
                "ville": row.get("location.city", "France"),
                "temps": f"{random.randint(1, 24)}h"
            })
    
    else:
        print(f"   ⚠️ {filename} : Format inconnu ou colonnes manquantes.")

    return annonces

def run_scraper():
    print("🏭 USINE D'IMPORTATION ACTIVÉE...")
    print(f"📂 Recherche de fichiers CSV dans '{IMPORT_FOLDER}'...")
    
    # Création du dossier imports s'il n'existe pas
    if not os.path.exists(IMPORT_FOLDER):
        os.makedirs(IMPORT_FOLDER)
        print(f"✅ Dossier '{IMPORT_FOLDER}' créé. Glisse tes CSV dedans !")
        return

    all_files = glob.glob(os.path.join(IMPORT_FOLDER, "*.csv"))
    if not all_files:
        print(f"⚠️ Aucun fichier CSV trouvé dans '{IMPORT_FOLDER}'.")
        return

    all_data = []
    
    # 1. Traitement de tous les fichiers
    for f in all_files:
        all_data.extend(detecter_et_convertir(f))
        
    # 2. Nettoyage et Fusion
    if all_data:
        df = pd.DataFrame(all_data)
        
        # Nettoyage types numériques
        df['prix'] = pd.to_numeric(df['prix'], errors='coerce').fillna(0).astype(int)
        
        # NOTE : La cote Argus "intelligente" est calculée dans app.py
        # Ici on met juste une valeur par défaut pour éviter les bugs
        df['cote_argus'] = (df['prix'] * 1.1).astype(int) 
        df['status'] = "Clean"
        df['distance'] = "10"
        df['date_scrape'] = datetime.now().strftime("%Y-%m-%d")
        
        # Sélection finale des colonnes pour app.py
        cols_finales = ["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", 
                        "ville", "distance", "url", "img_url", "options", "carburant", "boite", 
                        "couleur", "chevaux", "status", "source", "temps", "lien_annonce", 
                        "description", "date_scrape"]
        
        # Ajout colonnes manquantes vides
        for c in cols_finales:
            if c not in df.columns: df[c] = ""
            
        # Sauvegarde
        df[cols_finales].to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
        print(f"\n✅ SUCCÈS ! {len(df)} annonces injectées dans {OUTPUT_FILE}")
        print("👉 Lance 'streamlit run app.py' pour voir le résultat.")
    else:
        print("❌ Aucune annonce valide récupérée.")

if __name__ == "__main__":
    run_scraper()