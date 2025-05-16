import google.generativeai as genai
from google.adk import Agent
from inspect import signature
print('Agent params:', list(signature(Agent.__init__).parameters.keys()))
