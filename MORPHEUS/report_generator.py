"""
MORPHEUS-X Report Generation Engine
PDF report generation for malware analysis results
"""

import io
from datetime import datetime
from typing import Dict, List, Any, Tuple
from pathlib import Path

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, black, white, gray
    from reportlab.platypus import (
        SimpleDocTemplate,
        Table,
        TableStyle,
        Paragraph,
        Spacer,
        PageBreak,
        Image,
        KeepTogether,
    )
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ReportGenerator:
    """Generate comprehensive PDF reports for malware analysis."""
    
    # Color scheme
    COLORS = {
        "critical": "#d62728",
        "high": "#ff9900",
        "medium": "#fbc02d",
        "low": "#2ca02c",
        "header": "#667eea",
        "accent": "#764ba2",
    }
    
    # Risk level mappings
    RISK_COLORS = {
        "critical": HexColor("#d62728"),
        "high": HexColor("#ff9900"),
        "medium": HexColor("#fbc02d"),
        "low": HexColor("#2ca02c"),
    }
    
    @staticmethod
    def generate_report(
        analysis: Dict[str, Any],
        risk_result: Dict[str, Any],
        output_path: str = None,
        report_type: str = "detailed"
    ) -> io.BytesIO:
        """
        Generate a comprehensive PDF report.
        
        Args:
            analysis: Analysis results from analyzer
            risk_result: Risk assessment results
            output_path: Optional file path to save report
            report_type: "summary", "detailed", or "executive"
            
        Returns:
            BytesIO object containing PDF data
        """
        
        if not REPORTLAB_AVAILABLE:
            return None
        
        # Create PDF buffer
        pdf_buffer = io.BytesIO()
        
        # Create document
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=letter,
            rightMargin=0.75 * inch,
            leftMargin=0.75 * inch,
            topMargin=0.75 * inch,
            bottomMargin=0.75 * inch,
        )
        
        # Get styles
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=HexColor(ReportGenerator.COLORS["header"]),
            spaceAfter=30,
            alignment=1,  # Center
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=HexColor(ReportGenerator.COLORS["accent"]),
            spaceAfter=12,
            spaceBefore=12,
        )
        
        # Build content
        story = []
        
        # Title page
        story.extend(ReportGenerator._create_title_page(title_style, heading_style, analysis))
        
        # Executive summary
        story.append(PageBreak())
        story.extend(ReportGenerator._create_executive_summary(analysis, risk_result, heading_style, styles))
        
        # Technical analysis
        story.append(PageBreak())
        story.extend(ReportGenerator._create_technical_analysis(analysis, risk_result, heading_style, styles))
        
        # Behaviors and indicators
        story.append(PageBreak())
        story.extend(ReportGenerator._create_indicators_section(analysis, heading_style, styles))
        
        # MITRE techniques
        story.append(PageBreak())
        story.extend(ReportGenerator._create_mitre_section(analysis, heading_style, styles))
        
        # Detailed findings
        if report_type in ["detailed", "full"]:
            story.append(PageBreak())
            story.extend(ReportGenerator._create_detailed_findings(analysis, heading_style, styles))
        
        # Build PDF
        doc.build(story)
        
        # Save if path provided
        if output_path:
            with open(output_path, "wb") as f:
                f.write(pdf_buffer.getvalue())
        
        pdf_buffer.seek(0)
        return pdf_buffer
    
    @staticmethod
    def _create_title_page(title_style, heading_style, analysis: Dict) -> List:
        """Create title page content."""
        story = []
        
        story.append(Spacer(1, 1.5 * inch))
        story.append(Paragraph("MORPHEUS-X", title_style))
        story.append(Paragraph("Malware Analysis Report", heading_style))
        story.append(Spacer(1, 0.5 * inch))
        
        story.append(Paragraph(f"<b>Analysis Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              styles=getSampleStyleSheet()['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        
        story.append(Paragraph(f"<b>File Name:</b> {analysis.get('file_name', 'Unknown')}", 
                              styles=getSampleStyleSheet()['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        
        story.append(Paragraph("<b>Classification:</b> Confidential", 
                              styles=getSampleStyleSheet()['Normal']))
        
        return story
    
    @staticmethod
    def _create_executive_summary(analysis: Dict, risk_result: Dict, heading_style, styles) -> List:
        """Create executive summary section."""
        story = []
        
        story.append(Paragraph("Executive Summary", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Risk verdict
        risk_level = risk_result.get("risk_level", "unknown").upper()
        verdict = risk_result.get("verdict", "No verdict available")
        risk_score = risk_result.get("risk_score", 0)
        
        summary_text = f"""
        <b>Risk Assessment:</b> {risk_level} (Score: {risk_score}/100)<br/>
        <b>Verdict:</b> {verdict}<br/>
        <b>File Name:</b> {analysis.get('file_name', 'Unknown')}<br/>
        <b>File Size:</b> {analysis.get('file_size_kb', 0):.1f} KB<br/>
        <b>Analysis Type:</b> Static Analysis with Behavioral Intelligence
        """
        
        story.append(Paragraph(summary_text, styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))
        
        # Key findings
        story.append(Paragraph("<b>Key Findings:</b>", styles['Normal']))
        
        findings = [
            f"File is PE executable: {analysis.get('is_pe', False)}",
            f"File is digitally signed: {analysis.get('is_signed', False)}",
            f"Packer suspected: {analysis.get('packer_indicators', {}).get('packer_suspected', False)}",
            f"Behaviors detected: {len(analysis.get('predicted_behaviors', []))}",
            f"MITRE techniques mapped: {len(analysis.get('mitre_techniques', {}).get('techniques', []))}",
        ]
        
        for finding in findings:
            story.append(Paragraph(f"• {finding}", styles['Normal']))
        
        return story
    
    @staticmethod
    def _create_technical_analysis(analysis: Dict, risk_result: Dict, heading_style, styles) -> List:
        """Create technical analysis section."""
        story = []
        
        story.append(Paragraph("Technical Analysis", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # File metadata table
        story.append(Paragraph("<b>File Metadata</b>", styles['Normal']))
        
        hashes = analysis.get("hashes", {})
        metadata_data = [
            ["Attribute", "Value"],
            ["File Name", analysis.get("file_name", "N/A")],
            ["File Size", f"{analysis.get('file_size_kb', 0):.1f} KB"],
            ["MD5", hashes.get("md5", "N/A")],
            ["SHA1", hashes.get("sha1", "N/A")],
            ["SHA256", hashes.get("sha256", "N/A")],
            ["Entry Point", analysis.get("entry_point", "N/A")],
            ["Timestamp", analysis.get("timestamp", "N/A")],
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2 * inch, 4 * inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), HexColor(ReportGenerator.COLORS["header"])),
            ('TEXTCOLOR', (0, 0), (-1, 0), white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
            ('GRID', (0, 0), (-1, -1), 1, black),
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 0.3 * inch))
        
        # Risk factors
        story.append(Paragraph("<b>Risk Assessment Breakdown</b>", styles['Normal']))
        
        risk_factors = risk_result.get("risk_factors", {})
        if risk_factors:
            factor_data = [["Risk Factor", "Score"]]
            for factor, score in risk_factors.items():
                factor_data.append([factor.replace("_", " ").title(), f"{score:.1f}"])
            
            factor_table = Table(factor_data, colWidths=[3 * inch, 1.5 * inch])
            factor_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor(ReportGenerator.COLORS["header"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
            ]))
            
            story.append(factor_table)
        
        return story
    
    @staticmethod
    def _create_indicators_section(analysis: Dict, heading_style, styles) -> List:
        """Create indicators section."""
        story = []
        
        story.append(Paragraph("Detected Indicators", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # Behaviors
        story.append(Paragraph("<b>Predicted Behaviors</b>", styles['Normal']))
        behaviors = analysis.get("predicted_behaviors", [])
        
        if behaviors:
            behavior_data = [["Behavior", "Category", "Confidence"]]
            for behavior in behaviors[:10]:
                behavior_data.append([
                    behavior.get("name", "Unknown")[:30],
                    behavior.get("category", "Unknown"),
                    f"{behavior.get('confidence', 0):.0%}"
                ])
            
            behavior_table = Table(behavior_data, colWidths=[2.5 * inch, 1.5 * inch, 1.5 * inch])
            behavior_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor(ReportGenerator.COLORS["header"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
            ]))
            
            story.append(behavior_table)
        else:
            story.append(Paragraph("No behaviors detected.", styles['Normal']))
        
        story.append(Spacer(1, 0.3 * inch))
        
        # Suspicious APIs
        story.append(Paragraph("<b>Suspicious API Imports</b>", styles['Normal']))
        suspicious_apis = analysis.get("suspicious_imports", [])
        
        if suspicious_apis:
            api_count = len(suspicious_apis)
            story.append(Paragraph(f"Found {api_count} suspicious API imports.", styles['Normal']))
            
            api_data = [["DLL", "Function"]]
            for api in suspicious_apis[:8]:
                api_data.append([
                    api.get("dll", "Unknown"),
                    api.get("function", "Unknown")[:35]
                ])
            
            api_table = Table(api_data, colWidths=[2 * inch, 3.5 * inch])
            api_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor(ReportGenerator.COLORS["header"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
            ]))
            
            story.append(api_table)
        else:
            story.append(Paragraph("No suspicious APIs detected.", styles['Normal']))
        
        return story
    
    @staticmethod
    def _create_mitre_section(analysis: Dict, heading_style, styles) -> List:
        """Create MITRE ATT&CK section."""
        story = []
        
        story.append(Paragraph("MITRE ATT&CK Framework", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        mitre_data = analysis.get("mitre_techniques", {})
        techniques = mitre_data.get("techniques", [])
        
        if techniques:
            technique_data = [["ID", "Technique", "Tactic", "Confidence"]]
            for tech in techniques[:12]:
                technique_data.append([
                    tech.get("id", "N/A"),
                    tech.get("name", "Unknown")[:25],
                    tech.get("tactic", "Unknown"),
                    f"{tech.get('confidence', 0):.0%}"
                ])
            
            technique_table = Table(technique_data, colWidths=[1 * inch, 2 * inch, 1.5 * inch, 1 * inch])
            technique_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor(ReportGenerator.COLORS["header"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
            ]))
            
            story.append(technique_table)
        else:
            story.append(Paragraph("No MITRE techniques identified.", styles['Normal']))
        
        return story
    
    @staticmethod
    def _create_detailed_findings(analysis: Dict, heading_style, styles) -> List:
        """Create detailed findings section."""
        story = []
        
        story.append(Paragraph("Detailed Findings", heading_style))
        story.append(Spacer(1, 0.2 * inch))
        
        # PE Sections
        story.append(Paragraph("<b>PE File Sections</b>", styles['Normal']))
        
        sections = analysis.get("sections", [])
        if sections:
            section_data = [["Name", "Virtual Size", "Entropy", "Suspicious"]]
            for sec in sections:
                section_data.append([
                    sec.get("name", "Unknown"),
                    f"{sec.get('virtual_size', 0)} bytes",
                    f"{sec.get('entropy', 0):.2f}",
                    "Yes" if sec.get("suspicious") else "No"
                ])
            
            section_table = Table(section_data, colWidths=[1.5 * inch, 1.5 * inch, 1 * inch, 1 * inch])
            section_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor(ReportGenerator.COLORS["header"])),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('GRID', (0, 0), (-1, -1), 1, black),
                ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0f0f0')),
            ]))
            
            story.append(section_table)
        
        story.append(Spacer(1, 0.3 * inch))
        
        # Strings
        story.append(Paragraph("<b>Extracted Strings (Sample)</b>", styles['Normal']))
        strings = analysis.get("strings", [])
        
        if strings:
            story.append(Paragraph(f"Total strings found: {len(strings)}", styles['Normal']))
            
            # Show first 20 strings
            for s in strings[:20]:
                story.append(Paragraph(f"• {s[:60]}", styles['Normal']))
        else:
            story.append(Paragraph("No strings extracted.", styles['Normal']))
        
        return story
    
    @staticmethod
    def generate_summary_report(
        analysis: Dict[str, Any],
        risk_result: Dict[str, Any],
    ) -> str:
        """Generate a text summary report."""
        
        report = f"""
{'='*80}
MORPHEUS-X ANALYSIS REPORT - SUMMARY
{'='*80}

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

FILE INFORMATION
{'-'*80}
File Name: {analysis.get('file_name', 'Unknown')}
File Size: {analysis.get('file_size_kb', 0):.1f} KB
MD5: {analysis.get('hashes', {}).get('md5', 'N/A')}
SHA256: {analysis.get('hashes', {}).get('sha256', 'N/A')[:32]}...

RISK ASSESSMENT
{'-'*80}
Risk Score: {risk_result.get('risk_score', 0)}/100
Risk Level: {risk_result.get('risk_level', 'Unknown').upper()}
Verdict: {risk_result.get('verdict', 'N/A')}

TECHNICAL DETAILS
{'-'*80}
Is PE: {analysis.get('is_pe', False)}
Is Signed: {analysis.get('is_signed', False)}
Packer Detected: {analysis.get('packer_indicators', {}).get('packer_suspected', False)}
Entry Point: {analysis.get('entry_point', 'N/A')}

INDICATORS
{'-'*80}
Behaviors Detected: {len(analysis.get('predicted_behaviors', []))}
Suspicious APIs: {len(analysis.get('suspicious_imports', []))}
Suspicious Strings: {len(analysis.get('suspicious_strings', []))}
MITRE Techniques: {len(analysis.get('mitre_techniques', {}).get('techniques', []))}

RECOMMENDATIONS
{'-'*80}
1. Review the file in an isolated environment
2. Check against threat intelligence databases
3. Monitor for similar samples
4. Deploy detection rules based on indicators

{'='*80}
"""
        
        return report
