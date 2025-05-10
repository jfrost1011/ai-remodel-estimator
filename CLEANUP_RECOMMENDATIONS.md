# Renovation Estimator - Cleanup Recommendations

This document outlines recommended cleanups to improve code quality, reduce redundancy, and enhance maintainability of the Renovation Estimator project.

## 1. Redundant Test Scripts

Several test scripts have overlapping functionality and should be consolidated:

### Recommendation: Consolidate Test Scripts

| Redundant Scripts | Consolidated Solution |
|-------------------|----------------------|
| `scripts/test_estimator_simple.py` and `scripts/test_estimator.py` | Merge into a single `test_estimator.py` with flags for simple vs. full tests |
| `scripts/simple_test_vector_store.py` and vector store tests in `scripts/test_app.py` | Extract to a comprehensive `test_vector_store.py` |
| `scripts/simple_test_evaluation.py` and evaluation tests in other scripts | Create a standalone `test_evaluation.py` |

This consolidation will make the testing framework more maintainable and easier to understand.

## 2. Duplicate Data Loading Functions

Multiple files contain similar code for loading project data from JSON files.

### Recommendation: Create a Common Data Loader

Create a shared utility function in `utils/data_loader.py` to handle loading data from various sources.

```python
# Example implementation
def load_project_data(data_file=None, fallback_to_synthetic=True, count=20):
    """Load project data from file or generate synthetic data."""
    # Check multiple file paths
    # Generate synthetic if needed
    # Return formatted data
```

Use this utility function in:
- `backend/vector_store.py` (both MockVectorStore and OpenAIVectorStore)
- Data generation scripts

## 3. Environment Variable Loading

While the project has a good environment variable loader utility, it's not consistently used.

### Recommendation: Ensure Consistent Environment Loading

Remove direct imports of `dotenv` from any file except `utils/env_loader.py`.

Update these files to use the standard approach:
- `simple_openai_test.py` (uses direct dotenv loading)

## 4. Test Script Strategy

Many test scripts have overlapping setup code for importing modules and loading environment variables.

### Recommendation: Create a Test Helper Module

Create `scripts/test_helpers.py` with common test setup functions:
- Setting up paths
- Loading environment variables
- Initializing common components
- Test fixtures

## 5. Redundant Basic Tests

There are multiple simple "smoke test" scripts that could be consolidated.

### Recommendation: Unified Test Suite

Create a unified test suite in `scripts/run_tests.py` that can run different test categories:
- Basic smoke tests
- API integration tests
- Full system tests

## 6. API Key Checks

Multiple scripts check for the presence of API keys in slightly different ways.

### Recommendation: Standardize API Key Validation

Create a standard function in `utils/env_loader.py` to check API keys:

```python
def validate_api_keys(required_keys=None):
    """Validate that required API keys are present."""
    if required_keys is None:
        required_keys = ["OPENAI_API_KEY", "PINECONE_API_KEY", "LANGSMITH_API_KEY"]
    # Check each key and return results
```

## 7. Data Generation Redundancy

There are overlapping functions for generating synthetic data in different files.

### Recommendation: Centralize Data Generation

Ensure all data generation happens through `backend/data_generator.py`, and have other scripts import from there.

## 8. LangSmith Integration Redundancy

The LangSmith logging has some unnecessarily complex methods.

### Recommendation: Simplify LangSmith Logger

Streamline the `langsmith_logger.py` file by removing redundant logging methods and focusing on the core tracing functionality that is actually used.

## 9. Overlapping Environment Files

Multiple environment test scripts with similar functionality.

### Recommendation: Consolidate Environment Test Scripts

Merge the following scripts into a single comprehensive test:
- `test_keys.py`
- `simple_test_keys.py`
- `final_test_keys.py`

## 10. README and Documentation Sync

Ensure that README reflects the actual codebase structure and requirements.

### Recommendation: Update Documentation

- Ensure setup instructions match the actual dependencies
- Document the consolidated test scripts
- Update environment variable information 

## Implementation Priority

1. Consolidate test scripts (high priority)
2. Create common data loader (high priority)
3. Standardize environment variable loading (medium priority)
4. Simplify LangSmith logger (medium priority)
5. Create test helper module (lower priority)
6. Update documentation (final step) 