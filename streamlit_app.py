import streamlit as st
import random
import time
import sys
import os
import textwrap

# Add backend to path so we can import model
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
try:
    from model import predict_risk
except ImportError:
    # Fallback if running from root without backend in path
    sys.path.append('backend')
    from model import predict_risk

# --- Constants ---
CONDITIONS = {
    'SPEED': [30, 40, 50, 60, 70, 80, 90, 100, 110, 120],
    'ROAD_TYPE': ['Highway', 'Urban', 'Rural'],
    'WEATHER': ['Clear', 'Rain', 'Fog', 'Snow'],
    'LIGHTING': ['Day', 'Night', 'Dusk']
}

MISSIONS = [
    "Urgent medical delivery to the city hospital.",
    "Transporting fragile cargo across the state.",
    "Family road trip to the mountains.",
    "Late night commute home after a double shift.",
    "Escaping a sudden zombie outbreak.",
    "High-speed pursuit of a fugitive."
]

# --- Logic ---
def generate_scenario():
    speed = random.choice(CONDITIONS['SPEED'])
    weather = random.choice(CONDITIONS['WEATHER'])
    lighting = random.choice(CONDITIONS['LIGHTING'])
    road_type = random.choice(CONDITIONS['ROAD_TYPE'])
    curvature = round(random.random(), 2)

    scenario = {
        'speed': speed,
        'weather': weather,
        'lighting': lighting,
        'roadType': road_type,
        'curvature': curvature,
    }
    
    # Get risk from XGBoost model
    try:
        scenario['riskScore'] = predict_risk(scenario)
    except Exception as e:
        st.error(f"Model Error: {e}")
        scenario['riskScore'] = 50 
        
    return scenario

def generate_round():
    left = generate_scenario()
    right = generate_scenario()
    
    # Ensure distinct risks
    tries = 0
    while abs(left['riskScore'] - right['riskScore']) < 5 and tries < 5:
        right = generate_scenario()
        tries += 1
        
    mission = random.choice(MISSIONS)
    return {'left': left, 'right': right, 'mission': mission}

# --- UI ---
st.set_page_config(page_title="Road Safety Quiz", page_icon="🚗", layout="wide")

# Custom CSS for "Premium" Card feel
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Global Background */
    .stApp {
        background-color: #0f1115;
        color: #ffffff;
    }
    
    /* Remove standard Streamlit padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1000px;
    }

    /* Scoreboard */
    .scoreboard {
        display: flex;
        justify-content: space-between;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.1);
        padding: 1rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        align-items: center;
    }
    
    /* Mission Box */
    .mission-box {
        text-align: center;
        margin-bottom: 3rem;
        padding: 1rem;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        border-top: 1px solid rgba(255,255,255,0.1);
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    /* Custom Card HTML */
    .road-card-visual {
        background-color: #181a20;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 2rem;
        height: 100%;
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        padding-bottom: 1rem;
    }
    
    .stat-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0;
    }
    
    .stat-label {
        color: #9ca3af;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 0.9rem;
    }
    
    .stat-value {
        color: white;
        font-weight: 600;
        font-size: 1rem;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3rem;
        background: #3b82f6;
        color: white;
        border: none;
        font-weight: 600;
        font-size: 0.9rem;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 1rem;
        transition: all 0.2s;
    }
    .stButton>button:hover {
        background: #2563eb;
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
    }

    /* Hide generic elements */
    [data-testid="stHeader"] {display: none;}
    [data-testid="stToolbar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# Session State
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'streak' not in st.session_state:
    st.session_state.streak = 0
if 'round_data' not in st.session_state:
    st.session_state.round_data = generate_round()
if 'result' not in st.session_state:
    st.session_state.result = None 

# --- HEADER (HTML) ---
st.markdown("""
<div style="text-align: center; margin-bottom: 2rem;">
    <h1 style='font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #60a5fa, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.5rem;'>Road Safety Quiz</h1>
    <p style='color: #9ca3af;'>Test your intuition. Which road is safer?</p>
</div>
""", unsafe_allow_html=True)

# --- SCOREBOARD (HTML) ---
col1, col2 = st.columns([1, 19]) # Hack to center? No, just use div
st.markdown(f"""
<div class="scoreboard">
    <div style="display: flex; gap: 1.5rem;">
        <div style="display: flex; gap: 0.5rem; align-items: center;">
            <span style="color: #9ca3af;">🏆</span> 
            <span style="color: #9ca3af; font-size: 0.9rem;">Score</span>
            <span style="font-weight: 700; font-size: 1.1rem;">{st.session_state.score}</span>
        </div>
        <div style="display: flex; gap: 0.5rem; align-items: center;">
            <span style="color: #10b981;">✅</span>
            <span style="color: #9ca3af; font-size: 0.9rem;">Streak</span>
            <span style="font-weight: 700; font-size: 1.1rem;">{st.session_state.streak}</span>
        </div>
    </div>
    <div style="color: #9ca3af; font-size: 0.9rem; cursor: pointer;">Exit Game</div>
</div>
""", unsafe_allow_html=True)

# --- MISSION (HTML) ---
st.markdown(f"""
<div class="mission-box">
    <div style="color: #3b82f6; font-size: 0.8rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem;">Current Mission</div>
    <div style="font-size: 1.2rem; font-weight: 500;">📍 {st.session_state.round_data['mission']}</div>
</div>
""", unsafe_allow_html=True)

# --- GAME AREA ---
rd = st.session_state.round_data
res = st.session_state.result

# Icons map (Text fallback for Streamlit)
ICONS = {'Sun': '☀️', 'Moon': '🌙', 'CloudRain': '🌧️', 'CloudFog': '🌫️', 'Snowflake': '❄️'} # Simplified

def render_card_html(scenario, is_winner=None, show_result=False):
    # Determine Border Color
    border_style = "border: 1px solid rgba(255, 255, 255, 0.1);"
    bg_style = "background-color: #181a20;"
    
    if show_result:
        if is_winner:
            border_style = "border: 2px solid #10b981;"
            bg_style = "background-color: rgba(16, 185, 129, 0.05);"
        else:
            border_style = "border: 2px solid #ef4444;"
            bg_style = "background-color: rgba(239, 68, 68, 0.05);"

    icon = "☀️"
    if scenario['weather'] == 'Rain': icon = "🌧️"
    if scenario['weather'] == 'Fog': icon = "🌫️"
    if scenario['weather'] == 'Snow': icon = "❄️"
    
    lighting_icon = "☀️" if scenario['lighting'] == 'Day' else "🌙"

    # HTML Template - Flattened to avoid Markdown code block bugs
    html = f"""
    <div class="road-card-visual" style="{border_style} {bg_style}">
        <div class="card-header">
            <div style="display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <span style="font-size: 1.2rem; font-weight: 600;">{scenario['weather']}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.5rem; color: #9ca3af; font-size: 0.9rem;">
                <span>{lighting_icon}</span>
                <span>{scenario['lighting']}</span>
            </div>
        </div>
        <div>
            <div class="stat-row">
                <div class="stat-label">⚡ Speed Limit</div>
                <div class="stat-value">{scenario['speed']} mph</div>
            </div>
            <div class="stat-row">
                <div class="stat-label">🧭 Road Type</div>
                <div class="stat-value">{scenario['roadType']}</div>
            </div>
            <div class="stat-row">
                <div class="stat-label">⚠️ Curvature</div>
                <div class="stat-value">{int(scenario['curvature']*100)}%</div>
            </div>
        </div>
    """
    # Flatten: Remove newlines and leading spaces
    html = html.replace("\n", "").replace("    ", "")

    if show_result:
        score_color = "#10b981" if is_winner else "#ef4444"
        res_html = f"""
        <div style="margin-top: 1rem; text-align: center; background: {score_color}10; border-radius: 8px; padding: 1rem; border: 1px solid {score_color};">
            <div style="color: #9ca3af; font-size: 0.9rem;">Predicted Risk</div>
            <div style="font-size: 2rem; font-weight: 800; color: {score_color};">{int(scenario['riskScore'])}%</div>
        </div>
        """
        html += res_html.replace("\n", "").replace("    ", "")
        
    html += "</div>"
    return html

# Logic for handling choice
def handle_choice(chose_left):
    left_risk = rd['left']['riskScore']
    right_risk = rd['right']['riskScore']
    left_is_safer = left_risk < right_risk
    
    is_correct = (chose_left and left_is_safer) or (not chose_left and not left_is_safer)
    
    winner_is_left = left_is_safer
    
    if is_correct:
        st.session_state.score += 100 + (st.session_state.streak * 10)
        st.session_state.streak += 1
        st.success("Correct! You chose the safer road.")
    else:
        st.session_state.streak = 0
        st.error("Wrong! Hidden risks were higher.")
        
    st.session_state.result = {'correct': is_correct, 'winner': winner_is_left}
    st.rerun()

# Columns: Card | vs | Card
c_left, c_mid, c_right = st.columns([10, 2, 10])

with c_left:
    is_left_winner = res['winner'] if res else False
    st.markdown(render_card_html(rd['left'], is_left_winner if res else None, res is not None), unsafe_allow_html=True)
    
    if res is None:
        if st.button("SELECT ROUTE", key="left_btn"):
            handle_choice(True)

with c_mid:
    st.markdown("<div style='height: 300px; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 800; color: #9ca3af;'>VS</div>", unsafe_allow_html=True)

with c_right:
    is_right_winner = not res['winner'] if res else False
    st.markdown(render_card_html(rd['right'], is_right_winner if res else None, res is not None), unsafe_allow_html=True)
    
    if res is None:
        if st.button("SELECT ROUTE", key="right_btn"):
            handle_choice(False)

# Next Round
if res is not None:
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        if st.button("NEXT SCENARIO ➡️", type="primary"):
            st.session_state.round_data = generate_round()
            st.session_state.result = None
            st.rerun()
