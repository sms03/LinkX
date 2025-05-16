"""
Test script for LinkX functionality
"""

import os
import sys
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.algorithms import PostGenerator, ViralStrategy
from src.config import validate_config
from src.utils import test_all_connections


def test_config():
    """Test the configuration and environment variables."""
    print("Testing configuration...")
    issues = validate_config()
    
    if issues:
        print("Configuration issues found:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("Configuration valid!")


def test_connections():
    """Test API connections."""
    print("\nTesting API connections...")
    results = test_all_connections()
    
    # Google ADK connection
    if results["google_adk"]["status"] == "success":
        print("✓ Google ADK connection successful")
        print(f"  Available models: {', '.join(results['google_adk']['available_models'][:3])}")
    else:
        print(f"✗ Google ADK connection failed: {results['google_adk']['message']}")
    
    # Twitter connection
    if results["twitter"]["status"] == "success":
        print("✓ Twitter API connection successful")
    else:
        print(f"✗ Twitter API connection failed: {results['twitter']['message']}")
    
    # LinkedIn connection
    if results["linkedin"]["status"] == "success":
        print("✓ LinkedIn API connection successful")
    else:
        print(f"✗ LinkedIn API connection failed: {results['linkedin']['message']}")


def test_post_generation():
    """Test post generation functionality."""
    print("\nTesting post generation...")
    
    # Only proceed if Google API key is available
    from dotenv import load_dotenv
    load_dotenv()
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("Skipping post generation test - GOOGLE_API_KEY not found in environment")
        return
    
    generator = PostGenerator()
    
    # Test scenarios
    test_cases = [
        {
            "platform": "linkedin",
            "scenario": "Launching a new software tool that helps data scientists visualize large datasets",
            "requirements": "Highlight ease of use and performance",
            "viral_strategy": "Use a surprising statistic about data visualization challenges"
        },
        {
            "platform": "twitter",
            "scenario": "Announcing a free webinar about digital marketing trends in 2025",
            "requirements": "Include date, time, and registration link placeholder",
            "viral_strategy": "Ask an engaging question about current marketing challenges"
        }
    ]
    
    for i, test in enumerate(test_cases):
        print(f"\nTest {i+1}: {test['platform']} post with {test['viral_strategy']}")
        result = generator._generate_post(
            platform=test["platform"],
            scenario=test["scenario"],
            requirements=test["requirements"],
            viral_strategy=test["viral_strategy"]
        )
        
        # Print a brief summary of the result
        print(f"Post content (excerpt): {result['post_content'][:100]}...")
        print(f"Hashtags: {', '.join(['#' + h for h in result['hashtags']])}")
        print(f"Recommended posting time: {result['posting_time']}")


if __name__ == "__main__":
    print("LinkX Test Script\n" + "=" * 20)
    test_config()
    test_connections()
    test_post_generation()
    print("\nTest completed!")
