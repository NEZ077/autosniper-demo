import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(
    page_title="AutoSniper Ultimate",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS PERSONNALISÉ (Le Makeover) ---
st.markdown("""
<style>
    /* Fond global plus doux */
    .stApp {
        background-color: #0e1117;
    }
    /* Style des cartes KPIs */
    div[data-testid="stMetric"] {
        background-color: #262730;
        border: 1px solid #464b5c;
        padding: 15px;
        border-radius: 10px;
        color: white;
    }
    /* Style des onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #262730;
        border-radius: 5px;
        padding-top: 10px;
        padding-bottom: 10px;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# --- CHARGEMENT ET LOGIQUE ---
# ttl=900 veut dire : "Expire au bout de 900 secondes (15 min)"
@st.cache_data(ttl=900)
def charger_donnees():
    if not os.path.exists("annonces.csv"):
        return pd.DataFrame()
    df = pd.read_csv("annonces.csv")
    
    # Nettoyage
    df['prix'] = pd.to_numeric(df['prix'], errors='coerce')
    df['km'] = pd.to_numeric(df['km'], errors='coerce')
    df['annee'] = pd.to_numeric(df['annee'], errors='coerce')
    
    # --- CERVEAU DU SNIPER ---
    def calculer_score(row):
        # 1. Calcul de la cote théorique
        base = 35000
        if any(x in row['titre'] for x in ["Audi", "BMW", "Mercedes"]): base += 6000
        if any(x in row['titre'] for x in ["Clio", "208", "C3"]): base -= 15000
        
        decote_km = row['km'] * 0.06
        decote_annee = (2025 - row['annee']) * 1500
        
        cote_estimee = base - decote_km - decote_annee
        profit = cote_estimee - row['prix']
        
        # 2. Score sur 100
        # Si profit = 0 -> Score 50. Si profit = 5000 -> Score 100.
        score = 50 + (profit / 100)
        return min(100, max(0, int(score))), int(profit)

    # On applique le calcul et on récupère deux colonnes (Score et Profit)
    resultats = df.apply(calculer_score, axis=1, result_type='expand')
    df['score'] = resultats[0]
    df['profit'] = resultats[1]
    
    # Label
    def get_label(score):
        if score >= 80: return "🔥 Super Affaire"
        if score >= 60: return "✅ Bonne Affaire"
        return "😐 Standard / Cher"
    
    df['label'] = df['score'].apply(get_label)
    
    return df.sort_values(by='score', ascending=False)

df = charger_donnees()

# --- SIDEBAR (Centre de Contrôle) ---
with st.sidebar:
    st.title("🎯 AutoSniper")
    st.caption("v2.0 Ultimate")
    
    if st.button("🔄 Rafraîchir les données", use_container_width=True):
        st.cache_data.clear() # On force le rechargement
        st.rerun()
    
    st.divider()
    st.header("Filtres")
    
    # Filtres Intelligents
    if not df.empty:
        marques_dispo = sorted(list(set([t.split(' ')[0] for t in df['titre']])))
        filtre_marque = st.multiselect("Marques", marques_dispo)
        
        col_budget, col_km = st.columns(2)
        budget_max = col_budget.number_input("Budget Max", value=int(df['prix'].max()), step=1000)
        km_max = col_km.number_input("KM Max", value=150000, step=5000)
        
        # Filtre de Productivité : "Montre-moi que le top"
        filtre_qualite = st.radio("Qualité", ["Tout voir", "🔥 Super Affaire uniquement", "✅ Bonne Affaire +"], index=0)

# --- FILTRAGE DES DONNÉES ---
if df.empty:
    st.warning("⚠️ Aucune donnée. Lance scraper.py !")
    st.stop()

df_filtre = df.copy()
if filtre_marque:
    df_filtre = df_filtre[df_filtre['titre'].apply(lambda x: any(m in x for m in filtre_marque))]
df_filtre = df_filtre[(df_filtre['prix'] <= budget_max) & (df_filtre['km'] <= km_max)]

if filtre_qualite == "🔥 Super Affaire uniquement":
    df_filtre = df_filtre[df_filtre['score'] >= 80]
elif filtre_qualite == "✅ Bonne Affaire +":
    df_filtre = df_filtre[df_filtre['score'] >= 60]

# --- DASHBOARD PRINCIPAL ---
# KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Annonces ciblées", len(df_filtre), f"{len(df)} total")
if not df_filtre.empty:
    prix_moyen = int(df_filtre['prix'].mean())
    c2.metric("Prix Moyen", f"{prix_moyen} €")
    
    top_profit = int(df_filtre['profit'].max())
    c3.metric("Potentiel Max", f"+ {top_profit} €", delta="Cash")
    
    score_moyen = int(df_filtre['score'].mean())
    c4.metric("Qualité Moyenne", f"{score_moyen}/100", delta_color="normal")

st.write("") # Espace

# --- ONGLETS (Productivité) ---
tab1, tab2, tab3 = st.tabs(["📊 Analyse Visuelle", "🚘 Liste Détaillée", "🗃️ Données Brutes"])

with tab1:
    st.subheader("Où sont les pépites ?")
    st.caption("Cherchez les grosses bulles vertes en bas à gauche.")
    
    if not df_filtre.empty:
        fig = px.scatter(
            df_filtre, 
            x="km", y="prix", 
            size="score", color="label",
            color_discrete_map={"🔥 Super Affaire": "#00CC96", "✅ Bonne Affaire": "#636EFA", "😐 Standard / Cher": "#EF553B"},
            hover_name="titre",
            hover_data=["annee", "profit"],
            height=500
        )
        # Amélioration du look du graphique
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            xaxis=dict(showgrid=True, gridcolor='#444'),
            yaxis=dict(showgrid=True, gridcolor='#444')
        )
        st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.subheader(f"Les {len(df_filtre)} meilleures opportunités")
    
    # Affichage en Grille plus compacte
    cols = st.columns(3)
    for index, row in df_filtre.iterrows():
        with cols[index % 3]:
            # Définition de la couleur de bordure
            border_color = "#00CC96" if row['score'] >= 80 else "#636EFA" if row['score'] >= 60 else "#EF553B"
            
            with st.container(border=True):
                # En-tête avec Badge
                c_head1, c_head2 = st.columns([3, 1])
                c_head1.write(f"**{row['titre']}**")
                c_head2.markdown(f"**{row['score']}/100**")
                
                st.image(row['img_url'], use_container_width=True)
                
                # Prix et Infos
                st.markdown(f"### {row['prix']} €")
                st.caption(f"📅 {row['annee']} | 🛣️ {row['km']} km | 📍 {row['ville']}")
                
                # Barre de rentabilité visuelle
                st.progress(row['score'] / 100)
                
                # Bouton Action
                st.link_button(f"Voir l'annonce (Gain: +{row['profit']}€)", row['url'], use_container_width=True)

with tab3:
    st.subheader("Mode Tableur (Excel)")
    # Tableau interactif
    st.dataframe(
        df_filtre[['titre', 'prix', 'km', 'annee', 'ville', 'profit', 'score', 'label']],
        use_container_width=True,
        column_config={
            "prix": st.column_config.NumberColumn(format="%d €"),
            "profit": st.column_config.NumberColumn(format="+ %d €"),
            "score": st.column_config.ProgressColumn("Score Deal", format="%d", min_value=0, max_value=100),
            "img_url": st.column_config.ImageColumn("Aperçu"),
        },
        hide_index=True
    )