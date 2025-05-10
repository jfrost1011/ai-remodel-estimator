import streamlit as st

# Page configuration
st.set_page_config(page_title="🏡 AI Remodel Cost Estimator", layout="wide")

import os
import json
import pandas as pd
from utils.env_loader import load_env_vars

# Load environment variables properly
if not load_env_vars():
    st.error("Failed to load environment variables. Please check your .env file.")
    st.stop()

# Initialize LangSmith if available
LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT", "renovation-estimator")
if LANGSMITH_API_KEY:
    from langsmith import Client
    langsmith_client = Client(api_key=LANGSMITH_API_KEY)
    print(f"LangSmith initialized with project: {LANGSMITH_PROJECT}")

# Import backend components
from backend.vector_store import get_vector_store
from backend.estimator import CostEstimator
from backend.evaluation import evaluate_with_ragas, generate_model_comparison

# Import utility functions
from utils.vc_dashboard import render_vc_dashboard
from utils.pdf_generator import display_pdf_html

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.inputs = {}
    st.session_state.estimate = None

# Main function
def main():
    """Main application entry point that handles the multi-step wizard flow."""
    # Page title
    st.title("🏡 AI Remodel Cost Estimator")
    
    # Show steps based on current state
    if st.session_state.step == 0:
        intro_screen()
    elif st.session_state.step == 1:
        zip_code_step()
    elif st.session_state.step == 2:
        project_type_step()
    elif st.session_state.step == 3:
        square_footage_step()
    elif st.session_state.step == 4:
        material_grade_step()
    elif st.session_state.step == 5:
        timeline_step()
    elif st.session_state.step == 6:
        results_screen()

# Define step functions
def intro_screen():
    """Intro screen with simple welcome message."""
    # Simple, user-friendly explanation
    st.info("""
    This tool will help you:
    ✓ Calculate renovation costs based on your specific project
    ✓ See a detailed breakdown of expected expenses
    ✓ Get a realistic timeline for your renovation project
    ✓ Create a shareable report for contractors
    """)
    
    if st.button("Start Estimating", use_container_width=True):
        st.session_state.step = 1
        st.rerun()

def zip_code_step():
    """Step 1: Location."""
    st.header("Step 1: Location")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        zip_code = st.text_input(
            "Enter ZIP Code",
            max_chars=5,
            placeholder="e.g. 90210"
        )
    with col2:
        if st.button("Next", disabled=not (zip_code and len(zip_code) == 5 and zip_code.isdigit())):
            next_step(zip_code=zip_code)
    
    # Show location-based insights
    if "zip_code" in st.session_state.inputs:
        st.success(f"Location validated: {st.session_state.inputs['zip_code']}")
        
        # Show regional context based on first digit
        region_map = {
            "0": "New England",
            "1": "Northeast",
            "2": "Mid-Atlantic",
            "3": "Southeast",
            "4": "Midwest",
            "5": "Midwest",
            "6": "South/Southwest",
            "7": "South/Southwest",
            "8": "Mountain",
            "9": "West Coast"
        }
        
        zip_first_digit = st.session_state.inputs['zip_code'][0]
        region = region_map.get(zip_first_digit, "Unknown")
        
        st.info(f"Region: {region}")
        
        # Show cost context based on region
        if zip_first_digit == "9":
            st.info("Average renovation costs in your area are 20% above national average")
        elif zip_first_digit in ["0", "1"]:
            st.info("Average renovation costs in your area are 10% above national average")
        elif zip_first_digit in ["4", "5"]:
            st.info("Average renovation costs in your area are 15% below national average")
        else:
            st.info("Average renovation costs in your area are near the national average")

def project_type_step():
    """Step 2: Project type."""
    st.header("Step 2: Project Type")
    
    # Navigation buttons
    cols = st.columns([1, 8, 1])
    with cols[0]:
        if st.button("← Back"):
            back_step()
    
    # Project type selection
    project_type = st.radio(
        "Select renovation project type:",
        options=["Kitchen", "Bathroom", "Home Addition"],
        index=0,
        horizontal=True
    )
    
    # Project descriptions
    if project_type == "Kitchen":
        st.info("Kitchen renovations typically include cabinets, countertops, appliances, flooring, and lighting.")
        st.image("https://placehold.co/600x400?text=Kitchen+Renovation", caption="Sample Kitchen Renovation")
    elif project_type == "Bathroom":
        st.info("Bathroom renovations typically include fixtures, tiling, vanity, shower/tub, and flooring.")
        st.image("https://placehold.co/600x400?text=Bathroom+Renovation", caption="Sample Bathroom Renovation")
    else:
        st.info("Home additions expand your living space with entirely new rooms or extensions.")
        st.image("https://placehold.co/600x400?text=Home+Addition", caption="Sample Home Addition")
    
    # Map frontend selections to backend values
    type_mapping = {
        "Kitchen": "kitchen",
        "Bathroom": "bathroom",
        "Home Addition": "addition"
    }
    
    # Continue button
    with cols[2]:
        if st.button("Next →"):
            next_step(project_type=type_mapping[project_type])

def square_footage_step():
    """Step 3: Square footage."""
    st.header("Step 3: Square Footage")
    
    # Navigation buttons
    cols = st.columns([1, 8, 1])
    with cols[0]:
        if st.button("← Back"):
            back_step()
    
    # Get project type for context
    project_type = st.session_state.inputs.get("project_type", "kitchen")
    
    # Suggested square footage range based on project type
    if project_type == "kitchen":
        min_range, max_range = 100, 300
        default_value = 180
    elif project_type == "bathroom":
        min_range, max_range = 40, 150
        default_value = 80
    else:  # addition
        min_range, max_range = 200, 800
        default_value = 400
    
    # Square footage slider
    square_feet = st.slider(
        "Select square footage:",
        min_value=min_range,
        max_value=max_range,
        value=default_value,
        step=10
    )
    
    # Show context based on selection
    if square_feet < (min_range + max_range) // 3:
        st.info(f"This is a smaller than average {project_type} project.")
    elif square_feet > (min_range + max_range) * 2 // 3:
        st.info(f"This is a larger than average {project_type} project.")
    else:
        st.info(f"This is an average-sized {project_type} project.")
    
    # Continue button
    with cols[2]:
        if st.button("Next →"):
            next_step(square_feet=square_feet)

def material_grade_step():
    """Step 4: Material grade."""
    st.header("Step 4: Material Grade")
    
    # Navigation buttons
    cols = st.columns([1, 8, 1])
    with cols[0]:
        if st.button("← Back"):
            back_step()
    
    # Initialize the selected grade in session state if not already there
    if "temp_material_grade" not in st.session_state:
        st.session_state.temp_material_grade = None
    
    # Material grade selection
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Standard", use_container_width=True, key="btn_standard"):
            st.session_state.temp_material_grade = "standard"
    
    with col2:
        if st.button("Premium", use_container_width=True, key="btn_premium"):
            st.session_state.temp_material_grade = "premium"
    
    with col3:
        if st.button("Luxury", use_container_width=True, key="btn_luxury"):
            st.session_state.temp_material_grade = "luxury"
    
    # Display details based on selection
    if st.session_state.temp_material_grade == "standard":
        st.success("✓ Standard selected")
        st.markdown("- Mid-range appliances\n- Laminate countertops\n- Stock cabinets")
    elif st.session_state.temp_material_grade == "premium":
        st.success("✓ Premium selected")
        st.markdown("- Higher-end appliances\n- Quartz countertops\n- Semi-custom cabinets")
    elif st.session_state.temp_material_grade == "luxury":
        st.success("✓ Luxury selected")
        st.markdown("- Top-tier appliances\n- Marble/granite countertops\n- Custom cabinets")
    
    # Continue button (only show if a material grade is selected)
    if st.session_state.temp_material_grade:
        with cols[2]:
            if st.button("Next →"):
                next_step(material_grade=st.session_state.temp_material_grade)
                # Clear temporary selection after moving to next step
                st.session_state.temp_material_grade = None

def timeline_step():
    """Step 5: Timeline."""
    st.header("Step 5: Timeline")
    
    # Navigation buttons
    cols = st.columns([1, 8, 1])
    with cols[0]:
        if st.button("← Back"):
            back_step()
    
    # Timeline selection
    timeline_months = st.radio(
        "How quickly do you need this project completed?",
        options=[1, 2, 3],
        format_func=lambda x: f"{x} {'month' if x == 1 else 'months'}",
        horizontal=True
    )
    
    # Show timeline context
    if timeline_months == 1:
        st.warning("Rush projects typically cost 20% more but can be completed faster.")
    elif timeline_months == 2:
        st.info("Standard timeline with balanced cost efficiency.")
    else:
        st.success("Extended timeline may reduce costs by 5% but takes longer to complete.")
    
    # Continue button
    with cols[2]:
        if st.button("Get Estimate"):
            next_step(timeline_months=timeline_months)

def results_screen():
    """Final step: Display results."""
    st.header("🎉 Your Instant Estimate")
    
    # Get inputs
    inputs = st.session_state.inputs
    
    # Generate estimate if not already done
    if st.session_state.estimate is None:
        with st.spinner("Generating your estimate..."):
            # Check environment variables
            use_mock = os.environ.get("MOCK_DATA", "true").lower() == "true"
            use_pinecone = os.environ.get("USE_PINECONE", "false").lower() == "true"
            
            # Initialize vector store and estimator
            vector_store = get_vector_store(use_mock=use_mock, use_pinecone=use_pinecone)
            estimator = CostEstimator(vector_store)
            
            # Generate estimate
            st.session_state.estimate = estimator.estimate(inputs)
            
            # Extract context for evaluation
            try:
                contexts = [doc.page_content for doc in estimator.retriever.get_relevant_documents(
                    f"Cost estimate for {inputs.get('project_type', 'kitchen')} with {inputs.get('square_feet', 200)} sq ft"
                )]
            except:
                contexts = None
            
            # Use RAGAS for evaluation with LangSmith tracing
            query = f"Cost estimate for {inputs.get('project_type', 'kitchen')} with {inputs.get('square_feet', 200)} sq ft"
            st.session_state.ragas_scores = evaluate_with_ragas(
                question=query,
                answer=json.dumps(st.session_state.estimate),
                contexts=contexts
            )
    
    estimate = st.session_state.estimate
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Estimated Cost",
            f"${estimate['total_range'][0]:,} - ${estimate['total_range'][1]:,}"
        )
    with col2:
        st.metric(
            "Timeline",
            f"{estimate['timeline_weeks']} weeks"
        )
    with col3:
        st.metric(
            "Confidence",
            f"{estimate['confidence'] * 100:.0f}%"
        )
    
    # Display cost breakdown
    st.subheader("Cost Breakdown")
    breakdown = estimate["cost_breakdown"]
    
    # Create chart data
    chart_data = pd.DataFrame({
        "Category": list(breakdown.keys()),
        "Amount": list(breakdown.values())
    })
    
    # Display chart
    st.bar_chart(chart_data.set_index("Category"))
    
    # Show RAGAS evaluation metrics
    with st.expander("🔍 RAGAS Evaluation Metrics"):
        ragas_scores = st.session_state.ragas_scores
        if 'metrics' in ragas_scores and ragas_scores['metrics']:
            # Create a pandas DataFrame from the metrics dictionary
            metrics_df = pd.DataFrame({
                'Metric': list(ragas_scores['metrics'].keys()),
                'Score': list(ragas_scores['metrics'].values())
            })
            st.table(metrics_df.set_index('Metric'))
        else:
            # Fallback to direct access if metrics dict is not available
            metrics_df = pd.DataFrame({
                'Metric': ['Faithfulness', 'Answer Relevancy', 'Context Precision', 'Context Recall'],
                'Score': [
                    ragas_scores.get('faithfulness', 0),
                    ragas_scores.get('answer_relevancy', 0),
                    ragas_scores.get('context_precision', 0),
                    ragas_scores.get('context_recall', 0)
                ]
            })
            st.table(metrics_df.set_index('Metric'))
    
    # Show next steps
    st.subheader("Next Steps")
    st.write("""
    Now that you have your estimate, you can:
    1. Contact contractors for quotes
    2. Plan your renovation timeline
    3. Create a budget based on this estimate
    4. Download a detailed report to share
    """)
    
    # PDF Export
    st.subheader("Export Options")
    if st.button("Download PDF Report"):
        display_pdf_html(inputs, estimate)
    
    # Start over
    if st.button("Start New Estimate"):
        st.session_state.step = 0
        st.session_state.inputs = {}
        st.session_state.estimate = None
        st.rerun()

# Helper functions
def next_step(**kwargs):
    """Advance to next step and save inputs."""
    # Save inputs
    for key, value in kwargs.items():
        st.session_state.inputs[key] = value
    
    # Move to next step
    st.session_state.step += 1
    st.rerun()

def back_step():
    """Go back to previous step."""
    st.session_state.step -= 1
    st.rerun()

# Run app
if __name__ == "__main__":
    main()
