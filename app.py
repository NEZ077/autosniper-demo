import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="AutoSniper", layout="wide")

# --- FONCTION DE CHARGEMENT ---
def charger_donnees():
    if not os.path.exists("annonces.csv"):
        return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    # Conversion des types pour les calculs
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
    
    # --- LOGIQUE MÉTIER (Le Cerveau du Sniper) ---
    # On invente une "Cote Théorique" pour voir si c'est une bonne affaire
    # Dans la vraie vie, on récupérerait la vraie cote Argus via une API
    
    def calculer_rentabilite(row):
        # Prix de base estimé selon la marque (simplifié pour la démo)
        cote_theorique = 25000 
        if "Audi" in row['titre'] or "BMW" in row['titre']:
            cote_theorique += 5000
        if "Renault" in row['titre'] or "Peugeot" in row['titre']:
            cote_theorique -= 5000
            
        # Décote par année et km
        age = 2024 - row['annee']
        cote_reelle = cote_theorique - (age * 1000) - (int(str(row['km']).replace(' km','')) / 1000 * 50)
        
        # Marge espérée
        profit_potentiel = cote_reelle - row['prix']
        return profit_potentiel

    df['profit'] = df.apply(calculer_rentabilite, axis=1)
    
    # Tri par rentabilité (les meilleures affaires en premier)
    df = df.sort_values(by='profit', ascending=False)
    
    return df

# --- INTERFACE ---
st.title("🎯 AutoSniper - Chasseur de Rentabilité")
st.markdown("### Analyse de marché en temps réel")

if st.button("🔄 Rafraîchir les opportunités"):
    st.rerun()

df = charger_donnees()

if df.empty:
    st.warning("⚠️ Aucune donnée. Lance le scraper !")
else:
    # --- KPI (Indicateurs Clés) ---
    meilleure_affaire = df.iloc[0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Annonces scannées", len(df))
    col2.metric("Meilleur profit estimé", f"{int(meilleure_affaire['profit'])} €", delta="Top opportunité")
    col3.metric("Prix moyen marché", f"{int(df['prix'].mean())} €")
    
    st.divider()

    # --- LISTING INTELLIGENT ---
    cols = st.columns(3)
    for index, row in df.iterrows():
        col = cols[index % 3]
        with col:
            # Code couleur selon la rentabilité
            border_color = "grey"
            badge = ""
            
            if row['profit'] > 3000:
                badge = "🔥 SUPER AFFAIRE"
                style = "background-color: #d4edda; padding: 10px; border-radius: 5px;"
            elif row['profit'] > 1000:
                badge = "✅ Rentable"
                style = "background-color: #fff3cd; padding: 10px; border-radius: 5px;"
            else:
                badge = "❌ Trop cher"
                style = "background-color: #f8d7da; padding: 10px; border-radius: 5px;"

            with st.container(border=True):
                st.image(row['img_url'], use_container_width=True)
                
                # Badge de rentabilité
                st.markdown(f"<div style='{style}'><strong>{badge}</strong><br>Gain est.: +{int(row['profit'])}€</div>", unsafe_allow_html=True)
                
                st.write("") # Espace
                st.subheader(f"{int(row['prix'])} €")
                st.write(f"**{row['titre']}**")
                st.caption(f"{row['ville']} | {row['annee']} | {row['km']}")
                st.link_button("Voir l'annonce", row['url'])