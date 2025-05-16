"""
Post Generation Algorithms for LinkX
-----------------------------------
This module contains algorithms and strategies for generating
viral social media posts for LinkedIn and Twitter.
"""

import google.generativeai as genai
import json


class PostGenerator:
    def __init__(self, model_name='gemini-1.5-pro'):
        """Initialize the post generator with a specific Google ADK model."""
        self.model = genai.GenerativeModel(model_name)
    
    def generate_linkedin_post(self, scenario, requirements, viral_strategy):
        """
        Generate a LinkedIn post based on user inputs.
        
        Args:
            scenario (str): The scenario or context for the post
            requirements (str): Specific content requirements
            viral_strategy (str): Strategy to make the post go viral
            
        Returns:
            dict: Generated post content and metadata
        """
        return self._generate_post('linkedin', scenario, requirements, viral_strategy)
    
    def generate_twitter_post(self, scenario, requirements, viral_strategy):
        """
        Generate a Twitter (X) post based on user inputs.
        
        Args:
            scenario (str): The scenario or context for the post
            requirements (str): Specific content requirements
            viral_strategy (str): Strategy to make the post go viral
            
        Returns:
            dict: Generated post content and metadata
        """
        return self._generate_post('twitter', scenario, requirements, viral_strategy)
    
    def _generate_post(self, platform, scenario, requirements, viral_strategy):
        """
        Core post generation method used by both LinkedIn and Twitter generators.
        
        Args:
            platform (str): 'linkedin' or 'twitter'
            scenario (str): The scenario or context for the post
            requirements (str): Specific content requirements
            viral_strategy (str): Strategy to make the post go viral
            
        Returns:
            dict: Generated post content and metadata
        """
        # Platform-specific parameters
        if platform.lower() == 'linkedin':
            max_chars = 3000
            hashtag_count = "3-5"
            tone = "professional but engaging"
            platform_specific = """
            - Use professional language appropriate for LinkedIn
            - Format with appropriate line breaks for readability
            - Consider adding a call-to-action
            - Include mention of professional growth or industry insights where relevant
            """
        else:  # Twitter/X
            max_chars = 280
            hashtag_count = "1-3"
            tone = "conversational, engaging, concise"
            platform_specific = """
            - Be concise but impactful (max 280 characters)
            - Create opportunities for retweets and replies
            - Consider adding an engaging question
            - Use strong, attention-grabbing language
            """
        
        # Build the viral algorithm prompt
        prompt = f"""
        Create a highly engaging {platform.upper()} post about the following scenario:
        
        SCENARIO: {scenario}
        
        CONTENT REQUIREMENTS: {requirements}
        
        VIRAL STRATEGY: {viral_strategy}
        
        POST SPECIFICATIONS:
        - Maximum length: {max_chars} characters
        - Tone: {tone}
        - Include {hashtag_count} relevant hashtags
        {platform_specific}
        
        VIRAL ALGORITHM TECHNIQUES TO INCORPORATE:
        1. Hook the audience in the first line with a pattern interrupt or curiosity gap
        2. Use emotional triggers (inspiration, surprise, awe, etc.)
        3. Incorporate storytelling elements when possible
        4. Include a clear, compelling call-to-action
        5. Use social proof or authority markers if relevant
        
        OUTPUT FORMAT:
        Respond with a JSON object containing:
        1. "post_content": The ready-to-publish text with proper formatting
        2. "hashtags": Array of recommended hashtags (without # symbol)
        3. "posting_time": Recommended time to post (e.g., "Weekday mornings between 8-10 AM")
        4. "target_audience": Description of who this post targets
        5. "engagement_strategy": How to maximize engagement after posting
        """
        
        # Generate content using Google's ADK
        response = self.model.generate_content(prompt)
        
        # Parse the response and handle potential formatting issues
        try:
            # Try to parse direct JSON response
            result = json.loads(response.text)
        except json.JSONDecodeError:
            # If not valid JSON, try to extract JSON from markdown code block
            text = response.text
            if "```json" in text and "```" in text.split("```json", 1)[1]:
                json_text = text.split("```json", 1)[1].split("```", 1)[0]
                try:
                    result = json.loads(json_text)
                except json.JSONDecodeError:
                    # If still not valid, create a simple response
                    result = self._create_fallback_response(response.text, platform)
            else:
                # Create simple response with just the post content
                result = self._create_fallback_response(response.text, platform)
        
        return result
    
    def _create_fallback_response(self, text, platform):
        """Create a fallback response when JSON parsing fails."""
        # Extract just the content without any formatting or explanations
        content_lines = []
        capture = False
        
        for line in text.split('\n'):
            if "post_content" in line.lower() or "here's the post" in line.lower():
                capture = True
                continue
            if capture and ("hashtag" in line.lower() or line.strip() == ''):
                capture = False
            if capture:
                content_lines.append(line)
        
        # If no content was captured, just use the first 280/3000 chars based on platform
        if not content_lines:
            max_len = 280 if platform.lower() == 'twitter' else 3000
            post_content = text[:max_len]
        else:
            post_content = '\n'.join(content_lines)
        
        # Extract hashtags (looking for #something patterns)
        import re
        hashtags = re.findall(r'#(\w+)', text)
        
        # Create the fallback result
        return {
            "post_content": post_content,
            "hashtags": hashtags,
            "posting_time": "Weekday mornings (8-10 AM) or early evenings (5-7 PM)",
            "target_audience": "Professionals in the relevant industry",
            "engagement_strategy": "Respond to comments promptly and ask engaging questions"
        }


class ViralStrategy:
    """
    Predefined viral strategies for social media posts
    """
    
    @staticmethod
    def get_strategy(strategy_name):
        """Get a predefined viral strategy by name."""
        strategies = {
            "storytelling": ViralStrategy.storytelling_strategy(),
            "question": ViralStrategy.question_strategy(),
            "statistic": ViralStrategy.statistic_strategy(),
            "controversy": ViralStrategy.controversy_strategy(),
            "listicle": ViralStrategy.listicle_strategy(),
        }
        
        return strategies.get(strategy_name.lower(), "Custom strategy: " + strategy_name)
    
    @staticmethod
    def storytelling_strategy():
        return """
        Use a compelling narrative structure:
        1. Start with a relatable problem or situation
        2. Introduce a turning point or realization
        3. Share the resolution or insight gained
        4. Connect to the broader message or call-to-action
        """
    
    @staticmethod
    def question_strategy():
        return """
        Lead with a thought-provoking question that:
        1. Challenges conventional wisdom
        2. Points to a common pain point
        3. Creates curiosity about the answer
        4. Makes the reader reflect on their own experience
        """
    
    @staticmethod
    def statistic_strategy():
        return """
        Use a surprising or counter-intuitive statistic:
        1. Lead with the most impactful number
        2. Explain what it means in practical terms
        3. Provide context on why it matters
        4. Offer insight or solution related to the statistic
        """
    
    @staticmethod
    def controversy_strategy():
        return """
        Take a contrarian but thoughtful position:
        1. Challenge a widely-held belief in the industry
        2. Provide logical reasoning for the alternative view
        3. Use personal experience to back up the claim
        4. Invite discussion rather than being divisive
        """
    
    @staticmethod
    def listicle_strategy():
        return """
        Create a concise, valuable list:
        1. Use a number in the headline (e.g., "5 ways to...")
        2. Make each point scannable and substantive
        3. Deliver on the promise with actionable tips
        4. Include an unexpected or high-value item in the list
        """
