"""
Inspect Google ADK packages structure
"""
import sys
import importlib
import pkgutil

def print_module_contents(module_name):
    try:
        module = importlib.import_module(module_name)
        print(f"\n{module_name} contents:")
        for item in dir(module):
            if not item.startswith('_'):  # Skip private members
                print(f"- {item}")
                try:
                    # Try to get more info about the item
                    obj = getattr(module, item)
                    if isinstance(obj, type):
                        print(f"  (class) {obj.__module__}.{obj.__name__}")
                except Exception as e:
                    print(f"  (error getting info: {e})")
    except ImportError as e:
        print(f"\nCould not import {module_name}: {e}")

def explore_package_structure(package_name):
    """Explore the structure of a package"""
    try:
        package = importlib.import_module(package_name)
        print(f"\nExploring {package_name}:")
        
        # List immediate submodules and packages
        print(f"\nSubmodules of {package_name}:")
        for _, name, ispkg in pkgutil.iter_modules(package.__path__, package.__name__ + '.'):
            module_type = "package" if ispkg else "module"
            print(f"- {name} ({module_type})")
            
            # Try to import the submodule/package to inspect further
            try:
                submodule = importlib.import_module(name)
                if ispkg:  # If it's a package, list its contents too
                    for _, subname, _ in pkgutil.iter_modules(submodule.__path__, submodule.__name__ + '.'):
                        print(f"  - {subname}")
            except ImportError as e:
                print(f"  (import error: {e})")
    except ImportError as e:
        print(f"Could not import {package_name}: {e}")

# Main execution
if __name__ == "__main__":
    print("Google ADK Package Inspection Tool")
    print("=================================")
    
    # Check if google.adk is available
    try:
        import google.adk
        print("✓ Successfully imported google.adk")
        
        # Print version info if available
        if hasattr(google.adk, "version"):
            print(f"Version: {google.adk.version}")
            
        # Explore the package structure
        explore_package_structure("google.adk")
        
        # Check specific modules we need
        print_module_contents("google.adk")
        
        # Try some tools-related modules
        for module in ["google.adk.tools", "google.adk.tool"]:
            print_module_contents(module)
            
        # Check Model class
        print("\nChecking for Model class:")
        try:
            from google.generativeai.types import Model
            print("✓ Found Model class in google.generativeai.types")
        except ImportError:
            print("✗ Model class not found in google.generativeai.types")
            
    except ImportError as e:
        print(f"✗ Failed to import google.adk: {e}")
