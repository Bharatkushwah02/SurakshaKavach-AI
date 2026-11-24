import os
import io
import json
import urllib.request
from flask import Flask, render_template, request, jsonify, Response
from forensic_engine import (
    MessageAnalyzer,
    URLAnalyzer,
    APKAnalyzer,
    WebsiteAnalyzer,
    CorrelationEngine,
    ReportGenerator
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024 # 32 MB max APK upload

# Initialize Forensic Engines with cross-engine wiring
url_analyzer = URLAnalyzer()
msg_analyzer = MessageAnalyzer(url_analyzer=url_analyzer) # Cross-engine URL analysis
apk_analyzer = APKAnalyzer()
web_analyzer = WebsiteAnalyzer()
db = CorrelationEngine("surakshakavach.db")
report_gen = ReportGenerator()

# Seed mock database with initial cases if empty
db.seed_initial_data()

# Whitelist allowed sample APK files (Path Traversal Protection)
ALLOWED_SAMPLE_APKS = {
    "CashSpeed_PredatoryLoan_v2.apk",
    "Simple_Calculator_Safe.apk"
}

@app.route('/')
def index():
    heatlist = db.get_heatlist()
    cases = db.search_cases()
    return render_template('index.html', heatlist=heatlist, initial_cases=cases)

@app.route('/api/analyze/message', methods=['POST'])
def analyze_message():
    data = request.get_json() or {}
    text = data.get('text', '').strip()
    if not text:
        return jsonify({"error": "No message text provided"}), 400

    result = msg_analyzer.analyze(text)
    
    # Save to investigation cases
    case_id, case_number = db.add_case(
        source_type="SMS",
        title=f"SMS Scam: {result.get('threat_type', 'Scam Alert')}",
        risk_level=result['risk_level'],
        risk_score=result['risk_score'],
        threat_category=result.get('threat_type', 'SMS_FRAUD'),
        raw_data=text,
        analysis_result=result
    )
    result['case_id'] = case_id
    result['case_number'] = case_number
    return jsonify(result)

@app.route('/api/analyze/url', methods=['POST'])
def analyze_url():
    data = request.get_json() or {}
    url = data.get('url', '').strip()
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    result = url_analyzer.analyze(url)
    
    # Save to investigation cases
    case_id, case_number = db.add_case(
        source_type="URL",
        title=f"Phishing URL: {result.get('domain', 'Suspicious Link')}",
        risk_level=result['risk_level'],
        risk_score=result['risk_score'],
        threat_category="PHISHING_DOMAIN",
        raw_data=url,
        analysis_result=result
    )
    result['case_id'] = case_id
    result['case_number'] = case_number
    return jsonify(result)

@app.route('/api/analyze/apk', methods=['POST'])
def analyze_apk():
    # Check if a file was uploaded
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty file name"}), 400
        content = file.read()
        filename = file.filename
    else:
        # Check if pre-packaged sample APK was requested
        data = request.get_json() or {}
        sample_name = data.get('sample')
        if not sample_name:
            return jsonify({"error": "Upload an APK file or specify an available sample"}), 400
        
        # Security: Whitelist check
        if sample_name not in ALLOWED_SAMPLE_APKS:
            return jsonify({"error": f"Unauthorized sample name: {sample_name}"}), 403

        sample_path = os.path.join('sample_apks', sample_name)
        if not os.path.exists(sample_path):
            return jsonify({"error": f"Sample APK '{sample_name}' not found"}), 404
        with open(sample_path, 'rb') as f:
            content = f.read()
        filename = sample_name

    result = apk_analyzer.analyze_file(content, filename=filename)

    case_id, case_number = db.add_case(
        source_type="APK",
        title=f"Android APK: {result.get('app_name', filename)}",
        risk_level=result['risk_level'],
        risk_score=result['risk_score'],
        threat_category=result.get('classification', 'MALICIOUS_APP'),
        raw_data=filename,
        analysis_result=result
    )
    result['case_id'] = case_id
    result['case_number'] = case_number
    return jsonify(result)

@app.route('/api/analyze/website', methods=['POST'])
def analyze_website():
    data = request.get_json() or {}
    content = data.get('content', '').strip()
    source_url = data.get('url', '').strip()

    if not content and not source_url:
        return jsonify({"error": "Please provide website content or URL"}), 400

    fetch_failed = False
    if not content and source_url:
        try:
            req = urllib.request.Request(source_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=4) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
        except Exception:
            fetch_failed = True

    # Fix 2: Never fabricate fake content or fake UPIs/numbers!
    if fetch_failed or (not content and source_url):
        # Analyze purely based on URL/domain heuristics without fake evidence
        url_res = url_analyzer.analyze(source_url)
        result = {
            "source_url": source_url,
            "fraud_type": "UNREACHABLE_HOST / DOMAIN_TRIAGE",
            "risk_level": url_res["risk_level"],
            "risk_score": url_res["risk_score"],
            "reasons": [
                "Website content could not be retrieved from host (server offline, unreachable, or domain inactive).",
                *url_res["reasons"]
            ],
            "extracted_identifiers": {
                "upi_ids": [],
                "phone_numbers": [],
                "bank_accounts": [],
                "ifsc_codes": [],
                "crypto_wallets": [],
                "social_redirects": []
            },
            "summary": f"{url_res['risk_level']} Risk: Host unreachable. Domain risk evaluated as {url_res['risk_level']}."
        }
    else:
        result = web_analyzer.analyze(content, source_url=source_url)

    case_id, case_number = db.add_case(
        source_type="WEBSITE",
        title=f"Web Scam: {result.get('fraud_type', 'Suspicious Platform')}",
        risk_level=result['risk_level'],
        risk_score=result['risk_score'],
        threat_category=result.get('fraud_type', 'FRAUDULENT_WEBSITE'),
        raw_data=source_url or content[:200],
        analysis_result=result
    )
    result['case_id'] = case_id
    result['case_number'] = case_number
    return jsonify(result)

@app.route('/api/cases', methods=['GET'])
def get_cases():
    query = request.args.get('q', '').strip()
    cases = db.search_cases(query)
    return jsonify(cases)

@app.route('/api/cases/<int:case_id>', methods=['GET'])
def get_case_detail(case_id):
    case = db.get_case(case_id)
    if not case:
        return jsonify({"error": "Case not found"}), 404
    return jsonify(case)

@app.route('/api/heatlist', methods=['GET'])
def get_heatlist():
    return jsonify(db.get_heatlist())

@app.route('/api/report/<int:case_id>/pdf', methods=['GET'])
def download_pdf_report(case_id):
    case = db.get_case(case_id)
    if not case:
        return jsonify({"error": "Case not found"}), 404

    pdf_bytes = report_gen.generate_case_pdf(case)
    return Response(
        pdf_bytes,
        mimetype="application/pdf",
        headers={"Content-Disposition": f"attachment;filename=FORENSIC_REPORT_{case.get('case_number', case_id)}.pdf"}
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"[*] SurakshaKavach AI starting on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=False)
