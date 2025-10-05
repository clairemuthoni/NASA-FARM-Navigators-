import streamlit as st
import pandas as pd
import numpy as np
import google.generativeai as genai
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import json
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Shambabyte - Historical Farming Simulator",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Gemini (optional)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
    except:
        model = None
else:
    model = None

# Translation cache
TRANSLATION_CACHE = {}

def translate_text(text, target_lang='Kiswahili'):
    """Translate text using Gemini API with caching"""
    if target_lang == 'English' or not model:
        return text
    
    cache_key = f"{text}_{target_lang}"
    if cache_key in TRANSLATION_CACHE:
        return TRANSLATION_CACHE[cache_key]
    
    try:
        prompt = f"Translate this to {target_lang}, keeping emojis: {text}"
        response = model.generate_content(prompt)
        translated = response.text.strip()
        TRANSLATION_CACHE[cache_key] = translated
        return translated
    except:
        return text

def t(text):
    """Quick translation wrapper"""
    return translate_text(text, st.session_state.get('language', 'English'))

# Save system
SAVES_DIR = Path("saves")
SAVES_DIR.mkdir(exist_ok=True)

# ERA CONFIGURATION
ERAS = {
    "1960s": {
        "name": "1960s Independence Era",
        "icon": "🇰🇪",
        "color": "#D84315",
        "description": "The dawn of independence and agricultural modernization",
        "years": "1960-1969",
        "total_events": 4,
        "data_range": (0, 73),
        "unlocked": True,
        "challenges": [
            "Experience Kenya's independence",
            "Navigate land reforms",
            "Ride the coffee boom",
            "Survive East African drought"
        ]
    },
    "1980s": {
        "name": "1980s Green Revolution",
        "icon": "🚜",
        "color": "#F57C00",
        "description": "New technologies transform Kenyan farms",
        "years": "1980-1989",
        "total_events": 4,
        "data_range": (74, 146),
        "unlocked": False,
        "challenges": [
            "Survive the coffee crisis",
            "Adopt Green Revolution tech",
            "Adapt to structural adjustment",
            "Combat locust invasion"
        ]
    },
    "2000s": {
        "name": "2000s Digital Age",
        "icon": "📱",
        "color": "#0288D1",
        "description": "Technology meets traditional farming",
        "years": "2000-2009",
        "total_events": 4,
        "data_range": (147, 219),
        "unlocked": False,
        "challenges": [
            "Navigate post-election period",
            "Adopt M-Pesa for trading",
            "Survive millennium drought",
            "Export flowers globally"
        ]
    },
    "2010s": {
        "name": "2010s Tech Boom",
        "icon": "🛰️",
        "color": "#7B1FA2",
        "description": "IoT sensors and precision agriculture",
        "years": "2010-2019",
        "total_events": 4,
        "data_range": (220, 292),
        "unlocked": False,
        "challenges": [
            "Benefit from devolution",
            "Implement climate-smart practices",
            "Use IoT and satellite data",
            "Combat fall armyworm"
        ]
    },
    "2020s": {
        "name": "2020s Climate Action",
        "icon": "🌍",
        "color": "#00897B",
        "description": "Fighting climate change through smart farming",
        "years": "2020-2025",
        "total_events": 4,
        "data_range": (293, 366),
        "unlocked": False,
        "challenges": [
            "Survive COVID-19 pandemic",
            "Battle locust swarms",
            "Access climate finance",
            "Master AI agriculture"
        ]
    }
}

# Historical Events Database
HISTORICAL_EVENTS = {
    "1960s": [
        {
            "name": "Kenya Independence",
            "year": 1963,
            "day": 3,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "Nairobi"},
            "type": "political",
            "effect": {"morale": 30, "prices": 20},
            "description": "Kenya achieves independence! Uhuru celebrations bring hope and new opportunities for farmers.",
            "challenge": "Participate in national food drive for independence celebrations",
            "emoji": "🇰🇪"
        },
        {
            "name": "Land Reform Programme",
            "year": 1964,
            "day": 5,
            "location": {"lat": -0.0917, "lon": 34.7680, "name": "Rift Valley"},
            "type": "political",
            "effect": {"land_size": 25},
            "description": "Government land redistribution program. Opportunity to acquire more farmland!",
            "challenge": "Purchase additional land plot for expansion",
            "emoji": "🏞️"
        },
        {
            "name": "Coffee Boom",
            "year": 1966,
            "day": 10,
            "location": {"lat": -0.4023, "lon": 36.9630, "name": "Central Kenya"},
            "type": "economic",
            "effect": {"crop_value": 50},
            "description": "Global coffee prices soar! Kenyan coffee farmers prosper.",
            "challenge": "Plant and harvest premium coffee for export",
            "emoji": "☕"
        },
        {
            "name": "East African Drought",
            "year": 1968,
            "day": 15,
            "location": {"lat": 1.2921, "lon": 36.8219, "name": "Northern Kenya"},
            "type": "disaster",
            "effect": {"water": -40, "crop_health": -30},
            "description": "Severe drought hits East Africa. Water sources dry up, crops wither.",
            "challenge": "Survive 10 days with reduced water supply",
            "emoji": "🏜️"
        }
    ],
    "1980s": [
        {
            "name": "Coffee Crisis",
            "year": 1987,
            "day": 20,
            "location": {"lat": -0.4023, "lon": 36.9630, "name": "Kiambu"},
            "type": "economic",
            "effect": {"crop_value": -40},
            "description": "International coffee prices collapse! Many farmers struggle.",
            "challenge": "Diversify crops to survive market crash",
            "emoji": "📉"
        },
        {
            "name": "Green Revolution",
            "year": 1982,
            "day": 22,
            "location": {"lat": -1.2864, "lon": 36.8172, "name": "Nairobi"},
            "type": "technological",
            "effect": {"yield": 60},
            "description": "High-yield seed varieties introduced! Agriculture transformed.",
            "challenge": "Adopt new hybrid seeds and fertilizers",
            "emoji": "🌱"
        },
        {
            "name": "Structural Adjustment",
            "year": 1986,
            "day": 25,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "National"},
            "type": "political",
            "effect": {"subsidy": -50},
            "description": "Government removes agricultural subsidies. Input costs rise.",
            "challenge": "Maintain profitability with higher costs",
            "emoji": "💰"
        },
        {
            "name": "Locust Invasion",
            "year": 1989,
            "day": 27,
            "location": {"lat": 2.2869, "lon": 40.8529, "name": "Eastern Kenya"},
            "type": "disaster",
            "effect": {"crop_health": -60},
            "description": "Massive locust swarms devastate crops across Eastern Kenya!",
            "challenge": "Deploy emergency pesticides and save what you can",
            "emoji": "🦗"
        }
    ],
    "2000s": [
        {
            "name": "Post-Election Impact",
            "year": 2008,
            "day": 30,
            "location": {"lat": -0.0917, "lon": 34.7680, "name": "Rift Valley"},
            "type": "political",
            "effect": {"safety": -40, "market_access": -50},
            "description": "Post-election violence disrupts farming. Markets inaccessible.",
            "challenge": "Protect farm and maintain food production",
            "emoji": "⚠️"
        },
        {
            "name": "M-Pesa Launch",
            "year": 2007,
            "day": 35,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "Nairobi"},
            "type": "technological",
            "effect": {"market_access": 50},
            "description": "Mobile money revolution! Farmers can now trade digitally.",
            "challenge": "Set up M-Pesa account and sell crops via mobile",
            "emoji": "📱"
        },
        {
            "name": "Millennium Drought",
            "year": 2009,
            "day": 37,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "Nationwide"},
            "type": "disaster",
            "effect": {"water": -50},
            "description": "Worst drought in decades! National food crisis declared.",
            "challenge": "Implement water conservation and drought-resistant crops",
            "emoji": "🌵"
        },
        {
            "name": "Horticultural Export Boom",
            "year": 2005,
            "day": 40,
            "location": {"lat": -0.3762, "lon": 36.0973, "name": "Naivasha"},
            "type": "economic",
            "effect": {"export_value": 70},
            "description": "Kenya becomes world's leading flower exporter!",
            "challenge": "Grow and export premium roses to Europe",
            "emoji": "🌹"
        }
    ],
    "2010s": [
        {
            "name": "Devolution Implementation",
            "year": 2013,
            "day": 42,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "County Level"},
            "type": "political",
            "effect": {"local_support": 40},
            "description": "County governments bring agriculture services closer to farmers!",
            "challenge": "Access county agricultural extension services",
            "emoji": "🏛️"
        },
        {
            "name": "Climate-Smart Agriculture",
            "year": 2015,
            "day": 45,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "National"},
            "type": "technological",
            "effect": {"resilience": 50},
            "description": "CSA practices adopted nationwide. Farmers adapt to climate change.",
            "challenge": "Implement conservation agriculture techniques",
            "emoji": "🌍"
        },
        {
            "name": "IoT Revolution",
            "year": 2018,
            "day": 47,
            "location": {"lat": -1.2864, "lon": 36.8172, "name": "Nairobi Tech Hub"},
            "type": "technological",
            "effect": {"precision": 60},
            "description": "Soil sensors and satellite data transform farming! Precision agriculture arrives.",
            "challenge": "Install IoT sensors and use satellite data for decisions",
            "emoji": "🛰️"
        },
        {
            "name": "Fall Armyworm Outbreak",
            "year": 2017,
            "day": 50,
            "location": {"lat": -0.0917, "lon": 34.7680, "name": "Western Kenya"},
            "type": "disaster",
            "effect": {"maize_health": -70},
            "description": "Invasive pest devastates maize crops! Emergency response needed.",
            "challenge": "Combat armyworm using integrated pest management",
            "emoji": "🐛"
        }
    ],
    "2020s": [
        {
            "name": "COVID-19 Pandemic",
            "year": 2020,
            "day": 10,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "Global/Kenya"},
            "type": "disaster",
            "effect": {"market_access": -60},
            "description": "Global pandemic! Markets close, labor shortages, supply chain disruption.",
            "challenge": "Adapt to lockdowns and maintain food production",
            "emoji": "😷"
        },
        {
            "name": "Locust Swarms Return",
            "year": 2020,
            "day": 25,
            "location": {"lat": 2.2869, "lon": 40.8529, "name": "Northern Kenya"},
            "type": "disaster",
            "effect": {"crop_health": -80},
            "description": "Worst locust invasion in 70 years! Biblical proportions.",
            "challenge": "Deploy drones and emergency response to save crops",
            "emoji": "🦗"
        },
        {
            "name": "Climate Finance Access",
            "year": 2023,
            "day": 40,
            "location": {"lat": -1.2921, "lon": 36.8219, "name": "National"},
            "type": "economic",
            "effect": {"grants": 500},
            "description": "Climate adaptation funds available! Green technology subsidized.",
            "challenge": "Apply for climate finance and install solar irrigation",
            "emoji": "💚"
        },
        {
            "name": "AI Agriculture Boom",
            "year": 2024,
            "day": 55,
            "location": {"lat": -1.2864, "lon": 36.8172, "name": "Nairobi"},
            "type": "technological",
            "effect": {"ai_predictions": 1},
            "description": "AI advisors predict optimal planting, harvesting, and market timing!",
            "challenge": "Use AI to maximize yield and profit",
            "emoji": "🤖"
        }
    ]
}

# Crop types
CROP_TYPES = {
    "maize": {"name": "Maize", "emoji": "🌽", "days": 15, "value": 50},
    "beans": {"name": "Beans", "emoji": "🫘", "days": 12, "value": 40},
    "coffee": {"name": "Coffee", "emoji": "☕", "days": 30, "value": 150},
    "sukuma": {"name": "Sukuma Wiki", "emoji": "🥬", "days": 8, "value": 30},
    "tomatoes": {"name": "Tomatoes", "emoji": "🍅", "days": 18, "value": 60},
}

# Avatar options
AVATAR_OPTIONS = {
    "skin_tones": ["👨🏾", "👨🏿", "👩🏾", "👩🏿", "🧑🏾", "🧑🏿"],
    "hats": ["👨‍🌾", "🧢", "👒", "🎩", "⛑️"],
    "tools": ["🔨", "⚒️", "🪓", "⛏️", "🔧"],
    "outfits": ["👔", "👕", "👗", "🥼", "🦺"]
}

MAX_ENERGY = 100

# Custom CSS with Afrocentric pixel art theme
def get_theme_css():
    is_dark = st.session_state.get('dark_mode', False)
    
    if is_dark:
        # Dark Mode - Inspired by African night skies
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Ubuntu:wght@400;700&display=swap');
            
            .main {
                background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                color: #e8e8e8;
                font-family: 'Ubuntu', sans-serif;
            }
            
            .game-header {
                background: linear-gradient(135deg, #D84315 0%, #BF360C 100%);
                padding: 1.5rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                box-shadow: 0 8px 16px rgba(216, 67, 21, 0.4);
                border: 4px solid #FFB74D;
                border-style: double;
            }
            
            .era-card {
                background: linear-gradient(145deg, #2d2d44 0%, #1f1f35 100%);
                padding: 2rem;
                border-radius: 12px;
                border: 4px solid #FFB74D;
                border-style: outset;
                position: relative;
                margin-bottom: 1rem;
                box-shadow: 8px 8px 0px #0f0f20;
            }
            
            .era-card:hover {
                transform: translate(-2px, -2px);
                box-shadow: 12px 12px 0px #0f0f20;
            }
            
            .era-card::before {
                content: '';
                position: absolute;
                top: 8px;
                left: 8px;
                right: 8px;
                bottom: 8px;
                border: 2px dashed #FFB74D;
                border-radius: 8px;
                opacity: 0.3;
            }
            
            .era-card-locked {
                opacity: 0.4;
                filter: grayscale(100%);
            }
            
            .avatar-preview {
                font-size: 6rem;
                text-align: center;
                padding: 2rem;
                background: linear-gradient(145deg, #2d2d44 0%, #1f1f35 100%);
                border-radius: 12px;
                border: 4px solid #FFB74D;
                margin: 1rem 0;
            }
            
            .event-alert {
                background: linear-gradient(135deg, #D84315 0%, #BF360C 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 4px solid #FFD54F;
                margin: 1rem 0;
                animation: pulse 2s infinite;
                box-shadow: 8px 8px 0px rgba(0,0,0,0.4);
            }
            
            @keyframes pulse {
                0%, 100% { box-shadow: 8px 8px 0px rgba(255, 213, 79, 0.3); }
                50% { box-shadow: 8px 8px 20px rgba(255, 213, 79, 0.6); }
            }
            
            .crop-plot {
                background: linear-gradient(145deg, #4a3728 0%, #3d2f22 100%);
                border: 4px solid #8D6E63;
                border-style: ridge;
                border-radius: 8px;
                padding: 1.5rem;
                margin: 0.5rem;
                text-align: center;
                box-shadow: 4px 4px 0px rgba(0,0,0,0.4);
                min-height: 180px;
            }
            
            .crop-plot:hover {
                transform: translate(-2px, -2px);
                box-shadow: 6px 6px 0px rgba(0,0,0,0.4);
            }
            
            .energy-bar {
                background: linear-gradient(90deg, #D84315 0%, #FFB74D 50%, #4CAF50 100%);
                height: 28px;
                border-radius: 4px;
                border: 3px solid #1a1a2e;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.3);
            }
            
            .pixel-title {
                font-family: 'Press Start 2P', cursive;
                text-shadow: 4px 4px 0px rgba(0,0,0,0.5);
                letter-spacing: 2px;
            }
            
            .african-pattern {
                background-image: repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 10px,
                    rgba(255, 183, 77, 0.05) 10px,
                    rgba(255, 183, 77, 0.05) 20px
                );
            }
            
            .stButton>button {
                border: 4px solid #FFB74D !important;
                border-radius: 8px !important;
                font-family: 'Ubuntu', sans-serif !important;
                font-weight: 700 !important;
                box-shadow: 4px 4px 0px rgba(0,0,0,0.3) !important;
                transition: all 0.1s !important;
            }
            
            .stButton>button:hover {
                transform: translate(-2px, -2px) !important;
                box-shadow: 6px 6px 0px rgba(0,0,0,0.3) !important;
            }
            
            .stButton>button:active {
                transform: translate(2px, 2px) !important;
                box-shadow: 2px 2px 0px rgba(0,0,0,0.3) !important;
            }
        </style>
        """
    else:
        # Light Mode - Inspired by African sunlight and savanna
        return """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Ubuntu:wght@400;700&display=swap');
            
            .main {
                background: linear-gradient(180deg, #FFF8E1 0%, #FFECB3 50%, #FFE082 100%);
                color: #2d2d2d;
                font-family: 'Ubuntu', sans-serif;
            }
            
            .game-header {
                background: linear-gradient(135deg, #FF6F00 0%, #E65100 100%);
                padding: 1.5rem;
                border-radius: 8px;
                margin-bottom: 1rem;
                box-shadow: 0 8px 16px rgba(255, 111, 0, 0.4);
                border: 4px solid #FFA726;
                border-style: double;
                color: white;
            }
            
            .era-card {
                background: linear-gradient(145deg, #FFFDE7 0%, #FFF9C4 100%);
                padding: 2rem;
                border-radius: 12px;
                border: 4px solid #FF6F00;
                border-style: outset;
                position: relative;
                margin-bottom: 1rem;
                box-shadow: 8px 8px 0px #D84315;
            }
            
            .era-card:hover {
                transform: translate(-2px, -2px);
                box-shadow: 12px 12px 0px #D84315;
            }
            
            .era-card::before {
                content: '';
                position: absolute;
                top: 8px;
                left: 8px;
                right: 8px;
                bottom: 8px;
                border: 2px dashed #FF6F00;
                border-radius: 8px;
                opacity: 0.3;
            }
            
            .era-card-locked {
                opacity: 0.4;
                filter: grayscale(100%);
            }
            
            .avatar-preview {
                font-size: 6rem;
                text-align: center;
                padding: 2rem;
                background: linear-gradient(145deg, #FFFDE7 0%, #FFF9C4 100%);
                border-radius: 12px;
                border: 4px solid #FF6F00;
                margin: 1rem 0;
            }
            
            .event-alert {
                background: linear-gradient(135deg, #FF6F00 0%, #E65100 100%);
                padding: 1.5rem;
                border-radius: 12px;
                border: 4px solid #FFD54F;
                margin: 1rem 0;
                animation: pulse 2s infinite;
                box-shadow: 8px 8px 0px rgba(0,0,0,0.2);
                color: white;
            }
            
            @keyframes pulse {
                0%, 100% { box-shadow: 8px 8px 0px rgba(255, 213, 79, 0.5); }
                50% { box-shadow: 8px 8px 20px rgba(255, 213, 79, 0.8); }
            }
            
            .crop-plot {
                background: linear-gradient(145deg, #A1887F 0%, #8D6E63 100%);
                border: 4px solid #5D4037;
                border-style: ridge;
                border-radius: 8px;
                padding: 1.5rem;
                margin: 0.5rem;
                text-align: center;
                box-shadow: 4px 4px 0px rgba(0,0,0,0.3);
                min-height: 180px;
                color: white;
            }
            
            .crop-plot:hover {
                transform: translate(-2px, -2px);
                box-shadow: 6px 6px 0px rgba(0,0,0,0.3);
            }
            
            .energy-bar {
                background: linear-gradient(90deg, #D84315 0%, #FFB74D 50%, #66BB6A 100%);
                height: 28px;
                border-radius: 4px;
                border: 3px solid #5D4037;
                box-shadow: inset 0 2px 4px rgba(0,0,0,0.2);
            }
            
            .pixel-title {
                font-family: 'Press Start 2P', cursive;
                text-shadow: 4px 4px 0px rgba(0,0,0,0.2);
                letter-spacing: 2px;
            }
            
            .african-pattern {
                background-image: repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 10px,
                    rgba(216, 67, 21, 0.08) 10px,
                    rgba(216, 67, 21, 0.08) 20px
                );
            }
            
            .stButton>button {
                border: 4px solid #FF6F00 !important;
                border-radius: 8px !important;
                font-family: 'Ubuntu', sans-serif !important;
                font-weight: 700 !important;
                box-shadow: 4px 4px 0px rgba(0,0,0,0.2) !important;
                transition: all 0.1s !important;
            }
            
            .stButton>button:hover {
                transform: translate(-2px, -2px) !important;
                box-shadow: 6px 6px 0px rgba(0,0,0,0.2) !important;
            }
            
            .stButton>button:active {
                transform: translate(2px, 2px) !important;
                box-shadow: 2px 2px 0px rgba(0,0,0,0.2) !important;
            }
        </style>
        """

# NASA data loading
@st.cache_data
def load_nasa_data():
    try:
        df = pd.read_csv('nasa_data.csv')
        df['day'] = range(len(df))
        return df
    except Exception as e:
        st.error(f"NASA data not found: {e}")
        return None

# Initialize session state
def init_session_state():
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_screen = 'welcome'
        st.session_state.language = 'English'
        st.session_state.dark_mode = False
        st.session_state.player_name = ""
        st.session_state.avatar = {}
        st.session_state.level = 1
        st.session_state.xp = 0
        st.session_state.energy = MAX_ENERGY
        st.session_state.money = 1000
        st.session_state.seeds = 50
        st.session_state.water = 100
        st.session_state.fertilizer = 20
        st.session_state.farm_plots = []
        st.session_state.active_events = []
        st.session_state.current_era = None
        st.session_state.day = 0
        st.session_state.era_day = 0
        st.session_state.completed_challenges = []
        
        # Era progress
        st.session_state.era_progress = {
            era: {"unlocked": ERAS[era]["unlocked"], "events_completed": 0, "completed": False}
            for era in ERAS.keys()
        }

def save_game():
    """Save game state"""
    if not st.session_state.get('player_name'):
        return False
    
    save_data = {
        'player_name': st.session_state.player_name,
        'avatar': st.session_state.avatar,
        'dark_mode': st.session_state.dark_mode,
        'last_save': datetime.now().isoformat(),
        'level': st.session_state.level,
        'xp': st.session_state.xp,
        'energy': st.session_state.energy,
        'money': st.session_state.money,
        'seeds': st.session_state.seeds,
        'water': st.session_state.water,
        'fertilizer': st.session_state.fertilizer,
        'farm_plots': st.session_state.farm_plots,
        'current_era': st.session_state.current_era,
        'day': st.session_state.day,
        'era_progress': st.session_state.era_progress,
        'active_events': st.session_state.active_events,
        'completed_challenges': st.session_state.completed_challenges
    }
    
    try:
        safe_name = "".join(c for c in st.session_state.player_name if c.isalnum()).lower()
        save_file = SAVES_DIR / f"{safe_name}_save.json"
        with open(save_file, 'w') as f:
            json.dump(save_data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Save failed: {e}")
        return False

def create_event_map(events):
    """Create interactive map with event locations"""
    fig = go.Figure()
    
    # Your farm location (Nairobi area)
    fig.add_trace(go.Scattermapbox(
        lat=[-1.2921],
        lon=[36.8219],
        mode='markers+text',
        marker=dict(size=20, color='green'),
        text=['🏠 Your Farm'],
        textposition='top center',
        name='Your Farm'
    ))
    
    # Event locations
    for event in events:
        loc = event['location']
        color = 'red' if event['type'] == 'disaster' else 'blue' if event['type'] == 'economic' else 'purple'
        
        fig.add_trace(go.Scattermapbox(
            lat=[loc['lat']],
            lon=[loc['lon']],
            mode='markers+text',
            marker=dict(size=15, color=color),
            text=[f"{event['emoji']} {event['name']}"],
            textposition='top center',
            name=event['name'],
            hovertext=f"{event['name']}<br>{event['description']}"
        ))
    
    fig.update_layout(
        mapbox=dict(
            style='open-street-map',
            center=dict(lat=-1.2921, lon=36.8219),
            zoom=5.5
        ),
        height=500,
        margin=dict(l=0, r=0, t=0, b=0),
        showlegend=False
    )
    
    return fig

def render_welcome():
    """Welcome screen"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <h1 style='text-align: center; font-size: 3.5rem;' class='pixel-title'>
            SHAMBABYTE
        </h1>
        """, unsafe_allow_html=True)
        
        st.markdown(f"<h3 style='text-align: center; color: #FFB74D;'>{t('🌾 Farm Through Kenyan History 🇰🇪')}</h3>", unsafe_allow_html=True)
        
        # Theme toggle
        col_a, col_b = st.columns(2)
        with col_a:
            lang = st.selectbox(t("🌍 Language"), ["English", "Kiswahili"])
            st.session_state.language = lang
        with col_b:
            theme_label = "🌙 Dark Mode" if not st.session_state.dark_mode else "☀️ Light Mode"
            if st.button(theme_label, use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        
        st.markdown(f"<p style='text-align: center; font-size: 1.2rem;'>{t('Experience 60+ years of real Kenyan agricultural history! Use NASA satellite data, survive historical disasters, and become a legendary farmer!')}</p>", unsafe_allow_html=True)
        
        player_name = st.text_input(t("👤 Enter Your Name"), placeholder=t("Farmer Name"))
        
        if st.button(t("🚀 Start Adventure"), use_container_width=True, type="primary"):
            if player_name:
                st.session_state.player_name = player_name
                st.session_state.current_screen = 'avatar_creator'
                st.rerun()
            else:
                st.warning(t("Please enter your name!"))

def render_avatar_creator():
    """Avatar creation screen"""
    st.markdown(f"### {t('🎨 Create Your Farmer')}")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown(f"#### {t('Customize Your Character')}")
        
        skin = st.selectbox(t("Face"), AVATAR_OPTIONS['skin_tones'], format_func=lambda x: x)
        hat = st.selectbox(t("Headwear"), AVATAR_OPTIONS['hats'], format_func=lambda x: x)
        outfit = st.selectbox(t("Clothing"), AVATAR_OPTIONS['outfits'], format_func=lambda x: x)
        tool = st.selectbox(t("Tool"), AVATAR_OPTIONS['tools'], format_func=lambda x: x)
        
        farmer_name = st.text_input(t("Farm Name"), placeholder="Shamba Ya Amani")
    
    with col2:
        avatar_display = f"{skin}{hat}"
        st.markdown(f"""
        <div class='avatar-preview african-pattern'>
            {avatar_display}<br>
            {outfit} {tool}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**{t('Your Farmer')}:** {st.session_state.player_name}")
        if farmer_name:
            st.markdown(f"**{t('Farm')}:** {farmer_name}")
    
    if st.button(t("✅ Start Farming!"), type="primary", use_container_width=True):
        st.session_state.avatar = {
            'skin': skin,
            'hat': hat,
            'outfit': outfit,
            'tool': tool,
            'farm_name': farmer_name or "Shamba Ya Amani"
        }
        # Initialize 4 farm plots instead of 9
        st.session_state.farm_plots = [
            {"crop": None, "planted_day": 0, "health": 100, "watered": False}
            for _ in range(4)
        ]
        st.session_state.current_screen = 'era_selection'
        save_game()
        st.rerun()

def render_era_selection():
    """Era selection screen with progress tracking"""
    st.markdown(f"""
    <div style='text-align: center; margin: 2rem 0;' class='african-pattern'>
        <h1 style='font-size: 2.5rem;' class='pixel-title'>
            ⏰ {t('CHOOSE YOUR ERA')}
        </h1>
        <p style='font-size: 1.2rem; opacity: 0.8;'>
            {t('Travel through 60 years of Kenyan agricultural history')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display eras in grid
    for era_key, era in ERAS.items():
        progress = st.session_state.era_progress[era_key]
        is_locked = not progress['unlocked']
        
        card_class = 'era-card era-card-locked' if is_locked else 'era-card'
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div class='{card_class}'>
                <div style='display: flex; align-items: center; gap: 1rem;'>
                    <div style='font-size: 4rem;'>{era['icon']}</div>
                    <div style='flex: 1;'>
                        <h2 style='color: {era["color"]}; font-family: Ubuntu; font-weight: 700; margin: 0;'>{t(era['name'])}</h2>
                        <p style='opacity: 0.8; margin: 0.5rem 0;'>{t(era['description'])}</p>
                        <p style='opacity: 0.6;'>📅 {era['years']}</p>
                    </div>
                </div>
                <div style='margin-top: 1rem;'>
                    <p style='color: {era["color"]}; font-weight: bold;'>
                        {progress['events_completed']}/{era['total_events']} {t('Events Completed')} ⭐
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            if is_locked:
                st.button(f"🔒 {t('LOCKED')}", key=f"lock_{era_key}", disabled=True, use_container_width=True)
            else:
                if st.button(f"▶️ {t('PLAY')}", key=f"play_{era_key}", use_container_width=True, type="primary"):
                    st.session_state.current_era = era_key
                    st.session_state.current_screen = 'gameplay'
                    # Set era-specific day range
                    start_day, end_day = era['data_range']
                    st.session_state.day = start_day
                    st.session_state.era_start_day = start_day
                    st.session_state.era_end_day = end_day
                    st.session_state.era_day = 0
                    st.session_state.active_events = []
                    save_game()
                    st.rerun()
        
        # Show challenges
        if not is_locked:
            with st.expander(f"{t('View Challenges')} - {era['name']}"):
                for i, challenge in enumerate(era['challenges'], 1):
                    status = "✅" if i <= progress['events_completed'] else "⭕"
                    st.markdown(f"{status} {t(challenge)}")

def check_for_events():
    """Check if any events trigger today"""
    era = st.session_state.current_era
    current_day = st.session_state.era_day
    
    if era not in HISTORICAL_EVENTS:
        return []
    
    triggered = []
    for event in HISTORICAL_EVENTS[era]:
        if event['day'] == current_day:
            if event not in st.session_state.active_events:
                triggered.append(event)
    
    return triggered

def render_gameplay():
    """Main gameplay screen with map"""
    nasa_data = load_nasa_data()
    if nasa_data is None:
        st.error("NASA data failed to load. Please check nasa_data.csv exists.")
        return
    
    # Check for events
    new_events = check_for_events()
    if new_events:
        st.session_state.active_events.extend(new_events)
        # Update progress
        era_progress = st.session_state.era_progress[st.session_state.current_era]
        era_progress['events_completed'] = len(st.session_state.active_events)
    
    # Back button and theme toggle
    col_back, col_theme = st.columns([3, 1])
    with col_back:
        if st.button(f"⬅️ {t('Back to Era Selection')}"):
            st.session_state.current_screen = 'era_selection'
            save_game()
            st.rerun()
    with col_theme:
        theme_label = "🌙" if not st.session_state.dark_mode else "☀️"
        if st.button(theme_label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    
    # Header with avatar
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        avatar = st.session_state.avatar
        st.markdown(f"""
        <div style='text-align: center;' class='african-pattern'>
            <div style='font-size: 3rem;'>{avatar.get('skin', '👨🏾')}{avatar.get('hat', '👨‍🌾')}</div>
            <strong>{st.session_state.player_name}</strong><br>
            <small>{avatar.get('farm_name', 'Shamba')}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        era = ERAS[st.session_state.current_era]
        st.markdown(f"### {era['icon']} {t('Day')} {st.session_state.era_day} - {t(era['name'])}")
        
        # Energy bar
        energy_pct = (st.session_state.energy / MAX_ENERGY) * 100
        st.markdown(f"""
        <div style='background: rgba(0,0,0,0.2); border-radius: 8px; padding: 5px; border: 2px solid rgba(255,183,77,0.3);'>
            <div class='energy-bar' style='width: {energy_pct}%;'></div>
        </div>
        <small>{t('Energy')}: {st.session_state.energy}/{MAX_ENERGY}</small>
        """, unsafe_allow_html=True)
    
    with col3:
        st.metric(t("💰 Money"), f"KSh {st.session_state.money:,}")
        st.metric(t("⭐ Level"), st.session_state.level)
        progress = st.session_state.era_progress[st.session_state.current_era]
        st.metric(t("🎯 Events"), f"{progress['events_completed']}/{era['total_events']}")
    
    # Active events with map
    if st.session_state.active_events:
        st.markdown(f"### {t('🗺️ ACTIVE HISTORICAL EVENTS')}")
        
        # Show last 2 events as alerts
        for event in st.session_state.active_events[-2:]:
            st.markdown(f"""
            <div class='event-alert'>
                <h3>{event['emoji']} {t(event['name'])} ({event['year']})</h3>
                <p>{t(event['description'])}</p>
                <small>📍 {event['location']['name']}</small><br>
                <strong>{t('Challenge')}: {t(event['challenge'])}</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Interactive map
        st.markdown(f"#### {t('📍 Event Locations Map')}")
        event_map = create_event_map(st.session_state.active_events)
        st.plotly_chart(event_map, use_container_width=True)
    
    # Tabs for different views
    tab1, tab2, tab3 = st.tabs([t("🌾 Farm"), t("🏪 Market"), t("📊 Progress")])
    
    with tab1:
        st.markdown(f"### {t('Your Farm')}")
        
        # 2x2 grid for 4 plots
        cols = st.columns(2)
        for i, plot in enumerate(st.session_state.farm_plots):
            with cols[i % 2]:
                if plot['crop']:
                    crop = CROP_TYPES[plot['crop']]
                    days_growing = st.session_state.day - plot['planted_day']
                    growth = min(100, (days_growing / crop['days']) * 100)
                    
                    st.markdown(f"""
                    <div class='crop-plot african-pattern'>
                        <div style='font-size: 3.5rem;'>{crop['emoji']}</div>
                        <strong style='font-size: 1.1rem;'>{t(crop['name'])}</strong><br>
                        <small>{t('Growth')}: {growth:.0f}%</small><br>
                        <small>{t('Health')}: {plot['health']}%</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if growth >= 100:
                        if st.button(t("🌾 Harvest"), key=f"h{i}", use_container_width=True):
                            harvest_value = int(crop['value'] * (plot['health']/100))
                            st.session_state.money += harvest_value
                            st.session_state.xp += 25
                            plot['crop'] = None
                            st.success(f"{t('Harvested!')} +KSh{harvest_value}")
                            save_game()
                            st.rerun()
                    else:
                        if st.button(t("💧 Water"), key=f"w{i}", use_container_width=True):
                            if st.session_state.water >= 5:
                                st.session_state.water -= 5
                                plot['health'] = min(100, plot['health'] + 10)
                                st.success(t("Watered!"))
                                save_game()
                                st.rerun()
                else:
                    st.markdown(f"""
                    <div class='crop-plot african-pattern'>
                        <div style='font-size: 3.5rem;'>🟫</div>
                        <small>{t('Empty Plot')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    selected = st.selectbox(
                        t("Crop"),
                        list(CROP_TYPES.keys()),
                        key=f"s{i}",
                        format_func=lambda x: f"{CROP_TYPES[x]['emoji']} {t(CROP_TYPES[x]['name'])}"
                    )
                    
                    if st.button(t("🌱 Plant"), key=f"p{i}", use_container_width=True):
                        if st.session_state.seeds >= 1:
                            st.session_state.seeds -= 1
                            plot['crop'] = selected
                            plot['planted_day'] = st.session_state.day
                            st.success(t("Planted!"))
                            save_game()
                            st.rerun()
    
    with tab2:
        st.markdown(f"### {t('🏪 Market')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {t('Buy Seeds')}")
            for crop_id, crop in CROP_TYPES.items():
                price = crop['value'] // 3
                if st.button(f"{crop['emoji']} {t(crop['name'])} - KSh{price}", key=f"buy_{crop_id}"):
                    if st.session_state.money >= price:
                        st.session_state.money -= price
                        st.session_state.seeds += 5
                        st.success(f"{t('Bought')} 5 {t('seeds')}!")
                        save_game()
                        st.rerun()
        
        with col2:
            st.markdown(f"#### {t('Buy Supplies')}")
            
            if st.button(t("💧 Water (20L) - KSh50")):
                if st.session_state.money >= 50:
                    st.session_state.money -= 50
                    st.session_state.water += 20
                    save_game()
                    st.rerun()
    
    with tab3:
        st.markdown(f"### {t('📊 Your Progress')}")
        
        # Era completion
        for era_key, era in ERAS.items():
            progress = st.session_state.era_progress[era_key]
            completion = (progress['events_completed'] / era['total_events']) * 100
            
            st.markdown(f"**{era['icon']} {t(era['name'])}**")
            st.progress(completion / 100, text=f"{progress['events_completed']}/{era['total_events']} {t('events')}")
    
    # Actions
    st.markdown(f"### {t('⚡ Quick Actions')}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(t("💤 Rest"), use_container_width=True):
            st.session_state.energy = MAX_ENERGY
            st.success(t("Refreshed!"))
            save_game()
            st.rerun()
    
    with col2:
        ai_label = t("🤖 AI Advisor") if model else t("🤖 AI (Disabled)")
        if st.button(ai_label, use_container_width=True, disabled=not model):
            if model:
                with st.spinner(t("Analyzing...")):
                    weather = nasa_data.iloc[st.session_state.day]
                    prompt = f"""You're advising a Kenyan farmer in {era['name']}. 
                    Weather: Temp {weather['T2M']:.1f}°C, Rain {weather['PRECTOTCORR']:.2f}mm
                    Give advice in {st.session_state.language} with emojis. 2 sentences."""
                    
                    response = model.generate_content(prompt)
                    st.info(response.text)
            else:
                st.warning(t("Set GEMINI_API_KEY environment variable to enable AI advisor"))
    
    with col3:
        if st.button(t("⏭️ Next Day"), use_container_width=True, type="primary"):
            st.session_state.day += 1
            st.session_state.era_day += 1
            st.session_state.energy = MAX_ENERGY
            
            # Check if era complete
            if st.session_state.day >= st.session_state.era_end_day:
                st.session_state.era_progress[st.session_state.current_era]['completed'] = True
                # Unlock next era
                era_keys = list(ERAS.keys())
                current_idx = era_keys.index(st.session_state.current_era)
                if current_idx < len(era_keys) - 1:
                    next_era = era_keys[current_idx + 1]
                    st.session_state.era_progress[next_era]['unlocked'] = True
                
                st.balloons()
                st.success(f"{t('Era Complete!')} {era['name']} 🎉")
                st.session_state.current_screen = 'era_selection'
                save_game()
                st.rerun()
            
            # Weather effects
            if st.session_state.day < len(nasa_data):
                weather = nasa_data.iloc[st.session_state.day]
                rain_water = int(weather['PRECTOTCORR'] * 3)
                st.session_state.water = min(100, st.session_state.water + rain_water)
            
            # Update crops
            for plot in st.session_state.farm_plots:
                if plot['crop'] and not plot['watered']:
                    plot['health'] -= 5
                plot['watered'] = False
            
            save_game()
            st.rerun()

def main():
    init_session_state()
    
    # Apply theme CSS
    st.markdown(get_theme_css(), unsafe_allow_html=True)
    
    # Route to screens
    if st.session_state.current_screen == 'welcome':
        render_welcome()
    elif st.session_state.current_screen == 'avatar_creator':
        render_avatar_creator()
    elif st.session_state.current_screen == 'era_selection':
        render_era_selection()
    elif st.session_state.current_screen == 'gameplay':
        render_gameplay()
    else:
        st.error(f"Unknown screen: {st.session_state.current_screen}")

if __name__ == "__main__":
    main()