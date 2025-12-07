import csv
import random
import time
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- BASE DE DONNÉES GÉANTE (50 Marques) ---
DB_AUTO = {
    "Abarth": ["500", "595", "695", "124 Spider"],
    "Alfa Romeo": ["Giulia", "Stelvio", "Tonale", "4C", "Giulietta"],
    "Alpine": ["A110", "A110 S", "A110 GT"],
    "Aston Martin": ["DB11", "Vantage", "DBS", "DBX"],
    "Audi": ["A1", "A3", "A4", "A5", "A6", "A7", "A8", "Q2", "Q3", "Q5", "Q7", "Q8", "TT", "R8", "e-tron GT", "RS3", "RS6"],
    "Bentley": ["Continental GT", "Bentayga", "Flying Spur"],
    "BMW": ["Série 1", "Série 2", "Série 3", "Série 4", "Série 5", "Série 7", "X1", "X3", "X5", "X6", "X7", "Z4", "M2", "M3", "M4", "i4", "iX"],
    "Bugatti": ["Chiron", "Veyron"],
    "Citroen": ["C3", "C3 Aircross", "C4", "C5 X", "Berlingo", "Ami"],
    "Cupra": ["Formentor", "Born", "Leon", "Ateca"],
    "Dacia": ["Sandero", "Duster", "Jogger", "Spring"],
    "DS": ["DS 3", "DS 4", "DS 7", "DS 9"],
    "Ferrari": ["488 Pista", "F8 Tributo", "Roma", "812 Superfast", "296 GTB", "SF90"],
    "Fiat": ["500", "500e", "500X", "Panda", "Tipo"],
    "Ford": ["Fiesta", "Focus", "Puma", "Kuga", "Mustang", "Mach-E", "Ranger", "Bronco"],
    "Honda": ["Civic", "HR-V", "CR-V", "Jazz", "e"],
    "Hyundai": ["i20", "i30", "Tucson", "Santa Fe", "Kona", "IONIQ 5"],
    "Jaguar": ["F-Type", "F-Pace", "E-Pace", "I-Pace", "XE", "XF"],
    "Jeep": ["Renegade", "Compass", "Wrangler", "Grand Cherokee", "Avenger"],
    "Kia": ["Picanto", "Rio", "Ceed", "Sportage", "Sorento", "EV6", "Niro"],
    "Lamborghini": ["Urus", "Huracan", "Aventador", "Revuelto"],
    "Land Rover": ["Defender", "Discovery", "Range Rover", "Range Rover Sport", "Evoque", "Velar"],
    "Lexus": ["UX", "NX", "RX", "ES", "LC"],
    "Lotus": ["Emira", "Evija", "Eletre"],
    "Maserati": ["Ghibli", "Levante", "Quattroporte", "MC20", "Grecale"],
    "Mazda": ["MX-5", "CX-30", "CX-5", "CX-60", "Mazda3"],
    "McLaren": ["720S", "570S", "Artura", "GT"],
    "Mercedes": ["Classe A", "Classe C", "Classe E", "Classe S", "CLA", "GLA", "GLC", "GLE", "Classe G", "AMG GT", "SL", "EQE", "EQS"],
    "Mini": ["Cooper", "Cooper S", "Clubman", "Countryman"],
    "Nissan": ["Micra", "Juke", "Qashqai", "X-Trail", "GTR", "Ariya"],
    "Opel": ["Corsa", "Astra", "Mokka", "Grandland"],
    "Peugeot": ["208", "308", "408", "508", "2008", "3008", "5008", "Rifter"],
    "Porsche": ["911", "718 Cayman", "718 Boxster", "Panamera", "Macan", "Cayenne", "Taycan"],
    "Renault": ["Clio", "Captur", "Megane", "Arkana", "Austral", "Espace", "Rafale", "Zoe", "Twingo"],
    "Rolls-Royce": ["Phantom", "Ghost", "Cullinan", "Spectre"],
    "Seat": ["Ibiza", "Leon", "Ateca", "Arona", "Tarraco"],
    "Skoda": ["Fabia", "Octavia", "Superb", "Kamiq", "Karoq", "Kodiaq", "Enyaq"],
    "Smart": ["Fortwo", "Forfour", "#1", "#3"],
    "Suzuki": ["Swift", "Ignis", "Vitara", "Jimny", "S-Cross"],
    "Tesla": ["Model 3", "Model Y", "Model S", "Model X"],
    "Toyota": ["Yaris", "Corolla", "C-HR", "RAV4", "Land Cruiser", "Supra", "Aygo X"],
    "Volkswagen": ["Polo", "Golf", "T-Roc", "Tiguan", "Passat", "Arteon", "Touareg", "ID.3", "ID.4", "ID. Buzz"],
    "Volvo": ["XC40", "XC60", "XC90", "S60", "V60", "C40"]
}

OPTIONS_POSSIBLES = [
    "Toit Ouvrant Pano", "Cuir Nappa", "Sièges Chauffants", "CarPlay", "Caméra 360°", 
    "Affichage Tête Haute", "Son Burmester", "Pack Carbone", "Jantes 21 pouces", 
    "Matrix LED", "Suspension Pneumatique", "Attelage", "Pack Hiver", "Night Package"
]

VILLES = ["Paris", "Lyon", "Marseille", "Bordeaux", "Lille", "Nantes", "Strasbourg", "Nice", "Monaco", "Cannes", "Luxembourg", "Genève"]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Ajout de la colonne 'options'
        writer.writerow(["id", "marque", "modele", "finition", "titre", "prix", "cote_argus", "km", "annee", "ville", "url", "img_url", "options", "date_scrape"])

def generer_voiture():
    marque = random.choice(list(DB_AUTO.keys()))
    modele = random.choice(DB_AUTO[marque])
    
    # Prix de base estimé (très simplifié pour couvrir tout le monde)
    prix_base = 25000
    if marque in ["Porsche", "Ferrari", "Lamborghini", "McLaren", "Rolls-Royce", "Bentley"]: prix_base = 150000
    elif marque in ["Audi", "BMW", "Mercedes", "Land Rover", "Jaguar", "Maserati"]: prix_base = 50000
    elif marque in ["Dacia", "Fiat", "Suzuki"]: prix_base = 15000
    
    annee = random.randint(2016, 2024)
    km = random.randint(1000, 180000)
    
    # Calcul Cote
    age = 2025 - annee
    decote = (age * 0.09) + (km / 150000 * 0.20)
    cote_theorique = int(prix_base * (1 - decote))
    
    # Prix de Vente
    variation = random.uniform(0.75, 1.25)
    prix_vente = int(cote_theorique * variation)
    if prix_vente < 4000: prix_vente = 4000
    
    # Options (3 ou 4 au hasard)
    opts = random.sample(OPTIONS_POSSIBLES, k=random.randint(2, 4))
    options_str = " | ".join(opts) # On les sépare par une barre verticale

    titre = f"{marque} {modele}"
    finition = random.choice(["Business", "Sport", "Luxe", "Standard"])
    
    # Image
    rand = random.randint(1, 9999)
    # Mot clé pour l'image
    keyword = marque.lower().replace(" ", "")
    img_url = f"https://loremflickr.com/600/400/{keyword},car?lock={rand}"
    
    ad_id = f"ref-{random.randint(100000, 999999)}"

    return [
        ad_id,
        marque,
        modele,
        finition,
        titre,
        str(prix_vente),
        str(cote_theorique),
        str(km),
        str(annee),
        random.choice(VILLES),
        "https://www.google.com",
        img_url,
        options_str,
        datetime.now().strftime("%Y-%m-%d")
    ]

def run_simulation():
    print("🌍 Génération de la base de données Mondiale...")
    init_csv()
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for i in range(250): # 250 voitures pour avoir du choix
            writer.writerow(generer_voiture())
            
    print("✅ 250 véhicules générés (Toutes marques).")

if __name__ == "__main__":
    run_simulation()