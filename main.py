import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Configuration de la page
st.set_page_config(page_title="Aave Advanced Dashboard", layout="wide")

st.title("🚀 Aave Yield Optimizer v2")

# 1. Chargement des données avec Cache
@st.cache_data
def load_data():
    yields_url = "https://yields.llama.fi/pools"
    response = requests.get(yields_url).json()
    df = pd.DataFrame(response['data'])
    
    # Filtrage Aave
    df_aave = df[df['project'].str.lower().str.contains('aave')].copy()
    
    # Correction de la fonction de risque pour éviter le crash 'NoneType'
    def calculate_risk(pred):
        if isinstance(pred, dict):
            conf = pred.get('predictedProbability')
            # Si conf est None ou pas un nombre, on met un score par défaut (50)
            if conf is None or not isinstance(conf, (int, float)):
                return 50
            return 100 - conf
        return 50
    
    df_aave['risk_score'] = df_aave['predictions'].apply(calculate_risk)
    return df_aave

df_raw = load_data()

# --- SIDEBAR : FILTRES ---
st.sidebar.header("⚙️ Configuration des Filtres")

# Filtre Blockchain
all_chains = sorted(df_raw['chain'].unique())
selected_chains = st.sidebar.multiselect("Sélectionner les Blockchains", all_chains, default=all_chains)

# Filtre Token (Symbol)
all_symbols = sorted(df_raw['symbol'].unique())
selected_symbols = st.sidebar.multiselect("Filtrer par Token", all_symbols, default=all_symbols)

# Filtre TVL
max_tvl = int(df_raw['tvlUsd'].max())
min_tvl = st.sidebar.slider("TVL Minimum ($)", 0, max_tvl, 1000000)

# Application des filtres
df_filtered = df_raw[
    (df_raw['chain'].isin(selected_chains)) & 
    (df_raw['symbol'].isin(selected_symbols)) &
    (df_raw['tvlUsd'] >= min_tvl)
]

# --- AFFICHAGE ---
if df_filtered.empty:
    st.warning("⚠️ Aucune donnée ne correspond à ces filtres.")
else:
    # Métriques
    c1, c2, c3 = st.columns(3)
    c1.metric("Pools", len(df_filtered))
    c2.metric("TVL Totale", f"${df_filtered['tvlUsd'].sum()/1e6:.1f}M")
    c3.metric("APY Max", f"{df_filtered['apy'].max():.2f}%")

    # Graphique
    fig, ax = plt.subplots(figsize=(10, 6))
    # On évite les tailles trop petites ou trop grandes
    sizes = np.clip(np.sqrt(df_filtered['tvlUsd']) / 20, 10, 1000)
    
    scatter = ax.scatter(
        x=df_filtered['apy'], 
        y=df_filtered['risk_score'], 
        s=sizes, 
        c=df_filtered['risk_score'], 
        cmap='RdYlGn_r', 
        alpha=0.6, 
        edgecolors="white"
    )

    # Annotations top 5
    for i, row in df_filtered.nlargest(5, 'tvlUsd').iterrows():
        ax.annotate(row['symbol'], (row['apy'], row['risk_score']), fontsize=9)

    plt.colorbar(scatter, label='Score de Risque')
    ax.set_xlabel('APY (%)')
    ax.set_ylabel('Risk Score')
    st.pyplot(fig)

    # Tableau
    st.dataframe(df_filtered[['chain', 'symbol', 'apy', 'tvlUsd', 'risk_score']].sort_values('apy', ascending=False))
