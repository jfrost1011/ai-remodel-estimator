import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from backend import estimator   # backend/estimator.py must exist

# ── Page functions ────────────────────────────────────────────

def render_home():
    st.title("🏠 AI Renovation Cost Estimator")
    st.write("Enter your project details in the sidebar ➡️")
    
    st.markdown("""
    ## Welcome to the Renovation Cost Estimator!
    
    This tool helps homeowners and contractors estimate the cost of common renovation projects
    based on key parameters like:
    
    - Project type (kitchen, bathroom, addition, etc.)
    - Square footage
    - Material quality
    - Timeline requirements
    - Location (ZIP code)
    
    ### How to use
    
    1. Select the "Estimator" option from the navigation
    2. Enter your project details in the sidebar
    3. Click "Estimate" to generate a cost breakdown
    4. Review the results and adjust parameters as needed
    
    ### Advanced features
    
    - Regional cost adjustments based on ZIP code
    - Detailed cost breakdowns by category
    - Timeline estimates
    - Historical project comparisons
    
    To get started, select "Estimator" from the navigation.
    """)

def render_estimator():
    st.title("💰 Renovation Cost Estimator")
    st.write("Use the sidebar to enter your project details")
    
    st.sidebar.header("Project details")

    zip_code     = st.sidebar.text_input("ZIP code", "90210")
    project_type = st.sidebar.selectbox(
        "Project type", 
        ["kitchen", "bathroom", "addition", "basement", "living_room", "bedroom"]
    )
    sqft         = st.sidebar.number_input(
        "Square footage", 50, 10_000, 250
    )
    material     = st.sidebar.selectbox(
        "Material grade", 
        ["economy", "standard", "premium", "luxury"]
    )
    timeline     = st.sidebar.selectbox(
        "Timeline", 
        ["flexible", "standard", "rush", "emergency"]
    )

    if st.sidebar.button("Estimate"):
        with st.spinner("Calculating estimate..."):
            result = estimator.simple_estimate(
                zip_code, project_type, sqft, material, timeline
            )
        
        # Display total and per sq ft costs
        st.success(
            f"### Estimated total: **${result['total']:,}**\n"
            f"(${result['per_sqft']}/sq ft)"
        )
        
        # Display timeline
        st.info(f"**Estimated timeline:** {result['timeline_weeks']} weeks")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["Cost Breakdown", "Details", "Compare"])
        
        with tab1:
            # Display cost breakdown as a pie chart
            breakdown = result.get('breakdown', {})
            if breakdown:
                fig, ax = plt.subplots(figsize=(8, 5))
                wedges, texts, autotexts = ax.pie(
                    breakdown.values(), 
                    labels=breakdown.keys(),
                    autopct='%1.1f%%',
                    startangle=90
                )
                # Equal aspect ratio ensures that pie is drawn as a circle
                ax.axis('equal')
                plt.title("Cost Breakdown")
                st.pyplot(fig)
                
                # Also show as a table
                st.subheader("Cost Categories")
                breakdown_df = pd.DataFrame({
                    'Category': breakdown.keys(),
                    'Amount': ['$' + f"{value:,}" for value in breakdown.values()]
                })
                st.table(breakdown_df)
        
        with tab2:
            # Display project details
            st.subheader("Project Details")
            details_df = pd.DataFrame({
                'Parameter': ['Project Type', 'Square Footage', 'Material Grade', 'Timeline', 'ZIP Code'],
                'Value': [project_type.title(), f"{sqft} sq ft", material.title(), timeline.title(), zip_code]
            })
            st.table(details_df)
            
            # Display regional factors
            region_name = {
                "9": "West Coast",
                "1": "Northeast",
                "3": "Southeast",
                "7": "Midwest",
                "8": "Mountain"
            }.get(zip_code[0:1] if zip_code and zip_code[0:1].isdigit() else "", "Other")
            
            st.subheader("Cost Factors")
            st.write(f"**Region:** {region_name}")
            st.write(f"**Base cost for {project_type}:** ${250} per sq ft")
            st.write(f"**Material upgrade factor:** {1.0 if material == 'standard' else '0.8' if material == 'economy' else '1.3' if material == 'premium' else '1.8'}")
            st.write(f"**Timeline adjustment:** {1.0 if timeline == 'standard' else '0.9' if timeline == 'flexible' else '1.25' if timeline == 'rush' else '1.5'}")
        
        with tab3:
            # Show similar projects for comparison
            st.subheader("Similar Projects")
            
            query = f"{project_type} renovation {sqft} square feet {material} materials"
            similar_projects = estimator.search_similar_projects(query, k=3)
            
            for i, project in enumerate(similar_projects):
                with st.expander(f"Project {i+1}: {project['project_type'].title()} Renovation in {project['location']}"):
                    st.write(f"**Square Footage:** {project['square_feet']} sq ft")
                    st.write(f"**Material Grade:** {project['material_grade'].title()}")
                    st.write(f"**Timeline:** {project['timeline'].title()}")
                    st.write(f"**Total Cost:** ${project['total_cost']:,}")
                    st.write(f"**Completion Date:** {project['completion_date']}")

# ── Router used by streamlit_app.py ───────────────────────────

pages = {
    "Home":      render_home,
    "Estimator": render_estimator,
}
