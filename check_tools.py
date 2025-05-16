import google.adk
print("ADK attributes:", [attr for attr in dir(google.adk) if not attr.startswith('_')])

# Check for tools module
try:
    import google.adk.tools
    print("\ntools module exists!")
    print("tools attributes:", [attr for attr in dir(google.adk.tools) if not attr.startswith('_')])
except ImportError as e:
    print("\nCannot import tools module:", e)

# Check for tool module
try:
    import google.adk.tool
    print("\ntool module exists!")
    print("tool attributes:", [attr for attr in dir(google.adk.tool) if not attr.startswith('_')])
except ImportError as e:
    print("\nCannot import tool module:", e)

# Check if Tool class is directly in google.adk
if hasattr(google.adk, 'Tool'):
    print("\nTool class is in google.adk!")
else:
    print("\nTool class is NOT in google.adk")

# Look for Tool class in all obvious places
for module_name in ['google.adk', 'google.adk.tools', 'google.adk.tool']:
    try:
        module = __import__(module_name, fromlist=[''])
        if hasattr(module, 'Tool'):
            print(f"\nFound Tool class in {module_name}")
    except ImportError:
        pass
