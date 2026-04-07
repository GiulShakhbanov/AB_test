# A/B Test Analysis: Premium Armor Discount in an Online Shooter

## Overview
Analysis of an A/B test conducted in an online shooter game to evaluate the impact of a **premium armor discount** on key revenue metrics. The goal is to determine whether the promotion should be repeated.

## Key Metrics
| Metric | Description |
|--------|-------------|
| **ARPU** | Average Revenue Per User |
| **ARPPU** | Average Revenue Per Paying User |
| **Avg Cash Spent** | Average in-game currency spending |

## Methodology
- Comparison of **test** (discount) vs **control** (no discount) groups
- 95% confidence intervals via bootstrap
- Segmentation by platform (PC, PS4, XBox, Android, iOS)
- Cheater detection and removal

## Tech Stack
- **Python** (pandas, numpy, scipy, seaborn, matplotlib) — data processing & statistical analysis
- **Jupyter Notebook** — exploratory analysis
- **Power BI** — interactive dashboards

## Project Structure
```
├── notebooks/
│   └── ab_test_analysis.ipynb   # Full analysis notebook
├── output/
│   └── powerbi_data/            # Aggregated CSVs for Power BI
├── data/
│   └── raw/                     # Source CSVs (not tracked)
├── requirements.txt
└── .gitignore
```

## How to Run
```bash
pip install -r requirements.txt
jupyter notebook notebooks/ab_test_analysis.ipynb
```

## Status
🔧 Work in progress
