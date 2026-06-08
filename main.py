import streamlit as st
import pandas as pd
from datetime import datetime

from OccupancyFuzzyClassifier import OccupancyFuzzyClassifier

st.set_page_config(
    page_title="Klasyfikator zajęcia pokoju",
    layout="centered",
    menu_items={
        # 'Get Help': None,
        # 'Report a bug': None,
        # 'About': None
    }
)

hide_deploy_style = """
    <style>
    .stAppDeployButton {
        display: none;
    }
    </style>
"""
st.markdown(hide_deploy_style, unsafe_allow_html=True)

st.title("Klasyfikator zajęcia pokoju")
st.markdown("#### Podaj odczyty sensorów:")

@st.cache_resource
def load_classifier():
    return OccupancyFuzzyClassifier(data_path="data/Occupancy_Estimation.csv",under_sample_size=600,spread=0.6)


@st.dialog("Estymowana liczba mieszkańców:")
def show_prediction(predicted_people):
    st.markdown(f"# **{predicted_people}**")
    if st.button("Powrót"):
        st.rerun()

with st.form("occupancy_form"):

    st.subheader("🌡️ Temperatura (°C)")
    col1, col2 = st.columns(2)
    with col1:
        s1_temp = st.number_input("S1 Temperatura", value=24.0, step=0.1, format="%.2f")
        s3_temp = st.number_input("S3 Temperatura", value=24.0, step=0.1, format="%.2f")
    with col2:
        s2_temp = st.number_input("S2 Temperatura", value=24.0, step=0.1, format="%.2f")
        s4_temp = st.number_input("S4 Temperatura", value=24.0, step=0.1, format="%.2f")

    st.subheader("💡 Światło (lux)")
    col1, col2 = st.columns(2)
    with col1:
        s1_light = st.number_input("S1 Światło", value=0.0, step=1.0, format="%.1f")
        s3_light = st.number_input("S3 Światło", value=0.0, step=1.0, format="%.1f")
    with col2:
        s2_light = st.number_input("S2 Światło", value=0.0, step=1.0, format="%.1f")
        s4_light = st.number_input("S4 Światło", value=0.0, step=1.0, format="%.1f")

    st.subheader("🔊 Dźwięk (voltage, V)")
    col1, col2 = st.columns(2)
    with col1:
        s1_sound = st.number_input("S1 Dźwięk", value=0.0, step=0.1, format="%.2f")
        s3_sound = st.number_input("S3 Dźwięk", value=0.0, step=0.1, format="%.2f")
    with col2:
        s2_sound = st.number_input("S2 Dźwięk", value=0.0, step=0.1, format="%.2f")
        s4_sound = st.number_input("S4 Dźwięk", value=0.0, step=0.1, format="%.2f")

    st.subheader("🌫️ CO₂")
    col1, col2 = st.columns(2)
    with col1:
        s5_co2 = st.number_input("CO₂ (ppm)", value=400.0, step=0.1, format="%.1f")
    with col2:
        s5_co2_slope = st.number_input("CO₂ Slope (ppm/jednostka czasu)", value=0.0, step=0.1, format="%.2f")

    st.subheader("👤 PIR Ruch")
    col1, col2 = st.columns(2)
    with col1:
        s6_pir = st.selectbox("PIR Sensor 6", options=[0, 1], format_func=lambda x: "Ruch" if x else "Brak Ruchu")
    with col2:
        s7_pir = st.selectbox("PIR Sensor 7", options=[0, 1], format_func=lambda x: "Ruch" if x else "Brak Ruchu")

    col1, col2, col3 = st.columns(3)

    with col2:
        submitted = st.form_submit_button("Generuj wynik")

if submitted:
    input_data = pd.DataFrame([{
        'S1_Temp': s1_temp,
        'S2_Temp': s2_temp,
        'S3_Temp': s3_temp,
        'S4_Temp': s4_temp,
        'S1_Light': s1_light,
        'S2_Light': s2_light,
        'S3_Light': s3_light,
        'S4_Light': s4_light,
        'S1_Sound': s1_sound,
        'S2_Sound': s2_sound,
        'S3_Sound': s3_sound,
        'S4_Sound': s4_sound,
        'S5_CO2': s5_co2,
        'S5_CO2_Slope': s5_co2_slope,
        'S6_PIR': s6_pir,
        'S7_PIR': s7_pir
    }])

    # print(input_data)
    # Load the classifier (cached)
    classifier = load_classifier()
    # Predict
    prediction = classifier.predict(input_data)[0]  # returns a list, take first element
    # Show result in modal
    show_prediction(prediction)