import time
import os
from datetime import datetime

# Combien de temps attendre entre deux scans (en minutes)
MINUTES_ATTENTE = 60

def run_auto():
    print("🤖 AUTO-SNIPER : Pilote activé.")
    print("Laisse cette fenêtre ouverte pour que le site se mette à jour.\n")

    while True:
        now = datetime.now().strftime("%H:%M")
        print(f"[{now}] 🚀 Lancement du scan...")
        
        # 1. Lance le scraper
        # (Assure-toi que scraper.py fonctionne bien quand tu le lances seul)
        exit_code = os.system("python scraper.py")
        
        if exit_code == 0:
            print(f"[{now}] ✅ Scan terminé. Envoi vers le site...")
            
            # 2. Envoie sur GitHub (ce qui mettra à jour Streamlit)
            os.system("git add annonces.csv")
            os.system('git commit -m "Auto-update depuis PC"')
            os.system("git push")
            
            print(f"[{now}] ☁️ Site mis à jour !")
        else:
            print(f"[{now}] ❌ Erreur pendant le scan.")

        print(f"💤 Pause de {MINUTES_ATTENTE} minutes...\n")
        time.sleep(MINUTES_ATTENTE * 60)

if __name__ == "__main__":
    run_auto()