# Renovation Cost Estimator

A specialized tool that provides accurate renovation cost estimates based on project details and similar historical projects.

## [Click here to access the live application](https://renovation-cost-estimator.streamlit.app/)

## Features

- 🏠 **Smart Cost Estimation**: Get accurate renovation cost estimates based on project type, size, materials, and location
- 🔍 **Semantic Search**: Find similar renovation projects with fine-tuned embeddings
- 📊 **Data Visualization**: Explore cost breakdowns and comparisons
- 🧠 **AI-Powered**: Uses fine-tuned embeddings for domain-specific understanding of renovation projects

## Technology Stack

- **Python**: Core programming language
- **Streamlit**: Web application framework
- **LangChain**: For embedding and vector operations
- **Sentence Transformers**: Fine-tuned embedding model
- **Pinecone**: Vector database (optional)
- **Plotly & Matplotlib**: Data visualization
- **OpenAI**: For advanced cost estimation (optional)

## About the App

The Renovation Cost Estimator helps homeowners plan their renovation projects by providing accurate cost estimates based on real-world data. By leveraging fine-tuned embeddings and semantic search technology, the app can find similar projects and provide relevant cost comparisons.

### How it Works

1. **Input your project details**: Enter information about your renovation project including type, square footage, material grade, and timeline.
2. **AI-powered analysis**: Our fine-tuned model analyzes your project and finds similar historical projects.
3. **Get detailed estimates**: Receive a breakdown of costs including materials, labor, permits, and other expenses.
4. **Explore alternatives**: See how changing parameters affects your total cost.

## Local Development

See the detailed instructions in the [renovation-estimator/README.md](renovation-estimator/README.md) file.

## Deployment

This application is deployed on Streamlit Cloud. The deployment uses:

- `app.py`: Main entry point that loads the core application
- `requirements.txt`: Dependencies needed for deployment
- `.streamlit/config.toml`: Streamlit configuration settings

To deploy your own version:

1. Fork this repository
2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and connect it to your forked repository
4. Set up the necessary secrets in Streamlit Cloud settings

## Deployment Troubleshooting

If you encounter dependency issues when deploying to Streamlit Cloud, here are some solutions:

### Version Conflicts

The key dependencies for this project must be compatible. We've carefully selected matching versions:

```
langchain==0.2.5
langchain-community==0.2.5
langchain-core==0.2.7
```

### Understanding Error Messages

If you see errors like this:
```
ERROR: Cannot install package A and package B because these package versions have conflicting dependencies.
```

This means that two packages require different versions of a shared dependency. To fix:
1. Look for the specific conflict in the error message
2. Update one of the packages to a compatible version
3. Or pin both to exact compatible versions

### Fallback System

The app includes a triple-layer fallback system:
1. First tries to load the full app with all LangChain features
2. If that fails, falls back to a simplified cloud version
3. As a last resort, runs a minimal embedded version

This ensures the app will always display something useful to users, even if there are dependency issues.

## Acknowledgements

This project uses a fine-tuned embedding model specifically trained for the renovation domain. The model is available at [jfrost10/renovation-cost-estimator-fine-tune](https://huggingface.co/jfrost10/renovation-cost-estimator-fine-tune) on Hugging Face. 