# Makefile for Renovation Estimator project

.PHONY: setup run generate-data run-evaluation clean lint test test-app

# Default Python interpreter
PYTHON = python

# Setup the project
setup:
	@echo "Setting up Renovation Estimator..."
	@if [ -f "scripts/setup.sh" ]; then \
		bash scripts/setup.sh; \
	else \
		pip install -r requirements.txt; \
	fi

# Run the Streamlit app
run:
	@echo "Starting Renovation Estimator app..."
	streamlit run app.py

# Generate synthetic data
generate-data:
	@echo "Generating synthetic data..."
	$(PYTHON) scripts/generate_data.py

# Run RAGAS evaluation
run-evaluation:
	@echo "Running RAGAS evaluation..."
	$(PYTHON) scripts/run_evaluation.py

# Clean generated data
clean:
	@echo "Cleaning generated data..."
	rm -rf data/synthetic/*
	rm -rf data/fine_tuning/*
	rm -rf data/evaluation/*
	@echo "Data cleaned."

# Lint the code
lint:
	@echo "Linting code..."
	flake8 .

# Run tests
test:
	@echo "Running tests..."
	pytest

# Run simple app test
test-app:
	@echo "Running app test..."
	$(PYTHON) scripts/test_app.py

# Help command
help:
	@echo "Renovation Estimator Makefile commands:"
	@echo "  setup          - Set up the project environment"
	@echo "  run            - Run the Streamlit application"
	@echo "  generate-data  - Generate synthetic data for the estimator"
	@echo "  run-evaluation - Run RAGAS evaluation on the model"
	@echo "  clean          - Clean generated data"
	@echo "  lint           - Run code linting"
	@echo "  test           - Run pytest tests"
	@echo "  test-app       - Run simple app functionality test"
	@echo "  help           - Show this help message" 