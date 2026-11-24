import re
import urllib.parse
from bs4 import BeautifulSoup

class WebsiteAnalyzer:
    def __init__(self):
        # MLM, Ponzi, and Guaranteed Return Fraud Triggers
        self.ponzi_triggers = [
            "guaranteed return", "daily income", "100% profit", "double your money",
            "daily 5%", "daily 10%", "daily profit", "referral bonus", "direct bonus",
            "level income", "downline bonus", "team commission", "vip tier", "task reward",
            "recharge bonus", "matrix plan", "risk free investment", "passive income stream"
        ]

        # Illegal Betting & Color Prediction Platform Triggers
        self.betting_triggers = [
            "color prediction", "aviator", "dragon vs tiger", "teen patti", "win big cash",
            "fast withdrawal", "instant cashout", "recharge now to play", "betting platform",
            "daman games", "91club", "winzo hack", "lottery spin", "lucky draw cash"
        ]

        # Fake KYC / Phishing Triggers
        self.phishing_triggers = [
            "enter your atm pin", "enter cvv", "verify netbanking password", "submit otp",
            "update aadhar", "link pan with bank", "account deactivation warning", "download remote app"
        ]

        # Regex for extractable identifiers
        self.upi_regex = re.compile(r'[\w.-]+@(?:okaxis|okhdfcbank|oksbi|okicici|paytm|ybl|apl|ibl|axisbank|barodampay|freecharge|airtel|upi)\b', re.IGNORECASE)
        self.phone_regex = re.compile(r'(?:(?:\+|00)91[\s.-]?)?(?:\(?0?[6789]\d{2}\)?[\s.-]?\d{3}[\s.-]?\d{4}|\b[6789]\d{9}\b)')
        self.ifsc_regex = re.compile(r'\b[A-Z]{4}0[A-Z0-9]{6}\b')
        self.account_regex = re.compile(r'(?:A/c|Account\s*(?:No|Number)?|Acc)[\s.:#]*([0-9]{9,18})', re.IGNORECASE)
        self.crypto_trc20_regex = re.compile(r'\bT[A-Za-z1-9]{33}\b') # USDT TRON address
        self.crypto_eth_regex = re.compile(r'\b0x[a-fA-F0-9]{40}\b') # ETH / BSC address

    def analyze(self, content_or_html, source_url=""):
        # Strip HTML tags if HTML is provided
        soup = BeautifulSoup(content_or_html, 'html.parser')
        text = soup.get_text(separator=' ')
        text_lower = text.lower()

        # Extract financial identifiers
        extracted_upis = list(set(self.upi_regex.findall(text)))
        extracted_phones = list(set([re.sub(r'[\s.-]', '', p) for p in self.phone_regex.findall(text)]))
        extracted_ifscs = list(set(self.ifsc_regex.findall(text)))
        extracted_accounts = list(set(self.account_regex.findall(text)))
        extracted_trc20 = list(set(self.crypto_trc20_regex.findall(text)))
        extracted_eth = list(set(self.crypto_eth_regex.findall(text)))

        # Also search in href attributes (e.g., wa.me links, mailto)
        whatsapp_links = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'wa.me' in href or 'api.whatsapp.com' in href or 't.me' in href:
                whatsapp_links.append(href)

        # Matched categories
        ponzi_matches = [w for w in self.ponzi_triggers if w in text_lower]
        betting_matches = [w for w in self.betting_triggers if w in text_lower]
        phishing_matches = [w for w in self.phishing_triggers if w in text_lower]

        reasons = []
        risk_score = 0
        fraud_type = "LEGITIMATE / UNKNOWN"

        if ponzi_matches:
            risk_score += 45
            fraud_type = "PONZI / FRAUDULENT INVESTMENT SCHEME"
            reasons.append(f"Ponzi / High-Yield Investment fraud indicators: '{', '.join(ponzi_matches[:4])}'")

        if betting_matches:
            risk_score += 45
            fraud_type = "ILLEGAL BETTING / COLOR PREDICTION PLATFORM"
            reasons.append(f"Illegal gambling / betting keywords detected: '{', '.join(betting_matches[:4])}'")

        if phishing_matches:
            risk_score += 50
            fraud_type = "CREDENTIAL HARVESTING / BANKING PHISHING"
            reasons.append(f"Credential harvesting cues (PIN/OTP/Aadhaar): '{', '.join(phishing_matches[:3])}'")

        if extracted_upis:
            reasons.append(f"Payment destination UPI IDs identified: {', '.join(extracted_upis[:3])}")
            risk_score += 15

        if extracted_accounts:
            reasons.append(f"Bank Account / IFSC handles found: Acc: {extracted_accounts[0]} (IFSC: {', '.join(extracted_ifscs) if extracted_ifscs else 'N/A'})")
            risk_score += 15

        if extracted_trc20 or extracted_eth:
            wallets = extracted_trc20 + extracted_eth
            reasons.append(f"Cryptocurrency laundering addresses found: {', '.join(wallets[:2])}")
            risk_score += 20

        if whatsapp_links:
            reasons.append(f"Direct redirection to unmonitored Telegram/WhatsApp channels: {len(whatsapp_links)} link(s)")
            risk_score += 10

        risk_score = min(100, max(risk_score, 10 if (extracted_upis or extracted_phones) else 0))

        if risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            if not reasons:
                reasons.append("Content analysis did not find active fraud patterns.")

        return {
            "source_url": source_url,
            "fraud_type": fraud_type,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "reasons": reasons,
            "extracted_identifiers": {
                "upi_ids": extracted_upis,
                "phone_numbers": extracted_phones,
                "bank_accounts": extracted_accounts,
                "ifsc_codes": extracted_ifscs,
                "crypto_wallets": extracted_trc20 + extracted_eth,
                "social_redirects": whatsapp_links[:5]
            },
            "summary": f"{risk_level} Risk: Classified as {fraud_type}."
        }
