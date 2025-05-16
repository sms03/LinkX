"""
ADK Agent Module for LinkX
-------------------------
This module implements a Google ADK agent with custom tools for generating
and publishing social media content.
"""

import os
import json
import asyncio
from google.adk import Agent, Runner
from google.adk.tools.function_tool import FunctionTool
from google.generativeai.types import Model  # Using Google Generative AI types
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LinkXAdkAgent:
    """Google ADK-based agent for generating social media posts"""
    
    def __init__(self, api_key=None, model_name="gemini-1.5-pro-latest"):
        """Initialize the ADK agent"""
        if not api_key:
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                raise ValueError("No API key provided and GOOGLE_API_KEY not found in environment variables")
        
        # Initialize model and agent
        # Google ADK 0.5.0 uses a different approach to create models
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        
        # Define tools for the agent
        self.tools = self._create_tools()
        
        # Create the agent with tools - Using the format that's compatible with ADK version 0.5.0
        try:
            self.agent = Agent(
                name="LinkXAgent",
                description="""AI agent for creating viral social media posts.
                
            For LinkedIn posts:
            - Use professional language and tone
            - Maximum length: 3,000 characters
            - Include 3-5 relevant hashtags
            - Format with appropriate line breaks
            - Include a call-to-action
            
            For Twitter posts:
            - Be concise (max 280 characters)
            - Include 1-3 strategic hashtags
            - Make content engaging and shareable
            - Consider adding an engaging question
            
            Always respond with well-formatted JSON containing:
            - post_content: The ready-to-publish text
            - hashtags: Array of recommended hashtags
            - posting_time: Recommended posting time
            - target_audience: Who the post targets
            - engagement_strategy: Tips to maximize engagement""",
                tools=self.tools,
                llm=model_name,  # ADK 0.5.0 expects the model name directly, not a dict
                api_key=api_key
            )
        except Exception as e:
            print(f"Error creating ADK Agent: {e}")
            self.agent = None
    
    def _create_tools(self):
        """Create custom tools for the agent"""
        
        # Create function tools directly using typed function definitions
        # We don't need Parameter class, just use Python type annotations
        
        # Tool to analyze hashtag effectiveness
        def analyze_hashtags(platform: str, industry: str, count: int = 5):
            """
            Analyze the effectiveness of hashtags for a given platform and industry.
            
            Args:
                platform: The social media platform ('linkedin' or 'twitter')
                industry: The industry or niche for the hashtags
                count: Number of hashtags to suggest (default: 5)
                
            Returns:
                Dictionary with hashtag analysis
            """
            return self._analyze_hashtags_function(platform, industry, count)
        
        # Tool to suggest optimal posting times
        def suggest_posting_time(platform: str, target_audience: str = None):
            """
            Suggest optimal posting times for a social media platform.
            
            Args:
                platform: The social media platform ('linkedin' or 'twitter')
                target_audience: Description of the target audience (optional)
                
            Returns:
                Dictionary with posting time recommendations
            """
            return self._suggest_posting_time_function(platform, target_audience)
        
        # Tool to analyze post sentiment and tone
        def analyze_sentiment(content: str, platform: str):
            """
            Analyze the sentiment and tone of a social media post.
            
            Args:
                content: The content of the social media post
                platform: The social media platform ('linkedin' or 'twitter')
                
            Returns:
                Dictionary with sentiment analysis results
            """
            return self._analyze_sentiment_function(content, platform)
        
        # Create FunctionTool instances
        analyze_hashtags_tool = FunctionTool(analyze_hashtags)
        suggest_posting_time_tool = FunctionTool(suggest_posting_time)
        analyze_sentiment_tool = FunctionTool(analyze_sentiment)
        
        return [analyze_hashtags_tool, suggest_posting_time_tool, analyze_sentiment_tool]
    
    def _analyze_hashtags_function(self, platform, industry, count=5):
        """Analyze hashtag effectiveness (implementation)"""
        # This would ideally connect to a real hashtag analytics API
        # For now, we'll return mock data
        linkedin_hashtags = {
            "technology": ["tech", "innovation", "future", "ai", "machinelearning", "digital", "data"],
            "marketing": ["marketing", "digitalmarketing", "branding", "socialmedia", "strategy", "content"],
            "finance": ["finance", "investing", "wealth", "fintech", "banking", "trading", "money"],
            "healthcare": ["healthcare", "health", "wellness", "medical", "pharma", "biotech"],
            "hr": ["hr", "recruiting", "talentacquisition", "careers", "leadership", "remotework"]
        }
        
        twitter_hashtags = {
            "technology": ["Tech", "AI", "ML", "Data", "Programming", "DevOps", "Cloud"],
            "marketing": ["Marketing", "SEO", "ContentMarketing", "SocialMedia", "Growth"],
            "finance": ["Finance", "Crypto", "Investing", "Stocks", "FinTech", "Trading"],
            "healthcare": ["Healthcare", "MedTech", "Wellness", "Health", "MedicalTech"],
            "hr": ["Jobs", "Hiring", "HR", "Careers", "ResumeAdvice", "RemoteWork"]
        }
        
        # Find the closest industry
        if platform.lower() == "linkedin":
            hashtags_dict = linkedin_hashtags
        else:
            hashtags_dict = twitter_hashtags
        
        # Get the closest industry match or default to technology
        best_industry = "technology"
        for key in hashtags_dict.keys():
            if key.lower() in industry.lower():
                best_industry = key
                break
        
        selected_hashtags = hashtags_dict[best_industry][:count]
        
        return {
            "platform": platform,
            "industry": industry,
            "hashtags": selected_hashtags,
            "popularity": "high",
            "reach_potential": "good",
            "recommendation": f"Use these {len(selected_hashtags)} hashtags for best visibility"
        }
    
    def _suggest_posting_time_function(self, platform, target_audience=None):
        """Suggest optimal posting times (implementation)"""
        # This would ideally be based on real analytics
        # For now, providing general best practice data
        
        linkedin_times = {
            "general": ["Tuesday 9-10 AM", "Wednesday 8-10 AM", "Thursday 1-2 PM"],
            "professionals": ["Tuesday-Thursday 7:30-8:30 AM", "Tuesday-Thursday 12-1 PM"],
            "executives": ["Monday-Friday 7-8 AM", "Saturday 9-10 AM"],
            "job_seekers": ["Monday-Wednesday 8-9 AM", "Sunday 4-5 PM"]
        }
        
        twitter_times = {
            "general": ["Monday 9 AM", "Wednesday 12 PM", "Friday 3 PM"],
            "tech": ["Monday-Thursday 2-3 PM", "Friday 1-2 PM"],
            "consumers": ["Saturday-Sunday 11 AM-1 PM", "Wednesday 5-7 PM"],
            "news": ["Early morning 6-7 AM", "Evening 7-9 PM"]
        }
        
        if platform.lower() == "linkedin":
            times_dict = linkedin_times
            audience_match = "general"
        else:
            times_dict = twitter_times
            audience_match = "general"
        
        # Try to match the target audience if provided
        if target_audience:
            target_audience = target_audience.lower()
            for key in times_dict.keys():
                if key in target_audience:
                    audience_match = key
                    break
        
        return {
            "platform": platform,
            "target_audience": target_audience or "general",
            "recommended_times": times_dict[audience_match],
            "timezone": "User's local timezone",
            "note": "Posting consistency is as important as timing"
        }
    
    def _analyze_sentiment_function(self, content, platform):
        """Analyze sentiment and tone of post content"""
        # This would ideally use NLP for sentiment analysis
        # For now, we'll use a basic analysis algorithm
        
        # Check for positive words
        positive_words = ["amazing", "great", "excellent", "best", "thrilled", 
                         "excited", "happy", "delighted", "wonderful", "success"]
        # Check for negative words
        negative_words = ["disappointed", "unfortunate", "problem", "issue", "fail", 
                         "bad", "worst", "terrible", "unhappy", "frustrating"]
        
        # Check for professional tone words
        professional_words = ["expert", "professional", "strategy", "data", "analysis", 
                             "results", "effective", "solution", "industry", "research"]
        
        # Check for casual tone words
        casual_words = ["wow", "hey", "cool", "awesome", "yeah", 
                       "crazy", "omg", "lol", "haha", "btw"]
        
        content_lower = content.lower()
        
        # Count occurrences
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        professional_count = sum(1 for word in professional_words if word in content_lower)
        casual_count = sum(1 for word in casual_words if word in content_lower)
        
        # Determine sentiment
        if positive_count > negative_count:
            sentiment = "positive"
        elif negative_count > positive_count:
            sentiment = "negative"
        else:
            sentiment = "neutral"
            
        # Determine tone
        if professional_count > casual_count:
            tone = "professional"
        elif casual_count > professional_count:
            tone = "casual"
        else:
            tone = "balanced"
            
        # Calculate engagement prediction
        if platform.lower() == "linkedin" and tone == "professional":
            engagement_prediction = "high"
        elif platform.lower() == "twitter" and (sentiment == "positive" or tone == "casual"):
            engagement_prediction = "high"
        else:
            engagement_prediction = "moderate"
            
        # Provide recommendations based on analysis
        recommendations = []
        
        if platform.lower() == "linkedin" and tone != "professional":
            recommendations.append("Consider using more professional language for LinkedIn")
            
        if platform.lower() == "twitter" and len(content) > 200:
            recommendations.append("Consider shortening your Twitter post for better engagement")
            
        if sentiment == "negative" and platform.lower() == "linkedin":
            recommendations.append("LinkedIn audiences respond better to positive, solution-oriented content")
            
        return {
            "platform": platform,
            "sentiment": sentiment,
            "tone": tone,
            "engagement_prediction": engagement_prediction,
            "positive_words_count": positive_count,
            "negative_words_count": negative_count,
            "professional_tone_score": professional_count,
            "casual_tone_score": casual_count,
            "recommendations": recommendations
        }
    
    async def generate_post_async(self, platform, scenario, requirements, viral_strategy):
        """
        Generate a social media post using the ADK agent asynchronously
        
        Args:
            platform (str): 'linkedin' or 'twitter'
            scenario (str): Context or scenario for the post
            requirements (str): Specific requirements for the content
            viral_strategy (str): Strategy to make the post go viral
            
        Returns:
            dict: Generated post content and additional insights
        """
        # Create the query
        query = f"""
        Create a compelling {platform.upper()} post based on this information:
        
        SCENARIO: {scenario}
        
        REQUIREMENTS: {requirements}
        
        VIRAL STRATEGY: {viral_strategy}
        
        Use the analyze_hashtags tool to find suitable hashtags for this content.
        Use the suggest_posting_time tool to provide optimal posting times.
        After generating the post, use the analyze_sentiment tool to check if the tone is appropriate.
        
        Format your response as a JSON object with these fields:
        - post_content: The ready-to-publish text
        - hashtags: Array of recommended hashtags (without # symbol)
        - posting_time: Best time to post
        - target_audience: Who this post targets
        - engagement_strategy: How to maximize engagement
        - sentiment_analysis: Results of sentiment analysis
        """
        
        # Updated to use Runner instead of AgentRuntimeConfig
        runner = Runner(
            agent=self.agent,
            temperature=0.7,
            top_p=0.8,
            top_k=40,
            max_output_tokens=1024,
        )
        
        try:
            # Run the agent with updated API
            response = await runner.run_async(query=query)
            
            # Process the response
            if response and hasattr(response, 'text'):
                try:
                    # First try direct JSON parsing
                    result = json.loads(response.text)
                except json.JSONDecodeError:
                    # Try to extract JSON from markdown code blocks
                    text = response.text
                    if "```json" in text and "```" in text.split("```json", 1)[1]:
                        json_text = text.split("```json", 1)[1].split("```", 1)[0]
                        try:
                            result = json.loads(json_text)
                        except json.JSONDecodeError:
                            # Fallback to text response
                            result = {
                                "post_content": response.text[:3000 if platform.lower() == "linkedin" else 280],
                                "hashtags": [],
                                "posting_time": "Not specified",
                                "target_audience": "Not specified",
                                "engagement_strategy": "Not specified",
                                "sentiment_analysis": None
                            }
                    else:
                        # Fallback to text response
                        result = {
                            "post_content": response.text[:3000 if platform.lower() == "linkedin" else 280],
                            "hashtags": [],
                            "posting_time": "Not specified",
                            "target_audience": "Not specified",
                            "engagement_strategy": "Not specified",
                            "sentiment_analysis": None
                        }
                
                # If sentiment_analysis is missing, generate it manually
                if "sentiment_analysis" not in result and "post_content" in result:
                    try:
                        result["sentiment_analysis"] = self._analyze_sentiment_function(
                            content=result["post_content"],
                            platform=platform
                        )
                    except Exception as e:
                        print(f"Error analyzing sentiment: {str(e)}")
                        result["sentiment_analysis"] = None
                
                return result
            else:
                # Return error message if response is invalid
                return {
                    "post_content": "Error generating content. Please try again.",
                    "hashtags": [],
                    "posting_time": "Not specified",
                    "target_audience": "Not specified",
                    "engagement_strategy": "Not specified",
                    "sentiment_analysis": None
                }
        except Exception as e:
            print(f"Exception in ADK agent: {str(e)}")
            return {
                "post_content": f"Error generating content: {str(e)}",
                "hashtags": [],
                "posting_time": "Not specified",
                "target_audience": "Not specified",
                "engagement_strategy": "Not specified",
                "sentiment_analysis": None,
                "error": str(e)
            }
    
    def generate_post(self, platform, scenario, requirements, viral_strategy):
        """Synchronous wrapper around generate_post_async"""
        return asyncio.run(self.generate_post_async(platform, scenario, requirements, viral_strategy))


# Example usage
if __name__ == "__main__":
    # This allows testing the module directly
    agent = LinkXAdkAgent()
    
    result = agent.generate_post(
        platform="linkedin",
        scenario="Launching a new AI-powered analytics platform",
        requirements="Highlight our key differentiators and include a call to action for a free trial",
        viral_strategy="Use surprising statistics about data analytics ROI"
    )
    
    print(json.dumps(result, indent=2))
