import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen layout
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # Color Palette - Cyber Police / Defense Theme
    BG_COLOR = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)        # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700
    ACCENT_CYAN = RGBColor(56, 189, 248)  # Cyan 400
    ACCENT_GOLD = RGBColor(251, 191, 36)  # Amber 400
    ACCENT_RED = RGBColor(248, 113, 113)  # Rose 400
    ACCENT_GREEN = RGBColor(74, 222, 128) # Emerald 400
    TEXT_WHITE = RGBColor(248, 250, 252)  # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400
    
    blank_layout = prs.slide_layouts[6]
    
    def set_slide_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg
        
    def add_header(slide, title_text, category_text="RAJASTHAN POLICE ACADEMY (RPA) — R4C CYBER HACKATHON 2026"):
        # Category / Tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN
        
        # Main Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.8))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(26)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_WHITE

    # -------------------------------------------------------------
    # SLIDE 1: TITLE SLIDE
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s1)
    
    # Badge
    badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(5.8), Inches(0.45))
    badge.fill.solid()
    badge.fill.fore_color.rgb = CARD_BG
    badge.line.color.rgb = ACCENT_CYAN
    badge.line.width = Pt(1.5)
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.text = "🛡️ RAJASTHAN POLICE ACADEMY (RPA) • R4C HACKATHON 2026"
    p_b.font.size = Pt(11)
    p_b.font.bold = True
    p_b.font.color.rgb = ACCENT_CYAN
    p_b.alignment = PP_ALIGN.CENTER
    
    # Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.6))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "SurakshaKavach AI (सुरक्षा कवच)"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE
    
    p2 = tf_t.add_paragraph()
    p2.text = "Unified Cyber Threat Triage & Cross-Case Forensic Intelligence Platform"
    p2.font.size = Pt(22)
    p2.font.color.rgb = ACCENT_GOLD
    p2.space_before = Pt(8)
    
    # Subtitle / Problem Statement
    sub_box = s1.shapes.add_textbox(Inches(0.8), Inches(3.6), Inches(11.5), Inches(1.2))
    tf_sub = sub_box.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = "Problem Statement PS01: Scam Message & Phishing Link Detection with Fake Loan / Investment App and Fraudulent Website Analysis"
    p_sub.font.size = Pt(15)
    p_sub.font.color.rgb = TEXT_MUTED
    
    # Metadata Cards (Team, Target Agency, Tech Stack)
    card1 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.0), Inches(3.6), Inches(1.8))
    card1.fill.solid()
    card1.fill.fore_color.rgb = CARD_BG
    card1.line.color.rgb = CARD_BORDER
    tf_c1 = card1.text_frame
    tf_c1.word_wrap = True
    p_c1_title = tf_c1.paragraphs[0]
    p_c1_title.text = "TEAM DETAILS"
    p_c1_title.font.bold = True
    p_c1_title.font.size = Pt(12)
    p_c1_title.font.color.rgb = ACCENT_CYAN
    p_c1_body = tf_c1.add_paragraph()
    p_c1_body.text = "Team: Rakshak\nLead: Bharat\nRole: Cyber Defense & AI Engine"
    p_c1_body.font.size = Pt(13)
    p_c1_body.font.color.rgb = TEXT_WHITE
    p_c1_body.space_before = Pt(6)
    
    card2 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.7), Inches(5.0), Inches(3.6), Inches(1.8))
    card2.fill.solid()
    card2.fill.fore_color.rgb = CARD_BG
    card2.line.color.rgb = CARD_BORDER
    tf_c2 = card2.text_frame
    tf_c2.word_wrap = True
    p_c2_title = tf_c2.paragraphs[0]
    p_c2_title.text = "TARGET AGENCY"
    p_c2_title.font.bold = True
    p_c2_title.font.size = Pt(12)
    p_c2_title.font.color.rgb = ACCENT_GOLD
    p_c2_body = tf_c2.add_paragraph()
    p_c2_body.text = "Rajasthan Police Cyber Crime Cell\nR4C (Rajasthan Center for Cyber Crime)\nI4C & District Cyber PS"
    p_c2_body.font.size = Pt(13)
    p_c2_body.font.color.rgb = TEXT_WHITE
    p_c2_body.space_before = Pt(6)
    
    card3 = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.6), Inches(5.0), Inches(3.9), Inches(1.8))
    card3.fill.solid()
    card3.fill.fore_color.rgb = CARD_BG
    card3.line.color.rgb = CARD_BORDER
    tf_c3 = card3.text_frame
    tf_c3.word_wrap = True
    p_c3_title = tf_c3.paragraphs[0]
    p_c3_title.text = "KEY HIGHLIGHT"
    p_c3_title.font.bold = True
    p_c3_title.font.size = Pt(12)
    p_c3_title.font.color.rgb = ACCENT_GREEN
    p_c3_body = tf_c3.add_paragraph()
    p_c3_body.text = "✓ Zero-False-Positive Whitelist\n✓ Static APK Triad (No Sandbox)\n✓ Sec 63 BSA / Sec 65B Dossier"
    p_c3_body.font.size = Pt(13)
    p_c3_body.font.color.rgb = TEXT_WHITE
    p_c3_body.space_before = Pt(6)

    # Speaker notes for Slide 1
    s1.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Jai Hind Sir / Good morning judges. Hum present kar rahe hain SurakshaKavach AI "
        "jo Rajasthan Police Academy R4C Hackathon 2026 ke PS01 ke liye ek dedicated cyber intelligence platform hai. "
        "Yeh tool police officers ko scam messages, predatory loan APKs aur phishing links ko instant forensic triaging aur court-admissible dossiers me convert karne ki capability deta hai."
    )

    # -------------------------------------------------------------
    # SLIDE 2: THE PROBLEM & GROUND REALITY IN RAJASTHAN
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s2)
    add_header(s2, "The Ground Reality: 4 Major Cyber Syndicates in Rajasthan")
    
    # 4 Threat Cards
    threats = [
        ("⚡ 1. Discom Electricity Scams", 
         "Impersonation of JVVNL / AVVNL / JDVVNL.\n'Your power will be disconnected at 9:30 PM tonight'. Creates severe psychological urgency to click malicious links or dial cyber thug numbers.",
         ACCENT_RED, Inches(0.8), Inches(1.8)),
        ("📱 2. Predatory Loan Extortion APKs", 
         "Untrusted sideloaded APKs (CashSpeed, QuickLoan).\nHarvests Contacts, SMS OTPs, and Camera photos to aggressively blackmail victims and their families without RBI compliance.",
         ACCENT_RED, Inches(6.8), Inches(1.8)),
        ("🏦 3. Banking KYC & Phishing Portals", 
         "SBI YONO, PNB, Post Office KYC alerts.\nLook-alike typosquatted domains (sbi-kyc-quickupdate.xyz) spoofing NetBanking credentials and stealing OTPs.",
         ACCENT_GOLD, Inches(0.8), Inches(4.3)),
        ("🎰 4. Ponzi & Color Prediction Games", 
         "Part-time Telegram tasks, Daman Games, Aviator.\nPromising 10-20% guaranteed daily returns, siphoning citizen funds through layered mule UPI/Bank accounts.",
         ACCENT_GOLD, Inches(6.8), Inches(4.3)),
    ]
    
    for title, desc, accent, left, top in threats:
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(15)
        p_t.font.color.rgb = accent
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_before = Pt(6)

    s2.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Sir, Rajasthan me daily hazaron log 4 main syndicates se target hote hain: "
        "1. JVVNL bijli disconnection ke fake SMS jisme 9:30 PM ka fear trigger hota hai. "
        "2. Chinese predatory loan apps jo contacts chura kar blackmail karti hain. "
        "3. Fake SBI YONO KYC links. 4. Telegram aur Color prediction betting apps. "
        "Sabse badi samasya ye hai ki police stations me ye complaints alag-alag aati hain aur interconnectedness miss ho jaati hai."
    )

    # -------------------------------------------------------------
    # SLIDE 3: THE INVESTIGATIVE BOTTLENECK & OUR SOLUTION
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s3)
    add_header(s3, "The Bottleneck vs. SurakshaKavach AI Unified Paradigm")
    
    # Left Box: The Current Bottleneck
    b_left = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    b_left.fill.solid()
    b_left.fill.fore_color.rgb = CARD_BG
    b_left.line.color.rgb = ACCENT_RED
    b_left.line.width = Pt(1.5)
    tf_l = b_left.text_frame
    tf_l.word_wrap = True
    p_lt = tf_l.paragraphs[0]
    p_lt.text = "❌ CURRENT POLICE BOTTLENECK"
    p_lt.font.bold = True
    p_lt.font.size = Pt(16)
    p_lt.font.color.rgb = ACCENT_RED
    
    points_l = [
        ("Fragmented Complaints: ", "SMS, APK, and URL complaints logged in isolated case dairies across 50+ police districts."),
        ("Slow Dynamic Sandboxes: ", "Dynamic execution takes 10+ minutes and requires costly GPU cloud infrastructure."),
        ("Black-Box AI Trust Deficit: ", "Standard LLMs hallucinate or provide opaque scores inadmissible in trial court."),
        ("Delayed Telecom Requisitions: ", "Manual drafting of Section 91 CrPC notices causes crucial Golden-Hour evidence loss.")
    ]
    for bold_txt, norm_txt in points_l:
        p = tf_l.add_paragraph()
        p.space_before = Pt(12)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ACCENT_RED
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_WHITE
        
    # Right Box: SurakshaKavach Solution
    b_right = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0))
    b_right.fill.solid()
    b_right.fill.fore_color.rgb = CARD_BG
    b_right.line.color.rgb = ACCENT_GREEN
    b_right.line.width = Pt(1.5)
    tf_r = b_right.text_frame
    tf_r.word_wrap = True
    p_rt = tf_r.paragraphs[0]
    p_rt.text = "✅ SURAKSHAKAVACH AI ARCHITECTURE"
    p_rt.font.bold = True
    p_rt.font.size = Pt(16)
    p_rt.font.color.rgb = ACCENT_GREEN
    
    points_r = [
        ("Unified Triage Dashboard: ", "Single forensic engine ingesting SMS, WhatsApp, URLs, APKs, and Websites."),
        ("Sub-Second Static Forensic: ", "Decompiles APK Manifests and DEX strings in <2s without detonating malware."),
        ("Hybrid Explainable AI (Rule + ML): ", "Every risk score is backed by clear, statutory evidence points, not black-box guesses."),
        ("Cross-Case Syndicate Heat-List: ", "Inverted index instantly unmasks repeated phone numbers & UPI IDs across cases."),
        ("1-Click Sec 63 BSA Forensic Dossier: ", "Auto-generates court-ready PDF with SHA-256 hash and Sec 91 CrPC notices.")
    ]
    for bold_txt, norm_txt in points_r:
        p = tf_r.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = "✔ " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = ACCENT_GREEN
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(13)
        r2.font.color.rgb = TEXT_WHITE

    s3.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Yahan hum bottleneck compare karte hain. Currently police ke paas centralized system nahi hai. "
        "Ek district me jo phone number JVVNL scam me use hua, wahi number doosre district me loan app me use hota hai. "
        "SurakshaKavach dono ko unify karta hai, sub-second static analysis karta hai aur 1-click me court-ready dossier deta hai."
    )

    # -------------------------------------------------------------
    # SLIDE 4: SYSTEM ARCHITECTURE & DATA FLOW
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s4)
    add_header(s4, "Technical Architecture: Multi-Modal Forensic Pipeline")
    
    # 4 Horizontal flow steps
    steps = [
        ("Step 1: Input Ingestion", 
         "• SMS / WhatsApp Raw Text\n• Suspicious Phishing URL\n• Android Binary (.apk)\n• Ponzi / Betting Web HTML\n• Multi-lingual (Hindi/Hinglish)",
         ACCENT_CYAN, Inches(0.8), Inches(1.8), Inches(2.7)),
        ("Step 2: Dual AI/ML Analysis", 
         "• Heuristic Rule Urgency Engine\n• Scikit-learn TF-IDF + Logistic ML\n• Static DEX & Manifest Triad\n• Typosquatting & TLD Inspector\n• Ponzi & Mule Bank Scraper",
         ACCENT_GOLD, Inches(3.8), Inches(1.8), Inches(2.8)),
        ("Step 3: Syndicate Correlation", 
         "• Inverted Hash Indexing\n• Recurrent Phone / UPI Linkage\n• Domain Cluster Mapping\n• Real-Time Threat Heat-List\n• Zero-False-Positive Whitelist",
         ACCENT_CYAN, Inches(6.9), Inches(1.8), Inches(2.7)),
        ("Step 4: Actionable Output", 
         "• High / Med / Low Risk Card\n• Extracted IOC Registry Table\n• Interactive Cross-Link Modal\n• Section 63 BSA Forensic PDF\n• Sec 91 CrPC Draft Notice",
         ACCENT_GREEN, Inches(9.9), Inches(1.8), Inches(2.6))
    ]
    
    for st_title, st_desc, accent, left, top, width in steps:
        card = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, Inches(4.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = st_title
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = accent
        p_d = tf.add_paragraph()
        p_d.text = st_desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_before = Pt(10)

    s4.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Yeh hamara complete data pipeline hai: Ingestion -> Dual Heuristic + ML Engine -> "
        "Correlation Inverted Index -> Section 63 BSA Output. "
        "Har step transparent hai aur police officer ko exact reasons batata hai ki risk score kyun generate hua."
    )

    # -------------------------------------------------------------
    # SLIDE 5: MODULE SPOTLIGHT - STATIC APK & THE EXTORTION TRIAD
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s5)
    add_header(s5, "Deep Dive: Static Android Decompilation & The Extortion Triad")
    
    # Left Card: Extortion Triad
    c_triad = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c_triad.fill.solid()
    c_triad.fill.fore_color.rgb = CARD_BG
    c_triad.line.color.rgb = ACCENT_RED
    c_triad.line.width = Pt(1.5)
    tf_tr = c_triad.text_frame
    tf_tr.word_wrap = True
    p_trt = tf_tr.paragraphs[0]
    p_trt.text = "🎯 THE EXTORTION TRIAD SIGNATURE"
    p_trt.font.bold = True
    p_trt.font.size = Pt(16)
    p_trt.font.color.rgb = ACCENT_RED
    
    triad_desc = (
        "Predatory Instant Loan Apps (e.g. CashSpeed) deceive victims by promising instant cash, but their true mission is extortion.\n\n"
        "Our static analyzer inspects AndroidManifest.xml for the lethal combination:\n"
        "1. android.permission.READ_CONTACTS\n"
        "   → Steals complete phone book of family, friends & employers.\n"
        "2. android.permission.READ_SMS\n"
        "   → Intercepts bank balance OTPs and personal financial data.\n"
        "3. android.permission.CAMERA / READ_STORAGE\n"
        "   → Harvests private gallery photos for morphing and harassment.\n\n"
        "⚖️ Result: Triggered as 'CRITICAL EXTORTION SPYWARE PROFILE' (Score: 100/100) instantly without opening or running the APK."
    )
    p_trd = tf_tr.add_paragraph()
    p_trd.text = triad_desc
    p_trd.font.size = Pt(12)
    p_trd.font.color.rgb = TEXT_WHITE
    p_trd.space_before = Pt(8)
    
    # Right Card: DEX Bytecode Mining
    c_dex = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0))
    c_dex.fill.solid()
    c_dex.fill.fore_color.rgb = CARD_BG
    c_dex.line.color.rgb = ACCENT_CYAN
    c_dex.line.width = Pt(1.5)
    tf_dx = c_dex.text_frame
    tf_dx.word_wrap = True
    p_dxt = tf_dx.paragraphs[0]
    p_dxt.text = "🔍 DEX BYTECODE & C2 MINING (NO SANDBOX)"
    p_dxt.font.bold = True
    p_dxt.font.size = Pt(16)
    p_dxt.font.color.rgb = ACCENT_CYAN
    
    dex_desc = (
        "Standard sandboxes fail because malware uses anti-emulator evasion techniques.\n\n"
        "SurakshaKavach parses classes.dex bytecode and raw string pool directly using Androguard:\n\n"
        "• Hardcoded C2 Callback Endpoints:\n"
        "  Extracted: http://api.cashspeed-loan-app.xyz/sync_data\n"
        "• Suspect Recovery Numbers:\n"
        "  Extracted: +91 9829012345 (Embedded in recovery intent triggers)\n"
        "• Repayment UPI Destination:\n"
        "  Extracted: cashspeed.recovery@okhdfcbank\n\n"
        "⚡ Police Benefit: Instant IOCs available for SIM deactivation and payment freeze before victim data is even leaked!"
    )
    p_dxd = tf_dx.add_paragraph()
    p_dxd.text = dex_desc
    p_dxd.font.size = Pt(12)
    p_dxd.font.color.rgb = TEXT_WHITE
    p_dxd.space_before = Pt(8)

    s5.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Judges ko batayein ki humne bina sandbox ke static analysis kyun chuna. "
        "Dynamic sandboxes 10 minute lete hain aur malware emulator detect karke sleep ho jata hai. "
        "Hum Androguard se Manifest me 'Extortion Triad' (Contacts + SMS + Camera) detect karte hain aur DEX bytecode se hardcoded C2 URL aur recovery phone numbers 2 second me nikal lete hain."
    )

    # -------------------------------------------------------------
    # SLIDE 6: MODULE SPOTLIGHT - CROSS-CASE CORRELATION & HEATLIST
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s6)
    add_header(s6, "Unmasking Organized Syndicates: Cross-Case Correlation Engine")
    
    # Big Top Card: How it works
    c_synd = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(2.2))
    c_synd.fill.solid()
    c_synd.fill.fore_color.rgb = CARD_BG
    c_synd.line.color.rgb = ACCENT_GOLD
    c_synd.line.width = Pt(1.5)
    tf_syn = c_synd.text_frame
    tf_syn.word_wrap = True
    p_st = tf_syn.paragraphs[0]
    p_st.text = "🕸️ INVERTED INDEX ENTITY RESOLUTION GRAPH"
    p_st.font.bold = True
    p_st.font.size = Pt(16)
    p_st.font.color.rgb = ACCENT_GOLD
    p_sd = tf_syn.add_paragraph()
    p_sd.text = (
        "Fraudsters operate across multiple formats (a phishing SMS in the morning, a loan app extortion in the evening). "
        "SurakshaKavach normalizes every extracted Phone Number, UPI ID, and Domain into an inverted index database. "
        "When a new complaint is filed, the system instantly traces back all previous incidents sharing the same infrastructure."
    )
    p_sd.font.size = Pt(13)
    p_sd.font.color.rgb = TEXT_WHITE
    p_sd.space_before = Pt(6)
    
    # 2 Bottom Columns: Real Proven Linkage + Threat Heat-List
    c_l1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.3), Inches(5.7), Inches(2.6))
    c_l1.fill.solid()
    c_l1.fill.fore_color.rgb = CARD_BG
    c_l1.line.color.rgb = ACCENT_CYAN
    c_l1.line.width = Pt(1.5)
    tf_l1 = c_l1.text_frame
    tf_l1.word_wrap = True
    p_l1_t = tf_l1.paragraphs[0]
    p_l1_t.text = "🔗 Verified Linkage Example in Our System"
    p_l1_t.font.bold = True
    p_l1_t.font.size = Pt(14)
    p_l1_t.font.color.rgb = ACCENT_CYAN
    p_l1_b = tf_l1.add_paragraph()
    p_l1_b.text = (
        "• Case #1: JVVNL Power Disconnection Fake SMS\n"
        "  Suspect Contact: +91 9829012345\n"
        "• Case #2: CashSpeed Loan Extortion App (.apk)\n"
        "  Hardcoded C2 Recovery: +91 9829012345\n\n"
        "🚨 System Action: Cross-links both cases instantly! IO opens modal and sees the organized Mewat/Alwar syndicate pattern."
    )
    p_l1_b.font.size = Pt(12)
    p_l1_b.font.color.rgb = TEXT_WHITE
    p_l1_b.space_before = Pt(6)
    
    c_l2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(4.3), Inches(5.7), Inches(2.6))
    c_l2.fill.solid()
    c_l2.fill.fore_color.rgb = CARD_BG
    c_l2.line.color.rgb = ACCENT_GREEN
    c_l2.line.width = Pt(1.5)
    tf_l2 = c_l2.text_frame
    tf_l2.word_wrap = True
    p_l2_t = tf_l2.paragraphs[0]
    p_l2_t.text = "🔥 Dynamic Threat Heat-List (Actionable Intel)"
    p_l2_t.font.bold = True
    p_l2_t.font.size = Pt(14)
    p_l2_t.font.color.rgb = ACCENT_GREEN
    p_l2_b = tf_l2.add_paragraph()
    p_l2_b.text = (
        "• Maintains real-time frequency score across all districts.\n"
        "• Top Suspect Phone Leaderboard for bulk DoT / Sanchar Saathi blocking.\n"
        "• Top Mule UPI & Bank Leaderboard for NPCI / 1930 freeze.\n"
        "• Top Phishing Domains for CERT-In / NCIIPC DNS sinkholing."
    )
    p_l2_b.font.size = Pt(12)
    p_l2_b.font.color.rgb = TEXT_WHITE
    p_l2_b.space_before = Pt(6)

    s6.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Yeh hamara sabse bada competitive edge hai! Fraudsters infrastructure recycle karte hain. "
        "Hamara system JVVNL SMS ke phone number 9829012345 ko CashSpeed loan app ke recovery contact se match kar deta hai. "
        "Police officer ko turant pata chal jata hai ki ye akela case nahi balki organized syndicate hai."
    )

    # -------------------------------------------------------------
    # SLIDE 7: STATUTORY COMPLIANCE & SECTION 63 BSA / 65B IEA
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s7)
    add_header(s7, "Judicial Admissibility: Section 63 BSA (65B IEA) & Sec 91 CrPC")
    
    # 3 Pillar Cards
    pills = [
        ("⚖️ Section 63 BSA 2023\n(Formerly Sec 65B IEA)",
         "• Automated Electronic Record Certificate.\n• Certified date, time, and hash manifest.\n• Removes procedural objections during courtroom trials.\n• Complies with modern Bharatiya Sakshya Adhiniyam standards.",
         ACCENT_CYAN, Inches(0.8)),
        ("🔒 SHA-256 Cryptographic\nEvidence Integrity",
         "• Generates unique SHA-256 digest of original input (SMS, APK hash, URL).\n• Guarantees non-repudiation in chain of custody.\n• Prevents defense lawyers from claiming evidence tampering.",
         ACCENT_GOLD, Inches(4.7)),
        ("📜 Section 91 CrPC / Sec 94 BNSS\nAutomated Requisition Notice",
         "• Auto-drafts legal notice to Telecom Service Providers (Airtel/Jio) for CDR/SDR.\n• Auto-drafts freeze requisition to Banks/NPCI for mule UPI IDs.\n• Saves 4-6 hours of manual paper drafting.",
         ACCENT_GREEN, Inches(8.6))
    ]
    
    for p_title, p_desc, accent, left in pills:
        card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.8), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = p_title
        p_t.font.bold = True
        p_t.font.size = Pt(15)
        p_t.font.color.rgb = accent
        p_d = tf.add_paragraph()
        p_d.text = p_desc
        p_d.font.size = Pt(13)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_before = Pt(12)

    s7.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Naye criminal laws (BSA 2023 aur BNSS 2023) ke tahat electronic evidence ko court me prove karna critical hai. "
        "Hamara system 1-click me Section 63 BSA certified PDF generate karta hai jisme SHA-256 cryptographic hash hota hai. "
        "Saath hi Section 91 CrPC notice pre-draft ho jata hai jisse IO turant telecom aur banks ko freeze notice bhej sake."
    )

    # -------------------------------------------------------------
    # SLIDE 8: VERIFICATION, TESTING & BENCHMARKS
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s8)
    add_header(s8, "Rigorous Verification: 16/16 Acceptance Tests Passed")
    
    # 4 Metric Cards
    metrics = [
        ("16 / 16", "ACCEPTANCE TESTS PASSED", "All core forensic, ML & correlation suites verified", ACCENT_GREEN, Inches(0.8), Inches(1.8)),
        ("0.0%", "FALSE POSITIVE RATE", "Gov (.gov.in/.nic.in) & Banks (sbi.co.in) 100% Whitelisted", ACCENT_CYAN, Inches(3.8), Inches(1.8)),
        ("< 1.8s", "STATIC DECOMPILATION TIME", "Ultra-fast APK manifest & DEX string analysis without sandbox", ACCENT_GOLD, Inches(6.8), Inches(1.8)),
        ("100%", "BSA 2023 COMPLIANCE", "Automated Section 63 hash generation & court-ready PDF output", ACCENT_CYAN, Inches(9.8), Inches(1.8)),
    ]
    
    for val, lbl, sub, accent, left, top in metrics:
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(2.7), Inches(2.0))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p_v = tf.paragraphs[0]
        p_v.text = val
        p_v.font.bold = True
        p_v.font.size = Pt(28)
        p_v.font.color.rgb = accent
        p_v.alignment = PP_ALIGN.CENTER
        p_l = tf.add_paragraph()
        p_l.text = lbl
        p_l.font.bold = True
        p_l.font.size = Pt(11)
        p_l.font.color.rgb = TEXT_WHITE
        p_l.alignment = PP_ALIGN.CENTER
        p_l.space_before = Pt(4)
        p_s = tf.add_paragraph()
        p_s.text = sub
        p_s.font.size = Pt(10)
        p_s.font.color.rgb = TEXT_MUTED
        p_s.alignment = PP_ALIGN.CENTER
        p_s.space_before = Pt(4)
        
    # Table of verified test cases
    table_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(4.1), Inches(11.7), Inches(2.7))
    table_card.fill.solid()
    table_card.fill.fore_color.rgb = CARD_BG
    table_card.line.color.rgb = CARD_BORDER
    tf_tb = table_card.text_frame
    tf_tb.word_wrap = True
    p_tbt = tf_tb.paragraphs[0]
    p_tbt.text = "📋 KEY VERIFIED TEST SCENARIOS (EVIDENCE-BACKED)"
    p_tbt.font.bold = True
    p_tbt.font.size = Pt(13)
    p_tbt.font.color.rgb = ACCENT_GOLD
    
    rows = (
        "✔ Test 1: JVVNL Power Disconnection Scam SMS → Detected Urgency (HIGH 88), Extracted Phone & URL, ML Score: 91%\n"
        "✔ Test 2: Devanagari Hindi Electricity SMS → Correct Hindi linguistic parsing, Urgency detected, HIGH RISK (70)\n"
        "✔ Test 3: SBI Typosquatted Domain (sbi-kyc-quickupdate.xyz) → Detected Brand spoofing + Dangerous TLD (100)\n"
        "✔ Test 4: Official SBI Domain (sbi.co.in / uidai.gov.in) → Zero False Positive verified, Risk: 0 (LOW)\n"
        "✔ Test 5: CashSpeed Predatory APK → Extortion Triad triggered (100), Hardcoded C2 & Phone extracted\n"
        "✔ Test 6: Cross-Case Syndicate Linkage → Successfully linked JVVNL SMS to CashSpeed APK via Phone 9829012345"
    )
    p_tbb = tf_tb.add_paragraph()
    p_tbb.text = rows
    p_tbb.font.size = Pt(11)
    p_tbb.font.color.rgb = TEXT_WHITE
    p_tbb.space_before = Pt(6)

    s8.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Sir, hamara project sirf prototype nahi hai, 16 out of 16 automated acceptance tests pass ho chuke hain. "
        "Isme zero false positive rate hai official gov aur bank portals par. Aur static decompilation time 2 second se kam hai."
    )

    # -------------------------------------------------------------
    # SLIDE 9: LIVE DEMO & JUDGE WALKTHROUGH
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s9)
    add_header(s9, "2-Minute Live Demonstration Walkthrough")
    
    demo_cards = [
        ("Step 1: SMS Triaging", 
         "1. Click '⚡ JVVNL Electricity Bill Scam'\n2. Click 'Run Forensic Triaging'\n3. Observe: HIGH RISK (88/100), Urgency detected, ML Model: 91%, Phone & Link extracted.",
         ACCENT_CYAN, Inches(0.8), Inches(1.8)),
        ("Step 2: Dual Domain Test", 
         "1. Test 'sbi-kyc-quickupdate.xyz' → Flags 100/100 Phishing.\n2. Test official 'sbi.co.in' → Scores 0/100 Verified Official Brand (Zero False Positive proof).",
         ACCENT_GOLD, Inches(6.8), Inches(1.8)),
        ("Step 3: APK Static Forensics", 
         "1. Select '🚨 CashSpeed Loan Spyware APK'\n2. Static analyzer reveals Extortion Triad (Contacts + SMS + Camera) and C2 endpoints without running malware.",
         ACCENT_RED, Inches(0.8), Inches(4.3)),
        ("Step 4: Syndicate & PDF Export", 
         "1. Open Investigation Dossier tab.\n2. Click on case to see cross-link modal (+91 9829012345 linked across SMS & APK).\n3. Click '📄 PDF' to export Section 63 BSA dossier.",
         ACCENT_GREEN, Inches(6.8), Inches(4.3)),
    ]
    
    for title, desc, accent, left, top in demo_cards:
        card = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(15)
        p_t.font.color.rgb = accent
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_before = Pt(6)

    s9.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Demo ke time screen par 4 steps dikhayenge: "
        "Pehle JVVNL scam SMS test karenge, fir fake domain vs real sbi.co.in dikhayenge, fir CashSpeed loan APK ka Extortion Triad dikhayenge, "
        "aur end me Investigation Dossier me cross-link modal aur Section 63 BSA certified PDF download karke dikhayenge."
    )

    # -------------------------------------------------------------
    # SLIDE 10: IMPACT, ROADMAP & CONCLUSION
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_bg(s10)
    add_header(s10, "Impact, Operational Roadmap & Vision for Rajasthan Police")
    
    # 3 Horizontal Strategy Cards
    strats = [
        ("🚀 Deployment with 1930 & CCTNS", 
         "• Direct API integration with NCRP 1930 portal.\n• Automated ingestion of incoming citizen SMS complaints.\n• Auto-tagging of repeated syndicated threats across district cyber cells.\n• Integration with Chakshu (DoT) for instant SIM disconnection.",
         ACCENT_CYAN, Inches(0.8)),
        ("📲 Citizen WhatsApp Verification Bot", 
         "• Citizens forward suspicious SMS or APK before clicking or installing.\n• Instant 'Safe / Danger' reply with explainable reason in Hindi/Marwari.\n• Nips the fraud at the inception before money is deducted.",
         ACCENT_GOLD, Inches(4.7)),
        ("🏛️ Statewide Cyber Command Heat-Map", 
         "• Centralized R4C dashboard for SPs & IGs showing active mule networks in Mewat/Alwar.\n• Automated bulk Section 91 CrPC requisition generation.\n• Strengthens prosecution conviction rate under IT Act & BNS.",
         ACCENT_GREEN, Inches(8.6)),
    ]
    
    for s_title, s_desc, accent, left in strats:
        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, Inches(1.8), Inches(3.8), Inches(3.8))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p_t = tf.paragraphs[0]
        p_t.text = s_title
        p_t.font.bold = True
        p_t.font.size = Pt(14)
        p_t.font.color.rgb = accent
        p_d = tf.add_paragraph()
        p_d.text = s_desc
        p_d.font.size = Pt(12)
        p_d.font.color.rgb = TEXT_WHITE
        p_d.space_before = Pt(8)
        
    # Closing Banner
    banner = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1.0))
    banner.fill.solid()
    banner.fill.fore_color.rgb = CARD_BG
    banner.line.color.rgb = ACCENT_CYAN
    tf_bn = banner.text_frame
    tf_bn.word_wrap = True
    p_bnt = tf_bn.paragraphs[0]
    p_bnt.text = "SURAKSHAKAVACH AI: PROTECTING CITIZENS • EMPOWERING INVESTIGATORS • SECURING RAJASTHAN"
    p_bnt.font.bold = True
    p_bnt.font.size = Pt(14)
    p_bnt.font.color.rgb = ACCENT_CYAN
    p_bnt.alignment = PP_ALIGN.CENTER
    p_bnb = tf_bn.add_paragraph()
    p_bnb.text = "Team Rakshak | Thank You Judges & Rajasthan Police Academy | Open for Q&A"
    p_bnb.font.size = Pt(12)
    p_bnb.font.color.rgb = TEXT_WHITE
    p_bnb.alignment = PP_ALIGN.CENTER
    p_bnb.space_before = Pt(4)

    s10.notes_slide.notes_text_frame.text = (
        "Hindi Speaker Notes: Conclusion me batayein: SurakshaKavach sirf hackathon project nahi, balki Rajasthan Police ke 1930 NCRP portal aur citizen WhatsApp bot ke sath directly plug ho sakta hai. "
        "Yeh Rajasthan Police ko proactive cyber defense aur high conviction rate deta hai. Thank you judges, Jai Hind!"
    )

    output_path = "/mnt/c/Users/dell/OneDrive/Desktop/HACKTHON/SurakshaKavach_AI_Presentation.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
