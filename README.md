# DeFi Yield & Risk Optimizer (Aave Edition)

## Présentation du Projet
Ce projet est un outil d'aide à la décision conçu pour les analystes DeFi et les investisseurs. Il permet d'extraire, de traiter et de visualiser en temps réel les opportunités de rendement (APY) sur le protocole **Aave**, tout en les pondérant par un **score de risque composite**.

L'objectif est de résoudre le problème de l'asymétrie d'information en DeFi : un APY élevé cache souvent un risque de liquidité ou de smart-contract important.

## Stack Technique
- **Langage** : Python 3.x
- **Data Ingestion** : API DefiLlama (Endpoints `/pools`)
- **Data Processing** : Pandas (Nettoyage, filtrage par regex, gestion des valeurs nulles)
- **Data Visualization** : Matplotlib & Numpy

## Méthodologie : Le "Risk Score"
Le projet ne se contente pas d'afficher les rendements bruts. Il calcule un indicateur de risque basé sur les données de prédiction Machine Learning fournies par l'API :

$$Risk Score = 100 - Confidence_{IA}$$

Où **Confidence_IA** représente la probabilité (`predictedProbability`) que le rendement soit stable ou à la hausse. 
- **Score proche de 0** : Actif très stable, confiance maximale.
- **Score proche de 100** : Actif volatil ou manque de données, risque maximal.

## Visualisation : Bubble Chart Multi-Dimensionnel
L'outil génère une analyse graphique en 4 dimensions :
1. **Axe X** : Rendement (APY %)
2. **Axe Y** : Score de Risque (Bas est mieux)
3. **Taille des bulles** : Volume des fonds bloqués (TVL en USD)
4. **Couleur** : Gradient de risque (Vert vers Rouge)

Cela permet d'identifier immédiatement la **Frontière d'Efficience** (les actifs offrant le meilleur ratio rendement/risque).

## Installation et Utilisation

### Pré-requis
```bash
pip install requests pandas matplotlib numpy


`![Analyse Graphique](./aave_analysis.png)`
