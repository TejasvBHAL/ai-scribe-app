# app.py (V2.2 - The Awesome UI)

import streamlit as st
import requests
from streamlit_lottie import st_lottie
from report_generator import generate_dynamic_report
from templates import REPORT_TEMPLATES
from file_generator import create_docx, create_pdf

# --- Helper & Config Functions (No Change) ---
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(page_title="AI Scribe", page_icon="✒️", layout="wide")

def load_css(theme):
    file_path = f"themes/{theme}.css"
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Theme file '{file_path}' not found.")

# --- Session State & Theme Application ---
if "theme" not in st.session_state:
    st.session_state.theme = "Light" # Default to the colorful theme
if "final_report" not in st.session_state:
    st.session_state.final_report = None

load_css(st.session_state.theme)

# ======================================================================================
# --- SIDEBAR (Options Panel) ---
# ======================================================================================
with st.sidebar:
    st.title("Options")
    
    # Theme Switcher
    if st.toggle("🌙 Activate Dark Mode", value=(st.session_state.theme == "Dark")):
        st.session_state.theme = "Dark"
        st.rerun()
    else:
        st.session_state.theme = "Light"

    st.write("---")

    # Template Selection
    st.header("Report Template")
    template_name = st.selectbox(
        "Select a report type:",
        options=list(REPORT_TEMPLATES.keys()),
        label_visibility="collapsed"
    )

# ======================================================================================
# --- MAIN CONTENT AREA (Canvas) ---
# ======================================================================================
st.title("✒️ AI Scribe")
st.caption("Your AI-powered reporting assistant.")

# If a report exists, show it immediately
if st.session_state.final_report:
    st.header("✅ Report Finalized")
    st.markdown(st.session_state.final_report)
    
    st.write("---")
    st.header("📥 Download Report")
    docx_file = create_docx(st.session_state.final_report)
    pdf_file = create_pdf(st.session_state.final_report)
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button("📄 Download as DOCX", docx_file, f"{st.session_state.get('incident_id', 'report')}.docx", use_container_width=True)
    with dl_col2:
        st.download_button("📕 Download as PDF", pdf_file, f"{st.session_state.get('incident_id', 'report')}.pdf", use_container_width=True)
    
    if st.button("Start New Report"):
        st.session_state.final_report = None
        st.rerun()

# If no report, show the data entry form
else:
    col1, col2 = st.columns([2, 1]) # Main form on the left, animation on the right

    with col1:
        st.header("Incident Details")
        with st.form("data_entry_form"):
            analyst_name = st.text_input("Analyst Name", placeholder="e.g., Priya Singh")
            incident_id = st.text_input("Incident ID / Case Number", placeholder="e.g., INC-1138")
            raw_notes = st.text_area("Analyst's Raw Notes", height=250, placeholder="Describe the incident in detail...")
            
            generate_button = st.form_submit_button("🚀 Generate Report", type="primary", use_container_width=True)

    with col2:
        lottie_url = "https://lottie.host/8040adb2-1594-484c-a773-827019805625/B1j27cr0gD.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=400, key="initial")

    if generate_button:
        if not raw_notes:
            st.warning("Please provide your raw notes before generating a report.")
        else:
            incident_data = {"Analyst Name": analyst_name, "Incident ID": incident_id, "Raw Notes": raw_notes}
            st.session_state.incident_id = incident_id # Store for filename
            
            with st.spinner("Initializing AI Analyst..."):
                template_sections = REPORT_TEMPLATES[template_name]['sections']
                report = generate_dynamic_report(raw_alert_data=incident_data, required_sections=template_sections)
                st.session_state.final_report = report
            st.rerun()