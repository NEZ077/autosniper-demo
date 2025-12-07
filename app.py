import streamlit as st
import pandas as pd
import time
import os
from fpdf import FPDF

# --- CONFIGURATION ---
st.set_page_config(
    page_title="La Truffe | Trading Auto",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="collapsed" # On replie la sidebar au démarrage pour immersion totale
)

# --- CSS PRO & NETTOYAGE UI ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');

    /* 1. CACHER LE MENU STREAMLIT (Look App Native) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* FOND & TYPO */
    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #121418; border-right: 1px solid #2b2f36; }

    /* CARTE VOITURE */
    .lc-card {
        background-color: #181b20;
        border: 1px solid #333;
        border-radius: 12px;
        margin-bottom: 25px;
        overflow: hidden;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .lc-card:hover {
        transform: translateY(-5px);
        border-color: #d4af37;
        box-shadow: 0 10px 20px rgba(212, 175, 55, 0.1);
    }

    /* IMAGE & BADGES */
    .lc-img-container { position: relative; height: 180px; width: 100%; }
    .lc-img { width: 100%; height: 100%; object-fit: cover; }
    
    /* Badge Rentabilité (Le "Pute à clic" vert fluo) */
    .badge-gain {
        position: absolute; top: 10px; right: 10px;
        background-color: #00e676; color: #000;
        padding: 6px 12px; font-size: 14px; font-weight: 800;
        border-radius: 4px; box-shadow: 0 2px 10px rgba(0,230,118,0.4);
    }
    
    .badge-source {
        position: absolute; bottom: 10px; left: 10px;
        background-color: rgba(0,0,0,0.7); color: #fff;
        padding: 2px 6px; font-size: 10px; border-radius: 4px;
    }

    /* CONTENU */
    .lc-content { padding: 18px; }
    .lc-title { font-size: 18px; font-weight: 700; color: white; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .lc-subtitle { font-size: 13px; color: #888; margin-bottom: 12px; display: flex; align-items: center; gap: 10px;}

    /* PRIX & FOOTER */
    .lc-footer { 
        display: flex; justify-content: space-between; align-items: flex-end; 
        margin-top: 15px; padding-top: 15px; border-top: 1px solid #2b2f36; 
    }
    .lc-price { font-size: 24px; font-weight: 800; color: #fff; }
    .lc-cote { font-size: 12px; color: #666; text-align: right; }
    .lc-cote span { color: #d4af37; font-weight: bold; text-decoration: line-through;}

    /* TAGS OPTIONS */
    .opt-tag { background: #25282e; color: #aaa; padding: 3px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; }

    /* HEADER PÉPITES */
    .pepite-header { 
        font-size: 24px; font-weight: 800; margin-bottom: 25px; 
        background: linear-gradient(90deg, #d4af37, #fef9c3); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
</style>
""", unsafe_allow_html=True)

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
    pdf.cell(0, 10, f"Dossier Investisseur : {voiture['titre']}", 0, 1, 'L')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, f"Prix Achat : {voiture['prix']} EUR", 0, 1)
    pdf.cell(50, 10, f"Revante Estimée : {voiture['cote_argus']} EUR", 0, 1)
    gain = voiture['cote_argus'] - voiture['prix']
    pdf.set_text_color(34, 139, 34)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(50, 10, f"Marge Brute : +{gain} EUR", 0, 1)
    return pdf.output(dest='S').encode('latin-1')

# --- PAYWALL AGRESSIF (Capture de Leads) ---
@st.dialog("🔒 Accès Restreint")
def afficher_paywall(row):
    gain = row['cote_argus'] - row['prix']
    
    st.markdown(f"""
    <h3 style='text-align:center; color:#d4af37;'>Opportunité Détectée</h3>
    <p style='text-align:center; font-size:14px;'>Ce véhicule présente une marge potentielle immédiate de :</p>
    <h1 style='text-align:center; color:#00e676;'>+ {gain} €</h1>
    <hr>
    <p style='font-size:13px; color:#aaa;'>
    ⚠️ <b>Attention :</b> L'accès aux coordonnées vendeur est réservé aux membres fondateurs.
    <br>Nous ouvrons <b>10 nouvelles places</b> pour la Bêta cette semaine.
    </p>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Votre Email Pro :", placeholder="contact@garage.com")
    
    if st.button("Recevoir mon invitation prioritaire", use_container_width=True):
        if "@" in email:
            # Ici tu pourrais sauvegarder l'email dans un fichier
            time.sleep(1)
            pdf_data = creer_pdf(row)
            st.success("Dossier débloqué à titre exceptionnel.")
            st.download_button(
                label="📂 TÉLÉCHARGER LE DOSSIER PDF",
                data=pdf_data,
                file_name=f"Dossier_LaTruffe_{row['id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.warning("Email invalide.")

# --- CHARGEMENT ---
@st.cache_data
def charger_donnees():
    if not os.path.exists("annonces.csv"): return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    cols = ['prix', 'cote_argus', 'km', 'annee']
    for c in cols: df[c] = pd.to_numeric(df[c], errors='coerce')
    df['gain'] = df['cote_argus'] - df['prix']
    # Score de rareté pour le tri
    df['score'] = df.apply(lambda r: 50 + ((r['gain']) / r['cote_argus'] * 200), axis=1)
    return df

df = charger_donnees()

# --- HERO SECTION (Value Proposition Violente) ---
# Plus de "st.title" classique, on y va fort
st.markdown("""
<h1 style='font-size: 50px; font-weight: 800; margin-bottom: 0;'>LA TRUFFE <span style='font-size:30px'>🍄</span></h1>
<p style='font-size: 20px; color: #d4af37; margin-top: 0;'>Détecteur de Sous-Cotes Auto | <span style='color:#666'>Scan Temps Réel : Europe</span></p>
<div style='background: #1a1d21; padding: 15px; border-left: 4px solid #00e676; margin-bottom: 30px;'>
    <p style='margin:0; font-weight:bold; color: white;'>⚡ Ne ratez plus jamais une voiture vendue -20% sous le marché.</p>
    <p style='margin:0; font-size: 12px; color: #888;'>Algorithme connecté : Mobile.de, AutoScout24, LeBoncoin.</p>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown('<h2 style="color:#d4af37; text-align:center;">FILTRES</h2>', unsafe_allow_html=True)
    if st.button("🔄 Rafraîchir le Flux", use_container_width=True): st.cache_data.clear(); st.rerun()
    
    if not df.empty:
        f_marque = st.selectbox("Marque", ["Toutes"] + sorted(df['marque'].unique().tolist()))
        mods = ["Tous"]
        if f_marque != "Toutes": mods += sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
        f_modele = st.selectbox("Modèle", mods)
        f_carb = st.selectbox("Carburant", ["Tous"] + sorted(df['carburant'].unique().tolist()))
        budget = st.slider("Budget Achat Max", 5000, 200000, 80000, step=5000)

# --- LISTING ---
if df.empty: st.error("Initialisation du système..."); st.stop()

mask = (df['prix'] <= budget)
if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
if f_modele != "Tous": mask &= (df['modele'] == f_modele)
if f_carb != "Tous": mask &= (df['carburant'] == f_carb)

df_final = df[mask].sort_values(by='score', ascending=False)

# 1. TOP PÉPITES (Les plus gros gains)
df_pepites = df_final.head(3) # On prend les 3 meilleures absolues

if not df_pepites.empty:
    st.markdown('<div class="pepite-header">🔥 OPPORTUNITÉS IMMÉDIATES</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, (_, row) in enumerate(df_pepites.iterrows()):
        with cols[i]:
            opt_list = str(row.get('options', '')).split('|')[:2]
            tags_html = "".join([f'<span class="opt-tag">{o.strip()}</span>' for o in opt_list])
            
            st.markdown(f"""
            <div class="lc-card">
                <div class="lc-img-container">
                    <img src="{row['img_url']}" class="lc-img">
                    <div class="badge-gain">+{row['gain']} €</div>
                    <div class="badge-source">AutoScout24</div>
                </div>
                <div class="lc-content">
                    <div class="lc-title">{row['titre']}</div>
                    <div class="lc-subtitle">
                        <span>{row['annee']}</span> • <span>{row['km']} km</span> • <span>{row['boite']}</span>
                    </div>
                    <div style="height:25px; overflow:hidden;">{tags_html}</div>
                    <div class="lc-footer">
                        <div>
                            <div class="lc-price">{row['prix']} €</div>
                            <div class="lc-cote">Cote: <span>{row['cote_argus']} €</span></div>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔒 BLOQUER CE VÉHICULE", key=f"pep_{row['id']}", use_container_width=True):
                afficher_paywall(row)

st.write("---")

# 2. LISTE STANDARD
st.subheader(f"Flux Live ({len(df_final)} véhicules)")
if df_final.empty:
    st.info("Aucune opportunité détectée avec ces critères.")
else:
    for i in range(3, len(df_final), 4): # On commence après les pépites
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(df_final):
                row = df_final.iloc[i+j]
                with cols[j]:
                    opt_list = str(row.get('options', '')).split('|')[:2]
                    tags_html = "".join([f'<span class="opt-tag">{o.strip()}</span>' for o in opt_list])
                    
                    st.markdown(f"""
                    <div class="lc-card">
                        <div class="lc-img-container">
                            <img src="{row['img_url']}" class="lc-img">
                            <div class="badge-gain" style="font-size:12px; padding:4px 8px; background:#2ea043; color:white;">+{row['gain']} €</div>
                        </div>
                        <div class="lc-content">
                            <div class="lc-title" style="font-size:16px;">{row['titre']}</div>
                            <div class="lc-subtitle">{row['annee']} | {row['km']} km</div>
                            <div class="lc-footer">
                                <div class="lc-price" style="font-size:20px;">{row['prix']} €</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Analyser", key=f"lst_{row['id']}", use_container_width=True):
                        afficher_paywall(row)