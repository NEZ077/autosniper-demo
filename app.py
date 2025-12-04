import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="AutoSniper Pro", layout="wide", page_icon="🏎️")

# --- CSS PERSONNALISÉ (Pour le look) ---
st.markdown("""
<style>
    .metric-card {background-color: #f0f2f6; border-radius: 10px; padding: 15px;}
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT ---
def charger_donnees():
    if not os.path.exists("annonces.csv"):
        return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    # Nettoyage et typage
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    df['km'] = pd.to_numeric(df['km'], errors='coerce')
    df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
    
    # --- INTELLIGENCE (Algorithme de Rentabilité) ---
    def calculer_rentabilite(row):
        # Cote théorique simplifiée
        base = 35000
        if any(x in row['titre'] for x in ["Audi", "BMW", "Mercedes"]): base += 5000
        if any(x in row['titre'] for x in ["Clio", "208", "C3"]): base -= 15000
        
        decote_km = row['km'] * 0.05
        decote_annee = (2025 - row['annee']) * 1200
        
        cote = base - decote_km - decote_annee
        profit = cote - row['prix']
        return profit

    df['profit'] = df.apply(calculer_rentabilite, axis=1)
    df['rentabilite_label'] = df['profit'].apply(lambda x: "Excellente" if x > 3000 else ("Bonne" if x > 1000 else "Mauvaise"))
    
    return df.sort_values(by='profit', ascending=False)

# --- INTERFACE ---
st.title("🏎️ AutoSniper Pro")
st.markdown("### Le Cockpit de chasse automobile")

if st.button("🔄 Scanner le marché (Refresh)"):
    st.rerun()

df = charger_donnees()

if df.empty:
    st.error("❌ Données manquantes. Lance le script 'scraper.py' d'abord !")
else:
    # --- SIDEBAR (Filtres) ---
    st.sidebar.header("🔍 Filtres de Chasse")
    
    # Filtre Marque
    all_marques = sorted(list(set([t.split(' ')[0] for t in df['titre']])))
    choix_marques = st.sidebar.multiselect("Marques", all_marques, default=all_marques[:3])
    
    # Filtres Sliders
    budget_max = st.sidebar.slider("Budget Max (€)", int(df['prix'].min()), int(df['prix'].max()), 25000)
    km_max = st.sidebar.slider("Kilométrage Max", 0, 200000, 100000)
    
    # Application des filtres
    mask_marque = df['titre'].apply(lambda x: any(m in x for m in choix_marques)) if choix_marques else True
    df_filtered = df[mask_marque & (df['prix'] <= budget_max) & (df['km'] <= km_max)]

    # --- KPI ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Véhicules ciblés", len(df_filtered))
    if not df_filtered.empty:
        col2.metric("Prix Moyen", f"{int(df_filtered['prix'].mean())} €")
        best_deal = df_filtered.iloc[0]
        col3.metric("Meilleur Profit", f"+ {int(best_deal['profit'])} €", delta="Top Deal")
        col4.metric("Année Moyenne", int(df_filtered['annee'].mean()))

    st.divider()

    # --- GRAPHIQUE INTELLIGENT (Le cœur du Sniper) ---
    if not df_filtered.empty:
        st.subheader("📊 Analyse du Marché (Prix vs Km)")
        st.info("💡 Astuce : Les meilleures affaires sont les points en BAS à GAUCHE (Peu de km, petit prix).")
        
        fig = px.scatter(
            df_filtered, 
            x="km", 
            y="prix", 
            color="rentabilite_label",
            color_discrete_map={"Excellente": "green", "Bonne": "orange", "Mauvaise": "red"},
            hover_data=["titre", "annee", "profit"],
            size="profit", # Plus le point est gros, plus le profit est gros
            size_max=15
        )
        st.plotly_chart(fig, use_container_width=True)

    # --- LISTE DES ANNONCES ---
    st.subheader("📋 Liste des opportunités filtrées")
    
    cols = st.columns(3)
    for index, row in df_filtered.iterrows():
        with cols[index % 3]:
            # Badge couleur
            color = "green" if row['profit'] > 3000 else "orange" if row['profit'] > 1000 else "red"
            badge_text = "🔥 SUPER DEAL" if row['profit'] > 3000 else "✅ CORRECT"
            
            with st.container(border=True):
                st.markdown(f"<span style='color:{color}; font-weight:bold'>{badge_text}</span>", unsafe_allow_html=True)
                st.image(row['img_url'], use_container_width=True)
                st.write(f"**{row['titre']}**")
                st.write(f"💰 **{row['prix']} €** | 🛣️ {row['km']} km")
                st.progress(min(100, max(0, int((row['profit']/5000)*100)))) # Barre de rentabilité
                st.caption(f"Profit estimé : {int(row['profit'])} €")