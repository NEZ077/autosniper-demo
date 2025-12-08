import csv
import random
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- 1. LA BASE DE DONNÉES COMPLÈTE (BR-PERFORMANCE) ---
# J'ai intégré ici les marques et modèles que tu voulais récupérer.
DB_AUTO = {
    "Abarth": ["500", "595", "695", "Punto Evo"],
    "Alfa Romeo": ["Giulia", "Stelvio", "4C", "Giulietta", "MiTo", "Tonale"],
    "Alpine": ["A110", "A110 S", "A110 GT"],
    "Aston Martin": ["Vantage", "DB11", "DBS Superleggera", "DBX", "Rapide"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "RS3", "RS4", "RS6"],
    "Bentley": ["Continental GT", "Bentayga", "Flying Spur"],
    "BMW": ["Série 1", "Série 2", "Série 3", "Série 4", "Série 5", "Série 7", "X1", "X3", "X5", "X6", "M2", "M3", "M4", "Z4"],
    "Bugatti": ["Chiron", "Veyron"],
    "Cadillac": ["Escalade", "CTS-V", "ATS-V"],
    "Caterham": ["Seven 165", "Seven 275", "Seven 485"],
    "Chevrolet": ["Camaro", "Corvette C7", "Corvette C8"],
    "Citroen": ["C3", "C4", "C5 Aircross", "Berlingo", "DS3 Racing"],
    "Cupra": ["Ateca", "Leon", "Formentor", "Born"],
    "Dacia": ["Duster", "Sandero", "Spring"],
    "Dodge": ["Challenger", "Charger", "Ram 1500"],
    "Ferrari": ["488 Pista", "F8 Tributo", "812 Superfast", "Roma", "SF90", "296 GTB"],
    "Fiat": ["500", "500X", "Tipo", "Panda", "124 Spider"],
    "Ford": ["Fiesta ST", "Focus RS", "Mustang", "Ranger", "Puma", "Kuga"],
    "Honda": ["Civic Type R", "NSX", "HR-V", "CR-V"],
    "Hyundai": ["i20 N", "i30 N", "Kona", "Tucson", "Santa Fe"],
    "Jaguar": ["F-Type", "F-Pace", "XE", "XF", "I-Pace"],
    "Jeep": ["Wrangler", "Renegade", "Compass", "Grand Cherokee"],
    "Kia": ["Stinger", "Sportage", "Ceed GT", "EV6"],
    "KTM": ["X-Bow"],
    "Lamborghini": ["Aventador", "Huracan", "Urus"],
    "Land Rover": ["Defender", "Range Rover", "Evoque", "Velar", "Sport"],
    "Lexus": ["LC 500", "RX", "NX", "UX", "RC F"],
    "Lotus": ["Elise", "Exige", "Evora", "Emira"],
    "Maserati": ["Ghibli", "Levante", "Quattroporte", "MC20", "GranTurismo"],
    "Mazda": ["MX-5", "3", "CX-5", "CX-30"],
    "McLaren": ["720S", "570S", "600LT", "GT", "Artura"],
    "Mercedes": ["A45 AMG", "C63 AMG", "E63 AMG", "G63 AMG", "AMG GT", "CLA", "GLA", "GLC"],
    "Mini": ["Cooper S", "JCW", "Clubman", "Countryman"],
    "Mitsubishi": ["Lancer Evo", "Outlander", "Eclipse Cross"],
    "Nissan": ["GT-R", "370Z", "Juke", "Qashqai", "X-Trail"],
    "Opel": ["Corsa OPC", "Astra", "Insignia", "Mokka"],
    "Pagani": ["Huayra", "Zonda"],
    "Peugeot": ["208 GTi", "308 GTi", "3008", "508 PSE", "2008"],
    "Porsche": ["911", "718 Cayman", "718 Boxster", "Panamera", "Macan", "Cayenne", "Taycan"],
    "Renault": ["Clio R.S.", "Megane R.S.", "Alpine A110", "Arkana", "Austral"],
    "Rolls-Royce": ["Wraith", "Ghost", "Phantom", "Cullinan"],
    "Seat": ["Ibiza Cupra", "Leon Cupra", "Ateca", "Arona"],
    "Skoda": ["Octavia RS", "Fabia", "Superb", "Kodiaq"],
    "Smart": ["Brabus", "Fortwo", "Forfour"],
    "Subaru": ["WRX STI", "BRZ", "Forester"],
    "Suzuki": ["Swift Sport", "Jimny", "Vitara"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
    "Toyota": ["Supra", "GR Yaris", "GT86", "RAV4", "C-HR"],
    "Volkswagen": ["Golf GTI", "Golf R", "Polo GTI", "Tiguan", "Arteon", "T-Roc R"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "V60"],
    "Wiesmann": ["GT MF4", "GT MF5"]
}

# --- IMAGES PAR MARQUE (Pour que ça s'affiche bien) ---
IMAGES_MARQUES = {
    "Abarth": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Abarth_500_Monza_1.jpg/800px-Abarth_500_Monza_1.jpg",
    "Alpine": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Alpine_A110_Premiere_Edition_2017_%2837330560274%29.jpg/800px-Alpine_A110_Premiere_Edition_2017_%2837330560274%29.jpg",
    "Audi": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Audi_RS6_Avant_C8.jpg/800px-Audi_RS6_Avant_C8.jpg",
    "BMW": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/BMW_M4_Competition_G82.jpg/800px-BMW_M4_Competition_G82.jpg",
    "Bugatti": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Bugatti_Chiron_%2836559710091%29.jpg/800px-Bugatti_Chiron_%2836559710091%29.jpg",
    "Ferrari": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Ferrari_SF90_Stradale_IMG_5076.jpg/800px-Ferrari_SF90_Stradale_IMG_5076.jpg",
    "Ford": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/2018_Ford_Mustang_GT_5.0_facelift.jpg/800px-2018_Ford_Mustang_GT_5.0_facelift.jpg",
    "Lamborghini": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Lamborghini_Huracan_Evo_RWD_IMG_4418.jpg/800px-Lamborghini_Huracan_Evo_RWD_IMG_4418.jpg",
    "Mercedes": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Mercedes-AMG_G_63_W463A_IMG_3756.jpg/800px-Mercedes-AMG_G_63_W463A_IMG_3756.jpg",
    "Porsche": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Porsche_911_GT3_RS_%28992%29_IMG_6488.jpg/800px-Porsche_911_GT3_RS_%28992%29_IMG_6488.jpg",
    "Renault": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Renault_Megane_RS_Trophy_R_IAA_2019_JM_04.jpg/800px-Renault_Megane_RS_Trophy_R_IAA_2019_JM_04.jpg",
    "Tesla": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/2020_Tesla_Model_3_Performance_AWD_Front.jpg/800px-2020_Tesla_Model_3_Performance_AWD_Front.jpg",
    "Volkswagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/VW_Golf_8_R_IMG_4111.jpg/800px-VW_Golf_8_R_IMG_4111.jpg"
}

# --- PARAMETRES ---
CARBURANTS = ["Essence", "Diesel", "Hybride", "Électrique"]
BOITES = ["Automatique", "Manuelle", "Séquentielle"]
COULEURS = ["Noir", "Gris", "Blanc", "Bleu", "Rouge", "Vert", "Jaune", "Orange", "Mat"]
VILLES = ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Monaco", "Genève", "Luxembourg", "Nice", "Toulouse"]
OPTIONS_LIST = ["Stage 1", "Stage 2", "Ligne Échappement", "Filtre à air Sport", "Reprog E85", "Turbo Hybride", "Châssis Sport", "Freins Céramique"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "date_scrape"])

def get_image_auto(marque):
    # Si on a l'image exacte de la marque, on la prend
    if marque in IMAGES_MARQUES:
        return IMAGES_MARQUES[marque]
    # Sinon, image générique de sport
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/VW_Golf_8_R_IMG_4111.jpg/800px-VW_Golf_8_R_IMG_4111.jpg"

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix de base selon le prestige
    if marque in ["Ferrari", "Lamborghini", "Bugatti", "Pagani", "McLaren", "Rolls-Royce"]:
        prix_base = 200000
        chevaux = random.randint(500, 1000)
    elif marque in ["Porsche", "Bentley", "Aston Martin", "Wiesmann"]:
        prix_base = 100000
        chevaux = random.randint(350, 600)
    elif marque in ["Audi", "BMW", "Mercedes", "Maserati", "Jaguar", "Land Rover"]:
        prix_base = 50000
        chevaux = random.randint(200, 500)
    else:
        prix_base = 25000
        chevaux = random.randint(150, 300)
    
    annee = random.randint(2015, 2024)
    km = random.randint(2000, 140000)
    
    # Calcul Cote
    age = 2025 - annee
    decote = (age * 0.08) + (km / 150000 * 0.15)
    cote = int(prix_base * (1 - decote))
    if cote < 5000: cote = 5000
    
    # Création d'opportunité
    variation = random.uniform(0.8, 1.2)
    prix = int(cote * variation)
    
    distance = random.randint(5, 500)
    opts = " | ".join(random.sample(OPTIONS_LIST, k=random.randint(2, 4)))
    img_url = get_image_auto(marque)
    
    return [
        f"ref-{random.randint(10000,99999)}",
        marque, modele, f"{marque} {modele}",
        str(prix), str(cote), str(km), str(annee),
        random.choice(VILLES), str(distance), 
        "https://www.br-performance.fr", # Lien vers le site source
        img_url, opts,
        random.choice(CARBURANTS), random.choice(BOITES), random.choice(COULEURS),
        str(chevaux),
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🚀 Génération de la base BR-Performance Complète...")
    init_csv()
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # On génère beaucoup de voitures pour avoir du choix dans les filtres
        for _ in range(600): writer.writerow(generer_voiture())
    print(f"✅ Terminé : 600 véhicules générés ({len(DB_AUTO)} marques).")

if __name__ == "__main__":
    run_simulation()