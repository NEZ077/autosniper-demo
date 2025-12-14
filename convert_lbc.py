import pandas as pd
import random
from datetime import datetime
import os

INPUT_FILE = "compiled-results.csv"
OUTPUT_FILE = "annonces.csv"

def convert_lbc_csv():
    print(f"🔄 Lecture du fichier {INPUT_FILE}...")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Erreur : Le fichier {INPUT_FILE} est introuvable.")
        return

    try:
        df_raw = pd.read_csv(INPUT_FILE)
    except Exception as e:
        print(f"❌ Erreur de lecture CSV : {e}")
        return

    annonces = []
    
    print(f"⚙️ Traitement de {len(df_raw)} annonces...")

    # On parcourt chaque ligne du fichier brut
    for index, row in df_raw.iterrows():
        # --- 1. CHAMPS DE BASE ---
        titre = row.get("subject", "Sans titre")
        
        # Gestion Prix (parfois vide ou mal formaté)
        try:
            prix = int(row.get("price.0", 0))
        except:
            prix = 0
            
        lien_annonce = row.get("url", "")
        description = str(row.get("body", "Pas de description")).replace("\n", " <br> ") # Formatage pour HTML
        
        # --- 2. GESTION IMAGES ---
        # On cherche la plus grande image disponible
        img_url = "https://via.placeholder.com/400x300?text=Pas+de+Photo"
        if "images.urls_large.0" in row and pd.notna(row["images.urls_large.0"]):
             img_url = row["images.urls_large.0"]
        elif "images.urls.0" in row and pd.notna(row["images.urls.0"]):
             img_url = row["images.urls.0"]
        elif "images.thumb_url" in row and pd.notna(row["images.thumb_url"]):
             img_url = row["images.thumb_url"]

        # --- 3. EXTRACTION INTELLIGENTE DES ATTRIBUTS ---
        # Les infos (Km, Année, Carburant...) sont cachées dans des colonnes "attributes.X.key"
        # On crée un dictionnaire propre pour cette annonce
        attrs = {}
        for col in df_raw.columns:
            if col.startswith("attributes.") and col.endswith(".key"):
                # On récupère l'index (ex: 'attributes.5.key' -> '5')
                idx = col.split(".")[1]
                key_col = f"attributes.{idx}.key"
                val_col = f"attributes.{idx}.value_label" # La valeur lisible (ex: "Diesel")
                val_raw_col = f"attributes.{idx}.value"   # La valeur brute (au cas où)
                
                if key_col in row and pd.notna(row[key_col]):
                    key_name = row[key_col]
                    # On essaie de prendre le label, sinon la valeur brute
                    val = row.get(val_col)
                    if pd.isna(val):
                        val = row.get(val_raw_col)
                    attrs[key_name] = val
        
        # Mapping des attributs trouvés vers ton format App
        marque = attrs.get("brand", "Marque Inconnue")
        modele = attrs.get("model", "Modèle Inconnu")
        km = str(attrs.get("mileage", "0")).replace(" ", "")
        annee = str(attrs.get("regdate", "2020"))
        carburant = attrs.get("fuel", "N/C")
        boite = attrs.get("gearbox", "N/C")
        chevaux = attrs.get("horsepower", "N/C")
        couleur = attrs.get("color", "N/C")
        
        # --- 4. SIMULATION INTELLIGENTE ---
        # Calcul d'une fausse cote pour faire fonctionner tes badges "Pépite"
        # On simule que la voiture vaut 15% de plus que le prix affiché
        cote_argus = int(prix * random.uniform(1.05, 1.25)) if prix > 0 else 0
        gain = cote_argus - prix
        
        # Détermination du Status
        status = "Clean"
        if "accident" in str(titre).lower() or "choc" in str(titre).lower() or "panne" in str(titre).lower():
            status = "Accidentée"
        elif gain > 3000:
            status = "Pépite"
            
        # Temps aléatoire pour faire "Live"
        temps = f"{random.randint(1, 23)}h"
        
        # Création de la ligne finale
        annonce = {
            "id": f"lbc-{row.get('list_id', index)}",
            "marque": marque,
            "modele": modele,
            "titre": titre,
            "prix": prix,
            "cote_argus": cote_argus,
            "km": km,
            "annee": annee,
            "ville": row.get("location.city", "France"),
            "distance": "10",
            "url": "https://www.leboncoin.fr",
            "img_url": img_url,
            "options": "Voir description détaillée", 
            "carburant": carburant,
            "boite": boite,
            "couleur": couleur,
            "chevaux": chevaux,
            "status": status,
            "source": "LeBonCoin",
            "temps": temps,
            "lien_annonce": lien_annonce,
            "description": description[:600] + "..." if len(description) > 600 else description,
            "date_scrape": datetime.now().strftime("%Y-%m-%d")
        }
        annonces.append(annonce)
        
    # --- 5. SAUVEGARDE ---
    df_out = pd.DataFrame(annonces)
    
    # Ordre des colonnes strict pour ton app.py
    cols_order = ["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", 
                  "ville", "distance", "url", "img_url", "options", "carburant", "boite", 
                  "couleur", "chevaux", "status", "source", "temps", "lien_annonce", 
                  "description", "date_scrape"]
    
    # Ajout des colonnes manquantes si besoin
    for c in cols_order:
        if c not in df_out.columns: df_out[c] = ""
            
    df_out = df_out[cols_order]
    
    # Encodage utf-8-sig pour Excel
    df_out.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
    print(f"\n✅ SUCCÈS ! {len(df_out)} annonces converties dans '{OUTPUT_FILE}'.")
    print("👉 Tu peux maintenant lancer 'streamlit run app.py'")

if __name__ == "__main__":
    convert_lbc_csv()