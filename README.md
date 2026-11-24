# SurakshaKavach AI (सुरक्षा कवच)
### Rajasthan Police Academy (RPA) - R4C Cyber Security Hackathon 2026
**Problem Statement PS01:** Scam Message & Phishing Link Detection with Fake Loan / Investment App and Fraudulent Website Analysis

---

## 📌 Project Overview
**SurakshaKavach AI** is a police-grade, unified cyber threat triage and intelligence platform built for Rajasthan Police Cyber Crime Cell. It analyzes suspicious SMS, WhatsApp forwards, phishing URLs, malicious Android APKs, and fraudulent Ponzi/betting websites.

### 🌟 Key Capabilities
- **SMS & Message Urgency Scorer:** Classifies urgency pressure cues and impersonation of Rajasthan utilities (JVVNL/AVVNL) or banks (SBI/PNB).
- **Phishing URL Inspector:** Detects typosquatting, look-alike domains, high-risk TLDs (.xyz, .top), and blacklisted IOCs.
- **Static Android APK Decompiler:** Detects predatory loan spyware profiles (`READ_CONTACTS` + `READ_SMS` + `CAMERA`) and extracts embedded C2 URLs and phone numbers without needing a sandbox.
- **APK samples:** Executable demo APKs are intentionally excluded from this public repository. Upload an APK you are authorized to analyze.
- **Ponzi & Betting Scanner:** Linguistic detection of MLM bonus hierarchies, guaranteed daily returns, and illegal color prediction platforms (Daman Games).
- **Threat Heat-List & Case Registry:** Inverted index linking recurrent phones, UPI IDs, and domains across isolated complaints to uncover organized syndicates.
- **Section 65B Indian Evidence Act Forensic PDF Export:** Automated one-click court-admissible dossiers with SHA-256 cryptographic hashes and pre-drafted Section 91 CrPC notices.

---

## 🚀 Quick Setup & Execution

### 1. Requirements
- Python 3.9+
- Dependencies installed via `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python3 app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📁 Repository Structure
```
HACKTHON/
├── app.py                                # Flask web application & REST APIs
├── forensic_engine/                      # Core intelligence engines
│   ├── message_analyzer.py               # SMS & WhatsApp NLP urgency/impersonation scorer
│   ├── url_analyzer.py                   # Domain typosquatting & blacklist inspector
│   ├── apk_analyzer.py                   # Static Android APK Manifest & DEX extractor
│   ├── website_analyzer.py               # Ponzi, MLM & Betting scraper
│   ├── correlation_engine.py             # Cross-case entity linking & heat-list
│   └── report_generator.py               # Section 65B certified ReportLab PDF generator
├── templates/
│   └── index.html                        # Cyber Police Command Dashboard UI
├── ACTION_PLAN_SUBMISSION.md             # Official Action Plan document for hackathon portal
├── SURAKSHAKAVACH_ACTION_PLAN_RPA_2026.pdf # Ready-to-upload Action Plan PDF
├── PRESENTATION_CHEATSHEET.md            # Viva questions, answers, and demo walkthrough
└── requirements.txt                      # Dependencies
```

---

## ⚖️ Statutory Alignment
- **Section 65B, Indian Evidence Act / Section 63, Bharatiya Sakshya Adhiniyam (BSA 2023):** Electronic record certificate generation.
- **Section 66D, Information Technology Act, 2000:** Punishment for cheating by personation by using computer resource.
- **Section 91 CrPC / Section 94 BNSS:** Automated requisition drafting for Telecom & Intermediary records.
