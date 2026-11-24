# VIVA & PRESENTATION CHEAT-SHEET FOR BHARAT
## Rajasthan Police Academy (RPA) - R4C Cyber Security Hackathon 2026
### Project: SurakshaKavach AI (सुरक्षा कवच) | Problem Statement: PS01

Bhai, is updated sheet ko dhyan se padh lo. Saare code bugs fix ho chuke hain aur 16/16 acceptance tests pass ho chuke hain. Judges jo bhi technical sawal poochenge, unka sach aur verified answer yahan hai!

---

### 1. Elevator Pitch (30 Seconds me Project Explain Kaise Karein)
> *"Jai Hind Sir / Good morning judges. Hamara project hai **SurakshaKavach AI** jo Rajasthan me badhte cyber fraud—jaise **JVVNL Bijli Disconnection Scam**, **Chinese Predatory Loan Apps**, aur **SBI YONO KYC Phishing**—ko rokne ke liye banaya gaya hai.*  
> *Jab bhi kisi citizen ya police officer ko suspicious SMS, link, APK ya betting website milti hai, hamara system instantly usko statically analyze karta hai, **Hybrid Explainable AI + ML Model** se risk score deta hai, suspect ke **Phone number, UPI ID aur C2 URLs** extract karta hai, aur police ke liye 1-click me **Section 63 Bharatiya Sakshya Adhiniyam (BSA 2023) / Section 65B certified Electronic Evidence Dossier** generate karta hai."*

---

### 2. Top Expected Questions & Ready-Made Answers

#### Q1: "Aapka tool AI use kar raha hai ya sirf Rule-based / Regex hai?"
**Ans:** 
*"Sir, hamara system **Hybrid Explainable Architecture** follow karta hai:  
1. **Rule & Heuristics Layer:** Psychological urgency keywords ('tonight at 9:30 PM'), utility impersonation (JVVNL, SBI), typosquatting, aur predatory permission analysis.  
2. **Machine Learning Layer:** Humne `scikit-learn` me TF-IDF Vectorizer + Logistic Regression model integrate kiya hai jo Hindi, Hinglish aur English text messages par trained hai.  
Result card me dono ka weighted confidence score dikhta hai (e.g. Rule: 85/100, ML: 91%), jisse black-box hone ka ilzam nahi lagta aur court me explainable reasons milte hain."*

---

#### Q2: "APK ko bina run kiye (bina sandbox) kaise analyze kar rahe ho?"
**Ans:** 
*"Sir, PS01 ke scope ke according dynamic analysis out-of-scope tha. Hum **Static Forensic Decompilation** perform karte hain (`androguard` library ke sath):*
1. **The Extortion Triad:** Agar koi instant loan app `READ_CONTACTS` + `READ_SMS` + `CAMERA` mang rahi hai, toh ye clear predatory extortion spyware profile hai jo victim ki contact list chura kar parivar ko blackmail karti hai.
2. **Binary Bytecode Parsing:** DEX bytecode aur string pool se hardcoded Command & Control (C2) callback URLs, recovery agent ke phone numbers, aur repayment UPI IDs extract ho jate hain — bina malware ko phone me run kiye!"*

---

#### Q3: "Syndicate Correlation Engine ka kya faayda hai police ke liye?"
**Ans:** 
*"Sir, cyber criminal gangs (Mewat, Jamtara, Alwar) alag-alag scams run karte hain lekin backend infrastructure same use karte hain.  
Jab hum koi SMS, APK ya Website scan karte hain, hamara database unke phone numbers, UPIs aur domains ko inverted index me store karta hai.  
**Example:** Jo phone number `9829012345` JVVNL ke fake electricity SMS me mila tha, wahi number CashSpeed loan app ke APK me bhi recovery contact ke taur pe nikla. System ne turant dono cases ko cross-link kar diya aur trending heat-list me alert daal diya."*

---

#### Q4: "Official websites (sbi.co.in, uidai.gov.in) ko aapka system scam toh nahi bolta?"
**Ans:** 
*"Sir, bilkul nahi! Hamare paas ek comprehensive **Official Brand & Gov Whitelist** hai. Sabhi `.gov.in` aur `.nic.in` domains (jaise `uidai.gov.in`, `incometax.gov.in`), aur verified bank domains (jaise `sbi.co.in`, `onlinesbi.sbi`, `axisbank.com`, `pnbindia.in`) turant verified LOW risk (score 0) classify hote hain. Typosquatting tabhi flag hoti hai jab domain unverified ho (jaise `sbi-kyc-quickupdate.xyz`)."*

---

#### Q5: "Police Evidence Report me Section 63 BSA ka kya role hai?"
**Ans:** 
*"Sir, naye criminal laws ke tehat **Section 63 of Bharatiya Sakshya Adhiniyam (BSA 2023)** (purana Section 65B Indian Evidence Act) electronic records ki court admissibility govern karta hai. Hamari PDF report me:  
- Pure evidence ka **SHA-256 cryptographic hash** hota hai.  
- Extracted IOCs (Phone, UPI, C2 endpoints) ki forensic table hoti hai.  
- Nodal telecom officers aur banks ke liye **Section 91 CrPC / Section 94 BNSS** ka notice draft pre-written hota hai."*

---

### 3. Live Demo Steps (2-Minute Walkthrough)
1. Terminal me run karo: `python3 app.py`
2. Browser me kholo: `http://127.0.0.1:5000`
3. **SMS Scanner:** Click karo **"⚡ JVVNL Electricity Bill Scam"** preset -> Click **"Run Forensic Triaging"** -> Dikhao ki **HIGH RISK (88/100)** aaya, Urgency detect hui, Phone & URL extract hue, aur ML Model ne bhi scam flag kiya!
4. **Hindi SMS Test:** Click karo **"🇮🇳 Hindi: बिजली बिल डिस्कनेक्शन"** -> Dikhao ki Hindi Devanagari message par bhi **HIGH RISK (70/100)** aaya!
5. **URL Inspector:** Click karo **"sbi-kyc-quickupdate.xyz"** -> HIGH 100 Phishing detect hui! Phir click karo **"sbi.co.in"** -> Verified Official LOW (Score 0) aaya!
6. **APK Analyzer:** Click karo **"🚨 CashSpeed Loan Spyware APK"** -> Contacts + SMS + Camera extortion profile aur C2 endpoints dikhao!
7. **Syndicate & Heatlist:** Investigation Dossier tab me jao -> Case row par click karo -> Modal open hoga jisme dikhega ki SMS aur APK case **same phone number `9829012345`** se linked hain!
8. **PDF Export:** **"📄 PDF"** button par click karo -> Section 63 BSA certified official dossier download ho jayega!
