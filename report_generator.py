# report_generator.py (Backend V2)

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import streamlit as st

# --- Unified API Key Configuration ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("GEMINI_API_KEY not found in Streamlit secrets.")
        st.stop()
genai.configure(api_key=api_key)

# Initialize the Gemini Model
model = genai.GenerativeModel('gemini-1.5-flash')

def run_ai_stage(prompt):
    """A helper function to run a single AI stage."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An AI stage failed: {e}")
        return None

def generate_dynamic_report(raw_alert_data: dict, required_sections: list) -> str:
    """
    Runs the multi-stage AI chain to generate a high-quality report.
    """
    raw_data_str = json.dumps(raw_alert_data, indent=2)

    # --- Stage 1: Triage & IOC Extraction ---
    st.info("Stage 1: Extracting Indicators of Compromise...")
    ioc_prompt = f"""
    Analyze the following raw incident data. Your only task is to extract all potential Indicators of Compromise (IOCs) such as IP addresses, domains, file hashes (MD5, SHA1, SHA256), URLs, and email addresses. Present the output as a clean, structured list. If no IOCs are found, state "No IOCs identified."
    
    Raw Data:
    {raw_data_str}
    """
    extracted_iocs = run_ai_stage(ioc_prompt)
    if not extracted_iocs: return "Report generation failed at Stage 1."

    # --- Stage 2: Impact Analysis ---
    st.info("Stage 2: Analyzing Business Impact...")
    impact_prompt = f"""
    Given the following incident data and extracted IOCs, analyze the potential business impact. Your only task is to provide a brief "Impact Assessment" and a "Severity Rating" (choose from: Informational, Low, Medium, High, Critical).

    Raw Data:
    {raw_data_str}

    Extracted IOCs:
    {extracted_iocs}
    """
    impact_analysis = run_ai_stage(impact_prompt)
    if not impact_analysis: return "Report generation failed at Stage 2."

    # --- Stage 3: Narrative Generation ---
    st.info("Stage 3: Writing the Full Report...")
    formatted_sections = "\n".join(f"- {section}" for section in required_sections)
    final_prompt = f"""
    You are a world-class cybersecurity analyst and technical writer. Your task is to write a complete, formal incident report.

    Use all the information provided below: the initial raw data, the extracted IOCs, and the impact analysis.
    You MUST structure your report using these sections ONLY:
    {formatted_sections}

    Synthesize all information into a coherent narrative. Be professional, clear, and precise.

    **Initial Raw Data:**
    {raw_data_str}

    **Extracted Indicators of Compromise (IOCs):**
    {extracted_iocs}

    **Impact & Severity Analysis:**
    {impact_analysis}
    
    Begin the final report now.
    """
    final_report = run_ai_stage(final_prompt)
    if not final_report: return "Report generation failed at Stage 3."
    
    st.success("All AI stages complete. Report generated.")
    return final_report