import streamlit as st
from backend import estimator   # backend/estimator.py must exist

# ── Page functions ────────────────────────────────────────────

def render_home():
    st.title("🏠 AI Renovation Cost Estimator")
    st.write("Enter your project details in the sidebar ➡️")

def render_estimator():
    st.sidebar.header("Project details")

    zip_code     = st.sidebar.text_input("ZIP code", "90210")
    project_type = st.sidebar.selectbox(
        "Project type", ["kitchen", "bathroom", "addition"]
    )
    sqft         = st.sidebar.number_input(
        "Square footage", 50, 10_000, 250
    )
    material     = st.sidebar.selectbox(
        "Material grade", ["economy", "standard", "premium"]
    )
    timeline     = st.sidebar.selectbox(
        "Timeline", ["flexible", "standard", "rush"]
    )

    if st.sidebar.button("Estimate"):
        result = estimator.simple_estimate(
            zip_code, project_type, sqft, material, timeline
        )
        st.success(
            f"Estimated total: **${result['total']:,}** "
            f"(${result['per_sqft']}/sq ft)"
        )

# ── Router used by streamlit_app.py ───────────────────────────

pages = {
    "Home":      render_home,
    "Estimator": render_estimator,
}
