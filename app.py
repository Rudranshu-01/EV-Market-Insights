from pathlib import Path
from functools import lru_cache
import os
import pandas as pd
from flask import Flask, render_template, request

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data' / 'compressed_data-2.csv.gz'
app = Flask(__name__)
DASHBOARD_URL = os.getenv('TABLEAU_DASHBOARD_URL', 'https://public.tableau.com/views/EV_Market_Performance_Market_Story_2026-10-25/EVExecutiveDashboard?:showVizHome=no')
STORY_URL = os.getenv('TABLEAU_STORY_URL', 'https://public.tableau.com/views/EV_Market_Performance_Green_Executive_Refresh/Story2?:showVizHome=no')

@lru_cache(maxsize=1)
def load_data():
    cols = ['manufacturer','model_year','market_region','category','battery_type','annual_sales_units','range_km','price_usd','customer_rating']
    df = pd.read_csv(DATA, usecols=cols)
    for col in ['annual_sales_units','range_km','price_usd','customer_rating']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def summarize(df):
    def series(col, metric='annual_sales_units', limit=8):
        grouped = df.groupby(col, dropna=True)[metric].sum().nlargest(limit)
        return [{'label': str(k), 'value': round(float(v), 1)} for k, v in grouped.items()]
    sales = df['annual_sales_units'].sum()
    return {
        'rows': f'{len(df):,}', 'sales': f'{sales:,.0f}',
        'range': f"{df['range_km'].mean():,.0f}" if df['range_km'].notna().any() else 'N/A',
        'rating': f"{df['customer_rating'].mean():.2f}" if df['customer_rating'].notna().any() else 'N/A',
        'manufacturers': series('manufacturer'), 'regions': series('market_region'),
        'categories': series('category'), 'battery': series('battery_type'),
        'years': [{'label': str(k), 'value': round(float(v), 1)} for k,v in df.groupby('model_year')['annual_sales_units'].sum().sort_index().items()]
    }

@app.route('/')
def index():
    df = load_data()
    regions = sorted(df['market_region'].dropna().astype(str).unique().tolist())
    selected = request.args.get('region', '')
    if selected in regions:
        df = df[df['market_region'].astype(str) == selected]
    else:
        selected = ''
    return render_template('index.html', stats=summarize(df), regions=regions, selected=selected,
                           dashboard_url=DASHBOARD_URL, story_url=STORY_URL)

@app.route('/health')
def health():
    return {'status': 'ok', 'data_available': DATA.exists()}

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=int(os.getenv('PORT','5000')))
