import streamlit as st
import pandas as pd
import time
import os
import base64 # Indispensable pour tes photos locales
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(
    page_title="La Truffe | Pro",
    page_icon="🍄",
    layout="wide"
)

# --- CSS FULL SCREEN & STYLE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    
    .lc-card {
        background-color: #181b20; border: 1px solid #333; border-radius: 12px; margin-bottom: 25px; overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease;
    }
    .lc-card:hover { transform: translateY(-5px); border-color: #d4af37; }
    
    .lc-img-container { position: relative; height: 200px; width: 100%; }
    .lc-img { width: 100%; height: 100%; object-fit: cover; }
    
    .badge-gain {
        position: absolute; top: 10px; right: 10px; background-color: #00e676; color: #000;
        padding: 6px 12px; font-size: 14px; font-weight: 800; border-radius: 4px;
    }
    
    .lc-content { padding: 18px; }
    .lc-title { font-size: 18px; font-weight: 700; color: white; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .lc-subtitle { font-size: 13px; color: #888; margin-top:5px; margin-bottom: 12px; }
    .lc-footer { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px; border-top: 1px solid #2b2f36; padding-top: 10px;}
    .lc-price { font-size: 24px; font-weight: 800; color: #fff; }
    
    .market-box { background: #1a1d21; padding: 10px 20px; border-radius: 8px; border: 1px solid #333; display: flex; align-items: center; justify-content: space-between; }
    .market-val { color: #2ea043; font-weight: bold; }
    .main-header { font-size: 40px; font-weight: 800; color: white; text-align: center; margin-top: 20px;}
    .gold-text { color: #d4af37; }
    
    .stTextInput>div>div>input, .stSelectbox>div>div>div { background-color: #1a1d21; color: white; }
</style>
""", unsafe_allow_html=True)

# --- FONCTION MAGIQUE : IMAGE LOCALE -> HTML ---
def get_img_src(img_path):
    # Si c'est un lien internet, on le renvoie tel quel
    if img_path.startswith("http"):
        return img_path
    
    # Si c'est un fichier local (ex: 1.jpg)
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/jpeg;base64,{data}"
    
    # Si l'image n'est pas trouvée
    return "https://via.placeholder.com/400x300?text=Photo+Manquante"

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
    return pdf.output(dest='S').encode('latin-1')

# --- PAYWALL ---
@st.dialog("🔒 Dossier Investisseur")
def afficher_paywall(row):
    st.subheader(row['titre'])
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
    cols = ['prix', 'cote_argus', 'km', 'annee']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    df['gain'] = df['cote_argus'] - df['prix']
    df['score'] = df.apply(lambda r: 50 + ((r['gain']) / r['cote_argus'] * 200), axis=1)
    return df

df = charger_donnees()

# --- HEADER ---
c_logo, c_stats = st.columns([1, 2])
with c_logo: st.markdown('<div class="main-header">LA TRUFFE <span class="gold-text">🍄</span></div>', unsafe_allow_html=True)
with c_stats:
    st.write(""); st.write("")
    s1, s2, s3 = st.columns(3)
    s1.markdown('<div class="market-box"><span>Tendance</span><span class="market-val">↗ BULL</span></div>', unsafe_allow_html=True)
    s2.markdown('<div class="market-box"><span>Opportunités</span><span class="market-val" style="color:#d4af37">10</span></div>', unsafe_allow_html=True)
    s3.markdown('<div class="market-box"><span>Scan</span><span style="color:#666">Actif ●</span></div>', unsafe_allow_html=True)

st.write("---")

# --- LISTING ---
tab1, tab2 = st.tabs(["📡 RADAR", "⭐ FAVORIS"])

with tab1:
    with st.expander("🔍 FILTRER", expanded=True):
        if st.button("🔄 Reset"): st.rerun()

    if df.empty: 
        st.error("Données vides. Lancez 'python scraper.py'")
    else:
        st.markdown(f"### 🎯 {len(df)} véhicules détectés")
        
        # Grille 3 colonnes
        for i in range(0, len(df), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(df):
                    row = df.iloc[i+j]
                    with cols[j]:
                        # --- C'EST ICI QUE LA MAGIE OPÈRE ---
                        # On transforme le nom de fichier (1.jpg) en code image affichable
                        img_source = get_img_src(row['img_url'])
                        
                        st.markdown(f"""
                        <div class="lc-card">
                            <div class="lc-img-container">
                                <img src="{img_source}" class="lc-img">
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
                        
                        if st.button("🔒 Analyser", key=f"btn_{row['id']}", use_container_width=True):
                            afficher_paywall(row)