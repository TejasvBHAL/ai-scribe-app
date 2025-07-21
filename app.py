# app.py (V3.2 - The Intelligent Analyst UI)

import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_lottie import st_lottie
import requests
from report_generator import generate_orca_report
from orca_alerts import ALL_ALERTS, BUSINESS_UNITS
from file_generator import create_docx, create_pdf

# --- Page Configuration ---
st.set_page_config(page_title="Orca Scribe", page_icon="🐳", layout="wide")

# --- Helper function for Lottie animations ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200: return None
    return r.json()

# --- Custom CSS ---
st.markdown("""
<style>
    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    .stApp { background-color: #0d1117; color: #c9d1d9; }
    .st-emotion-cache-16txtl3 { background-color: transparent; }
    .main-title { font-size: 3rem; font-weight: bold; text-align: center; animation: fadeIn 1s ease-out; background: -webkit-linear-gradient(45deg, #58a6ff, #a5d6ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; animation: fadeIn 1.2s ease-out; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 8px; border: 1px solid #30363d; color: #8b949e; }
    .stTabs [aria-selected="true"] { background-color: #161b22; color: #58a6ff; font-weight: bold; }
    .stButton>button[kind="primary"] { height: 3rem; font-size: 1.2rem; font-weight: bold; border: none; background: linear-gradient(45deg, #238636, #2ea043); transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(46, 160, 67, 0.3); }
    .stButton>button[kind="primary"]:hover { transform: scale(1.05); box-shadow: 0 8px 25px rgba(46, 160, 67, 0.5); }
</style>
""", unsafe_allow_html=True)

# --- Session State Initialization ---
if "report" not in st.session_state:
    st.session_state.report = None
if "report_data" not in st.session_state:
    st.session_state.report_data = {}

# --- Main App UI ---
st.markdown('<h1 class="main-title">Orca Scribe Intelligent Assistant</h1>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["**Step 1: Define Scope**", "**Step 2: Provide Analysis**", "**Step 3: Generate & Download**"])

with tab1:
    st.subheader("🎯 Define Alert Scope")
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox("Business Unit", BUSINESS_UNITS, key="business_unit")
        st.selectbox(
            "Select or Search for an Orca Alert:",
            options=ALL_ALERTS,
            key="alert_name"
        )
        st.caption("Click the box and start typing to filter the list.")
    with col2:
        lottie_url = "https://lottie.host/276352e2-9e33-4f13-a4a8-a518a2489a37/Bv8nTx1S2c.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=300, key="scope_anim")

with tab2:
    st.subheader("✍️ Provide Your Analysis")
    col1, col2 = st.columns([2, 1])
    with col1:
        st.radio("Verdict:", ["False Positive", "True Positive"], key="verdict", horizontal=True)
        st.text_area("Your Detailed Analysis", height=300, key="analyst_notes", placeholder="For an FP, explain why. For a TP, describe the impact and required remediation steps.")
    with col2:
        st.text_input("Asset(s) Impacted", key="asset_name")
        st.selectbox("Severity", ["Informational", "Low", "Medium", "High", "Critical"], key="severity")
        st.text_input("Platform Risk Rating (if applicable)", key="risk_rating")
        st.text_input("Affected URL (if applicable)", key="url")

with tab3:
    st.subheader("🚀 Generate, Preview, and Download")
    if st.button("Generate Report", use_container_width=True, type="primary"):
        report_data = {
            "business_unit": st.session_state.business_unit,
            "alert_name": st.session_state.alert_name,
            "verdict": st.session_state.verdict,
            "analyst_notes": st.session_state.analyst_notes,
            "asset_name": st.session_state.asset_name,
            "severity": st.session_state.severity,
            "risk_rating": st.session_state.risk_rating,
            "url": st.session_state.url,
            "analyst_name": "Tejas Bhal (CONTRACTOR)"
        }
        st.session_state.report_data = report_data

        final_report = generate_orca_report(report_data)
        st.session_state.report = final_report
        st.balloons()
            
    if st.session_state.report:
        st.markdown("---")
        st.subheader("📄 Report Preview")
        st.markdown(st.session_state.report)
        
        st.markdown("---")
        st.subheader("📥 Download Final Report")
        col1, col2 = st.columns(2)
        with col1:
            st.download_button("Download as DOCX", create_docx(st.session_state.report), f"{st.session_state.report_data.get('alert_name', 'report')}.docx", use_container_width=True)
        with col2:
            st.download_button("Download as PDF", create_pdf(st.session_state.report), f"{st.session_state.report_data.get('alert_name', 'report')}.pdf", use_container_width=True)