# report_generator.py (V3.2 - The Intelligent Analyst)

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import streamlit as st
from datetime import datetime

# --- API Key Configuration ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
    except (KeyError, FileNotFoundError):
        st.error("GEMINI_API_KEY not found.")
        st.stop()
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Failed to configure Gemini API: {e}")
    st.stop()

# --- MODEL UPGRADE: Using the more powerful Pro model for better reasoning ---
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def run_ai_stage(prompt):
    """A helper function to run a single AI stage."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An AI stage failed: {e}")
        return None

def generate_orca_report(report_data: dict) -> str:
    """
    Runs an advanced "Two-Pass" AI chain to generate a high-quality, bespoke report.
    """
    alert_name = report_data.get("alert_name", "Unknown Alert")
    verdict = report_data.get("verdict", "False Positive")
    
    # --- Pass 1: The "Template Generator" ---
    st.info(f"Step 1: Designing a bespoke report template for '{alert_name}'...")
    template_generation_prompt = f"""
    You are an expert cybersecurity report designer specializing in Orca Security.
    Your task is to generate a professional Markdown report template for the following Orca alert: "{alert_name}".
    
    The final report will be for a verdict of: **{verdict}**.
    
    Based on the alert name and verdict, create the ideal report structure.
    - Start with a key-value pair section at the top (Report Date, Category, Severity, etc.).
    - For a False Positive, include a detailed "Analysis and Justification for False Positive" section.
    - For a True Positive, include detailed "Impact" and "Remediation" sections.
    - Include sections like "Alert Details" and "POC".
    - Use clear Markdown headings (e.g., `## Section Title`).
    - Use placeholders like `[Analyst to provide details on...]` in the main sections to guide the final writing stage.

    Generate the Markdown template now.
    """
    bespoke_template = run_ai_stage(template_generation_prompt)
    if not bespoke_template: return "Report generation failed at Template Generation stage."

    # --- Pass 2: The "Report Writer" ---
    st.info("Step 2: Writing the report using the custom template...")
    report_writing_prompt = f"""
    You are a Senior Security Analyst. Your task is to write a final, professional report by filling in the provided "Bespoke Report Template".
    
    Use the "Analyst's Raw Data" to populate the template. Your writing must be clear, concise, and professional.
    - Fill in all key-value pairs at the top using the provided data.
    - Use the "Analyst's Notes" to write the main narrative sections of the report, replacing the placeholders.
    - If a piece of information isn't available in the raw data, write "Not Applicable" or "N/A".
    - Do not deviate from the structure of the bespoke template.
    - Today's date is {datetime.now().strftime('%d %B, %Y')}.

    **Bespoke Report Template:**
    ```markdown
    {bespoke_template}
    ```

    **Analyst's Raw Data (JSON):**
    ```json
    {json.dumps(report_data, indent=2)}
    ```

    Generate the final, populated report now.
    """
    final_report = run_ai_stage(report_writing_prompt)
    if not final_report: return "Report generation failed at the Report Writing stage."
    
    st.success("AI analysis complete. Report finalized.")
    return final_report