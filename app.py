import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Bike Demand Predictor",
    page_icon="🚲",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------- MODEL ----------------
model = joblib.load("bike_demand_model.pkl")

# ---------------- CUSTOM CSS (light/dark aware, warm terracotta + forest palette) ----------------
st.markdown("""
<style>
:root {
    --accent: #E07A5F;
    --accent-soft: #F2CC8F;
    --forest: #3D5A4C;
    --bg-card: #ffffff;
    --bg-page: #FAF7F2;
    --text-main: #2B2B2B;
    --text-sub: #6b6b6b;
    --border-soft: rgba(0,0,0,0.06);
}

@media (prefers-color-scheme: dark) {
    :root {
        --accent: #E9967A;
        --accent-soft: #D9A441;
        --forest: #7FA98F;
        --bg-card: #1E211F;
        --bg-page: #141615;
        --text-main: #F2EFEA;
        --text-sub: #b7b3ac;
        --border-soft: rgba(255,255,255,0.08);
    }
}

.stApp {
    background: var(--bg-page);
    color: var(--text-main);
}

/* Hero header */
.hero {
    text-align: center;
    padding: 2.2rem 1rem 1.6rem 1rem;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-soft) 100%);
    border-radius: 18px;
    margin-bottom: 1.8rem;
    box-shadow: 0 8px 24px rgba(224, 122, 95, 0.25);
}
.hero h1 {
    color: white;
    font-size: 2.1rem;
    font-weight: 800;
    margin: 0;
    letter-spacing: -0.5px;
}
.hero p {
    color: rgba(255,255,255,0.92);
    font-size: 1rem;
    margin-top: 0.4rem;
}

/* Section cards */
.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border-soft);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 10px rgba(0,0,0,0.04);
}
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--forest);
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Labels */
label, .stSelectbox label, .stSlider label {
    color: var(--text-main) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

/* Slider accent */
.stSlider [role="slider"] {
    background-color: var(--accent) !important;
}
div[data-baseweb="slider"] > div > div > div {
    background: var(--accent) !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: var(--bg-card) !important;
    border-color: var(--border-soft) !important;
    border-radius: 10px !important;
}

/* Predict button */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, var(--forest) 0%, #2E4438 100%);
    color: white;
    font-weight: 700;
    font-size: 1.05rem;
    padding: 0.8rem 0;
    border-radius: 12px;
    border: none;
    box-shadow: 0 6px 16px rgba(61, 90, 76, 0.3);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(61, 90, 76, 0.4);
    color: white;
}

/* Result card */
.result-card {
    text-align: center;
    background: linear-gradient(135deg, var(--forest) 0%, #2E4438 100%);
    border-radius: 18px;
    padding: 1.8rem;
    margin-top: 1.4rem;
    box-shadow: 0 8px 24px rgba(61, 90, 76, 0.3);
}
.result-card .label {
    color: rgba(255,255,255,0.85);
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
.result-card .value {
    color: white;
    font-size: 3rem;
    font-weight: 800;
    margin: 0.3rem 0;
}
.result-card .sub {
    color: var(--accent-soft);
    font-size: 0.9rem;
}

footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- HERO ----------------
st.markdown("""
<div class="hero">
    <h1>🚲 Bike Sharing Demand Predictor</h1>
    <p>Estimate hourly rental demand from weather &amp; time conditions</p>
</div>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">📅 Time Details</div>', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    year = st.selectbox("Year", [2011, 2012])
with c2:
    month = st.selectbox("Month", list(range(1, 13)))
with c3:
    weekday = st.selectbox("Weekday", list(range(0, 7)),format_func=lambda x: ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][x])
hour = st.slider("Hour of Day", 0, 23, 12)
c4, c5 = st.columns(2)
with c4:
    holiday = st.selectbox("Holiday?", [0, 1], format_func=lambda x: "Yes" if x else "No")
with c5:
    workingday = st.selectbox("Working Day?", [0, 1], format_func=lambda x: "Yes" if x else "No")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🌦️ Weather Conditions</div>', unsafe_allow_html=True)
c6, c7 = st.columns(2)
with c6:
    season = st.selectbox("Season", [1, 2, 3, 4],
                           format_func=lambda x: {1:"🌱 Spring",2:"☀️ Summer",3:"🍂 Fall",4:"❄️ Winter"}[x])
with c7:
    weather = st.selectbox("Weather", [1, 2, 3],
                            format_func=lambda x: {1:"Clear",2:"Mist / Cloudy",3:"Rain / Snow"}[x])
temp = st.slider("Temperature (°C)", 0.0, 45.0, 20.0)
humidity = st.slider("Humidity (%)", 0, 100, 50)
windspeed = st.slider("Windspeed", 0.0, 60.0, 10.0)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICT ----------------
if st.button("Predict Demand"):
    input_df = pd.DataFrame([{
        'season': season,
        'weather': weather,
        'holiday': holiday,
        'workingday': workingday,
        'temp': temp,
        'humidity': humidity,
        'windspeed': windspeed,
        'hour_sin': np.sin(2 * np.pi * hour / 24),
        'hour_cos': np.cos(2 * np.pi * hour / 24),
        'year': year,
        'month': month,
        'weekday': weekday
    }])

    pred_log = model.predict(input_df)
    pred = int(np.expm1(pred_log)[0])

    st.markdown(f"""
    <div class="result-card">
        <div class="label">Predicted Rentals</div>
        <div class="value">{pred}</div>
        <div class="sub">bikes for this hour</div>
    </div>
    """, unsafe_allow_html=True)