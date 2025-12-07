import streamlit as st
import pandas as pd
import time
import os

# --- CONFIGURATION ---
st.set_page_config(
    page_title="La Truffe",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PREMIUM V2 ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700&display=swap');

    .stApp { background-color: #0a0a0a; color: #e0e0e0; font-family: 'Lato', sans-serif; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #111; border-right: 1px solid #222; }
    
    /* Carte Voiture */
    .truffle-card {
        background: #141414;
        border: 1px solid #333;
        border-radius: 12px;
        padding: 0; /* Padding 0 pour que l'image colle aux bords */
        overflow: hidden;
        margin-bottom: 20px;
        transition: transform 0.2s;
    }
    .truffle-card:hover {
        border-color: #d4af37;
        transform: translateY(-3px);
    }
    
    /* Contenu Carte */
    .card-content { padding: 15px; }
    
    /* Titres et Textes */
    .card-title { font-size: 18px; font-weight: bold; color: white; margin-bottom: 5px; }
    .card-sub { font-size: 13px; color: #888; margin-bottom: 10px; }
    .card-price { font-size: 22px; color: #d4af37; font-weight: bold; }
    
    /* Badges Options (C'est ça qui remplace le code bizarre) */
    .option-tag {
        display: inline-block;
        background-color: #222;
        color: #aaa;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 10px;
        margin-right: 5px;
        margin-bottom: 5px;
        border: 1px solid #333;
    }
    
    /* Badge Rentabilité */
    .badge-gain {
        background-color: rgba(35, 134, 54, 0.2);
        color: #2ea043;
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        float: right;
    }
    
    /* Image */
    .card-img { width: 100%; height: 180px; object-fit: cover; }
</style>
""", unsafe_allow_html=True)

# --- PAYWALL (Capture Email) ---
@st.dialog("💎 Rejoindre le Cercle Privé")
def afficher_paywall(voiture_titre):
    st.markdown(f"**{voiture_titre}**")
    st.info("🔒 Cette opportunité est réservée aux membres.")
    email = st.text_input("Votre Email :", placeholder="exemple@mail.com")
    if st.button("Accéder au dossier", use_container_width=True):
        if "@" in email:
            st.success("Accès autorisé. Redirection...")
            time.sleep(2)
            st.rerun()
        else:
            st.error("Email invalide.")

# --- CHARGEMENT ---
@st.cache_data
def charger_donnees():
    if not os.path.exists("annonces.csv"): return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    cols = ['prix', 'cote_argus', 'km', 'annee']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    
    def score_algo(row):
        diff = row['cote_argus'] - row['prix']
        score = 50 + ((diff / row['cote_argus']) * 200)
        return min(100, max(0, int(score))), int(diff)

    res = df.apply(score_algo, axis=1, result_type='expand')
    df['score'] = res[0]
    df['gain'] = res[1]
    return df

df = charger_donnees()

# --- SIDEBAR (Filtres Massifs) ---
with st.sidebar:
    st.sidebar.image("logo.png", width=200)
    st.header("💎 La Truffe")
    if st.button("🔄 Reload"): st.cache_data.clear(); st.rerun()
    st.write("---")
    
    # 1. Marque (Toutes les 50 marques sont là)
    all_marques = ["Toutes"] + sorted(df['marque'].unique().tolist())
    f_marque = st.selectbox("Marque", all_marques)
    
    # 2. Modèle (Adaptatif)
    f_modele = "Tous"
    if f_marque != "Toutes":
        mods = ["Tous"] + sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
        f_modele = st.selectbox("Modèle", mods)
        
    st.write("")
    budget = st.slider("Budget Max", 5000, 200000, 60000, step=1000)
    pepite = st.checkbox("💎 Pépites uniquement")

# --- FILTRAGE ---
if df.empty: st.error("Lancez scraper.py !"); st.stop()

mask = (df['prix'] <= budget)
if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
if f_modele != "Tous": mask &= (df['modele'] == f_modele)
if pepite: mask &= (df['score'] >= 80)

df_final = df[mask].sort_values(by='score', ascending=False)

# --- KPI ---
c1, c2, c3 = st.columns(3)
c1.metric("Résultats", len(df_final))
c2.metric("Prix Moyen", f"{int(df_final['prix'].mean())} €" if not df_final.empty else "-")
top_gain = df_final['gain'].max() if not df_final.empty else 0
c3.metric("Meilleur Gain", f"+{top_gain} €")

st.write("")

# --- AFFICHAGE GRILLE ---
if df_final.empty:
    st.info("Aucun véhicule trouvé.")
else:
    # Grille de 3 colonnes
    for i in range(0, len(df_final), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(df_final):
                row = df_final.iloc[i+j]
                with cols[j]:
                    
                    # Construction des badges d'options (HTML propre)
                    # On récupère la chaine "GPS | Cuir" et on la coupe
                    options_list = str(row.get('options', 'Standard')).split('|')
                    options_html = ""
                    for opt in options_list[:3]: # On affiche max 3 options pour pas surcharger
                        options_html += f'<span class="option-tag">{opt.strip()}</span>'
                    
                    gain_html = f'<span class="badge-gain">+{row["gain"]}€</span>' if row['gain'] > 0 else ""

                    st.markdown(f"""
                    <div class="truffle-card">
                        <img src="{row['img_url']}" class="card-img">
                        <div class="card-content">
                            {gain_html}
                            <div class="card-title">{row['titre']}</div>
                            <div class="card-sub">{row['annee']} | {row['km']} km | {row['ville']}</div>
                            <div style="margin-bottom:10px;">
                                {options_html}
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                                <span class="card-price">{row['prix']} €</span>
                                <span style="font-size:12px; color:#555;">Cote: {row['cote_argus']}€</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🔒 Voir le dossier", key=f"b_{row['id']}", use_container_width=True):
                        afficher_paywall(row['titre'])