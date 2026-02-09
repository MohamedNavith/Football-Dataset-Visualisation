import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Football Analytics Pro",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for UI Polish
st.markdown("""
    <style>
    /* Dark Theme & Typography */
    .stApp { background-color: #0e1117; }
    h1, h2, h3 { color: #3b82f6 !important; font-family: 'Segoe UI', sans-serif; }
    
    /* Metrics Styling */
    div[data-testid="stMetricValue"] { font-size: 24px; color: #ffffff; }
    div[data-testid="stMetricLabel"] { color: #94a3b8; }
    .stMetric { background-color: #1e293b; padding: 10px; border-radius: 8px; border: 1px solid #334155; }
    
    /* Search Box Styling */
    .stSelectbox div[data-baseweb="select"] { cursor: pointer; }
    
    /* Expander Styling */
    .streamlit-expanderHeader { background-color: #1e293b; color: white; border-radius: 5px; }
    
    /* Highlight Box Styling */
    .highlight-box { padding: 15px; border-radius: 10px; background-color: #1e293b; border-left: 5px solid #3b82f6; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADER ---
@st.cache_data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(script_dir, 'backend', 'data'),
        os.path.join(script_dir, 'data'),
        r"F:\graph project\Football-Dataset-Visualisation\backend\data"
    ]
    
    data_dir = None
    for path in possible_paths:
        if os.path.exists(path):
            data_dir = path
            break
            
    if not data_dir:
        return None, "Data folder not found."

    files = {
        'EPL': 'EPL_14_20_players_stat.csv',
        'LaLiga': 'laliga_14_20_players_stat.csv',
        'Bundesliga': 'Bundesliga_14_20_players_stat.csv'
    }
    
    datasets = []
    for league, filename in files.items():
        file_path = os.path.join(data_dir, filename)
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
                df['league'] = league
                
                # Numeric cleaning
                cols = ['goals', 'assists', 'minutes', 'xg', 'xa', 'shots', 'goals_per90', 'assists_per90', 'xg_per90', 'xa_per90']
                for col in cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
                
                # Standardize Positions
                df['position'] = df['position'].astype(str)
                
                datasets.append(df)
            except:
                continue
    
    if not datasets: return None, "No files loaded."
    return pd.concat(datasets, ignore_index=True), None

df, error_msg = load_data()

if df is None or df.empty:
    st.error(f"🚨 Error: {error_msg}")
    st.stop()

# --- 3. SIDEBAR FILTERS ---
st.sidebar.title("⚽ Analytics Pro")

# 1. League Filter
leagues = ['All'] + sorted(df['league'].unique().tolist())
selected_league = st.sidebar.selectbox("📅 Select League", leagues)

# Filter Dataset based on League
league_filtered_df = df if selected_league == 'All' else df[df['league'] == selected_league]

# 2. Team Filter
teams = ['All'] + sorted(league_filtered_df['team_name'].unique().tolist())
selected_team = st.sidebar.selectbox("🛡️ Select Team", teams)

if selected_team != 'All':
    team_filtered_df = league_filtered_df[league_filtered_df['team_name'] == selected_team]
else:
    team_filtered_df = league_filtered_df

# 3. Position Filter
positions = ['All'] + sorted(df['position'].unique().tolist())
selected_pos = st.sidebar.selectbox("📍 Select Position", positions)

# Final Filtering
filtered_df = team_filtered_df.copy()
if selected_pos != 'All':
    filtered_df = filtered_df[filtered_df['position'] == selected_pos]

st.sidebar.markdown("---")

# 4. Smart Search
all_player_names = sorted(filtered_df['player_name'].unique().tolist())
searched_player = st.sidebar.selectbox(
    "🔍 Search Player (Type to find)", 
    ['None'] + all_player_names,
    index=0,
    help="Type a name to instantly find stats."
)

# Apply Search Filter
if searched_player != 'None':
    filtered_df = filtered_df[filtered_df['player_name'] == searched_player]

# --- 4. DASHBOARD HEADER ---
st.title(f"📊 {selected_league} Analysis")

# "Season Report" (Formerly AI Insights - Restored MVP/Clinical Labels)
with st.expander("💡 Season Report (Key Performers)", expanded=True):
    if not filtered_df.empty:
        top_scorer = filtered_df.loc[filtered_df['goals'].idxmax()]
        top_assister = filtered_df.loc[filtered_df['assists'].idxmax()]
        filtered_df['efficiency'] = filtered_df['goals'] - filtered_df['xg']
        most_clinical = filtered_df.loc[filtered_df['efficiency'].idxmax()]
        
        c1, c2, c3 = st.columns(3)
        c1.info(f"**MVP (Goals):** {top_scorer['player_name']} ({top_scorer['goals']} goals)")
        c2.success(f"**Clinical Finisher:** {most_clinical['player_name']} (+{most_clinical['efficiency']:.1f} goals vs xG)")
        c3.info(f"**Top Creator:** {top_assister['player_name']} ({top_assister['assists']} assists)")
    else:
        st.write("No data available for insights.")

# --- 5. TABS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Team / Player Analysis", "⚔️ Player Comparison", "📈 Growth & Trends", "📄 Data Grid"])

# --- TAB 1: TEAM / PLAYER ANALYSIS ---
with tab1:
    # 1. PLAYER SEARCH VIEW (Restored Detailed Text)
    if searched_player != 'None':
        p = filtered_df.iloc[0]
        
        # Calculate Logic
        est_games = int(p['minutes'] / 90)
        performance_verdict = "Squad Rotation Player"
        if p['goals'] > 50 or p['assists'] > 30: performance_verdict = "League Legend 🌟"
        elif p['goals'] > 20 or p['assists'] > 15: performance_verdict = "Key Starter ✅"
        
        efficiency_text = "better" if p['goals'] > p['xg'] else "lower"
        
        # Display the "Old" Rich Text Style (without "AI" label)
        st.subheader(f"📝 Statistical Summary: {p['player_name']}")
        st.markdown(f"""
        <div class="highlight-box">
        <b>{p['player_name']}</b> has been a significant presence for <b>{p['team_name']}</b>.
        Over the analyzed period (2014-2020), they played approximately <b>{est_games} full games</b> ({p['minutes']} mins).
        <br><br>
        They contributed <b>{p['goals']} goals</b> and <b>{p['assists']} assists</b>. 
        Their finishing was <b>{efficiency_text}</b> than expected (xG: {p['xg']:.1f}), 
        indicating their quality in front of goal.
        <br><br>
        <b>Verdict:</b> Based on aggregate data, they performed as a <b>{performance_verdict}</b>.
        </div>
        """, unsafe_allow_html=True)

    # 2. TEAM VIEW (If Team Selected & No Player Searched)
    elif selected_team != 'All':
        st.subheader(f"🛡️ {selected_team}: Scoring Distribution")
        st.caption("How goals were shared among the squad (2014-2020).")
        
        team_players = team_filtered_df.sort_values(by='goals', ascending=True)
        team_players = team_players[team_players['goals'] > 0]
        
        fig_team = px.bar(
            team_players, 
            x='goals', y='player_name', orientation='h',
            color='goals', color_continuous_scale='Viridis',
            title=f"Total Goals by Player ({selected_team})",
            height=max(500, len(team_players) * 20)
        )
        fig_team.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
        st.plotly_chart(fig_team, use_container_width=True)

    # 3. GENERAL LEAGUE VIEW
    else:
        st.subheader(f"1. {selected_pos if selected_pos != 'All' else 'All Positions'} Performance Matrix")
        y_metric = 'goals_per90'
        x_metric = 'assists_per90'
        
        fig = px.scatter(
            filtered_df[filtered_df['minutes'] > 500],
            x=x_metric, y=y_metric,
            color='position', size='minutes',
            hover_data=['player_name', 'team_name', 'goals', 'assists'],
            color_discrete_sequence=px.colors.qualitative.Bold,
            title=f"{y_metric} vs {x_metric} (Bubble Size = Minutes Played)",
            height=550
        )
        fig.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            st.subheader("2. Top Performers (Goals)")
            top_n = filtered_df.nlargest(10, 'goals')
            fig_bar = px.bar(top_n, x='goals', y='player_name', orientation='h', color='goals', color_continuous_scale='Viridis')
            fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig_bar, use_container_width=True)
        
        with c2:
            st.subheader("3. xG Distribution")
            fig_hist = px.histogram(filtered_df, x='xg', nbins=20, title="Expected Goals Spread", color_discrete_sequence=['#3b82f6'])
            fig_hist.update_layout(plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white')
            st.plotly_chart(fig_hist, use_container_width=True)

# --- TAB 2: PLAYER COMPARISON ---
with tab2:
    st.header("⚔️ Player Face-Off")
    
    all_players = sorted(df['player_name'].unique().tolist())
    c_sel1, c_sel2 = st.columns(2)
    p1_name = c_sel1.selectbox("Select Player A", all_players, index=0)
    p2_name = c_sel2.selectbox("Select Player B", all_players, index=1)
    
    if p1_name and p2_name:
        p1 = df[df['player_name'] == p1_name].iloc[0]
        p2 = df[df['player_name'] == p2_name].iloc[0]
        
        st.markdown("### 📊 Tale of the Tape")
        metrics = {"Goals": "goals", "Assists": "assists", "xG": "xg", "Shots": "shots", "Mins": "minutes"}
        cols = st.columns(len(metrics))
        for i, (label, key) in enumerate(metrics.items()):
            v1 = p1[key]
            v2 = p2[key]
            color1 = "green" if v1 > v2 else "white"
            color2 = "green" if v2 > v1 else "white"
            with cols[i]:
                st.markdown(f"<div style='text-align:center; font-size:14px; color:#888'>{label}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold; color:{color1}'>{v1}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; color:#555'>vs</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='text-align:center; font-size:20px; font-weight:bold; color:{color2}'>{v2}</div>", unsafe_allow_html=True)

        st.markdown("---")

        st.subheader("🧠 Ability Radar (Percentile Rank)")
        radar_keys = ['goals_per90', 'assists_per90', 'xg_per90', 'xa_per90', 'shots_per90']
        radar_labels = ['Goals/90', 'Assists/90', 'xG/90', 'xA/90', 'Shots/90']
        
        def get_rank(val, col):
            return df[col].rank(pct=True)[df[col] == val].iloc[0] * 100
            
        r1 = [get_rank(p1[k], k) for k in radar_keys]
        r2 = [get_rank(p2[k], k) for k in radar_keys]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=r1, theta=radar_labels, fill='toself', name=p1_name, line_color='#10b981'))
        fig_radar.add_trace(go.Scatterpolar(r=r2, theta=radar_labels, fill='toself', name=p2_name, line_color='#f43f5e'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False), bgcolor='#1e293b'),
            paper_bgcolor='#0e1117', font_color='white', height=500
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# --- TAB 3: GROWTH & TRENDS ---
with tab3:
    st.header("📈 Cumulative Impact Analysis")
    st.info("ℹ️ Comparing Player Performance vs Team & League Averages (2014-2020 Aggregate).")
    
    if searched_player != 'None':
        p = filtered_df.iloc[0]
        team_name = p['team_name']
        league_avg = df[['goals', 'assists', 'xg', 'xa']].mean()
        team_avg = df[df['team_name'] == team_name][['goals', 'assists', 'xg', 'xa']].mean()
        
        categories = ['Goals', 'Assists', 'xG', 'xA']
        p_stats = [p['goals'], p['assists'], p['xg'], p['xa']]
        t_stats = [team_avg['goals'], team_avg['assists'], team_avg['xg'], team_avg['xa']]
        l_stats = [league_avg['goals'], league_avg['assists'], league_avg['xg'], league_avg['xa']]

        # Combo Chart: Bars for Player/Team, Line for League Baseline
        fig_growth = go.Figure()
        fig_growth.add_trace(go.Bar(name=p['player_name'], x=categories, y=p_stats, marker_color='#3b82f6'))
        fig_growth.add_trace(go.Bar(name=f"{team_name} Avg", x=categories, y=t_stats, marker_color='#10b981', opacity=0.6))
        fig_growth.add_trace(go.Scatter(name='League Avg', x=categories, y=l_stats, mode='lines+markers', line=dict(color='#ef4444', width=3, dash='dash')))

        fig_growth.update_layout(
            barmode='group', 
            plot_bgcolor='#0e1117', paper_bgcolor='#0e1117', font_color='white', 
            title=f"Performance Hierarchy: {p['player_name']} vs Team vs League",
            height=500
        )
        st.plotly_chart(fig_growth, use_container_width=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.metric("vs Team Avg (Goals)", f"{p['goals'] - team_avg['goals']:.1f}", help="Difference from average teammate")
        with c2:
            st.metric("vs League Avg (Goals)", f"{p['goals'] - league_avg['goals']:.1f}", help="Difference from average league player")
    else:
        st.write("🔍 **Select a player from the sidebar search to see their impact analysis.**")

# --- TAB 4: DATA GRID ---
with tab4:
    st.dataframe(filtered_df, use_container_width=True, height=600)