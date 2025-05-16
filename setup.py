#!/usr/bin/env python
"""
LinkX Setup Script
-----------------
This script helps configure the LinkX application.

It checks the environment, installs dependencies, and sets up the required API keys.
"""

import os
import sys
import argparse
import subprocess
import shutil
from dotenv import load_dotenv

def check_python_version():
    """Check if the Python version is compatible"""
    min_version = (3, 8)
    current_version = sys.version_info[:2]
    
    if current_version < min_version:
        print(f"Error: Python {min_version[0]}.{min_version[1]} or higher is required.")
        print(f"Current Python version: {current_version[0]}.{current_version[1]}")
        sys.exit(1)
    
    print(f"✅ Python version {current_version[0]}.{current_version[1]} is compatible")

def check_dependencies():
    """Check if required external dependencies are installed"""
    dependencies = []
    
    # Check for pip
    if not shutil.which("pip"):
        dependencies.append("pip")
    
    # Check for uv if specified
    if args.use_uv and not shutil.which("uv"):
        dependencies.append("uv")
    
    if dependencies:
        print("Error: The following dependencies are missing:")
        for dep in dependencies:
            print(f"  - {dep}")
        print("\nPlease install these dependencies before continuing.")
        sys.exit(1)
    
    print("✅ All external dependencies are installed")

def install_requirements():
    """Install Python package dependencies"""
    requirements_file = "requirements-enhanced.txt" if os.path.exists("requirements-enhanced.txt") else "requirements.txt"
    
    print(f"Installing dependencies from {requirements_file}...")
    
    try:
        if args.use_uv:
            subprocess.run(["uv", "pip", "install", "-r", requirements_file], check=True)
        else:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], check=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def setup_environment():
    """Set up the environment variables"""
    # Check if .env file exists
    env_file = ".env"
    env_exists = os.path.exists(env_file)
    
    # Load existing environment variables if .env exists
    if env_exists:
        load_dotenv()
    
    # Dictionary to store environment variables
    env_vars = {}
    
    # Required API keys
    api_keys = {
        "GOOGLE_API_KEY": "Google API Key (required for ADK)",
        "GROQ_API_KEY": "Groq API Key (required for LangChain integration)",
        "TWITTER_API_KEY": "Twitter API Key (optional for direct publishing)",
        "TWITTER_API_SECRET": "Twitter API Secret (optional for direct publishing)",
        "TWITTER_ACCESS_TOKEN": "Twitter Access Token (optional for direct publishing)",
        "TWITTER_ACCESS_TOKEN_SECRET": "Twitter Access Token Secret (optional for direct publishing)",
        "LINKEDIN_EMAIL": "LinkedIn Email (optional for direct publishing)",
        "LINKEDIN_PASSWORD": "LinkedIn Password (optional for direct publishing)"
    }
    
    # Get API keys from user if not set
    for key, description in api_keys.items():
        # Check if key already exists in environment
        existing_value = os.getenv(key)
        
        if existing_value and not args.reset_config:
            print(f"✅ {key} is already configured")
            env_vars[key] = existing_value
            continue
        
        # Determine if key is required
        required = "required" in description
        
        # Prompt for key
        prompt = f"Enter {description}: "
        if not required:
            prompt += "(press Enter to skip) "
        
        value = input(prompt)
        
        # Skip if not required and no value provided
        if not value and not required:
            print(f"Skipping {key}")
            continue
        
        # Validate required keys
        if required and not value:
            print(f"Error: {key} is required")
            sys.exit(1)
        
        # Store the key
        env_vars[key] = value
        print(f"✅ {key} configured")
    
    # Additional configuration options
    config_options = {
        "ENABLE_ADK": ("Enable Google ADK (y/n)", "True"),
        "ENABLE_TWITTER": ("Enable Twitter integration (y/n)", "True"),
        "ENABLE_LINKEDIN": ("Enable LinkedIn integration (y/n)", "True"),
        "ADK_MODEL": ("Default ADK Model", "gemini-1.5-pro-latest")
    }
    
    for key, (description, default) in config_options.items():
        # Check if key already exists in environment
        existing_value = os.getenv(key)
        
        if existing_value and not args.reset_config:
            print(f"✅ {key} is already configured as '{existing_value}'")
            env_vars[key] = existing_value
            continue
        
        if description.endswith("(y/n)"):
            # Yes/no question
            response = input(f"{description} [Y/n]: ").strip().lower()
            value = "True" if not response or response == 'y' else "False"
        else:
            # Free-form input with default
            value = input(f"{description} [default: {default}]: ").strip()
            if not value:
                value = default
        
        env_vars[key] = value
        print(f"✅ {key} configured as '{value}'")
    
    # Write environment variables to .env file
    with open(env_file, "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"✅ Environment variables saved to {env_file}")

def verify_installation():
    """Verify the installation by running a simple check"""
    print("Verifying installation...")
    
    try:
        # Create a simple verification script
        verify_script = """
import os
import sys

success = True
missing_packages = []

def check_package(package_name):
    global success, missing_packages
    try:
        __import__(package_name)
        return True
    except ImportError:
        success = False
        missing_packages.append(package_name)
        return False

# Check required packages
check_package('google')
check_package('google.adk')
check_package('langchain')
check_package('langchain_groq')
check_package('google.generativeai')
check_package('dotenv')
check_package('flask')

# Check for optional UI packages based on arguments
if 'streamlit' in sys.argv:
    check_package('streamlit')
if 'reflex' in sys.argv:
    check_package('reflex')

# Print results
if success:
    print("SUCCESS: All required packages are installed")
else:
    print(f"ERROR: The following packages are missing: {', '.join(missing_packages)}")
    sys.exit(1)

# Check if API keys are configured
if os.getenv("GOOGLE_API_KEY"):
    print("SUCCESS: Google API key is configured")
else:
    print("WARNING: Google API key is not configured")
    
if 'langchain' in sys.argv and not os.getenv("GROQ_API_KEY"):
    print("WARNING: Groq API key is not configured, LangChain integration will not work")
"""
        
        # Write verification script to temporary file
        verify_file = "verify_installation.py"
        with open(verify_file, "w") as f:
            f.write(verify_script)
        
        # Run the verification script
        cmd = [sys.executable, verify_file]
        if args.ui == "streamlit":
            cmd.append("streamlit")
        elif args.ui == "reflex":
            cmd.append("reflex")
        if args.use_langchain:
            cmd.append("langchain")
            
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up
        os.remove(verify_file)
        
        # Print results
        for line in result.stdout.splitlines():
            if line.startswith("SUCCESS:"):
                print(f"✅ {line[9:]}")
            elif line.startswith("WARNING:"):
                print(f"⚠️  {line[9:]}")
            elif line.startswith("ERROR:"):
                print(f"❌ {line[7:]}")
                return False
            else:
                print(line)
        
        if result.returncode != 0:
            print(f"❌ Verification failed with code {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
        
        return True
    
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def setup_ui():
    """Configure the user interface"""
    if args.ui == "streamlit":
        print("Setting up Streamlit UI...")
        
        # Check if streamlit is installed
        try:
            import streamlit
            print("✅ Streamlit is installed")
        except ImportError:
            print("❌ Streamlit is not installed. Installing...")
            try:
                if args.use_uv:
                    subprocess.run(["uv", "pip", "install", "streamlit"], check=True)
                else:
                    subprocess.run([sys.executable, "-m", "pip", "install", "streamlit"], check=True)
                print("✅ Streamlit installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error installing Streamlit: {e}")
                return False
        
        # Create a streamlit run script
        run_streamlit = "#!/bin/bash\n\nstreamlit run streamlit_app.py"
        run_streamlit_bat = "@echo off\nstreamlit run streamlit_app.py"
        
        with open("run_streamlit.sh", "w") as f:
            f.write(run_streamlit)
        with open("run_streamlit.bat", "w") as f:
            f.write(run_streamlit_bat)
        
        os.chmod("run_streamlit.sh", 0o755)
        
        print("✅ Streamlit UI setup completed")
        print("To run the Streamlit UI, use: python -m streamlit run streamlit_app.py")
        
    elif args.ui == "reflex":
        print("Setting up Reflex UI...")
        
        # Check if reflex is installed
        try:
            import reflex
            print("✅ Reflex is installed")
        except ImportError:
            print("❌ Reflex is not installed. Installing...")
            try:
                if args.use_uv:
                    subprocess.run(["uv", "pip", "install", "reflex"], check=True)
                else:
                    subprocess.run([sys.executable, "-m", "pip", "install", "reflex"], check=True)
                print("✅ Reflex installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error installing Reflex: {e}")
                return False
        
        # Create a reflex init script
        init_reflex = "reflex init"
        reflex_run = "reflex run --loglevel debug"
        
        # Write run scripts
        with open("init_reflex.sh", "w") as f:
            f.write("#!/bin/bash\n\n" + init_reflex)
        with open("init_reflex.bat", "w") as f:
            f.write("@echo off\n" + init_reflex)
        with open("run_reflex.sh", "w") as f:
            f.write("#!/bin/bash\n\n" + reflex_run)
        with open("run_reflex.bat", "w") as f:
            f.write("@echo off\n" + reflex_run)
        
        os.chmod("init_reflex.sh", 0o755)
        os.chmod("run_reflex.sh", 0o755)
        
        print("✅ Reflex UI setup completed")
        print("To initialize Reflex, run: init_reflex.sh or init_reflex.bat")
        print("To run the Reflex UI, use: run_reflex.sh or run_reflex.bat")
    
    return True

def main():
    """Main function to run the setup script"""
    print("="*50)
    print("LinkX - Setup Assistant")
    print("="*50)
    
    check_python_version()
    check_dependencies()
    install_requirements()
    setup_environment()
    
    if args.ui:
        setup_ui()
    
    success = verify_installation()
    
    if success:
        print("\n" + "="*50)
        print("LinkX setup completed successfully! 🚀")
        print("="*50)
        print("\nTo run the application:")
        print("1. With Flask: python run.py")
        if args.ui == "streamlit":
            print("2. With Streamlit: python -m streamlit run streamlit_app.py")
        elif args.ui == "reflex":
            print("2. With Reflex: reflex run")
        print("\nMake sure to set up your API keys in the .env file if you haven't already.")
        return 0
    else:
        print("\n" + "="*50)
        print("LinkX setup encountered issues. Please resolve them and try again.")
        print("="*50)
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LinkX Setup Script")
    parser.add_argument("--use-uv", action="store_true", help="Use uv instead of pip for package installation")
    parser.add_argument("--use-langchain", action="store_true", help="Set up LangChain integration")
    parser.add_argument("--ui", choices=["streamlit", "reflex", "flask", "all"], help="Set up the specified UI")
    parser.add_argument("--reset-config", action="store_true", help="Reset all configuration values")
    
    args = parser.parse_args()
    
    sys.exit(main())
