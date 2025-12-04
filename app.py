import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION (La Truffe Branding) ---
st.set_page_config(
    page_title="La Truffe",
    page_icon="💎", # Ou 🍄 si tu préfères le côté littéral
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS LUXURY / DARK MODE ---
st.markdown("""
<style>
    /* Import de police élégante (Google Fonts) */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap');

    /* FOND GÉNÉRAL */
    .stApp {
        background-color: #0a0a0a; /* Noir très profond */
        color: #e0e0e0;
        font-family: 'Lato', sans-serif;
    }
    
    /* TITRES */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif; /* Police type "Luxe" */
        color: #d4af37 !important; /* Couleur OR */
        font-weight: 700;
    }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #333;
    }
    
    /* CARTES VOITURES (Style Carte de Crédit Black) */
    .truffle-card {
        background: linear-gradient(145deg, #1a1a1a, #141414);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 25px;
        border: 1px solid #333;
        box-shadow: 0 4px 15px rgba(0,0,0,0.7);
        transition: all 0.3s ease;
    }
    .truffle-card:hover {
        border-color: #d4af37; /* Bordure Or au survol */
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(212, 175, 55, 0.15); /* Ombre dorée légère */
    }
    
    /* PRIX & BADGES */
    .price-gold {
        font-family: 'Playfair Display', serif;
        font-size: 26px;
        color: #d4af37;
        font-weight: bold;
    }
    .badge-rare {
        background-color: rgba(212, 175, 55, 0.15); /* Fond or transparent */
        border: 1px solid #d4af37;
        color: #d4af37;
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 11px;
        letter-spacing: 1px;
        text-transform: uppercase;
        float: right;
    }
    .badge-standard {
        background-color: #222;
        color: #666;
        padding: 5px 12px;
        border-radius: 50px;
        font-size: 11px;
        float: right;
    }

    /* BOUTON */
    .stButton button {
        background-color: transparent;
        border: 1px solid #d4af37;
        color: #d4af37;
        border-radius: 4px;
        transition: 0.3s;
    }
    .stButton button:hover {
        background-color: #d4af37;
        color: black;
        border-color: #d4af37;
    }

    /* KPI BOXES */
    div[data-testid="stMetric"] {
        background-color: #111;
        border: 1px solid #222;
        border-radius: 0px; /* Carré pour faire sérieux */
        border-left: 3px solid #d4af37; /* Petite touche or */
    }
    label[data-testid="stMetricLabel"] {
        font-size: 14px;
        color: #888;
    }
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT DONNÉES ---
@st.cache_data
def charger_donnees():
    if not os.path.exists("annonces.csv"): return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    cols = ['prix', 'cote_argus', 'km', 'annee']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    
    # Algo "Le Flair"
    def flairer_truffe(row):
        # Calcul de la différence avec la cote
        diff = row['cote_argus'] - row['prix']
        # Score de "Rareté" (0 à 100)
        score = 50 + ((diff / row['cote_argus']) * 200)
        return min(100, max(0, int(score))), int(diff)

    res = df.apply(flairer_truffe, axis=1, result_type='expand')
    df['score'] = res[0]
    df['gain'] = res[1]
    
    return df

df = charger_donnees()

# --- SIDEBAR (Le Menu du Chef) ---
with st.sidebar:
    # TITRE LOGO
    st.markdown("<h1 style='text-align: center; color: #d4af37;'>LA TRUFFE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-style: italic; font-size: 12px; color: #666;'>Le flair de l'investisseur.</p>", unsafe_allow_html=True)
    
    st.write("") # Espace
    
    if st.button("👃 Flairer le marché", use_container_width=True):
        st.cache_data.clear(); st.rerun()
    
    st.write("---")
    
    # Filtres
    marques = ["Toutes"] + sorted(df['marque'].unique().tolist())
    f_marque = st.selectbox("Marque", marques)
    
    f_modele = "Tous"
    if f_marque != "Toutes":
        modeles = ["Tous"] + sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
        f_modele = st.selectbox("Modèle", modeles)
        
    st.write("")
    budget = st.slider("Budget Investissement", 10000, 200000, 80000, step=5000)
    
    st.write("---")
    pepite_only = st.checkbox("💎 Afficher uniquement les raretés")

# --- FILTRAGE ---
if df.empty: st.error("Base de données vide."); st.stop()

mask = (df['prix'] <= budget)
if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
if f_modele != "Tous": mask &= (df['modele'] == f_modele)
if pepite_only: mask &= (df['score'] >= 80)

df_final = df[mask].sort_values(by='score', ascending=False)

# --- KPI LUXE ---
c1, c2, c3 = st.columns(3)
c1.metric("Opportunités", len(df_final))
c2.metric("Ticket Moyen", f"{int(df_final['prix'].mean())} €" if not df_final.empty else "-")
best = df_final.iloc[0] if not df_final.empty else None
if best is not None:
    c3.metric("Plus Belle Truffe", f"Gain : {best['gain']} €")

st.write("")
st.subheader("Sélection du Jour")
st.write("")

# --- VUE LISTE (Design La Truffe) ---
if df_final.empty:
    st.info("Le marché est sec. Aucune truffe détectée avec ces critères.")
else:
    for i in range(0, len(df_final), 2): # 2 cartes par ligne pour faire plus "grand format"
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(df_final):
                row = df_final.iloc[i+j]
                with cols[j]:
                    # Logique Badge
                    badge_html = f'<span class="badge-rare">💎 Rareté ({row["score"]}/100)</span>' if row['score'] > 80 else '<span class="badge-standard">Standard</span>'
                    
                    st.markdown(f"""
                    <div class="truffle-card">
                        <div style="height: 200px; overflow: hidden; border-radius: 8px; margin-bottom: 15px;">
                            <img src="{row['img_url']}" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        {badge_html}
                        <h3 style="margin-top: 0; font-size: 20px;">{row['titre']}</h3>
                        <p style="color: #888; font-size: 14px; margin-bottom: 15px;">
                            {row['annee']} | {row['km']} km | {row['ville']} | <span style="color:#d4af37">Finition {row['finition']}</span>
                        </p>
                        
                        <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                            <div>
                                <span style="font-size: 12px; color: #555;">Valeur estimée: {row['cote_argus']} €</span><br>
                                <span class="price-gold">{row['prix']} €</span>
                            </div>
                            <div style="text-align: right;">
                                <span style="color: #238636; font-weight: bold; font-size: 14px;">Gain pot.: +{row['gain']} €</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.link_button("Examiner le lot", row['url'], use_container_width=True)