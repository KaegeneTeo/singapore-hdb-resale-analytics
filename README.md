# Singapore HDB Resale Price Analytics

A data analytics project to uncover the trends in HDB (Housing & Development Board) resale flat prices over the years in Singapore.

## Overview

This project analyses the publicly available HDB resale transaction data from the [Singapore Government Open Data Portal](https://data.gov.sg) to answer questions such as:

- How have HDB resale prices trended from 1990 to 2024?
- How do prices differ by flat type (3-Room, 4-Room, Executive, …)?
- Which towns command the highest premiums, and has that changed over time?
- How have cooling measures and macro events (AFC, GFC, COVID-19) affected prices?
- How does price per square metre compare across towns and time periods?

## Key Findings

| # | Finding |
|---|---------|
| 1 | **Long-run appreciation** – Median resale prices roughly tripled from ~S$120k in 1990 to ~S$450k+ by 2024. |
| 2 | **Cyclical corrections** – The Asian Financial Crisis (1997–98) and GFC (2008–09) each caused 5–12% dips before renewed growth. |
| 3 | **Cooling-measure impact** – Policies introduced from 2013 (ABSD hikes, loan caps) dampened prices for ~6 years. |
| 4 | **Post-COVID surge** – Prices rose ~25% from mid-2020 to 2023, one of the sharpest multi-year increases on record. |
| 5 | **Location premium** – Central/mature towns (Central Area, Bukit Timah, Marine Parade) command a 30–70% premium over peripheral estates. |
| 6 | **Flat-size multiplier** – Each step up in flat type adds roughly 20–35% to median price; Executive units trade at ~3× a 3-Room flat in the same town. |

## Project Structure

```
singapore-hdb-resale-analytics/
├── data/                          # Raw and combined datasets (gitignored)
│   └── resale_flat_prices_sample.csv   # Synthetic sample data for demos
├── figures/                       # Exported chart images (auto-generated)
├── notebooks/
│   └── hdb_resale_analysis.ipynb  # Main analysis notebook
├── src/
│   ├── fetch_data.py              # Download official data from data.gov.sg
│   ├── generate_sample_data.py    # Generate synthetic sample data
│   └── build_notebook.py         # Build & execute the notebook programmatically
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Obtain data

**Option A – Download official data from data.gov.sg** (requires internet access):

```bash
python src/fetch_data.py
# Saves individual CSVs and a combined file to data/
```

**Option B – Use the synthetic sample dataset** (no internet required):

```bash
python src/generate_sample_data.py
# Generates data/resale_flat_prices_sample.csv
```

### 3. Run the analysis

Open the notebook in JupyterLab or Jupyter Notebook:

```bash
jupyter lab notebooks/hdb_resale_analysis.ipynb
```

Or rebuild and re-execute the notebook from the command line:

```bash
python src/build_notebook.py
```

Exported chart images are saved to the `figures/` directory.

## Visualisations

The notebook produces 9 charts:

| # | Chart | Description |
|---|-------|-------------|
| 1 | Annual median price trend | Median & mean price with IQR band, key events annotated |
| 2 | Year-on-year change | Bar chart of % change, green = growth, red = decline |
| 3 | Price by flat type | Multi-line trend for each flat type |
| 4 | Price by town | Horizontal bar chart ranked by median price |
| 5 | Town × period heat-map | Median price for each town across 5-year periods |
| 6 | Price per sqm | Annual trend of median price per square metre |
| 7 | Distribution by flat type | Box plots showing spread and outliers |
| 8 | Floor area vs. price | Scatter plot with OLS regression line |
| 9 | Top 5 towns (recent) | Price trends for the 5 most expensive towns since 2015 |

## Data Sources

- **HDB Resale Flat Prices (1990–present)** – Singapore Government Open Data Portal: [data.gov.sg](https://data.gov.sg/datasets/d_8b84c4ee58e3cfc0ece0d773c8ca6abc/view)
- The portal publishes five separate datasets covering different date ranges; `src/fetch_data.py` downloads and merges all of them automatically.

## Tech Stack

- **Python 3.12**
- **pandas** – data wrangling
- **Matplotlib / Seaborn** – visualisations
- **SciPy** – regression statistics
- **Jupyter** – interactive notebook environment
