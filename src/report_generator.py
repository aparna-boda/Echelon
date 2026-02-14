"""PDF report generation for evaluation results."""

from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime

from src.scoring import DIMENSION_LABELS, WEIGHTS


def get_score_color(score: int) -> tuple[float, float, float]:
    """Get RGB color tuple for score."""
    if score >= 85:
        return (0.0, 0.824, 0.416)  # #00D26A
    elif score >= 70:
        return (0.29, 0.62, 1.0)  # #4A9EFF
    elif score >= 50:
        return (1.0, 0.72, 0.0)  # #FFB800
    elif score >= 30:
        return (1.0, 0.42, 0.208)  # #FF6B35
    else:
        return (1.0, 0.231, 0.361)  # #FF3B5C


def generate_single_report(result: dict, problem_statement: str = "") -> BytesIO:
    """Generate PDF report for a single evaluation result."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#4A4AFF'),  # Darker purple for better visibility
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.black,  # Black for visibility
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.black,  # Black for visibility
        spaceAfter=6,
        leading=14,
    )
    
    # Title
    story.append(Paragraph("Echelon Code Evaluation Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Header info
    overall_score = result.get("overall_score", 0)
    verdict = result.get("verdict", "Unknown")
    language = result.get("language", "Unknown")
    eval_time = result.get("evaluation_time_seconds", 0)
    
    header_data = [
        ["Overall Score", "Verdict", "Language", "Evaluation Time"],
        [str(overall_score), verdict, language, f"{eval_time}s"],
    ]
    
    # Use auto column widths that fit the page (letter size is 8.5" wide, minus margins)
    header_table = Table(header_data, colWidths=[1.8*inch, 1.8*inch, 1.8*inch, 1.8*inch])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),  # Purple header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text on header
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, 1), colors.white),  # White background
        ('TEXTCOLOR', (0, 1), (-1, 1), colors.black),  # Black text
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, 1), 12),
        ('TOPPADDING', (0, 1), (-1, 1), 10),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey),  # Grey grid lines
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Problem Context (if provided)
    if problem_statement:
        story.append(Paragraph("Problem Context", heading_style))
        story.append(Paragraph(problem_statement, body_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Dimension Scores
    story.append(Paragraph("Dimension Breakdown", heading_style))
    
    dims = result.get("dimensions", {})
    dim_data = [["Dimension", "Score", "Weight", "Details"]]
    
    for key, label in DIMENSION_LABELS.items():
        dim = dims.get(key, {})
        score = dim.get("score", 0)
        weight_pct = int(WEIGHTS[key] * 100)
        
        # Get suggestion or key details
        details = dim.get("suggestion", "N/A")
        if len(details) > 60:
            details = details[:57] + "..."
        
        dim_data.append([label, str(score), f"{weight_pct}%", details])
    
    # Adjust column widths to fit page (7.5" usable width after margins)
    dim_table = Table(dim_data, colWidths=[2.2*inch, 0.9*inch, 0.9*inch, 3.5*inch])
    dim_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),  # Purple header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text on header
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 1), (1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Grey grid lines
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),  # Alternating light grey
    ]))
    story.append(dim_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Strengths
    strengths = result.get("strengths", [])
    if strengths:
        story.append(Paragraph("Strengths", heading_style))
        for strength in strengths:
            story.append(Paragraph(f"• {strength}", body_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Improvements
    improvements = result.get("improvements", [])
    if improvements:
        story.append(Paragraph("Areas for Improvement", heading_style))
        for improvement in improvements:
            story.append(Paragraph(f"• {improvement}", body_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Better Approach
    better_approach = result.get("better_approach")
    if better_approach and better_approach.strip().lower() != "n/a":
        story.append(Paragraph("Better Approach", heading_style))
        story.append(Paragraph(better_approach, body_style))
        story.append(Spacer(1, 0.2*inch))
    
    # Static Analysis (if available)
    sa = result.get("static_analysis")
    if sa:
        story.append(PageBreak())
        # Dynamic heading based on language
        lang = result.get("language", "Unknown")
        analysis_type = "AST" if lang == "Python" else "Tree-sitter"
        story.append(Paragraph(f"Static Analysis ({lang} {analysis_type})", heading_style))
        
        sa_data = [
            ["Metric", "Value"],
            ["Total Lines", str(sa.get("total_lines", 0))],
            ["Functions", str(len(sa.get("functions", [])))],
            ["Classes", str(len(sa.get("classes", [])))],
            ["Max Nesting Depth", str(sa.get("max_nesting_depth", 0))],
            ["Nested Loops", str(sa.get("nested_loops", 0))],
            ["Comment Ratio", str(sa.get("comment_ratio", 0))],
            ["Naming Quality", sa.get("naming_quality", "N/A")],
            ["Has Docstrings", "Yes" if sa.get("has_docstrings") else "No"],
            ["Has Type Hints", "Yes" if sa.get("has_type_hints") else "No"],
            ["Has Error Handling", "Yes" if sa.get("has_error_handling") else "No"],
            ["Has Tests", "Yes" if sa.get("has_tests") else "No"],
        ]
        
        sa_table = Table(sa_data, colWidths=[3.5*inch, 3.5*inch])
        sa_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),  # Purple header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text on header
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Grey grid lines
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),  # Alternating light grey
        ]))
        story.append(sa_table)
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"Generated by Echelon on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,  # Grey for footer
        alignment=TA_CENTER,
    )))
    
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_batch_report(batch_results: dict, problem_statement: str = "") -> BytesIO:
    """Generate PDF report for batch evaluation results."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=colors.HexColor('#4A4AFF'),  # Darker purple for better visibility
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.black,  # Black for visibility
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=11,
        textColor=colors.black,  # Black for visibility
        spaceAfter=6,
        leading=14,
    )
    
    # Title
    story.append(Paragraph("Echelon Batch Evaluation Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Summary Statistics
    summary = batch_results.get("summary", {})
    story.append(Paragraph("Summary Statistics", heading_style))
    
    summary_data = [
        ["Metric", "Value"],
        ["Total Submissions", str(summary.get("total_submissions", 0))],
        ["Successful", str(summary.get("successful", 0))],
        ["Failed", str(summary.get("failed", 0))],
        ["Average Score", f"{summary.get('average_score', 0):.1f}"],
        ["Min Score", str(summary.get("min_score", 0))],
        ["Max Score", str(summary.get("max_score", 0))],
        ["Median Score", str(summary.get("median_score", 0))],
        ["Total Time", f"{batch_results.get('total_time', 0)}s"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3.5*inch, 3.5*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),  # Purple header
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text on header
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('TOPPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Grey grid lines
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),  # Alternating light grey
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Verdict Distribution
    verdict_dist = summary.get("verdict_distribution", {})
    if verdict_dist:
        story.append(Paragraph("Verdict Distribution", heading_style))
        verdict_data = [["Verdict", "Count"]]
        for verdict, count in verdict_dist.items():
            verdict_data.append([verdict, str(count)])
        
        verdict_table = Table(verdict_data, colWidths=[3.5*inch, 3.5*inch])
        verdict_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),  # Purple header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text on header
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Grey grid lines
        ]))
        story.append(verdict_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Individual Results
    results = batch_results.get("results", [])
    if results:
        story.append(PageBreak())
        story.append(Paragraph("Individual Results", heading_style))
        
        # Create results table
        results_data = [["Name", "Score", "Verdict", "Language"]]
        for r in results:
            if not r.get("error"):
                results_data.append([
                    r.get("name", "Unknown")[:30],  # Truncate long names
                    str(r.get("overall_score", 0)),
                    r.get("verdict", "Unknown"),
                    r.get("language", "Unknown"),
                ])
        
        if len(results_data) > 1:  # More than just header
            # Adjust column widths to fit page
            results_table = Table(results_data, colWidths=[2.8*inch, 1*inch, 1.5*inch, 1.2*inch])
            results_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6C63FF')),  # Purple header
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),  # White text on header
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('ALIGN', (1, 1), (1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                ('TOPPADDING', (0, 0), (-1, 0), 6),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # White background
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),  # Black text
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),  # Grey grid lines
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),  # Alternating light grey
            ]))
            story.append(results_table)
    
    # Footer
    story.append(Spacer(1, 0.3*inch))
    footer_text = f"Generated by Echelon on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    story.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey,  # Grey for footer
        alignment=TA_CENTER,
    )))
    
    doc.build(story)
    buffer.seek(0)
    return buffer
