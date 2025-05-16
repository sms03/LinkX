"""Check ADK imports"""
import sys
import pkgutil

def check_import(module_name):
    """Check if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ Successfully imported {module_name}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import {module_name}: {e}")
        return False

# Try different import combinations
print("Checking ADK import options:")
check_import("google.adk")
check_import("adk")

# List all modules in the google namespace
print("\nPackages in 'google' namespace:")
import google
for _, name, ispkg in pkgutil.iter_modules(google.__path__, google.__name__ + '.'):
    print(f"- {name} ({'package' if ispkg else 'module'})")

# If adk is available, check its structure
if check_import("adk"):
    print("\nADK Module structure:")
    import adk
    print(dir(adk))
