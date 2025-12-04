import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION PAGE ---
st.set_page_config(
    page_title="AutoSniper Elite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLE CSS (Dark & Gold) ---
st.markdown("""
<style>
    .stApp {background-color: #0e1117;}
    div[data-testid="stMetric"] {
        background-color: #1f2937;
        border: 1px solid #374151;
        padding: 10px;
        border-radius: 8px;
    }
    .big-font {font-size:20px !important; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT ---
@st.cache_data(ttl=900) # Mise à jour toutes les 15 min
def charger_donnees():
    if not os.path.exists("annonces.csv"):
        return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    # Conversion types
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    df['km'] = pd.to_numeric(df['km'], errors='coerce')
    df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
    
    # --- CALCUL SCORE DEAL (Intelligence Artificielle Simulée) ---
    def analyser_deal(row):
        # On refait une estimation simplifiée pour la démo
        # Dans la vraie vie, ce serait une requête API Argus
        base_price = row['prix']
        # On estime que la "valeur réelle" est basée sur le prix moyen des modèles similaires dans la base
        # Ici on triche un peu pour la démo : on utilise une formule inverse du générateur
        
        # Score de 0 à 100.
        # Plus le rapport (KM / Prix) est avantageux par rapport à l'année, mieux c'est.
        score = 50 # Neutre
        
        # Bonus Année
        if row['annee'] >= 2022: score += 10
        
        # Logique Prix : Si c'est une Porsche à 20k, c'est louche ou génial.
        # Pour la simulation, on va simuler un score aléatoire cohérent avec le générateur
        import random
        random.seed(row['id']) # Pour que le score reste fixe pour une même voiture
        
        # On booste les scores pour que l'interface soit jolie
        score_final = random.randint(40, 95)
        
        label = "Standard"
        if score_final >= 85: label = "💎 PÉPITE"
        elif score_final >= 70: label = "✅ Bon coup"
        elif score_final <= 50: label = "❌ Trop cher"
            
        return score_final, label

    res = df.apply(analyser_deal, axis=1, result_type='expand')
    df['score'] = res[0]
    df['label'] = res[1]
    
    return df.sort_values(by='score', ascending=False)

df = charger_donnees()

# --- SIDEBAR ---
with st.sidebar:
    st.title("💎 AutoSniper Elite")
    st.caption("Market Scanner v3.0")
    
    if st.button("🔄 Reload Data"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # Filtres
    if not df.empty:
        marques = sorted(list(set([t.split(' ')[0] for t in df['titre']])))
        sel_marque = st.multiselect("Marque", marques)
        
        range_prix = st.slider("Budget", 5000, 150000, (10000, 80000))
        
        filtre_pepite = st.checkbox("💎 Afficher uniquement les Pépites")

# --- FILTRAGE ---
if df.empty:
    st.warning("⚠️ Base de données vide. Lancez la simulation.")
    st.stop()

df_f = df.copy()
if sel_marque:
    df_f = df_f[df_f['titre'].apply(lambda x: any(m in x for m in sel_marque))]
df_f = df_f[(df_f['prix'] >= range_prix[0]) & (df_f['prix'] <= range_prix[1])]

if filtre_pepite:
    df_f = df_f[df_f['score'] >= 85]

# --- DASHBOARD ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Véhicules Scanés", len(df_f))
c2.metric("Prix Moyen", f"{int(df_f['prix'].mean()):,} €".replace(',', ' '))
c3.metric("Meilleur Score", f"{df_f['score'].max()}/100")
c4.metric("Pépites Trouvées", len(df_f[df_f['score'] >= 85]))

st.write("")

# Onglets
tab1, tab2 = st.tabs(["📊 Market Map", "🚘 Liste des Annonces"])

with tab1:
    st.markdown("##### 📍 Positionnement Prix / KM")
    fig = px.scatter(
        df_f, x="km", y="prix", size="score", color="label",
        color_discrete_map={"💎 PÉPITE": "#00ff00", "✅ Bon coup": "#3498db", "Standard": "#95a5a6", "❌ Trop cher": "#e74c3c"},
        hover_data=["titre", "annee"], height=500
    )
    fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.markdown(f"##### {len(df_f)} Opportunités identifiées")
    cols = st.columns(3)
    for i, row in df_f.iterrows():
        with cols[i % 3]:
            # Couleur bordure
            color = "#00ff00" if row['score'] >= 85 else "#333"
            
            with st.container(border=True):
                # Image
                st.image(row['img_url'], use_container_width=True)
                
                # Header
                c_a, c_b = st.columns([3, 1])
                c_a.write(f"**{row['titre']}**")
                if row['score'] >= 85:
                    c_b.markdown("💎")
                
                # Prix
                st.markdown(f"<div class='big-font'>{row['prix']} €</div>", unsafe_allow_html=True)
                st.caption(f"{row['annee']} | {row['km']} km | {row['ville']}")
                
                # Jauge
                st.progress(row['score'] / 100, text=f"Deal Score: {row['score']}/100")
                
                st.button("Voir détails", key=row['id'], use_container_width=True)