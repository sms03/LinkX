"""Check Google ADK module structure"""
import google.adk

# Print all attributes in the google.adk module
print("Attributes in google.adk module:")
for attr in dir(google.adk):
    if not attr.startswith('_'):  # Skip private attributes
        print(f"- {attr}")

# Check if llm module exists
try:
    import google.adk.llm
    print("\nAttributes in google.adk.llm module:")
    for attr in dir(google.adk.llm):
        if not attr.startswith('_'):
            print(f"- {attr}")
except ImportError as e:
    print(f"\nFailed to import google.adk.llm: {e}")

# Check for other potential import paths
for module in ["genai", "generativeai", "llm", "agent", "tool"]:
    try:
        # Try to import from google.adk
        __import__(f"google.adk.{module}")
        print(f"\n✓ google.adk.{module} is available")
    except ImportError:
        print(f"\n✗ google.adk.{module} is not available")

# Check if we can import Model directly from generative AI
try:
    from google.generativeai.types import Model
    print("\n✓ Successfully imported Model from google.generativeai.types")
except ImportError as e:
    print(f"\n✗ Failed to import Model from google.generativeai.types: {e}")
    
# Check if google-genai package has a Model class
try:
    from google.genai import Model
    print("\n✓ Successfully imported Model from google.genai")
except ImportError as e:
    print(f"\n✗ Failed to import Model from google.genai: {e}")
