import time
import random
import csv
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
CSV_FILE = "annonces.csv"

# Liste des cibles (Tu peux modifier les filtres ici, par exemple ajouter &pricefrom=10000)
URLS_CIBLES = {
    "Audi": "https://www.autoscout24.fr/lst/audi?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU",
    "BMW": "https://www.autoscout24.fr/lst/bmw?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU",
    "Mercedes": "https://www.autoscout24.fr/lst/mercedes-benz?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU",
    "Porsche": "https://www.autoscout24.fr/lst/porsche?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU",
    "Renault": "https://www.autoscout24.fr/lst/renault?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU"
}

def init_csv():
    # On écrase le fichier pour repartir à zéro
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "titre", "prix", "km", "annee", "ville", "url", "img_url", "date_scrape"])

def clean_text(text):
    if not text: return "0"
    return "".join(re.findall(r'\d+', text))

def run_scraper():
    init_csv()
    
    with sync_playwright() as p:
        # On garde le mode visible pour être sûr que les images chargent
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1366, "height": 768})
        page = context.new_page()

        print("[START] Démarrage de la tournée des constructeurs...")

        # BOUCLE SUR CHAQUE MARQUE
        for marque, url in URLS_CIBLES.items():
            print(f"\n[ÉTAPE] Analyse de : {marque.upper()}...")
            
            try:
                page.goto(url, timeout=60000)
                
                # Gestion cookies (seulement au premier passage ou si elle réapparait)
                try:
                    if page.locator("button:has-text('Accepter')").is_visible():
                        page.click("button:has-text('Accepter')")
                        time.sleep(1)
                except: pass

                # Scroll progressif pour charger les images (Lazy Loading)
                for _ in range(5):
                    page.mouse.wheel(0, 500)
                    time.sleep(0.5)
                
                page.wait_for_selector("article", timeout=10000)
                annonces = page.locator("article[data-testid='list-item']").all()
                print(f"  -> {len(annonces)} annonces trouvées pour {marque}.")

                count = 0
                existing_ids = set() # Reset des IDs pour éviter doublons intra-page mais pas inter-marques

                with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)

                    for card in annonces:
                        try:
                            # 1. LIEN (Correction du bug de lien)
                            link_el = card.locator("a").first
                            raw_url = link_el.get_attribute("href")
                            
                            if not raw_url: continue
                            
                            # Si le lien commence par http, c'est bon, sinon on ajoute le domaine
                            full_url = raw_url if raw_url.startswith("http") else "https://www.autoscout24.fr" + raw_url
                            
                            # ID unique
                            ad_id = raw_url.split('-')[-1]
                            if ad_id in existing_ids: continue

                            # 2. IMAGE (On cherche le srcset qui contient la HD, sinon src)
                            img_url = "https://placehold.co/600x400?text=Pas+d+image"
                            try:
                                # On cible la première image de l'article
                                img_el = card.locator("img").first
                                # AutoScout met souvent l'image HD dans srcset. On prend le premier lien du srcset.
                                srcset = img_el.get_attribute("srcset")
                                if srcset:
                                    img_url = srcset.split(',')[0].split(' ')[0] # On prend la 1ère URL du lot
                                else:
                                    img_url = img_el.get_attribute("src")
                            except: pass

                            # 3. DONNÉES CLASSIQUES
                            titre = card.locator("h2").first.inner_text().strip()
                            
                            prix_raw = card.locator("p[data-testid='regular-price']").first.inner_text()
                            prix = clean_text(prix_raw)

                            all_text = card.inner_text()
                            match_annee = re.search(r'(20\d{2})', all_text)
                            annee = match_annee.group(1) if match_annee else "2020"

                            match_km = re.search(r'([\d\s\.]+)\s*km', all_text)
                            km = clean_text(match_km.group(1)) if match_km else "0"

                            # 4. SAUVEGARDE
                            writer.writerow([ad_id, titre, prix, km, annee, "France", full_url, img_url, datetime.now()])
                            existing_ids.add(ad_id)
                            count += 1
                            print(f"    + {titre} ({prix}€)")

                        except Exception as e:
                            continue
                
                print(f"  ✅ {count} {marque} ajoutées.")

            except Exception as e:
                print(f"  ❌ Erreur sur {marque}: {e}")

            # Petite pause entre les marques pour ne pas énerver le site
            time.sleep(3)

        print("\n[FIN] Tournée terminée. Fichier annonces.csv prêt.")
        browser.close()

if __name__ == "__main__":
    run_scraper()