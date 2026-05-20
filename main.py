import streamlit as st
import pandas as pd
from datetime import datetime

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

st.title("Klasyfikator liczby mieszkańców pokoju")
st.markdown("Podaj odczyty sensorów:")

@st.dialog("Liczba mieszkańców")
def show_prediction(predicted_people):
    st.markdown(f"### Estymowana liczba mieszkańców:")
    st.markdown(f"# **{predicted_people}**")
    st.markdown("Lorem Ipsum Dolor")
    if st.button("Close"):
        st.rerun()

with st.form("occupancy_form"):
    st.subheader("📅 Data i Godzina")
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Data", datetime.now().date())
    with col2:
        time = st.time_input("Godzina", datetime.now().time())

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
        s1_light = st.number_input("S1 Światło", value=0.0, step=0.1, format="%.2f")
        s3_light = st.number_input("S3 Światło", value=0.0, step=0.1, format="%.2f")
    with col2:
        s2_light = st.number_input("S2 Światło", value=0.0, step=0.1, format="%.2f")
        s4_light = st.number_input("S4 Światło", value=0.0, step=0.1, format="%.2f")

    st.subheader("🔊 Dźwięk (voltage, V)")
    col1, col2 = st.columns(2)
    with col1:
        s1_sound = st.number_input("S1 Dźwięk", value=0.0, step=0.1, format="%.4f")
        s3_sound = st.number_input("S3 Dźwięk", value=0.0, step=0.1, format="%.4f")
    with col2:
        s2_sound = st.number_input("S2 Dźwięk", value=0.0, step=0.1, format="%.4f")
        s4_sound = st.number_input("S4 Dźwięk", value=0.0, step=0.1, format="%.4f")

    st.subheader("🌫️ CO₂ (ppm)")
    s5_co2 = st.number_input("CO₂ (S5)", value=400.0, step=0.1, format="%.1f")

    st.subheader("👤 PIR Ruch")
    col1, col2 = st.columns(2)
    with col1:
        s6_pir = st.selectbox("PIR Sensor 6", options=[0, 1], format_func=lambda x: "Ruch" if x else "Brak Ruchu")
    with col2:
        s7_pir = st.selectbox("PIR Sensor 7", options=[0, 1], format_func=lambda x: "Ruch" if x else "Brak Ruchu")

    submitted = st.form_submit_button("🔍 Predykcja")

if submitted:
    # Placeholder prediction
    predicted_people = 3
    # Call the modal dialog function
    show_prediction(predicted_people)