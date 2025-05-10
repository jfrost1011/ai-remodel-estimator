"""
PDF Generation Utility

This module provides functions to generate PDF documents from renovation cost estimates.
"""

import os
import tempfile
from datetime import datetime
import base64
from typing import Dict, Any
import io

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def create_pdf_download_link(estimate_data: Dict[str, Any]) -> str:
    """
    Create a PDF download link for the estimate data
    
    Args:
        estimate_data: Dictionary containing the renovation cost estimate data
        
    Returns:
        HTML string with PDF download link
    """
    # Create a nice wrapper for our export section
    export_section_start = '<div class="export-section">'
    export_section_end = '</div>'
    
    try:
        # Generate PDF using ReportLab (no external dependencies)
        pdf_bytes = generate_pdf_report(estimate_data)
        
        # Encode PDF as base64
        b64_pdf = base64.b64encode(pdf_bytes).decode()
        
        # Create PDF download button
        pdf_button = f'''
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <a href="data:application/pdf;base64,{b64_pdf}" 
               download="renovation_estimate.pdf" 
               class="download-button blue">
                <span style="vertical-align: middle; font-size: 16px;">📄 Download PDF Estimate</span>
            </a>
        </div>
        '''
        
        # Final output with everything wrapped in a nice container
        downloads = f"""
        {export_section_start}
        <h3>Export Your Estimate</h3>
        <p>Download your estimate to share with contractors or save for your records:</p>
        {pdf_button}
        {export_section_end}
        """
        
        return downloads
    except Exception as e:
        # Provide a user-friendly error message
        error_message = f"""
        {export_section_start}
        <h3>Export Your Estimate</h3>
        <div class="warning-box">
            <p><strong>⚠️ Unable to generate PDF:</strong> {str(e)}</p>
            <p>Please try refreshing the page or contact support if the issue persists.</p>
        </div>
        {export_section_end}
        """
        return error_message

def generate_pdf_report(estimate_data: Dict[str, Any]) -> bytes:
    """
    Generate a PDF report from the estimate data using ReportLab
    
    Args:
        estimate_data: Dictionary containing the renovation cost estimate data
        
    Returns:
        PDF as bytes
    """
    try:
        from reportlab.lib.pagesizes import LETTER
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib.units import inch
    except ImportError:
        # If ReportLab is not available, try to install it
        import subprocess
        import sys
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
            from reportlab.lib.pagesizes import LETTER
            from reportlab.lib import colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
            from reportlab.lib.units import inch
        except:
            # If installation fails, raise an error
            raise ImportError("ReportLab library is required for PDF generation. Please install it using 'pip install reportlab'.")
    
    # Create a file-like object to receive PDF data
    buffer = io.BytesIO()
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=LETTER,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Get styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    subheading_style = styles['Heading2']
    normal_style = styles['Normal']
    
    # Create a list to hold the PDF elements
    elements = []
    
    # Add title
    elements.append(Paragraph("Renovation Cost Estimate", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Add date
    date_text = f"Generated on {datetime.now().strftime('%B %d, %Y')}"
    elements.append(Paragraph(date_text, normal_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Project details section
    elements.append(Paragraph("Project Details", heading_style))
    
    # Create project details table
    project_data = [
        ["Project Type", estimate_data.get("project_type", "").title()],
        ["Location", f"ZIP Code {estimate_data.get('zip_code', '')}"],
        ["Square Footage", f"{estimate_data.get('sqft', 0)} sq ft"],
        ["Material Grade", estimate_data.get("material_grade", "").title()],
        ["Timeline", estimate_data.get("timeline", "").title()]
    ]
    
    project_table = Table(project_data, colWidths=[2*inch, 3.5*inch])
    project_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(project_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Cost summary section
    elements.append(Paragraph("Cost Summary", heading_style))
    
    # Add total cost
    cost_text = f"Total Estimated Cost: ${estimate_data.get('total', 0):,}"
    elements.append(Paragraph(cost_text, ParagraphStyle(
        'CostStyle',
        fontName="Helvetica-Bold",
        fontSize=14,
        textColor=colors.green,
        spaceAfter=12
    )))
    
    # Add per square foot cost
    per_sqft_text = f"Cost Per Square Foot: ${estimate_data.get('per_sqft', 0)}"
    elements.append(Paragraph(per_sqft_text, normal_style))
    
    # Add timeline
    timeline_text = f"Estimated Timeline: {estimate_data.get('timeline_weeks', 0)} weeks"
    elements.append(Paragraph(timeline_text, ParagraphStyle(
        'TimelineStyle',
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=colors.blue,
        spaceAfter=12
    )))
    
    elements.append(Spacer(1, 0.25*inch))
    
    # Cost breakdown section
    elements.append(Paragraph("Cost Breakdown", subheading_style))
    
    # Create cost breakdown table
    breakdown = estimate_data.get("breakdown", {})
    breakdown_data = [["Category", "Amount", "Percentage"]]
    
    for category, amount in breakdown.items():
        percentage = round((amount / estimate_data.get('total', 1)) * 100, 1)
        breakdown_data.append([
            category.title(),
            f"${amount:,}",
            f"{percentage}%"
        ])
    
    breakdown_table = Table(breakdown_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    breakdown_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(breakdown_table)
    elements.append(Spacer(1, 0.5*inch))
    
    # Timeline guidance
    elements.append(Paragraph("Timeline Guidance", heading_style))
    
    timeline_type = estimate_data.get("timeline", "")
    timeline_guidance = ""
    
    if timeline_type == "flexible":
        timeline_guidance = """
        <b>Flexible Timeline:</b>
        • Lower overall costs (5-10% savings)
        • Contractors can schedule work during their less busy periods
        • More time for material selection and potential sales/discounts
        • Less rush fees for expedited services
        
        <b>Recommendation:</b> Schedule your project 3-6 months in advance for maximum flexibility and cost savings.
        """
    elif timeline_type == "standard":
        timeline_guidance = """
        <b>Standard Timeline:</b>
        • Regular market rates for labor and materials
        • Project begins within 4-8 weeks of finalizing contracts
        • Standard ordering timelines for materials and fixtures
        • Regular working hours with typical project progression
        
        <b>Recommendation:</b> Begin contacting contractors within the next 1-2 months to get quotes and secure your spot in their schedule.
        """
    elif timeline_type == "rush":
        timeline_guidance = """
        <b>Rush Timeline:</b>
        • Higher costs (15-25% premium)
        • Priority scheduling with contractors
        • Expedited material delivery fees
        • Potential for overtime work
        • Less time to shop around for competitive quotes
        
        <b>Recommendation:</b> Be prepared for additional costs and consider which aspects of the project are most important if compromises need to be made to meet your timeline.
        """
    elif timeline_type == "emergency":
        timeline_guidance = """
        <b>Emergency Timeline:</b>
        • Significant cost premium (30-50% higher)
        • Immediate contractor attention
        • Highest priority for materials and services
        • Potential 24/7 work schedules
        • Limited material selection based on immediate availability
        
        <b>Recommendation:</b> Focus on addressing critical issues first, then consider a phased approach for less urgent aspects of the renovation.
        """
    
    elements.append(Paragraph(timeline_guidance, normal_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Recommended services
    elements.append(Paragraph("Recommended Services", heading_style))
    
    project_type = estimate_data.get("project_type", "")
    services_text = ""
    
    # Project-specific services
    if project_type == "kitchen":
        services_text += """
        <b>Kitchen-Specific Services:</b>
        • Kitchen Design Specialist: Professional layout optimization ($1,500-3,000)
        • Appliance Package Deals: Coordinated appliance selection for cohesive look
        • Custom Cabinetry Consultation: Maximize storage and functionality
        • Lighting Design: Task and ambient lighting plan for improved functionality
        • Plumbing Upgrades: Consider water filtration systems and efficient fixtures
        """
    elif project_type == "bathroom":
        services_text += """
        <b>Bathroom-Specific Services:</b>
        • Waterproofing Specialist: Ensure proper moisture management ($500-1,200)
        • Tile Design Consultation: Optimize layout and reduce waste
        • Ventilation Assessment: Prevent moisture issues and improve air quality
        • Plumbing Fixture Package: Coordinated fixtures for consistent styling
        • Accessibility Options: Future-proof your bathroom with universal design elements
        """
    elif project_type == "addition":
        services_text += """
        <b>Addition-Specific Services:</b>
        • Architectural Services: Professional plans and permits ($2,500-5,000)
        • Structural Engineer: Ensure proper foundation and support
        • HVAC Specialist: Properly size heating/cooling for new space
        • Insulation Consultation: Maximize energy efficiency
        • Exterior Finish Matching: Seamlessly blend your addition with existing structure
        """
    
    # Add general services for all project types
    services_text += """
    <b>General Services:</b>
    • 3D Rendering: Visualize your project before construction begins
    • Project Management: Professional oversight to keep your project on track
    • Permit Expediting: Navigate local building codes and requirements
    • Financing Options: Explore renovation loans with competitive rates
    • Post-Construction Cleaning: Professional detailed cleaning once work is complete
    """
    
    elements.append(Paragraph(services_text, normal_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Next steps
    elements.append(Paragraph("Next Steps", heading_style))
    
    next_steps_text = """
    1. Contact contractors for quotes
    2. Plan your renovation timeline
    3. Create a budget based on this estimate
    4. Share this report with potential contractors
    """
    
    elements.append(Paragraph(next_steps_text, normal_style))
    elements.append(Spacer(1, 0.5*inch))
    
    # Footer
    footer_text = f"© {datetime.now().year} HomeAdvisorAI - This estimate is for planning purposes only. Actual costs may vary based on specific contractor quotes and local market conditions."
    elements.append(Paragraph(footer_text, ParagraphStyle(
        'Footer',
        fontName="Helvetica-Oblique",
        fontSize=8,
        textColor=colors.grey,
        alignment=1  # Center alignment
    )))
    
    # Build the PDF
    doc.build(elements)
    
    # Get the PDF data
    pdf_data = buffer.getvalue()
    buffer.close()
    
    return pdf_data

def generate_text_report(estimate_data: Dict[str, Any]) -> str:
    """
    Generate a text report from the estimate data
    
    Args:
        estimate_data: Dictionary containing the renovation cost estimate data
        
    Returns:
        Text report as a string
    """
    # Create a text report
    text_report = f"""
=============================================================
                RENOVATION COST ESTIMATE
=============================================================
Generated on {datetime.now().strftime("%B %d, %Y")}

PROJECT DETAILS
--------------
Project Type:    {estimate_data.get("project_type", "").title()}
Location:        ZIP Code {estimate_data.get("zip_code", "")}
Square Footage:  {estimate_data.get("sqft", 0)} sq ft
Material Grade:  {estimate_data.get("material_grade", "").title()}
Timeline:        {estimate_data.get("timeline", "").title()}

COST SUMMARY
-----------
Total Estimated Cost:    ${estimate_data.get('total', 0):,}
Cost Per Square Foot:    ${estimate_data.get('per_sqft', 0)}
Estimated Timeline:      {estimate_data.get('timeline_weeks', 0)} weeks

COST BREAKDOWN
------------
"""
    
    # Add breakdown details
    breakdown = estimate_data.get("breakdown", {})
    max_category_length = max([len(category.title()) for category in breakdown.keys()], default=10)
    
    for category, amount in breakdown.items():
        percentage = round((amount / estimate_data.get('total', 1)) * 100, 1)
        # Format with alignment for cleaner text report
        text_report += f"{category.title():{max_category_length}}    ${amount:10,}    ({percentage:4.1f}%)\n"
    
    # Add timeline guidance based on selected timeline
    timeline_type = estimate_data.get("timeline", "")
    if timeline_type:
        text_report += f"""
TIMELINE GUIDANCE
---------------
{timeline_type.title()} Timeline:"""
        
        if timeline_type == "flexible":
            text_report += """
- Lower overall costs (5-10% savings)
- Contractors can schedule work during their less busy periods
- More time for material selection and potential sales/discounts
- Less rush fees for expedited services

Recommendation: Schedule your project 3-6 months in advance for maximum flexibility and cost savings.
"""
        elif timeline_type == "standard":
            text_report += """
- Regular market rates for labor and materials
- Project begins within 4-8 weeks of finalizing contracts
- Standard ordering timelines for materials and fixtures
- Regular working hours with typical project progression

Recommendation: Begin contacting contractors within the next 1-2 months to get quotes and secure your spot in their schedule.
"""
        elif timeline_type == "rush":
            text_report += """
- Higher costs (15-25% premium)
- Priority scheduling with contractors
- Expedited material delivery fees
- Potential for overtime work
- Less time to shop around for competitive quotes

Recommendation: Be prepared for additional costs and consider which aspects of the project are most important if compromises need to be made to meet your timeline.
"""
        elif timeline_type == "emergency":
            text_report += """
- Significant cost premium (30-50% higher)
- Immediate contractor attention
- Highest priority for materials and services
- Potential 24/7 work schedules
- Limited material selection based on immediate availability

Recommendation: Focus on addressing critical issues first, then consider a phased approach for less urgent aspects of the renovation.
"""
    
    # Add recommended services based on project type
    project_type = estimate_data.get("project_type", "")
    text_report += f"""
RECOMMENDED SERVICES
------------------
"""
    
    # Project-specific services
    if project_type == "kitchen":
        text_report += """
Kitchen-Specific Services:
- Kitchen Design Specialist: Professional layout optimization ($1,500-3,000)
- Appliance Package Deals: Coordinated appliance selection for cohesive look
- Custom Cabinetry Consultation: Maximize storage and functionality
- Lighting Design: Task and ambient lighting plan for improved functionality
- Plumbing Upgrades: Consider water filtration systems and efficient fixtures
"""
    elif project_type == "bathroom":
        text_report += """
Bathroom-Specific Services:
- Waterproofing Specialist: Ensure proper moisture management ($500-1,200)
- Tile Design Consultation: Optimize layout and reduce waste
- Ventilation Assessment: Prevent moisture issues and improve air quality
- Plumbing Fixture Package: Coordinated fixtures for consistent styling
- Accessibility Options: Future-proof your bathroom with universal design elements
"""
    elif project_type == "addition":
        text_report += """
Addition-Specific Services:
- Architectural Services: Professional plans and permits ($2,500-5,000)
- Structural Engineer: Ensure proper foundation and support
- HVAC Specialist: Properly size heating/cooling for new space
- Insulation Consultation: Maximize energy efficiency
- Exterior Finish Matching: Seamlessly blend your addition with existing structure
"""
    
    # Add general services for all project types
    text_report += """
General Services:
- 3D Rendering: Visualize your project before construction begins
- Project Management: Professional oversight to keep your project on track
- Permit Expediting: Navigate local building codes and requirements
- Financing Options: Explore renovation loans with competitive rates
- Post-Construction Cleaning: Professional detailed cleaning once work is complete
"""
    
    # Add next steps
    text_report += """
NEXT STEPS
---------
1. Contact contractors for quotes
2. Plan your renovation timeline
3. Create a budget based on this estimate
4. Share this report with potential contractors

=============================================================
© HomeAdvisorAI - This estimate is for planning purposes only.
Actual costs may vary based on specific contractor quotes and
local market conditions.
=============================================================
"""
    
    return text_report

def generate_estimate_html(estimate_data: Dict[str, Any]) -> str:
    """
    Generate HTML content for the PDF
    
    Args:
        estimate_data: Dictionary containing the renovation cost estimate data
        
    Returns:
        HTML string for the PDF
    """
    # Basic HTML template with inline CSS for style
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Renovation Cost Estimate</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .header h1 {
                color: #2c3e50;
                margin-bottom: 5px;
            }
            .date {
                color: #7f8c8d;
                font-size: 14px;
                margin-bottom: 20px;
            }
            .section {
                margin-bottom: 30px;
                border-bottom: 1px solid #eee;
                padding-bottom: 20px;
            }
            .section h2 {
                color: #2980b9;
                margin-bottom: 15px;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            table, th, td {
                border: 1px solid #ddd;
            }
            th, td {
                padding: 12px;
                text-align: left;
            }
            th {
                background-color: #f2f2f2;
            }
            .cost {
                font-size: 24px;
                font-weight: bold;
                color: #27ae60;
                margin: 20px 0;
            }
            .timeline {
                font-size: 18px;
                color: #2980b9;
                margin: 20px 0;
            }
            .next-steps {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 5px;
            }
            .next-steps ol {
                margin-left: 20px;
            }
            .footer {
                margin-top: 50px;
                text-align: center;
                color: #7f8c8d;
                font-size: 12px;
            }
            .logo {
                text-align: center;
                margin-bottom: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <div class="logo">🏠</div>
            <h1>Renovation Cost Estimate</h1>
            <div class="date">Generated on {{ date }}</div>
        </div>
        
        <div class="section">
            <h2>Project Details</h2>
            <table>
                <tr>
                    <th>Parameter</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Project Type</td>
                    <td>{{ project_type }}</td>
                </tr>
                <tr>
                    <td>Location</td>
                    <td>ZIP Code {{ zip_code }}</td>
                </tr>
                <tr>
                    <td>Square Footage</td>
                    <td>{{ square_feet }} sq ft</td>
                </tr>
                <tr>
                    <td>Material Grade</td>
                    <td>{{ material_grade }}</td>
                </tr>
                <tr>
                    <td>Timeline</td>
                    <td>{{ timeline }}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Cost Summary</h2>
            <div class="cost">Total Estimated Cost: ${{ total_cost }}</div>
            <div class="timeline">Estimated Timeline: {{ timeline_weeks }} weeks</div>
            
            <h3>Cost Breakdown</h3>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Percentage</th>
                </tr>
                {% for category, amount in breakdown.items() %}
                <tr>
                    <td>{{ category|title }}</td>
                    <td>${{ amount }}</td>
                    <td>{{ (amount / total_cost * 100)|round(1) }}%</td>
                </tr>
                {% endfor %}
            </table>
        </div>
        
        <div class="section next-steps">
            <h2>Next Steps</h2>
            <ol>
                <li>Contact contractors for quotes</li>
                <li>Plan your renovation timeline</li>
                <li>Create a budget based on this estimate</li>
                <li>Share this report with potential contractors</li>
            </ol>
        </div>
        
        <div class="section">
            <h2>Additional Recommended Services</h2>
            <ul>
                <li><strong>Professional Design Services:</strong> For complex renovations, professional design services can help maximize space and functionality</li>
                <li><strong>Permit Assistance:</strong> Navigate local building codes and permit requirements</li>
                <li><strong>Project Management:</strong> Coordinate contractors and timeline to keep your project on schedule</li>
                <li><strong>Financing Options:</strong> Explore home equity loans or renovation-specific financing</li>
            </ul>
        </div>
        
        <div class="footer">
            <p>© {{ current_year }} HomeAdvisorAI - This estimate is for planning purposes only and actual costs may vary.</p>
        </div>
    </body>
    </html>
    """
    
    # Import Template class if not already imported
    try:
        from jinja2 import Template
    except ImportError:
        return "<h1>Error: jinja2 is required for PDF generation</h1>"
    
    # Format values for the template
    today = datetime.now().strftime("%B %d, %Y")
    current_year = datetime.now().year
    
    # Capitalize names
    project_type = estimate_data.get("project_type", "").title()
    material_grade = estimate_data.get("material_grade", "").title()
    timeline = estimate_data.get("timeline", "").title()
    
    # Format the total cost with commas
    total_cost = f"{estimate_data.get('total', 0):,}"
    
    # Prepare context for the template
    context = {
        "date": today,
        "current_year": current_year,
        "project_type": project_type,
        "zip_code": estimate_data.get("zip_code", ""),
        "square_feet": estimate_data.get("sqft", 0),
        "material_grade": material_grade,
        "timeline": timeline,
        "total_cost": total_cost,
        "timeline_weeks": estimate_data.get("timeline_weeks", 0),
        "breakdown": estimate_data.get("breakdown", {})
    }
    
    # Render the template with the context
    template = Template(html_template)
    html_content = template.render(**context)
    
    return html_content 