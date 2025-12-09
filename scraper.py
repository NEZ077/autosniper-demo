import csv
from datetime import datetime

CSV_FILE = "annonces.csv"

# --- DONNÉES MANUELLES RÉELLES (LE TOP DU TOP) ---
# Ce sont des configurations réalistes de marché actuel (2024/2025)
REAL_DATA = [
    {
        "marque": "Porsche", "modele": "911 (992) GT3", "titre": "Porsche 911 (992) GT3 Clubsport - 4.0L Atmo",
        "prix": 225000, "cote": 245000, "km": 12500, "annee": 2022,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/Porsche_992_GT3_at_IAA_2021_1X7A0322.jpg/1200px-Porsche_992_GT3_at_IAA_2021_1X7A0322.jpg",
        "ville": "Monaco", "cv": "510", "carb": "Essence", "boite": "PDK", "couleur": "Bleu Requin",
        "options": "Pack Clubsport | Lift System | Freins Céramiques | Sièges Baquets Carbone | Chrono Pack",
        "status": "Pépite"
    },
    {
        "marque": "Audi", "modele": "RS6 Avant", "titre": "Audi RS6 Avant C8 - Céramique / Akrapovic",
        "prix": 118000, "cote": 129000, "km": 42000, "annee": 2021,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8b/Audi_RS6_C8_Avant_Sindelfingen_2020_1X7A6266.jpg/1200px-Audi_RS6_C8_Avant_Sindelfingen_2020_1X7A6266.jpg",
        "ville": "Strasbourg", "cv": "600", "carb": "Essence", "boite": "Tiptronic", "couleur": "Gris Nardo",
        "options": "Pack Dynamique Plus | Échappement Akrapovic | Toit Panoramique | Bang & Olufsen",
        "status": "Clean"
    },
    {
        "marque": "Ferrari", "modele": "Roma", "titre": "Ferrari Roma V8 - Française - Malus Payé",
        "prix": 205000, "cote": 215000, "km": 8500, "annee": 2022,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Ferrari_Roma_IMG_5082.jpg/1200px-Ferrari_Roma_IMG_5082.jpg",
        "ville": "Paris 16e", "cv": "620", "carb": "Essence", "boite": "F1", "couleur": "Gris Silverstone",
        "options": "Écussons d'ailes | Caméra 360 | Sièges Daytona | Carbone Intérieur",
        "status": "Clean"
    },
    {
        "marque": "Mercedes", "modele": "G63 AMG", "titre": "Mercedes Classe G 63 AMG - Manufaktur",
        "prix": 185000, "cote": 195000, "km": 25000, "annee": 2021,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Mercedes-AMG_G_63_W463A_IMG_3756.jpg/1200px-Mercedes-AMG_G_63_W463A_IMG_3756.jpg",
        "ville": "Cannes", "cv": "585", "carb": "Essence", "boite": "Speedshift", "couleur": "Noir Mat",
        "options": "Pack Nuit | Sièges Massants | Jantes 22 | Attelage",
        "status": "Clean"
    },
    {
        "marque": "BMW", "modele": "M4 Competition", "titre": "BMW M4 Competition xDrive - Pack Carbone",
        "prix": 89000, "cote": 96000, "km": 18000, "annee": 2022,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/BMW_M4_Competition_G82.jpg/1200px-BMW_M4_Competition_G82.jpg",
        "ville": "Lyon", "cv": "510", "carb": "Essence", "boite": "Auto", "couleur": "Jaune Sao Paulo",
        "options": "Sièges Carbone | Laser Light | HUD | Drift Analyzer",
        "status": "Pépite"
    },
    {
        "marque": "Lamborghini", "modele": "Urus", "titre": "Lamborghini Urus - 4.0 V8 - Config Full Black",
        "prix": 260000, "cote": 255000, "km": 35000, "annee": 2020,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3b/Lamborghini_Urus_IMG_3619.jpg/1200px-Lamborghini_Urus_IMG_3619.jpg",
        "ville": "Monaco", "cv": "650", "carb": "Essence", "boite": "Auto", "couleur": "Noir",
        "options": "Toit Ouvrant | Bang & Olufsen | Pack ADAS | Jantes 23",
        "status": "Clean"
    },
    {
        "marque": "Peugeot", "modele": "308 GT", "titre": "Peugeot 308 III SW GT - Hybride 225",
        "prix": 32000, "cote": 36000, "km": 15000, "annee": 2023,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/Peugeot_308_SW_GT_Hybrid_225_IMG_5527.jpg/1200px-Peugeot_308_SW_GT_Hybrid_225_IMG_5527.jpg",
        "ville": "Nantes", "cv": "225", "carb": "Hybride", "boite": "EAT8", "couleur": "Vert Avatar",
        "options": "Toit Ouvrant | Matrix LED | Caméra 360 | Drive Assist",
        "status": "Pépite"
    },
    {
        "marque": "Alpine", "modele": "A110", "titre": "Alpine A110 Première Édition - Numérotée",
        "prix": 62000, "cote": 65000, "km": 40000, "annee": 2018,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Alpine_A110_Premiere_Edition_2017_%2837330560274%29.jpg/1200px-Alpine_A110_Premiere_Edition_2017_%2837330560274%29.jpg",
        "ville": "Dieppe", "cv": "252", "carb": "Essence", "boite": "Auto", "couleur": "Bleu Alpine",
        "options": "Échappement Sport | Gros Freins | Audio Focal",
        "status": "Clean"
    },
    {
        "marque": "Porsche", "modele": "Macan (LEASING)", "titre": "Porsche Macan S - 1er Loyer Majoré (ATTENTION)",
        "prix": 9900, "cote": 65000, "km": 80000, "annee": 2019,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Porsche_Macan_GTS_Genf_2018.jpg/1200px-Porsche_Macan_GTS_Genf_2018.jpg",
        "ville": "Bordeaux", "cv": "354", "carb": "Essence", "boite": "PDK", "couleur": "Gris Volcan",
        "options": "PASM | Toit Ouvrant | Jantes RS Spyder",
        "status": "Leasing" # Pour tester ton filtre "Anti-Leasing"
    },
    {
        "marque": "Volkswagen", "modele": "Golf 8 R", "titre": "VW Golf 8 R - 320ch - Performance - Moteur HS",
        "prix": 18000, "cote": 45000, "km": 15000, "annee": 2022,
        "img": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/VW_Golf_8_R_IMG_4111.jpg/1200px-VW_Golf_8_R_IMG_4111.jpg",
        "ville": "Lille", "cv": "320", "carb": "Essence", "boite": "DSG", "couleur": "Bleu Lapiz",
        "options": "Akrapovic | Drift Mode | Cuir Nappa",
        "status": "Accidentée" # Pour tester ton filtre "Anti-Épave"
    }
]

def init_csv():
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "marque", "modele", "titre", "prix", "cote_argus", "km", "annee", "ville", "distance", "url", "img_url", "options", "carburant", "boite", "couleur", "chevaux", "status", "source", "date_scrape"])

def run_injection():
    print("💎 Injection des données DÉMO INVESTISSEUR...")
    init_csv()
    
    count = 0
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        for i, car in enumerate(REAL_DATA):
            # Construction de la ligne CSV parfaite
            row = [
                f"demo-{i+1000}", # ID
                car['marque'],
                car['modele'],
                car['titre'],
                str(car['prix']),
                str(car['cote']),
                str(car['km']),
                str(car['annee']),
                car['ville'],
                "15", # Distance fictive proche
                "https://www.leboncoin.fr", # Lien source
                car['img'],
                car['options'],
                car['carb'],
                car['boite'],
                car['couleur'],
                car['cv'],
                car['status'],
                "LeBonCoin" if i % 2 == 0 else "LaCentrale", # Alternance des sources
                datetime.now().strftime("%Y-%m-%d")
            ]
            writer.writerow(row)
            count += 1
            
    print(f"✅ {count} annonces haute qualité injectées.")
    print("👉 Lance 'streamlit run app.py' pour voir le résultat.")

if __name__ == "__main__":
    run_injection()