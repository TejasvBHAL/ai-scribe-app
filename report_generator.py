# report_generator.py (V2.1 - With Report Formatter)

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
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()

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
    """Runs the multi-stage AI chain, now with a final formatting stage."""
    raw_data_str = json.dumps(raw_alert_data, indent=2)
    
    # --- Stages 1, 2, 3: Data Processing and Narrative Generation ---
    st.info("Stage 1: Extracting Indicators of Compromise...")
    ioc_prompt = f"Analyze the following raw incident data. Extract all potential IOCs (IPs, domains, hashes, URLs, emails). Output as a clean list. Raw Data:\n{raw_data_str}"
    extracted_iocs = run_ai_stage(ioc_prompt)
    if not extracted_iocs: return "Report generation failed at Stage 1."

    st.info("Stage 2: Analyzing Business Impact...")
    impact_prompt = f"Given the following data, provide a brief 'Impact Assessment' and a 'Severity Rating' (Informational, Low, Medium, High, Critical). Data:\n{raw_data_str}\nIOCs:\n{extracted_iocs}"
    impact_analysis = run_ai_stage(impact_prompt)
    if not impact_analysis: return "Report generation failed at Stage 2."

    st.info("Stage 3: Generating Raw Report Narrative...")
    formatted_sections = "\n".join(f"- {section}" for section in required_sections)
    narrative_prompt = f"Write a formal incident report using ALL the information below. Use these sections ONLY:\n{formatted_sections}\n\n**Initial Data:**\n{raw_data_str}\n\n**Extracted IOCs:**\n{extracted_iocs}\n\n**Impact Analysis:**\n{impact_analysis}"
    messy_report = run_ai_stage(narrative_prompt)
    if not messy_report: return "Report generation failed at Stage 3."

    # --- NEW: Stage 4: Professional Formatting ---
    st.info("Stage 4: Formatting Report into Professional Template...")
    formatting_prompt = f"""
    You are a document formatting expert. Your task is to take the "Raw Report Text" below and reformat it EXACTLY into the following clean, professional structure.

    **TARGET FORMAT:**
    Date of Report: [Extract or use today's date]
    Category: [Extract from raw text, e.g., Malicious Activity, Phishing]
    Platform: [Extract from raw text, e.g., Orca Security]
    Severity: [Extract from raw text]
    Risk Rating: [Extract if available, otherwise omit]
    Asset Name: [Extract asset name from raw text]
    Verdict: [Extract from raw text, e.g., False Positive, True Positive]

    ## Orca Alert Details:
    [Place the general description of the alert here. Rewrite in a clean paragraph.]

    ## Analysis and Justification:
    [Place the detailed analysis and justification here. Use clean paragraphs and bullet points for key findings.]

    ## POC:
    [If screenshots or evidence are mentioned, list them here.]

    ---
    **Instructions:**
    - Extract the key-value data for the top section from the raw text.
    - Clean up the main text: remove excessive bolding (**), extra spaces, and rephrase for clarity.
    - Do NOT add any new information. Only reformat the existing content.

    **Raw Report Text to be Formatted:**
    {messy_report}

    Begin final formatted report now.
    """
    final_report = run_ai_stage(formatting_prompt)
    if not final_report: return "Report generation failed at Stage 4."

    st.success("All AI stages complete. Report polished.")
    return final_report