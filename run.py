"""
ClinicalTrial Match AI - Runner script
HealthTech & Bio-Innovation Hackathon
"""

import sys
import os

# Ensure backend package can be imported
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.app import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"==================================================")
    print(f"  ClinicalTrial Match AI - HealthTech Platform")
    print(f"  Live at: http://localhost:{port}")
    print(f"  Official API: https://clinicaltrials.gov/api/v2/studies")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
