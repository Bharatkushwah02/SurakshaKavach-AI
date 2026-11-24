import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def generate_action_plan_pdf(output_filename="SURAKSHAKAVACH_ACTION_PLAN_RPA_2026.pdf"):
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        alignment=1 # Center
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#1E3A8A'),
        alignment=1
    )
    h1_style = ParagraphStyle(
        'DocH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        spaceBefore=12,
        spaceAfter=5
    )
    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#0F172A'),
        spaceBefore=8,
        spaceAfter=3
    )
    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#334155')
    )
    bullet_style = ParagraphStyle(
        'DocBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#1E293B'),
        leftIndent=15
    )
    callout_style = ParagraphStyle(
        'DocCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#0369A1')
    )

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    story = []

    # Title & Subtitle Banner
    story.append(Paragraph("RAJASTHAN POLICE ACADEMY (RPA), JAIPUR", subtitle_style))
    story.append(Paragraph("CYBER SECURITY HACKATHON 2026 (R4C)", subtitle_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("SURAKSHAKAVACH AI (सुरक्षा कवच)", title_style))
    story.append(Paragraph("Unified Phishing, Malicious APK & Fraud Infrastructure Triage Platform", subtitle_style))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=10))

    # Proposal Metadata Block
    meta_data = [
        [
            Paragraph("<b>Problem Statement:</b> PS01 (Cyber Fraud / Phishing / Malicious Apps)", body_style),
            Paragraph("<b>Target Agency:</b> Rajasthan Police Cyber Crime Cell / I4C", body_style)
        ],
        [
            Paragraph("<b>Project Title:</b> SurakshaKavach AI", body_style),
            Paragraph("<b>Core Focus:</b> Explainable AI, APK Forensics & Entity Graph", body_style)
        ],
        [
            Paragraph("<b>Legal Alignment:</b> Sec 65B IEA / Sec 63 BSA & IT Act Sec 66D", body_style),
            Paragraph("<b>Deployment Readiness:</b> Working MVP / TRL-6 Prototype Ready", body_style)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[265, 265])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 1. Executive Summary
    story.append(Paragraph("1. EXECUTIVE SUMMARY & GROUND PROBLEM", h1_style))
    story.append(Paragraph(
        "Across Rajasthan and northern India, cyber financial fraud is driven primarily by four converged syndicates: (a) <b>Electricity Bill Disconnection Scams</b> impersonating state discoms (JVVNL, AVVNL, JDVVNL), (b) <b>Predatory Chinese Loan App Spyware</b> that harvest victim contacts and camera images for extortion, (c) <b>Banking KYC Suspensions</b> spoofing SBI/PNB netbanking, and (d) <b>Telegram/WhatsApp Part-Time Job and Illegal Color Prediction Betters</b>. "
        "Currently, these threats are logged as fragmented, isolated complaints across police stations. Fraudsters exploit this by recycling the same virtual numbers, mule UPI IDs, and disposable cloud infrastructure across multiple campaigns. "
        "<b>SurakshaKavach AI</b> solves this by delivering a unified, explainable threat triage platform that ingests suspicious text messages, URLs, Android APK binaries, and website content to immediately calculate explainable risk scores, isolate actionable Indicators of Compromise (IOCs), link recurring syndicates on an entity graph, and generate court-admissible Section 65B forensic dossiers.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # 2. Key Modules & Architecture
    story.append(Paragraph("2. SYSTEM ARCHITECTURE & CORE CAPABILITIES", h1_style))
    modules_data = [
        [Paragraph("<b>Forensic Module</b>", body_style), Paragraph("<b>Technical Mechanism</b>", body_style), Paragraph("<b>Key Output for Police</b>", body_style)],
        [
            Paragraph("<b>SMS / Message Analyzer</b>", body_style),
            Paragraph("Context-aware heuristic NLP detecting psychological urgency levers ('tonight at 9:30 PM', 'within 2 hours') and institution impersonation (JVVNL, SBI, India Post).", body_style),
            Paragraph("Urgency score (0-100), impersonation flags, extracted suspect phone numbers & unshortened URLs.", body_style)
        ],
        [
            Paragraph("<b>Phishing URL Inspector</b>", body_style),
            Paragraph("Typosquatting/look-alike domain analysis, disposable TLD inspection (.xyz, .top, .cc), unencrypted HTTP flags, direct IP hosting checks, and CERT-In/I4C blacklist matching.", body_style),
            Paragraph("Domain classification, registration anomalies, deceptive brand attribution, and victim warning.", body_style)
        ],
        [
            Paragraph("<b>Static APK Extortion Engine</b>", body_style),
            Paragraph("Safe, non-detonation static inspection decompiling AndroidManifest.xml and DEX bytecode. Detects predatory loan spyware profiles (READ_CONTACTS + READ_SMS + CAMERA).", body_style),
            Paragraph("Package SHA256, dangerous permission breakdown, hardcoded C2 backend URLs, and mule recovery numbers.", body_style)
        ],
        [
            Paragraph("<b>Ponzi & Betting Scanner</b>", body_style),
            Paragraph("Heuristic linguistic parser detecting MLM bonus hierarchies, guaranteed daily returns, color prediction triggers (Daman, 91Club), and payment destination harvesting.", body_style),
            Paragraph("Extracted mule UPI IDs, bank accounts, IFSC codes, crypto TRC-20/ETH addresses, and WhatsApp redirects.", body_style)
        ],
        [
            Paragraph("<b>Syndicate Entity Graph & Heat-List</b>", body_style),
            Paragraph("Cross-threat relational index linking phones, UPIs, and domains across unrelated complaints to uncover organized cybercrime syndicates.", body_style),
            Paragraph("Live heat-list of top offending numbers, domains, and payment handles for automated 1930 NCRP flagging.", body_style)
        ]
    ]
    mod_table = Table(modules_data, colWidths=[130, 240, 160])
    mod_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(mod_table)
    story.append(Spacer(1, 8))

    # 3. Explainability & Zero-False Positive Philosophy
    story.append(Paragraph("3. EXPLAINABILITY & LAW ENFORCEMENT COMPLIANCE", h1_style))
    story.append(Paragraph(
        "<b>1. Zero 'Black-Box' Decision Making:</b> Black-box AI models that merely output a percentage probability without transparent reasons are inadmissible in court. SurakshaKavach AI provides human-readable justification bullets (e.g. <i>'Impersonates JVVNL Discom' + 'Artificial time pressure: tonight 9:30 PM' + 'Disposable domain .online'</i>).",
        bullet_style
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>2. Section 65B Indian Evidence Act / Section 63 BSA Certification:</b> Every analysis automatically formats an investigation report complete with cryptographic hash (SHA-256), UTC/IST timestamps, and structured evidence references ready for charge sheet annexures.",
        bullet_style
    ))
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<b>3. Actionable Notice Generation:</b> Pre-drafts requisition templates under Section 91 CrPC / Section 94 BNSS for Telecom Service Providers (TSPs) and Section 69A IT Act emergency takedowns to CERT-In/NIXI.",
        bullet_style
    ))
    story.append(Spacer(1, 8))

    # 4. Tech Stack & Implementation Roadmap (24-Hour Final at RPA)
    story.append(Paragraph("4. TECHNOLOGY STACK & 24-HOUR HACKATHON ROADMAP", h1_style))
    story.append(Paragraph(
        "<b>Backend & Forensics:</b> Python 3, Flask, BeautifulSoup4, TLDExtract, ZipFile Binary Parsers, ReportLab Forensic Engine.<br/>"
        "<b>Database & Linking:</b> SQLite / PostgreSQL relational entity graph with inverted indexing on IOC hashes.<br/>"
        "<b>Frontend:</b> Responsive Cyber Command UI built on Tailwind CSS, FontAwesome, Chart.js, and Lucide Icons.",
        body_style
    ))
    story.append(Spacer(1, 5))

    roadmap_data = [
        [Paragraph("<b>Time Phase</b>", body_style), Paragraph("<b>24-Hour Final Deliverables at RPA, Jaipur</b>", body_style)],
        [Paragraph("<b>Hours 01 – 04</b>", body_style), Paragraph("Ingest R4C official sample datasets (real scam SMS, test APKs, fraudulent URLs). Calibrate heuristic weights to sample ground truth.", body_style)],
        [Paragraph("<b>Hours 05 – 10</b>", body_style), Paragraph("Enhance multi-layer entity graph correlation (Neo4j / NetworkX graph visualization showing interconnected cyber gangs).", body_style)],
        [Paragraph("<b>Hours 11 – 16</b>", body_style), Paragraph("Integrate citizen report intake widget and automated WhatsApp/Telegram alert bot forwarding suspicious links directly to cyber police.", body_style)],
        [Paragraph("<b>Hours 17 – 20</b>", body_style), Paragraph("Conduct rigorous end-to-end stress testing with edge cases (Hindi/Hinglish slang messages, obfuscated APK Dex files).", body_style)],
        [Paragraph("<b>Hours 21 – 24</b>", body_style), Paragraph("Finalize live command dashboard presentation, Section 65B automated dossier verification, and jury demonstration.", body_style)]
    ]
    road_table = Table(roadmap_data, colWidths=[120, 410])
    road_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(road_table)
    story.append(Spacer(1, 10))

    # Footer Sign-off
    story.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#94A3B8'), spaceAfter=5))
    story.append(Paragraph("<b>SURAKSHAKAVACH AI — INNOVATE • SECURE • EMPOWER | RAJASTHAN POLICE ACADEMY 2026</b>", subtitle_style))

    doc.build(story)
    print(f"Action plan PDF generated successfully at: {output_filename}")

if __name__ == '__main__':
    generate_action_plan_pdf()
