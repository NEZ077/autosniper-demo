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

# --- CSS STYLE "LA CENTRALE" (Dark Mode) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

    .stApp { background-color: #f4f4f4; color: #333; font-family: 'Roboto', sans-serif; }
    
    /* Si l'utilisateur est en mode sombre via Streamlit settings, on force un fond sombre propre */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0e1117; color: #e0e0e0; }
    }

    /* CARTE TYPE "LA CENTRALE" */
    .lc-card {
        background-color: #ffffff;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        overflow: hidden;
        border: 1px solid #e0e0e0;
        transition: transform 0.2s;
    }
    
    /* Mode sombre pour la carte */
    @media (prefers-color-scheme: dark) {
        .lc-card { background-color: #1e2126; border-color: #2e333d; }
    }

    .lc-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        border-color: #ff5252; /* Rouge La Centrale au survol */
    }

    /* IMAGE */
    .lc-img-container {
        position: relative;
        height: 200px;
        width: 100%;
    }
    .lc-img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    /* BADGES SUR L'IMAGE */
    .badge-corner {
        position: absolute;
        top: 10px;
        left: 10px;
        background-color: #ff5252; /* Rouge */
        color: white;
        padding: 4px 8px;
        font-size: 11px;
        font-weight: bold;
        border-radius: 4px;
        text-transform: uppercase;
        box-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .badge-score {
        position: absolute;
        bottom: 10px;
        right: 10px;
        background-color: rgba(0,0,0,0.8);
        color: #4caf50; /* Vert */
        padding: 4px 8px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
        border: 1px solid #4caf50;
    }

    /* CONTENU */
    .lc-content { padding: 15px; }

    .lc-title {
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .lc-subtitle {
        font-size: 14px;
        color: #888;
        margin-bottom: 15px;
    }

    /* PRIX & INFO */
    .lc-footer {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        margin-top: 10px;
        padding-top: 10px;
        border-top: 1px solid #eee;
    }
    
    @media (prefers-color-scheme: dark) {
        .lc-footer { border-top-color: #333; }
    }

    .lc-price {
        font-size: 24px;
        font-weight: 800;
        color: #ff5252; /* Rouge Prix */
    }
    
    .lc-cote {
        font-size: 12px;
        color: #2ea043; /* Vert gain */
        text-align: right;
        font-weight: bold;
    }

    /* OPTIONS (Tags propres) */
    .opt-tag {
        display: inline-block;
        font-size: 11px;
        background-color: #f0f2f6;
        color: #555;
        padding: 2px 6px;
        border-radius: 4px;
        margin-right: 4px;
        margin-bottom: 4px;
    }
    @media (prefers-color-scheme: dark) {
        .opt-tag { background-color: #2c3036; color: #aaa; }
    }

    /* Section Header Pépites */
    .pepite-header {
        font-size: 22px; 
        font-weight: bold; 
        margin-bottom: 20px; 
        border-left: 5px solid #d4af37; 
        padding-left: 15px;
    }
            
        /* Ajoute ça dans ton CSS existant */
    .market-box { background: #1a1d21; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #333; }
    .market-val { color: #2ea043; font-weight: bold; font-size: 14px; }
    .market-lbl { color: #666; font-size: 10px; text-transform: uppercase; }
    .logo-text { font-size: 26px; font-weight: 800; color: #d4af37; text-align: center; letter-spacing: 2px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# --- PAYWALL ---
@st.dialog("💎 Dossier Confidentiel")
def afficher_paywall(voiture_titre):
    st.subheader(voiture_titre)
    st.warning("🔒 Accès réservé aux membres.")
    st.write("Entrez votre email pour débloquer le lien vendeur et l'historique.")
    email = st.text_input("Email :", placeholder="moi@exemple.com")
    if st.button("Voir l'annonce", use_container_width=True):
        if "@" in email:
            st.success("Redirection...")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Email requis.")

# --- CHARGEMENT ---
@st.cache_data
def charger_donnees():
    if not os.path.exists("annonces.csv"): return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    cols = ['prix', 'cote_argus', 'km', 'annee']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    
    def algo_score(row):
        diff = row['cote_argus'] - row['prix']
        score = 50 + ((diff / row['cote_argus']) * 200)
        return min(100, max(0, int(score))), int(diff)

    res = df.apply(algo_score, axis=1, result_type='expand')
    df['score'] = res[0]
    df['gain'] = res[1]
    
    return df

df = charger_donnees()

# --- SIDEBAR ---
# --- NOUVELLE SIDEBAR COCKPIT ---
with st.sidebar:
    # 1. LOGO TEXTE (Remplace l'image carrée par une bannière texte classe)
    st.markdown('<div class="logo-text">LA TRUFFE</div>', unsafe_allow_html=True)

    # 2. NAVIGATION (Boutons radios stylés)
    menu = st.radio("Navigation", ["📡 Radar", "⭐ Favoris", "🔔 Alertes"], label_visibility="collapsed")
    
    st.write("---")

    # 3. MARKET PULSE (Remplissage visuel pro)
    st.caption("📊 TENDANCE MARCHÉ")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="market-box"><div class="market-val">↗ BULL</div><div class="market-lbl">Porsche</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="market-box"><div class="market-val">↘ BEAR</div><div class="market-lbl">Diesel</div></div>""", unsafe_allow_html=True)

    st.write("---")
    
    # 4. FILTRES DENSES (Ça remplit l'espace)
    st.header("🎯 Ciblage")
    
    if st.button("🔄 Scan Réseau", use_container_width=True): 
        st.cache_data.clear()
        st.rerun()

    if not df.empty:
        # Ligne 1 : Marque
        marques = ["Toutes"] + sorted(df['marque'].unique().tolist())
        f_marque = st.selectbox("Marque", marques)
        
        # Ligne 2 : Modèle
        mods = ["Tous"]
        if f_marque != "Toutes":
            mods += sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
        f_modele = st.selectbox("Modèle", mods)

        # Ligne 3 : Carburant & Boite (Cote à cote pour densifier)
        c_carb, c_boite = st.columns(2)
        f_carb = c_carb.selectbox("Carburant", ["Tous"] + sorted(df['carburant'].unique().tolist()))
        f_boite = c_boite.selectbox("Boîte", ["Toutes"] + sorted(df['boite'].unique().tolist()))

        # Sliders
        budget = st.slider("Budget Max", 10000, 200000, 80000, step=5000)
        
    st.write("---")
    
    # 5. PROFIL MEMBRE (En bas pour finir proprement)
    st.markdown("""
    <div style="background:#1a1d21; padding:12px; border-radius:8px; display:flex; align-items:center; border:1px solid #333;">
        <div style="background:#d4af37; width:35px; height:35px; border-radius:50%; margin-right:10px; display:flex; align-items:center; justify-content:center; color:black; font-weight:bold;">M</div>
        <div>
            <div style="font-size:13px; font-weight:bold; color:white;">Membre Invité</div>
            <div style="font-size:11px; color:#2ea043;">● Connecté</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- FILTRAGE ---
if df.empty: st.error("Aucune donnée. Lancez scraper.py"); st.stop()

mask = (df['prix'] <= budget)
if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
if f_modele != "Tous": mask &= (df['modele'] == f_modele)

df_final = df[mask].sort_values(by='score', ascending=False)

# --- 1. SECTION : LES DERNIÈRES PÉPITES (Top 3) ---
# On prend les 3 meilleures voitures avec un score > 80
df_pepites = df_final[df_final['score'] >= 80].head(3)

if not df_pepites.empty:
    st.markdown('<div class="pepite-header">🔥 Arrivages Pépites (Top Rentabilité)</div>', unsafe_allow_html=True)
    
    cols = st.columns(3)
    for i, (_, row) in enumerate(df_pepites.iterrows()):
        with cols[i]:
            # Nettoyage des options (on en prend 2 max)
            opt_list = str(row.get('options', '')).split('|')[:2]
            tags_html = "".join([f'<span class="opt-tag">{o.strip()}</span>' for o in opt_list])

            st.markdown(f"""
            <div class="lc-card">
                <div class="lc-img-container">
                    <img src="{row['img_url']}" class="lc-img">
                    <div class="badge-corner">SUPER DEAL</div>
                    <div class="badge-score">Score: {row['score']}/100</div>
                </div>
                <div class="lc-content">
                    <div class="lc-title">{row['titre']}</div>
                    <div class="lc-subtitle">{row['annee']} | {row['km']} km | {row['ville']}</div>
                    <div>{tags_html}</div>
                    <div class="lc-footer">
                        <div class="lc-price">{row['prix']} €</div>
                        <div class="lc-cote">Gain estimé<br>+{row['gain']} €</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔒 Voir", key=f"pep_{row['id']}", use_container_width=True):
                afficher_paywall(row['titre'])

    st.write("---") # Séparateur

# --- 2. SECTION : TOUTES LES ANNONCES ---
st.subheader(f"Toutes les annonces ({len(df_final)})")

if df_final.empty:
    st.info("Aucun résultat avec ces filtres.")
else:
    # Grille de 4 colonnes pour faire plus dense comme La Centrale
    for i in range(0, len(df_final), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(df_final):
                row = df_final.iloc[i+j]
                with cols[j]:
                    # Badge "Nouveau" ou "Top" selon le score
                    badge_txt = "TOP" if row['score'] > 75 else "OCCASION"
                    color_badge = "#d4af37" if row['score'] > 75 else "#555"
                    
                    # Options clean
                    opt_list = str(row.get('options', '')).split('|')[:2]
                    tags_html = "".join([f'<span class="opt-tag">{o.strip()}</span>' for o in opt_list])
                    
                    st.markdown(f"""
                    <div class="lc-card">
                        <div class="lc-img-container">
                            <img src="{row['img_url']}" class="lc-img">
                            <div class="badge-corner" style="background-color:{color_badge}">{badge_txt}</div>
                        </div>
                        <div class="lc-content">
                            <div class="lc-title">{row['titre']}</div>
                            <div class="lc-subtitle">{row['annee']} | {row['km']} km</div>
                            <div style="height:25px; overflow:hidden;">{tags_html}</div>
                            <div class="lc-footer">
                                <div class="lc-price" style="font-size:20px;">{row['prix']} €</div>
                                <div style="font-size:12px; color:#888;">Cote: {row['cote_argus']}€</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Détails", key=f"list_{row['id']}", use_container_width=True):
                        afficher_paywall(row['titre'])