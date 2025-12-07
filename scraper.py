import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- 1. LES LISTES DE DONNÉES (C'est ça qui manquait !) ---
CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique"]
BOITES = ["Automatique", "Manuelle"]
VILLES = ["Paris", "Lyon", "Bordeaux", "Marseille", "Lille", "Monaco", "Genève", "Luxembourg"]
OPTIONS_LIST = ["Toit Panoramique", "Sièges Cuir", "Caméra 360", "Apple CarPlay", "Son Burmester", "Sièges Chauffants", "Pack Nuit", "Matrix LED", "Affichage Tête Haute"]

DB_AUTO = {
    "Audi": ["A1", "A3", "A4", "A5", "Q2", "Q3", "Q5", "Q7", "Q8", "RS3", "RS6", "e-tron"],
    "BMW": ["Série 1", "Série 3", "Série 4", "M2", "M3", "M4", "X1", "X3", "X5", "X6", "iX"],
    "Mercedes": ["Classe A", "Classe C", "CLA", "GLA", "GLC", "GLE", "Classe G", "AMG GT", "EQA"],
    "Porsche": ["911", "718 Cayman", "Macan", "Cayenne", "Panamera", "Taycan"],
    "Volkswagen": ["Golf 8", "Polo", "Tiguan", "T-Roc", "Arteon", "Touareg", "ID.4"],
    "Peugeot": ["208", "308", "2008", "3008", "5008", "408", "508"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Rafale"],
    "Land Rover": ["Defender", "Range Rover", "Evoque", "Velar"],
    "Ferrari": ["F8 Tributo", "Roma", "296 GTB"],
    "Lamborghini": ["Urus", "Huracan"]
}

def init_csv():
    """Crée le fichier avec les nouvelles colonnes Carburant et Boite"""
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "finition", "titre", "prix", "cote_argus", "km", "annee", "ville", "url", "img_url", "options", "carburant", "boite", "date_scrape"])

def generer_voiture():
    """Génère une fausse voiture réaliste"""
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix de base selon la marque
    prix_base = 25000
    if marque in ["Porsche", "Ferrari", "Lamborghini"]: prix_base = 120000
    elif marque in ["Audi", "BMW", "Mercedes", "Land Rover"]: prix_base = 45000
    elif marque in ["Peugeot", "Renault", "Volkswagen"]: prix_base = 20000
    
    annee = random.randint(2017, 2024)
    km = random.randint(1000, 160000)
    
    # Calcul Cote
    age = 2025 - annee
    decote = (age * 0.09) + (km / 150000 * 0.20)
    cote = int(prix_base * (1 - decote))
    
    # Prix Vente
    prix = int(cote * random.uniform(0.8, 1.2))
    if prix < 5000: prix = 5000
    
    # Options (3 au hasard)
    opts = " | ".join(random.sample(OPTIONS_LIST, k=random.randint(2, 4)))
    
    # Image
    rand = random.randint(1, 9999)
    # Astuce : on colle la marque pour avoir une image cohérente
    keyword = marque.lower().replace(" ", "")
    img_url = f"https://loremflickr.com/600/400/{keyword},car?lock={rand}"
    
    # ID unique
    ad_id = f"ref-{random.randint(10000,99999)}"

    return [
        ad_id,
        marque,
        modele,
        "Finition Luxe", # Finition générique pour simplifier
        f"{marque} {modele}",
        str(prix),
        str(cote),
        str(km),
        str(annee),
        random.choice(VILLES),
        "https://google.com",
        img_url,
        opts,
        random.choice(CARBURANTS), # Utilisation de la liste corrigée
        random.choice(BOITES),     # Utilisation de la liste corrigée
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🚀 Génération Données V4 (Complètes)...")
    init_csv()
    
    # On génère 300 voitures
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for _ in range(300):
            writer.writerow(generer_voiture())
            
    print("✅ Terminé. Fichier annonces.csv prêt.")

if __name__ == "__main__":
    run_simulation()