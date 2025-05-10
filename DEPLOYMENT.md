# Renovation Cost Estimator - Streamlit Cloud Deployment Guide

This guide explains how to deploy the Renovation Cost Estimator on Streamlit Cloud.

## Deployment Setup

1. **Requirements File**: Use either:
   - `requirements.txt` (full dependencies)
   - `streamlit_requirements.txt` (minimal set for deployment)

2. **Main App File**: The entry point is `streamlit_app.py` in the root directory. 

3. **Environment Variables**: Set these in Streamlit Cloud's secrets management:
   - `MOCK_DATA`: Set to "true" for demo mode with sample data
   - `USE_PINECONE`: Set to "false" unless using Pinecone for vector search
   - `EMBEDDING_MODEL_PATH`: Path to the embedding model (default: "jfrost10/renovation-cost-estimator-fine-tune")
   - `LOG_LEVEL`: Logging level (default: "INFO")

4. **API Keys (Optional)**:
   - `OPENAI_API_KEY`: For OpenAI integration
   - `PINECONE_API_KEY`, `PINECONE_ENVIRONMENT`, `PINECONE_INDEX`: For Pinecone vector DB
   - `LANGCHAIN_API_KEY`, `LANGCHAIN_PROJECT`: For LangSmith monitoring

## Troubleshooting

Common issues:
- Check that all dependencies are installed correctly
- Ensure the correct main application file is selected
- Verify environment variables in Streamlit Cloud's secrets manager
- Check deployment logs for specific errors

## Repository Structure

- `streamlit_app.py`: Main entry point for Streamlit Cloud
- `requirements.txt`: Full dependencies list
- `streamlit_requirements.txt`: Minimal dependencies for deployment
- `.streamlit/secrets.toml`: Template for secrets configuration
- `renovation-estimator/`: Core application folder containing UI components and backend logic

## Deployment Updates

To update the deployed application:
1. Make changes to the code
2. Commit and push to the GitHub repository
3. Streamlit Cloud will automatically detect changes and redeploy 