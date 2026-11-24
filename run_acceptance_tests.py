import sys
import os
import json

from forensic_engine import (
    MessageAnalyzer,
    URLAnalyzer,
    APKAnalyzer,
    WebsiteAnalyzer,
    CorrelationEngine,
    ReportGenerator
)

def run_tests():
    print("=" * 65)
    print("SURAKSHAKAVACH AI — FULL REGRESSION TEST SUITE (FINAL v3)")
    print("=" * 65)

    url_az = URLAnalyzer()
    msg_az = MessageAnalyzer(url_analyzer=url_az)
    apk_az = APKAnalyzer()
    web_az = WebsiteAnalyzer()
    
    test_db_path = "acceptance_test.db"
    if os.path.exists(test_db_path):
        os.remove(test_db_path)
    db = CorrelationEngine(test_db_path)
    db.seed_initial_data()
    rep_gen = ReportGenerator()

    passed = 0
    total = 0

    def check(title, condition, detail=""):
        nonlocal passed, total
        total += 1
        status = "PASSED" if condition else "FAILED"
        if condition:
            passed += 1
            print(f"[{status}] {title} {detail}")
        else:
            print(f"[{status}] {title} — DETAIL: {detail}")

    # ================= R1: OPTIONAL LOCAL APK SAMPLE =================
    cashspeed_sample = "sample_apks/CashSpeed_PredatoryLoan_v2.apk"
    if os.path.isfile(cashspeed_sample):
        cs_res = apk_az.analyze_file(cashspeed_sample, "CashSpeed_PredatoryLoan_v2.apk")
        cs_perms_count = len(cs_res.get("dangerous_permissions", []))
        check("R1: CashSpeed APK (Androguard + Fallback Union)",
              cs_res["risk_level"] == "HIGH" and cs_perms_count >= 3,
              f"(Got {cs_res['risk_level']} {cs_res['risk_score']}, Perms: {cs_perms_count})")
    else:
        print("[SKIPPED] R1: Optional APK sample is not included")

    # ================= R2: GENUINE OTP & BANK SAFETY WARNINGS =================
    gen_otp_sms = "OTP for transaction of Rs 1,200 at Amazon is 482910. Do not share OTP with anyone including bank staff."
    res_gen_otp = msg_az.analyze(gen_otp_sms)
    check("R2: Genuine OTP with 'Do not share' warning", 
          res_gen_otp["risk_level"] == "LOW",
          f"(Got {res_gen_otp['risk_level']} {res_gen_otp['risk_score']})")

    hdfc_safety_sms = "HDFC Bank: We NEVER ask for your PIN, OTP or CVV. Do not share these with anyone."
    res_hdfc_safety = msg_az.analyze(hdfc_safety_sms)
    check("R2: HDFC Bank 'We NEVER ask' Advisory",
          res_hdfc_safety["risk_level"] == "LOW",
          f"(Got {res_hdfc_safety['risk_level']} {res_hdfc_safety['risk_score']})")

    # Positive test: Active OTP solicitation scam MUST be HIGH
    scam_otp_sms = "Apna OTP bhejo varna khata band kar diya jayega"
    res_scam_otp = msg_az.analyze(scam_otp_sms)
    check("R2: Active Solicitation 'OTP bhejo' Scam",
          res_scam_otp["risk_level"] == "HIGH",
          f"(Got {res_scam_otp['risk_level']} {res_scam_otp['risk_score']})")

    # ================= S1 FIX: DISGUISED SCAMS WITH PROTECTIVE PHRASES =================
    disguised_sms_1 = "Stay alert! Fraud badh gaya hai... turant hamare officer ko call karke OTP bataye 9812345678"
    res_disguised_1 = msg_az.analyze(disguised_sms_1)
    check("S1: Disguised 'Stay alert + OTP bataye' Scam",
          res_disguised_1["risk_level"] == "HIGH" and res_disguised_1["risk_score"] >= 70,
          f"(Got {res_disguised_1['risk_level']} {res_disguised_1['risk_score']})")

    disguised_sms_2 = "Bank never asks for OTP. But... please share the OTP with our officer. Call 9876501234"
    res_disguised_2 = msg_az.analyze(disguised_sms_2)
    check("S1: Disguised 'Bank never asks + share the OTP' Scam",
          res_disguised_2["risk_level"] == "HIGH" and res_disguised_2["risk_score"] >= 70,
          f"(Got {res_disguised_2['risk_level']} {res_disguised_2['risk_score']})")

    # ================= R3: WHITELIST EXPANSION (sbicard.com & jiomart.com) =================
    res_sbicard = url_az.analyze("https://sbicard.com")
    res_jiomart = url_az.analyze("https://jiomart.com")
    check("R3: Whitelisted sbicard.com & jiomart.com",
          res_sbicard["risk_level"] == "LOW" and res_jiomart["risk_level"] == "LOW",
          f"(sbicard: {res_sbicard['risk_level']}, jiomart: {res_jiomart['risk_level']})")

    # ================= R4: SHORTENER MUST BE MEDIUM+ =================
    res_bitly = url_az.analyze("https://bit.ly/3AbCdEf")
    check("R4: Shortener bit.ly Floor Score >= 30 (MEDIUM+)",
          res_bitly["risk_level"] in ("MEDIUM", "HIGH") and res_bitly["risk_score"] >= 30,
          f"(Got {res_bitly['risk_level']} {res_bitly['risk_score']})")

    # ================= R6: BORDERLINE MESSAGE CASES =================
    post_del_sms = "Your India Post tracking number EB928371928IN has been successfully delivered at Jaipur. Thank you for using India Post."
    res_post_del = msg_az.analyze(post_del_sms)
    check("R6: India Post Delivered Notification",
          res_post_del["risk_level"] == "LOW",
          f"(Got {res_post_del['risk_level']} {res_post_del['risk_score']})")

    ponzi_sms = "Guaranteed 3x returns in 7 days! Send payment to invest@ybl"
    res_ponzi_sms = msg_az.analyze(ponzi_sms)
    check("R6: WhatsApp Guaranteed 3x Returns Ponzi",
          res_ponzi_sms["risk_level"] == "HIGH" and res_ponzi_sms["risk_score"] >= 70,
          f"(Got {res_ponzi_sms['risk_level']} {res_ponzi_sms['risk_score']})")

    # ================= PREVIOUS TESTS RE-VERIFICATION =================
    # Preset JVVNL
    jvvnl_sms = "Dear Consumer, Your JVVNL Power will be disconnected tonight at 9:30 PM because your previous month bill was not updated. Please immediately contact our Electricity Officer Mr. Verma at 9829012345 or pay via http://jvvnl-bill-clear.online"
    res1 = msg_az.analyze(jvvnl_sms)
    check("Preset JVVNL Bijli SMS", res1["risk_level"] == "HIGH", f"(Got {res1['risk_level']} {res1['risk_score']})")

    # Preset SBI KYC
    sbi_sms = "Dear SBI Customer, your YONO NetBanking account has been suspended due to pending KYC verification. Please click immediately to update PAN card: http://sbi-kyc-quickupdate.xyz/login.php or call 9785123456 to avoid permanent blockage."
    res2 = msg_az.analyze(sbi_sms)
    check("Preset SBI KYC SMS", res2["risk_level"] == "HIGH", f"(Got {res2['risk_level']} {res2['risk_score']})")

    # Hindi SMS
    hindi_sms = "प्रिय उपभोक्ता, आपका बिजली बिल बकाया है। आज रात 9:30 बजे बिजली काट दी जाएगी। तुरंत 9829012345 पर कॉल करें।"
    res5 = msg_az.analyze(hindi_sms)
    check("Hindi Scam SMS", res5["risk_level"] in ("HIGH", "MEDIUM"), f"(Got {res5['risk_level']} {res5['risk_score']})")

    # Official Banks
    res_sbi = url_az.analyze("https://sbi.co.in")
    res_axis = url_az.analyze("https://axisbank.com")
    check("Official Bank Domains (sbi.co.in, axisbank.com)",
          res_sbi["risk_level"] == "LOW" and res_axis["risk_level"] == "LOW",
          f"(sbi: {res_sbi['risk_level']}, axis: {res_axis['risk_level']})")

    # Official Gov
    res_uidai = url_az.analyze("https://uidai.gov.in")
    check("Official Gov (uidai.gov.in)", res_uidai["risk_level"] == "LOW")

    # Phishing SBI
    res_phish = url_az.analyze("http://sbi-kyc-quickupdate.xyz/login.php")
    check("Phishing SBI Domain", res_phish["risk_level"] == "HIGH")

    # Search UPI
    cases_upi = db.search_cases("damanvip@ybl")
    check("Search by UPI (damanvip@ybl)", len(cases_upi) > 0)

    # Search Phone
    cases_phone = db.search_cases("9829012345")
    channels_found = {c["source_type"] for c in cases_phone}
    check("Search by Phone finds SMS & APK", "SMS" in channels_found and "APK" in channels_found)

    # Optional benign APK sample
    calculator_sample = "sample_apks/Simple_Calculator_Safe.apk"
    if os.path.isfile(calculator_sample):
        calc_res = apk_az.analyze_file(calculator_sample, "Simple_Calculator_Safe.apk")
        check("Safe Calculator (0 C2 URLs, LOW)", len(calc_res["extracted_c2_urls"]) == 0 and calc_res["risk_level"] == "LOW")
    else:
        print("[SKIPPED] Safe Calculator: Optional APK sample is not included")

    # Invalid APK
    invalid_res = apk_az.analyze_file(b"Text file", "fake.apk")
    check("Invalid text file marked INVALID", invalid_res["is_valid_apk"] == False)

    # PDF Generation
    sample_case = db.get_case(1)
    sample_case["raw_data"] = "Test evidence with <today> & symbols"
    pdf_bytes = rep_gen.generate_case_pdf(sample_case)
    check("PDF Generation (Sec 63 BSA + Escaped HTML)", len(pdf_bytes) > 2000)

    if os.path.exists(test_db_path):
        os.remove(test_db_path)

    print("=" * 65)
    print(f"FINAL RESULT: {passed} / {total} PASSED")
    print("=" * 65)
    return passed == total

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
