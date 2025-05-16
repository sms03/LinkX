#!/usr/bin/env python3
"""
LinkX - AI Agent for LinkedIn and Twitter (X) Posts
--------------------------------------------------
This application uses Google's Agent Development Kit (ADK) to create professional and
engaging LinkedIn and Twitter posts based on user input.
"""

import os
import google.generativeai as genai
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import tweepy
from linkedin_api import Linkedin
import asyncio

# Import our ADK Agent implementation
import os
import sys

# Add src directory to the path if needed
if os.path.basename(os.getcwd()) != "src" and os.path.exists(os.path.join(os.getcwd(), "src")):
    sys.path.insert(0, os.path.join(os.getcwd(), "src"))

# Now we can import our agent
from src.adk_agent import LinkXAdkAgent

# Load environment variables
load_dotenv()

# Configure Google's Generative AI for backward compatibility
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__)

class LinkXAgent:
    def __init__(self):
        """Initialize the LinkX agent with API connections."""
        # Configure Google Gemini model (for backward compatibility)
        self.model = genai.GenerativeModel('gemini-1.5-pro')
          # Initialize the ADK agent if enabled in config
        from src.config import ENABLE_ADK, GOOGLE_API_KEY, ADK_MODEL
        
        self.adk_enabled = ENABLE_ADK
        if self.adk_enabled:
            try:
                self.adk_agent = LinkXAdkAgent(api_key=GOOGLE_API_KEY, model_name=ADK_MODEL)
                print(f"ADK Agent initialized successfully with model: {ADK_MODEL}")
            except Exception as e:
                self.adk_enabled = False
                print(f"Failed to initialize ADK Agent: {str(e)}")
        
        # Initialize Twitter client
        twitter_api_key = os.getenv("TWITTER_API_KEY")
        twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        twitter_access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
        
        if all([twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_token_secret]):
            self.twitter_client = tweepy.Client(
                consumer_key=twitter_api_key,
                consumer_secret=twitter_api_secret,
                access_token=twitter_access_token,
                access_token_secret=twitter_access_token_secret
            )
        else:
            self.twitter_client = None
            print("Warning: Twitter API credentials not configured")
        
        # Initialize LinkedIn client
        linkedin_email = os.getenv("LINKEDIN_EMAIL")
        linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        
        if linkedin_email and linkedin_password:
            try:
                self.linkedin_client = Linkedin(linkedin_email, linkedin_password)
            except Exception as e:
                self.linkedin_client = None
                print(f"Warning: LinkedIn API connection failed - {str(e)}")
        else:
            self.linkedin_client = None
            print("Warning: LinkedIn API credentials not configured")
            
    def generate_post(self, platform, scenario, requirements, viral_strategy):
        """
        Generate a post for the specified platform.
        Uses Google's Agent Development Kit if available, falls back to Generative AI.
        
        Args:
            platform (str): 'linkedin' or 'twitter'
            scenario (str): Context or scenario for the post
            requirements (str): Specific requirements for the content
            viral_strategy (str): Strategy to make the post go viral
            
        Returns:
            dict: Generated post content and additional insights
        """
        max_length = 3000 if platform.lower() == 'linkedin' else 280
        
        # Try to use ADK agent if available
        if self.adk_enabled:
            try:
                print("Using ADK agent for content generation")
                result = self.adk_agent.generate_post(
                    platform=platform,
                    scenario=scenario,
                    requirements=requirements,
                    viral_strategy=viral_strategy
                )
                
                # Add metadata to indicate ADK was used
                result["generated_with"] = "ADK"
                return result
            except Exception as e:
                print(f"Error using ADK agent: {str(e)}. Falling back to legacy method.")
        else:
            print("ADK Agent not available, using legacy method")
            
        # Fallback to traditional Generative AI
        result = self._generate_post_legacy(platform, scenario, requirements, viral_strategy)
        result["generated_with"] = "Legacy"
        return result
    
    def _generate_post_legacy(self, platform, scenario, requirements, viral_strategy):
        """Legacy method using the Generative AI SDK as fallback"""
        # Platform-specific instructions
        if platform.lower() == 'linkedin':
            platform_guide = """
            - Use professional language appropriate for LinkedIn
            - Maximum characters: 3,000
            - Include hashtags (3-5) that professionals follow
            - Format text with line breaks for readability
            - Consider adding a call-to-action
            - Maintain professional tone throughout
            """
            max_length = 3000
        else:  # Twitter/X
            platform_guide = """
            - Be concise but impactful (max 280 characters)
            - Use hashtags (1-3) strategically
            - Consider adding an engaging question
            - Create opportunities for retweets and replies
            - Use strong, engaging language
            """
            max_length = 280
        
        # Build the prompt
        prompt = f"""
        Create a compelling {platform} post based on the following:
        
        SCENARIO:
        {scenario}
        
        REQUIREMENTS:
        {requirements}
        
        VIRAL STRATEGY:
        {viral_strategy}
        
        PLATFORM GUIDELINES:
        {platform_guide}
        
        Respond with a JSON object that includes:
        1. "post_content": The ready-to-publish text
        2. "hashtags": Recommended hashtags (as an array)
        3. "posting_time": Best time to post (in general terms)
        4. "target_audience": Who this post will resonate with most
        5. "engagement_strategy": How to maximize engagement after posting
        """
        
        # Generate content using Google's Generative AI with specific settings
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
            "response_mime_type": "application/json"
        }
        
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Try to parse response as JSON
            try:
                # First try direct JSON parsing
                result = json.loads(response.text)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks if present
                text = response.text
                if "```json" in text and "```" in text.split("```json", 1)[1]:
                    json_text = text.split("```json", 1)[1].split("```", 1)[0]
                    try:
                        result = json.loads(json_text)
                    except json.JSONDecodeError:
                        # If still not valid JSON, create a simple response
                        result = self._create_fallback_response(response.text, platform, max_length)
                else:
                    # Create a simple response with the content
                    result = self._create_fallback_response(response.text, platform, max_length)
        except Exception as e:
            # Handle any API errors
            print(f"Error generating content: {str(e)}")
            result = {
                "post_content": f"Error generating content. Please try again later. ({str(e)[:100]}...)",
                "hashtags": [],
                "posting_time": "Not specified",
                "target_audience": "Not specified",
                "engagement_strategy": "Not specified"
            }
        
        return result
        
    def _create_fallback_response(self, text, platform, max_length):
        """Create a fallback response when JSON parsing fails."""
        # Extract just the content, removing any explanations
        content_lines = []
        capture = False
        
        for line in text.split('\n'):
            # Start capturing after potential headers like "Post Content:" or similar
            if any(marker in line.lower() for marker in ["post content", "here's the post", "generated post"]):
                capture = True
                if ":" in line:  # Skip the header line itself
                    continue
            # Stop capturing if we see any markers for the next sections
            elif capture and any(marker in line.lower() for marker in ["hashtag", "posting time", "target audience", "engagement"]):
                capture = False
            
            if capture and line.strip():
                content_lines.append(line)
        
        # If no content was captured, just use the first portion of the text
        if not content_lines:
            post_content = text[:max_length]
        else:
            post_content = '\n'.join(content_lines)[:max_length]
        
        # Extract hashtags (looking for #something patterns)
        import re
        hashtags = re.findall(r'#(\w+)', text)
        if not hashtags:
            # Try to find a "hashtags" section and extract words
            hashtag_section = ""
            if "hashtag" in text.lower():
                parts = text.lower().split("hashtag")
                if len(parts) > 1:
                    hashtag_section = parts[1].split("\n\n")[0]
                    hashtags = re.findall(r'(\w+)', hashtag_section)
        
        # Create the fallback result
        return {
            "post_content": post_content,
            "hashtags": hashtags[:5],  # Limit to 5 hashtags max
            "posting_time": "Weekday mornings (8-10 AM) or early evenings (5-7 PM)",
            "target_audience": "Professionals in the relevant industry",
            "engagement_strategy": "Respond to comments promptly and ask engaging questions"
        }
    
    def publish_to_twitter(self, content):
        """Publish content to Twitter (X)"""
        if not self.twitter_client:
            return {"success": False, "message": "Twitter API not configured"}
        
        try:
            # Ensure content is within Twitter's character limit
            if len(content) > 280:
                content = content[:277] + "..."
            
            response = self.twitter_client.create_tweet(text=content)
            return {"success": True, "tweet_id": response.data['id']}
        except Exception as e:
            return {"success": False, "message": str(e)}
    
    def publish_to_linkedin(self, content):
        """Publish content to LinkedIn"""
        if not self.linkedin_client:
            return {"success": False, "message": "LinkedIn API not configured"}
        
        try:
            # The LinkedIn API wrapper doesn't directly support posting
            # This would require additional implementation with the LinkedIn API
            return {"success": False, "message": "LinkedIn posting not yet implemented"}
        except Exception as e:
            return {"success": False, "message": str(e)}


# Initialize the LinkX agent
agent = LinkXAgent()

@app.route('/')
def home():
    """Render the home page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_post():
    """Generate a post based on user input"""
    data = request.json
    platform = data.get('platform', 'linkedin')
    scenario = data.get('scenario', '')
    requirements = data.get('requirements', '')
    viral_strategy = data.get('viral_strategy', '')
    
    result = agent.generate_post(platform, scenario, requirements, viral_strategy)
    return jsonify(result)

@app.route('/publish', methods=['POST'])
def publish_post():
    """Publish a post to the selected platform"""
    data = request.json
    platform = data.get('platform', '').lower()
    content = data.get('content', '')
    
    if not content:
        return jsonify({"success": False, "message": "No content provided"})
    
    if platform == 'twitter':
        result = agent.publish_to_twitter(content)
    elif platform == 'linkedin':
        result = agent.publish_to_linkedin(content)
    else:
        result = {"success": False, "message": "Invalid platform specified"}
    
    return jsonify(result)

if __name__ == '__main__':
    # Check if Google API key is configured
    if not os.getenv("GOOGLE_API_KEY"):
        print("Warning: GOOGLE_API_KEY not found in environment variables")
        print("Please set up your .env file with the required API keys")
    
    # Run the Flask application
    app.run(debug=True)
