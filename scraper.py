import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- 1. LA BASE DE DONNÉES ULTIME (Type Leboncoin) ---
DB_AUTO = {
    # --- FRANÇAISES ---
    "Peugeot": ["208", "2008", "308", "3008", "5008", "408", "508", "Rifter", "Partner", "108", "RCZ"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Espace", "Rafale", "Zoe", "Twingo", "Kangoo", "Scenic", "Talisman", "Koleos"],
    "Citroen": ["C3", "C3 Aircross", "C4", "C4 X", "C5 Aircross", "C5 X", "Berlingo", "Ami", "C1", "Jumpy"],
    "Dacia": ["Sandero", "Duster", "Jogger", "Spring", "Logan", "Lodgy"],
    "DS": ["DS 3", "DS 4", "DS 7", "DS 9", "DS 5"],
    "Alpine": ["A110", "A290"],

    # --- ALLEMANDES ---
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q4", "Q5", "Q7", "Q8", "TT", "R8", "RS3", "RS6", "e-tron"],
    "BMW": ["Série 1", "Série 2", "Série 3", "Série 4", "Série 5", "Série 7", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "Z4", "i4", "iX"],
    "Mercedes": ["Classe A", "Classe B", "Classe C", "Classe E", "Classe S", "CLA", "GLA", "GLB", "GLC", "GLE", "Classe G", "AMG GT", "EQA", "Vito"],
    "Volkswagen": ["Polo", "Golf", "T-Roc", "Tiguan", "Passat", "Arteon", "Touareg", "ID.3", "ID.4", "ID. Buzz", "T-Cross", "Caddy"],
    "Porsche": ["911", "718 Cayman", "Boxster", "Macan", "Cayenne", "Panamera", "Taycan"],
    "Opel": ["Corsa", "Astra", "Mokka", "Crossland", "Grandland", "Insignia", "Zafira"],
    "Smart": ["Fortwo", "Forfour", "#1", "#3"],

    # --- ITALIENNES ---
    "Fiat": ["500", "500X", "Panda", "Tipo", "600", "Punto", "Doblo", "Spider 124"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "Giulietta", "MiTo"],
    "Ferrari": ["488", "F8 Tributo", "Roma", "Portofino", "812 Superfast", "296 GTB", "SF90", "458 Italia"],
    "Lamborghini": ["Urus", "Huracan", "Aventador"],
    "Maserati": ["Ghibli", "Levante", "Quattroporte", "Grecale", "GranTurismo"],
    "Abarth": ["500", "595", "695"],

    # --- ASIATIQUES ---
    "Toyota": ["Yaris", "Corolla", "C-HR", "RAV4", "Land Cruiser", "Highlander", "Supra", "Aygo X", "Prius", "Hilux"],
    "Nissan": ["Micra", "Juke", "Qashqai", "X-Trail", "GTR", "Leaf", "Navara", "370Z"],
    "Kia": ["Picanto", "Rio", "Ceed", "Sportage", "Sorento", "EV6", "Niro", "Stonic"],
    "Hyundai": ["i10", "i20", "i30", "Kona", "Tucson", "Santa Fe", "IONIQ 5"],
    "Suzuki": ["Swift", "Ignis", "Vitara", "Jimny", "S-Cross"],
    "Mazda": ["MX-5", "CX-30", "CX-5", "CX-60", "Mazda2", "Mazda3", "Mazda6"],
    "Honda": ["Civic", "HR-V", "CR-V", "Jazz"],
    "Lexus": ["UX", "NX", "RX", "ES", "LBX"],

    # --- ANGLAISES / AMÉRICAINES / AUTRES ---
    "Ford": ["Fiesta", "Focus", "Puma", "Kuga", "Mustang", "Ranger", "Bronco", "Mach-E"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X", "Cybertruck"],
    "Land Rover": ["Defender", "Range Rover", "Evoque", "Velar", "Sport"],
    "Mini": ["Cooper", "Clubman", "Countryman"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "V60", "C40"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Arona", "Tarraco"],
    "Skoda": ["Fabia", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq", "Enyaq"],
    "Cupra": ["Formentor", "Born", "Leon", "Ateca"],
    "Jaguar": ["F-Type", "F-Pace", "E-Pace", "XE", "XF"],
    "Jeep": ["Renegade", "Compass", "Wrangler", "Avenger"],
    
    # --- SANS PERMIS & RARES ---
    "Aixam": ["City", "Coupé", "Crossline"],
    "Ligier": ["JS50", "JS60"],
    "Microcar": ["M.Go", "Dué"],
    "Bentley": ["Continental GT", "Bentayga"],
    "Rolls-Royce": ["Phantom", "Cullinan"],
    "Lotus": ["Emira", "Elise"]
}

# --- IMAGES PAR DÉFAUT (Pour éviter les trous) ---
# Si une marque n'a pas d'image spécifique, on utilise une image générique de qualité
IMG_DEFAULT = "https://images.caradisiac.com/logos-ref/modele/modele--peugeot-208-2/S0-modele--peugeot-208-2.jpg"

IMAGES_MARQUES = {
    "Porsche": "https://images.caradisiac.com/logos-ref/modele/modele--porsche-911-type-992/S0-modele--porsche-911-type-992.jpg",
    "Ferrari": "https://sf2.auto-moto.com/wp-content/uploads/sites/9/2020/09/ferrari-roma-2020-01-750x410.jpg",
    "Lamborghini": "https://images.caradisiac.com/logos/modele/modele--lamborghini-urus/S7-modele--lamborghini-urus.jpg",
    "BMW": "https://www.largus.fr/images/images/bmw-m4-competition-2021-av-g-dyn_1.jpg",
    "Audi": "https://images.caradisiac.com/logos-ref/modele/modele--audi-rs3/S0-modele--audi-rs3.jpg",
    "Mercedes": "https://sf1.auto-moto.com/wp-content/uploads/sites/9/2021/08/mercedes-c63-s-amg-wagon-1-750x410.jpg",
    "Tesla": "https://images.caradisiac.com/logos-ref/modele/modele--tesla-model-3/S0-modele--tesla-model-3.jpg",
    "Peugeot": "https://images.caradisiac.com/logos-ref/modele/modele--peugeot-308-3/S0-modele--peugeot-308-3.jpg",
    "Renault": "https://images.caradisiac.com/logos-ref/modele/modele--renault-clio-5/S0-modele--renault-clio-5.jpg",
    "Dacia": "https://images.caradisiac.com/logos-ref/modele/modele--dacia-duster-2/S0-modele--dacia-duster-2.jpg",
    "Volkswagen": "https://images.caradisiac.com/logos-ref/modele/modele--volkswagen-golf-8/S0-modele--volkswagen-golf-8.jpg",
    "Fiat": "https://images.caradisiac.com/logos-ref/modele/modele--fiat-500-2/S0-modele--fiat-500-2.jpg",
    "Aixam": "https://www.aixam.com/ressources/images/gamme/emotion/city/sport/aixam-city-sport-blanc-nacré.jpg"
}

# --- PARAMETRES ---
CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique", "GPL"]
BOITES = ["Automatique", "Manuelle"]
COULEURS = ["Noir", "Gris", "Blanc", "Bleu", "Rouge", "Vert", "Jaune", "Orange", "Beige"]
VILLES = ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Nantes", "Strasbourg", "Montpellier", "Nice", "Toulouse"]
OPTIONS_LIST = ["Toit Ouvrant", "Cuir", "GPS", "CarPlay", "Caméra de recul", "Radars AV/AR", "Régulateur Adaptatif", "Sièges Chauffants", "Attelage", "Jantes Alu"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def get_image_auto(marque):
    # Retourne l'image de la marque si elle existe, sinon une image par défaut
    return IMAGES_MARQUES.get(marque, IMG_DEFAULT)

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix de base selon le standing
    if marque in ["Ferrari", "Lamborghini", "Porsche", "Bentley", "Rolls-Royce", "Maserati"]:
        prix_base = 120000
        chevaux = random.randint(350, 700)
    elif marque in ["Audi", "BMW", "Mercedes", "Land Rover", "Jaguar", "Tesla", "Volvo", "Lexus"]:
        prix_base = 45000
        chevaux = random.randint(150, 400)
    elif marque in ["Aixam", "Ligier", "Microcar"]: # Sans permis
        prix_base = 12000
        chevaux = random.randint(5, 15)
    else:
        prix_base = 22000
        chevaux = random.randint(90, 200)
    
    annee = random.randint(2014, 2024)
    km = random.randint(5000, 160000)
    
    # Calcul Cote
    age = 2025 - annee
    decote = (age * 0.08) + (km / 150000 * 0.15)
    cote = int(prix_base * (1 - decote))
    if cote < 3000: cote = 3000
    
    # Prix Vendeur (Opportunité ou pas)
    variation = random.uniform(0.8, 1.2)
    prix = int(cote * variation)
    
    distance = random.randint(1, 500)
    opts = " | ".join(random.sample(OPTIONS_LIST, k=random.randint(2, 5)))
    img_url = get_image_auto(marque)
    
    return [
        f"LBC-{random.randint(100000,999999)}",
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
    print("🚀 Génération DATABASE LEBONCOIN COMPLETE...")
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # On génère 800 voitures pour avoir une densité énorme dans les filtres
        for _ in range(800): writer.writerow(generer_voiture())
    print(f"✅ Terminé : 800 annonces générées couvrant {len(DB_AUTO)} marques.")

if __name__ == "__main__":
    run_simulation()