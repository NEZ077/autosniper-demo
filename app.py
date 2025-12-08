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
    initial_sidebar_state="collapsed"
)

# --- 1. SIMULATION LIVE (TOASTS) ---
if 'init' not in st.session_state:
    st.session_state.init = True
    # On simule un délai de chargement pour faire "Vrai"
    time.sleep(0.5)
    st.toast('🟢 Connexion sécurisée aux serveurs Leboncoin...', icon='📡')
    time.sleep(0.8)
    st.toast('🟢 Connexion sécurisée aux serveurs AutoScout24...', icon='📡')
    time.sleep(0.8)
    st.toast('🚀 3 nouvelles opportunités détectées en temps réel !', icon='🔥')

# --- CSS PRO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;800&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    
    /* STYLE DES INPUTS */
    .stTextInput>div>div>input { color: white; background-color: #1a1d21; }
    .stSelectbox>div>div>div { background-color: #1a1d21; color: white; }
    
    /* CARTE */
    .lc-card {
        background-color: #181b20; border: 1px solid #333; border-radius: 12px; margin-bottom: 25px; overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3); transition: all 0.3s ease;
    }
    .lc-card:hover { transform: translateY(-5px); border-color: #d4af37; box-shadow: 0 10px 20px rgba(212, 175, 55, 0.15); }

    /* IMAGE */
    .lc-img-container { position: relative; height: 180px; width: 100%; }
    .lc-img { width: 100%; height: 100%; object-fit: cover; }
    
    .badge-gain {
        position: absolute; top: 10px; right: 10px; background-color: #00e676; color: #000;
        padding: 6px 12px; font-size: 14px; font-weight: 800; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,230,118,0.4);
    }
    
    .badge-info {
        position: absolute; bottom: 10px; left: 10px; background-color: rgba(0,0,0,0.8); color: #fff;
        padding: 3px 8px; font-size: 10px; border-radius: 4px; border: 1px solid #555;
    }

    /* CONTENU */
    .lc-content { padding: 15px; }
    .lc-title { font-size: 18px; font-weight: 700; color: white; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .lc-subtitle { font-size: 13px; color: #888; margin-bottom: 12px; display: flex; align-items: center; gap: 10px; flex-wrap: wrap;}
    
    .lc-footer { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px; padding-top: 15px; border-top: 1px solid #2b2f36; }
    .lc-price { font-size: 24px; font-weight: 800; color: #fff; }
    .lc-cote { font-size: 12px; color: #666; text-align: right; }
    .lc-cote span { color: #d4af37; font-weight: bold; text-decoration: line-through;}

    .opt-tag { background: #25282e; color: #aaa; padding: 3px 8px; border-radius: 4px; font-size: 11px; margin-right: 5px; }
    .pepite-header { font-size: 22px; font-weight: 800; margin-bottom: 20px; color: #d4af37; }
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
    pdf.cell(50, 10, f"Prix : {voiture['prix']} EUR", 0, 1)
    pdf.cell(50, 10, f"Cote : {voiture['cote_argus']} EUR", 0, 1)
    gain = voiture['cote_argus'] - voiture['prix']
    pdf.set_text_color(34, 139, 34)
    pdf.cell(50, 10, f"Marge : +{gain} EUR", 0, 1)
    return pdf.output(dest='S').encode('latin-1')

# --- PAYWALL AGRESSIF ---
@st.dialog("🔒 Accès Restreint")
def afficher_paywall(row):
    gain = row['cote_argus'] - row['prix']
    st.markdown(f"""
    <h3 style='text-align:center; color:#d4af37;'>Marge Immédiate : + {gain} €</h3>
    <hr>
    <p style='font-size:14px;'>🔒 <b>Accès Réservé aux Membres Fondateurs.</b></p>
    <p style='font-size:13px; color:#aaa;'>Nous ouvrons <b>10 nouvelles places</b> pour la Bêta cette semaine.<br>Laissez votre email pour recevoir votre invitation.</p>
    """, unsafe_allow_html=True)
    
    email = st.text_input("Votre Email Pro :")
    if st.button("Obtenir mon accès prioritaire", use_container_width=True):
        if "@" in email:
            time.sleep(1)
            pdf_data = creer_pdf(row)
            st.success("Accès validé.")
            st.download_button("📂 TÉLÉCHARGER LE DOSSIER", data=pdf_data, file_name=f"Dossier_{row['id']}.pdf", mime="application/pdf", use_container_width=True)

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

# --- HERO HEADER ---
st.markdown("""
<div style="margin-bottom:20px;">
    <h1 style='font-size: 32px; font-weight: 800; margin: 0; color:white;'>LA TRUFFE <span style='font-size:24px'>🍄</span></h1>
    <p style='font-size: 14px; color: #d4af37; margin: 0;'>Détecteur de Sous-Cotes | <span style='color:#666'>Europe (Scan Live)</span></p>
</div>
""", unsafe_allow_html=True)

# --- FILTRES (EXPANDER) ---
with st.expander("🔍 CONFIGURER LE SCAN (Localisation, Budget...)", expanded=True):
    if st.button("🔄 Lancer un nouveau scan", use_container_width=True): 
        st.cache_data.clear()
        st.rerun()
    
    if not df.empty:
        c1, c2, c3 = st.columns(3)
        marques = ["Toutes"] + sorted(df['marque'].unique().tolist())
        f_marque = c1.selectbox("Marque", marques)
        
        mods = ["Tous"]
        if f_marque != "Toutes": mods += sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
        f_modele = c2.selectbox("Modèle", mods)
        f_couleur = c3.multiselect("Couleur", sorted(df['couleur'].unique().tolist()), default=[])

        st.write("---")
        c4, c5 = st.columns(2)
        range_prix = c4.slider("Budget (€)", 10000, 200000, (20000, 120000), step=1000)
        range_km = c5.slider("Kilométrage", 0, 150000, (0, 90000), step=5000)
        f_rayon = st.slider("📍 Rayon de recherche", 10, 500, 200, format="%d km")

# --- LISTING ---
if df.empty: st.error("Données en cours de chargement..."); st.stop()

mask = (df['prix'] >= range_prix[0]) & (df['prix'] <= range_prix[1])
mask &= (df['km'] >= range_km[0]) & (df['km'] <= range_km[1])
mask &= (df['distance'] <= f_rayon)
if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
if f_modele != "Tous": mask &= (df['modele'] == f_modele)
if f_couleur: mask &= (df['couleur'].isin(f_couleur))

df_final = df[mask].sort_values(by='score', ascending=False)

# --- 2. BARRE DE STATUT (REASSURANCE) ---
st.markdown(f"""
    <div style="background-color: #1a1d21; padding: 10px; border-radius: 5px; border-left: 4px solid #d4af37; margin-bottom: 20px; border: 1px solid #333;">
        <p style="margin:0; color: #ccc; font-size:13px;">
        ⚡ <strong>Scan en cours :</strong> {f_marque if f_marque != 'Toutes' else 'Global'} | 
        <strong>Cible :</strong> {len(df_final)} véhicules détectés | 
        <strong>Latence :</strong> 0.4s
        </p>
    </div>
""", unsafe_allow_html=True)

if df_final.empty:
    st.info("Aucun véhicule trouvé dans ce rayon.")
else:
    # PÉPITES
    st.markdown('<div class="pepite-header">🔥 TOP OPPORTUNITÉS</div>', unsafe_allow_html=True)
    df_pepites = df_final.head(3)
    
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
                    <div class="badge-info">{row['distance']} km • {row['chevaux']} Ch</div>
                </div>
                <div class="lc-content">
                    <div class="lc-title">{row['titre']}</div>
                    <div class="lc-subtitle">
                        <span>{row['annee']}</span> • <span>{row['km']} km</span> • <span>{row['couleur']}</span>
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
            if st.button("🔒 BLOQUER LE VÉHICULE", key=f"pep_{row['id']}", use_container_width=True):
                afficher_paywall(row)

    # RESTE
    st.write("---")
    st.subheader("Flux Live")
    for i in range(3, len(df_final), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(df_final):
                row = df_final.iloc[i+j]
                with cols[j]:
                    st.markdown(f"""
                    <div class="lc-card">
                        <div class="lc-img-container">
                            <img src="{row['img_url']}" class="lc-img">
                            <div class="badge-gain" style="font-size:12px; padding:4px 8px; background:#2ea043; color:white;">+{row['gain']} €</div>
                        </div>
                        <div class="lc-content">
                            <div class="lc-title" style="font-size:16px;">{row['titre']}</div>
                            <div class="lc-subtitle">{row['annee']} | {row['chevaux']} Ch | {row['couleur']}</div>
                            <div class="lc-footer">
                                <div class="lc-price" style="font-size:20px;">{row['prix']} €</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("Voir", key=f"lst_{row['id']}", use_container_width=True):
                        afficher_paywall(row)