import inspect
import pkgutil
import importlib
import google.adk

# Check if examples module exists
examples_module = None
for _, name, ispkg in pkgutil.iter_modules(google.adk.__path__, google.adk.__name__ + '.'):
    if name.endswith('examples'):
        examples_module = name
        break

if examples_module:
    print(f"Found examples module: {examples_module}")
    examples = importlib.import_module(examples_module)
    
    # Look for example files
    example_files = []
    for _, name, ispkg in pkgutil.iter_modules(examples.__path__, examples.__name__ + '.'):
        if 'tool' in name.lower():
            example_files.append(name)
    
    print(f"Found {len(example_files)} example files with 'tool' in name:")
    for name in example_files:
        print(f"- {name}")

# Check built-in tools
tools_module = importlib.import_module('google.adk.tools')
print("\nChecking all modules in google.adk.tools:")
for item in dir(tools_module):
    if not item.startswith('_'):
        print(f"- {item}")
        
# Let's examine FunctionTool more closely
print("\nExamining FunctionTool class:")
from google.adk.tools.function_tool import FunctionTool
print(f"Init signature: {str(inspect.signature(FunctionTool.__init__))}")

# Print all methods of FunctionTool
print("\nMethods of FunctionTool:")
for name, method in inspect.getmembers(FunctionTool, predicate=inspect.isfunction):
    if not name.startswith('_'):
        print(f"- {name}{str(inspect.signature(method))}")

# Check if there's any alternate for Parameter
print("\nLooking for parameter or argument classes in tools module:")
for module_name in dir(tools_module):
    try:
        if not module_name.startswith('_'):
            module = getattr(tools_module, module_name)
            if inspect.ismodule(module):
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and ('param' in name.lower() or 'arg' in name.lower()):
                        print(f"- {module.__name__}.{name}")
    except Exception as e:
        print(f"Error examining {module_name}: {str(e)}")
