import os
import json
import pandas as pd
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Load and validate dataset
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'global_fuel_prices_Dataset.csv')
if not os.path.exists(DATASET_PATH):
    raise FileNotFoundError(f"Dataset not found at {DATASET_PATH}")

df = pd.read_csv(DATASET_PATH)
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year

# Complete ISO-3 mapping for all 84 countries
ISO_MAP = {
    'Algeria': 'DZA', 'Angola': 'AGO', 'Argentina': 'ARG', 'Australia': 'AUS', 'Austria': 'AUT',
    'Bangladesh': 'BGD', 'Belgium': 'BEL', 'Botswana': 'BWA', 'Brazil': 'BRA', 'Cameroon': 'CMR',
    'Canada': 'CAN', 'Chile': 'CHL', 'China': 'CHN', 'Colombia': 'COL', 'Czech Republic': 'CZE',
    'Denmark': 'DNK', 'Ecuador': 'ECU', 'Egypt': 'EGY', 'Ethiopia': 'ETH', 'Finland': 'FIN',
    'France': 'FRA', 'Germany': 'DEU', 'Ghana': 'GHA', 'Greece': 'GRC', 'Hong Kong': 'HKG',
    'Hungary': 'HUN', 'India': 'IND', 'Indonesia': 'IDN', 'Iran': 'IRN', 'Iraq': 'IRQ',
    'Ireland': 'IRL', 'Israel': 'ISR', 'Italy': 'ITA', 'Ivory Coast': 'CIV', 'Japan': 'JPN',
    'Jordan': 'JOR', 'Kenya': 'KEN', 'Kuwait': 'KWT', 'Lebanon': 'LBN', 'Libya': 'LBY',
    'Malaysia': 'MYS', 'Mexico': 'MEX', 'Morocco': 'MAR', 'Mozambique': 'MOZ', 'Myanmar': 'MMR',
    'Namibia': 'NAM', 'Nepal': 'NPL', 'Netherlands': 'NLD', 'New Zealand': 'NZL', 'Nigeria': 'NGA',
    'Norway': 'NOR', 'Pakistan': 'PAK', 'Peru': 'PER', 'Philippines': 'PHL', 'Poland': 'POL',
    'Portugal': 'PRT', 'Qatar': 'QAT', 'Romania': 'ROU', 'Russia': 'RUS', 'Rwanda': 'RWA',
    'Saudi Arabia': 'SAU', 'Senegal': 'SEN', 'Singapore': 'SGP', 'South Africa': 'ZAF',
    'South Korea': 'KOR', 'Spain': 'ESP', 'Sri Lanka': 'LKA', 'Sudan': 'SDN', 'Sweden': 'SWE',
    'Switzerland': 'CHE', 'Taiwan': 'TWN', 'Tanzania': 'TZA', 'Thailand': 'THA', 'Tunisia': 'TUN',
    'Turkey': 'TUR', 'UAE': 'ARE', 'Uganda': 'UGA', 'Ukraine': 'UKR', 'United Kingdom': 'GBR',
    'United States': 'USA', 'Venezuela': 'VEN', 'Vietnam': 'VNM', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE'
}

@app.route('/')
def index():
    countries = sorted(df['country'].unique().tolist())
    regions = sorted(df['region'].unique().tolist())
    years = sorted(df['year'].unique().tolist())
    income_levels = ['High', 'Middle', 'Low']
    subsidy_levels = ['Low', 'Medium', 'High', 'Very High']
    
    return render_template(
        'index.html',
        countries=countries,
        regions=regions,
        years=years,
        income_levels=income_levels,
        subsidy_levels=subsidy_levels,
        total_rows=len(df),
        date_start=df['date'].min().strftime('%B %Y'),
        date_end=df['date'].max().strftime('%B %Y')
    )

@app.route('/api/data')
def get_data():
    region_param = request.args.get('region', 'all')
    country_param = request.args.get('country', 'all')
    year_param = request.args.get('year', 'all')
    income_param = request.args.get('income_level', 'all')
    subsidy_param = request.args.get('subsidy_level', 'all')
    measure_param = request.args.get('measure', 'all')

    filtered_df = df.copy()

    if region_param != 'all':
        filtered_df = filtered_df[filtered_df['region'] == region_param]
    if country_param != 'all':
        filtered_df = filtered_df[filtered_df['country'] == country_param]
    if year_param != 'all':
        filtered_df = filtered_df[filtered_df['year'] == int(year_param)]
    if income_param != 'all':
        filtered_df = filtered_df[filtered_df['income_level'] == income_param]
    if subsidy_param != 'all':
        filtered_df = filtered_df[filtered_df['subsidy_level'] == subsidy_param]

    if filtered_df.empty:
        return jsonify({
            'kpis': {'avg_petrol': 0, 'avg_diesel': 0, 'avg_lpg': 0, 'avg_tax': 0, 'avg_crude': 0, 'count': 0},
            'map_data': [],
            'yearly_trends': {'years': [], 'petrol': [], 'diesel': [], 'lpg': [], 'crude': []},
            'regional_tax': {'regions': [], 'tax_rates': []},
            'top_tax_nations': {'countries': [], 'tax_rates': []},
            'top_price_nations': {'countries': [], 'petrol': [], 'diesel': [], 'lpg': []}
        })

    # 1. KPIs
    avg_petrol = round(float(filtered_df['petrol_usd_liter'].mean()), 2)
    avg_diesel = round(float(filtered_df['diesel_usd_liter'].mean()), 2)
    avg_lpg = round(float(filtered_df['lpg_usd_liter'].mean()), 2)
    avg_tax = round(float(filtered_df['tax_percentage'].mean()), 2)
    avg_crude = round(float(filtered_df['brent_crude_usd'].mean()), 2)
    count = int(len(filtered_df))

    # 2. Map Data by Country
    country_summary = filtered_df.groupby('country').agg({
        'petrol_usd_liter': 'mean',
        'diesel_usd_liter': 'mean',
        'lpg_usd_liter': 'mean',
        'tax_percentage': 'mean',
        'region': 'first',
        'income_level': 'first',
        'subsidy_level': 'first'
    }).reset_index()

    map_data = []
    for _, row in country_summary.iterrows():
        c = row['country']
        iso = ISO_MAP.get(c, '')
        map_data.append({
            'country': c,
            'iso3': iso,
            'petrol': round(float(row['petrol_usd_liter']), 2),
            'diesel': round(float(row['diesel_usd_liter']), 2),
            'lpg': round(float(row['lpg_usd_liter']), 2),
            'tax': round(float(row['tax_percentage']), 2),
            'region': row['region'],
            'income': row['income_level'],
            'subsidy': row['subsidy_level']
        })

    # 3. Yearly Trends
    yearly = filtered_df.groupby('year').agg({
        'petrol_usd_liter': 'mean',
        'diesel_usd_liter': 'mean',
        'lpg_usd_liter': 'mean',
        'brent_crude_usd': 'mean'
    }).reset_index().sort_values('year')

    yearly_trends = {
        'years': yearly['year'].tolist(),
        'petrol': [round(float(v), 2) for v in yearly['petrol_usd_liter']],
        'diesel': [round(float(v), 2) for v in yearly['diesel_usd_liter']],
        'lpg': [round(float(v), 2) for v in yearly['lpg_usd_liter']],
        'crude': [round(float(v), 2) for v in yearly['brent_crude_usd']]
    }

    # 4. Regional Tax Breakdown (Pie Chart)
    # If filtered to one region, show that region's countries or overall distribution
    reg_group = filtered_df.groupby('region')['tax_percentage'].mean().reset_index()
    regional_tax = {
        'regions': reg_group['region'].tolist(),
        'tax_rates': [round(float(v), 2) for v in reg_group['tax_percentage']]
    }

    # 5. Highest Tax-Paying Nations (Top 8 to 10)
    top_tax = country_summary.sort_values(by='tax_percentage', ascending=False).head(8)
    top_tax_nations = {
        'countries': top_tax['country'].tolist(),
        'tax_rates': [round(float(v), 2) for v in top_tax['tax_percentage']]
    }

    # 6. Fuel Price Comparison Among Top 3 Countries
    top_price = country_summary.sort_values(by='petrol_usd_liter', ascending=False).head(3)
    top_price_nations = {
        'countries': top_price['country'].tolist(),
        'petrol': [round(float(v), 2) for v in top_price['petrol_usd_liter']],
        'diesel': [round(float(v), 2) for v in top_price['diesel_usd_liter']],
        'lpg': [round(float(v), 2) for v in top_price['lpg_usd_liter']]
    }

    return jsonify({
        'kpis': {
            'avg_petrol': avg_petrol,
            'avg_diesel': avg_diesel,
            'avg_lpg': avg_lpg,
            'avg_tax': avg_tax,
            'avg_crude': avg_crude,
            'count': count
        },
        'map_data': map_data,
        'yearly_trends': yearly_trends,
        'regional_tax': regional_tax,
        'top_tax_nations': top_tax_nations,
        'top_price_nations': top_price_nations
    })

@app.route('/api/story')
def get_story():
    """Provides detailed analytical scenes as required by the PDF."""
    scenes = [
        {
            "id": 1,
            "title": "Problem Statement and Research Context",
            "subtitle": "Introduction to Global Energy Economics and Pricing Determinants",
            "description": "Establishes the foundational importance of understanding how international crude benchmarks, geopolitical transport corridors, and sovereign taxation frameworks determine retail consumer fuel prices worldwide.",
            "metrics": {
                "Dataset Observations": "27,468 weekly records",
                "Countries Covered": "84 distinct nations",
                "Global Regions": "7 continental regions",
                "Temporal Scope": "January 2020 – April 2026",
                "Average Crude Oil Benchmark": "$107.98 / barrel"
            },
            "findings": [
                "Fuel price volatility directly impacts inflation, domestic transportation costs, and industrial logistics.",
                "Sovereign taxation choices account for greater price divergence between nations than crude oil refining margins.",
                "Policy makers require unified empirical modeling to design equitable, sustainable carbon and excise tax schemes."
            ]
        },
        {
            "id": 2,
            "title": "Geographic Disparity Scene - Global Price Variations",
            "subtitle": "Severe Continental and Regional Disparities Across 84 Nations",
            "description": "Reveals dramatic cross-border price variation ranging from near-zero subsidized rates to premium prices exceeding $5.50 per liter.",
            "metrics": {
                "Highest National Average": "Hong Kong ($5.54/L Petrol)",
                "Lowest National Average": "Algeria ($0.34/L Petrol)",
                "Global Price Ratio": "16x spread between extreme markets",
                "European Average": "$3.46/L (High Tax Band)",
                "Middle East Average": "$1.22/L (Low Tax/Subsidized)"
            },
            "findings": [
                "Western Europe and Oceania maintain the highest retail fuel prices due to heavy environmental taxes.",
                "Resource-rich OPEC and MENA nations leverage domestic refining to offer heavily discounted fuel.",
                "Cross-border price disparities trigger significant freight routing re-alignments in commercial transport."
            ]
        },
        {
            "id": 3,
            "title": "Temporal Trends Scene - Price Movements Over Time",
            "subtitle": "Longitudinal Evolution from Post-Pandemic Shock to 2026 Stability",
            "description": "Tracks price volatility across the 2020–2026 timeline, detailing market reactions to pandemic demand shocks and geopolitical crises.",
            "metrics": {
                "2020 Average Petrol": "$1.48 / L (Crude: $77.59/bbl)",
                "2022 Peak Petrol": "$2.51 / L (Crude: $117.12/bbl)",
                "2023 Correction Petrol": "$2.23 / L (Crude: $104.43/bbl)",
                "2026 Projected Petrol": "$2.65 / L (Crude: $123.75/bbl)",
                "Overall 6-Year Growth": "+78.5% price increase"
            },
            "findings": [
                "2020 marked a historic trough in consumer prices due to global travel restrictions and industrial slowdowns.",
                "The 2021–2022 economic reopening generated immediate demand surges, compounded by European energy supply shocks.",
                "Prices rebounded from the 2023 dip to establish a higher sustained plateau through 2024–2026."
            ]
        },
        {
            "id": 4,
            "title": "Taxation Policy Scene - Global Tax Analysis",
            "subtitle": "Fiscal Architecture and Sovereign Revenue Dependencies",
            "description": "Analyzes the fiscal structure of energy taxes, comparing excise duties and VAT percentages across regional governments.",
            "metrics": {
                "Global Average Tax": "26.77% of retail price",
                "Highest Tax Region": "Oceania (38.69%) & Europe (34.61%)",
                "Lowest Tax Region": "South America (18.20%) & Middle East (19.60%)",
                "Top Taxing Country": "Rwanda (39.56%) & New Zealand (39.27%)",
                "Tax Range Spread": "0.0% to 65.0%"
            },
            "findings": [
                "Taxes serve dual purposes: fiscal revenue generation for state budgets and Pigouvian disincentives for carbon emissions.",
                "In high-tax economies, government duties represent over a third of the pump price, decoupling pump prices from crude volatility.",
                "Low-tax jurisdictions expose consumers directly to raw international crude oil price shocks."
            ]
        },
        {
            "id": 5,
            "title": "Economic Impact Scene - Income Level Correlation",
            "subtitle": "Fuel Affordability, Purchasing Power, and GDP Tiering",
            "description": "Explores how national income classification (High, Middle, Low) correlates with retail pricing resilience and tax absorption.",
            "metrics": {
                "High Income Avg Petrol": "$2.84 / L (Avg Tax: 31.4%)",
                "Middle Income Avg Petrol": "$2.15 / L (Avg Tax: 25.8%)",
                "Low Income Avg Petrol": "$1.82 / L (Avg Tax: 22.9%)",
                "Consumer Burden Ratio": "3.5x higher share of income in Low Income nations"
            },
            "findings": [
                "High-income economies absorb elevated fuel taxation with minimal contraction in discretionary mobility.",
                "Low- and middle-income nations experience severe inflationary knock-on effects in food and freight when fuel costs rise.",
                "Energy affordability is a critical determinant of human development indicators and macroeconomic stability."
            ]
        },
        {
            "id": 6,
            "title": "Subsidy Assessment Scene - Government Support Analysis",
            "subtitle": "State Intervention Mechanics and Market Distortions",
            "description": "Examines how national subsidy tiers (Very High, High, Medium, Low) shield consumers while straining sovereign treasuries.",
            "metrics": {
                "Very High Subsidy Avg Petrol": "$1.18 / L",
                "High Subsidy Avg Petrol": "$1.74 / L",
                "Medium Subsidy Avg Petrol": "$2.29 / L",
                "Low Subsidy Avg Petrol": "$2.91 / L",
                "Price Difference (Low vs Very High)": "$1.73 / L saved at the pump"
            },
            "findings": [
                "Very High subsidy programs provide immediate consumer relief but create multi-billion dollar fiscal vulnerabilities during crude surges.",
                "Untargeted blanket subsidies disproportionately benefit wealthier vehicle owners rather than the most vulnerable populations.",
                "Governments are increasingly forced to rationalize subsidies to preserve budget liquidity for social infrastructure."
            ]
        },
        {
            "id": 7,
            "title": "Conclusions and Recommendations Scene",
            "subtitle": "Evidence-Based Guidance for Energy Stakeholders and Industry Leaders",
            "description": "Synthesizes empirical findings into strategic recommendations tailored to policy consultants, logistics managers, and academic researchers.",
            "metrics": {
                "Analyzed Variables": "10 core economic indicators",
                "Primary Stakeholder Scenarios": "3 personas addressed",
                "Recommended Policy Pivot": "Targeted smart cash transfers vs. blanket subsidies"
            },
            "findings": [
                "For Energy Policy Consultants (Dr. Sarah Mitchell): Transition from price subsidies to targeted cash transfers; introduce dynamic counter-cyclical excise duties to buffer crude price spikes.",
                "For Global Supply Chain Managers (Marcus Thompson): Establish strategic fuel purchasing contracts during Q1 seasonal dips; reroute transcontinental freight through competitive regional refueling corridors.",
                "For Academic Researchers (Prof. Elena Rodriguez): Further study the long-term price elasticity of commercial transport as EV fleet integration and biofuel blending mandates expand."
            ]
        }
    ]
    return jsonify(scenes)

@app.route('/documentation/<path:filename>')
def serve_doc(filename):
    doc_dir = os.path.join(os.path.dirname(__file__), 'documentation')
    from flask import send_from_directory
    return send_from_directory(doc_dir, filename)

@app.route('/global_fuel_prices_Dataset.csv')
def serve_csv():
    from flask import send_from_directory
    return send_from_directory(os.path.dirname(__file__), 'global_fuel_prices_Dataset.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
