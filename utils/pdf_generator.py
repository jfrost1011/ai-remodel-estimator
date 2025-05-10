"""
PDF Generation Utility

This module provides functions to generate PDF documents from renovation cost estimates.
"""

import os
import tempfile
from datetime import datetime
import base64
from typing import Dict, Any

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

def create_pdf_download_link(estimate_data: Dict[str, Any]) -> str:
    """
    Create a PDF download link from estimate data
    
    Args:
        estimate_data: Dictionary containing the renovation cost estimate data
        
    Returns:
        HTML string with download link for the PDF or installation instructions
    """
    # Create a nice wrapper for our export section
    export_section_start = '<div class="export-section">'
    export_section_end = '</div>'
    
    # First check for installation instructions message
    install_message = """
    <div class="warning-box">
        <p><strong>PDF Export Requires Additional Tools</strong></p>
        <p>To enable PDF export, you need to install:</p>
        <ol>
            <li>Install Python packages: <code>pip install pdfkit jinja2</code></li>
            <li>Download wkhtmltopdf from <a href="https://wkhtmltopdf.org/downloads.html" target="_blank">wkhtmltopdf.org</a></li>
            <li>Install the downloaded package for your system</li>
            <li>Restart your Streamlit app</li>
        </ol>
    </div>
    """
    
    # For now, since this doesn't work in the deployed environment, let's provide a simulated download
    # This creates a "download" that actually contains JSON data of the estimate
    
    # Format the estimate data nicely
    formatted_data = {
        "project_details": {
            "project_type": estimate_data.get("project_type", "").title(),
            "location": f"ZIP Code {estimate_data.get('zip_code', '')}",
            "square_footage": f"{estimate_data.get('sqft', 0)} sq ft",
            "material_grade": estimate_data.get("material_grade", "").title(),
            "timeline": estimate_data.get("timeline", "").title()
        },
        "cost_summary": {
            "total_cost": f"${estimate_data.get('total', 0):,}",
            "per_sqft_cost": f"${estimate_data.get('per_sqft', 0)}",
            "timeline_weeks": f"{estimate_data.get('timeline_weeks', 0)} weeks"
        },
        "cost_breakdown": estimate_data.get("breakdown", {}),
        "generation_date": datetime.now().strftime("%B %d, %Y")
    }
    
    # Convert to JSON
    import json
    json_data = json.dumps(formatted_data, indent=2)
    
    # Encode as base64
    b64_data = base64.b64encode(json_data.encode()).decode()
    
    # Create a direct download link for the estimate data as JSON
    direct_download = f'''
    <a href="data:application/json;base64,{b64_data}" 
       download="renovation_estimate.json" 
       class="download-button">
        <span style="vertical-align: middle;">📊 Download Estimate Data</span>
    </a>
    '''
    
    # Create link for a simple text report
    text_report = f"""
Renovation Cost Estimate
========================
Generated on {datetime.now().strftime("%B %d, %Y")}

PROJECT DETAILS
--------------
Project Type: {estimate_data.get("project_type", "").title()}
Location: ZIP Code {estimate_data.get("zip_code", "")}
Square Footage: {estimate_data.get("sqft", 0)} sq ft
Material Grade: {estimate_data.get("material_grade", "").title()}
Timeline: {estimate_data.get("timeline", "").title()}

COST SUMMARY
-----------
Total Estimated Cost: ${estimate_data.get('total', 0):,}
Cost Per Square Foot: ${estimate_data.get('per_sqft', 0)}
Estimated Timeline: {estimate_data.get('timeline_weeks', 0)} weeks

COST BREAKDOWN
------------
"""
    
    # Add breakdown details
    breakdown = estimate_data.get("breakdown", {})
    for category, amount in breakdown.items():
        percentage = round((amount / estimate_data.get('total', 1)) * 100, 1)
        text_report += f"{category.title()}: ${amount:,} ({percentage}%)\n"
    
    # Add notes
    text_report += """
NEXT STEPS
---------
1. Contact contractors for quotes
2. Plan your renovation timeline
3. Create a budget based on this estimate
4. Share this report with potential contractors

© HomeAdvisorAI - This estimate is for planning purposes only and actual costs may vary.
"""
    
    # Encode text report as base64
    b64_text = base64.b64encode(text_report.encode()).decode()
    
    # Create a direct download link for the text report
    text_download = f'''
    <a href="data:text/plain;base64,{b64_text}" 
       download="renovation_estimate.txt" 
       class="download-button blue">
        <span style="vertical-align: middle;">📄 Download Text Report</span>
    </a>
    '''
    
    # Combine both download options with a better header
    downloads = f"""
    {export_section_start}
    <h3>Download Your Estimate</h3>
    <p>Choose one of the following export options:</p>
    <div style="margin: 20px 0;">
        {direct_download}
        {text_download}
    </div>
    {install_message}
    {export_section_end}
    """
    
    return downloads

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