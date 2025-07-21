# report_generator.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

# --- Configuration ---
# Load environment variables from .env file (for the API key)
load_dotenv()

# Securely configure the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")
genai.configure(api_key=api_key)


# --- The Core Dynamic Function ---

def generate_dynamic_report(raw_alert_data: dict, required_sections: list) -> str:
    """
    Generates a dynamic cybersecurity incident report using Gemini Pro.

    This function is designed to be highly flexible:
    - It takes raw alert data as a Python dictionary, allowing for any type of alert.
    - It takes a list of required sections, allowing the user to define the report structure.

    Args:
        raw_alert_data (dict): A dictionary containing all the raw data, notes, and IOCs
                               related to the security incident.
        required_sections (list): A list of strings, where each string is a required
                                  section header for the final report.

    Returns:
        str: The generated report in Markdown format, or an error message.
    """
    # Convert the Python dictionary of alert data into a clean, readable string format for the prompt.
    # JSON format is excellent for this.
    formatted_alert_data = json.dumps(raw_alert_data, indent=4)

    # Convert the list of required sections into a numbered list for the prompt.
    formatted_sections = "\n".join(f"{i+1}. {section}" for i, section in enumerate(required_sections))

    # --- The New, Dynamic Master Prompt ---
    # This prompt is the "brain" of our operation. It instructs Gemini on how to behave
    # and what to do with the dynamic data we provide.
    master_prompt = f"""
    **Role and Goal:**
    You are a world-class Tier 3 Cybersecurity Analyst and technical writer. Your primary task is to synthesize raw, unstructured incident data into a formal, professional, and clear incident report suitable for both technical teams and management.

    **Instructions:**
    1.  Carefully analyze the provided "Raw Incident Data" in JSON format. This data contains everything known about the incident.
    2.  You MUST generate a report that includes the following sections ONLY, and they must appear in this EXACT order:
        {formatted_sections}
    3.  For each section, synthesize the relevant information from the raw data. If data for a section is not provided, state "No data available for this section."
    4.  The tone must be authoritative, objective, and precise. Use clear headings with Markdown (`## Section Title`).
    5.  Do not add any sections that were not explicitly requested. Do not include any introductory or concluding remarks outside of the requested sections.

    **Raw Incident Data (JSON):**
    ```json
    {formatted_alert_data}
    ```

    **Begin Report Generation:**
    """

    try:
        # Initialize the Gemini Pro model
        model = genai.GenerativeModel('gemini-pro')

        # Send the prompt to the model
        response = model.generate_content(master_prompt)

        # Return the generated text
        return response.text

    except Exception as e:
        # Handle potential errors during the API call
        error_message = f"An error occurred while generating the report: {e}"
        print(error_message)
        return error_message