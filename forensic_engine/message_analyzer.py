import re
import urllib.parse
from .ml_classifier import ScamMLClassifier

class MessageAnalyzer:
    def __init__(self, url_analyzer=None):
        self.url_analyzer = url_analyzer
        self.ml_classifier = ScamMLClassifier()

        # Targeted institutions & keywords (English, Hinglish & Hindi Devanagari)
        self.impersonation_targets = {
            "ELECTRICITY_BOARD": [
                "jvvnl", "avvnl", "jdvvnl", "electricity", "bijli", "power office", "power cut", 
                "disconnection", "bill overdue", "substation", "executive engineer", "sdow",
                "bijli kategi", "power supply", "बिजली", "विद्युत", "डिस्कनेक्शन", "बिल बकाया"
            ],
            "BANKING_FINANCE": [
                "sbi", "yono", "hdfc", "icici", "pnb", "axis", "bank", "kyc", "pan card", 
                "aadhar", "debit card", "credit card", "blocked", "suspended", "netbanking",
                "deactivated", "khata band", "खाता", "केवाईसी", "बैंक", "पैन कार्ड", "आधार"
            ],
            "POSTAL_COURIER": [
                "india post", "post office", "speed post", "courier", "parcel", "delivery failed", 
                "address update", "shipment", "पार्सल", "डाकघर"
            ],
            "PART_TIME_JOB_PONZI": [
                "part time job", "earn money", "daily income", "work from home", "telegram task", 
                "youtube like", "hotel review", "guaranteed profit", "investment double",
                "ghar baithe", "pese kamaye", "घर बैठे", "पैसे कमाए", "इनाम", "लॉटरी", "टास्क",
                "guaranteed returns", "guaranteed 3x", "daily return", "color prediction"
            ],
            "FAKE_LOAN": [
                "instant loan", "pre-approved loan", "zero interest loan", "fast credit", 
                "loan disbursement", "without cibil", "bad cibil loan", "cash loan",
                "लोन", "ऋण", "बिना सिबिल"
            ]
        }

        self.urgency_keywords = [
            "tonight", "today", "immediately", "urgent", "last warning", "within 2 hours",
            "within 24 hours", "power will be disconnected", "account will be blocked",
            "avoid disconnection", "final notice", "call now", "urgent basis", "penal action",
            "suspended", "blockage", "deactivated", "action required", "expiring",
            "turant", "aaj raat", "jaldi", "तुरंत", "आज रात", "अंतिम चेतावनी", "बंद कर दिया"
        ]

        # Protective advisory phrases used by genuine banks (R2 Negation Check)
        self.protective_phrases = [
            "never ask", "never share", "do not share", "don't share", "we never",
            "bank never", "does not ask", "share mat karo", "share mat karna",
            "kisi ko na bataye", "kisi se share na kare", "do not disclose", "stay alert"
        ]

        # Active credential solicitation regex (Fraudulent OTP harvest with negative lookbehind to avoid catching warnings)
        self.credential_theft_patterns = [
            re.compile(r'(?<!do not\s)(?<!never\s)(?<!don\'t\s)(?<!not\s)(?:share|send|provide|give|bhejo|batao|submit)\s+(?:the\s+|your\s+|apna\s+)?(?:otp|pin|password|cvv)', re.I),
            re.compile(r'otp\s*(?:bataye|batao|bhejo|share\s*karo|do|daalo|de\s*do|de\s*de|bata\s*do)', re.I),
            re.compile(r'otp\b.*?\b(?:de\s*do|de\s*de|bata\s*do|batao|bhejo|share\s*karo)', re.I),
            re.compile(r'(?:call|officer).*otp\s*(?:bataye|batao|bhejo|share|de\s*do)', re.I),
            re.compile(r'share\s+the\s+otp', re.I)
        ]

        # Indian phone regex
        self.phone_regex = re.compile(r'(?:(?:\+|00)91[\s.-]?)?(?:\(?0?[6789]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\b[6789]\d{9}\b)')
        
        # URL regex
        self.url_regex = re.compile(r'https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)')
        
        # UPI ID regex
        self.upi_regex = re.compile(r'[\w.-]+@(?:okaxis|okhdfcbank|oksbi|okicici|paytm|ybl|apl|ibl|axisbank|barodampay|freecharge|airtel|upi)\b', re.IGNORECASE)

    def analyze(self, text):
        extracted_phones = list(set([re.sub(r'[\s.-]', '', p) for p in self.phone_regex.findall(text)]))
        extracted_urls = list(set(self.url_regex.findall(text)))
        extracted_upis = list(set(self.upi_regex.findall(text)))

        text_lower = text.lower()
        reasons = []

        # ================= S1 FIX: INDEPENDENT SOLICITATION & PROTECTIVE ADVISORY CHECK =================
        # 1. Active solicitation check runs independently
        is_asking_otp = False
        for pat in self.credential_theft_patterns:
            if pat.search(text_lower):
                is_asking_otp = True
                break

        # 2. Protective phrases check
        is_protective_warning = any(phrase in text_lower for phrase in self.protective_phrases)

        # Active solicitation ALWAYS WINS over protective phrases (Disguised scam defense)
        if is_asking_otp:
            reasons.append("CRITICAL: Active solicitation of confidential OTP/PIN detected (Unauthorized harvest)")
        elif is_protective_warning:
            reasons.append("Protective advisory detected: Message warns recipient NOT to share credentials")

        # Delivery check: if message confirms successful delivery, it is benign (R6 Fix)
        is_delivered_notice = any(k in text_lower for k in ["has been delivered", "successfully delivered", "order has been delivered", "shipment delivered"])

        # ================= URGENCY SCORING =================
        urgency_matches = []
        if not is_delivered_notice:
            urgency_matches = [w for w in self.urgency_keywords if w in text_lower]
        urgency_score = min(100, len(urgency_matches) * 35)

        # ================= IMPERSONATION SCORING =================
        detected_categories = []
        impersonation_score = 0
        for category, keywords in self.impersonation_targets.items():
            matched = [k for k in keywords if k in text_lower]
            if matched:
                detected_categories.append({"category": category, "keywords": matched})
                impersonation_score += 45

        # Standalone Ponzi / Guaranteed returns regex (R6 Fix)
        ponzi_match = re.search(r'guaranteed\s+(?:\d+x|\d+%|\d+)?\s*(?:returns?|profit|income|paisa)', text_lower)
        if ponzi_match:
            impersonation_score += 50
            if not any(c["category"] == "PART_TIME_JOB_PONZI" for c in detected_categories):
                detected_categories.append({"category": "PART_TIME_JOB_PONZI", "keywords": [ponzi_match.group(0)]})
            reasons.append(f"Unrealistic financial inducement: '{ponzi_match.group(0)}'")

        impersonation_score = min(100, impersonation_score)

        if urgency_matches:
            reasons.append(f"High-pressure psychological urgency levers: '{', '.join(urgency_matches[:3])}'")
        if detected_categories:
            cats = [c["category"].replace('_', ' ') for c in detected_categories]
            reasons.append(f"Impersonation indicators targeting: {', '.join(cats)}")
        if extracted_urls:
            reasons.append(f"Unverified hyperlinks found ({len(extracted_urls)} link(s))")
        if extracted_phones:
            reasons.append(f"Suspicious callback contact numbers extracted ({len(extracted_phones)} phone(s))")
        if extracted_upis:
            reasons.append(f"Beneficiary payment handle requested: {', '.join(extracted_upis)}")

        # ================= URL CROSS-EVALUATION =================
        url_risk_boost = 0
        if self.url_analyzer and extracted_urls:
            for u in extracted_urls:
                u_res = self.url_analyzer.analyze(u)
                if u_res.get('risk_level') == 'HIGH':
                    url_risk_boost = max(url_risk_boost, 45)
                    reasons.append(f"Embedded URL flagged as HIGH RISK: {u_res.get('domain')} ({u_res.get('summary')})")
                elif u_res.get('risk_level') == 'MEDIUM':
                    url_risk_boost = max(url_risk_boost, 25)

        # ================= ML MODEL PREDICTION =================
        ml_res = self.ml_classifier.predict(text)
        ml_prob = ml_res["scam_probability"]

        if ml_prob >= 0.70:
            reasons.append(f"AI Machine Learning Model: Flagged as Scam with {round(ml_prob * 100)}% confidence")
        elif ml_prob <= 0.25:
            reasons.append(f"AI Machine Learning Model: Matches benign communication profile ({round((1 - ml_prob) * 100)}% genuine)")

        # ================= COMBINED SCORE =================
        rule_score = (urgency_score * 0.35) + (impersonation_score * 0.35)
        
        if extracted_urls:
            rule_score += 15
        if extracted_phones:
            rule_score += 10
        if extracted_upis:
            rule_score += 15
        if is_asking_otp:
            rule_score += 45
        if url_risk_boost:
            rule_score += url_risk_boost

        # If protective advisory detected without phishing links or suspicious phones -> strong benign bonus
        if is_protective_warning and not extracted_urls and not url_risk_boost and not is_asking_otp:
            rule_score = max(0, rule_score - 40)
            ml_prob = min(ml_prob, 0.15)

        if is_delivered_notice and not extracted_urls and not is_asking_otp:
            rule_score = max(0, rule_score - 30)
            ml_prob = min(ml_prob, 0.15)

        rule_score = min(100, rule_score)

        # Hybrid Score: 60% Rule/Forensics + 40% ML Probability
        total_risk_score = round((rule_score * 0.60) + ((ml_prob * 100) * 0.40))
        
        # Override rules (Active OTP solicitation or Ponzi ALWAYS WINS)
        if is_asking_otp or (impersonation_score >= 45 and urgency_score >= 35) or url_risk_boost >= 40 or ponzi_match:
            total_risk_score = max(total_risk_score, 75)

        # Absolute clamp for protective advisories / genuine delivered alerts without URLs
        if (is_protective_warning or is_delivered_notice) and not extracted_urls and not is_asking_otp:
            total_risk_score = min(total_risk_score, 25)

        # Classification
        if total_risk_score >= 60:
            risk_level = "HIGH"
            threat_type = detected_categories[0]["category"] if detected_categories else "PHISHING_ATTEMPT"
        elif total_risk_score >= 30:
            risk_level = "MEDIUM"
            threat_type = detected_categories[0]["category"] if detected_categories else "SUSPICIOUS_COMMUNICATION"
        else:
            risk_level = "LOW"
            threat_type = "BENIGN_OR_LOW_RISK"
            if not reasons:
                reasons.append("Standard communication patterns; no malicious indicators identified.")

        return {
            "risk_level": risk_level,
            "risk_score": total_risk_score,
            "threat_type": threat_type,
            "urgency_score": urgency_score,
            "impersonation_score": impersonation_score,
            "ml_prediction": ml_res,
            "extracted_identifiers": {
                "phones": extracted_phones,
                "urls": extracted_urls,
                "upi_ids": extracted_upis
            },
            "reasons": reasons,
            "summary": f"{risk_level} Risk: Identified as {threat_type.replace('_', ' ').title()} (Rule: {round(rule_score)}/100, ML: {round(ml_prob * 100)}%)."
        }
