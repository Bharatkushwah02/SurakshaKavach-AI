import sqlite3
import json
import os
import hashlib
from datetime import datetime

class CorrelationEngine:
    def __init__(self, db_path="surakshakavach.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # Cases Table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_number TEXT UNIQUE,
                timestamp TEXT,
                source_type TEXT, -- SMS, URL, APK, WEBSITE
                title TEXT,
                risk_level TEXT, -- HIGH, MEDIUM, LOW
                risk_score INTEGER,
                threat_category TEXT,
                raw_data TEXT,
                raw_sha256 TEXT,
                analysis_json TEXT
            )
            """)

            # Entity Mapping Table (For cross-linking Phone, UPI, Domain across cases)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS entity_links (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                entity_type TEXT, -- PHONE, UPI, DOMAIN, IP, CRYPTO, BANK_ACC, IFSC, SHA256
                entity_value TEXT,
                FOREIGN KEY(case_id) REFERENCES cases(id)
            )
            """)
            conn.commit()

    def add_case(self, source_type, title, risk_level, risk_score, threat_category, raw_data, analysis_result):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            # 4-byte random hex to guarantee 0 collisions
            case_number = f"RAJ-CYBER-{datetime.now().strftime('%y%m%d')}-{os.urandom(4).hex().upper()}"
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Calculate SHA256 of raw evidence
            if isinstance(raw_data, str):
                raw_bytes = raw_data.encode('utf-8')
            else:
                raw_bytes = bytes(raw_data)
            raw_sha256 = analysis_result.get("sha256") or hashlib.sha256(raw_bytes).hexdigest()
            analysis_result["sha256"] = raw_sha256

            cursor.execute("""
            INSERT INTO cases (case_number, timestamp, source_type, title, risk_level, risk_score, threat_category, raw_data, raw_sha256, analysis_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (case_number, timestamp, source_type, title, risk_level, risk_score, threat_category, str(raw_data), raw_sha256, json.dumps(analysis_result)))
            
            case_id = cursor.lastrowid

            # Extract entities to index
            entities = []
            extracted = analysis_result.get("extracted_identifiers", {})
            
            # Phones
            phones = extracted.get("phones", []) or extracted.get("phone_numbers", []) or analysis_result.get("extracted_phones", [])
            for p in phones:
                entities.append(("PHONE", p.strip()))

            # UPIs
            upis = extracted.get("upi_ids", []) or analysis_result.get("extracted_upis", [])
            for u in upis:
                entities.append(("UPI", u.strip().lower()))

            # URLs / Domains
            urls = extracted.get("urls", []) or ([analysis_result.get("domain")] if analysis_result.get("domain") else [])
            for u in urls:
                domain = u.split('/')[2] if '://' in u else u.split('/')[0]
                entities.append(("DOMAIN", domain.lower()))

            # C2 URLs for APK
            c2_urls = analysis_result.get("extracted_c2_urls", [])
            for c2 in c2_urls:
                domain = c2.split('/')[2] if '://' in c2 else c2.split('/')[0]
                entities.append(("DOMAIN", domain.lower()))

            # Bank Accounts & IFSC
            accounts = extracted.get("bank_accounts", [])
            for acc in accounts:
                entities.append(("BANK_ACC", str(acc).strip()))

            ifscs = extracted.get("ifsc_codes", [])
            for ifsc in ifscs:
                entities.append(("IFSC", str(ifsc).strip().upper()))

            # Crypto Wallets
            crypto_wallets = extracted.get("crypto_wallets", [])
            for cw in crypto_wallets:
                entities.append(("CRYPTO", str(cw).strip()))

            # SHA256 Checksum
            entities.append(("SHA256", raw_sha256))

            # Insert Entity Links
            for e_type, e_val in set(entities):
                if e_val:
                    cursor.execute("INSERT INTO entity_links (case_id, entity_type, entity_value) VALUES (?, ?, ?)", (case_id, e_type, e_val))

            conn.commit()
            return case_id, case_number

    def get_heatlist(self):
        """Returns the most frequently reported scam phone numbers, domains, and UPI IDs."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Trending Phones
            cursor.execute("""
            SELECT entity_value, count(*) as reports_count 
            FROM entity_links 
            WHERE entity_type = 'PHONE' 
            GROUP BY entity_value 
            ORDER BY reports_count DESC 
            LIMIT 6
            """)
            phones = [{"value": row["entity_value"], "count": row["reports_count"]} for row in cursor.fetchall()]

            # Trending Domains
            cursor.execute("""
            SELECT entity_value, count(*) as reports_count 
            FROM entity_links 
            WHERE entity_type = 'DOMAIN' 
            GROUP BY entity_value 
            ORDER BY reports_count DESC 
            LIMIT 6
            """)
            domains = [{"value": row["entity_value"], "count": row["reports_count"]} for row in cursor.fetchall()]

            # Trending UPIs
            cursor.execute("""
            SELECT entity_value, count(*) as reports_count 
            FROM entity_links 
            WHERE entity_type = 'UPI' 
            GROUP BY entity_value 
            ORDER BY reports_count DESC 
            LIMIT 6
            """)
            upis = [{"value": row["entity_value"], "count": row["reports_count"]} for row in cursor.fetchall()]

            return {
                "phones": phones,
                "domains": domains,
                "upis": upis
            }

    def search_cases(self, query=""):
        """Comprehensive search across case metadata, raw text, analysis JSON, and entity_links."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            if query:
                q = f"%{query}%"
                cursor.execute("""
                SELECT DISTINCT c.*, (
                    SELECT GROUP_CONCAT(entity_type || ':' || entity_value, ', ') 
                    FROM entity_links 
                    WHERE case_id = c.id
                ) as linked_entities
                FROM cases c
                LEFT JOIN entity_links el ON c.id = el.case_id
                WHERE c.case_number LIKE ? 
                   OR c.title LIKE ? 
                   OR c.raw_data LIKE ? 
                   OR c.threat_category LIKE ?
                   OR c.analysis_json LIKE ?
                   OR el.entity_value LIKE ?
                ORDER BY c.id DESC
                """, (q, q, q, q, q, q))
            else:
                cursor.execute("""
                SELECT c.*, (
                    SELECT GROUP_CONCAT(entity_type || ':' || entity_value, ', ') 
                    FROM entity_links 
                    WHERE case_id = c.id
                ) as linked_entities
                FROM cases c
                ORDER BY c.id DESC
                LIMIT 50
                """)
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_case(self, case_id):
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cases WHERE id = ? OR case_number = ?", (case_id, case_id))
            row = cursor.fetchone()
            if not row:
                return None
            case = dict(row)
            case["analysis"] = json.loads(case["analysis_json"])
            
            # Fetch linked entities
            cursor.execute("SELECT entity_type, entity_value FROM entity_links WHERE case_id = ?", (case["id"],))
            case["entities"] = [dict(r) for r in cursor.fetchall()]
            
            # Find related cases sharing ANY of these entities
            related_cases = []
            for ent in case["entities"]:
                if ent["entity_type"] == "SHA256":
                    continue # Skip raw hash for syndicate linking
                cursor.execute("""
                SELECT c.id, c.case_number, c.source_type, c.title, c.risk_level, c.timestamp
                FROM cases c
                JOIN entity_links el ON c.id = el.case_id
                WHERE el.entity_type = ? AND el.entity_value = ? AND c.id != ?
                GROUP BY c.id
                """, (ent["entity_type"], ent["entity_value"], case["id"]))
                for match in cursor.fetchall():
                    m_dict = dict(match)
                    m_dict["shared_entity"] = f"{ent['entity_type']}: {ent['entity_value']}"
                    related_cases.append(m_dict)

            case["related_cases"] = related_cases
            return case

    def seed_initial_data(self):
        """Populates the database with realistic Rajasthan Cyber Crime Cell sample cases."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) as cnt FROM cases")
            if cursor.fetchone()["cnt"] > 0:
                return # Already seeded

        # Seed 1: JVVNL Electricity Bill SMS Scam
        sms_text_1 = "Dear Consumer, Your JVVNL Power will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Please immediately contact our Electricity Officer Mr. Verma at 9829012345 or pay via http://jvvnl-bill-clear.online"
        self.add_case(
            source_type="SMS",
            title="JVVNL Electricity Disconnection Phishing Campaign",
            risk_level="HIGH",
            risk_score=95,
            threat_category="ELECTRICITY_BOARD_FRAUD",
            raw_data=sms_text_1,
            analysis_result={
                "risk_level": "HIGH",
                "risk_score": 95,
                "threat_type": "ELECTRICITY_BOARD",
                "urgency_score": 85,
                "impersonation_score": 90,
                "extracted_identifiers": {
                    "phones": ["9829012345"],
                    "urls": ["http://jvvnl-bill-clear.online"],
                    "upi_ids": []
                },
                "reasons": [
                    "High-pressure urgency tactics ('tonight at 9:30 PM')",
                    "Impersonating Rajasthan State Utility (JVVNL)",
                    "Known phishing domain registered on disposable host"
                ]
            }
        )

        # Seed 2: CashSpeed Predatory Loan App APK
        self.add_case(
            source_type="APK",
            title="CashSpeed Instant Personal Loan Extortion APK",
            risk_level="HIGH",
            risk_score=90,
            threat_category="PREDATORY_LOAN_EXTORTION",
            raw_data="CashSpeed_PredatoryLoan_v2.apk",
            analysis_result={
                "app_name": "CashSpeed",
                "filename": "CashSpeed_PredatoryLoan_v2.apk",
                "package_name": "com.cashspeed.loan.fastcredit",
                "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
                "risk_level": "HIGH",
                "risk_score": 90,
                "classification": "MALICIOUS / FAKE LOAN EXTORTION APP",
                "dangerous_permissions": [
                    {"name": "android.permission.READ_CONTACTS", "label": "Access Contact List", "risk": 30},
                    {"name": "android.permission.READ_SMS", "label": "Read Incoming SMS / OTPs", "risk": 35},
                    {"name": "android.permission.CAMERA", "label": "Access Device Camera", "risk": 20}
                ],
                "extracted_c2_urls": ["http://quick-loan-instant-disburse.top/api/sync", "http://jvvnl-bill-clear.online/loan_hook"],
                "extracted_phones": ["9829012345", "9785123456"],
                "extracted_upis": ["loanrepay@ybl", "fastsettle@paytm"],
                "reasons": [
                    "Classic predatory loan spyware profile (Contacts + SMS + Camera)",
                    "C2 server correlates with electricity scam domain",
                    "Hardcoded recovery agent phone 9829012345 linked to prior SMS campaign"
                ]
            }
        )

        # Seed 3: SBI Yono KYC Pan Link Phishing URL
        self.add_case(
            source_type="URL",
            title="SBI Yono Look-alike Netbanking Phishing",
            risk_level="HIGH",
            risk_score=92,
            threat_category="BANKING_PHISHING",
            raw_data="http://sbi-kyc-quickupdate.xyz/login.php",
            analysis_result={
                "url": "http://sbi-kyc-quickupdate.xyz/login.php",
                "domain": "sbi-kyc-quickupdate.xyz",
                "tld": "xyz",
                "risk_level": "HIGH",
                "risk_score": 92,
                "indicators": ["BLACKLISTED_DOMAIN", "BRAND_SPOOFING", "SUSPICIOUS_TLD_XYZ"],
                "reasons": [
                    "Critical: Matches known SBI phishing syndicate IOC",
                    "Brand Impersonation targeting State Bank of India",
                    "Suspicious disposable .xyz top-level domain"
                ],
                "extracted_identifiers": {
                    "urls": ["http://sbi-kyc-quickupdate.xyz"],
                    "phones": ["9785123456"],
                    "upi_ids": []
                }
            }
        )

        # Seed 4: Daman Games Color Prediction Ponzi
        self.add_case(
            source_type="WEBSITE",
            title="Daman VIP Color Prediction & Illegal Betting Scheme",
            risk_level="HIGH",
            risk_score=88,
            threat_category="ILLEGAL_BETTING_PONZI",
            raw_data="https://daman-vip-color99.cc/recharge",
            analysis_result={
                "source_url": "https://daman-vip-color99.cc/recharge",
                "fraud_type": "ILLEGAL BETTING / COLOR PREDICTION PLATFORM",
                "risk_level": "HIGH",
                "risk_score": 88,
                "extracted_identifiers": {
                    "upi_ids": ["damanvip@ybl", "fastsettle@paytm"],
                    "phone_numbers": ["9123456780"],
                    "bank_accounts": ["918237461928"],
                    "ifsc_codes": ["PYTM0123456"],
                    "crypto_wallets": ["TJw5mNB4k9fVbE9yM5zD1a7k2p9xK"],
                    "social_redirects": ["https://wa.me/919123456780"]
                },
                "reasons": [
                    "Color prediction illegal gambling keywords detected",
                    "Unregistered payment gateway using mule UPI ID (damanvip@ybl)",
                    "Telegram and WhatsApp direct rerouting"
                ]
            }
        )
