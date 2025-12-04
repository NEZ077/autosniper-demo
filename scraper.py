import csv
import random
import time
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- BASE DE DONNÉES INTELLIGENTE ---
# Structure : "Modele": (Prix_Neuf_Moyen, [Liste_Finitions])
DB_AUDI = {
    "A1": (24000, ["Business", "S-Line", "Design", "Attraction"]),
    "A3": (32000, ["S-Line", "Design Luxe", "Business Line", "Sportback"]),
    "Q3": (42000, ["S-Line", "Avus", "Midnight", "Advanced"]),
    "RS6": (140000, ["Performance", "Avant", "GT"])
}
DB_BMW = {
    "Série 1": (30000, ["M Sport", "Lounge", "Business Design"]),
    "M2": (75000, ["Competition", "CS", "Pack M"]),
    "X5": (85000, ["xLine", "M Sport", "Lounge Plus"])
}
DB_MERCEDES = {
    "Classe A": (35000, ["AMG Line", "Progressive", "Style"]),
    "CLA": (40000, ["AMG Line", "Shooting Brake", "Business"]),
    "G63": (190000, ["AMG", "Brabus", "Manufaktur"])
}
DB_PORSCHE = {
    "911": (130000, ["Carrera S", "Turbo S", "GT3", "Targa"]),
    "Macan": (70000, ["S", "GTS", "Turbo"]),
    "Cayenne": (90000, ["E-Hybrid", "Coupe", "Platinum"])
}
DB_RENAULT = {
    "Clio V": (21000, ["Intens", "RS Line", "Zen", "Initiale Paris"]),
    "Austral": (38000, ["Esprit Alpine", "Techno", "Iconic"]),
    "Megane": (28000, ["RS", "GT Line", "Business"])
}

# Fusion des bases
FULL_DB = {**DB_AUDI, **DB_BMW, **DB_MERCEDES, **DB_PORSCHE, **DB_RENAULT}
MARQUES_MAP = {} # Pour retrouver la marque depuis le modèle
for m, v in {"Audi": DB_AUDI, "BMW": DB_BMW, "Mercedes": DB_MERCEDES, "Porsche": DB_PORSCHE, "Renault": DB_RENAULT}.items():
    for mod in v.keys(): MARQUES_MAP[mod] = m

VILLES = ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Nantes", "Strasbourg", "Nice", "Monaco"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # On ajoute les colonnes 'finition' et 'cote_argus'
        writer.writerow(["id", "marque", "modele", "finition", "titre", "prix", "cote_argus", "km", "annee", "ville", "url", "img_url", "date_scrape"])

def calculer_cote(prix_neuf, annee, km, finition):
    # 1. Décote Annuelle (Moyenne 12% par an)
    age = 2025 - annee
    decote_temps = 1 - (0.12 * age)
    if decote_temps < 0.2: decote_temps = 0.2 # Plancher à 20%
    
    valeur_temps = prix_neuf * decote_temps
    
    # 2. Décote KM (Standard : 15 000km/an)
    km_theorique = age * 15000
    diff_km = km - km_theorique
    # Si plus de km que prévu, on perd 0.05€ par km
    ajustement_km = diff_km * 0.05
    
    cote = valeur_temps - ajustement_km
    
    # 3. Bonus Finition
    if any(x in finition for x in ["S-Line", "AMG", "M Sport", "RS", "GT3", "Turbo"]):
        cote *= 1.15 # +15% pour les finitions sport
    elif "Business" in finition or "Zen" in finition:
        cote *= 0.95 # -5% pour les finitions entrée de gamme
        
    return int(cote)

def generer_voiture():
    modele = random.choice(list(FULL_DB.keys()))
    marque = MARQUES_MAP[modele]
    infos = FULL_DB[modele]
    prix_neuf = infos[0]
    finition = random.choice(infos[1])
    
    annee = random.randint(2017, 2024)
    km = random.randint(5000, 160000)
    
    # --- CALCUL DE LA VRAIE COTE ARGUS ---
    cote_officielle = calculer_cote(prix_neuf, annee, km, finition)
    
    # --- DÉTERMINATION DU PRIX DE VENTE (Simule la réalité) ---
    # Parfois le vendeur est gourmand (+20%), parfois pressé (-20%)
    facteur_marche = random.uniform(0.75, 1.25) 
    prix_vente = int(cote_officielle * facteur_marche)
    
    if prix_vente < 5000: prix_vente = 5000 # Sécurité
    
    titre = f"{marque} {modele} {finition}"
    
    # Image
    rand = random.randint(1,9999)
    img_url = f"https://loremflickr.com/600/400/{marque.lower()},car?lock={rand}"
    
    ad_id = f"an-{random.randint(100000, 999999)}"

    return [
        ad_id,
        marque,
        modele,
        finition,
        titre,
        str(prix_vente),
        str(cote_officielle), # On sauvegarde la cote pour l'app
        str(km),
        str(annee),
        random.choice(VILLES),
        "https://www.google.com",
        img_url,
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🧮 Calcul des cotes Argus et génération des annonces...")
    init_csv()
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(150): # 150 voitures
            writer.writerow(generer_voiture())
            
    print("✅ Base de données générée avec Cotes Officielles.")

if __name__ == "__main__":
    run_simulation()