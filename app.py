# app.py (v2.0 - The Masterpiece UI)

import streamlit as st
from report_generator import generate_dynamic_report
from templates import REPORT_TEMPLATES
from file_generator import create_docx, create_pdf

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Scribe",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS Styling ---
def load_css(theme):
    """Loads a CSS file based on the selected theme."""
    file_path = f"themes/{theme}.css"
    try:
        with open(file_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback to default styling if CSS is not found
        st.warning(f"Theme file '{file_path}' not found. Using default Streamlit styling.")

# --- Session State Initialization ---
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"
if "incident_data" not in st.session_state:
    st.session_state.incident_data = {}
if "final_report" not in st.session_state:
    st.session_state.final_report = None

# Apply the selected theme
load_css(st.session_state.theme)

# ======================================================================================
# --- SIDEBAR (Control Panel) ---
# ======================================================================================
with st.sidebar:
    # --- Theme Switcher ---
    if st.toggle("✨ Activate Light Mode", value=(st.session_state.theme == "Light")):
        st.session_state.theme = "Light"
    else:
        st.session_state.theme = "Dark"
        
    st.title("✒️ AI Scribe")
    st.caption("Your AI-powered reporting assistant.")
    
    st.write("---")

    # --- Template Selection ---
    st.header("Step 1: Choose a Template")
    template_name = st.selectbox(
        "Select a report type:",
        options=list(REPORT_TEMPLATES.keys())
    )
    
    # --- Core Data Entry ---
    st.header("Step 2: Provide Incident Details")
    with st.form("core_details_form"):
        analyst_name = st.text_input("Analyst Name", placeholder="e.g., Priya Singh")
        incident_id = st.text_input("Incident ID / Case Number", placeholder="e.g., INC-1138")
        raw_notes = st.text_area("Analyst's Raw Notes", height=200, placeholder="Describe the incident... what you found, what you did, any initial thoughts.")
        
        submitted = st.form_submit_button("Lock Core Details")
        if submitted:
            st.session_state.incident_data = {
                "Analyst Name": analyst_name,
                "Incident ID": incident_id,
                "Raw Notes": raw_notes
            }
            st.success("Core details saved!")

    # --- Generate Button ---
    st.write("---")
    if st.button("🚀 Generate Report", use_container_width=True, type="primary"):
        if not st.session_state.get("incident_data"):
            st.warning("Please lock in the core details first.")
        else:
            # This triggers the report generation in the main panel
            st.session_state.final_report = "GENERATING" 

# ======================================================================================
# --- MAIN CONTENT AREA (Canvas) ---
# ======================================================================================

# If a report is being generated, show the multi-stage process
if st.session_state.final_report == "GENERATING":
    with st.spinner("Initializing AI Analyst..."):
        # Get the chosen template's sections
        template_sections = REPORT_TEMPLATES[template_name]['sections']
        
        # Call the powerful backend function
        report = generate_dynamic_report(
            raw_alert_data=st.session_state.incident_data,
            required_sections=template_sections
        )
        st.session_state.final_report = report
    st.rerun() # Rerun to display the final report

# If a report has been generated, display it
elif st.session_state.final_report:
    st.header("✅ Report Finalized")
    st.markdown(st.session_state.final_report)
    
    st.write("---")
    st.header("📥 Download Report")

    # Create downloadable files in memory
    docx_file = create_docx(st.session_state.final_report)
    pdf_file = create_pdf(st.session_state.final_report)

    dl_col1, dl_col2 = st.columns(2)
    with dl_col1:
        st.download_button(
            label="📄 Download as DOCX",
            data=docx_file,
            file_name=f"{st.session_state.incident_data.get('Incident ID', 'report')}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )
    with dl_col2:
        st.download_button(
            label="📕 Download as PDF",
            data=pdf_file,
            file_name=f"{st.session_state.incident_data.get('Incident ID', 'report')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

# If the app is idle, show a welcome screen
else:
    st.header("Welcome to your AI Reporting Assistant")
    st.markdown("Please fill out the details in the sidebar to your left and click **Generate Report** to begin.")
    st.image("https://images.pexels.com/photos/5474040/pexels-photo-5474040.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2", caption="Your canvas awaits...")