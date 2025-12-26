import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 1. Récupération des données via l'API Yields du fichier JSON
yields_url = "https://yields.llama.fi/pools"
response = requests.get(yields_url).json()
df = pd.DataFrame(response['data'])

# 2. Filtrage robuste (contient 'aave')
df_aave = df[df['project'].str.lower().str.contains('aave')].copy()

# 3. Feature Engineering : Création du Risk Score
# On utilise la 'predictedProbability' de l'IA de DefiLlama
def calculate_risk(pred):
    if isinstance(pred, dict):
        # On récupère la valeur, et si c'est None ou absent, on met 50
        conf = pred.get('predictedProbability')
        if conf is None:
            conf = 50
        return 100 - conf
    return 50

df_aave['risk_score'] = df_aave['predictions'].apply(calculate_risk)

# 4. Génération du Bubble Chart
plt.figure(figsize=(12, 8))

# Taille des bulles : proportionnelle à la racine carrée de la TVL pour la lisibilité
sizes = np.sqrt(df_aave['tvlUsd']) / 100 

scatter = plt.scatter(
    x=df_aave['apy'], 
    y=df_aave['risk_score'], 
    s=sizes, 
    c=df_aave['risk_score'], 
    cmap='RdYlGn_r', # Vert (Risque bas) vers Rouge (Risque haut)
    alpha=0.6, 
    edgecolors="grey"
)

# Annotations pour les 5 plus grosses pools par TVL
for i, row in df_aave.nlargest(5, 'tvlUsd').iterrows():
    plt.annotate(f"{row['symbol']} ({row['chain']})", (row['apy'], row['risk_score']), 
                 textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

plt.colorbar(scatter, label='Risk Score (Bas est mieux)')
plt.title('Aave Yield Optimizer : Rendement vs Risque vs TVL', fontsize=15)
plt.xlabel('APY (%)', fontsize=12)
plt.ylabel('Risk Score (Basé sur IA Confidence)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)

# Sauvegarde du graphique pour ton portfolio
plt.savefig('aave_analysis.png')
print("Graphique 'aave_analysis.png' généré avec succès !")
plt.show()
