import time
import random
import csv
import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
CSV_FILE = "annonces.csv"
TARGET_URL = "https://www.autoscout24.fr/lst/audi/a1?atype=C&cy=F&desc=0&sort=standard&source=homepage_search-mask&ustate=N%2CU"

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
        # --- OPTIMISATION 1 : HEADLESS = TRUE (Mode Invisible) ---
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        # --- OPTIMISATION 2 : BLOQUER LES IMAGES ET LE CSS ---
        # Ça empêche de charger les trucs lourds inutiles
        def block_heavy_resources(route):
            if route.request.resource_type in ["image", "stylesheet", "font", "media"]:
                route.abort()
            else:
                route.continue_()
        
        page.route("**/*", block_heavy_resources)

        print(f"[START] Connexion Rapide à AutoScout24 (Mode Turbo)...")
        
        try:
            start_time = time.time()
            page.goto(TARGET_URL, timeout=60000)
            
            # Plus besoin d'attendre l'affichage visuel des cookies car on ne clique pas dessus
            # On va direct aux données
            
            print("[INFO] Page chargée. Extraction en cours...")
            
            # On attend juste que le texte des articles soit là
            page.wait_for_selector("article", timeout=10000)
            
            annonces = page.locator("article[data-testid='list-item']").all()
            print(f"[INFO] {len(annonces)} annonces détectées.")

            count = 0
            existing_ids = set()

            with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)

                for card in annonces:
                    try:
                        # Extraction ultra-rapide
                        titre = card.locator("h2").first.inner_text().strip()
                        
                        prix_raw = card.locator("p[data-testid='regular-price']").first.inner_text()
                        prix = clean_text(prix_raw)

                        all_text = card.inner_text()
                        match_annee = re.search(r'(20\d{2})', all_text)
                        annee = match_annee.group(1) if match_annee else "2020"

                        match_km = re.search(r'([\d\s\.]+)\s*km', all_text)
                        km = clean_text(match_km.group(1)) if match_km else "0"

                        lien_el = card.locator("a").first
                        relative_url = lien_el.get_attribute("href")
                        full_url = "https://www.autoscout24.fr" + relative_url
                        ad_id = relative_url.split('-')[-1]
                        
                        if ad_id in existing_ids: continue

                        # On met une fausse image car on a bloqué le chargement des vraies pour la vitesse
                        # (L'app Streamlit chargera la vraie image plus tard si on clique sur le lien, 
                        # ou on peut laisser le placeholder pour la liste)
                        img_url = "https://placehold.co/600x400/222/fff?text=Image+Non+Chargee"

                        writer.writerow([ad_id, titre, prix, km, annee, "France", full_url, img_url, datetime.now()])
                        existing_ids.add(ad_id)
                        count += 1
                        
                        # Petit print pour voir que ça avance
                        print(f"  ⚡ {titre} -> {prix}€")

                    except:
                        continue
            
            duration = round(time.time() - start_time, 2)
            print(f"[RESULTAT] {count} voitures extraites en {duration} secondes !")

        except Exception as e:
            print(f"[ERREUR] {e}")

        browser.close()

if __name__ == "__main__":
    run_scraper()