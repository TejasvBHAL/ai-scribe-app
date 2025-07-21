# app.py (Clean Version)

import streamlit as st
from report_generator import generate_dynamic_report

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Scribe",
    page_icon="✒️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session State Initialization ---
if 'incident_data' not in st.session_state:
    st.session_state.incident_data = {}

# --- UI Rendering ---
st.title("✒️ AI Scribe: Dynamic Incident Reporter")
st.caption("A tool to assist with professional reporting.")


col1, col2 = st.columns((1, 1))

with col1:
    st.header("Step 1: Input Incident Data")
    st.info("Add all the raw details about the incident here.", icon="ℹ️")

    with st.form("data_input_form", clear_on_submit=True):
        key = st.text_input("Field Name (e.g., 'Analyst Name', 'Source IP')")
        value = st.text_input("Value")
        add_button = st.form_submit_button("Add Field")

        if add_button and key:
            st.session_state.incident_data[key] = value

    if st.session_state.incident_data:
        st.write("Current Incident Data:")
        st.json(st.session_state.incident_data)
        if st.button("Clear All Data"):
            st.session_state.incident_data = {}
            st.experimental_rerun()

with col2:
    st.header("Step 2: Define Report Structure")
    st.info("Select the sections you want in your final report.", icon="📝")

    common_sections = [
        "Executive Summary",
        "Incident Timeline",
        "Detailed Findings",
        "Indicators of Compromise (IOCs)",
        "MITRE ATT&CK Mapping",
        "Business Impact Assessment",
        "Recommended Remediation Plan",
    ]
    required_sections = st.multiselect(
        "Select or type the sections for your report:",
        options=common_sections,
        default=["Executive Summary", "Detailed Findings", "Recommended Remediation Plan"]
    )

    st.write("---")

    if st.button("✨ Generate Report ✨", type="primary", use_container_width=True):
        if not st.session_state.incident_data or not required_sections:
            st.warning("Please add data and select sections before generating.", icon="⚠️")
        else:
            with st.spinner("Your AI Scribe is writing..."):
                st.session_state.final_report = generate_dynamic_report(
                    raw_alert_data=st.session_state.incident_data,
                    required_sections=required_sections
                )

# --- Display Final Report ---
if 'final_report' in st.session_state:
    st.header("Generated Report")
    st.markdown(st.session_state.final_report)
    st.success("Report generated successfully!", icon="✅")
    st.balloons()