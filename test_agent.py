import google.generativeai as genai
from google.adk import Agent
from google.adk.tools.function_tool import FunctionTool
from inspect import signature
import os

def test_function(name: str) -> str:
    \"\"\"A simple test function\"\"\"
    return f'Hello {name}'

# Create a function tool
tool = FunctionTool(test_function)

# Get API key from environment
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print('Warning: No API key found in environment')

# Configure Google Generative AI
genai.configure(api_key=api_key)

# Try to create an agent following the docs
try:
    # Print Agent constructor signature
    sig = signature(Agent.__init__)
    print(f'Agent constructor params: {list(sig.parameters.keys())}')
    
    # Try to create an agent with different parameter formats
    print('Attempting to create an agent...')
    
    agent = Agent(data={
        'name': 'TestAgent',
        'description': 'A test agent',
        'tools': [tool],
        'model': 'gemini-1.5-pro-latest'
    })
    
    print('Agent created successfully!')
    print(f'Agent: {agent}')
    print(f'Agent tools: {agent.tools}')
    print(f'Agent model: {agent.model}')
except Exception as e:
    print(f'Error creating agent: {e}')
