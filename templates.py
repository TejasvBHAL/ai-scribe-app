# templates.py

REPORT_TEMPLATES = {
    "Default Generic Report": {
        "description": "A standard template for general-purpose incident reports.",
        "sections": [
            "Executive Summary",
            "Detailed Findings",
            "Indicators of Compromise (IOCs)",
            "Recommended Remediation Plan"
        ]
    },
    "Phishing Email Analysis": {
        "description": "A specific template for analyzing and reporting on phishing attempts.",
        "sections": [
            "Executive Summary",
            "Email Header & Payload Analysis",
            "Analysis of Malicious Link/Attachment",
            "User Actions and Containment",
            "Indicators of Compromise (IOCs)",
            "Remediation and User Education"
        ]
    },
    "Cloud Security Misconfiguration": {
        "description": "For reporting security issues found in cloud environments (AWS, Azure, GCP).",
        "sections": [
            "Vulnerability Summary",
            "Affected Resource Details (ID, Region, etc.)",
            "Description of Misconfiguration",
            "Potential Business Impact",
            "Step-by-Step Remediation Guide"
        ]
    }
}