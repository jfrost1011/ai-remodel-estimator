# Script to check if all required packages are installed
import sys
import subprocess
import pkg_resources

# Check all required packages
packages = [
    "openai",
    "pinecone-client",
    "sentence-transformers",
    "ragas", 
    "scikit-learn",
    "streamlit",
    "pandas",
    "numpy",
    "matplotlib"
]

print(f"Python version: {sys.version}")
print(f"Python path: {sys.executable}")
print("\nChecking packages:")

all_good = True
for package in packages:
    try:
        pkg_resources.get_distribution(package)
        print(f"{package}: ✓")
    except pkg_resources.DistributionNotFound:
        print(f"{package}: ✗ - Not found")
        all_good = False

if all_good:
    print("\nAll packages installed successfully!")
else:
    print("\nSome packages are missing. Please install them.") 