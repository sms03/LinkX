"""
LinkX Streamlit Interface
-----------------------
This module provides a modern web interface for the LinkX application using Streamlit.
"""

import os
import json
import asyncio
import streamlit as st
from dotenv import load_dotenv
import sys

# Add src directory to path if needed
if os.path.exists(os.path.join(os.getcwd(), "src")):
    sys.path.insert(0, os.path.join(os.getcwd()))

# Import our agent implementations
from src.adk_agent import LinkXAdkAgent
from src.langchain_integration import LinkXLangChainAgent

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="LinkX - AI Social Media Post Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .reportview-container {
        background: #f0f2f6;
    }
    .sidebar .sidebar-content {
        background: #262730;
    }
    h1, h2, h3 {
        color: #0077B5;
    }
    .stButton>button {
        background-color: #0077B5;
        color: white;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0077B5;
        margin-bottom: 1rem;
    }
    .platform-linkedin {
        border-left: 5px solid #0077B5;
        padding-left: 1rem;
    }
    .platform-twitter {
        border-left: 5px solid #1DA1F2;
        padding-left: 1rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if "generated_posts" not in st.session_state:
        st.session_state.generated_posts = []
    if "api_configured" not in st.session_state:
        # Check if API keys are configured
        google_api_key = os.getenv("GOOGLE_API_KEY")
        groq_api_key = os.getenv("GROQ_API_KEY")
        st.session_state.api_configured = {
            "google": bool(google_api_key),
            "groq": bool(groq_api_key)
        }

def sidebar():
    """Create sidebar with configuration options"""
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/0077B5/FFFFFF?text=LinkX", width=200)
        st.title("Configuration")
        
        # API Keys
        with st.expander("API Keys"):
            if not st.session_state.api_configured["google"]:
                google_key = st.text_input("Google API Key", type="password")
                if google_key:
                    os.environ["GOOGLE_API_KEY"] = google_key
                    st.session_state.api_configured["google"] = True
                    st.success("Google API Key configured!")
            else:
                st.success("✅ Google API Key configured")
                
            if not st.session_state.api_configured["groq"]:
                groq_key = st.text_input("Groq API Key", type="password")
                if groq_key:
                    os.environ["GROQ_API_KEY"] = groq_key
                    st.session_state.api_configured["groq"] = True
                    st.success("Groq API Key configured!")
            else:
                st.success("✅ Groq API Key configured")
        
        # Model settings
        with st.expander("Model Settings"):
            google_model = st.selectbox(
                "Google AI Model",
                ["gemini-1.5-pro-latest", "gemini-1.5-pro", "gemini-1.5-flash"],
                index=0
            )
            
            groq_model = st.selectbox(
                "Groq Model",
                ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
                index=0
            )
            
            temperature = st.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.1)
            
        # About
        st.markdown("---")
        st.markdown("### About LinkX")
        st.markdown("""
        LinkX is an AI-powered social media post generator that creates professional LinkedIn and engaging Twitter content optimized for virality.
        
        Built with:
        - Google's Agent Development Kit (ADK)
        - LangChain
        - Groq
        - Streamlit
        """)
        
        st.markdown("---")
        st.markdown("© 2025 LinkX")

def main_interface():
    """Create the main interface"""
    st.markdown('<div class="main-header">LinkX - AI Social Media Content Generator</div>', unsafe_allow_html=True)
    st.markdown("Create viral LinkedIn and Twitter posts powered by Google ADK and LangChain-Groq")
    
    # Create tabs for different platforms
    tabs = st.tabs(["LinkedIn", "Twitter", "History"])
    
    with tabs[0]:  # LinkedIn tab
        linkedin_interface()
        
    with tabs[1]:  # Twitter tab
        twitter_interface()
        
    with tabs[2]:  # History tab
        history_interface()

def linkedin_interface():
    """Create interface for LinkedIn post generation"""
    st.markdown('<div class="platform-linkedin">', unsafe_allow_html=True)
    st.markdown("## LinkedIn Post Generator")
    st.markdown("Create engaging professional content optimized for LinkedIn's algorithm")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input form
    with st.form("linkedin_form"):
        scenario = st.text_area("Scenario/Context", 
                               placeholder="e.g., Announcing our company's new AI-powered analytics platform that helps businesses make data-driven decisions faster")
        
        requirements = st.text_area("Content Requirements",
                                  placeholder="e.g., Include our company name 'DataSight AI', mention key features like real-time insights and predictive analytics, include a call to action for a free trial")
        
        viral_strategy = st.selectbox("Viral Strategy", 
                                    ["Storytelling", "Controversial Statement", "Practical Advice", 
                                     "Data-Driven Insights", "Industry Trends", "Personal Achievement",
                                     "Question Hook", "Inspirational Quote", "Challenge or Problem-Solution"])
        
        col1, col2 = st.columns(2)
        with col1:
            target_audience = st.text_input("Target Audience", placeholder="e.g., Marketing professionals, Data analysts")
        
        with col2:
            industry = st.text_input("Industry/Niche", placeholder="e.g., Technology, Healthcare, Finance")
        
        st.markdown("### Generator Options")
        col1, col2 = st.columns(2)
        with col1:
            use_adk = st.checkbox("Use Google ADK", value=True)
        with col2:
            use_langchain = st.checkbox("Use LangChain-Groq", value=True)
        
        submit_linkedin = st.form_submit_button("Generate LinkedIn Post")
    
    # Generate content when form is submitted
    if submit_linkedin and scenario and viral_strategy:
        with st.spinner("Generating LinkedIn post... This may take a few seconds"):
            try:
                if use_adk and st.session_state.api_configured["google"]:
                    # Use Google ADK agent
                    adk_agent = LinkXAdkAgent()
                    adk_result = adk_agent.generate_post(
                        platform="linkedin",
                        scenario=scenario,
                        requirements=requirements or "Create a professional post",
                        viral_strategy=viral_strategy
                    )
                    
                    if use_langchain and st.session_state.api_configured["groq"]:
                        # Use LangChain to enhance the content
                        langchain_agent = LinkXLangChainAgent()
                        langchain_result = langchain_agent.enhance_content(
                            platform="linkedin",
                            base_content=adk_result.get("post_content", ""),
                            viral_strategy=viral_strategy,
                            target_audience=target_audience or "General professional audience"
                        )
                        
                        # Combine results
                        combined_result = {
                            "post_content": langchain_result.get("enhanced_content", adk_result.get("post_content", "")),
                            "hashtags": adk_result.get("hashtags", []),
                            "posting_time": adk_result.get("posting_time", "Not specified"),
                            "target_audience": adk_result.get("target_audience", "Not specified"),
                            "engagement_strategy": adk_result.get("engagement_strategy", "Not specified"),
                            "emotional_triggers": langchain_result.get("emotional_triggers", []),
                            "virality_score": langchain_result.get("virality_score", 0),
                            "optimization_notes": langchain_result.get("optimization_notes", "")
                        }
                        
                        display_post_result(combined_result, "linkedin")
                    else:
                        # Just display ADK result
                        display_post_result(adk_result, "linkedin")
                    
                elif use_langchain and st.session_state.api_configured["groq"]:
                    # Only use LangChain if ADK is not selected or not available
                    langchain_agent = LinkXLangChainAgent()
                    
                    # Generate hooks first
                    hooks = langchain_agent.generate_viral_hooks(
                        platform="linkedin",
                        industry=industry or "General",
                        topic=scenario,
                        count=3
                    )
                    
                    # Use the first hook as base content
                    base_content = f"{hooks[0]}\n\n{scenario}"
                    
                    langchain_result = langchain_agent.enhance_content(
                        platform="linkedin",
                        base_content=base_content,
                        viral_strategy=viral_strategy,
                        target_audience=target_audience or "General professional audience"
                    )
                    
                    # Format result
                    formatted_result = {
                        "post_content": langchain_result.get("enhanced_content", ""),
                        "hashtags": [],
                        "posting_time": "Business hours, weekdays",
                        "target_audience": target_audience or "General professional audience",
                        "engagement_strategy": "See optimization notes",
                        "emotional_triggers": langchain_result.get("emotional_triggers", []),
                        "virality_score": langchain_result.get("virality_score", 0),
                        "optimization_notes": langchain_result.get("optimization_notes", ""),
                        "headline_options": langchain_result.get("headline_options", [])
                    }
                    
                    display_post_result(formatted_result, "linkedin")
                else:
                    st.error("Please configure at least one AI model (Google API or Groq API) in the sidebar.")
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")

def twitter_interface():
    """Create interface for Twitter post generation"""
    st.markdown('<div class="platform-twitter">', unsafe_allow_html=True)
    st.markdown("## Twitter Post Generator")
    st.markdown("Create concise, viral content optimized for Twitter's algorithm")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Input form
    with st.form("twitter_form"):
        scenario = st.text_area("Scenario/Context",
                               placeholder="e.g., Sharing our new A/B testing tool that improved conversion rates by 35% for e-commerce clients",
                               max_chars=200)
        
        requirements = st.text_area("Content Requirements",
                                  placeholder="e.g., Keep it under 280 chars, include our handle @ConversionPro, add link: conv.pro/tool",
                                  max_chars=200)
        
        viral_strategy = st.selectbox("Viral Strategy", 
                                    ["Controversial Take", "Surprising Statistic", "Hot Take", 
                                     "Counterintuitive Insight", "Trend Commentary", "Industry Secret",
                                     "Engaging Question", "Bold Prediction", "Listicle"])
        
        col1, col2 = st.columns(2)
        with col1:
            target_audience = st.text_input("Target Audience", placeholder="e.g., Growth marketers, Startup founders")
        
        with col2:
            industry = st.text_input("Industry/Niche", placeholder="e.g., Marketing, Tech, Finance")
        
        st.markdown("### Generator Options")
        col1, col2 = st.columns(2)
        with col1:
            use_adk = st.checkbox("Use Google ADK", value=True, key="twitter_adk")
        with col2:
            use_langchain = st.checkbox("Use LangChain-Groq", value=True, key="twitter_langchain")
        
        submit_twitter = st.form_submit_button("Generate Twitter Post")
    
    # Generate content when form is submitted
    if submit_twitter and scenario and viral_strategy:
        with st.spinner("Generating Twitter post... This may take a few seconds"):
            try:
                if use_adk and st.session_state.api_configured["google"]:
                    # Use Google ADK agent
                    adk_agent = LinkXAdkAgent()
                    adk_result = adk_agent.generate_post(
                        platform="twitter",
                        scenario=scenario,
                        requirements=requirements or "Create a concise, engaging tweet",
                        viral_strategy=viral_strategy
                    )
                    
                    if use_langchain and st.session_state.api_configured["groq"]:
                        # Use LangChain to enhance the content
                        langchain_agent = LinkXLangChainAgent()
                        langchain_result = langchain_agent.enhance_content(
                            platform="twitter",
                            base_content=adk_result.get("post_content", ""),
                            viral_strategy=viral_strategy,
                            target_audience=target_audience or "General Twitter audience"
                        )
                        
                        # Combine results
                        combined_result = {
                            "post_content": langchain_result.get("enhanced_content", adk_result.get("post_content", "")),
                            "hashtags": adk_result.get("hashtags", []),
                            "posting_time": adk_result.get("posting_time", "Not specified"),
                            "target_audience": adk_result.get("target_audience", "Not specified"),
                            "engagement_strategy": adk_result.get("engagement_strategy", "Not specified"),
                            "emotional_triggers": langchain_result.get("emotional_triggers", []),
                            "virality_score": langchain_result.get("virality_score", 0),
                            "optimization_notes": langchain_result.get("optimization_notes", "")
                        }
                        
                        display_post_result(combined_result, "twitter")
                    else:
                        # Just display ADK result
                        display_post_result(adk_result, "twitter")
                    
                elif use_langchain and st.session_state.api_configured["groq"]:
                    # Only use LangChain if ADK is not selected or not available
                    langchain_agent = LinkXLangChainAgent()
                    
                    # Generate hooks first
                    hooks = langchain_agent.generate_viral_hooks(
                        platform="twitter",
                        industry=industry or "General",
                        topic=scenario,
                        count=3
                    )
                    
                    # Use the first hook as base content
                    base_content = hooks[0]
                    
                    langchain_result = langchain_agent.enhance_content(
                        platform="twitter",
                        base_content=base_content,
                        viral_strategy=viral_strategy,
                        target_audience=target_audience or "General Twitter audience"
                    )
                    
                    # Format result
                    formatted_result = {
                        "post_content": langchain_result.get("enhanced_content", "")[:280],  # Enforce Twitter limit
                        "hashtags": [],
                        "posting_time": "12-3PM weekdays",
                        "target_audience": target_audience or "General Twitter audience",
                        "engagement_strategy": "See optimization notes",
                        "emotional_triggers": langchain_result.get("emotional_triggers", []),
                        "virality_score": langchain_result.get("virality_score", 0),
                        "optimization_notes": langchain_result.get("optimization_notes", ""),
                        "headline_options": langchain_result.get("headline_options", [])
                    }
                    
                    display_post_result(formatted_result, "twitter")
                else:
                    st.error("Please configure at least one AI model (Google API or Groq API) in the sidebar.")
            except Exception as e:
                st.error(f"Error generating content: {str(e)}")

def display_post_result(result, platform):
    """Display the generated post with insights"""
    # Add to session state history
    result["platform"] = platform
    result["timestamp"] = import datetime
    st.session_state.generated_posts.append(result)
    
    # Display in two columns
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown("### Generated Post")
        post_box = st.text_area(
            "Ready to Copy",
            value=result.get("post_content", "No content generated"),
            height=300,
            key=f"{platform}_{len(st.session_state.generated_posts)}"
        )
        
        character_count = len(post_box)
        st.caption(f"Character count: {character_count}/{'3000' if platform == 'linkedin' else '280'}")
        
        copy_placeholder = st.empty()
        with copy_placeholder:
            st.button("📋 Copy to Clipboard", key=f"copy_{len(st.session_state.generated_posts)}")
        
        # Display hashtags if available
        if result.get("hashtags"):
            st.markdown("#### Recommended Hashtags")
            hashtags = [f"#{tag}" if not tag.startswith('#') else tag for tag in result.get("hashtags", [])]
            st.markdown(' '.join(hashtags))
    
    with col2:
        st.markdown("### Post Insights")
        
        # Display posting time
        st.markdown(f"**Best Posting Time:** {result.get('posting_time', 'Not specified')}")
        
        # Display target audience
        st.markdown(f"**Target Audience:** {result.get('target_audience', 'Not specified')}")
        
        # Display engagement strategy
        st.markdown(f"**Engagement Strategy:**")
        st.markdown(result.get('engagement_strategy', 'Not specified'))
        
        # Display sentiment analysis if available
        if result.get("sentiment_analysis"):
            sentiment = result.get("sentiment_analysis")
            st.markdown("#### Sentiment Analysis")
            st.markdown(f"**Sentiment:** {sentiment.get('sentiment', 'N/A')}")
            st.markdown(f"**Tone:** {sentiment.get('tone', 'N/A')}")
            st.markdown(f"**Engagement Prediction:** {sentiment.get('engagement_prediction', 'N/A')}")
        
        # Display LangChain enhancements if available
        if result.get("emotional_triggers"):
            st.markdown("#### Emotional Triggers")
            st.markdown(', '.join(result.get("emotional_triggers", [])))
            
        if result.get("virality_score"):
            st.markdown(f"**Virality Score:** {result.get('virality_score', 0)}/100")
            
        if result.get("optimization_notes"):
            st.markdown("#### Optimization Notes")
            st.markdown(result.get("optimization_notes", ""))
            
        if result.get("headline_options"):
            st.markdown("#### Alternative Headlines")
            for i, headline in enumerate(result.get("headline_options", []), 1):
                st.markdown(f"{i}. {headline}")

def history_interface():
    """Display the history of generated posts"""
    st.markdown("## Content History")
    st.markdown("Review and re-use your previously generated content")
    
    if not st.session_state.generated_posts:
        st.info("No posts generated yet. Generate some content using the LinkedIn or Twitter tabs!")
        return
    
    # Display posts in reverse chronological order
    for i, post in enumerate(reversed(st.session_state.generated_posts)):
        with st.expander(f"{post.get('platform', 'Post').capitalize()} - {post.get('timestamp', 'Unknown time')}"):
            st.text_area(
                "Content",
                value=post.get("post_content", ""),
                height=150,
                key=f"history_{i}"
            )
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("📋 Copy", key=f"history_copy_{i}")
            with col2:
                st.button("🔄 Regenerate", key=f"history_regen_{i}")
            with col3:
                st.button("✏️ Edit", key=f"history_edit_{i}")

def main():
    """Main function to run the Streamlit app"""
    initialize_session_state()
    sidebar()
    main_interface()

if __name__ == "__main__":
    main()
