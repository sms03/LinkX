"""
Runner script for the LinkX application
"""

import os
import sys
from src.app import app
from src.config import validate_config

def main():
    """Main entry point for the application."""
    
    # Check for configuration issues
    issues = validate_config()
    if issues:
        print("Configuration issues found:")
        for issue in issues:
            print(f" - {issue}")
        
        # Still continue if Google API key is set (minimum requirement)
        if os.getenv("GOOGLE_API_KEY") is None:
            print("\nERROR: GOOGLE_API_KEY is required. Please set it in your .env file.")
            print("Exiting...")
            sys.exit(1)
        else:
            print("\nWarning: Some features may be limited due to incomplete configuration.")
    
    # Run the Flask app
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() in ("true", "t", "1")
    
    print(f"\nStarting LinkX application on http://{host}:{port}")
    print("Press Ctrl+C to stop the server.")
    
    app.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()
