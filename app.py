import streamlit as st
import pandas as pd
import time
import os
from fpdf import FPDF  # <--- INDISPENSABLE POUR LE PDF

# --- CONFIGURATION ---
st.set_page_config(
    page_title="La Truffe",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS STYLE (Cockpit + La Centrale) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;500;700&display=swap');

    .stApp { background-color: #0d0f12; color: #e0e0e0; font-family: 'Outfit', sans-serif; }
    
    /* SIDEBAR */
    section[data-testid="stSidebar"] { background-color: #121418; border-right: 1px solid #2b2f36; }
    .logo-text { font-size: 26px; font-weight: 800; color: #d4af37; text-align: center; letter-spacing: 2px; margin-bottom: 20px;}
    .market-box { background: #1a1d21; padding: 10px; border-radius: 6px; text-align: center; border: 1px solid #333; }
    .market-val { color: #2ea043; font-weight: bold; font-size: 14px; }
    .market-lbl { color: #666; font-size: 10px; text-transform: uppercase; }

    /* CARTE TYPE "LA CENTRALE" DARK */
    .lc-card {
        background-color: #181b20;
        border: 1px solid #2b2f36;
        border-radius: 8px;
        margin-bottom: 20px;
        overflow: hidden;
        transition: transform 0.2s;
    }
    .lc-card:hover {
        transform: translateY(-3px);
        border-color: #d4af37;
    }

    /* IMAGE & BADGES */
    .lc-img-container { position: relative; height: 180px; width: 100%; }
    .lc-img { width: 100%; height: 100%; object-fit: cover; }
    
    .badge-corner {
        position: absolute; top: 10px; left: 10px;
        background-color: #d4af37; color: black;
        padding: 4px 8px; font-size: 10px; font-weight: bold;
        border-radius: 4px; text-transform: uppercase;
    }
    .badge-score {
        position: absolute; bottom: 10px; right: 10px;
        background-color: rgba(0,0,0,0.8); color: #2ea043;
        padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: bold; border: 1px solid #2ea043;
    }

    /* CONTENU */
    .lc-content { padding: 15px; }
    .lc-title { font-size: 16px; font-weight: 700; color: white; margin-bottom: 5px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .lc-subtitle { font-size: 13px; color: #888; margin-bottom: 10px; }

    /* PRIX & FOOTER */
    .lc-footer { display: flex; justify-content: space-between; align-items: flex-end; margin-top: 10px; padding-top: 10px; border-top: 1px solid #2b2f36; }
    .lc-price { font-size: 22px; font-weight: 800; color: #d4af37; }
    .lc-cote { font-size: 11px; color: #2ea043; text-align: right; font-weight: bold; }

    /* TAGS */
    .opt-tag { display: inline-block; font-size: 10px; background-color: #25282e; color: #999; padding: 2px 6px; border-radius: 4px; margin-right: 4px; }

    /* HEADER PÉPITES */
    .pepite-header { font-size: 20px; font-weight: bold; margin-bottom: 20px; border-left: 4px solid #d4af37; padding-left: 15px; color: white; }
</style>
""", unsafe_allow_html=True)

# --- MOTEUR PDF ---
def creer_pdf(voiture):
    pdf = FPDF()
    pdf.add_page()
    
    # Design Luxe Noir & Or sur PDF
    pdf.set_fill_color(20, 20, 20)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_font("Arial", 'B', 24)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 25, "LA TRUFFE", 0, 1, 'C')
    pdf.set_font("Arial", 'I', 10)
    pdf.set_text_color(200, 200, 200)
    pdf.cell(0, -10, "RAPPORT D'INVESTISSEMENT AUTOMOBILE", 0, 1, 'C')
    pdf.ln(20)
    
    # Titre
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, f"Dossier : {voiture['titre']}", 0, 1, 'L')
    pdf.line(10, 55, 200, 55)
    
    # Données
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    pdf.cell(50, 10, f"Prix Vendeur : {voiture['prix']} EUR", 0, 1)
    pdf.cell(50, 10, f"Cote Estimee : {voiture['cote_argus']} EUR", 0, 1)
    
    gain = voiture['cote_argus'] - voiture['prix']
    pdf.set_font("Arial", 'B', 12)
    pdf.set_text_color(34, 139, 34) if gain > 0 else pdf.set_text_color(200, 0, 0)
    pdf.cell(50, 10, f"Marge Potentielle : {gain} EUR", 0, 1)
    
    # Détails
    pdf.ln(10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 11)
    pdf.cell(0, 10, f"Configuration : {voiture['annee']} | {voiture['km']} km | {voiture['carburant']} | {voiture['boite']}", 0, 1)
    pdf.multi_cell(0, 10, f"Options : {voiture['options']}")
    
    return pdf.output(dest='S').encode('latin-1')

# --- PAYWALL PDF ---
@st.dialog("💎 Club Privé")
def afficher_paywall(row):
    st.subheader(row['titre'])
    st.info("🔒 Entrez votre email pour télécharger le rapport PDF complet.")
    email = st.text_input("Email membre :", placeholder="client@email.com")
    
    if st.button("Valider et Télécharger", use_container_width=True):
        if "@" in email:
            pdf_data = creer_pdf(row)
            st.success("Accès autorisé.")
            st.download_button(
                label="📄 TÉLÉCHARGER LE DOSSIER",
                data=pdf_data,
                file_name=f"Dossier_LaTruffe_{row['id']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
        else:
            st.error("Email invalide.")

# --- CHARGEMENT DONNÉES ---
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

# --- SIDEBAR COCKPIT ---
with st.sidebar:
    st.markdown('<div class="logo-text">LA TRUFFE</div>', unsafe_allow_html=True)
    menu = st.radio("Navigation", ["📡 Radar", "⭐ Favoris", "🔔 Alertes"], label_visibility="collapsed")
    st.write("---")
    
    st.caption("📊 TENDANCE MARCHÉ")
    c1, c2 = st.columns(2)
    with c1: st.markdown("""<div class="market-box"><div class="market-val">↗ BULL</div><div class="market-lbl">Porsche</div></div>""", unsafe_allow_html=True)
    with c2: st.markdown("""<div class="market-box"><div class="market-val">↘ BEAR</div><div class="market-lbl">Diesel</div></div>""", unsafe_allow_html=True)

    st.write("---")
    st.header("🎯 Ciblage")
    if st.button("🔄 Scan Réseau", use_container_width=True): st.cache_data.clear(); st.rerun()

    if not df.empty:
        marques = ["Toutes"] + sorted(df['marque'].unique().tolist())
        f_marque = st.selectbox("Marque", marques)
        
        mods = ["Tous"]
        if f_marque != "Toutes": mods += sorted(df[df['marque'] == f_marque]['modele'].unique().tolist())
        f_modele = st.selectbox("Modèle", mods)

        c_carb, c_boite = st.columns(2)
        f_carb = c_carb.selectbox("Carburant", ["Tous"] + sorted(df['carburant'].unique().tolist()))
        f_boite = c_boite.selectbox("Boîte", ["Toutes"] + sorted(df['boite'].unique().tolist()))

        budget = st.slider("Budget Max", 10000, 200000, 80000, step=5000)
        
    st.write("---")
    st.markdown("""<div style="background:#1a1d21; padding:12px; border-radius:8px; display:flex; align-items:center; border:1px solid #333;"><div style="background:#d4af37; width:35px; height:35px; border-radius:50%; margin-right:10px; display:flex; align-items:center; justify-content:center; color:black; font-weight:bold;">M</div><div><div style="font-size:13px; font-weight:bold; color:white;">Membre Invité</div><div style="font-size:11px; color:#2ea043;">● Connecté</div></div></div>""", unsafe_allow_html=True)

# --- LOGIQUE ---
if menu == "📡 Radar":
    if df.empty: st.error("Aucune donnée. Lancez scraper.py"); st.stop()

    mask = (df['prix'] <= budget)
    if f_marque != "Toutes": mask &= (df['marque'] == f_marque)
    if f_modele != "Tous": mask &= (df['modele'] == f_modele)
    if f_carb != "Tous": mask &= (df['carburant'] == f_carb)
    if f_boite != "Toutes": mask &= (df['boite'] == f_boite)

    df_final = df[mask].sort_values(by='score', ascending=False)

    # 1. TOP PÉPITES
    df_pepites = df_final[df_final['score'] >= 80].head(3)
    if not df_pepites.empty:
        st.markdown('<div class="pepite-header">🔥 Arrivages Pépites (Top Rentabilité)</div>', unsafe_allow_html=True)
        cols = st.columns(3)
        for i, (_, row) in enumerate(df_pepites.iterrows()):
            with cols[i]:
                opt_list = str(row.get('options', '')).split('|')[:2]
                tags_html = "".join([f'<span class="opt-tag">{o.strip()}</span>' for o in opt_list])
                st.markdown(f"""<div class="lc-card"><div class="lc-img-container"><img src="{row['img_url']}" class="lc-img"><div class="badge-corner">SUPER DEAL</div><div class="badge-score">Score: {int(row['score'])}</div></div><div class="lc-content"><div class="lc-title">{row['titre']}</div><div class="lc-subtitle">{row['annee']} | {row['km']} km | {row['ville']}</div><div style="height:25px; overflow:hidden;">{tags_html}</div><div class="lc-footer"><div class="lc-price">{row['prix']} €</div><div class="lc-cote">Gain estimé<br>+{row['gain']} €</div></div></div></div>""", unsafe_allow_html=True)
                if st.button("🔒 Dossier PDF", key=f"pep_{row['id']}", use_container_width=True):
                    afficher_paywall(row) # Envoi de la ligne complète pour le PDF
        st.write("---")

    # 2. TOUTES LES ANNONCES
    st.subheader(f"Toutes les annonces ({len(df_final)})")
    if df_final.empty:
        st.info("Aucun résultat.")
    else:
        for i in range(0, len(df_final), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(df_final):
                    row = df_final.iloc[i+j]
                    with cols[j]:
                        badge_txt = "TOP" if row['score'] > 75 else "OCCASION"
                        color_badge = "#d4af37" if row['score'] > 75 else "#555"
                        opt_list = str(row.get('options', '')).split('|')[:2]
                        tags_html = "".join([f'<span class="opt-tag">{o.strip()}</span>' for o in opt_list])
                        
                        st.markdown(f"""<div class="lc-card"><div class="lc-img-container"><img src="{row['img_url']}" class="lc-img"><div class="badge-corner" style="background-color:{color_badge}">{badge_txt}</div></div><div class="lc-content"><div class="lc-title">{row['titre']}</div><div class="lc-subtitle">{row['annee']} | {row['km']} km</div><div style="height:25px; overflow:hidden;">{tags_html}</div><div class="lc-footer"><div class="lc-price" style="font-size:20px;">{row['prix']} €</div><div style="font-size:12px; color:#888;">Cote: {row['cote_argus']}€</div></div></div></div>""", unsafe_allow_html=True)
                        if st.button("🔒 PDF", key=f"list_{row['id']}", use_container_width=True):
                            afficher_paywall(row)

elif menu == "⭐ Favoris": st.info("Vos favoris apparaîtront ici.")
elif menu == "🔔 Alertes": st.info("Module Alertes Email en maintenance.")