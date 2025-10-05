import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random

# Page config
st.set_page_config(
    page_title="Shambabyte - Farm Through History 🌾",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gaming-style CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: white;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Gaming Header */
    .game-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.4);
        margin-bottom: 1.5rem;
        border: 2px solid rgba(255,255,255,0.1);
    }
    
    /* XP Bar */
    .xp-bar-container {
        background: rgba(255,255,255,0.1);
        border-radius: 20px;
        height: 30px;
        padding: 3px;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    .xp-bar {
        background: linear-gradient(90deg, #FFD700 0%, #FFA500 100%);
        height: 100%;
        border-radius: 17px;
        transition: width 0.5s ease;
        box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        color: #000;
    }
    
    /* Stat Cards */
    .stat-card {
        background: rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        padding: 1rem;
        border-radius: 12px;
        border: 2px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        border-color: #667eea;
    }
    
    /* Era Cards - Gaming Style */
    .era-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 20px;
        border: 3px solid rgba(255,255,255,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .era-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .era-card:hover {
        transform: scale(1.05);
        border-color: #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
    }
    
    .era-card-locked {
        opacity: 0.4;
        filter: grayscale(100%);
    }
    
    /* Disaster Alert */
    .disaster-alert {
        background: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border: 3px solid #FF0000;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.5);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.5); }
        50% { box-shadow: 0 0 50px rgba(255, 0, 0, 0.8); }
    }
    
    /* Skill Tree Item */
    .skill-item {
        background: rgba(102, 126, 234, 0.2);
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid #667eea;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .skill-item:hover {
        background: rgba(102, 126, 234, 0.4);
        transform: translateX(10px);
    }
    
    .skill-unlocked {
        border-color: #FFD700;
        background: rgba(255, 215, 0, 0.2);
    }
    
    /* Map Container */
    .map-container {
        background: rgba(0,0,0,0.3);
        padding: 1rem;
        border-radius: 15px;
        border: 2px solid rgba(255,255,255,0.2);
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    
    /* Achievement Popup */
    .achievement-popup {
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        color: #000;
        padding: 1.5rem;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 0 40px rgba(255, 215, 0, 0.8);
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from { transform: translateY(-100px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

# Initialize Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

# NASA Resources
NASA_RESOURCES = {
    "Learning": {
        "Earth Observatory": "https://earthobservatory.nasa.gov/search?q=agriculture",
        "ARSET Agriculture Training": "https://appliedsciences.nasa.gov/what-we-do/capacity-building/arset/arset-agriculture-trainings",
        "Backgrounders": "https://www.earthdata.nasa.gov/learn/backgrounders",
        "Community Forum": "https://forum.earthdata.nasa.gov/"
    },
    "Data & Tools": {
        "Earth Data Portal": "https://urs.earthdata.nasa.gov/",
        "CropCASMA": "https://nassgeo.csiss.gmu.edu/CropCASMA/",
        "Earth Dashboard": "https://www.earthdata.nasa.gov/dashboard/",
        "GLAM": "https://glam1.gsfc.nasa.gov/",
        "Worldview": "https://worldview.earthdata.nasa.gov/",
        "Harvest Portal": "https://www.harvestportal.org/"
    },
    "Disaster Resources": {
        "Floods Data": "https://www.earthdata.nasa.gov/learn/pathfinders/disasters/floods-data-pathfinder",
        "Heat Events": "https://www.earthdata.nasa.gov/topics/human-dimensions/heat",
        "Agriculture & Water": "https://www.earthdata.nasa.gov/learn/pathfinders/agricultural-and-water-resources-data-pathfinder"
    }
}

# Disaster Types with emojis
DISASTERS = {
    "drought": {"emoji": "🏜️", "color": "#FF6B00", "severity": "high"},
    "flood": {"emoji": "🌊", "color": "#0096FF", "severity": "high"},
    "heatwave": {"emoji": "🔥", "color": "#FF0000", "severity": "medium"},
    "frost": {"emoji": "❄️", "color": "#00FFFF", "severity": "medium"},
    "locust": {"emoji": "🦗", "color": "#8B4513", "severity": "critical"},
    "windstorm": {"emoji": "🌪️", "color": "#808080", "severity": "medium"}
}

# Skills System
SKILLS = {
    "water_master": {"name": "💧 Water Master", "desc": "Reduce water usage by 20%", "xp_cost": 100},
    "weather_prophet": {"name": "🔮 Weather Prophet", "desc": "See 3 extra days forecast", "xp_cost": 200},
    "disaster_shield": {"name": "🛡️ Disaster Shield", "desc": "-30% damage from disasters", "xp_cost": 300},
    "fast_growth": {"name": "⚡ Fast Growth", "desc": "Crops grow 50% faster", "xp_cost": 250},
    "golden_harvest": {"name": "💰 Golden Harvest", "desc": "+50% crop value", "xp_cost": 400},
    "ai_insight": {"name": "🤖 AI Insight", "desc": "Free AI advice 3x per day", "xp_cost": 150},
    "satellite_vision": {"name": "🛰️ Satellite Vision", "desc": "Real-time NDVI updates", "xp_cost": 350},
    "drought_survivor": {"name": "🏜️ Drought Survivor", "desc": "Survive droughts easier", "xp_cost": 300}
}

# Enhanced Era Configuration
ERAS = {
    "1960s": {
        "name": "1960s Independence Era",
        "icon": "🌱",
        "color": "#4CAF50",
        "description": "The dawn of independence and agricultural modernization",
        "years": "1960-1969",
        "total_events": 8,
        "data_range": (0, 73),
        "unlocked": True,
        "disasters": ["drought", "locust"],
        "historical_context": "Post-independence Kenya focuses on food security and land reform"
    },
    "1980s": {
        "name": "1980s Green Revolution",
        "icon": "🚜",
        "color": "#FF9800",
        "description": "New technologies transform Kenyan farms",
        "years": "1980-1989",
        "total_events": 10,
        "data_range": (74, 146),
        "unlocked": False,
        "disasters": ["drought", "flood", "locust"],
        "historical_context": "Introduction of high-yield varieties and mechanization"
    },
    "2000s": {
        "name": "2000s Digital Age",
        "icon": "📱",
        "color": "#2196F3",
        "description": "Technology meets traditional farming",
        "years": "2000-2009",
        "total_events": 12,
        "data_range": (147, 219),
        "unlocked": False,
        "disasters": ["drought", "flood", "heatwave"],
        "historical_context": "Mobile money, GPS, and satellite data revolutionize farming"
    },
    "2010s": {
        "name": "2010s Tech Boom",
        "icon": "💻",
        "color": "#9C27B0",
        "description": "Smartphones, data analytics, and precision agriculture",
        "years": "2010-2019",
        "total_events": 14,
        "data_range": (220, 292),
        "unlocked": False,
        "disasters": ["drought", "flood", "heatwave", "windstorm"],
        "historical_context": "Big data, IoT sensors, and AI predictions transform agriculture"
    },
    "2020s": {
        "name": "2020s Climate Action",
        "icon": "🌍",
        "color": "#00BCD4",
        "description": "Fighting climate change through smart farming",
        "years": "2020-2025",
        "total_events": 10,
        "data_range": (293, 366),
        "unlocked": False,
        "disasters": ["drought", "flood", "heatwave", "frost", "windstorm"],
        "historical_context": "Climate-smart agriculture and sustainable practices lead the way"
    }
}

# Load NASA data
@st.cache_data
def load_nasa_data():
    try:
        df = pd.read_csv('nasa_data.csv')
        df['day'] = range(len(df))
        return df
    except:
        st.error("⚠️ NASA data file not found!")
        return None

# Initialize session state
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_screen = 'welcome'
        st.session_state.current_era = None
        st.session_state.player_name = ""
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.xp_to_next_level = 100
        st.session_state.total_score = 0
        st.session_state.language = 'English'
        
        # Era progress
        st.session_state.era_progress = {
            era: {"unlocked": ERAS[era]["unlocked"], "events_completed": 0, "completed": False}
            for era in ERAS.keys()
        }
        
        # Game state
        st.session_state.day = 0
        st.session_state.money = 1000
        st.session_state.seeds = 50
        st.session_state.water = 100
        st.session_state.fertilizer = 20
        st.session_state.farm_health = 100
        st.session_state.unlocked_skills = []
        st.session_state.upcoming_disasters = []
        st.session_state.disaster_warnings = []
        st.session_state.ai_uses_today = 0
        st.session_state.last_achievement = None
        
        # Map data
        st.session_state.map_markers = []
        st.session_state.current_location = {"lat": -1.286389, "lon": 36.817223, "name": "Nairobi, Kenya"}

def predict_disasters(nasa_data, current_day, era):
    """Predict upcoming disasters based on weather patterns"""
    disasters = []
    
    # Look ahead 7 days
    for i in range(1, 8):
        if current_day + i >= len(nasa_data):
            break
            
        weather = nasa_data.iloc[current_day + i]
        
        # Drought detection
        if weather['PRECTOTCORR'] < 0.5 and weather['GWETPROF'] < 0.3:
            disasters.append({
                "type": "drought",
                "day": i,
                "severity": "high" if weather['GWETPROF'] < 0.2 else "medium",
                "message": f"🏜️ Drought warning! Day +{i}: Very low rainfall expected ({weather['PRECTOTCORR']:.2f}mm)"
            })
        
        # Flood detection
        if weather['PRECTOTCORR'] > 20:
            disasters.append({
                "type": "flood",
                "day": i,
                "severity": "high",
                "message": f"🌊 Flood alert! Day +{i}: Heavy rainfall incoming ({weather['PRECTOTCORR']:.1f}mm)"
            })
        
        # Heatwave detection
        if weather['T2M_MAX'] > 35:
            disasters.append({
                "type": "heatwave",
                "day": i,
                "severity": "medium" if weather['T2M_MAX'] < 40 else "high",
                "message": f"🔥 Heatwave warning! Day +{i}: Extreme heat expected ({weather['T2M_MAX']:.1f}°C)"
            })
        
        # Frost detection
        if weather['T2M_MIN'] < 5:
            disasters.append({
                "type": "frost",
                "day": i,
                "severity": "medium",
                "message": f"❄️ Frost warning! Day +{i}: Cold snap coming ({weather['T2M_MIN']:.1f}°C)"
            })
    
    # Random disaster events based on era
    if random.random() < 0.05 and "locust" in ERAS[era]["disasters"]:
        disasters.append({
            "type": "locust",
            "day": random.randint(1, 7),
            "severity": "critical",
            "message": "🦗 LOCUST SWARM DETECTED! Prepare defenses!"
        })
    
    return disasters

def calculate_xp_gain(action, quality=1.0):
    """Calculate XP based on action"""
    base_xp = {
        "plant": 10,
        "water": 5,
        "harvest": 25,
        "survive_disaster": 50,
        "complete_challenge": 100,
        "use_ai": 15
    }
    
    xp = base_xp.get(action, 10) * quality
    return int(xp)

def level_up():
    """Handle level up"""
    st.session_state.level += 1
    st.session_state.xp = 0
    st.session_state.xp_to_next_level = int(st.session_state.xp_to_next_level * 1.5)
    st.session_state.money += 500  # Bonus money
    return True

def add_xp(amount):
    """Add XP and check for level up"""
    st.session_state.xp += amount
    
    if st.session_state.xp >= st.session_state.xp_to_next_level:
        if level_up():
            st.session_state.last_achievement = f"🎉 LEVEL UP! You're now Level {st.session_state.level}!"
            st.balloons()

def unlock_skill(skill_id):
    """Unlock a skill"""
    skill = SKILLS[skill_id]
    if st.session_state.xp >= skill["xp_cost"]:
        st.session_state.xp -= skill["xp_cost"]
        st.session_state.unlocked_skills.append(skill_id)
        st.session_state.last_achievement = f"🌟 NEW SKILL UNLOCKED: {skill['name']}!"
        return True
    return False

def render_gaming_header():
    """Render gaming-style header"""
    st.markdown(f"""
    <div class='game-header'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <h1 style='margin: 0; font-family: "Orbitron", sans-serif; font-size: 2rem;'>
                    🌾 SHAMBABYTE
                </h1>
                <span style='background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px;'>
                    Level {st.session_state.level}
                </span>
            </div>
            <div style='display: flex; gap: 1rem; flex-wrap: wrap;'>
                <div class='stat-card' style='padding: 0.5rem 1rem;'>
                    💰 ${st.session_state.money}
                </div>
                <div class='stat-card' style='padding: 0.5rem 1rem;'>
                    ⭐ {st.session_state.total_score} pts
                </div>
                <div class='stat-card' style='padding: 0.5rem 1rem;'>
                    🌍 {st.session_state.current_location['name']}
                </div>
            </div>
        </div>
        <div style='margin-top: 1rem;'>
            <div class='xp-bar-container'>
                <div class='xp-bar' style='width: {(st.session_state.xp / st.session_state.xp_to_next_level) * 100}%;'>
                    {st.session_state.xp} / {st.session_state.xp_to_next_level} XP
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_welcome_screen():
    """Gaming-style welcome screen"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style='text-align: center; padding: 3rem; background: rgba(255,255,255,0.05); border-radius: 20px; border: 2px solid rgba(255,255,255,0.1);'>
            <h1 style='font-size: 4rem; font-family: "Orbitron", sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem;'>
                SHAMBABYTE
            </h1>
            <h3 style='color: #FFD700; margin-bottom: 2rem;'>🌾 Farm Through History 🚀</h3>
            <p style='font-size: 1.2rem; margin-bottom: 3rem; color: rgba(255,255,255,0.8);'>
                Travel through 60+ years of Kenyan agriculture. Use real NASA satellite data to survive droughts, floods, and disasters. Level up your skills. Become a legendary farmer! 🏆
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        player_name = st.text_input("👤 Enter Your Farmer Name:", placeholder="MjanjaMkulima")
        
        if st.button("🚀 START ADVENTURE", use_container_width=True, type="primary"):
            st.session_state.player_name = player_name if player_name else "Farmer"
            st.session_state.current_screen = 'era_selection'
            st.rerun()
        
        if st.button("📚 NASA RESOURCES", use_container_width=True):
            st.session_state.current_screen = 'resources'
            st.rerun()

def render_nasa_resources():
    """Show NASA resources"""
    st.markdown("## 🛰️ NASA Agricultural Resources")
    
    for category, resources in NASA_RESOURCES.items():
        st.markdown(f"### {category}")
        for name, url in resources.items():
            st.markdown(f"- 🔗 [{name}]({url})")
    
    if st.button("⬅️ Back"):
        st.session_state.current_screen = 'welcome'
        st.rerun()

def render_era_selection():
    """Gaming-style era selection"""
    st.markdown("""
    <div style='text-align: center; margin: 2rem 0;'>
        <h1 style='font-family: "Orbitron", sans-serif; font-size: 3rem; background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            ⏰ CHOOSE YOUR ERA
        </h1>
        <p style='font-size: 1.2rem; color: rgba(255,255,255,0.7);'>
            Select a time period to begin your farming journey
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display eras in grid
    cols = st.columns(2)
    
    for idx, (era_key, era) in enumerate(ERAS.items()):
        with cols[idx % 2]:
            progress = st.session_state.era_progress[era_key]
            is_locked = not progress['unlocked']
            
            card_class = 'era-card era-card-locked' if is_locked else 'era-card'
            
            st.markdown(f"""
            <div class='{card_class}'>
                <div style='text-align: center;'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>{era['icon']}</div>
                    <h2 style='color: {era["color"]}; font-family: "Orbitron", sans-serif;'>{era['name']}</h2>
                    <p style='color: rgba(255,255,255,0.8); margin: 1rem 0;'>{era['description']}</p>
                    <p style='color: rgba(255,255,255,0.6);'>📅 {era['years']}</p>
                    <p style='color: #FFD700; font-weight: bold; margin: 1rem 0;'>
                        {progress['events_completed']}/{era['total_events']} Events ⭐
                    </p>
                    <p style='color: rgba(255,255,255,0.6); font-size: 0.9rem;'>
                        {era['historical_context']}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if is_locked:
                st.button(f"🔒 LOCKED", key=f"lock_{era_key}", disabled=True, use_container_width=True)
            else:
                if st.button(f"▶️ PLAY {era['name'].upper()}", key=f"play_{era_key}", use_container_width=True, type="primary"):
                    st.session_state.current_era = era_key
                    st.session_state.current_screen = 'gameplay'
                    start_day, end_day = era['data_range']
                    st.session_state.day = start_day
                    st.session_state.era_start_day = start_day
                    st.session_state.era_end_day = end_day
                    st.session_state.ai_uses_today = 0
                    st.rerun()

def create_disaster_map(disasters, current_location):
    """Create interactive disaster map"""
    # Create map centered on current location
    fig = go.Figure()
    
    # Add base location
    fig.add_trace(go.Scattermapbox(
        lat=[current_location['lat']],
        lon=[current_location['lon']],
        mode='markers+text',
        marker=dict(size=20, color='green'),
        text=['🏠 Your Farm'],
        textposition='top center',
        name='Farm'
    ))
    
    # Add disaster markers
    for disaster in disasters:
        offset_lat = current_location['lat'] + random.uniform(-0.5, 0.5)
        offset_lon = current_location['lon'] + random.uniform(-0.5, 0.5)
        
        fig.add_trace(go.Scattermapbox(
            lat=[offset_lat],
            lon=[offset_lon],
            mode='markers+text',
            marker=dict(
                size=15,
                color=DISASTERS[disaster['type']]['color']
            ),
            text=[f"{DISASTERS[disaster['type']]['emoji']} Day +{disaster['day']}"],
            textposition='top center',
            name=disaster['type'].title()
        ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=current_location['lat'], lon=current_location['lon']),
            zoom=8
        ),
        height=400,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    return fig

def render_gameplay():
    """Main gameplay screen - gaming style"""
    nasa_data = load_nasa_data()
    if nasa_data is None:
        return
    
    era = ERAS[st.session_state.current_era]
    weather = nasa_data.iloc[st.session_state.day]
    
    # Predict disasters
    if not st.session_state.upcoming_disasters:
        st.session_state.upcoming_disasters = predict_disasters(nasa_data, st.session_state.day, st.session_state.current_era)
    
    # Sidebar - Skills & Stats
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.player_name}")
        st.markdown(f"**Era:** {era['icon']} {era['name']}")
        st.markdown(f"**Day:** {st.session_state.day - st.session_state.era_start_day + 1}")
        
        st.markdown("### 🎒 Inventory")
        st.progress(min(1.0, st.session_state.seeds / 100), text=f"🌱 Seeds: {st.session_state.seeds}")
        st.progress(min(1.0, st.session_state.water / 100), text=f"💧 Water: {st.session_state.water}")
        st.progress(min(1.0, st.session_state.fertilizer / 100), text=f"🧪 Fertilizer: {st.session_state.fertilizer}")
        st.progress(st.session_state.farm_health / 100, text=f"❤️ Farm Health: {st.session_state.farm_health}%")
        
        st.markdown("### 🌟 SKILLS")
        for skill_id, skill in SKILLS.items():
            is_unlocked = skill_id in st.session_state.unlocked_skills
            skill_class = 'skill-item skill-unlocked' if is_unlocked else 'skill-item'
            
            status = "✅" if is_unlocked else f"🔒 {skill['xp_cost']} XP"
            
            st.markdown(f"""
            <div class='{skill_class}'>
                <strong>{skill['name']}</strong><br>
                <small>{skill['desc']}</small><br>
                <span style='color: #FFD700;'>{status}</span>
            </div>
            """, unsafe_allow_html=True)
            
            if not is_unlocked and st.session_state.xp >= skill['xp_cost']:
                if st.button(f"Unlock {skill['name']}", key=f"unlock_{skill_id}"):
                    unlock_skill(skill_id)
                    st.rerun()
    
    # Main area
    if st.button("⬅️ BACK TO ERA SELECT"):
        st.session_state.current_screen = 'era_selection'
        st.rerun()
    
    # Achievement popup
    if st.session_state.last_achievement:
        st.markdown(f"""
        <div class='achievement-popup'>
            {st.session_state.last_achievement}
        </div>
        """, unsafe_allow_html=True)
        if st.button("✅ Got it!"):
            st.session_state.last_achievement = None
            st.rerun()
    
    # Disaster warnings
    imminent_disasters = [d for d in st.session_state.upcoming_disasters if d['day'] <= 2]
    if imminent_disasters:
        for disaster in imminent_disasters:
            st.markdown(f"""
            <div class='disaster-alert'>
                <h3>⚠️ DISASTER WARNING</h3>
                <p style='font-size: 1.2rem; margin: 0.5rem 0;'>{disaster['message']}</p>
                <p style='font-size: 0.9rem;'>Severity: {disaster['severity'].upper()}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Main game area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div style='background: rgba(102, 126, 234, 0.2); padding: 1.5rem; border-radius: 15px; border: 2px solid {era['color']};'>
            <h2>{era['icon']} {era['name']} - Day {st.session_state.day - st.session_state.era_start_day + 1}</h2>
            <p>{era['historical_context']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Weather dashboard
        st.markdown("### 🌤️ NASA Weather Data")
        w_col1, w_col2, w_col3, w_col4 = st.columns(4)
        w_col1.metric("🌡️ Temp", f"{weather['T2M']:.1f}°C", f"Max: {weather['T2M_MAX']:.1f}°C")
        w_col2.metric("💧 Rain", f"{weather['PRECTOTCORR']:.2f}mm")
        w_col3.metric("💨 Humidity", f"{weather['RH2M']:.1f}%")
        w_col4.metric("🌱 NDVI", f"{weather['NDVI_raw']:.3f}")
        
        # Disaster Map
        st.markdown("### 🗺️ DISASTER MAP")
        if st.session_state.upcoming_disasters:
            disaster_map = create_disaster_map(st.session_state.upcoming_disasters, st.session_state.current_location)
            st.plotly_chart(disaster_map, use_container_width=True)
        else:
            st.success("✅ No disasters detected in the next 7 days!")
        
        # Farm Actions
        st.markdown("### 🎮 ACTIONS")
        a_col1, a_col2, a_col3, a_col4 = st.columns(4)
        
        with a_col1:
            if st.button("🌱 PLANT", use_container_width=True):
                if st.session_state.seeds >= 10:
                    st.session_state.seeds -= 10
                    add_xp(calculate_xp_gain("plant"))
                    st.success("Planted! +10 XP")
                    st.rerun()
                else:
                    st.error("Not enough seeds!")
        
        with a_col2:
            if st.button("💧 WATER", use_container_width=True):
                if st.session_state.water >= 10:
                    water_cost = 10
                    if "water_master" in st.session_state.unlocked_skills:
                        water_cost = 8  # 20% reduction
                    st.session_state.water -= water_cost
                    st.session_state.farm_health = min(100, st.session_state.farm_health + 5)
                    add_xp(calculate_xp_gain("water"))
                    st.success(f"Watered! -{water_cost} water, +5 XP")
                    st.rerun()
                else:
                    st.error("Not enough water!")
        
        with a_col3:
            if st.button("🌾 HARVEST", use_container_width=True):
                harvest_value = 100
                if "golden_harvest" in st.session_state.unlocked_skills:
                    harvest_value = 150  # 50% bonus
                st.session_state.money += harvest_value
                add_xp(calculate_xp_gain("harvest"))
                st.success(f"Harvested! +${harvest_value}, +25 XP")
                st.balloons()
                st.rerun()
        
        with a_col4:
            if st.button("⏭️ NEXT DAY", use_container_width=True, type="primary"):
                advance_day(nasa_data, era)
                st.rerun()
    
    with col2:
        # AI Advisor
        st.markdown("### 🤖 AI ADVISOR")
        
        max_uses = 3 if "ai_insight" in st.session_state.unlocked_skills else 1
        uses_left = max_uses - st.session_state.ai_uses_today
        
        st.markdown(f"**Uses today:** {st.session_state.ai_uses_today}/{max_uses}")
        
        if st.button("💡 GET ADVICE", use_container_width=True, disabled=(uses_left <= 0)):
            if uses_left > 0:
                with st.spinner("🤖 AI analyzing..."):
                    advice = get_ai_advice(weather, era, st.session_state.upcoming_disasters)
                    st.info(advice)
                    st.session_state.ai_uses_today += 1
                    add_xp(calculate_xp_gain("use_ai"))
            else:
                st.warning("No uses left today!")
        
        # Upcoming disasters list
        st.markdown("### ⚠️ UPCOMING THREATS")
        if st.session_state.upcoming_disasters:
            for disaster in st.session_state.upcoming_disasters[:5]:
                severity_color = {"low": "🟢", "medium": "🟡", "high": "🔴", "critical": "🔴"}
                st.markdown(f"""
                <div style='background: rgba(255,0,0,0.1); padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0; border-left: 4px solid {DISASTERS[disaster['type']]['color']};'>
                    <strong>{DISASTERS[disaster['type']]['emoji']} {disaster['type'].title()}</strong><br>
                    <small>Day +{disaster['day']} | {severity_color[disaster['severity']]} {disaster['severity'].upper()}</small>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ All clear!")
        
        # Quick shop
        st.markdown("### 🏪 QUICK BUY")
        if st.button("Buy 10 Seeds ($50)"):
            if st.session_state.money >= 50:
                st.session_state.seeds += 10
                st.session_state.money -= 50
                st.success("Bought!")
                st.rerun()

def get_ai_advice(weather, era, disasters):
    """Get AI advice considering disasters"""
    if not GEMINI_API_KEY:
        return "⚠️ Set GEMINI_API_KEY to unlock AI advisor! Visit: https://makersuite.google.com/app/apikey"
    
    try:
        disaster_text = ""
        if disasters:
            disaster_text = f"\\n\\nUPCOMING DISASTERS:\\n" + "\\n".join([f"- {d['message']}" for d in disasters[:3]])
        
        prompt = f"""You are a fun, engaging AI farming advisor for Gen Z and older players in {era['years']} Kenya.

Weather (NASA Data):
- Temp: {weather['T2M']:.1f}°C (Max: {weather['T2M_MAX']:.1f}°C)
- Rain: {weather['PRECTOTCORR']:.2f}mm
- Humidity: {weather['RH2M']:.1f}%
- NDVI: {weather['NDVI_raw']:.4f}
{disaster_text}

Give 2-3 sentences of practical, engaging advice. Use emojis. Be encouraging but realistic. Reference the era's technology level."""

        response = model.generate_content(prompt)
        return response.text
    except:
        return "💭 Yo fam! Check that rainfall - looks kinda sus. Maybe prep for dry times ahead! Stay hydrated 💧"

def advance_day(nasa_data, era):
    """Advance day with disaster checks"""
    st.session_state.day += 1
    st.session_state.ai_uses_today = 0
    
    # Check if era complete
    if st.session_state.day >= st.session_state.era_end_day:
        st.session_state.era_progress[st.session_state.current_era]['completed'] = True
        st.session_state.last_achievement = f"🎉 {era['name']} COMPLETED! You're a legend!"
        
        # Unlock next era
        era_keys = list(ERAS.keys())
        current_idx = era_keys.index(st.session_state.current_era)
        if current_idx < len(era_keys) - 1:
            next_era = era_keys[current_idx + 1]
            st.session_state.era_progress[next_era]['unlocked'] = True
        
        add_xp(500)  # Completion bonus
        st.session_state.current_screen = 'era_selection'
        return
    
    # Weather effects
    weather = nasa_data.iloc[st.session_state.day]
    rain_water = int(weather['PRECTOTCORR'] * 5)
    st.session_state.water = min(100, st.session_state.water + rain_water)
    
    # Check for disasters
    active_disasters = [d for d in st.session_state.upcoming_disasters if d['day'] == 1]
    
    for disaster in active_disasters:
        damage = 20
        if "disaster_shield" in st.session_state.unlocked_skills:
            damage = int(damage * 0.7)  # 30% reduction
        
        st.session_state.farm_health = max(0, st.session_state.farm_health - damage)
        st.session_state.last_achievement = f"{DISASTERS[disaster['type']]['emoji']} {disaster['type'].title()} hit! -{damage} health"
        add_xp(calculate_xp_gain("survive_disaster"))
    
    # Update disaster predictions
    st.session_state.upcoming_disasters = predict_disasters(nasa_data, st.session_state.day, st.session_state.current_era)
    
    # Random events
    if random.random() < 0.15:  # 15% chance
        event_xp = random.randint(20, 50)
        st.session_state.money += random.randint(50, 150)
        add_xp(event_xp)
        st.session_state.last_achievement = f"🎁 Lucky event! +{event_xp} XP"

def main():
    init_session_state()
    render_gaming_header()
    
    if st.session_state.current_screen == 'welcome':
        render_welcome_screen()
    elif st.session_state.current_screen == 'resources':
        render_nasa_resources()
    elif st.session_state.current_screen == 'era_selection':
        render_era_selection()
    elif st.session_state.current_screen == 'gameplay':
        render_gameplay()

if __name__ == "__main__":
    main()