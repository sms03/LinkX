import inspect
import google.adk.tools.base_tool
import google.adk.tools.function_tool

# Inspect the base_tool module
print("Classes in base_tool module:")
for name, obj in inspect.getmembers(google.adk.tools.base_tool):
    if inspect.isclass(obj):
        print(f"- {name}")

# Inspect the function_tool module
print("\nClasses in function_tool module:")
for name, obj in inspect.getmembers(google.adk.tools.function_tool):
    if inspect.isclass(obj):
        print(f"- {name}")

# Check for Parameter-like classes
print("\nLooking for Parameter-like classes in all modules:")
for module_name in dir(google.adk.tools):
    try:
        module = getattr(google.adk.tools, module_name)
        if inspect.ismodule(module):
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and ("Parameter" in name or "Argument" in name):
                    print(f"- {module.__name__}.{name}")
    except Exception as e:
        pass
