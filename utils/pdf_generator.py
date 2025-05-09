import streamlit as st
from datetime import datetime

def generate_html_report(inputs, estimate):
    """Generate HTML report for cost estimate (mocked PDF for MVP)."""
    # Extract data
    project_type = inputs.get("project_type", "kitchen").title()
    square_feet = inputs.get("square_feet", 200)
    material_grade = inputs.get("material_grade", "standard").title()
    zip_code = inputs.get("zip_code", "90210")
    
    # Format estimate data
    min_cost, max_cost = estimate["total_range"]
    timeline_weeks = estimate["timeline_weeks"]
    breakdown = estimate["cost_breakdown"]
    
    # Generate HTML
    html = f"""
    <style>
        .pdf-container {{
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            border: 1px solid #ddd;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .section {{
            margin: 20px 0;
        }}
        .summary-box {{
            background-color: #f5f5f5;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th, td {{
            padding: 8px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }}
        th {{
            background-color: #f2f2f2;
        }}
        .footer {{
            margin-top: 30px;
            font-size: 0.8em;
            text-align: center;
            color: #666;
        }}
    </style>
    
    <div class="pdf-container">
        <div class="header">
            <h1>Renovation Cost Estimate</h1>
            <p>Generated on {datetime.now().strftime("%B %d, %Y")}</p>
        </div>
        
        <div class="section">
            <h2>Project Details</h2>
            <table>
                <tr>
                    <th>Project Type</th>
                    <td>{project_type}</td>
                </tr>
                <tr>
                    <th>Location</th>
                    <td>ZIP Code {zip_code}</td>
                </tr>
                <tr>
                    <th>Square Footage</th>
                    <td>{square_feet} sq ft</td>
                </tr>
                <tr>
                    <th>Material Grade</th>
                    <td>{material_grade}</td>
                </tr>
            </table>
        </div>
        
        <div class="section">
            <h2>Cost Summary</h2>
            <div class="summary-box">
                <h3>Total Estimated Cost</h3>
                <h2>${min_cost:,} - ${max_cost:,}</h2>
                <p>Estimated Timeline: {timeline_weeks} weeks</p>
            </div>
        </div>
        
        <div class="section">
            <h2>Cost Breakdown</h2>
            <table>
                <tr>
                    <th>Category</th>
                    <th>Amount</th>
                    <th>Percentage</th>
                </tr>
    """
    
    # Add breakdown rows
    total_cost = sum(breakdown.values())
    for category, amount in breakdown.items():
        percentage = (amount / total_cost) * 100
        html += f"""
                <tr>
                    <td>{category.title()}</td>
                    <td>${amount:,}</td>
                    <td>{percentage:.1f}%</td>
                </tr>
        """
    
    # Complete HTML
    html += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>Next Steps</h2>
            <ol>
                <li>Review this estimate with potential contractors</li>
                <li>Request detailed quotes from 3-5 contractors</li>
                <li>Verify permit requirements with your local building department</li>
                <li>Consider financing options if needed</li>
            </ol>
        </div>
        
        <div class="footer">
            <p>This estimate is provided by AI Remodel Cost Estimator. Actual costs may vary.</p>
            <p>For more detailed estimates and contractor matching, upgrade to our Pro plan.</p>
        </div>
    </div>
    """
    
    return html

def display_pdf_html(inputs, estimate):
    """Display PDF report as HTML in Streamlit."""
    html = generate_html_report(inputs, estimate)
    
    # Display in Streamlit
    st.components.v1.html(html, height=600, scrolling=True)
    
    # Provide download link (would be actual PDF in production)
    st.download_button(
        label="Download PDF Report",
        data=html.encode(),
        file_name=f"renovation_estimate_{datetime.now().strftime('%Y%m%d')}.html",
        mime="text/html"
    )
