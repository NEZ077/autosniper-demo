import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- 1. BASE DE DONNÉES MASSIVE ---
DB_AUTO = {
    "Abarth": ["595", "695", "124 Spider"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "4C"],
    "Alpine": ["A110", "A110 GT", "A110 S"],
    "Aston Martin": ["Vantage", "DB11", "DBX"],
    "Audi": ["A1", "A3", "A4", "A5", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "RS3", "RS6", "e-tron"],
    "Bentley": ["Continental GT", "Bentayga"],
    "BMW": ["Série 1", "Série 3", "Série 4", "X1", "X3", "X5", "X6", "M2", "M3", "M4", "i4", "iX"],
    "Bugatti": ["Chiron", "Veyron"],
    "Citroen": ["C3", "C3 Aircross", "C4", "C5 Aircross", "Berlingo", "Ami"],
    "Cupra": ["Formentor", "Born", "Leon", "Ateca"],
    "Dacia": ["Sandero", "Duster", "Jogger", "Spring"],
    "DS": ["DS 3", "DS 4", "DS 7", "DS 9"],
    "Ferrari": ["488 Pista", "F8 Tributo", "Roma", "812 Superfast", "SF90"],
    "Fiat": ["500", "500e", "500X", "Panda", "Tipo"],
    "Ford": ["Fiesta", "Focus", "Puma", "Kuga", "Mustang", "Ranger"],
    "Honda": ["Civic", "HR-V", "CR-V"],
    "Hyundai": ["i20", "Tucson", "Santa Fe", "IONIQ 5"],
    "Jaguar": ["F-Type", "F-Pace", "I-Pace"],
    "Jeep": ["Renegade", "Compass", "Wrangler", "Avenger"],
    "Kia": ["Picanto", "Sportage", "EV6", "Niro"],
    "Lamborghini": ["Urus", "Huracan", "Aventador"],
    "Land Rover": ["Defender", "Range Rover", "Evoque", "Velar"],
    "Lexus": ["UX", "NX", "RX"],
    "Maserati": ["Ghibli", "Levante", "MC20", "Grecale"],
    "Mazda": ["MX-5", "CX-30", "CX-5"],
    "McLaren": ["720S", "570S", "Artura"],
    "Mercedes": ["Classe A", "Classe C", "Classe E", "CLA", "GLA", "GLC", "GLE", "Classe G", "AMG GT"],
    "Mini": ["Cooper", "Cooper S", "Clubman", "Countryman"],
    "Nissan": ["Juke", "Qashqai", "X-Trail", "GTR"],
    "Opel": ["Corsa", "Astra", "Mokka"],
    "Peugeot": ["208", "308", "408", "508", "2008", "3008", "5008", "Rifter"],
    "Porsche": ["911", "718 Cayman", "Macan", "Cayenne", "Taycan", "Panamera"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Espace", "Rafale", "Zoe", "Twingo"],
    "Rolls-Royce": ["Phantom", "Cullinan"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Arona"],
    "Skoda": ["Fabia", "Octavia", "Superb", "Kamiq", "Kodiaq", "Enyaq"],
    "Smart": ["Fortwo", "#1", "#3"],
    "Suzuki": ["Swift", "Ignis", "Vitara", "Jimny"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
    "Toyota": ["Yaris", "Corolla", "C-HR", "RAV4", "Land Cruiser", "Supra"],
    "Volkswagen": ["Polo", "Golf", "T-Roc", "Tiguan", "Passat", "Touareg", "ID.3", "ID.4"],
    "Volvo": ["XC40", "XC60", "XC90", "C40"]
}

# --- 2. IMAGES HD STABLES (Wikimedia Commons) ---
# Ces liens sont directs et ne cassent pas.
IMAGES_HD = {
    "Porsche": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Porsche_992_GT3_at_IAA_2021_1X7A0322.jpg/800px-Porsche_992_GT3_at_IAA_2021_1X7A0322.jpg",
    "Ferrari": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Ferrari_SF90_Stradale_IMG_5076.jpg/800px-Ferrari_SF90_Stradale_IMG_5076.jpg",
    "Lamborghini": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Lamborghini_Huracan_Evo_RWD_IMG_4418.jpg/800px-Lamborghini_Huracan_Evo_RWD_IMG_4418.jpg",
    "Audi": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Audi_RS6_Avant_C8.jpg/800px-Audi_RS6_Avant_C8.jpg",
    "BMW": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/BMW_M4_Competition_G82.jpg/800px-BMW_M4_Competition_G82.jpg",
    "Mercedes": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Mercedes-AMG_G_63_W463A_IMG_3756.jpg/800px-Mercedes-AMG_G_63_W463A_IMG_3756.jpg",
    "Tesla": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/2020_Tesla_Model_3_Performance_AWD_Front.jpg/800px-2020_Tesla_Model_3_Performance_AWD_Front.jpg",
    "Peugeot": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/ba/Peugeot_408_GT_IMG_5568.jpg/800px-Peugeot_408_GT_IMG_5568.jpg",
    "Renault": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Renault_Megane_RS_Trophy_R_IAA_2019_JM_04.jpg/800px-Renault_Megane_RS_Trophy_R_IAA_2019_JM_04.jpg",
    "Volkswagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/VW_Golf_8_R_IMG_4111.jpg/800px-VW_Golf_8_R_IMG_4111.jpg",
    "Fiat": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Fiat_500_Hybrid_IMG_3666.jpg/800px-Fiat_500_Hybrid_IMG_3666.jpg",
    "Alpine": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Alpine_A110_Premiere_Edition_2017_%2837330560274%29.jpg/800px-Alpine_A110_Premiere_Edition_2017_%2837330560274%29.jpg"
}

# --- PARAMETRES ---
CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique"]
BOITES = ["Automatique", "Manuelle", "Séquentielle"]
COULEURS = ["Noir", "Gris Nardo", "Blanc Glacier", "Bleu Nuit", "Rouge", "Vert Anglais", "Jaune", "Gris Argent"]
VILLES = ["Paris 16e", "Lyon", "Marseille", "Bordeaux", "Lille", "Monaco", "Genève", "Luxembourg", "Cannes", "Nice"]
OPTIONS_LIST = ["Toit Panoramique", "Cuir Nappa", "Caméra 360°", "CarPlay", "Son Burmester", "Sièges Ventilés", "Pack Carbone", "Matrix LED", "Affichage Tête Haute", "Suspension Pneumatique"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def get_image(marque):
    # 1. Si on a une image HD officielle, on la prend
    if marque in IMAGES_HD:
        return IMAGES_HD[marque]
    
    # 2. Sinon, on utilise LoremFlickr (générateur aléatoire mais réel)
    # On met un lock aléatoire pour avoir des voitures différentes à chaque ligne
    rand_id = random.randint(1, 9999)
    keyword = marque.lower().replace(" ", "")
    return f"https://loremflickr.com/640/480/{keyword},car?lock={rand_id}"

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix de base
    if marque in ["Ferrari", "Lamborghini", "Bugatti", "Rolls-Royce", "McLaren"]:
        prix_base = 250000
        chevaux = random.randint(500, 1000)
    elif marque in ["Porsche", "Aston Martin", "Bentley"]:
        prix_base = 110000
        chevaux = random.randint(350, 650)
    elif marque in ["Audi", "BMW", "Mercedes", "Land Rover", "Maserati"]:
        prix_base = 60000
        chevaux = random.randint(200, 500)
    else:
        prix_base = 25000
        chevaux = random.randint(90, 200)
    
    annee = random.randint(2017, 2024)
    km = random.randint(2000, 140000)
    
    age = 2025 - annee
    decote = (age * 0.08) + (km / 150000 * 0.15)
    cote = int(prix_base * (1 - decote))
    if cote < 5000: cote = 5000
    
    # Prix vendeur
    prix = int(cote * random.uniform(0.8, 1.15))
    
    distance = random.randint(5, 500)
    opts = " | ".join(random.sample(OPTIONS_LIST, k=random.randint(2, 4)))
    
    # IMAGE
    img_url = get_image(marque)
    
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
    print("🚀 Génération PHOTO RÉALISTE en cours...")
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for _ in range(500): writer.writerow(generer_voiture())
    print("✅ Terminé : 500 véhicules générés.")

if __name__ == "__main__":
    run_simulation()