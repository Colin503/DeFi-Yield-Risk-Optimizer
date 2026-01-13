# 🚀 Aave Yield & Risk Optimizer

An interactive data visualization dashboard built with **Streamlit** to analyze and compare yield opportunities across various **Aave** deployments.


## 📊 Overview
This tool fetches real-time data from the **DefiLlama Yields API** to help users visualize the relationship between **APY (Annual Percentage Yield)**, **TVL (Total Value Locked)**, and **Risk Scores**.

The risk score is calculated based on DefiLlama's AI-driven confidence intervals (`predictedProbability`), allowing for a better assessment of "too good to be true" yields.

## ✨ Key Features
* **Dynamic Filtering**: Filter by Blockchain (Ethereum, Polygon, Arbitrum, etc.) and specific Assets (USDC, WETH, GHO).
* **Bubble Chart Visualization**: 
    * **X-Axis**: APY (%)
    * **Y-Axis**: Risk Score (Lower is safer)
    * **Size**: Proportional to TVL.
* **Automated Insights**: Highlights the top 5 largest pools for quick decision-making.
* **Live Data**: Data is cached to ensure performance while staying up-to-date with DeFi markets.

## 🛠️ Installation & Local Usage

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/Colin503/DeFi-Yield-Risk-Optimizer.git](https://github.com/Colin503/DeFi-Yield-Risk-Optimizer.git)
   cd DeFi-Yield-Risk-Optimizer
