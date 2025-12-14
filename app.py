import streamlit as st
import pandas as pd
import os
import base64
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(page_title="La Truffe | Pro", page_icon="🍄", layout="wide")

# --- INITIALISATION ÉTAT ---
if 'page' not in st.session_state: st.session_state.page = 'radar'
if 'selected_car' not in st.session_state: st.session_state.selected_car = None

# --- CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');
    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    
    /* CARTE RADAR */
    .lc-card {
        background-color: #181b20; border: 1px solid #333; border-radius: 12px; margin-bottom: 25px; overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease; cursor: pointer;
    }
    .lc-card:hover { transform: translateY(-5px); border-color: #d4af37; }
    .lc-img-container { position: relative; height: 200px; width: 100%; }
    .lc-img { width: 100%; height: 100%; object-fit: cover; }
    .badge-gain { position: absolute; top: 10px; right: 10px; background-color: #00e676; color: #000; padding: 6px 12px; font-weight: 800; border-radius: 4px; }
    
    .lc-content { padding: 15px; }
    .lc-title { font-size: 18px; font-weight: 700; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .lc-meta { display: flex; justify-content: space-between; font-size: 12px; color: #aaa; margin-bottom: 5px; }
    .lc-price { font-size: 24px; font-weight: 800; color: #fff; }
    .source-badge { background: #333; padding: 2px 6px; border-radius: 4px; color: white; border: 1px solid #444; font-size: 10px;}
    
    /* PAGE FICHE */
    .fiche-container { background: #181b20; padding: 30px; border-radius: 15px; border: 1px solid #333; }
    .fiche-title { font-size: 32px; font-weight: 800; color: white; margin-bottom: 10px; }
    .fiche-price { font-size: 40px; font-weight: 800; color: #d4af37; }
    .fiche-desc { font-size: 16px; line-height: 1.6; color: #ccc; margin-top: 20px; background: #121418; padding: 20px; border-radius: 8px;}
    .opt-tag { display: inline-block; background: #2b2f36; padding: 5px 10px; border-radius: 5px; margin: 5px 5px 0 0; font-size: 13px; border: 1px solid #444; }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stMultiSelect>div>div>div { background-color: #1a1d21; color: white; }
</style>
""", unsafe_allow_html=True)

# --- ALGORITHME INTELLIGENCE COLLECTIVE ---
def calculer_cote_statistique(df):
    """
    Calcule la cote basée sur la moyenne du marché (LBC + AutoScout)
    """
    if df.empty: return df

    # 1. On crée des groupes : Marque + Modèle + Année
    # (C'est plus fiable que le titre exact qui varie trop)
    groupe = ['marque', 'modele', 'annee']
    
    # 2. On calcule le prix moyen par groupe
    # transform('mean') permet de remettre cette moyenne sur chaque ligne correspondante
    df['moyenne_marche'] = df.groupby(groupe)['prix'].transform('mean')
    
    # 3. On compte combien il y a de voitures dans le groupe
    df['nb_similaires'] = df.groupby(groupe)['prix'].transform('count')
    
    # 4. LOGIQUE HYBRIDE :
    # Si il y a au moins 2 voitures similaires -> On utilise la Statistique Réelle
    # Sinon -> On garde la cote simulée du CSV (pour éviter d'avoir Gain = 0 sur une voiture unique)
    
    def appliquer_cote_finale(row):
        if row['nb_similaires'] > 1:
            return int(row['moyenne_marche'])
        else:
            return row['cote_argus'] # Fallback sur la valeur du CSV

    df['cote_finale'] = df.apply(appliquer_cote_finale, axis=1)
    
    # 5. Recalcul du Gain
    df['gain'] = df['cote_finale'] - df['prix']
    
    return df

# --- FONCTIONS ---
def get_img_src(img_path):
    if str(img_path).startswith("http"): return img_path
    if os.path.exists(str(img_path)):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    return "https://via.placeholder.com/400x300?text=Image+Manquante"

@st.cache_data
def charger_donnees():
    if not os.path.exists("annonces.csv"): return pd.DataFrame()
    
    # Chargement
    df = pd.read_csv("annonces.csv")
    
    # Nettoyage & Conversion Numérique (Crucial pour les calculs)
    cols_num = ['prix', 'cote_argus', 'km', 'annee', 'chevaux']
    for c in cols_num: 
        # On force la conversion en nombre, on remplace les erreurs par 0
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(r'\D', '', regex=True), errors='coerce').fillna(0).astype(int)
    
    # --- APPLICATION DE L'INTELLIGENCE COLLECTIVE ---
    df = calculer_cote_statistique(df)
    
    return df

# Navigation
def go_to_fiche(row):
    st.session_state.selected_car = row
    st.session_state.page = 'fiche'

def go_to_radar():
    st.session_state.selected_car = None
    st.session_state.page = 'radar'

# --- VUE RADAR ---
def afficher_radar():
    df = charger_donnees()
    
    c1, c2 = st.columns([3, 1])
    c1.markdown("# 📡 RADAR <span style='color:#d4af37'>LIVE</span>", unsafe_allow_html=True)
    
    with st.expander("🔍 FILTRER LE MARCHÉ", expanded=True):
        if not df.empty:
            c_s, c_m, c_b = st.columns(3)
            sources = sorted(df['source'].astype(str).unique().tolist())
            f_source = c_s.multiselect("Sources", sources, default=sources)
            f_marque = c_m.selectbox("Marque", ["Toutes"] + sorted(df['marque'].unique().tolist()))
            budget = c_b.slider("Budget Max", 0, 300000, 300000, step=5000)

            mask = (df['prix'] <= budget) & (df['source'].isin(f_source))
            if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
            df_final = df[mask].sort_values(by='gain', ascending=False)
    
            st.write(f"**{len(df_final)} véhicules analysés** | *Intelligence Collective activée* 🧠")
    
    if not df_final.empty:
        for i in range(0, len(df_final), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(df_final):
                    row = df_final.iloc[i+j]
                    with cols[j]:
                        img_src = get_img_src(row['img_url'])
                        
                        # Affichage conditionnel de la fiabilité de la cote
                        nb_sim = row['nb_similaires']
                        info_cote = f"{nb_sim} vhc. comparables" if nb_sim > 1 else "Cote estimée"
                        
                        st.markdown(f"""
                        <div class="lc-card">
                            <div class="lc-img-container">
                                <img src="{img_src}" class="lc-img">
                                <div class="badge-gain">+{row['gain']} €</div>
                            </div>
                            <div class="lc-content">
                                <div class="lc-meta">
                                    <span class="source-badge">{row['source']}</span>
                                    <span style="color:#d4af37">🕒 {row['temps']}</span>
                                </div>
                                <div class="lc-title">{row['titre']}</div>
                                <div style="color:#888; font-size:13px; margin-bottom:5px;">
                                    {row['annee']} | {row['km']} km | {row['chevaux']} Ch
                                </div>
                                <div style="font-size:11px; color:#555;">📊 {info_cote}</div>
                                <div class="lc-price">{row['prix']} €</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        st.button("🔎 Détails", key=f"view_{row['id']}", on_click=go_to_fiche, args=(row,), use_container_width=True)

# --- VUE FICHE ---
def afficher_fiche(car):
    st.button("⬅ Retour au Radar", on_click=go_to_radar)
    st.markdown(f"<div class='fiche-title'>{car['titre']}</div>", unsafe_allow_html=True)
    
    col_img, col_infos = st.columns([1.5, 1])
    
    with col_img:
        st.image(get_img_src(car['img_url']), use_column_width=True)
        st.markdown("### 📝 Description")
        st.markdown(f"<div class='fiche-desc'>{car['description']}</div>", unsafe_allow_html=True)

    with col_infos:
        st.markdown(f"""
        <div style="background:#1a1d21; padding:20px; border-radius:10px; border:1px solid #333; margin-bottom:20px;">
            <div style="font-size:14px; color:#888;">PRIX DE VENTE</div>
            <div class="fiche-price">{car['prix']} €</div>
            <div style="color:#2ea043; font-weight:bold; font-size:20px; margin-top:5px;">
                Marge calculée : +{car['gain']} €
            </div>
            <div style="font-size:12px; color:#666; margin-top:5px;">
                Basé sur {car['nb_similaires']} véhicules similaires<br>
                Moyenne marché : {car['cote_finale']} €
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.link_button("🔗 VOIR L'ANNONCE ORIGINALE", str(car['lien_annonce']), use_container_width=True, type="primary")
        
        st.write("---")
        st.markdown("### ⚙️ Caractéristiques")
        c1, c2 = st.columns(2)
        c1.write(f"**Année:** {car['annee']}")
        c1.write(f"**Km:** {car['km']}")
        c1.write(f"**Boîte:** {car['boite']}")
        c2.write(f"**Énergie:** {car['carburant']}")
        c2.write(f"**Puissance:** {car['chevaux']}")
        c2.write(f"**Couleur:** {car['couleur']}")
        
        st.write("---")
        st.markdown("### ✨ Options")
        opts = str(car['options']).split(',')
        html = "".join([f"<span class='opt-tag'>{o.strip()}</span>" for o in opts if len(o)>2])
        st.markdown(html, unsafe_allow_html=True)

if st.session_state.page == 'radar': afficher_radar()
else: afficher_fiche(st.session_state.selected_car)