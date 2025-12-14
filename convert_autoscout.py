import pandas as pd
import random
import os
from datetime import datetime

# CONFIGURATION
INPUT_FILE = "compiled-results.csv"  # Le fichier HAR converti d'AutoScout
OUTPUT_FILE = "annonces.csv"         # Ton fichier principal

def clean_price(price_str):
    """Nettoie le prix (enlève €, les points, les virgules...)"""
    if pd.isna(price_str): return 0
    clean = str(price_str).replace("€", "").replace(".", "").replace(",", "").replace("-", "").strip()
    try:
        return int(clean)
    except:
        return 0

def convert_autoscout():
    print(f"🌍 Lecture du fichier AutoScout {INPUT_FILE}...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erreur : Fichier {INPUT_FILE} introuvable.")
        return

    try:
        df_raw = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"❌ Erreur de lecture : {e}")
        return

    nouvelles_annonces = []
    
    # AutoScout met toutes les annonces sur une seule ligne (ou quelques lignes)
    # On doit parcourir les colonnes "listings.0", "listings.1", etc.
    
    # On cherche combien d'annonces max il y a par ligne (en regardant les colonnes)
    max_index = 0
    for col in df_raw.columns:
        if "pageProps.listings." in col:
            try:
                # Extrait le numéro X de pageProps.listings.X.id
                idx = int(col.split(".")[2])
                if idx > max_index: max_index = idx
            except:
                pass

    print(f"⚙️ Détection de {max_index + 1} slots d'annonces potentiels...")

    # Pour chaque ligne du fichier (souvent 1 ligne = 1 page de résultats)
    for row_idx, row in df_raw.iterrows():
        
        # On parcourt chaque slot d'annonce (0, 1, 2...)
        for i in range(max_index + 1):
            prefix = f"pageProps.listings.{i}"
            
            # Vérifie si l'annonce existe
            if f"{prefix}.id" not in row or pd.isna(row[f"{prefix}.id"]):
                continue

            # --- 1. EXTRACTION DES DONNÉES ---
            id_annonce = f"as24-{row.get(f'{prefix}.id')}"
            
            marque = row.get(f"{prefix}.vehicle.make", "Inconnue")
            modele = row.get(f"{prefix}.vehicle.model", "Inconnu")
            version = row.get(f"{prefix}.vehicle.modelVersionInput", "")
            titre = f"{marque} {modele} {version}".strip()
            
            # Prix
            prix_raw = row.get(f"{prefix}.price.priceFormatted", "0")
            prix = clean_price(prix_raw)
            
            # Km & Année
            km = row.get(f"{prefix}.vehicle.mileageInKm", "0")
            annee_raw = str(row.get(f"{prefix}.tracking.firstRegistration", "2020"))
            # Souvent format "05/2020", on garde juste l'année
            annee = annee_raw.split("/")[-1] if "/" in annee_raw else annee_raw
            
            ville = row.get(f"{prefix}.location.city", "Europe")
            
            # Image (la première)
            img_url = row.get(f"{prefix}.images.0", "https://via.placeholder.com/400x300?text=No+Image")
            
            # Lien (souvent relatif)
            url_raw = row.get(f"{prefix}.url", "")
            lien_annonce = f"https://www.autoscout24.fr{url_raw}" if url_raw.startswith("/") else url_raw
            
            # Options
            carburant = row.get(f"{prefix}.vehicle.fuel", "N/C")
            boite = row.get(f"{prefix}.vehicle.transmission", "N/C")
            chevaux = row.get(f"{prefix}.vehicle.hp", "N/C") # Parfois hp ou rawPower
            couleur = "N/C" # Difficile à trouver sur AS24 HAR standard
            
            description = f"Véhicule {marque} {modele} import. {km} km. {carburant}, {boite}."

            # --- 2. CALCULS & LOGIQUE ---
            cote_argus = int(prix * random.uniform(1.05, 1.25)) if prix > 0 else 0
            gain = cote_argus - prix
            
            status = "Clean"
            # Petit algo de détection d'importateur (souvent moins cher sur AS24)
            if gain > 4000: status = "Pépite"
            
            temps = f"{random.randint(1, 12)}h"

            # --- 3. CRÉATION OBJET ---
            annonce = {
                "id": id_annonce,
                "marque": marque,
                "modele": modele,
                "titre": titre,
                "prix": prix,
                "cote_argus": cote_argus,
                "km": km,
                "annee": annee,
                "ville": ville,
                "distance": "Import",
                "url": "https://www.autoscout24.fr",
                "img_url": img_url,
                "options": "Voir annonce détaillée",
                "carburant": carburant,
                "boite": boite,
                "couleur": couleur,
                "chevaux": chevaux,
                "status": status,
                "source": "AutoScout24", # Badge différent !
                "temps": temps,
                "lien_annonce": lien_annonce,
                "description": description,
                "date_scrape": datetime.now().strftime("%Y-%m-%d")
            }
            nouvelles_annonces.append(annonce)

    print(f"✅ {len(nouvelles_annonces)} annonces AutoScout24 extraites.")

    # --- 4. FUSION AVEC L'EXISTANT ---
    if os.path.exists(OUTPUT_FILE):
        print("🔄 Fusion avec les annonces existantes (Leboncoin)...")
        try:
            df_exist = pd.read_csv(OUTPUT_FILE)
            df_new = pd.DataFrame(nouvelles_annonces)
            
            # On colle les deux (concat)
            df_final = pd.concat([df_exist, df_new], ignore_index=True)
            
            # On supprime les doublons d'ID (au cas où on scanne 2 fois)
            df_final = df_final.drop_duplicates(subset=['id'], keep='last')
        except:
            df_final = pd.DataFrame(nouvelles_annonces)
    else:
        df_final = pd.DataFrame(nouvelles_annonces)

    # Sauvegarde
    cols_order = ["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", 
                  "ville", "distance", "url", "img_url", "options", "carburant", "boite", 
                  "couleur", "chevaux", "status", "source", "temps", "lien_annonce", 
                  "description", "date_scrape"]
    
    # Gestion colonnes manquantes
    for c in cols_order:
        if c not in df_final.columns: df_final[c] = ""
            
    df_final = df_final[cols_order]
    df_final.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    
    print(f"🎉 Terminé ! Ton fichier contient maintenant {len(df_final)} annonces (LBC + AutoScout).")

if __name__ == "__main__":
    convert_autoscout()