import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page Streamlit
st.set_page_config(page_title="Aave Yield Optimizer", layout="wide")

st.title("🚀 Aave Yield Optimizer")
st.markdown("Analyse comparative du Rendement, du Risque et de la TVL sur les pools Aave.")

# 1. Récupération des données (avec cache pour éviter de recharger à chaque interaction)
@st.cache_data
def load_data():
    yields_url = "https://yields.llama.fi/pools"
    response = requests.get(yields_url).json()
    return pd.DataFrame(response['data'])

df = load_data()

# 2. Filtrage robuste
df_aave = df[df['project'].str.lower().str.contains('aave')].copy()

# 3. Feature Engineering
def calculate_risk(pred):
    if isinstance(pred, dict):
        conf = pred.get('predictedProbability')
        if conf is None:
            conf = 50
        return 100 - conf
    return 50

df_aave['risk_score'] = df_aave['predictions'].apply(calculate_risk)

# --- INTERFACE STREAMLIT ---

# Sidebar pour les filtres
st.sidebar.header("Filtres")
min_tvl = st.sidebar.slider("TVL Minimum ($)", 0, int(df_aave['tvlUsd'].max()), 1000000)
df_filtered = df_aave[df_aave['tvlUsd'] >= min_tvl]

# Affichage de quelques métriques clés
col1, col2, col3 = st.columns(3)
col1.metric("Nombre de Pools", len(df_filtered))
col2.metric("APY Max", f"{df_filtered['apy'].max():.2f}%")
col3.metric("TVL Totale", f"${df_filtered['tvlUsd'].sum()/1e9:.2f}B")

# 4. Génération du Bubble Chart avec Matplotlib
fig, ax = plt.subplots(figsize=(12, 8))

# Taille des bulles
sizes = np.sqrt(df_filtered['tvlUsd']) / 100 

scatter = ax.scatter(
    x=df_filtered['apy'], 
    y=df_filtered['risk_score'], 
    s=sizes, 
    c=df_filtered['risk_score'], 
    cmap='RdYlGn_r', 
    alpha=0.6, 
    edgecolors="grey"
)

# Annotations
for i, row in df_filtered.nlargest(5, 'tvlUsd').iterrows():
    ax.annotate(f"{row['symbol']} ({row['chain']})", (row['apy'], row['risk_score']), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

plt.colorbar(scatter, label='Risk Score (Bas est mieux)')
ax.set_title('Aave Yield Optimizer : Rendement vs Risque vs TVL', fontsize=15)
ax.set_xlabel('APY (%)')
ax.set_ylabel('Risk Score')
ax.grid(True, linestyle='--', alpha=0.5)

# --- AFFICHAGE DANS STREAMLIT ---
st.pyplot(fig)

# Optionnel : Afficher les données brutes
if st.checkbox("Afficher le tableau des données"):
    st.dataframe(df_filtered[['chain', 'symbol', 'apy', 'tvlUsd', 'risk_score']].sort_values('apy', ascending=False))
