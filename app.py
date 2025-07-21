# app.py (V2.1 - The Masterpiece UI)

import streamlit as st
import requests
from streamlit_lottie import st_lottie
from report_generator import generate_dynamic_report
from templates import REPORT_TEMPLATES
from file_generator import create_docx, create_pdf

# --- Helper function for Lottie animations ---
def load_lottieurl(url: str):
    """Fetches a Lottie animation from a URL."""
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Scribe",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS Styling ---
def load_css(theme):
    file_path = f"themes/{theme}.css"
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"Theme file '{file_path}' not found. Using default Streamlit styling.")

# --- Session State & Theme Application ---
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "incident_data" not in st.session_state:
    st.session_state.incident_data = {}
if "final_report" not in st.session_state:
    st.session_state.final_report = None

load_css(st.session_state.theme)

# --- SIDEBAR (Control Panel) ---
with st.sidebar:
    if st.toggle("✨ Activate Light Mode", value=(st.session_state.theme == "Light")):
        st.session_state.theme = "Light"
        st.rerun()
    else:
        st.session_state.theme = "Dark"
        
    st.title("✒️ AI Scribe")
    st.caption("Your AI-powered reporting assistant.")
    st.write("---")
    st.header("Step 1: Choose a Template")
    template_name = st.selectbox("Select a report type:", options=list(REPORT_TEMPLATES.keys()))
    st.header("Step 2: Provide Incident Details")
    with st.form("core_details_form"):
        analyst_name = st.text_input("Analyst Name", placeholder="e.g., Priya Singh")
        incident_id = st.text_input("Incident ID / Case Number", placeholder="e.g., INC-1138")
        raw_notes = st.text_area("Analyst's Raw Notes", height=200, placeholder="Describe the incident...")
        submitted = st.form_submit_button("Lock Core Details")
        if submitted:
            st.session_state.incident_data = {"Analyst Name": analyst_name, "Incident ID": incident_id, "Raw Notes": raw_notes}
            st.success("Core details saved!")
    st.write("---")
    if st.button("🚀 Generate Report", use_container_width=True, type="primary"):
        if not st.session_state.get("incident_data"):
            st.warning("Please lock in the core details first.")
        else:
            st.session_state.final_report = "GENERATING"
            st.rerun()

# --- MAIN CONTENT AREA (Canvas) ---
if st.session_state.final_report == "GENERATING":
    with st.spinner("Initializing AI Analyst..."):
        template_sections = REPORT_TEMPLATES[template_name]['sections']
        report = generate_dynamic_report(raw_alert_data=st.session_state.incident_data, required_sections=template_sections)
        st.session_state.final_report = report
    st.rerun()

elif st.session_state.final_report:
    st.header("✅ Report Finalized")
    st.markdown(st.session_state.final_report)
    st.write("---")
    st.header("📥 Download Report")
    docx_file = create_docx(st.session_state.final_report)
    pdf_file = create_pdf(st.session_state.final_report)
    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(label="📄 Download as DOCX", data=docx_file, file_name=f"{st.session_state.incident_data.get('Incident ID', 'report')}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with dl_col2:
        st.download_button(label="📕 Download as PDF", data=pdf_file, file_name=f"{st.session_state.incident_data.get('Incident ID', 'report')}.pdf", mime="application/pdf", use_container_width=True)

else:
    col1, col2 = st.columns((2,1))
    with col1:
        st.header("Welcome to your AI Reporting Assistant")
        st.markdown("""This tool helps you transform raw security notes into professional, structured incident reports in seconds.""")
    with col2:
        lottie_url = "https://lottie.host/8040adb2-1594-484c-a773-827019805625/B1j27cr0gD.json"
        try:
            r = requests.get(lottie_url)
            if r.status_code == 200:
                lottie_json = r.json()
                st_lottie(lottie_json, speed=1, height=200, key="initial")
        except requests.exceptions.RequestException as e:
            st.warning(f"Could not load animation: {e}")