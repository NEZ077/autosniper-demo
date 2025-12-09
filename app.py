import streamlit as st
import pandas as pd
import time
import os
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(
    page_title="La Truffe | Pro",
    page_icon="🍄",
    layout="wide"
)

# --- ANCRE POUR LE RETOUR EN HAUT ---
st.markdown('<div id="top_page"></div>', unsafe_allow_html=True)

# --- CSS FULL SCREEN & BOUTON FLOTTANT ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');
    
    /* SUPPRESSION DU MENU STREAMLIT PAR DÉFAUT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* FOND & TYPO */
    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    
    /* BOUTON RETOUR HAUT (Flèche Flottante) */
    .floating-arrow {
        position: fixed;
        bottom: 30px;
        right: 30px;
        background-color: #d4af37;
        color: black;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        text-align: center;
        line-height: 50px;
        font-size: 24px;
        cursor: pointer;
        z-index: 9999;
        box-shadow: 0 4px 10px rgba(212, 175, 55, 0.4);
        text-decoration: none;
        transition: transform 0.2s;
    }
    .floating-arrow:hover {
        transform: scale(1.1);
        color: black;
    }

    /* MARKET BOXES (Haut de page) */
    .market-box { 
        background: #1a1d21; padding: 10px 20px; border-radius: 8px; 
        border: 1px solid #333; display: flex; align-items: center; justify-content: space-between;
    }
    .market-val { color: #2ea043; font-weight: bold; }
    
    /* CARTE */
    .lc-card {
        background-color: #181b20; border: 1px solid #333; border-radius: 12px; margin-bottom: 25px; overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease;
    }
    .lc-card:hover { transform: translateY(-5px); border-color: #d4af37; }

    .lc-img-container { position: relative; height: 200px; width: 100%; }
    .lc-img { width: 100%; height: 100%; object-fit: cover; }
    
    .badge-gain {
        position: absolute; top: 10px; right: 10px; background-color: #00e676; color: #000;
        padding: 6px 12px; font-size: 14px; font-weight: 800; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,230,118,0.4);
    }
    
    .lc-content { padding: 18px; }
    .lc-title { font-size: 18px; font-weight: 700; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .lc-subtitle { font-size: 13px; color: #888; margin-top:5px; margin-bottom: 12px; }
    
    .lc-footer { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px; padding-top: 15px; border-top: 1px solid #2b2f36; }
    .lc-price { font-size: 24px; font-weight: 800; color: #fff; }
    
    /* HEADER */
    .main-header { font-size: 40px; font-weight: 800; color: white; text-align: center; margin-top: 20px;}
    .gold-text { color: #d4af37; }
    
    /* Inputs */
    .stTextInput>div>div>input { background-color: #1a1d21; color: white; }
    .stSelectbox>div>div>div { background-color: #1a1d21; color: white; }
</style>
""", unsafe_allow_html=True)

# --- BOUTON FLOTTANT HTML ---
st.markdown('<a href="#top_page" class="floating-arrow" title="Remonter">⬆</a>', unsafe_allow_html=True)

# --- MOTEUR PDF ---
def creer_pdf(voiture):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_fill_color(20, 20, 20)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 25, "LA TRUFFE", 0, 1, 'C')
    pdf.ln(20)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Dossier : {voiture['titre']}", 0, 1, 'L')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, f"Prix : {voiture['prix']} EUR", 0, 1)
    pdf.cell(50, 10, f"Cote : {voiture['cote_argus']} EUR", 0, 1)
    gain = voiture['cote_argus'] - voiture['prix']
    pdf.set_text_color(34, 139, 34)
    pdf.cell(50, 10, f"Marge : +{gain} EUR", 0, 1)
    return pdf.output(dest='S').encode('latin-1')

# --- PAYWALL ---
@st.dialog("🔒 Dossier Investisseur")
def afficher_paywall(row):
    st.subheader(f"Opportunité : {row['titre']}")
    st.info("Cette fiche est réservée aux membres.")
    email = st.text_input("Email Pro :")
    if st.button("Télécharger PDF", use_container_width=True):
        if "@" in email:
            time.sleep(1)
            pdf_data = creer_pdf(row)
            st.success("Validé.")
            st.download_button("📂 TÉLÉCHARGER", data=pdf_data, file_name=f"Dossier_{row['id']}.pdf", mime="application/pdf", use_container_width=True)

# --- CHARGEMENT ---
@st.cache_data
def charger_donnees():
    if not os.path.exists("annonces.csv"): return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    cols = ['prix', 'cote_argus', 'km', 'annee', 'distance', 'chevaux']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    df['gain'] = df['cote_argus'] - df['prix']
    df['score'] = df.apply(lambda r: 50 + ((r['gain']) / r['cote_argus'] * 200), axis=1)
    return df

df = charger_donnees()

# --- HEADER & MARKET PULSE (En haut) ---
c_logo, c_stats = st.columns([1, 2])

with c_logo:
    st.markdown('<div class="main-header">LA TRUFFE <span class="gold-text">🍄</span></div>', unsafe_allow_html=True)

with c_stats:
    st.write("") # Spacer
    st.write("")
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="market-box"><span>Tendance</span><span class="market-val">↗ BULL</span></div>', unsafe_allow_html=True)
    s2.markdown('<div class="market-box"><span>Opportunités</span><span class="market-val" style="color:#d4af37">142</span></div>', unsafe_allow_html=True)
    s3.markdown('<div class="market-box"><span>Scan</span><span style="color:#666">Actif ●</span></div>', unsafe_allow_html=True)

st.write("---")

# --- NAVIGATION ONGLET ---
tab1, tab2, tab3 = st.tabs(["📡 RADAR (Recherche)", "⭐ FAVORIS", "⚙️ CONFIGURATION"])

with tab1:
    # --- ZONE DE FILTRES (DÉPLIANT EN HAUT) ---
    with st.expander("🔍 FILTRER LES RÉSULTATS", expanded=True):
        if st.button("🔄 Lancer un nouveau scan", use_container_width=True): 
            st.cache_data.clear()
            st.rerun()
        
        if not df.empty:
            c1, c2, c3, c4 = st.columns(4)
            marques = ["Toutes"] + sorted(df['marque'].unique().tolist())
            f_marque = c1.selectbox("Marque", marques)
            
            mods = ["Tous"]
            if f_marque != "Toutes": mods += sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
            f_modele = c2.selectbox("Modèle", mods)
            
            f_carb = c3.selectbox("Carburant", ["Tous"] + sorted(df['carburant'].unique().tolist()))
            f_boite = c4.selectbox("Boîte", ["Toutes"] + sorted(df['boite'].unique().tolist()))

            c5, c6, c7 = st.columns(3)
            budget = c5.slider("Budget Max (€)", 5000, 300000, 80000, step=1000)
            kms = c6.slider("Km Max", 0, 200000, 100000, step=5000)
            f_rayon = c7.slider("Rayon (km)", 10, 500, 100)

    # --- LISTING ---
    if df.empty: 
        st.error("Données vides. Lancez 'python scraper.py'")
    else:
        # Filtrage
        mask = (df['prix'] <= budget) & (df['km'] <= kms) & (df['distance'] <= f_rayon)
        if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
        if f_modele != "Tous": mask &= (df['modele'] == f_modele)
        if f_carb != "Tous": mask &= (df['carburant'] == f_carb)
        if f_boite != "Toutes": mask &= (df['boite'] == f_boite)
        
        df_final = df[mask].sort_values(by='score', ascending=False)
        
        st.markdown(f"### 🎯 {len(df_final)} véhicules détectés")
        
        if df_final.empty:
            st.info("Aucun résultat. Élargissez vos filtres.")
        else:
            # Grille 3 colonnes
            for i in range(0, len(df_final), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(df_final):
                        row = df_final.iloc[i+j]
                        with cols[j]:
                            # Carte
                            st.markdown(f"""
                            <div class="lc-card">
                                <div class="lc-img-container">
                                    <img src="{row['img_url']}" class="lc-img">
                                    <div class="badge-gain">+{row['gain']} €</div>
                                </div>
                                <div class="lc-content">
                                    <div class="lc-title">{row['titre']}</div>
                                    <div class="lc-subtitle">
                                        {row['annee']} | {row['km']} km | {row['chevaux']} Ch
                                    </div>
                                    <div class="lc-footer">
                                        <div>
                                            <div class="lc-price">{row['prix']} €</div>
                                            <div style="font-size:11px; color:#888;">Cote: {row['cote_argus']} €</div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Bouton Action
                            if st.button("🔒 Analyser", key=f"btn_{row['id']}", use_container_width=True):
                                afficher_paywall(row)

with tab2:
    st.info("Vos véhicules favoris apparaîtront ici.")

with tab3:
    st.write("Paramètres de l'application (Devise, Notifications, etc.)")