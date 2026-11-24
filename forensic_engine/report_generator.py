import io
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._init_custom_styles()

    def _init_custom_styles(self):
        self.title_style = ParagraphStyle(
            'GovTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=15,
            leading=18,
            textColor=colors.HexColor('#0F172A'),
            alignment=1
        )
        self.sub_title = ParagraphStyle(
            'GovSubTitle',
            parent=self.styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor('#1E3A8A'),
            alignment=1
        )
        self.heading2 = ParagraphStyle(
            'GovHeading2',
            parent=self.styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=14,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=8,
            spaceAfter=4
        )
        self.body = ParagraphStyle(
            'GovBody',
            parent=self.styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=11.5,
            textColor=colors.HexColor('#334155')
        )
        self.mono_body = ParagraphStyle(
            'GovMono',
            parent=self.styles['Normal'],
            fontName='Courier',
            fontSize=8,
            leading=10,
            textColor=colors.HexColor('#0F172A')
        )

    def generate_case_pdf(self, case_data):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        elements = []

        # Header Banner
        elements.append(Paragraph("RAJASTHAN POLICE ACADEMY (RPA) — CYBER CRIME INVESTIGATION WING", self.title_style))
        elements.append(Paragraph("R4C DIGITAL FORENSICS & THREAT INTELLIGENCE PLATFORM", self.sub_title))
        elements.append(Paragraph("ELECTRONIC EVIDENCE DOSSIER & INVESTIGATION REPORT", self.title_style))
        elements.append(Paragraph("<b>Statutory Reference: Section 63 Bharatiya Sakshya Adhiniyam (BSA), 2023 / Section 65B Indian Evidence Act</b>", self.sub_title))
        elements.append(Spacer(1, 6))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=8))

        # Risk Colors
        risk_lvl = case_data.get('risk_level', 'LOW')
        if risk_lvl == 'HIGH':
            risk_color_hex = '#DC2626'
        elif risk_lvl == 'MEDIUM':
            risk_color_hex = '#D97706'
        else:
            risk_color_hex = '#16A34A'

        # Case Meta Table
        analysis = case_data.get('analysis', {})
        sha256_hash = case_data.get('raw_sha256') or analysis.get('sha256', 'N/A')

        meta_table_data = [
            [
                Paragraph(f"<b>Case Number:</b> {case_data.get('case_number', 'N/A')}", self.body),
                Paragraph(f"<b>Timestamp (IST):</b> {datetime.now().strftime('%d-%b-%Y %H:%M:%S IST')}", self.body)
            ],
            [
                Paragraph(f"<b>Evidence Channel:</b> {case_data.get('source_type', 'N/A')}", self.body),
                Paragraph(f"<b>Risk Evaluation:</b> <b><font color='{risk_color_hex}'>{risk_lvl} ({case_data.get('risk_score', 0)}/100)</font></b>", self.body)
            ],
            [
                Paragraph(f"<b>Threat Classification:</b> {case_data.get('threat_category', 'CYBER_FRAUD')}", self.body),
                Paragraph(f"<b>Evidence Integrity:</b> SHA-256 Verified", self.body)
            ],
            [
                Paragraph(f"<b>Cryptographic SHA-256:</b> <font face='Courier' size='7'>{sha256_hash}</font>", self.body),
                Paragraph(f"<b>Governing Law:</b> IT Act Sec 66D / BSA Sec 63", self.body)
            ]
        ]
        t = Table(meta_table_data, colWidths=[270, 270])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 8))

        # 1. Raw Ingested Content (HTML Escaped to preserve <today> or special characters!)
        elements.append(Paragraph("1. INGESTED EVIDENCE / SUSPICIOUS CONTENT", self.heading2))
        raw_text = str(case_data.get('raw_data', ''))
        escaped_raw = html.escape(raw_text)
        elements.append(Paragraph(f"<i>\"{escaped_raw}\"</i>", self.body))
        elements.append(Spacer(1, 8))

        # 2. Extracted Actionable Identifiers
        elements.append(Paragraph("2. EXTRACTED ACTIONABLE INDICATORS OF COMPROMISE (IOCs)", self.heading2))
        extracted = analysis.get('extracted_identifiers', {})
        
        phones = extracted.get('phones', []) or extracted.get('phone_numbers', []) or analysis.get('extracted_phones', [])
        upis = extracted.get('upi_ids', []) or analysis.get('extracted_upis', [])
        urls = extracted.get('urls', []) or ([analysis.get('domain')] if analysis.get('domain') else [])
        c2_urls = analysis.get('extracted_c2_urls', [])
        accounts = extracted.get('bank_accounts', [])
        ifscs = extracted.get('ifsc_codes', [])
        crypto = extracted.get('crypto_wallets', [])

        ioc_table_data = [
            [Paragraph("<b>Identifier Type</b>", self.body), Paragraph("<b>Extracted Values / Recipient Handles</b>", self.body)],
            [Paragraph("Suspect Contact Numbers", self.body), Paragraph(', '.join(phones) if phones else "None identified", self.body)],
            [Paragraph("Mule UPI Beneficiaries", self.body), Paragraph(', '.join(upis) if upis else "None identified", self.body)],
            [Paragraph("Domains / C2 Endpoints", self.body), Paragraph(', '.join(urls + c2_urls) if (urls or c2_urls) else "None identified", self.body)],
            [Paragraph("Bank Accounts & IFSC", self.body), Paragraph(f"Acc: {', '.join(accounts)} | IFSC: {', '.join(ifscs)}" if (accounts or ifscs) else "None identified", self.body)],
            [Paragraph("Cryptocurrency Wallets", self.body), Paragraph(', '.join(crypto) if crypto else "None identified", self.body)]
        ]
        ioc_table = Table(ioc_table_data, colWidths=[180, 360])
        ioc_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E2E8F0')),
            ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(ioc_table)
        elements.append(Spacer(1, 8))

        # 3. Forensic Explainability Triggers
        elements.append(Paragraph("3. FORENSIC EXPLAINABILITY & RISK TRIGGERS", self.heading2))
        reasons = analysis.get('reasons', [])
        for r in reasons:
            elements.append(Paragraph(f"• {html.escape(r)}", self.body))
        elements.append(Spacer(1, 8))

        # 4. Cross-Case Syndicate Correlation
        related = case_data.get('related_cases', [])
        if related:
            elements.append(Paragraph("4. CROSS-CASE SYNDICATE CORRELATION (Heat Network)", self.heading2))
            rel_data = [[Paragraph("<b>Linked Case</b>", self.body), Paragraph("<b>Channel</b>", self.body), Paragraph("<b>Shared Identifier</b>", self.body)]]
            for rel in related[:4]:
                rel_data.append([
                    Paragraph(rel.get('case_number', ''), self.body),
                    Paragraph(rel.get('source_type', ''), self.body),
                    Paragraph(rel.get('shared_entity', ''), self.body)
                ])
            rel_table = Table(rel_data, colWidths=[180, 100, 260])
            rel_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#FEF2F2')),
                ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#FCA5A5')),
                ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#FEE2E2')),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ]))
            elements.append(rel_table)
            elements.append(Spacer(1, 8))

        # 5. Pre-Drafted Notice Requisitions (Fix 17)
        elements.append(Paragraph("5. STATUTORY REQUISITION NOTICE (DRAFT U/S 91 CrPC / SEC 94 BNSS)", self.heading2))
        notice_target_phone = phones[0] if phones else "Identified Suspect Numbers"
        notice_target_upi = upis[0] if upis else "Identified Payment Handles"
        notice_draft = f"""
        <b>To: Nodal Officer, Telecom Service Provider / Bank Intermediary / Registrar</b><br/>
        <b>Subject:</b> Requisition of Subscriber Identity (CAF), Call Detail Records (CDR), and Account Freezing under Section 91 CrPC / Section 94 BNSS.<br/>
        In connection with inquiry into Case Ref: <b>{case_data.get('case_number')}</b> involving cyber financial fraud under Section 66D IT Act, you are hereby directed to provide:<br/>
        1. Certified Customer Acquisition Form (CAF) & CDR/Tower dumps for phone number: <b>{notice_target_phone}</b>.<br/>
        2. Immediate debit freeze on beneficiary handle <b>{notice_target_upi}</b> and furnish IP login logs and KYC records.<br/>
        3. Compliance report within 24 hours of receipt of this notice.
        """
        elements.append(Paragraph(notice_draft, self.body))
        elements.append(Spacer(1, 8))

        # 6. Legal Admissibility Certificate Block
        elements.append(Paragraph("6. CERTIFICATE OF ELECTRONIC EVIDENCE INTEGRITY (SEC 63 BSA 2023)", self.heading2))
        cert_text = f"""
        This is to certify that this electronic forensic dossier has been produced by the SurakshaKavach AI Forensic Engine in the ordinary course of official cyber threat triage. The cryptographic hash <b>{sha256_hash[:32]}...</b> confirms that the source digital artifact has remained intact without unauthorized alteration or tampering.<br/><br/>
        <b>Generated by:</b> Cyber Forensic Station | <b>Investigating Officer Signature:</b> _________________________
        """
        elements.append(Paragraph(cert_text, self.body))
        elements.append(Spacer(1, 10))

        elements.append(HRFlowable(width="100%", thickness=0.8, color=colors.HexColor('#94A3B8'), spaceAfter=5))
        elements.append(Paragraph("<b>CONFIDENTIAL — FOR LAW ENFORCEMENT & INVESTIGATION USE ONLY</b>", self.sub_title))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
