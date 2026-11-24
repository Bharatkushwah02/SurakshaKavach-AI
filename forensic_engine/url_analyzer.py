import re
import urllib.parse
import socket
import ssl
from datetime import datetime
import tldextract

try:
    import whois
    WHOIS_AVAILABLE = True
except ImportError:
    WHOIS_AVAILABLE = False

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

class URLAnalyzer:
    def __init__(self):
        # High-risk disposable TLDs heavily used by phishing kits
        self.suspicious_tlds = {
            "xyz", "top", "cc", "buzz", "cfd", "link", "club", "work", "icu", 
            "tk", "ml", "ga", "cf", "gq", "click", "online", "site", "vip"
        }

        # URL Shorteners
        self.url_shorteners = {
            "bit.ly", "tinyurl.com", "cutt.ly", "t.co", "shorturl.at", "rb.gy", 
            "is.gd", "ow.ly", "buff.ly", "rebrand.ly", "tiny.cc", "goo.gl"
        }

        # Comprehensive Official Whitelist for Indian Brands, Subsidiaries & Govt Utilities (R3 Fix)
        self.official_brand_domains = {
            "sbi": {"sbi.co.in", "onlinesbi.sbi", "onlinesbi.com", "statebankofindia.com", "sbicard.com", "sbilife.com", "sbimf.com"},
            "yono": {"onlinesbi.sbi", "sbi.co.in"},
            "hdfc": {"hdfcbank.com", "hdfc.com", "hdfcergo.com", "hdfclife.com"},
            "icici": {"icicibank.com", "icicilombard.com", "iciciprulife.com", "icicidirect.com"},
            "pnb": {"pnbindia.in", "pnb.bank.in"},
            "bob": {"bankofbaroda.in", "bobfinancial.com"},
            "axis": {"axisbank.com"},
            "paytm": {"paytm.com", "paytmbank.com", "paytmmall.com"},
            "phonepe": {"phonepe.com"},
            "googlepay": {"pay.google.com", "google.com"},
            "jio": {"jio.com", "jiomart.com", "reliancedigital.in"},
            "jvvnl": {"energy.rajasthan.gov.in", "jaipurdiscom.com"},
            "avvnl": {"energy.rajasthan.gov.in", "ajmerdiscom.com"},
            "jdvvnl": {"energy.rajasthan.gov.in", "jodhpurdiscom.com"},
            "uidai": {"uidai.gov.in", "resident.uidai.gov.in"},
            "irctc": {"irctc.co.in"},
            "incometax": {"incometax.gov.in", "incometaxindia.gov.in"},
            "epfo": {"epfindia.gov.in"},
            "airtel": {"airtel.in", "airtel.com"},
            "amazon": {"amazon.in", "amazon.com"},
            "flipkart": {"flipkart.com"}
        }

        # Phishing path keywords
        self.phishing_keywords = [
            "login", "verify", "update-kyc", "pan-link", "download-apk", "apk",
            "bill-payment", "electricity-due", "claim-reward", "lottery",
            "task-bonus", "fast-loan", "cibil-clear", "recharge-free", "account-blocked",
            "netbanking", "pan-verify", "kyc-update", "suspended"
        ]

        # Known reported cyber crime scam domains (CERT-In / I4C IOCs)
        self.known_scam_domains = {
            "sbi-kyc-quickupdate.xyz": "SBI Yono Phishing Campaign",
            "jvvnl-bill-clear.online": "Rajasthan JVVNL Electricity Scam",
            "quick-loan-instant-disburse.top": "Predatory Loan Extortion App C2",
            "telegram-task-vip-profit.cc": "Telegram MLM / Task Scam",
            "india-post-parcel-track.site": "Postal Courier Phishing",
            "income-tax-refund-claim.club": "Tax Refund Scam Portal",
            "rummy-gold-win99.vip": "Illegal Betting / Money Laundering APK Host"
        }

    def _resolve_shortener(self, url):
        """Unshortens URL and extracts redirect hops if online."""
        if not REQUESTS_AVAILABLE:
            return url, 0
        try:
            resp = requests.head(url, allow_redirects=True, timeout=3, headers={"User-Agent": "Mozilla/5.0"})
            hops = len(resp.history)
            return resp.url, hops
        except Exception:
            return url, 0

    def _check_domain_age(self, domain):
        """Checks WHOIS creation date for domain age."""
        if not WHOIS_AVAILABLE:
            return None, None
        try:
            w = whois.whois(domain)
            creation = w.creation_date
            if isinstance(creation, list):
                creation = creation[0]
            if creation:
                age_days = (datetime.now() - creation).days
                registrar = w.registrar or "Unknown"
                return age_days, registrar
        except Exception:
            pass
        return None, None

    def _check_ssl_cert(self, hostname):
        """Checks SSL certificate issuer and validity (R5 Fix)."""
        try:
            ctx = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=3) as sock:
                with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    issuer = dict(x[0] for x in cert.get('issuer', []))
                    issuer_org = issuer.get('organizationName') or issuer.get('commonName') or "Trusted CA"
                    return True, issuer_org
        except Exception as e:
            return False, str(e)

    def analyze(self, raw_url):
        original_url = raw_url.strip()
        if not original_url.startswith(("http://", "https://")):
            raw_url = "http://" + original_url
        else:
            raw_url = original_url

        parsed = urllib.parse.urlparse(raw_url)
        netloc = parsed.netloc.lower()
        host = netloc.split(':')[0]
        path = parsed.path.lower()
        query = parsed.query.lower()

        extracted = tldextract.extract(host)
        domain_name = extracted.domain
        suffix = extracted.suffix
        subdomain = extracted.subdomain
        full_domain = f"{domain_name}.{suffix}" if suffix else host

        reasons = []
        risk_score = 0
        indicators = []

        # ================= OFFICIAL GOV / WHITELIST CHECK =================
        if suffix in {"gov.in", "nic.in", "res.in", "ac.in"}:
            return {
                "url": original_url,
                "domain": full_domain,
                "tld": suffix,
                "scheme": parsed.scheme,
                "risk_level": "LOW",
                "risk_score": 0,
                "indicators": ["OFFICIAL_GOVERNMENT_DOMAIN"],
                "reasons": [f"Verified Official Government / National Informatics Center portal (.{suffix})"],
                "summary": "LOW Risk: Verified Official Indian Government Portal."
            }

        # Check if full_domain is in official brand whitelists
        for brand, valid_domains in self.official_brand_domains.items():
            if full_domain in valid_domains:
                return {
                    "url": original_url,
                    "domain": full_domain,
                    "tld": suffix,
                    "scheme": parsed.scheme,
                    "risk_level": "LOW",
                    "risk_score": 0,
                    "indicators": ["OFFICIAL_WHITELISTED_DOMAIN"],
                    "reasons": [f"Verified Official Domain for {brand.upper()}"],
                    "summary": f"LOW Risk: Verified Official {brand.upper()} Domain."
                }

        # ================= 1. URL SHORTENER & REDIRECT RESOLUTION (R4 Fix: +35 score) =================
        is_shortener = full_domain in self.url_shorteners
        if is_shortener:
            risk_score += 35 # Guarantees at least MEDIUM floor
            reasons.append(f"URL Shortener detected ({full_domain}) — hides real destination to bypass email/SMS filters")
            indicators.append("URL_SHORTENER")

            # Try unshortening
            final_url, hops = self._resolve_shortener(raw_url)
            if hops > 0 and final_url != raw_url:
                reasons.append(f"Redirect chain detected ({hops} hops) leading to: {final_url}")
                indicators.append("REDIRECT_CHAIN")
                if final_url.lower() != raw_url.lower():
                    sub_analysis = self.analyze(final_url)
                    if sub_analysis["risk_score"] > 30:
                        risk_score = max(risk_score, sub_analysis["risk_score"])
                        reasons.extend([f"Destination flag: {r}" for r in sub_analysis["reasons"][:2]])

        # ================= 2. BLACKLIST CHECK =================
        if full_domain in self.known_scam_domains:
            risk_score += 90
            threat_name = self.known_scam_domains[full_domain]
            reasons.append(f"CRITICAL: Domain matches active cyber crime syndicate IOC ({threat_name})")
            indicators.append("BLACKLISTED_DOMAIN")

        # ================= 3. DIRECT IP HOSTING =================
        ip_pattern = re.compile(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?$')
        if ip_pattern.match(netloc):
            risk_score += 45
            reasons.append("High risk: Website hosted directly on a raw IP address instead of a domain name (drive-by malware/C2)")
            indicators.append("DIRECT_IP_HOST")

        # ================= 4. INSECURE HTTP vs HTTPS CERT (R5 Fix) =================
        if parsed.scheme == "http":
            risk_score += 15
            reasons.append("Insecure connection (HTTP without TLS encryption)")
            indicators.append("INSECURE_HTTP")
        elif parsed.scheme == "https":
            # Active SSL Inspection (R5 Fix)
            ssl_ok, ssl_info = self._check_ssl_cert(host)
            if ssl_ok:
                indicators.append("VALID_SSL")
                reasons.append(f"TLS/SSL Certificate verified (Issuer: {ssl_info})")
            else:
                # If cert check failed or connection error
                if "CERTIFICATE_VERIFY_FAILED" in str(ssl_info):
                    risk_score += 30
                    reasons.append("Untrusted or invalid SSL certificate (Self-signed or hostname mismatch)")
                    indicators.append("INVALID_SSL")

        # ================= 5. SUSPICIOUS TLD =================
        if suffix in self.suspicious_tlds:
            risk_score += 30
            reasons.append(f"Suspicious disposable top-level domain (.{suffix}) heavily correlated with throwaway phishing campaigns")
            indicators.append(f"SUSPICIOUS_TLD_{suffix.upper()}")

        # ================= 6. BRAND SPOOFING / TYPOSQUATTING (R3 Token-Aware Fix) =================
        spoofed_brands = []
        host_tokens = re.split(r'[\.\-_]', host)
        for brand, official_set in self.official_brand_domains.items():
            if full_domain not in official_set:
                # Brand is a standalone token in host (e.g. sbi-kyc or sbi.update or hdfcbank)
                is_standalone_token = brand in host_tokens
                # Or lookalike compound (e.g. sbi-login, hdfc-update)
                is_compound = any(f"{brand}-" in host or f"-{brand}" in host for b in [brand])
                # Or in path
                is_in_path = brand in path and len(brand) >= 4

                if is_standalone_token or is_compound or is_in_path:
                    spoofed_brands.append(brand)

        if spoofed_brands:
            risk_score += 45
            reasons.append(f"Brand Impersonation / Look-alike spoofing detected targeting: {', '.join(spoofed_brands).upper()}")
            indicators.append("BRAND_SPOOFING")

        # ================= 7. PHISHING PATH KEYWORDS =================
        matched_keywords = [k for k in self.phishing_keywords if k in path or k in query]
        if matched_keywords:
            risk_score += 20
            reasons.append(f"Phishing lure parameters found in URL path: '{', '.join(matched_keywords)}'")
            indicators.append("SUSPICIOUS_URL_PATH")

        # ================= 8. SUBDOMAIN OBFUSCATION =================
        if subdomain.count('.') >= 2:
            risk_score += 20
            reasons.append("Excessive subdomain nesting designed to deceive mobile browser address bars")
            indicators.append("SUBDOMAIN_OBFUSCATION")

        # ================= 9. DOMAIN AGE & WHOIS =================
        age_days, registrar = self._check_domain_age(full_domain)
        if age_days is not None:
            if age_days < 7:
                risk_score += 35
                reasons.append(f"Extremely fresh domain: Registered only {age_days} day(s) ago (Registrar: {registrar})")
                indicators.append("VERY_NEW_DOMAIN")
            elif age_days < 30:
                risk_score += 20
                reasons.append(f"Recently registered domain: Created {age_days} days ago (Registrar: {registrar})")
                indicators.append("RECENT_DOMAIN")

        # Cap score
        risk_score = min(100, risk_score)

        if risk_score >= 60:
            risk_level = "HIGH"
        elif risk_score >= 30:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
            if not reasons:
                reasons.append("Standard domain structure with no prominent phishing indicators.")

        return {
            "url": original_url,
            "domain": full_domain,
            "tld": suffix,
            "scheme": parsed.scheme,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "indicators": indicators,
            "reasons": reasons,
            "summary": f"{risk_level} Risk: {reasons[0] if reasons else 'Domain appears benign.'}"
        }
