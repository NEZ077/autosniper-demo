import csv
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- TES 10 VOITURES (Modifie les titres/prix selon tes photos) ---
REAL_DATA = [
    {
        "file": "Porsche 911 (992) GT3 Clubsport - 4.0L Atmo.jpg", # Ta photo 1.jpg
        "marque": "Porsche", "modele": "911 GT3", "titre": "Porsche 911 (992) GT3 - Clubsport",
        "prix": 225000, "cote": 245000, "km": 12500, "annee": 2022,
        "ville": "Monaco", "cv": "510", "carb": "Essence", "boite": "PDK", "couleur": "Bleu",
        "options": "Pack Clubsport | Lift System | Céramique", "status": "Pépite"
    },
    {
        "file": "Audi RS6 Avant C8.jpg", # Ta photo 2.jpg
        "marque": "Audi", "modele": "RS6", "titre": "Audi RS6 Avant C8 - Full Black",
        "prix": 118000, "cote": 129000, "km": 42000, "annee": 2021,
        "ville": "Paris", "cv": "600", "carb": "Essence", "boite": "Auto", "couleur": "Noir",
        "options": "Toit Pano | Akrapovic | Bang & Olufsen", "status": "Clean"
    },
    {
        "file": "Ferrari Roma V8.jpg", 
        "marque": "Ferrari", "modele": "Roma", "titre": "Ferrari Roma V8 - Malus Payé",
        "prix": 205000, "cote": 215000, "km": 8500, "annee": 2022,
        "ville": "Cannes", "cv": "620", "carb": "Essence", "boite": "F1", "couleur": "Gris",
        "options": "Sièges Daytona | Caméra 360 | Écussons", "status": "Clean"
    },
    {
        "file": "Mercedes Classe G 63 AMG - Manufaktur.jpg",
        "marque": "Mercedes", "modele": "G63 AMG", "titre": "Mercedes Classe G 63 AMG",
        "prix": 185000, "cote": 195000, "km": 25000, "annee": 2021,
        "ville": "Lyon", "cv": "585", "carb": "Essence", "boite": "Auto", "couleur": "Noir Mat",
        "options": "Pack Nuit | Sièges Massants | Attelage", "status": "Clean"
    },
    {
        "file": "BMW M4 Competition xDrive - Pack Carbone.jpg",
        "marque": "BMW", "modele": "M4", "titre": "BMW M4 Competition xDrive",
        "prix": 89000, "cote": 96000, "km": 18000, "annee": 2022,
        "ville": "Lille", "cv": "510", "carb": "Essence", "boite": "Auto", "couleur": "Jaune",
        "options": "Sièges Carbone | Laser Light | HUD", "status": "Pépite"
    },
    {
        "file": "Lamborghini Urus - 4.0 V8 - Config Full Black.jpg",
        "marque": "Lamborghini", "modele": "Urus", "titre": "Lamborghini Urus 4.0 V8",
        "prix": 260000, "cote": 255000, "km": 35000, "annee": 2020,
        "ville": "Nice", "cv": "650", "carb": "Essence", "boite": "Auto", "couleur": "Jaune",
        "options": "Jantes 23 | Toit Ouvrant | Full ADAS", "status": "Clean"
    },
    {
        "file": "Peugeot 308 III SW GT - Hybride 225.jpg",
        "marque": "Peugeot", "modele": "308", "titre": "Peugeot 308 SW GT Hybride",
        "prix": 32000, "cote": 36000, "km": 15000, "annee": 2023,
        "ville": "Nantes", "cv": "225", "carb": "Hybride", "boite": "Auto", "couleur": "Vert",
        "options": "Matrix LED | Caméra 360 | Drive Assist", "status": "Pépite"
    },
    {
        "file": "Alpine A110 Première Édition - Numérotée.jpg",
        "marque": "Alpine", "modele": "A110", "titre": "Alpine A110 Première Édition",
        "prix": 62000, "cote": 65000, "km": 40000, "annee": 2018,
        "ville": "Dieppe", "cv": "252", "carb": "Essence", "boite": "Auto", "couleur": "Bleu",
        "options": "Échappement Sport | Gros Freins | Focal", "status": "Clean"
    },
    {
        "file": "Porsche Macan S - 1er Loyer Majoré (ATTENTION).jpg",
        "marque": "Porsche", "modele": "Macan", "titre": "Porsche Macan S Diesel",
        "prix": 9900, "cote": 65000, "km": 80000, "annee": 2019,
        "ville": "Bordeaux", "cv": "258", "carb": "Diesel", "boite": "PDK", "couleur": "Gris",
        "options": "PASM | Toit Ouvrant | Jantes RS Spyder", "status": "Leasing"
    },
    {
        "file": "VW Golf 8 R - 320ch - Performance - Moteur HS.jpg",
        "marque": "Volkswagen", "modele": "Golf R", "titre": "VW Golf 8 R Performance",
        "prix": 18000, "cote": 45000, "km": 15000, "annee": 2022,
        "ville": "Strasbourg", "cv": "320", "carb": "Essence", "boite": "DSG", "couleur": "Bleu",
        "options": "Akrapovic | Drift Mode | Cuir Nappa", "status": "Accidentée"
    }
]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "status", "source", "date_scrape"])

def run_injection():
    print("📸 Injection de tes PHOTOS PERSONNELLES...")
    init_csv()
    
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for i, car in enumerate(REAL_DATA):
            row = [
                f"perso-{i+1}",
                car['marque'], car['modele'], car['titre'],
                str(car['prix']), str(car['cote']), str(car['km']), str(car['annee']),
                car['ville'], "10", 
                "https://www.leboncoin.fr", 
                car['file'], # Ici on met juste "1.jpg"
                car['options'], car['carb'], car['boite'], car['couleur'], car['cv'],
                car['status'], "LeBonCoin", datetime.now().strftime("%Y-%m-%d")
            ]
            writer.writerow(row)
            
    print("✅ Terminé. Tes 10 photos sont liées.")

if __name__ == "__main__":
    run_injection()