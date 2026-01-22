import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

# 1. Professional Page Config
st.set_page_config(page_title="Sundowns Scout AI", page_icon="🇿🇦", layout="wide")

# 2. Unified UI Styling
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .scout-title {
        background-color: #FFDC00;
        color: #00A04A;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-family: 'Arial Black', sans-serif;
        border: 4px solid #00A04A;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .title-plate {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        border-bottom: 3px solid #00A04A;
        padding-bottom: 10px;
        margin-bottom: 30px;
        position: relative;
        z-index: 1; 
    }
    .main-title-text {
        font-size: 28px !important;
        color: #00A04A !important;
        font-weight: 850;
        margin: 0;
    }
    .tech-label {
        font-size: 14px;
        color: #000000;
        font-weight: 600;
        text-transform: uppercase;
        opacity: 0.7;
    }
    div[data-baseweb="popover"], div[data-baseweb="menu"], div[data-baseweb="select"] {
        z-index: 999999 !important; 
    }
    div[data-baseweb="select"] li { color: black !important; }
    div[data-baseweb="slider"] [role="slider"] {
        background-color: #000000 !important;
        border: 2px solid #000000 !important;
    }
    div[data-baseweb="slider"] > div > div > div { background-color: #000000 !important; }
    div[data-testid="stWidgetLabel"] p { color: #000000 !important; font-weight: bold !important; }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important; 
        border-right: 2px solid #EEEEEE;
        overflow: visible !important;
    }
    div.stButton > button:first-child {
        background-color: #00A04A !important;
        color: #FFDC00 !important;
        font-weight: bold !important;
        width: 100% !important;
        border-radius: 10px !important;
        border: none !important;
    }
    .bottom-spacer { height: 300px; }
    </style>
    
    <div class="scout-title">
        <h1>👆 THE BRAZILIANS: SCOUTING INTELLIGENCE</h1>
        <p style="font-weight: bold; margin:0;">Mamelodi Sundowns Performance Analysis Lab</p>
    </div>
    <div class="title-plate">
        <span class="main-title-text">⚽ KA BO YELLOW ELITE: PERFORMANCE TWIN FINDER</span>
        <span class="tech-label">Modern Tech-Focused</span>
    </div>
    """, unsafe_allow_html=True)

# 3. Data Loading
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('master_scouting_data.csv')
    except:
        return pd.DataFrame({
            'player': ['Themba Zwane', 'Teboho Mokoena', 'Peter Shalulile', 'Marcelo Allende', 'Neo Maema', 'Aubrey Modiba'], 
            'position': ['MF', 'MF', 'FW', 'MF', 'MF', 'DF'],
            'goals': [5,4,12,3,2,1], 'assists':[8,6,4,7,5,4], 'sh':[20,35,50,12,15,10], 
            'sot_pct':[40.1, 38.5, 55.2, 30.1, 33.4, 25.0], 'g_sh':[0.11, 0.09, 0.22, 0.08, 0.10, 0.05]
        })
    return df

df = load_data()

# 4. Search Function with Similarity Score
def get_twins(name, weight):
    features = ['goals', 'assists', 'sh', 'sot_pct', 'g_sh']
    if name not in df['player'].values: return None
    
    X = df[features].copy()
    X['assists'] *= weight
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(X_scaled)
    
    idx = df[df['player'] == name].index[0]
    distances, indices = knn.kneighbors(X_scaled[idx].reshape(1, -1), n_neighbors=6)
    
    raw_results = df.iloc[indices.flatten()[1:]].copy()
    raw_distances = distances.flatten()[1:]
    
    # Calculate Similarity Score
    raw_results['similarity'] = [(1 - d) * 100 for d in raw_distances]
    return raw_results

# 5. Radar Chart Function
def create_radar_chart(target_player, twin_player, metrics):
    label_map = {'goals':'Goals', 'assists':'Assists', 'sh':'Shots', 'sot_pct':'Shot Accuracy %', 'g_sh':'Goals/Shot'}
    display_labels = [label_map[m] for m in metrics]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[target_player[m] for m in metrics], theta=display_labels, fill='toself',
        name=f"Target: {target_player['player']}", line_color='#FFDC00', fillcolor='rgba(255, 220, 0, 0.3)'
    ))
    fig.add_trace(go.Scatterpolar(
        r=[twin_player[m] for m in metrics], theta=display_labels, fill='toself',
        name=f"Twin: {twin_player['player']}", line_color='#00A04A', fillcolor='rgba(0, 160, 74, 0.3)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, df[metrics].max().max()])),
        paper_bgcolor='rgba(0,0,0,0)', font=dict(color="black")
    )
    return fig

# 6. Sidebar & Selection
st.sidebar.header("Parameters")
assist_weight = st.sidebar.slider("Assist Importance (Weight)", 1.0, 3.0, 1.6)
target_player = st.selectbox("Select Benchmark Player", df['player'].unique())

# 7. Generate Report
if st.button("Generate Scouting Report"):
    results = get_twins(target_player, assist_weight)
    
    if results is not None:
        st.success(f"Scouting Report for {target_player}")
        
        # --- Data Formatting & Cleaning ---
        # Select columns including the new 'similarity'
        display_df = results[['player', 'position', 'similarity', 'goals', 'assists', 'sh', 'g_sh', 'sot_pct']].copy()
        
        # Formatting
        display_df['goals'] = display_df['goals'].astype(int)
        display_df['assists'] = display_df['assists'].astype(int)
        display_df['sh'] = display_df['sh'].astype(int)
        display_df['sot_pct'] = display_df['sot_pct'].round(2)
        display_df['g_sh'] = display_df['g_sh'].round(2)
        
        # Format similarity as a percentage string for display
        display_df['similarity'] = display_df['similarity'].map("{:,.1f}%".format)
        
        # Rename for UI
        display_df.columns = ['Player', 'Position', 'Match Strength', 'Goals', 'Assists', 'Shots', 'Goals per Shot', 'Shot Accuracy %']
        
        # Style logic: Highlight the first row
        def highlight_top(s):
            return ['background-color: #FFDC00; color: black; font-weight: bold' if s.name == results.index[0] else '' for _ in s]
        
        st.dataframe(display_df.style.apply(highlight_top, axis=1), use_container_width=True)
        
        # --- Radar Chart ---
        st.markdown("<h3 style='color: #00A04A; font-weight: 800; margin-top:30px;'>📊 Performance DNA Match</h3>", unsafe_allow_html=True)
        
        metrics = ['goals', 'assists', 'sh', 'sot_pct', 'g_sh']
        target_data = df[df['player'] == target_player].iloc[0]
        twin_data = results.iloc[0]
        
        st.plotly_chart(create_radar_chart(target_data, twin_data, metrics), use_container_width=True)
        
        # Download
        csv = results.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Scouting Report (CSV)", csv, f'Scout_Report_{target_player}.csv', "text/csv")

st.markdown('<div class="bottom-spacer"></div>', unsafe_allow_html=True)