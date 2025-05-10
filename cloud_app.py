"""
Streamlit Cloud App for Renovation Cost Estimator

A simplified version with minimal dependencies for cloud deployment.
"""
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up the page
st.set_page_config(
    page_title="Renovation Cost Estimator",
    page_icon="🏠",
    layout="wide"
)

# Main app header
st.title("🏠 Renovation Cost Estimator")
st.subheader("Cloud Version")

st.markdown("""
This is a simplified version of the Renovation Cost Estimator app for cloud deployment.
The full version includes:
- Cost estimation based on project details
- Semantic search for similar projects
- Visualization of cost breakdowns
- PDF report generation
""")

# Sample data for demonstration
sample_projects = [
    {"type": "Kitchen", "size": 200, "grade": "Premium", "cost": 45000},
    {"type": "Bathroom", "size": 100, "grade": "Standard", "cost": 25000},
    {"type": "Addition", "size": 400, "grade": "Luxury", "cost": 150000}
]

# Convert to DataFrame
df = pd.DataFrame(sample_projects)

# Display sample data
st.subheader("Sample Renovation Projects")
st.dataframe(df)

# Simple interactive elements
st.subheader("Try a Simple Estimate")

col1, col2 = st.columns(2)

with col1:
    project_type = st.selectbox("Project Type", ["Kitchen", "Bathroom", "Addition"])
    square_feet = st.slider("Square Footage", 50, 1000, 200)

with col2:
    material_grade = st.radio("Material Grade", ["Standard", "Premium", "Luxury"])
    
# Simple calculation for demo
base_costs = {
    "Kitchen": 200,
    "Bathroom": 250,
    "Addition": 300
}

multipliers = {
    "Standard": 1.0,
    "Premium": 1.5,
    "Luxury": 2.2
}

# Calculate estimated cost
base_cost = base_costs.get(project_type, 200)
multiplier = multipliers.get(material_grade, 1.0)
estimated_cost = base_cost * square_feet * multiplier

# Display result
st.subheader("Estimated Cost")
st.metric("Total Cost", f"${int(estimated_cost):,}")

# Create a simple chart
st.subheader("Cost Breakdown")
fig, ax = plt.subplots()
breakdown = {
    "Materials": 0.4 * estimated_cost,
    "Labor": 0.35 * estimated_cost,
    "Permits": 0.1 * estimated_cost,
    "Design": 0.15 * estimated_cost
}

ax.bar(breakdown.keys(), breakdown.values())
ax.set_ylabel("Cost ($)")
ax.set_title("Cost Breakdown")
for i, v in enumerate(breakdown.values()):
    ax.text(i, v + 1000, f"${int(v):,}", ha='center')

st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("© 2024 Renovation Estimator - Cloud Version")

if __name__ == "__main__":
    pass 