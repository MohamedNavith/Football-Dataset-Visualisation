from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
import numpy as np

app = Flask(__name__)
CORS(app)  # Enables frontend to talk to backend

# --- CONFIG ---
DATA_DIR = './data'
FILES = {
    'EPL': 'EPL_14_20_players_stat.csv',
    'LaLiga': 'laliga_14_20_players_stat.csv',
    'Bundesliga': 'Bundesliga_14_20_players_stat.csv'
}

# --- DATA LOADER ---
def load_data():
    datasets = []
    print("--- Loading Data ---")
    for league, filename in FILES.items():
        path = os.path.join(DATA_DIR, filename)
        if os.path.exists(path):
            try:
                df = pd.read_csv(path)
                # Normalize columns
                df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
                df['league'] = league
                
                # Fix numeric columns
                cols = ['goals', 'assists', 'minutes', 'xg', 'xa', 'shots', 'xg_per90']
                for c in cols:
                    if c in df.columns:
                        df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0)
                
                datasets.append(df)
                print(f"✅ Loaded {league}: {len(df)} rows")
            except Exception as e:
                print(f"❌ Error loading {league}: {e}")
        else:
            print(f"⚠️ File not found: {filename}")
            
    return pd.concat(datasets, ignore_index=True) if datasets else pd.DataFrame()

# Load data once at startup
df = load_data()

# --- ROUTES ---

@app.route('/')
def home():
    return "<h1>⚽ Backend is Running!</h1><p>Go to frontend (localhost:5173) to see the UI.</p>"

@app.route('/api/stats', methods=['GET'])
def get_stats():
    global df
    if df.empty: return jsonify({'error': 'No data loaded'}), 500

    # Filters
    league = request.args.get('league')
    search = request.args.get('search', '').lower()
    
    filtered = df.copy()
    if league and league != 'All':
        filtered = filtered[filtered['league'] == league]
    if search:
        filtered = filtered[filtered['player_name'].str.lower().str.contains(search)]

    # Stats for Dashboard
    total_players = len(filtered)
    total_goals = int(filtered['goals'].sum()) if not filtered.empty else 0
    avg_xg = round(filtered[filtered['minutes'] > 500]['xg_per90'].mean(), 2) if not filtered.empty else 0

    # Top Scorers Chart Data
    top_scorers = []
    if not filtered.empty:
        top_scorers = filtered.nlargest(10, 'goals')[['player_name', 'goals', 'league']].to_dict(orient='records')

    # Scatter Chart Data (Goals vs xG)
    scatter_data = []
    if not filtered.empty:
        # Limit scatter points for performance
        scatter_df = filtered[filtered['goals'] > 5]
        scatter_data = scatter_df[['player_name', 'goals', 'xg', 'league']].to_dict(orient='records')

    # Table Data (Pagination)
    page = int(request.args.get('page', 1))
    limit = 50
    start = (page - 1) * limit
    end = start + limit
    table_data = filtered.iloc[start:end].to_dict(orient='records')

    return jsonify({
        'meta': { 'total_players': total_players, 'total_goals': total_goals, 'avg_xg': avg_xg },
        'charts': { 'top_scorers': top_scorers, 'scatter': scatter_data },
        'table': table_data
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)