import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- 1. BASE DE DONNÉES MASSIVE (GOD MODE) ---
DB_AUTO = {
    "Abarth": ["595", "695", "124 Spider", "500e"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "4C", "Giulietta", "MiTo"],
    "Alpine": ["A110", "A110 GT", "A110 S", "A110 R", "A290"],
    "Aston Martin": ["Vantage", "DB11", "DB12", "DBS", "DBX", "Valhalla"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "RS3", "RS6", "e-tron"],
    "Bentley": ["Continental GT", "Bentayga", "Flying Spur"],
    "BMW": ["Série 1", "Série 3", "Série 4", "Série 5", "X1", "X3", "X5", "X6", "M2", "M3", "M4", "i4", "iX"],
    "Bugatti": ["Chiron", "Veyron", "Mistral"],
    "Citroen": ["C3", "C3 Aircross", "C4", "C5 Aircross", "C5 X", "Berlingo", "Ami"],
    "Cupra": ["Formentor", "Born", "Leon", "Ateca"],
    "Dacia": ["Sandero", "Duster", "Jogger", "Spring"],
    "DS": ["DS 3", "DS 4", "DS 7", "DS 9"],
    "Ferrari": ["488 Pista", "F8 Tributo", "Roma", "812 Superfast", "296 GTB", "SF90"],
    "Fiat": ["500", "500e", "500X", "Panda", "Tipo"],
    "Ford": ["Fiesta", "Focus", "Puma", "Kuga", "Mustang", "Ranger", "Bronco"],
    "Honda": ["Civic", "HR-V", "CR-V", "Jazz", "NSX"],
    "Hyundai": ["i20", "i30", "Kona", "Tucson", "Santa Fe", "IONIQ 5"],
    "Jaguar": ["F-Type", "F-Pace", "E-Pace", "I-Pace"],
    "Jeep": ["Renegade", "Compass", "Wrangler", "Grand Cherokee", "Avenger"],
    "Kia": ["Picanto", "Rio", "Ceed", "Sportage", "Sorento", "EV6", "Niro"],
    "Lamborghini": ["Urus", "Huracan", "Aventador", "Revuelto"],
    "Land Rover": ["Defender", "Range Rover", "Range Rover Sport", "Evoque", "Velar"],
    "Lexus": ["UX", "NX", "RX", "ES", "LC"],
    "Lotus": ["Emira", "Evija", "Eletre"],
    "Maserati": ["Ghibli", "Levante", "Quattroporte", "MC20", "Grecale"],
    "Mazda": ["MX-5", "CX-30", "CX-5", "CX-60", "Mazda3"],
    "McLaren": ["720S", "570S", "Artura", "GT"],
    "Mercedes": ["Classe A", "Classe C", "Classe E", "CLA", "GLA", "GLC", "GLE", "Classe G", "AMG GT", "SL"],
    "Mini": ["Cooper", "Cooper S", "Clubman", "Countryman"],
    "Nissan": ["Micra", "Juke", "Qashqai", "X-Trail", "GTR", "Ariya"],
    "Opel": ["Corsa", "Astra", "Mokka", "Grandland"],
    "Peugeot": ["208", "308", "408", "508", "2008", "3008", "5008", "Rifter"],
    "Porsche": ["911", "718 Cayman", "Boxster", "Panamera", "Macan", "Cayenne", "Taycan"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Espace", "Rafale", "Zoe", "Twingo"],
    "Rolls-Royce": ["Phantom", "Ghost", "Cullinan", "Spectre"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Arona"],
    "Skoda": ["Fabia", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq", "Enyaq"],
    "Smart": ["Fortwo", "Forfour", "#1", "#3"],
    "Suzuki": ["Swift", "Ignis", "Vitara", "Jimny", "S-Cross"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X", "Cybertruck"],
    "Toyota": ["Yaris", "Corolla", "C-HR", "RAV4", "Land Cruiser", "Supra", "Aygo X"],
    "Volkswagen": ["Polo", "Golf", "T-Roc", "Tiguan", "Passat", "Arteon", "Touareg", "ID.3", "ID.4", "ID. Buzz"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "V60", "C40"]
}

# --- PARAMETRES ---
CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique"]
BOITES = ["Automatique", "Manuelle", "Séquentielle"]
COULEURS = ["Noir", "Gris Nardo", "Blanc", "Bleu Nuit", "Rouge", "Vert Anglais", "Jaune", "Orange", "Mat"]
VILLES = ["Paris 16e", "Lyon", "Marseille", "Bordeaux", "Lille", "Monaco", "Genève", "Luxembourg", "Nice", "Toulouse", "Cannes"]
OPTIONS_LIST = ["Toit Panoramique", "Cuir Nappa", "Caméra 360°", "CarPlay", "Son Burmester", "Sièges Ventilés", "Pack Carbone", "Matrix LED", "Affichage Tête Haute", "Suspension Pneumatique", "Pack Nuit", "Jantes 21 pouces"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix & Puissance
    prix_base = 30000
    chevaux = random.randint(110, 200)
    
    # Ajustement Luxe
    if marque in ["Ferrari", "Lamborghini", "Bugatti", "Rolls-Royce", "McLaren"]:
        prix_base = 250000
        chevaux = random.randint(500, 1000)
    elif marque in ["Porsche", "Aston Martin", "Bentley"]:
        prix_base = 110000
        chevaux = random.randint(350, 650)
    elif marque in ["Audi", "BMW", "Mercedes", "Maserati", "Jaguar", "Land Rover"]:
        prix_base = 55000
        chevaux = random.randint(180, 500)
    elif marque in ["Dacia", "Fiat", "Suzuki", "Smart"]:
        prix_base = 18000
        chevaux = random.randint(70, 130)
    
    annee = random.randint(2016, 2024)
    km = random.randint(1000, 160000)
    
    # Calcul Cote
    age = 2025 - annee
    decote = (age * 0.08) + (km / 150000 * 0.15)
    cote = int(prix_base * (1 - decote))
    if cote < 5000: cote = 5000
    
    # Prix vendeur (Création d'opportunité)
    variation = random.uniform(0.75, 1.2) # De -25% à +20%
    prix = int(cote * variation)
    
    distance = random.randint(5, 500)
    opts = " | ".join(random.sample(OPTIONS_LIST, k=random.randint(3, 5)))
    
    # --- LA CORRECTION IMAGE ---
    # On utilise LoremFlickr qui génère une image à la volée. C'est INCREVABLE.
    # On ajoute ?lock=random pour que chaque voiture ait une photo différente.
    rand_id = random.randint(1, 99999)
    # On essaie de cibler la marque dans l'URL
    keyword = marque.lower().replace(" ", "")
    img_url = f"https://loremflickr.com/640/480/{keyword},car?lock={rand_id}"
    
    # Pour les marques très luxe, on force un mot clé "supercar" pour avoir de belles photos
    if marque in ["Ferrari", "Lamborghini", "Bugatti", "McLaren"]:
        img_url = f"https://loremflickr.com/640/480/supercar,luxury?lock={rand_id}"
    
    return [
        f"ref-{random.randint(10000,99999)}",
        marque, modele, f"{marque} {modele}",
        str(prix), str(cote), str(km), str(annee),
        random.choice(VILLES), str(distance), 
        "https://www.leboncoin.fr", 
        img_url, opts,
        random.choice(CARBURANTS), random.choice(BOITES), random.choice(COULEURS),
        str(chevaux),
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🚀 Génération DATABASE MONDIALE (Images Garanties)...")
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # On génère 600 voitures
        for _ in range(600): writer.writerow(generer_voiture())
    print("✅ Terminé : 600 véhicules prêts.")

if __name__ == "__main__":
    run_simulation()