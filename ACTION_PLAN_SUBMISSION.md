# CYBER SECURITY HACKATHON 2026 — RAJASTHAN POLICE ACADEMY (RPA), JAIPUR
## OFFICIAL ACTION PLAN SUBMISSION
### Team Name: Rakshak
### Problem Statement: PS01 — Cyber Fraud / Phishing / Malicious Apps
**Title:** Scam Message & Phishing Link Detection with Fake Loan / Investment App and Fraudulent Website Analysis  
**Project Name:** **SurakshaKavach AI (सुरक्षा कवच)** — Unified Threat Triage & Forensic Intelligence Platform  
**Target Agency:** Rajasthan Police Cyber Crime Cell / R4C / I4C  

---

## 1. Executive Summary & Problem Context
Across Rajasthan and northern India, citizens are bombarded daily with fraudulent SMS, WhatsApp lures, and malicious APK links targeting their hard-earned money. These attacks cluster into four distinct syndicates:
1. **Electricity Bill Disconnection Scams:** Impersonating state discoms (JVVNL, AVVNL, JDVVNL) threatening power cuts "tonight at 9:30 PM".
2. **Predatory Instant Loan App Extortion:** Apps sideloaded via malicious links that harvest victim contacts, SMS OTPs, and photos for vicious blackmail.
3. **Banking KYC Suspensions:** Fake SMS alerts spoofing SBI YONO, PNB, or HDFC claiming netbanking suspension.
4. **Ponzi, Part-Time Telegram Task & Illegal Betting Rackets:** Platforms like Daman Games or high-yield investment sites luring users with "guaranteed daily 10% returns" and siphoning deposits through mule UPI accounts.

**The Investigative Bottleneck:** Currently, these complaints arrive separately at police stations and portals (1930 NCRP). Fraudsters exploit this fragmentation by recycling the exact same phone numbers, mule UPI IDs, and C2 hosting servers across different scams.

**Our Solution:** **SurakshaKavach AI** is a unified cyber threat triage and investigation platform. It provides instant, explainable risk scoring on messages, URLs, Android APKs, and websites, automatically harvests actionable Indicators of Compromise (IOCs), correlates recurring entities across isolated cases, and generates Section 65B certified forensic investigation dossiers for police officers.

---

## 2. Key Modules & Technical Architecture

```
   [Citizen / Police Officer Input]
    ├── Suspicious SMS / WhatsApp Text
    ├── Phishing Link / Domain URL
    ├── Android APK Binary (.apk)
    └── Ponzi / Betting Website URL or HTML
                     │
                     ▼
       ┌───────────────────────────┐
       │   SURAKSHAKAVACH AI CORE  │
       └─────────────┬─────────────┘
                     │
      ┌──────────────┼──────────────┬──────────────┐
      ▼              ▼              ▼              ▼
[NLP Urgency &   [Domain & TLD  [Static APK    [Linguistic MLM &
 Impersonation   Typosquatting   DEX/Manifest   Betting Parser &
 Scorer]         Inspector]      Harvester]     Payment Scraper]
      │              │              │              │
      └──────────────┼──────────────┴──────────────┘
                     ▼
      ┌───────────────────────────┐
      │  EXPLAINABLE RISK ENGINE  │ (Low / Medium / High + Forensic Bullets)
      └──────────────┬────────────┘
                     │
      ┌──────────────┴────────────┐
      ▼                           ▼
[Entity Correlation Graph   [Automated Section 65B
 & Trending Threat Heat-List] Police Evidence Dossier (PDF)]
```

### Module 1: Message & Phishing Inspector
- **Context-Aware NLP Scoring:** Evaluates urgency pressure tactics ("tonight", "urgent basis", "within 2 hours") and targets of impersonation (JVVNL, SBI, India Post).
- **Automated Entity Extraction:** Regex parsers extract unverified Indian phone numbers (+91), unshortened hyperlinks, and suspect UPI handles.

### Module 2: Phishing URL & Domain Inspector
- **Brand Spoofing & Look-alike Detection:** Identifies deceptive subdomains and typosquatting (e.g., `sbi-kyc-update.xyz`, `jvvnl-bill-clear.online`).
- **Disposable Infrastructure Flags:** Flags cheap, throwaway TLDs (`.xyz`, `.top`, `.cc`, `.buzz`), unencrypted HTTP connections, and raw direct IP hosts (`http://103.22.x.x`).
- **Blacklist Corroboration:** Cross-checks domains against known CERT-In and I4C cyber syndicate IOC databases.

### Module 3: Static Android APK Extortion Engine
- **Safe Static Non-Detonation:** Safely parses `AndroidManifest.xml` and `classes.dex` without executing dangerous code in a sandbox.
- **Predatory Loan App Signature:** Flags the lethal extortion profile: `READ_CONTACTS` + `READ_SMS` + `CAMERA` + `REQUEST_INSTALL_PACKAGES`.
- **Hardcoded Identifier Extraction:** Scrapes hardcoded Command & Control (C2) callback URLs, recovery agent phone numbers, and repayment UPI IDs directly from decompiled string pools.

### Module 4: Fraudulent Website & Ponzi Scanner
- **Ponzi / MLM Classifier:** Flags guaranteed returns ("daily 10% profit", "double money"), pyramid referral hierarchies, and illegal betting triggers (color prediction, Daman Games, Aviator).
- **Financial Destination Miner:** Automatically extracts recipient UPI addresses, Indian Bank Account Numbers with IFSC codes, and TRC-20 USDT crypto wallet addresses.

### Module 5: Cross-Case Syndicate Correlation & Threat Heat-List
- **Entity Resolution Graph:** Links phone numbers, UPIs, and domains across unrelated complaints to reveal criminal networks recycling infrastructure.
- **Dynamic Threat Heat-List:** Maintains a real-time leaderboard of the most active scam phone numbers, domains, and payment handles for batch blocking.

### Module 6: Court-Admissible Forensic Dossier (Section 65B PDF Generator)
- **Legal Compliance:** Generates official investigation reports conforming to Section 65B of the Indian Evidence Act / Section 63 of Bharatiya Sakshya Adhiniyam (BSA 2023).
- **Cryptographic Integrity:** Includes SHA-256 package checksums, timestamp tracking, extracted IOC tables, and pre-drafted legal notices under Section 91 CrPC / Section 94 BNSS.

---

## 3. Uniqueness & Competitive Edge
1. **Zero False Positives & Explainable AI:** No opaque "black-box" predictions. Every finding is backed by plain-English evidence bullets admissible during judicial trial.
2. **True Unified Triaging:** Links an SMS to an APK and a website through common backend infrastructure.
3. **Optimized for Field Officers:** Generates ready-to-serve Section 91 CrPC telecom notices and 1930 NCRP freeze requests with a single click.
4. **Lightweight & High Performance:** Runs statically without expensive cloud sandbox GPUs, enabling instant responses on police station laptops and citizen smartphones.

---

## 4. 24-Hour Final Hackathon Roadmap at RPA, Jaipur
- **Hours 01 – 04:** Ingest R4C sample datasets (real scam SMS, test APKs, fraudulent URLs); calibrate detection thresholds to ground-truth data.
- **Hours 05 – 10:** Enhance multi-layer entity graph visualization (Vis.js / NetworkX) displaying live links between suspects.
- **Hours 11 – 16:** Deploy a citizen reporting portal / Telegram bot for real-time scam verification before opening links.
- **Hours 17 – 20:** Rigorous testing against obfuscated APKs and Hinglish/Rajasthani scam messages.
- **Hours 21 – 24:** Polish UI dashboard, verify Section 65B PDF dossiers, and deliver final jury demonstration.

---

## 5. Technology Stack
- **Backend Forensics:** Python 3, Flask, BeautifulSoup4, TLDExtract, ZipFile Binary Parsers.
- **Report Engine:** ReportLab Forensic PDF Generation (Section 65B / BSA 63 compliant).
- **Database:** SQLite relational entity graph with inverted IOC indices.
- **Frontend Dashboard:** Responsive Cyber Police Command UI (Tailwind CSS, FontAwesome, Chart.js).
