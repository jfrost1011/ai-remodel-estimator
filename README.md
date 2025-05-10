# Renovation Estimator

A streamlit-based application for AI-powered renovation cost estimation.

## Tech Stack

- **LLM**: GPT-4o-mini (OpenAI)
- **Embedding Model**: OpenAI text-embedding-3-small
- **Vector DB**: Pinecone
- **Orchestration & Data Handling**: LangChain
- **Monitoring & Evaluation**: LangSmith, RAGAS

## Features

- Interactive step-by-step wizard interface
- AI-powered cost estimates with confidence scores
- Cost breakdown by category
- Timeline estimation
- PDF report generation
- Performance evaluation with RAGAS metrics

## Setup

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your API keys (see `.env.example` for a template)
4. Run the app:
   ```
   streamlit run app.py
   ```

## Environment Variables

- `OPENAI_API_KEY`: OpenAI API key
- `PINECONE_API_KEY`: Pinecone API key
- `PINECONE_ENVIRONMENT`: Pinecone environment (use "us-east-1" for free tier)
- `PINECONE_INDEX`: Pinecone index name (default: "renovation-estimator")
- `LANGSMITH_API_KEY`: LangSmith API key (optional)
- `LANGSMITH_PROJECT`: LangSmith project name (default: "renovation-estimator")

## Architecture

The application uses a retrieval-augmented generation (RAG) approach:

1. User inputs project details through a step-by-step wizard
2. The application retrieves similar projects from the Pinecone vector database
3. OpenAI's GPT-4o-mini generates cost estimates based on the project details and similar projects
4. RAGAS evaluates the quality of the generated estimates
5. Results are displayed with visualizations and can be exported as PDF reports

## Core Utilities

The project includes several utilities to maintain code organization and reduce duplication:

### Environment Loading

The `utils.env_loader` module provides standardized environment variable loading:

```python
from utils.env_loader import load_env_vars, validate_api_keys

# Load environment variables
if not load_env_vars():
    print("Failed to load environment variables")
    sys.exit(1)
    
# Check for required API keys
valid, missing_keys = validate_api_keys(["OPENAI_API_KEY", "PINECONE_API_KEY"])
```

### Data Loading

The `utils.data_loader` module provides centralized data loading functionality:

```python
from utils.data_loader import load_project_data

# Load project data
projects = load_project_data(
    data_file="path/to/file.json",  # Optional
    fallback_to_synthetic=True,     # Generate synthetic data if file not found
    count=20,                       # Number of synthetic projects to generate
    return_formatted=True           # Format for vector store
)
```

### LangSmith Integration

The `backend.langsmith_logger` module provides tracing and monitoring for LLM operations:

```python
from backend.langsmith_logger import get_langsmith_logger

# Get the logger
langsmith_logger = get_langsmith_logger()

# Apply tracing to a function
@langsmith_logger.trace(name="my_function", run_type="chain")
def my_function(input_data):
    # Function implementation
    return result
```

## Testing Framework

The project includes a comprehensive testing framework:

### Unified Test Runner

Run tests for specific categories:

```bash
python scripts/run_tests.py --category env      # Test environment setup
python scripts/run_tests.py --category api      # Test API integrations
python scripts/run_tests.py --category vector   # Test vector store
python scripts/run_tests.py --category estimator # Test cost estimator
python scripts/run_tests.py --category system   # Run full system tests
python scripts/run_tests.py --category all      # Run all tests
```

### Test Environment Script

Verify your environment setup:

```bash
python scripts/test_environment.py --with-api-tests --verbose
```

### Test Helpers

The `scripts.test_helpers` module provides standardized test utilities:

```python
from scripts.test_helpers import (
    setup_test_env,             # Set up environment
    get_test_vector_store,      # Create vector store instance
    get_test_estimator,         # Create estimator instance
    get_test_inputs,            # Get standard test inputs
    print_estimate_results      # Print formatted results
)
```

## Monitoring and Evaluation

All LLM and RAG operations are tracked using LangSmith, providing:
- Tracing of LLM interactions
- Performance monitoring
- Quality evaluation with RAGAS metrics:
  - Faithfulness
  - Answer Relevancy
  - Context Precision
  - Context Recall

For detailed information about the LangSmith integration, see [docs/langsmith_integration.md](docs/langsmith_integration.md).

## License

MIT

## Environment Setup

This project uses environment variables for configuration. Follow these steps to set up your environment:

1. Navigate to the `renovation-estimator` directory
2. Copy the template file: `cp .env.example .env`
3. Edit the `.env` file and add your actual API keys

### Required API Keys

- **OpenAI API Key**: Required for AI functionality
  - Get from: https://platform.openai.com/api-keys
  
- **Pinecone API Key**: Required for vector database functionality
  - Get from: https://app.pinecone.io/
  
- **LangSmith API Key**: Required for tracing and evaluation
  - Get from: https://smith.langchain.com/

### Testing Your Environment

To verify your environment is set up correctly, run:

```bash
python scripts/test_environment.py
```

This script will check if all required API keys are properly loaded.

## Project Structure

- All code and configuration files should be in the `renovation-estimator` directory
- The `.env` file must be located in the `renovation-estimator` directory
- Scripts should be run from the project root directory

## Important Notes

- Never commit the `.env` file to version control
- Always use the `utils.env_loader` module to load environment variables:
  ```python
  from utils.env_loader import load_env_vars
  
  # Load environment variables
  if not load_env_vars():
      print("Failed to load environment variables")
      sys.exit(1)
  ```
- See `scripts/template_script.py` for a complete example
- The pre-commit hook will prevent commits with improper environment variable loading

## Development Guidelines

### Environment Variables

1. **Always use the utility module**:
   - Import `load_env_vars` from `utils.env_loader`
   - Call `load_env_vars()` at the beginning of your script
   - Check the return value to ensure variables loaded successfully

2. **Keep .env.example updated**:
   - Add any new environment variables to `.env.example`
   - Include comments explaining what each variable is for
   - Use placeholder values that indicate the expected format

3. **Run `test_environment.py` after changes**:
   - Verify environment setup with `python scripts/test_environment.py`
   - This ensures all required keys are properly loaded

4. **For new required variables**:
   - Add them to the `required_vars` list in `utils/env_loader.py`
   - Update the pre-commit hook to check for them
   - Document them in README.md
