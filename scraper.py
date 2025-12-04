import csv
import random
import time
from datetime import datetime, timedelta

# --- CONFIGURATION ---
CSV_FILE = "annonces.csv"

# Base de données de modèles réalistes
MARQUES = {
    "Audi": [("A1", 18000), ("A3 S-Line", 25000), ("Q3", 32000), ("RS6", 110000)],
    "BMW": [("Série 1", 20000), ("M2 Competition", 55000), ("X5", 60000), ("i4", 58000)],
    "Mercedes": [("Classe A", 22000), ("CLA", 29000), ("G63 AMG", 180000), ("GLC", 45000)],
    "Porsche": [("911 Carrera", 120000), ("Macan", 65000), ("Cayenne", 85000), ("Taycan", 95000)],
    "Renault": [("Clio V", 14000), ("Megane RS", 35000), ("Austral", 32000), ("Arkana", 28000)],
    "Tesla": [("Model 3", 38000), ("Model Y", 42000), ("Model S", 90000)]
}

VILLES = ["Paris", "Lyon", "Bordeaux", "Marseille", "Lille", "Strasbourg", "Nice", "Monaco"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "titre", "prix", "km", "annee", "ville", "url", "img_url", "date_scrape"])

def generer_voiture():
    marque = random.choice(list(MARQUES.keys()))
    modele_info = random.choice(MARQUES[marque])
    nom_modele = modele_info[0]
    prix_neuf_ref = modele_info[1]
    
    # Génération réaliste Age / KM
    annee = random.randint(2016, 2024)
    age = 2025 - annee
    km_par_an = random.randint(5000, 25000)
    km = age * km_par_an
    
    # Calcul du prix marché (Décote)
    decote = (age * 0.10) + ((km / 100000) * 0.15) # On perd de la valeur avec l'âge et les km
    if decote > 0.8: decote = 0.8 # Max 80% de décote
    
    prix_marche = int(prix_neuf_ref * (1 - decote))
    
    # Création d'opportunités (Le "Sniper" doit servir à quelque chose !)
    # 10% des voitures sont vendues 20% moins cher (Super Affaire)
    scenario = random.choices(["normal", "super_affaire", "trop_cher"], weights=[70, 10, 20])[0]
    
    prix_final = prix_marche
    if scenario == "super_affaire":
        prix_final = int(prix_marche * 0.8) # -20%
    elif scenario == "trop_cher":
        prix_final = int(prix_marche * 1.2) # +20%
        
    titre = f"{marque} {nom_modele}"
    
    # Image : On utilise un service qui donne des images de voitures aléatoires
    # Astuce : on ajoute un timestamp pour que chaque image soit différente
    rand_sig = random.randint(1, 1000)
    img_url = f"https://loremflickr.com/640/480/{marque.lower()},car?lock={rand_sig}"
    
    ad_id = f"sim-{random.randint(100000, 999999)}"
    
    return [
        ad_id,
        titre,
        str(prix_final),
        str(km),
        str(annee),
        random.choice(VILLES),
        "https://www.google.com", # Faux lien
        img_url,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

def run_simulation():
    print("[SIMULATION] Génération du marché parfait...")
    init_csv()
    
    nb_voitures = 80
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(nb_voitures):
            writer.writerow(generer_voiture())
            if i % 10 == 0:
                print(f"  -> {i} véhicules générés...")
                
    print(f"[SUCCÈS] {nb_voitures} annonces prêtes dans {CSV_FILE}.")

if __name__ == "__main__":
    run_simulation()