# LangSmith Integration

This document explains how LangSmith is integrated into the Renovation Estimator project for tracing and monitoring LLM operations.

## Overview

LangSmith provides observability for LLM applications, allowing you to:
- Track and monitor LLM calls
- Measure performance
- Debug issues
- Collect feedback

## Setup

1. **Get a LangSmith API Key**:
   - Sign up at [smith.langchain.com](https://smith.langchain.com/)
   - Create a new API key in your account settings

2. **Add to Environment Variables**:
   - Add your API key to the `.env` file:
   ```
   LANGSMITH_API_KEY=your_api_key_here
   LANGSMITH_PROJECT=renovation-estimator
   ```

3. **Verify Integration**:
   - Run the test script: `python scripts/test_langsmith.py`
   - Check the output to confirm that LangSmith is properly configured

## How It Works

The integration uses environment variables to enable LangChain tracing:

```python
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "renovation-estimator"
```

### LangSmithLogger Class

The `LangSmithLogger` class in `backend/langsmith_logger.py` provides:

1. **Initialization**:
   - Checks for the LangSmith API key
   - Creates a LangSmith client if the key is available

2. **Traceable Decorator**:
   - The `get_traceable_decorator` method returns a decorator that can be applied to any function
   - When applied, the function's execution is traced in LangSmith

3. **Feedback Collection**:
   - The `record_feedback` method allows recording feedback for a traced run

## Usage

### Tracing Functions

```python
from backend.langsmith_logger import get_langsmith_logger

# Get the logger
langsmith_logger = get_langsmith_logger()

# Apply the traceable decorator
@langsmith_logger.get_traceable_decorator(name="my_function", run_type="chain")
def my_function(input_data):
    # Function implementation
    return result
```

### Dynamic Tracing

For dynamic tracing (applying the decorator at runtime):

```python
def my_method(self, input_data):
    if langsmith_logger.is_enabled():
        # Apply traceable decorator dynamically
        traceable_func = langsmith_logger.get_traceable_decorator(
            name="my_method", 
            run_type="chain"
        )(self._internal_method)
        return traceable_func(input_data)
    else:
        return self._internal_method(input_data)
```

### Recording Feedback

```python
# Record feedback for a run
langsmith_logger.record_feedback(
    run_id="run-id-from-langsmith",
    feedback_type="accuracy",
    score=0.95,
    comment="Very accurate estimate"
)
```

## Viewing Traces

After running operations with LangSmith tracing enabled:

1. Go to [smith.langchain.com](https://smith.langchain.com/)
2. Navigate to the "Traces" section
3. Filter by project name "renovation-estimator"
4. Click on any trace to see details about the operation

## Troubleshooting

If LangSmith tracing isn't working:

1. **Check API Key**: Verify that `LANGSMITH_API_KEY` is correctly set in your `.env` file
2. **Check Environment Variables**: Make sure `LANGCHAIN_TRACING_V2` and `LANGCHAIN_PROJECT` are set
3. **Check Dependencies**: Ensure you have the latest versions of `langchain` and `langsmith` installed
4. **Check Logs**: Look for any error messages in the application logs

## References

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangChain Tracing Guide](https://python.langchain.com/docs/guides/tracing/) 