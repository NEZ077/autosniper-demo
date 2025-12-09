import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- CONFIGURATION ---
DB_AUTO = {
    "Abarth": ["595", "695", "124 Spider"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale"],
    "Alpine": ["A110", "A110 GT", "A110 S"],
    "Aston Martin": ["Vantage", "DB11", "DBX"],
    "Audi": ["A1", "A3", "A4", "A5", "Q3", "Q5", "Q7", "Q8", "RS3", "RS6", "e-tron"],
    "Bentley": ["Continental GT", "Bentayga"],
    "BMW": ["Série 1", "Série 3", "Série 4", "X1", "X3", "X5", "X6", "M2", "M3", "M4"],
    "Bugatti": ["Chiron", "Veyron"],
    "Citroen": ["C3", "C4", "C5 Aircross", "Berlingo"],
    "Cupra": ["Formentor", "Born", "Leon"],
    "Dacia": ["Sandero", "Duster", "Jogger", "Spring"],
    "DS": ["DS 3", "DS 4", "DS 7"],
    "Ferrari": ["F8 Tributo", "Roma", "SF90"],
    "Fiat": ["500", "500e", "Panda"],
    "Ford": ["Fiesta", "Puma", "Kuga", "Mustang", "Ranger"],
    "Honda": ["Civic", "HR-V", "CR-V"],
    "Hyundai": ["Tucson", "Santa Fe", "IONIQ 5"],
    "Jaguar": ["F-Type", "F-Pace"],
    "Jeep": ["Renegade", "Compass", "Wrangler"],
    "Kia": ["Sportage", "EV6", "Niro"],
    "Lamborghini": ["Urus", "Huracan"],
    "Land Rover": ["Defender", "Range Rover", "Evoque", "Velar"],
    "Lexus": ["NX", "RX", "UX"],
    "Maserati": ["Ghibli", "Levante", "MC20"],
    "Mazda": ["MX-5", "CX-30", "CX-5"],
    "McLaren": ["720S", "Artura", "GT"],
    "Mercedes": ["Classe A", "Classe C", "CLA", "GLA", "GLC", "GLE", "G63", "AMG GT"],
    "Mini": ["Cooper", "Countryman"],
    "Nissan": ["Qashqai", "Juke", "GTR"],
    "Opel": ["Corsa", "Mokka"],
    "Peugeot": ["208", "308", "2008", "3008", "5008", "408"],
    "Porsche": ["911", "718 Cayman", "Macan", "Cayenne", "Taycan", "Panamera"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Espace"],
    "Rolls-Royce": ["Phantom", "Cullinan"],
    "Seat": ["Ibiza", "Leon", "Ateca"],
    "Skoda": ["Fabia", "Octavia", "Kodiaq"],
    "Smart": ["Fortwo", "#1"],
    "Suzuki": ["Swift", "Jimny"],
    "Tesla": ["Model 3", "Model Y", "Model S"],
    "Toyota": ["Yaris", "Corolla", "RAV4", "C-HR"],
    "Volkswagen": ["Polo", "Golf", "Tiguan", "T-Roc", "ID.3"],
    "Volvo": ["XC40", "XC60", "XC90"]
}

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

CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique"]
BOITES = ["Automatique", "Manuelle"]
COULEURS = ["Noir", "Gris", "Blanc", "Bleu", "Rouge", "Vert", "Jaune"]
VILLES = ["Paris", "Lyon", "Bordeaux", "Marseille", "Lille", "Monaco", "Genève", "Nice"]
OPTIONS_LIST = ["Toit Pano", "Cuir", "Caméra 360", "CarPlay", "Son Burmester", "Sièges Sport", "Matrix LED"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # VOICI LA LIGNE IMPORTANTE QUI AJOUTE 'CHEVAUX'
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def get_image(marque):
    if marque in IMAGES_HD:
        return IMAGES_HD[marque]
    rand_id = random.randint(1, 9999)
    keyword = marque.lower().replace(" ", "")
    return f"https://loremflickr.com/640/480/{keyword},car?lock={rand_id}"

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    prix_base = 30000
    chevaux = random.randint(110, 200) # Base puissance
    
    if marque in ["Ferrari", "Lamborghini", "Bugatti", "Rolls-Royce", "McLaren"]:
        prix_base = 250000
        chevaux = random.randint(500, 1000)
    elif marque in ["Porsche", "Aston Martin", "Bentley"]:
        prix_base = 110000
        chevaux = random.randint(350, 650)
    elif marque in ["Audi", "BMW", "Mercedes", "Land Rover"]:
        prix_base = 55000
        chevaux = random.randint(180, 500)
    
    annee = random.randint(2017, 2024)
    km = random.randint(1000, 150000)
    
    age = 2025 - annee
    decote = (age * 0.08) + (km / 150000 * 0.15)
    cote = int(prix_base * (1 - decote))
    if cote < 5000: cote = 5000
    
    prix = int(cote * random.uniform(0.8, 1.15))
    distance = random.randint(5, 500)
    opts = " | ".join(random.sample(OPTIONS_LIST, k=random.randint(2, 4)))
    img_url = get_image(marque)
    
    return [
        f"ref-{random.randint(10000,99999)}",
        marque, modele, f"{marque} {modele}",
        str(prix), str(cote), str(km), str(annee),
        random.choice(VILLES), str(distance), 
        "https://www.leboncoin.fr", 
        img_url, opts,
        random.choice(CARBURANTS), random.choice(BOITES), random.choice(COULEURS),
        str(chevaux), # ICI ON ÉCRIT LES CHEVAUX DANS LE FICHIER
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🚀 RÉPARATION DES DONNÉES EN COURS...")
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for _ in range(500): writer.writerow(generer_voiture())
    print("✅ Terminé : Fichier annonces.csv réparé.")

if __name__ == "__main__":
    run_simulation()