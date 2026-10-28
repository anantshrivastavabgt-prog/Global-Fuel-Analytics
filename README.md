# Global Fuel Prices and Taxation Trends: A Comprehensive Analysis

A college capstone data analytics project that analyzes retail fuel prices, international crude oil benchmarks, sovereign taxation structures, and government subsidies across 84 sovereign nations and 7 global regions from 2020 to 2026.

---

## 📌 Project Overview

Consumer fuel prices do not exist in isolation. While upstream crude oil is priced in international commodity markets, the pump prices paid by motorists and logistics operators diverge by up to **16-fold** across borders due to local excise duties, green environmental levies, and subsidy programs.

This repository contains a full-stack, interactive data analytics web application developed with **Python, Flask, Pandas, and Plotly.js**, delivering:
* **9 Interactive Visualizations** including global choropleth heat maps, longitudinal trend charts, regional tax shares, and multi-fuel price rankings.
* **6-Tier Dynamic Filter Toolbar** (Region, Country, Year, Measure, Income Level, Subsidy Level).
* **7-Scene Analytical Data Story** translating raw energy metrics into economic intelligence.
* **3 Practical Stakeholder Scenarios** addressing energy policy consultants, global supply chain directors, and academic researchers.
* **Academic Submission Deliverables** including an official project documentation report, presentation walkthrough script, and companion Tableau workbook (`.twb`).

---

## 📊 Dataset Specification

| Attribute | Details |
| :--- | :--- |
| **Total Record Count** | 27,468 weekly observations |
| **Attribute Columns** | 10 columns |
| **Temporal Range** | January 2020 – April 2026 |
| **Geographic Scope** | 84 sovereign nations across 7 continental regions |
| **Data Completeness** | 100% verified (0 missing or null values) |

### Attribute Data Dictionary
* `date`: Weekly observation timestamp (YYYY-MM-DD).
* `country`: Sovereign country of observation (84 nations).
* `region`: Continental zone (`Africa`, `Asia`, `Europe`, `Middle East`, `North America`, `Oceania`, `South America`).
* `income_level`: National economic classification (`High`, `Middle`, `Low`).
* `subsidy_level`: Government fuel subsidy tier (`Very High`, `High`, `Medium`, `Low`).
* `petrol_usd_liter`: Retail automotive petrol/gasoline price (USD per liter).
* `diesel_usd_liter`: Retail automotive diesel price (USD per liter).
* `lpg_usd_liter`: Retail liquefied petroleum gas price (USD per liter).
* `brent_crude_usd`: Brent Crude international benchmark price (USD per barrel).
* `tax_percentage`: Sovereign tax percentage of retail pump price (0.0% to 65.0%).

*Note: Dataset sourced for academic evaluation via the SkillWallet educational module.*

---

## 🚀 How to Run the Project Locally

### Prerequisites
* **Python 3.10+** installed on your system.

### Quick Start (Windows)
Simply double-click the included batch launcher:
```bash
run_dashboard.bat
```
This automatically starts the local server and opens your default browser at `http://127.0.0.1:5000`.

### Manual Startup (Cross-Platform: Windows, macOS, Linux)
1. **Clone or download this repository:**
   ```bash
   git clone https://github.com/<your-username>/Global-Fuel-Analytics.git
   cd Global-Fuel-Analytics
   ```
2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the web application:**
   ```bash
   python app.py
   ```
4. **Open your web browser and navigate to:**
   ```
   http://127.0.0.1:5000
   ```

---

## 📁 Repository Structure

```
Global-Fuel-Analytics/
│
├── app.py                             # Main Flask application and RESTful API backend
├── global_fuel_prices_Dataset.csv     # Verified longitudinal dataset (27,468 records)
├── requirements.txt                   # Python package dependencies
├── .gitignore                         # Git exclusion rules for clean repository state
├── run_dashboard.bat                  # One-click Windows application launcher
├── Global_Fuel_Analytics.twb          # Companion Tableau workbook XML
├── generate_twb.py                    # Tableau workbook generation script
│
├── templates/
│   └── index.html                     # Frontend dashboard and story interface
│
├── static/
│   ├── css/
│   │   └── style.css                  # Professional light-blue and navy theme stylesheet
│   └── js/
│       └── dashboard.js               # Plotly.js charts, filters, and story interactivity
│
├── documentation/
│   ├── Project_Report.html            # Complete academic project report (printable to PDF)
│   ├── Project_Report.md              # Markdown version of official project report
│   ├── Video_Presentation_Script.html # 5-7 minute video demo script with slide cues
│   └── Video_Presentation_Script.md   # Markdown version of video walkthrough script
│
└── test_app.py                        # Automated test verification suite
```

---

## 📈 Visualizations & Story Architecture

1. **KPI Cards:** Instant computation of Global Average Petrol ($2.28/L), Diesel ($2.13/L), LPG ($1.71/L), Tax Rate (26.77%), and Brent Crude ($107.98/bbl).
2. **Geospatial Choropleth Heat Maps:** Worldwide distribution maps for Petrol and Diesel across 84 nations.
3. **Longitudinal Trend Lines (2020–2026):** Tracking 6-year price movements, the 2020 pandemic dip ($1.48/L), the 2022 peak ($2.51/L), and the 2024–2026 plateau ($2.65/L).
4. **Regional Tax Donut Chart:** Highlighting tax burdens across 7 continental zones (Oceania 38.7%, Europe 34.6%, South America 18.2%).
5. **Comparative Bar Charts:** Rankings of highest tax-paying nations and multi-fuel price comparison across premium markets (Hong Kong, Norway, Netherlands).
6. **7-Scene Interactive Data Story:**
   - Scene 1: Research Question & Global Energy Economics
   - Scene 2: Geographic Disparity & Continental Price Spreads
   - Scene 3: Temporal Trends & Longitudinal Volatility
   - Scene 4: Sovereign Taxation Policy Analysis
   - Scene 5: Economic Impact & Income-Level Correlation
   - Scene 6: Government Subsidy Assessment & Fiscal Costs
   - Scene 7: Conclusions & Evidence-Based Recommendations

---

## 🎓 Academic Deliverables Access

* **Full Project Report:** Open `http://127.0.0.1:5000/documentation/Project_Report.html` and click **"Print / Save as PDF"**.
* **5–7 Min Walkthrough Script:** Open `http://127.0.0.1:5000/documentation/Video_Presentation_Script.html`.

---

## 👤 Author

* **Student Name:** Anant Shrivastava
* **Curriculum:** SkillWallet Data Analytics Capstone Project
* **Status:** Fully Verified & Ready for Evaluation
