"""
LinkX LangChain-Groq Integration Module
--------------------------------------
This module provides enhanced content generation capabilities through LangChain and Groq.
"""

import os
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

class LinkXLangChainAgent:
    """LangChain-based agent for enhanced social media content generation"""
    
    def __init__(self, groq_api_key: Optional[str] = None, model_name: str = "llama3-70b-8192"):
        """
        Initialize the LangChain agent with Groq integration
        
        Args:
            groq_api_key: API key for Groq (defaults to GROQ_API_KEY environment variable)
            model_name: Name of the Groq model to use
        """
        if not groq_api_key:
            groq_api_key = os.getenv("GROQ_API_KEY")
            if not groq_api_key:
                raise ValueError("No Groq API key provided and GROQ_API_KEY not found in environment variables")
        
        # Initialize Groq model via LangChain
        self.model = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=model_name
        )
        
        # Initialize output parser for structured responses
        self.parser = JsonOutputParser()
    
    def enhance_content(self, 
                      platform: str, 
                      base_content: str, 
                      viral_strategy: str, 
                      target_audience: str) -> Dict[str, Any]:
        """
        Enhance existing content using LangChain and Groq
        
        Args:
            platform: 'linkedin' or 'twitter'
            base_content: Base content to enhance
            viral_strategy: Strategy to make content viral
            target_audience: Target audience description
            
        Returns:
            Dict containing enhanced content and additional insights
        """
        # Create prompt for content enhancement
        enhancement_template = """
        You are an expert social media content creator specializing in {platform}.
        
        Enhance the following post to make it more engaging and aligned with the viral strategy:
        
        ORIGINAL CONTENT:
        {base_content}
        
        VIRAL STRATEGY:
        {viral_strategy}
        
        TARGET AUDIENCE:
        {target_audience}
        
        Platform-specific guidelines for {platform}:
        {platform_guidelines}
        
        Provide your response as a JSON object with these fields:
        - enhanced_content: The improved post content
        - emotional_triggers: List of emotional triggers used
        - virality_score: Estimated virality score between 0-100
        - optimization_notes: Notes on how you optimized the content
        - headline_options: 3 alternative headline options if applicable
        """
        
        # Platform-specific guidelines
        platform_guidelines = {
            "linkedin": """
                - Be professional but conversational
                - Start with a compelling hook in the first 3 lines
                - Use white space strategically (single line paragraphs)
                - Include a strong call-to-action
                - 3-5 relevant hashtags at the end
                - Maximum 3,000 characters
                - Best performing content types: success stories, career milestones, industry insights, and practical advice
            """,
            "twitter": """
                - Be concise and punchy (maximum 280 characters)
                - Use strong, evocative language
                - 1-2 strategic hashtags
                - Consider adding a question to drive engagement
                - Make content easily shareable
                - Consider creating opportunities for quote tweets
                - Use emojis strategically but sparingly
            """
        }
        
        # Prepare prompt with platform-specific guidelines
        prompt = ChatPromptTemplate.from_template(enhancement_template)
        chain = prompt | self.model | self.parser
        
        # Generate enhanced content
        result = chain.invoke({
            "platform": platform.lower(),
            "base_content": base_content,
            "viral_strategy": viral_strategy,
            "target_audience": target_audience,
            "platform_guidelines": platform_guidelines.get(platform.lower(), "")
        })
        
        return result
    
    def generate_viral_hooks(self, 
                           platform: str, 
                           industry: str, 
                           topic: str,
                           count: int = 5) -> List[str]:
        """
        Generate viral hooks for a specific platform, industry and topic
        
        Args:
            platform: 'linkedin' or 'twitter'
            industry: Industry or niche
            topic: Content topic
            count: Number of hooks to generate
            
        Returns:
            List of viral hook options
        """
        # Create prompt for viral hooks
        hooks_template = """
        Generate {count} highly engaging hooks for a {platform} post about {topic} in the {industry} industry.
        
        Each hook should:
        - Create curiosity or emotional response
        - Be appropriate for {platform}'s audience
        - Follow {platform}'s best practices for viral content
        - Be under {max_length} characters
        
        Provide your response as a JSON array of strings, each containing one hook.
        """
        
        # Set maximum length based on platform
        max_length = 100 if platform.lower() == "linkedin" else 60
        
        # Prepare prompt
        prompt = ChatPromptTemplate.from_template(hooks_template)
        chain = prompt | self.model | self.parser
        
        # Generate hooks
        result = chain.invoke({
            "count": count,
            "platform": platform.lower(),
            "topic": topic,
            "industry": industry,
            "max_length": max_length
        })
        
        return result
    
    def analyze_competitor_content(self,
                                 platform: str,
                                 competitor_content: List[str],
                                 industry: str) -> Dict[str, Any]:
        """
        Analyze competitor content to identify patterns and strategies
        
        Args:
            platform: 'linkedin' or 'twitter'
            competitor_content: List of competitor post contents
            industry: Industry or niche
            
        Returns:
            Dict with analysis results
        """
        # Create prompt for competitor analysis
        analysis_template = """
        As an expert social media strategist, analyze these {platform} posts from competitors in the {industry} industry:
        
        COMPETITOR POSTS:
        {competitor_content}
        
        Provide your analysis as a JSON object with these fields:
        - common_patterns: List of common content patterns
        - engagement_triggers: Most effective engagement triggers used
        - content_gaps: Content gaps or opportunities to differentiate
        - top_strategies: Top 3 strategies that appear to be working
        - improvement_suggestions: How to create better content than competitors
        """
        
        # Format competitor content for prompt
        formatted_content = "\n\n".join([f"Post {i+1}:\n{post}" for i, post in enumerate(competitor_content)])
        
        # Prepare prompt
        prompt = ChatPromptTemplate.from_template(analysis_template)
        chain = prompt | self.model | self.parser
        
        # Generate analysis
        result = chain.invoke({
            "platform": platform.lower(),
            "competitor_content": formatted_content,
            "industry": industry
        })
        
        return result
