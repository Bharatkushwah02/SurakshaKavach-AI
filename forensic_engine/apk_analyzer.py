import os
import zipfile
import re
import hashlib
import io

try:
    from androguard.core.apk import APK as AndroguardAPK
    ANDROGUARD_AVAILABLE = True
except ImportError:
    ANDROGUARD_AVAILABLE = False

class APKAnalyzer:
    def __init__(self):
        # Critical intrusive permissions heavily abused by predatory loan apps & SMS stealers
        self.dangerous_permissions = {
            "android.permission.READ_CONTACTS": {
                "risk": 30,
                "label": "Access Contact List",
                "desc": "Used by predatory loan apps to harvest family contacts for extortion and public shaming."
            },
            "android.permission.WRITE_CONTACTS": {
                "risk": 20,
                "label": "Modify Contacts",
                "desc": "Can manipulate address book entries or inject spam contacts."
            },
            "android.permission.READ_SMS": {
                "risk": 35,
                "label": "Read Incoming SMS / OTPs",
                "desc": "Allows unauthorized interception of banking OTPs and personal messages."
            },
            "android.permission.RECEIVE_SMS": {
                "risk": 30,
                "label": "Intercept SMS Messages",
                "desc": "Monitors incoming SMS triggers to siphon OTPs silently."
            },
            "android.permission.SEND_SMS": {
                "risk": 25,
                "label": "Send SMS Silently",
                "desc": "Used for SMS toll fraud or spreading malicious links to contacts."
            },
            "android.permission.CAMERA": {
                "risk": 20,
                "label": "Access Device Camera",
                "desc": "Captures user facial photos, often morphed for blackmail in fake loan schemes."
            },
            "android.permission.ACCESS_FINE_LOCATION": {
                "risk": 15,
                "label": "High-Precision GPS Location",
                "desc": "Tracks victim live physical coordinates."
            },
            "android.permission.RECORD_AUDIO": {
                "risk": 20,
                "label": "Record Ambient Audio",
                "desc": "Eavesdropping on microphone audio."
            },
            "android.permission.READ_PHONE_STATE": {
                "risk": 15,
                "label": "Read IMEI and SIM Details",
                "desc": "Device fingerprinting and subscriber tracking."
            },
            "android.permission.REQUEST_INSTALL_PACKAGES": {
                "risk": 30,
                "label": "Install Dropper Apps",
                "desc": "Allows downloading and executing secondary payload malware without Play Store."
            },
            "android.permission.BIND_ACCESSIBILITY_SERVICE": {
                "risk": 40,
                "label": "Accessibility Service Abuse",
                "desc": "Keylogging, screen scraping, and full device hijacking."
            }
        }

        # Regex for extractable strings
        self.url_regex = re.compile(rb'https?://[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,6}(?::\d+)?(?:/[^\s"\'>]*)?')
        self.phone_regex = re.compile(rb'(?:\+?91)?[6-9]\d{9}')
        self.upi_regex = re.compile(rb'[\w\.\-]+@(?:okaxis|okhdfcbank|oksbi|okicici|paytm|ybl|apl|ibl|axisbank|barodampay|freecharge|airtel|upi)')

        # Whitelist of standard Android framework namespaces
        self.framework_url_ignore = [
            "schemas.android.com", "schema.android.com", "w3.org", "google.com/asf",
            "apache.org", "android.googlesource.com", "developer.android.com"
        ]

    def analyze_file(self, file_path_or_bytes, filename="uploaded.apk"):
        """Performs static forensic inspection of the Android APK package."""
        sha256_hash = hashlib.sha256()

        if isinstance(file_path_or_bytes, str) and os.path.isfile(file_path_or_bytes):
            file_size_kb = round(os.path.getsize(file_path_or_bytes) / 1024, 2)
            with open(file_path_or_bytes, 'rb') as f:
                content = f.read()
        else:
            content = file_path_or_bytes
            file_size_kb = round(len(content) / 1024, 2)

        sha256_hash.update(content)
        file_sha256 = sha256_hash.hexdigest()

        # Check if valid ZIP / APK archive
        is_valid_zip = False
        try:
            with zipfile.ZipFile(io.BytesIO(content), 'r') as z:
                is_valid_zip = True
                namelist = z.namelist()
                has_manifest = 'AndroidManifest.xml' in namelist
                has_dex = any(n.endswith('.dex') for n in namelist)
        except Exception:
            is_valid_zip = False
            has_manifest = False
            has_dex = False

        if not is_valid_zip or (not has_manifest and not has_dex):
            return {
                "app_name": filename,
                "filename": filename,
                "package_name": "INVALID_OR_CORRUPT",
                "file_size_kb": file_size_kb,
                "sha256": file_sha256,
                "is_valid_apk": False,
                "risk_level": "LOW",
                "risk_score": 0,
                "classification": "INVALID / NOT A VALID APK ARCHIVE",
                "permissions_count": 0,
                "dangerous_permissions": [],
                "extracted_c2_urls": [],
                "extracted_phones": [],
                "extracted_upis": [],
                "reasons": ["File format validation failed: Uploaded file is not a valid Android APK package."],
                "summary": "INVALID: Not a valid Android package file."
            }

        detected_permissions = {}
        c2_urls = set()
        extracted_phones = set()
        extracted_upis = set()
        package_name = "unknown.application.package"
        app_name = filename.replace('.apk', '')

        # 1. Try Parsing with Androguard
        if ANDROGUARD_AVAILABLE:
            try:
                apk_obj = AndroguardAPK(content, raw=True)
                pkg = apk_obj.get_package()
                if pkg:
                    package_name = pkg
                aname = apk_obj.get_app_name()
                if aname:
                    app_name = aname
                
                perms = apk_obj.get_permissions() or []
                for perm in perms:
                    for d_perm, info in self.dangerous_permissions.items():
                        if perm == d_perm or perm.endswith(d_perm.split('.')[-1]):
                            if d_perm not in detected_permissions:
                                detected_permissions[d_perm] = {
                                    "name": d_perm,
                                    "short_name": d_perm.split('.')[-1],
                                    "label": info["label"],
                                    "desc": info["desc"],
                                    "risk": info["risk"]
                                }
            except Exception:
                pass

        # 2. Decompile DEX and Asset Strings + Manifest String Fallback (R1 FIX: UNION of both methods!)
        try:
            with zipfile.ZipFile(io.BytesIO(content), 'r') as z:
                for item in z.namelist():
                    if item.endswith('.dex') or item.endswith('.xml') or item.endswith('.properties'):
                        try:
                            data = z.read(item)

                            # Extract C2 URLs
                            for u in self.url_regex.findall(data):
                                try:
                                    decoded_u = u.decode('utf-8', errors='ignore')
                                    if not any(ign in decoded_u for ign in self.framework_url_ignore):
                                        if len(decoded_u) < 120 and not decoded_u.endswith(('.png', '.jpg', '.xml')):
                                            c2_urls.add(decoded_u)
                                except Exception:
                                    pass

                            # Extract Phone numbers
                            for p in self.phone_regex.findall(data):
                                try:
                                    p_str = p.decode('utf-8', errors='ignore')
                                    if len(p_str) == 10 or (len(p_str) == 12 and p_str.startswith('91')):
                                        extracted_phones.add(p_str)
                                except Exception:
                                    pass

                            # Extract UPI IDs
                            for upi in self.upi_regex.findall(data):
                                try:
                                    extracted_upis.add(upi.decode('utf-8', errors='ignore'))
                                except Exception:
                                    pass

                            # String-based permission scan (works for both plain XML and fallback)
                            data_str = data.decode('latin1', errors='ignore')
                            for perm, info in self.dangerous_permissions.items():
                                short_name = perm.split('.')[-1]
                                if perm in data_str or short_name in data_str:
                                    if perm not in detected_permissions:
                                        detected_permissions[perm] = {
                                            "name": perm,
                                            "short_name": short_name,
                                            "label": info["label"],
                                            "desc": info["desc"],
                                            "risk": info["risk"]
                                        }

                            if package_name == "unknown.application.package":
                                pkg_match = re.search(r'package="([a-zA-Z0-9_\.]+)"', data_str)
                                if pkg_match:
                                    package_name = pkg_match.group(1)
                                else:
                                    cand = re.findall(r'\b(com\.[a-z0-9_]+\.[a-z0-9_]+)\b', data_str)
                                    if cand:
                                        package_name = cand[0]
                        except Exception:
                            continue
        except Exception:
            pass

        perms_list = list(detected_permissions.values())

        # 3. Risk Evaluation & Threat Triaging
        risk_score = 0
        reasons = []

        # Check Predatory Loan App extortion signature: Contacts + SMS + Camera
        has_contacts = any("READ_CONTACTS" in p["name"] for p in perms_list)
        has_sms = any("READ_SMS" in p["name"] or "RECEIVE_SMS" in p["name"] for p in perms_list)
        has_camera = any("CAMERA" in p["name"] for p in perms_list)
        has_dropper = any("REQUEST_INSTALL_PACKAGES" in p["name"] for p in perms_list)
        has_accessibility = any("BIND_ACCESSIBILITY_SERVICE" in p["name"] for p in perms_list)

        if has_contacts and has_sms:
            risk_score += 55
            reasons.append("CRITICAL: Predatory Loan App / Spyware extortion profile detected (Requests both Contacts & SMS Reading).")
        if has_contacts:
            risk_score += 25
            reasons.append("Requests sensitive Contact List access — harvested to blackmail borrower's friends & relatives.")
        if has_sms:
            risk_score += 30
            reasons.append("Requests SMS interception privileges — enables unauthorized interception of banking OTPs.")
        if has_camera:
            risk_score += 15
            reasons.append("Requests Camera access — frequently abused to capture and morph victim portraits for extortion.")
        if has_dropper:
            risk_score += 25
            reasons.append("Dropper privilege: Can install secondary unverified packages outside Google Play Store.")
        if has_accessibility:
            risk_score += 40
            reasons.append("CRITICAL: Requests Accessibility Service — allows full device takeover and screen recording.")

        # Hardcoded IOCs
        if c2_urls:
            reasons.append(f"Discovered {len(c2_urls)} embedded server endpoints / Command & Control (C2) URLs.")
            risk_score += 20
        if extracted_phones:
            reasons.append(f"Extracted {len(extracted_phones)} hardcoded contact / recovery numbers.")
        if extracted_upis:
            reasons.append(f"Extracted hardcoded payment handles: {', '.join(list(extracted_upis)[:3])}")
            risk_score += 15

        risk_score = min(100, max(risk_score, 10 if perms_list else 0))

        if risk_score >= 60:
            risk_level = "HIGH"
            app_classification = "MALICIOUS / FAKE LOAN EXTORTION APP"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
            app_classification = "SUSPICIOUS UTILITY APP"
        else:
            risk_level = "LOW"
            app_classification = "BENIGN ANDROID APPLICATION"
            if not reasons:
                reasons.append("Clean package: No predatory permissions or malicious C2 endpoints discovered.")

        return {
            "app_name": app_name,
            "filename": filename,
            "package_name": package_name,
            "file_size_kb": file_size_kb,
            "sha256": file_sha256,
            "is_valid_apk": True,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "classification": app_classification,
            "permissions_count": len(perms_list),
            "dangerous_permissions": perms_list,
            "extracted_c2_urls": list(c2_urls)[:10],
            "extracted_phones": list(extracted_phones)[:10],
            "extracted_upis": list(extracted_upis)[:10],
            "reasons": reasons,
            "summary": f"{risk_level} Risk: {app_classification} with {len(perms_list)} intrusive permission(s)."
        }
