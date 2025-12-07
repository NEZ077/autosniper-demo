import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- LISTES ÉTENDUES ---
CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique"]
BOITES = ["Automatique", "Manuelle"]
COULEURS = ["Noir", "Gris", "Blanc", "Bleu Nuit", "Rouge", "Vert Anglais", "Jaune", "Argent"]
VILLES = ["Paris", "Lyon", "Bordeaux", "Marseille", "Lille", "Monaco", "Genève", "Luxembourg"]

# Base de données (Marques/Modèles)
DB_AUTO = {
    "Audi": ["A1", "A3", "A4", "A5", "Q2", "Q3", "Q5", "Q7", "Q8", "RS3", "RS6"],
    "BMW": ["Série 1", "Série 3", "Série 4", "M2", "M3", "M4", "X1", "X3", "X5", "X6"],
    "Mercedes": ["Classe A", "Classe C", "CLA", "GLA", "GLC", "GLE", "Classe G", "AMG GT"],
    "Porsche": ["911", "718 Cayman", "Macan", "Cayenne", "Panamera", "Taycan"],
    "Volkswagen": ["Golf 8", "Polo", "Tiguan", "T-Roc", "Arteon", "Touareg"],
    "Peugeot": ["208", "308", "2008", "3008", "5008", "408", "508"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Rafale"],
    "Ferrari": ["F8 Tributo", "Roma", "296 GTB"],
    "Lamborghini": ["Urus", "Huracan"]
}

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Ajout colonnes : couleur, chevaux, distance
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix & Puissance (Logique simplifiée)
    prix_base = 25000
    chevaux = random.randint(110, 200) # Base
    
    if marque in ["Porsche", "Ferrari", "Lamborghini"]: 
        prix_base = 120000
        chevaux = random.randint(350, 700)
    elif marque in ["Audi", "BMW", "Mercedes"]: 
        prix_base = 45000
        chevaux = random.randint(150, 400)
    
    annee = random.randint(2016, 2024)
    km = random.randint(1000, 160000)
    
    # Calcul Cote
    age = 2025 - annee
    decote = (age * 0.09) + (km / 150000 * 0.20)
    cote = int(prix_base * (1 - decote))
    prix = int(cote * random.uniform(0.8, 1.2)) # Prix vendeur
    if prix < 5000: prix = 5000
    
    # Simulation Distance (Rayon)
    # On simule que la voiture est à X km de l'utilisateur
    distance = random.randint(5, 500) 
    
    # Options
    opts_list = ["Toit Pano", "Cuir", "Caméra 360", "CarPlay", "Son Burmester", "Sièges Chauffants", "Pack Nuit", "Matrix LED"]
    opts = " | ".join(random.sample(opts_list, k=random.randint(2, 4)))
    
    # Image
    rand = random.randint(1, 9999)
    keyword = marque.lower().replace(" ", "")
    img_url = f"https://loremflickr.com/600/400/{keyword},car?lock={rand}"
    
    return [
        f"ref-{random.randint(10000,99999)}",
        marque, modele, f"{marque} {modele}",
        str(prix), str(cote), str(km), str(annee),
        random.choice(VILLES),
        str(distance), # La nouvelle colonne distance
        "https://google.com",
        img_url,
        opts,
        random.choice(CARBURANTS),
        random.choice(BOITES),
        random.choice(COULEURS), # Nouvelle colonne couleur
        str(chevaux),            # Nouvelle colonne chevaux
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🚀 Génération Données V5 (Mobile Ready)...")
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for _ in range(300): writer.writerow(generer_voiture())
    print("✅ Base de données mise à jour.")

if __name__ == "__main__":
    run_simulation()