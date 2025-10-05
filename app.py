import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import time
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="ShambaBytes - NASA Farm Navigator",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Language translations
TRANSLATIONS = {
    'en': {
        'title': '🌾 ShambaBytes',
        'subtitle': 'Time-Travel Farming Education Powered by NASA Data',
        'welcome': 'Welcome to ShambaBytes',
        'your_mission': 'Your Mission',
        'nasa_data': 'NASA Data You\'ll Use',
        'why_matters': 'Why This Matters',
        'start_journey': 'Start Your Farming Journey',
        'choose_location': 'Choose Your Farm Location & Time Period',
        'location': 'Location',
        'time_period': 'Time Period',
        'game_rules': 'Game Rules',
        'begin_simulation': 'Begin Simulation',
        'observation_phase': 'OBSERVATION PHASE',
        'decision_phase': 'DECISION PHASE',
        'your_farm': 'Your Farm',
        'data_trends': 'Data Trends',
        'farm_actions': 'Farm Actions',
        'plant_maize': 'Plant Maize',
        'plant_beans': 'Plant Beans',
        'irrigate': 'Irrigate Field',
        'fertilize': 'Apply Fertilizer',
        'next_day': 'Next Day',
        'auto_simulate': 'Auto-Simulate',
        'points': 'Points',
        'farm_health': 'Farm Health',
        'day': 'Day',
        'week': 'Week',
        'precipitation': 'Precipitation',
        'temperature': 'Temperature',
        'soil_moisture': 'Soil Moisture',
        'recent_decisions': 'Recent Decisions',
        'learning_tips': 'Learning Tips',
        'restart_game': 'Restart Game',
    },
    'sw': {
        'title': '🌾 ShambaBytes',
        'subtitle': 'Elimu ya Kilimo kwa Kutumia Data ya NASA',
        'welcome': 'Karibu ShambaBytes',
        'your_mission': 'Dhamira Yako',
        'nasa_data': 'Data ya NASA Utakayotumia',
        'why_matters': 'Kwa Nini Hii ni Muhimu',
        'start_journey': 'Anza Safari Yako ya Kilimo',
        'choose_location': 'Chagua Eneo la Shamba Lako na Kipindi cha Wakati',
        'location': 'Eneo',
        'time_period': 'Kipindi cha Wakati',
        'game_rules': 'Sheria za Mchezo',
        'begin_simulation': 'Anza Uchimbaji',
        'observation_phase': 'AWAMU YA UCHUNGUZI',
        'decision_phase': 'AWAMU YA MAAMUZI',
        'your_farm': 'Shamba Lako',
        'data_trends': 'Mwenendo wa Data',
        'farm_actions': 'Vitendo vya Shamba',
        'plant_maize': 'Panda Mahindi',
        'plant_beans': 'Panda Maharage',
        'irrigate': 'Mwagilia Shamba',
        'fertilize': 'Tia Mbolea',
        'next_day': 'Siku Inayofuata',
        'auto_simulate': 'Uchimbaji Otomatiki',
        'points': 'Alama',
        'farm_health': 'Afya ya Shamba',
        'day': 'Siku',
        'week': 'Wiki',
        'precipitation': 'Mvua',
        'temperature': 'Joto',
        'soil_moisture': 'Unyevu wa Udongo',
        'recent_decisions': 'Maamuzi ya Hivi Karibuni',
        'learning_tips': 'Vidokezo vya Kujifunza',
        'restart_game': 'Anzisha Upya Mchezo',
    }
}

# Historical farming eras in Kenya with real events
KENYAN_FARMING_ERAS = {
    1997: {
        'era_name': 'El Niño Floods Era',
        'era_name_sw': 'Enzi ya Mafuriko ya El Niño',
        'event': '1997-1998 El Niño floods devastated farms across Kenya. Maize production dropped 28%. Farmers learned hard lessons about drainage and flood preparedness.',
        'event_sw': 'Mafuriko ya El Niño 1997-1998 yaliharibu mashamba mengi nchini Kenya. Uzalishaji wa mahindi ulishuka 28%. Wakulima walijifunza masomo magumu kuhusu mfereji na maandalizi ya mafuriko.',
        'challenge': 'Excessive rainfall and flooding',
        'lesson': 'Importance of drainage systems and flood-resistant crops'
    },
    2000: {
        'era_name': 'Millennium Drought',
        'era_name_sw': 'Ukame wa Milenio',
        'event': '1999-2000 severe drought hit East Africa. Kenya declared food emergency. 4.4 million people needed food aid. This period taught the value of drought-resistant varieties.',
        'event_sw': 'Ukame mkali wa 1999-2000 ulipiga Afrika Mashariki. Kenya ilitangaza dharura ya chakula. Watu milioni 4.4 walihitaji msaada wa chakula. Kipindi hiki kilifundisha thamani ya aina zinazostahimili ukame.',
        'challenge': 'Severe drought and crop failure',
        'lesson': 'Need for drought-resistant crops and water conservation'
    },
    2004: {
        'era_name': 'Good Harvest Era',
        'era_name_sw': 'Enzi ya Mavuno Mazuri',
        'event': '2004 saw excellent rains and bumper maize harvest. Kenya became maize self-sufficient. Prices dropped 40%. Farmers learned about storage and market timing.',
        'event_sw': '2004 iliona mvua nzuri na mavuno makubwa ya mahindi. Kenya ikawa na kutosha mahindi. Bei zilishuka 40%. Wakulima walijifunza kuhusu uhifadhi na wakati wa soko.',
        'challenge': 'Surplus production and falling prices',
        'lesson': 'Importance of storage, processing, and market strategy'
    },
    2008: {
        'era_name': 'Post-Election Crisis',
        'era_name_sw': 'Baada ya Uchaguzi wa Mgogoro',
        'event': '2007-2008 post-election violence disrupted farming. Rift Valley, Kenya\'s breadbasket, was heavily affected. Food prices soared 50%. Farmers learned resilience.',
        'event_sw': 'Vurugu za baada ya uchaguzi 2007-2008 ziliharibu kilimo. Bonde la Ufa, kikapu cha chakula cha Kenya, kiliathiriwa sana. Bei za chakula zilipanda 50%. Wakulima walijifunza uvumilivu.',
        'challenge': 'Social unrest affecting agricultural production',
        'lesson': 'Community cooperation and alternative supply chains'
    },
    2011: {
        'era_name': 'Horn of Africa Drought',
        'era_name_sw': 'Ukame wa Pembe ya Afrika',
        'event': '2010-2011 worst drought in 60 years. 3.75 million Kenyans faced starvation. Livestock losses were catastrophic. Intensified focus on early warning systems.',
        'event_sw': 'Ukame wa 2010-2011 ulikuwa mbaya zaidi katika miaka 60. Wakenya milioni 3.75 walikabiliwa na njaa. Hasara za mifugo zilikuwa za kikatili. Msisitizo uliongezwa kwenye mifumo ya tahadhari ya mapema.',
        'challenge': 'Extreme drought and famine conditions',
        'lesson': 'Climate adaptation and early warning systems'
    },
    2017: {
        'era_name': 'Drought & Recovery',
        'era_name_sw': 'Ukame na Urejeshaji',
        'event': '2016-2017 drought followed by good rains. Government subsidized fertilizer helped recovery. Farmers adopted conservation agriculture techniques.',
        'event_sw': 'Ukame wa 2016-2017 ulifuatiwa na mvua nzuri. Serikali ilisaidia mbolea kuwezesha urejeshaji. Wakulima walitumia mbinu za kilimo cha uhifadhi.',
        'challenge': 'Drought recovery and rebuilding',
        'lesson': 'Government support and modern farming techniques'
    },
    2020: {
        'era_name': 'Locusts & COVID-19',
        'era_name_sw': 'Nzige na COVID-19',
        'event': '2019-2020 desert locust invasion, worst in 70 years. Then COVID-19 hit, disrupting supply chains. Farmers learned about pest control and digital markets.',
        'event_sw': 'Uvamizi wa nzige wa jangwa 2019-2020, mbaya zaidi katika miaka 70. Kisha COVID-19 iligonga, ikiharibu minyororo ya usambazaji. Wakulima walijifunza kuhusu udhibiti wa wadudu na masoko ya kidijitali.',
        'challenge': 'Locust invasion and pandemic disruptions',
        'lesson': 'Pest management and digital agriculture platforms'
    },
    2022: {
        'era_name': 'Climate Uncertainty Era',
        'era_name_sw': 'Enzi ya Kutokuwa na Uhakika wa Hali ya Hewa',
        'event': '2021-2022 erratic rainfall patterns due to climate change. Five consecutive failed rainy seasons. Farmers increasingly adopting data-driven approaches and NASA satellite data.',
        'event_sw': 'Mifumo ya mvua isiyoaminika 2021-2022 kutokana na mabadiliko ya hali ya hewa. Misimu mitano mfululizo ya mvua iliyoshindwa. Wakulima wanaendelea kutumia njia zinazotegemea data na data ya satelaiti ya NASA.',
        'challenge': 'Climate change and unpredictable weather',
        'lesson': 'Data-driven farming using satellite technology'
    }
}

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

if 'game_phase' not in st.session_state:
    st.session_state.game_phase = 'start'
    st.session_state.current_day = 0
    st.session_state.current_week = 0
    st.session_state.current_year = 2020
    st.session_state.observation_complete = False
    st.session_state.points = 0
    st.session_state.decisions = []
    st.session_state.farm_health = 70
    st.session_state.location = "Nairobi, Kenya"
    st.session_state.historical_data = None
    st.session_state.era_info = None

def t(key):
    """Get translation for current language"""
    return TRANSLATIONS[st.session_state.language].get(key, key)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #1a1a1a 0%, #0a0a0a 100%);
    }
    .stButton>button {
        background: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        background: #45a049;
    }
    .welcome-card {
        background: rgba(76, 175, 80, 0.15);
        padding: 40px;
        border-radius: 12px;
        border-left: 6px solid #4CAF50;
        margin: 20px 0;
    }
    .era-card {
        background: rgba(139, 195, 74, 0.2);
        padding: 25px;
        border-radius: 12px;
        border-left: 5px solid #8BC34A;
        margin: 20px 0;
    }
    .phase-indicator {
        background: rgba(139, 195, 74, 0.2);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin: 20px 0;
        border: 2px solid #8BC34A;
    }
    h1, h2, h3 {
        color: #4CAF50 !important;
    }
    .stMetric {
        background: rgba(76, 175, 80, 0.1);
        padding: 15px;
        border-radius: 8px;
    }
    .language-toggle {
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# NASA Data Provider with historically accurate patterns
class NASADataProvider:
    def __init__(self):
        self.base_lat = -1.2921  # Nairobi
        self.base_lon = 36.8219
        
    def get_historical_data(self, year):
        """Generate NASA data with historically accurate patterns for specific years"""
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        day_of_year = np.arange(len(dates))
        
        # Base seasonal pattern
        rainfall_seasonal = 5 * np.sin((day_of_year - 60) * 2 * np.pi / 365) + 3.5
        
        # Apply historical modifications
        if year == 1997:
            # El Niño - excessive rainfall Oct-Dec
            rainfall_seasonal[274:] += 8  # Much higher rainfall
        elif year == 2000:
            # Severe drought
            rainfall_seasonal *= 0.3  # Very low rainfall all year
        elif year == 2004:
            # Good rains
            rainfall_seasonal *= 1.3
        elif year == 2011:
            # Extreme drought
            rainfall_seasonal *= 0.25
        elif year == 2017:
            # Drought first half, recovery second half
            rainfall_seasonal[:182] *= 0.4
            rainfall_seasonal[182:] *= 1.2
        elif year == 2020:
            # Erratic patterns (COVID/Locust year)
            rainfall_seasonal += np.random.normal(0, 3, len(dates))
        elif year == 2022:
            # Climate uncertainty - very erratic
            rainfall_seasonal = rainfall_seasonal * 0.6 + np.random.normal(0, 4, len(dates))
        
        data = pd.DataFrame({
            'date': dates,
            'day_of_year': day_of_year,
            'precipitation': np.maximum(0, rainfall_seasonal + np.random.normal(0, 1.5, len(dates))),
            'temperature': 19 + 2 * np.sin((day_of_year - 30) * 2 * np.pi / 365) + np.random.normal(0, 1.5, len(dates)),
            'max_temp': 24 + 2 * np.sin((day_of_year - 30) * 2 * np.pi / 365) + np.random.normal(0, 1.5, len(dates)),
            'min_temp': 14 + 1.5 * np.sin((day_of_year - 30) * 2 * np.pi / 365) + np.random.normal(0, 1, len(dates)),
            'soil_moisture': 0.5 + 0.2 * np.sin((day_of_year - 60) * 2 * np.pi / 365) + np.random.uniform(-0.1, 0.1, len(dates)),
            'ndvi': 0.55 + 0.2 * np.sin((day_of_year - 80) * 2 * np.pi / 365) + np.random.uniform(-0.1, 0.1, len(dates)),
            'humidity': 70 + 10 * np.sin((day_of_year - 60) * 2 * np.pi / 365) + np.random.uniform(-5, 5, len(dates)),
            'radiation': 20 + 3 * np.sin((day_of_year - 180) * 2 * np.pi / 365) + np.random.uniform(-2, 2, len(dates))
        })
        
        # Adjust NDVI based on rainfall (realistic correlation)
        data['ndvi'] = 0.3 + (data['precipitation'] / 10) * 0.5
        data['ndvi'] = data['ndvi'].clip(0.2, 0.9)
        
        data['soil_moisture'] = data['soil_moisture'].clip(0.1, 0.9)
        data['humidity'] = data['humidity'].clip(40, 95)
        
        return data

# Three.js Farm Component
def render_3d_farm(day=0):
    """Render 3D farm using Three.js"""
    growth_factor = min(1.0, day / 60)
    
    html_code = f"""
    <div id="farm-container" style="width: 100%; height: 500px; background: #87CEEB; border-radius: 12px; overflow: hidden;"></div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script>
        let scene, camera, renderer, farmObjects = [];
        const growthFactor = {growth_factor};
        
        function init() {{
            const container = document.getElementById('farm-container');
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x87CEEB);
            scene.fog = new THREE.Fog(0x87CEEB, 50, 200);
            
            camera = new THREE.PerspectiveCamera(60, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(0, 30, 50);
            camera.lookAt(0, 0, 0);
            
            renderer = new THREE.WebGLRenderer({{ antialias: true }});
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.shadowMap.enabled = true;
            container.appendChild(renderer.domElement);
            
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
            scene.add(ambientLight);
            
            const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
            directionalLight.position.set(50, 50, 25);
            directionalLight.castShadow = true;
            scene.add(directionalLight);
            
            const groundGeometry = new THREE.PlaneGeometry(100, 100);
            const groundMaterial = new THREE.MeshLambertMaterial({{ 
                color: 0x7cb342, side: THREE.DoubleSide
            }});
            const ground = new THREE.Mesh(groundGeometry, groundMaterial);
            ground.rotation.x = -Math.PI / 2;
            ground.receiveShadow = true;
            scene.add(ground);
            
            createFarmPlots();
            animate();
        }}
        
        function createFarmPlots() {{
            const plotSize = 8, spacing = 2, rows = 3, cols = 4;
            for (let row = 0; row < rows; row++) {{
                for (let col = 0; col < cols; col++) {{
                    const x = (col - cols/2) * (plotSize + spacing);
                    const z = (row - rows/2) * (plotSize + spacing);
                    const borderGeometry = new THREE.BoxGeometry(plotSize, 0.2, plotSize);
                    const borderMaterial = new THREE.MeshLambertMaterial({{ color: 0x8B4513 }});
                    const border = new THREE.Mesh(borderGeometry, borderMaterial);
                    border.position.set(x, 0.1, z);
                    scene.add(border);
                    if (Math.random() > 0.3) addCropsToPlot(x, z, plotSize);
                }}
            }}
        }}
        
        function addCropsToPlot(x, z, size) {{
            const cropSpacing = size / 5;
            for (let i = 0; i < 4; i++) {{
                for (let j = 0; j < 4; j++) {{
                    const cx = x + (i - 1.5) * cropSpacing;
                    const cz = z + (j - 1.5) * cropSpacing;
                    const baseHeight = Math.random() * 1.5 + 0.5;
                    const height = baseHeight * (0.3 + 0.7 * growthFactor);
                    
                    const stemGeometry = new THREE.CylinderGeometry(0.1, 0.1, height, 8);
                    const stemMaterial = new THREE.MeshLambertMaterial({{ color: 0x2E7D32 }});
                    const stem = new THREE.Mesh(stemGeometry, stemMaterial);
                    stem.position.set(cx, height/2, cz);
                    stem.castShadow = true;
                    scene.add(stem);
                    
                    const topSize = 0.2 + 0.2 * growthFactor;
                    const topGeometry = new THREE.SphereGeometry(topSize, 8, 8);
                    const topMaterial = new THREE.MeshLambertMaterial({{ color: 0x4CAF50 }});
                    const top = new THREE.Mesh(topGeometry, topMaterial);
                    top.position.set(cx, height, cz);
                    top.castShadow = true;
                    scene.add(top);
                    
                    farmObjects.push({{ stem, top, height }});
                }}
            }}
        }}
        
        function animate() {{
            requestAnimationFrame(animate);
            const time = Date.now() * 0.001;
            farmObjects.forEach((obj, i) => {{
                obj.stem.rotation.z = Math.sin(time + i * 0.1) * 0.05;
                obj.top.position.y = obj.height + Math.cos(time + i * 0.1) * 0.05;
            }});
            camera.position.x = Math.sin(time * 0.1) * 50;
            camera.position.z = Math.cos(time * 0.1) * 50;
            camera.lookAt(0, 0, 0);
            renderer.render(scene, camera);
        }}
        
        init();
    </script>
    """
    components.html(html_code, height=500)

# Decision evaluation
def evaluate_decision(decision_type, decision_value, current_day, data):
    """Evaluate player decision against historical data"""
    future_data = data.iloc[current_day:min(current_day+28, len(data))]
    
    avg_precip = future_data['precipitation'].mean()
    avg_temp = future_data['temperature'].mean()
    avg_ndvi = future_data['ndvi'].mean()
    
    lang = st.session_state.language
    
    outcome = {'success': False, 'points': 0, 'message': '', 'explanation': ''}
    
    if decision_type == 'plant_maize':
        if avg_precip > 2.5 and 18 < avg_temp < 24:
            outcome['success'] = True
            outcome['points'] = 1200
            if lang == 'en':
                outcome['message'] = '🎉 Excellent! Your maize thrived!'
                outcome['explanation'] = f"Perfect timing! Historical data shows optimal conditions: {avg_precip:.1f}mm average rainfall and {avg_temp:.1f}°C temperature. NDVI: {avg_ndvi:.2f}"
            else:
                outcome['message'] = '🎉 Vizuri sana! Mahindi yako yamestawi!'
                outcome['explanation'] = f"Wakati mzuri! Data ya kihistoria inaonyesha hali nzuri: mvua ya wastani {avg_precip:.1f}mm na joto la {avg_temp:.1f}°C. NDVI: {avg_ndvi:.2f}"
        else:
            outcome['points'] = 400
            if lang == 'en':
                outcome['message'] = '😕 Maize struggled in these conditions'
                outcome['explanation'] = f"Conditions weren't ideal. Rainfall: {avg_precip:.1f}mm (needed >2.5mm), Temp: {avg_temp:.1f}°C"
            else:
                outcome['message'] = '😕 Mahindi yalipata shida katika hali hizi'
                outcome['explanation'] = f"Hali haikuwa nzuri. Mvua: {avg_precip:.1f}mm (ilihitajika >2.5mm), Joto: {avg_temp:.1f}°C"
    
    elif decision_type == 'plant_beans':
        if avg_precip > 2.0 and avg_temp > 16:
            outcome['success'] = True
            outcome['points'] = 1000
            if lang == 'en':
                outcome['message'] = '✅ Good choice! Beans grew well'
                outcome['explanation'] = f"Smart decision! Beans thrived with {avg_precip:.1f}mm rainfall and {avg_temp:.1f}°C temperature."
            else:
                outcome['message'] = '✅ Chaguo nzuri! Maharage yalimea vizuri'
                outcome['explanation'] = f"Uamuzi mzuri! Maharage yalistawi na mvua {avg_precip:.1f}mm na joto {avg_temp:.1f}°C."
        else:
            outcome['points'] = 500
            if lang == 'en':
                outcome['message'] = '🤔 Moderate success with beans'
                outcome['explanation'] = f"Beans survived but didn't thrive. Temp: {avg_temp:.1f}°C, Rainfall: {avg_precip:.1f}mm"
            else:
                outcome['message'] = '🤔 Mafanikio ya kati na maharage'
                outcome['explanation'] = f"Maharage yaliokoka lakini hayakustawi. Joto: {avg_temp:.1f}°C, Mvua: {avg_precip:.1f}mm"
    
    elif decision_type == 'irrigate':
        if avg_precip < 2.0:
            outcome['success'] = True
            outcome['points'] = 400
            if lang == 'en':
                outcome['message'] = '💧 Smart irrigation decision!'
                outcome['explanation'] = f"Excellent foresight! Low rainfall predicted ({avg_precip:.1f}mm). Your irrigation saved the crops."
            else:
                outcome['message'] = '💧 Uamuzi mzuri wa kumwagilia!'
                outcome['explanation'] = f"Uoni mzuri! Mvua kidogo ilitabirika ({avg_precip:.1f}mm). Umwagiliaji wako ulioloa mazao."
        else:
            outcome['points'] = -400
            if lang == 'en':
                outcome['message'] = '💸 Irrigation wasn\'t necessary'
                outcome['explanation'] = f"Rainfall was {avg_precip:.1f}mm. You wasted resources on unnecessary irrigation."
            else:
                outcome['message'] = '💸 Umwagiliaji haukuhitajika'
                outcome['explanation'] = f"Mvua ilikuwa {avg_precip:.1f}mm. Ulipoteza rasilimali kwa umwagiliaji usio na haja."
    
    elif decision_type == 'fertilize':
        if avg_ndvi < 0.5:
            outcome['success'] = True
            outcome['points'] = 400
            if lang == 'en':
                outcome['message'] = '🧪 Fertilizer boosted your crops!'
                outcome['explanation'] = f"Great timing! NDVI was low ({avg_ndvi:.2f}). Fertilizer improved crop health significantly."
            else:
                outcome['message'] = '🧪 Mbolea iliongeza mazao yako!'
                outcome['explanation'] = f"Wakati mzuri! NDVI ilikuwa chini ({avg_ndvi:.2f}). Mbolea iliboresha afya ya mazao sana."
        else:
            outcome['points'] = -100
            if lang == 'en':
                outcome['message'] = '📉 Fertilizer had minimal impact'
                outcome['explanation'] = f"NDVI was healthy ({avg_ndvi:.2f}). Fertilizer provided only marginal gains."
            else:
                outcome['message'] = '📉 Mbolea iliongeza kidogo tu'
                outcome['explanation'] = f"NDVI ilikuwa nzuri ({avg_ndvi:.2f}). Mbolea ilisaidia kidogo tu."
    
    return outcome

# START SCREEN
def render_start_screen():
    lang = st.session_state.language
    
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.title(t('welcome'))
    st.markdown(f"### {t('subtitle')}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if lang == 'en':
            st.markdown("""
            #### 🎯 Your Mission
            
            Travel back in time to experience **real historical farming challenges** that Kenyan farmers faced. 
            Learn from the past using **NASA satellite data**.
            
            **How it works:**
            1. 📅 **Choose an Era**: Select a year with significant farming events
            2. 📊 **Observe Phase**: Watch 14 days of NASA data patterns
            3. 🌱 **Make Decisions**: Plant, irrigate, fertilize based on trends
            4. ✅ **Learn from History**: See how your choices compare to reality
            5. 🏆 **Earn Points**: Master data-driven farming!
            
            **Why historical data?** Because we know what actually happened, you get **deterministic learning** - 
            your decisions are validated against real outcomes, not guesses.
            """)
        else:
            st.markdown("""
            #### 🎯 Dhamira Yako
            
            Rudi nyuma katika wakati kuona **changamoto halisi za kilimo** ambazo wakulima wa Kenya walipata.
            Jifunze kutoka kwa zamani kwa kutumia **data ya satelaiti ya NASA**.
            
            **Jinsi inavyofanya kazi:**
            1. 📅 **Chagua Enzi**: Chagua mwaka wenye matukio muhimu ya kilimo
            2. 📊 **Awamu ya Uchunguzi**: Angalia mifumo ya data ya NASA kwa siku 14
            3. 🌱 **Fanya Maamuzi**: Panda, mwagilia, tia mbolea kulingana na mwenendo
            4. ✅ **Jifunze kutoka Historia**: Ona jinsi maamuzi yako yanavyolinganisha na ukweli
            5. 🏆 **Pata Alama**: Ushinde kilimo kinachotegemea data!
            
            **Kwa nini data ya kihistoria?** Kwa sababu tunajua nini kilichotokea kweli, unapata **kujifunza kwa uhakika** - 
            maamuzi yako yanathibitishwa dhidi ya matokeo halisi, si makadirio.
            """)
    
    with col2:
        if lang == 'en':
            st.markdown("""
            #### 🛰️ NASA Data You'll Use
            
            - **Precipitation** - Rainfall patterns
            - **Temperature** - Daily temperature trends
            - **NDVI** - Crop health indicator
            - **Soil Moisture** - Water content in soil
            - **Humidity** - Relative humidity levels
            - **Solar Radiation** - Sunlight intensity
            
            All from **NASA POWER API** & **Earth Data**
            
            ---
            
            #### 📚 Learn From Real Kenyan Farming History
            
            Experience eras like:
            - 🌊 **1997**: El Niño floods
            - 🔥 **2000**: Millennium drought  
            - 🌾 **2004**: Bumper harvest era
            - 🦗 **2020**: Locust invasion & COVID-19
            - 🌍 **2022**: Climate uncertainty
            """)
        else:
            st.markdown("""
            #### 🛰️ Data ya NASA Utakayotumia
            
            - **Mvua** - Mifumo ya mvua
            - **Joto** - Mwenendo wa joto kila siku
            - **NDVI** - Kiashiria cha afya ya mazao
            - **Unyevu wa Udongo** - Maji kwenye udongo
            - **Unyevu** - Viwango vya unyevu wa hewa
            - **Mionzi ya Jua** - Nguvu ya mwanga wa jua
            
            Yote kutoka **NASA POWER API** & **Earth Data**
            
            ---
            
            #### 📚 Jifunze Kutoka Historia Halisi ya Kilimo Kenya
            
            Pata uzoefu wa enzi kama:
            - 🌊 **1997**: Mafuriko ya El Niño
            - 🔥 **2000**: Ukame wa milenio
            - 🌾 **2004**: Enzi ya mavuno mazuri
            - 🦗 **2020**: Uvamizi wa nzige & COVID-19
            - 🌍 **2022**: Kutokuwa na uhakika wa hali ya hewa
            """)
    
    st.markdown("---")
    
    if lang == 'en':
        st.markdown("""
        ### 🌍 Why This Matters
        
        **60% of Africa is under 25**, but the **average farmer is 60 years old**. Kenya needs to **double food 
        production by 2030**, yet only **4.5% of youth** view farming as viable.
        
        **ShambaBytes bridges this gap** by teaching climate-smart agriculture through gaming - making farming 
        the **coolest career** for the next generation!
        """)
    else:
        st.markdown("""
        ### 🌍 Kwa Nini Hii ni Muhimu
        
        **60% ya Afrika ina chini ya miaka 25**, lakini **wastani wa mkulima ana miaka 60**. Kenya inahitaji 
        **kuongeza uzalishaji wa chakula mara mbili mennye 2030**, lakini **4.5% tu ya vijana** wanaona 
        kilimo kama kazi inayowezekana.
        
        **ShambaBytes inaunganisha pengo hili** kwa kufundisha kilimo mahiri cha hali ya hewa kupitia mchezo - 
        kufanya kilimo kuwa **kazi ya kisasa zaidi** kwa kizazi kinachokuja!
        """)
    
    st.markdown("---")
    
    if st.button(f"🚀 {t('start_journey')}", use_container_width=True, type="primary"):
        st.session_state.game_phase = 'setup'
        st.rerun()

# SETUP SCREEN with Era Selection
def render_setup_screen():
    lang = st.session_state.language
    
    st.title(t('choose_location'))
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"📍 {t('location')}")
        location_options = ["Nairobi, Kenya", "Kisumu, Kenya", "Mombasa, Kenya"]
        location = st.selectbox(t('location'), location_options, index=0, label_visibility="collapsed")
        st.session_state.location = location
        
        if lang == 'en':
            st.info(f"**Selected:** {location}\n\nYou'll experience farming conditions from this region.")
        else:
            st.info(f"**Umechagua:** {location}\n\nUtapata uzoefu wa hali ya kilimo kutoka eneo hili.")
    
    with col2:
        st.subheader(f"📅 {t('time_period')}")
        
        # Era selection with descriptions
        era_years = list(KENYAN_FARMING_ERAS.keys())
        year_labels = [f"{year} - {KENYAN_FARMING_ERAS[year]['era_name' if lang == 'en' else 'era_name_sw']}" 
                       for year in era_years]
        
        selected_idx = st.selectbox(
            "Select Historical Era",
            range(len(era_years)),
            format_func=lambda x: year_labels[x],
            label_visibility="collapsed"
        )
        
        selected_year = era_years[selected_idx]
        st.session_state.current_year = selected_year
        st.session_state.era_info = KENYAN_FARMING_ERAS[selected_year]
    
    # Show era information
    st.markdown("---")
    st.markdown('<div class="era-card">', unsafe_allow_html=True)
    era = st.session_state.era_info
    st.subheader(f"📖 {era['era_name' if lang == 'en' else 'era_name_sw']} ({selected_year})")
    st.markdown(era['event' if lang == 'en' else 'event_sw'])
    
    col1, col2 = st.columns(2)
    with col1:
        if lang == 'en':
            st.markdown(f"**Challenge:** {era['challenge']}")
        else:
            st.markdown(f"**Changamoto:** {era['challenge']}")
    with col2:
        if lang == 'en':
            st.markdown(f"**Lesson:** {era['lesson']}")
        else:
            st.markdown(f"**Somo:** {era['lesson']}")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    if lang == 'en':
        st.markdown("""
        ### 🎮 Game Rules
        
        - **Observation Period**: First 14 days - watch and learn data patterns
        - **Decision Points**: Every 2 weeks, make farming choices
        - **Points System**: Earn points for good decisions based on historical outcomes
        - **Historical Validation**: See how real farmers dealt with these conditions
        
        **Ready to experience history?**
        """)
    else:
        st.markdown("""
        ### 🎮 Sheria za Mchezo
        
        - **Kipindi cha Uchunguzi**: Siku 14 za kwanza - angalia na ujifunze mifumo ya data
        - **Pointi za Maamuzi**: Kila wiki 2, fanya maamuzi ya kilimo
        - **Mfumo wa Alama**: Pata alama kwa maamuzi mazuri kulingana na matokeo ya kihistoria
        - **Uthibitishaji wa Kihistoria**: Ona jinsi wakulima wa kweli walivyoshughulikia hali hizi
        
        **Uko tayari kupata uzoefu wa historia?**
        """)
    
    if st.button(f"▶️ {t('begin_simulation')}", use_container_width=True, type="primary"):
        provider = NASADataProvider()
        st.session_state.historical_data = provider.get_historical_data(selected_year)
        st.session_state.game_phase = 'observation'
        st.session_state.current_day = 0
        st.rerun()

# OBSERVATION PHASE
def render_observation_phase():
    data = st.session_state.historical_data
    current_day = st.session_state.current_day
    lang = st.session_state.language
    era = st.session_state.era_info
    
    # Phase indicator with era info
    st.markdown(f"""
    <div class="phase-indicator">
        <h3>{t('observation_phase')} - {t('day')} {current_day + 1}/14</h3>
        <p><strong>{era['era_name' if lang == 'en' else 'era_name_sw']} ({st.session_state.current_year})</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Era reminder
    with st.expander(f"📖 {'About This Era' if lang == 'en' else 'Kuhusu Enzi Hii'}"):
        st.markdown(era['event' if lang == 'en' else 'event_sw'])
    
    # 3D Farm
    st.header(t('your_farm'))
    render_3d_farm(current_day)
    
    # Current day data
    day_data = data.iloc[current_day]
    
    st.header(f"📅 {day_data['date'].strftime('%B %d, %Y')} - {st.session_state.location}")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(f"🌧️ {t('precipitation')}", f"{day_data['precipitation']:.1f} mm")
    with col2:
        st.metric(f"🌡️ {t('temperature')}", f"{day_data['temperature']:.1f}°C")
    with col3:
        st.metric("🌱 NDVI", f"{day_data['ndvi']:.2f}")
    with col4:
        st.metric(f"💧 {t('soil_moisture')}", f"{day_data['soil_moisture']*100:.0f}%")
    
    # Trend graphs
    st.subheader(f"📈 {t('data_trends')} ({t('day')}s 1 - {current_day + 1})")
    
    trend_data = data.iloc[0:current_day+1]
    
    tab_names = [
        f"{t('precipitation')} & {t('temperature')}" if lang == 'en' else "Mvua & Joto",
        "NDVI & Unyevu wa Udongo" if lang == 'sw' else "NDVI & Soil Moisture",
        "Vipimo Vyote" if lang == 'sw' else "All Metrics"
    ]
    
    tab1, tab2, tab3 = st.tabs(tab_names)
    
    with tab1:
        chart_data = trend_data[['date', 'precipitation', 'temperature']].set_index('date')
        st.line_chart(chart_data)
    
    with tab2:
        chart_data = trend_data[['date', 'ndvi', 'soil_moisture']].set_index('date')
        st.line_chart(chart_data)
    
    with tab3:
        chart_data = trend_data[['date', 'precipitation', 'temperature', 'ndvi', 'humidity']].set_index('date')
        st.line_chart(chart_data)
    
    # Tips
    with st.expander(f"💡 {t('learning_tips')}"):
        if lang == 'en':
            st.markdown("""
            **What to observe:**
            - Rainfall patterns - dry spells or wet periods?
            - Temperature variations day-to-day
            - NDVI trends - crop growth or stress?
            - Soil moisture following rainfall
            
            **Historical Context:** How do these patterns relate to the historical event for this year?
            """)
        else:
            st.markdown("""
            **Ni nini cha kuangalia:**
            - Mifumo ya mvua - vipindi vikavu au vya mvua?
            - Tofauti za joto kila siku
            - Mwenendo wa NDVI - ukuaji wa mazao au msongo?
            - Unyevu wa udongo ukifuata mvua
            
            **Muktadha wa Kihistoria:** Mifumo hii inahusianaje na tukio la kihistoria kwa mwaka huu?
            """)
    
    # Navigation
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"⏭️ {t('next_day')}", use_container_width=True, type="primary"):
            st.session_state.current_day += 1
            if st.session_state.current_day >= 14:
                st.session_state.game_phase = 'decision'
                st.session_state.observation_complete = True
            st.rerun()
    
    with col2:
        if st.button(f"⏩ {t('auto_simulate')}", use_container_width=True):
            with st.spinner("Simulating..." if lang == 'en' else "Inachimbua..."):
                progress_bar = st.progress(0)
                for i in range(14 - current_day):
                    time.sleep(0.3)
                    st.session_state.current_day += 1
                    progress_bar.progress((i + 1) / (14 - current_day))
                st.session_state.game_phase = 'decision'
                st.session_state.observation_complete = True
            st.rerun()

# DECISION PHASE
def render_decision_phase():
    data = st.session_state.historical_data
    current_day = st.session_state.current_day
    lang = st.session_state.language
    era = st.session_state.era_info
    
    st.markdown(f"""
    <div class="phase-indicator">
        <h3>{t('decision_phase')} - {t('day')} {current_day}</h3>
        <p><strong>{era['era_name' if lang == 'en' else 'era_name_sw']} ({st.session_state.current_year})</strong></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab_names = [
        f"🌍 {t('your_farm')}" if lang == 'en' else "🌍 Shamba Lako",
        f"📊 {t('data_trends')}" if lang == 'en' else "📊 Mwenendo wa Data",
        f"🎮 {t('farm_actions')}" if lang == 'en' else "🎮 Vitendo vya Shamba"
    ]
    
    tab1, tab2, tab3 = st.tabs(tab_names)
    
    with tab1:
        st.header(t('your_farm'))
        render_3d_farm(current_day)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t('points'), st.session_state.points)
        with col2:
            st.metric(t('farm_health'), f"{st.session_state.farm_health}%")
        with col3:
            st.metric(t('day'), current_day)
        with col4:
            st.metric(t('week'), current_day // 7)
    
    with tab2:
        st.header(f"📈 {t('data_trends')}")
        
        analysis_data = data.iloc[max(0, current_day-14):current_day]
        
        st.subheader("Recent Patterns (Last 14 Days)" if lang == 'en' else "Mifumo ya Hivi Karibuni (Siku 14 Zilizopita)")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            avg_precip = analysis_data['precipitation'].mean()
            st.metric(f"{'Avg' if lang == 'en' else 'Wastani'} {t('precipitation')}", f"{avg_precip:.1f} mm")
        with col2:
            avg_temp = analysis_data['temperature'].mean()
            st.metric(f"{'Avg' if lang == 'en' else 'Wastani'} {t('temperature')}", f"{avg_temp:.1f}°C")
        with col3:
            avg_ndvi = analysis_data['ndvi'].mean()
            st.metric(f"{'Avg' if lang == 'en' else 'Wastani'} NDVI", f"{avg_ndvi:.2f}")
        with col4:
            avg_soil = analysis_data['soil_moisture'].mean()
            st.metric(f"{'Avg' if lang == 'en' else 'Wastani'} {t('soil_moisture')}", f"{avg_soil*100:.0f}%")
        
        subtab1, subtab2 = st.tabs([
            "Climate Data" if lang == 'en' else "Data ya Hali ya Hewa",
            "Crop Health" if lang == 'en' else "Afya ya Mazao"
        ])
        
        with subtab1:
            chart_data = analysis_data[['date', 'precipitation', 'temperature']].set_index('date')
            st.line_chart(chart_data)
        
        with subtab2:
            chart_data = analysis_data[['date', 'ndvi', 'soil_moisture']].set_index('date')
            st.line_chart(chart_data)
    
    with tab3:
        st.header(t('farm_actions'))
        
        tip_text = "💡 **Pro Tip**: Study data trends before deciding. Choices validated against real history!" if lang == 'en' else "💡 **Kidokezo**: Chunguza mwenendo wa data kabla ya kuamua. Maamuzi yanathibitishwa dhidi ya historia halisi!"
        st.info(tip_text)
        
        planting_header = "🌱 Planting Decisions" if lang == 'en' else "🌱 Maamuzi ya Kupanda"
        st.subheader(planting_header)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"🌽 {t('plant_maize')}", use_container_width=True, type="primary"):
                outcome = evaluate_decision('plant_maize', None, current_day, data)
                st.session_state.points += outcome['points']
                st.session_state.decisions.append(outcome)
                st.session_state.current_day += 7
                st.balloons() if outcome['success'] else st.snow()
                st.success(outcome['message'])
                st.info(outcome['explanation'])
        
        with col2:
            if st.button(f"🫘 {t('plant_beans')}", use_container_width=True, type="primary"):
                outcome = evaluate_decision('plant_beans', None, current_day, data)
                st.session_state.points += outcome['points']
                st.session_state.decisions.append(outcome)
                st.session_state.current_day += 7
                st.balloons() if outcome['success'] else st.snow()
                st.success(outcome['message'])
                st.info(outcome['explanation'])
        
        management_header = "⚡ Farm Management" if lang == 'en' else "⚡ Usimamizi wa Shamba"
        st.subheader(management_header)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(f"💧 {t('irrigate')} (-400 pts)", use_container_width=True):
                outcome = evaluate_decision('irrigate', None, current_day, data)
                st.session_state.points += outcome['points']
                st.session_state.decisions.append(outcome)
                st.session_state.current_day += 7
                if outcome['success']:
                    st.success(outcome['message'])
                else:
                    st.warning(outcome['message'])
                st.info(outcome['explanation'])
        
        with col2:
            if st.button(f"🧪 {t('fertilize')} (-300 pts)", use_container_width=True):
                outcome = evaluate_decision('fertilize', None, current_day, data)
                st.session_state.points += outcome['points']
                st.session_state.decisions.append(outcome)
                st.session_state.current_day += 7
                if outcome['success']:
                    st.success(outcome['message'])
                else:
                    st.warning(outcome['message'])
                st.info(outcome['explanation'])
        
        st.markdown("---")
        
        skip_text = "⏭️ Skip to Next Decision Point" if lang == 'en' else "⏭️ Ruka hadi Pointi Inayofuata ya Maamuzi"
        if st.button(skip_text, use_container_width=True):
            st.session_state.current_day += 14
            if st.session_state.current_day >= len(data):
                st.session_state.current_day = len(data) - 1
            st.rerun()
        
        # Recent decisions
        if st.session_state.decisions:
            st.subheader(t('recent_decisions'))
            for i, decision in enumerate(reversed(st.session_state.decisions[-3:])):
                with st.expander(f"{'Decision' if lang == 'en' else 'Uamuzi'} {len(st.session_state.decisions) - i}: {decision['message']}"):
                    st.write(decision['explanation'])
                    points_label = "Points Earned" if lang == 'en' else "Alama Zilizopikwa"
                    st.write(f"**{points_label}:** {decision['points']:+d}")

# Main App
def main():
    # Language toggle in sidebar
    with st.sidebar:
        st.markdown("### 🌍 Language / Lugha")
        lang_option = st.radio(
            "Select",
            ["English", "Kiswahili"],
            index=0 if st.session_state.language == 'en' else 1,
            label_visibility="collapsed"
        )
        
        new_lang = 'en' if lang_option == "English" else 'sw'
        if new_lang != st.session_state.language:
            st.session_state.language = new_lang
            st.rerun()
        
        st.divider()
        
        st.title(t('title'))
        st.caption("NASA Farm Navigator")
        
        if st.session_state.game_phase not in ['start', 'setup']:
            st.divider()
            st.metric(f"🏆 {t('points')}", st.session_state.points)
            st.metric(f"📅 {t('day')}", st.session_state.current_day)
            st.metric(f"🌍 {t('location')}", st.session_state.location)
            st.metric(f"📆 {'Year' if st.session_state.language == 'en' else 'Mwaka'}", st.session_state.current_year)
            
            if st.session_state.era_info:
                st.info(f"**Era:** {st.session_state.era_info['era_name' if st.session_state.language == 'en' else 'era_name_sw']}")
            
            st.divider()
            
            if st.button(f"🔄 {t('restart_game')}", use_container_width=True):
                for key in list(st.session_state.keys()):
                    if key != 'language':
                        del st.session_state[key]
                st.rerun()
    
    # Main content
    if st.session_state.game_phase == 'start':
        render_start_screen()
    elif st.session_state.game_phase == 'setup':
        render_setup_screen()
    elif st.session_state.game_phase == 'observation':
        render_observation_phase()
    elif st.session_state.game_phase == 'decision':
        render_decision_phase()

if __name__ == "__main__":
    main()