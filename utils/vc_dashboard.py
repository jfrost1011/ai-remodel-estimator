import streamlit as st
import pandas as pd
import altair as alt

def render_vc_dashboard():
    """Render VC-focused dashboard with key metrics."""
    st.header("🚀 Market Opportunity")
    
    # Market stats in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Market Size", "$603B", "Annual")
    with col2:
        st.metric("Problem", "$241B", "Budget Overruns")
    with col3:
        st.metric("TAM", "2M Users", "$240M ARR")
    
    # Market visualization
    market_data = pd.DataFrame({
        "Category": ["Total Market", "Budget Overruns"],
        "Value": [603, 241]
    })
    
    chart = alt.Chart(market_data).mark_bar().encode(
        x=alt.X("Category", axis=alt.Axis(labelAngle=0)),
        y=alt.Y("Value", title="Billions USD"),
        color=alt.condition(
            alt.datum.Category == "Total Market",
            alt.value("#4CAF50"),
            alt.value("#FF5252")
        )
    ).properties(
        title="Home Renovation Market (2024)"
    )
    
    st.altair_chart(chart, use_container_width=True)
    
    # Technical differentiation
    st.subheader("💡 Technical Edge")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.metric("Accuracy", "92%", "+8.5% with fine-tuning")
    with tech_col2:
        st.metric("Speed", "1.8s", "63% faster than contractors")
    with tech_col3:
        st.metric("Cost Savings", "$2.4k", "per average project")
