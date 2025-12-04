import time
import random
import csv
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
CSV_FILE = "annonces.csv"

# On limite à 2 marques pour le test Cloud (plus rapide et moins risqué)
URLS_CIBLES = {
    "Audi": "https://www.autoscout24.fr/lst/audi?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU",
    "BMW": "https://www.autoscout24.fr/lst/bmw?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU"
}

def init_csv():
    # En mode Cloud, on veut parfois garder l'historique, mais ici on écrase pour le test
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "titre", "prix", "km", "annee", "ville", "url", "img_url", "date_scrape"])

def clean_text(text):
    if not text: return "0"
    return "".join(re.findall(r'\d+', text))

def run_scraper():
    init_csv()
    
    with sync_playwright() as p:
        # --- CONFIGURATION NINJA CLOUD ---
        # 1. Headless = True (Obligatoire sur GitHub Actions sinon ça crash)
        # 2. Args spécifiques pour cacher le mode Robot
        browser = p.chromium.launch(
            headless=True, 
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )
        
        # 3. User Agent de Mr Tout-le-monde
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        
        # 4. Script pour effacer la variable 'webdriver' (La preuve n°1 qu'on est un robot)
        context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        page = context.new_page()

        print("[START] Démarrage du Robot Furtif...")

        total_global = 0

        for marque, url in URLS_CIBLES.items():
            print(f"\n[SCAN] Recherche : {marque}...")
            
            try:
                page.goto(url, timeout=90000)
                
                # Attente aléatoire humaine
                time.sleep(random.uniform(2, 5))

                # Gestion Cookies (Si présent)
                try:
                    if page.locator("button:has-text('Accepter')").is_visible():
                        page.click("button:has-text('Accepter')")
                except: pass

                # On attend le chargement des articles
                try:
                    page.wait_for_selector("article", timeout=20000)
                except:
                    print(f"  ⚠️ {marque} : Page chargée mais pas d'articles détectés (Blocage possible).")
                    # On tente un screenshot pour debugger si besoin (non visible ici)
                    continue

                annonces = page.locator("article[data-testid='list-item']").all()
                print(f"  -> {len(annonces)} annonces détectées.")

                count = 0
                existing_ids = set()

                with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)

                    for card in annonces:
                        try:
                            # Extraction simplifiée pour robustesse
                            titre = "Inconnu"
                            if card.locator("h2").count() > 0:
                                titre = card.locator("h2").first.inner_text().strip()
                            
                            prix = "0"
                            if card.locator("[data-testid='regular-price']").count() > 0:
                                prix = clean_text(card.locator("[data-testid='regular-price']").first.inner_text())

                            # Lien
                            link_el = card.locator("a").first
                            raw_url = link_el.get_attribute("href") or ""
                            full_url = "https://www.autoscout24.fr" + raw_url if not raw_url.startswith("http") else raw_url
                            ad_id = full_url.split('-')[-1]
                            
                            if ad_id in existing_ids: continue

                            # Image (Placeholder si échec pour aller vite)
                            img_url = "https://placehold.co/600x400?text=Image+Non+Dispo"
                            try:
                                imgs = card.locator("img").all()
                                for img in imgs:
                                    src = img.get_attribute("src")
                                    if src and "autoscout" in src:
                                        img_url = src
                                        break
                            except: pass

                            # Autres infos
                            all_text = card.inner_text()
                            match_annee = re.search(r'(20\d{2})', all_text)
                            annee = match_annee.group(1) if match_annee else "2020"
                            match_km = re.search(r'([\d\s\.]+)\s*km', all_text)
                            km = clean_text(match_km.group(1)) if match_km else "0"

                            writer.writerow([ad_id, titre, prix, km, annee, "France", full_url, img_url, datetime.now()])
                            existing_ids.add(ad_id)
                            count += 1
                            total_global += 1

                        except: continue
                
                print(f"  ✅ {count} {marque} extraites.")

            except Exception as e:
                print(f"  ❌ Erreur critique sur {marque}: {e}")

        print(f"\n[FIN] Total voitures récupérées : {total_global}")
        browser.close()

if __name__ == "__main__":
    run_scraper()