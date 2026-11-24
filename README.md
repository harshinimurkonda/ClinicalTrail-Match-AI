# ClinicalTrial Match AI 🧬

> **HealthTech & Bio-Innovation Hackathon Project**  
> An explainable clinical trial discovery platform connecting patients and caregivers to real-world clinical trials using live **ClinicalTrials.gov API v2** data and transparent AI-assisted plain-language translations.

---

## 🌟 Key Highlights

- **Live Official Data:** Queries the official ClinicalTrials.gov API v2 (`https://clinicaltrials.gov/api/v2/studies`). Never fakes results.
- **Privacy-First Architecture:** Collects zero Personally Identifiable Information (PII). No names, emails, phone numbers, or social security numbers.
- **Explainable Criteria Alignment:** Evaluates age limits, biological sex restrictions, condition focus, and location accessibility using clear status labels:
  - 🟢 **Supported** (Verifiable criteria align with patient profile)
  - 🟡 **Unknown** (Requires doctor review, missing lab/biomarker data)
  - 🔴 **Potential Conflict** (Administrative criteria mismatch detected)
- **Ethical Healthcare Design:** Explicitly states that criteria alignment is **never** an eligibility probability. Only the clinical investigator team can confirm eligibility.
- **AI-Powered Plain-Language Navigator:**
  - Simplifies dense inclusion & exclusion criteria into layperson terms.
  - Generates a **Missing Information Checklist** (e.g., genetic biomarkers, disease stage, ECOG performance status, kidney/liver blood panels).
  - Generates **Questions to Ask the Study Coordinator or Physician**.
  - **Dual Engine:** Out-of-the-box deterministic Clinical NLP parser (zero keys required) + optional Google Gemini generative synthesis.
- **Watchlist & Doctor Consultation Export:**
  - Save trials to browser `localStorage`.
  - Print/export a formatted **Doctor Discussion Summary** ready to bring to an appointment.

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.10+ installed
- Active internet connection (to reach `clinicaltrials.gov`)

### 2. Installation
Navigate to the project root directory:
```bash
cd "C:\Users\HARSHINI\.gemini\antigravity\scratch\clinical-trial-match-ai"
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Optional: Configure Google Gemini API (Server-Side)
The application includes a built-in deterministic Clinical NLP parser that works **100% out-of-the-box with zero API keys**.

If you wish to enable Google Gemini generative AI synthesis:
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Add your Gemini API key in `.env`:
   ```ini
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
*(Note: Your API key is strictly kept on the backend server and is never exposed to the frontend).*

### 4. Run the Application
```bash
python run.py
```
Open your web browser at:
👉 **`http://localhost:5000`**

---

## 🧪 Testing and Verification

Run the automated end-to-end verification suite:
```bash
python test_app.py
```
This tests:
1. Age parsing logic across different units (years, months, days).
2. Live connection to the ClinicalTrials.gov API v2.
3. Criteria matching and conflict detection.
4. Plain-language AI summary and question generation.
5. REST API endpoints (`/api/health`, `/api/search`, `/api/study/<nct_id>`, `/api/explain`).

---

## 📐 Architecture & Endpoints

```
clinical-trial-match-ai/
├── backend/
│   ├── app.py            # Flask REST API & Web Server
│   ├── clinical_api.py   # ClinicalTrials.gov API v2 Client & Parser
│   ├── matcher.py        # Explainable Criteria Matching Engine
│   └── explainer.py      # Dual-mode AI Plain-Language Explainer (NLP + Gemini)
├── static/
│   ├── css/
│   │   └── styles.css    # Healthcare design system (Navy #0a1128, Teal #0d9488)
│   └── js/
│       └── app.js        # Responsive UI controller, localStorage, print export
├── templates/
│   └── index.html        # Main application layout
├── run.py                # Server runner
├── test_app.py           # Automated test suite
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

### REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service health status and AI engine indicator |
| `POST` | `/api/search` | Search ClinicalTrials.gov with patient profile & matching |
| `GET` | `/api/study/<nct_id>` | Fetch full study protocol by NCT identifier |
| `POST` | `/api/explain` | Generate plain-language summary & questions |
| `GET` | `/api/config-status` | Report Gemini configuration status |

---

## 🛡️ Responsible Use Disclaimer

**ClinicalTrial Match AI is an educational exploration tool.** It does not provide medical advice, diagnose medical conditions, or determine official clinical trial eligibility. A label of **Supported** only indicates administrative alignment with public trial criteria (age, sex, location, and condition). Only the designated clinical trial physician and research team can determine participant qualification. Always consult your qualified healthcare provider.
