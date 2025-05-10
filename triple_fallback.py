"""
Triple Fallback System for Renovation Cost Estimator

This script implements a triple-fallback system for the Renovation Cost Estimator app:
1. First tries to run the full app with all features
2. If that fails, tries to run a simplified version with fewer dependencies
3. If that also fails, falls back to an ultra-minimal version

This ensures the app will always display something useful to users, even with dependency issues.
"""
import os
import sys
import traceback
from pathlib import Path
import platform

# Print Python version for diagnostics
print(f"Python version: {platform.python_version()}")

# Configure paths
project_root = Path(__file__).parent.absolute()
sys.path.append(str(project_root))

# Set default environment variables
os.environ.setdefault("EMBEDDING_MODEL_PATH", "text-embedding-3-small")
os.environ.setdefault("MOCK_DATA", "true")
os.environ.setdefault("USE_PINECONE", "false")
os.environ.setdefault("LOG_LEVEL", "INFO")

# Record dependency errors to display to the user
dependency_errors = []

def check_dependencies():
    """Check and print core dependency versions"""
    try:
        import pkg_resources
        packages_to_check = [
            "langchain", "langchain-core", "langchain-community", 
            "langchain-pinecone", "langsmith", "streamlit", "pandas"
        ]
        
        results = {}
        for package in packages_to_check:
            try:
                version = pkg_resources.get_distribution(package).version
                print(f"  {package}: {version}")
                results[package] = version
            except pkg_resources.DistributionNotFound:
                print(f"  {package}: Not installed")
                results[package] = "Not installed"
        return results
    except Exception as e:
        print(f"Error checking package versions: {e}")
        return {}

def try_run_full_app():
    """Try to run the full app with all features."""
    try:
        print("\n--- TRYING FULL APP ---")
        # Try to import the main app
        from renovation_estimator.app import main
        print("Successfully imported full app")
        return main
    except ImportError as e:
        error_msg = f"Error importing full app: {str(e)}"
        print(error_msg)
        dependency_errors.append(error_msg)
        # If we can't find app.py, look for it
        try:
            import glob
            for path in glob.glob("**/*.py", recursive=True):
                if path.endswith("app.py"):
                    print(f"Found app.py at: {path}")
        except:
            pass
        return None

def try_run_simple_app():
    """Try to run a simplified version with fewer dependencies."""
    try:
        print("\n--- TRYING SIMPLIFIED APP ---")
        # Try importing a simpler app with fewer dependencies
        import simple_app
        print("Successfully imported simple app")
        return simple_app.main
    except ImportError as e:
        error_msg = f"Error importing simplified app: {str(e)}"
        print(error_msg)
        dependency_errors.append(error_msg)
        return None

def run_ultra_minimal_app():
    """Run the ultra-minimal app as a final fallback."""
    print("\n--- RUNNING ULTRA-MINIMAL APP ---")
    try:
        import ultra_minimal_app
        print("Successfully imported ultra-minimal app")
        return True
    except ImportError as e:
        error_msg = f"Error importing ultra-minimal app: {str(e)}"
        print(error_msg)
        dependency_errors.append(error_msg)
        # Last resort - create a minimal app right here
        try:
            import streamlit as st
            
            # Set up page
            st.set_page_config(page_title="Renovation Estimator", page_icon="🏠")
            
            # Display error information
            st.title("🏠 Renovation Cost Estimator - Emergency Mode")
            st.error("**Critical Dependency Issues Detected**")
            
            st.write("The application encountered severe dependency issues:")
            for i, error in enumerate(dependency_errors, 1):
                st.code(f"Error {i}: {error}")
            
            st.info("""
            **How to Fix This:**
            
            This is likely due to incompatible package versions. The app requirements should be updated to:
            
            ```
            langchain==0.2.5
            langchain-community==0.2.5
            langchain-core==0.2.7
            langsmith==0.1.17  # Must be version 0.1.17 or later
            ```
            
            If you're the app developer, please update your requirements.txt file.
            """)
            
            # Show some basic info
            st.write("### About This App")
            st.write("""
            The Renovation Cost Estimator helps homeowners plan their renovation projects by providing accurate 
            cost estimates based on real-world data. When working correctly, it uses LangChain and fine-tuned 
            embeddings to provide intelligent cost estimates and find similar projects.
            """)
            
            # Footer
            st.caption("© 2024 Renovation Estimator - Emergency Fallback Mode")
        except Exception as final_e:
            print(f"CRITICAL ERROR: Even the emergency UI failed: {final_e}")
            print(traceback.format_exc())
        return True

if __name__ == "__main__":
    # Check dependency versions for diagnostic purposes
    package_versions = check_dependencies()
    
    try:
        # Try each app in turn, falling back if there are errors
        main_func = try_run_full_app()
        if main_func:
            main_func()
        else:
            simple_func = try_run_simple_app()
            if simple_func:
                simple_func()
            else:
                run_ultra_minimal_app()
    except Exception as e:
        print(f"Error running app: {e}")
        print(traceback.format_exc())
        dependency_errors.append(f"Runtime error: {str(e)}")
        run_ultra_minimal_app() 