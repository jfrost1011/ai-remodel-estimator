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
        HTML string with download link for the PDF
    """
    try:
        # Import optional dependencies
        import pdfkit
        from jinja2 import Template
    except ImportError:
        st.warning("PDF export requires pdfkit and jinja2. Install with: pip install pdfkit jinja2")
        return ""
    
    # Create a temporary directory for our files
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Generate a PDF file
        pdf_path = os.path.join(tmpdirname, "renovation_estimate.pdf")
        
        # Create HTML content for the PDF
        html_content = generate_estimate_html(estimate_data)
        
        # Write HTML to a temporary file
        html_path = os.path.join(tmpdirname, "estimate.html")
        with open(html_path, "w") as f:
            f.write(html_content)
        
        # Convert HTML to PDF
        try:
            # Try with installed wkhtmltopdf
            pdfkit.from_file(html_path, pdf_path)
        except OSError:
            # Fallback message if wkhtmltopdf is not installed
            st.error("PDF generation requires wkhtmltopdf to be installed. Please install it from https://wkhtmltopdf.org/downloads.html")
            return ""
        
        # Read the PDF file
        with open(pdf_path, "rb") as f:
            pdf_data = f.read()
        
        # Convert to base64 for the download link
        b64_pdf = base64.b64encode(pdf_data).decode()
        
        # Create download link
        href = f'<a href="data:application/pdf;base64,{b64_pdf}" download="renovation_estimate.pdf">Download PDF Report</a>'
        return href

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
        </style>
    </head>
    <body>
        <div class="header">
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