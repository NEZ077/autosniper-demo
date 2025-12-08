import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

VILLES = ["Paris", "Lyon", "Bordeaux", "Monaco", "Genève", "Luxembourg"]

# Liens Wikimedia STABLES (ne changeront pas)
LUXURY_IMAGES = [
    "https://upload.wikimedia.org/wikipedia/commons/3/31/2018_Audi_RS3_Saloon_TFSI_Quattro_S-A_2.5_Front.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/66/Ferrari_Roma_1.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/f/f4/BMW_M3_G80_IMG_4020.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/0/0c/Porsche_911_992_Carrera_4S_Geneva_2019_1Y7A5401.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/29/2018_Mercedes-AMG_GT_C_Roadster_%281%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/9/91/Lamborghini_Urus_Performante_IAA_2023_1M7A0168.jpg"
]

DB_AUTO = {
    "Audi": ["RS3", "RS6"],
    "BMW": ["M3", "M4"],
    "Mercedes": ["AMG GT", "G63"],
    "Porsche": ["911", "Macan"],
    "Ferrari": ["Roma", "F8"],
    "Lamborghini": ["Urus"]
}

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # PRIX AJUSTÉS pour apparaître dans tes filtres (entre 30k et 80k pour la démo)
    prix_base = random.randint(35000, 75000)
    
    annee = random.randint(2019, 2024)
    km = random.randint(15000, 80000)
    
    # Cote toujours supérieure au prix pour l'effet "Bonne Affaire"
    cote = int(prix_base * 1.2) 
    
    return [
        f"ref-{random.randint(1000,9999)}",
        marque, modele, f"{marque} {modele} Competition",
        prix_base, cote, km, annee,
        random.choice(VILLES),
        random.randint(10, 200),
        "https://www.google.com",
        random.choice(LUXURY_IMAGES), # Image fiable
        "Toit Pano | Cuir | Sport Chrono",
        "Essence", "Automatique", "Noir",
        random.randint(300, 600),
        datetime.now().strftime("%Y-%m-%d")
    ]

if __name__ == "__main__":
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for _ in range(50): writer.writerow(generer_voiture())
    print("✅ Données réparées et Images stabilisées.")