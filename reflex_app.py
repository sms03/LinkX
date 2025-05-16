"""
LinkX Reflex Interface
---------------------
This module provides a modern web interface for the LinkX application using Reflex.
"""

import os
import sys
import json
import asyncio
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

import reflex as rx

# Add src directory to path if needed
if os.path.exists(os.path.join(os.getcwd(), "src")):
    sys.path.insert(0, os.path.join(os.getcwd()))

# Import our agent implementations
from src.adk_agent import LinkXAdkAgent
from src.langchain_integration import LinkXLangChainAgent

# Load environment variables
load_dotenv()

# Define the state
class LinkXState(rx.State):
    """State for the LinkX application"""
    
    # Configuration
    google_api_key: str = ""
    groq_api_key: str = ""
    google_model: str = "gemini-1.5-pro-latest"
    groq_model: str = "llama3-70b-8192"
    temperature: float = 0.7
    
    # Form inputs
    platform: str = "linkedin"
    scenario: str = ""
    requirements: str = ""
    viral_strategy: str = "Storytelling"
    target_audience: str = ""
    industry: str = ""
    use_adk: bool = True
    use_langchain: bool = True
    
    # Generated content
    loading: bool = False
    generated_posts: List[Dict[str, Any]] = []
    current_post: Dict[str, Any] = {}
    error_message: str = ""
    
    # API configuration status
    @rx.var
    def google_api_configured(self) -> bool:
        return bool(self.google_api_key) or bool(os.getenv("GOOGLE_API_KEY"))
    
    @rx.var
    def groq_api_configured(self) -> bool:
        return bool(self.groq_api_key) or bool(os.getenv("GROQ_API_KEY"))
    
    def set_platform(self, platform: str):
        """Set the platform"""
        self.platform = platform
    
    def set_google_api_key(self, key: str):
        """Set the Google API key"""
        self.google_api_key = key
        if key:
            os.environ["GOOGLE_API_KEY"] = key
    
    def set_groq_api_key(self, key: str):
        """Set the Groq API key"""
        self.groq_api_key = key
        if key:
            os.environ["GROQ_API_KEY"] = key
    
    def reset_form(self):
        """Reset the form inputs"""
        self.scenario = ""
        self.requirements = ""
        self.viral_strategy = "Storytelling" if self.platform == "linkedin" else "Engaging Question"
        self.target_audience = ""
        self.industry = ""
        self.current_post = {}
    
    async def generate_post(self):
        """Generate a social media post"""
        # Validate inputs
        if not self.scenario:
            self.error_message = "Please enter a scenario/context"
            return
        
        if not self.viral_strategy:
            self.error_message = "Please select a viral strategy"
            return
        
        if self.use_adk and not self.google_api_configured:
            self.error_message = "Google API key is required for ADK"
            return
        
        if self.use_langchain and not self.groq_api_configured:
            self.error_message = "Groq API key is required for LangChain"
            return
        
        # Clear error message
        self.error_message = ""
        self.loading = True
        
        try:
            result = {}
            
            # Use Google ADK agent
            if self.use_adk and self.google_api_configured:
                api_key = self.google_api_key or os.getenv("GOOGLE_API_KEY")
                adk_agent = LinkXAdkAgent(api_key=api_key, model_name=self.google_model)
                adk_result = await adk_agent.generate_post_async(
                    platform=self.platform,
                    scenario=self.scenario,
                    requirements=self.requirements or f"Create a {'professional' if self.platform == 'linkedin' else 'concise, engaging'} post",
                    viral_strategy=self.viral_strategy
                )
                
                result = adk_result
            
            # Use LangChain to enhance the content
            if self.use_langchain and self.groq_api_configured:
                api_key = self.groq_api_key or os.getenv("GROQ_API_KEY")
                langchain_agent = LinkXLangChainAgent(groq_api_key=api_key, model_name=self.groq_model)
                
                if result:
                    # Enhance the ADK result
                    langchain_result = langchain_agent.enhance_content(
                        platform=self.platform,
                        base_content=result.get("post_content", ""),
                        viral_strategy=self.viral_strategy,
                        target_audience=self.target_audience or f"General {'professional' if self.platform == 'linkedin' else ''} audience"
                    )
                    
                    # Combine results
                    combined_result = {
                        "post_content": langchain_result.get("enhanced_content", result.get("post_content", "")),
                        "hashtags": result.get("hashtags", []),
                        "posting_time": result.get("posting_time", "Not specified"),
                        "target_audience": result.get("target_audience", "Not specified"),
                        "engagement_strategy": result.get("engagement_strategy", "Not specified"),
                        "sentiment_analysis": result.get("sentiment_analysis", {}),
                        "emotional_triggers": langchain_result.get("emotional_triggers", []),
                        "virality_score": langchain_result.get("virality_score", 0),
                        "optimization_notes": langchain_result.get("optimization_notes", "")
                    }
                    
                    result = combined_result
                else:
                    # Generate from scratch with LangChain
                    hooks = langchain_agent.generate_viral_hooks(
                        platform=self.platform,
                        industry=self.industry or "General",
                        topic=self.scenario,
                        count=3
                    )
                    
                    # Use the first hook as base content
                    base_content = hooks[0] if hooks else self.scenario
                    if self.platform == "linkedin":
                        base_content = f"{base_content}\n\n{self.scenario}"
                    
                    langchain_result = langchain_agent.enhance_content(
                        platform=self.platform,
                        base_content=base_content,
                        viral_strategy=self.viral_strategy,
                        target_audience=self.target_audience or f"General {'professional' if self.platform == 'linkedin' else ''} audience"
                    )
                    
                    # Format result
                    max_length = 3000 if self.platform == "linkedin" else 280
                    result = {
                        "post_content": langchain_result.get("enhanced_content", "")[:max_length],
                        "hashtags": [],
                        "posting_time": "Business hours, weekdays" if self.platform == "linkedin" else "12-3PM weekdays",
                        "target_audience": self.target_audience or f"General {'professional' if self.platform == 'linkedin' else ''} audience",
                        "engagement_strategy": "See optimization notes",
                        "emotional_triggers": langchain_result.get("emotional_triggers", []),
                        "virality_score": langchain_result.get("virality_score", 0),
                        "optimization_notes": langchain_result.get("optimization_notes", ""),
                        "headline_options": langchain_result.get("headline_options", [])
                    }
            
            # Set the generated post
            if result:
                result["platform"] = self.platform
                result["timestamp"] = str(rx.utils.format_datetime(rx.utils.now()))
                self.current_post = result
                self.generated_posts.append(result)
            else:
                self.error_message = "Failed to generate content. Please configure at least one AI model."
        
        except Exception as e:
            self.error_message = f"Error generating content: {str(e)}"
        
        finally:
            self.loading = False

# Define UI components
def navbar():
    """Create a navigation bar"""
    return rx.box(
        rx.hstack(
            rx.heading("LinkX", size="lg", color="primary"),
            rx.text("AI Social Media Post Generator", font_weight="bold"),
            rx.spacer(),
            rx.hstack(
                rx.link("About", href="#", color="gray"),
                rx.link("Docs", href="#", color="gray"),
                rx.link("Support", href="#", color="gray"),
                spacing="4",
            ),
            width="100%",
            padding="2",
            bg="rgba(255, 255, 255, 0.8)",
            backdrop_filter="blur(10px)",
            border_bottom="1px solid #eaeaea",
            position="sticky",
            top="0",
            z_index="1000",
        )
    )

def sidebar():
    """Create a sidebar with configuration options"""
    return rx.box(
        rx.vstack(
            rx.heading("Configuration", size="md"),
            rx.divider(),
            
            # API Keys
            rx.heading("API Keys", size="sm"),
            rx.cond(
                ~rx.State.google_api_configured,
                rx.password(
                    placeholder="Enter Google API Key",
                    on_change=rx.State.set_google_api_key,
                ),
                rx.badge("Google API Configured", color_scheme="green"),
            ),
            rx.spacer(height="1"),
            rx.cond(
                ~rx.State.groq_api_configured,
                rx.password(
                    placeholder="Enter Groq API Key",
                    on_change=rx.State.set_groq_api_key,
                ),
                rx.badge("Groq API Configured", color_scheme="green"),
            ),
            rx.divider(),
            
            # Model settings
            rx.heading("Model Settings", size="sm"),
            rx.select(
                ["gemini-1.5-pro-latest", "gemini-1.5-pro", "gemini-1.5-flash"],
                placeholder="Select Google AI Model",
                value=rx.State.google_model,
                on_change=lambda value: setattr(rx.State, "google_model", value),
                size="sm",
                width="100%",
            ),
            rx.spacer(height="1"),
            rx.select(
                ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
                placeholder="Select Groq Model",
                value=rx.State.groq_model,
                on_change=lambda value: setattr(rx.State, "groq_model", value),
                size="sm",
                width="100%",
            ),
            rx.spacer(height="1"),
            rx.slider(
                default_value=0.7,
                min_=0.0,
                max_=1.0,
                step=0.1,
                on_change=lambda value: setattr(rx.State, "temperature", value),
                label="Temperature",
                width="100%",
            ),
            rx.divider(),
            
            # About
            rx.heading("About LinkX", size="sm"),
            rx.text(
                "LinkX is an AI-powered social media post generator that creates professional LinkedIn and engaging Twitter content.",
                font_size="xs",
                color="gray.500",
            ),
            rx.spacer(height="1"),
            rx.text(
                "Built with Google ADK, LangChain, and Groq",
                font_size="xs",
                color="gray.500",
            ),
            rx.spacer(),
            rx.text("© 2025 LinkX", font_size="xs", color="gray.500"),
            
            width="250px",
            height="100vh",
            padding="4",
            border_right="1px solid #eaeaea",
            position="fixed",
            overflow_y="auto",
            spacing="3",
        )
    )

def platform_tabs():
    """Create platform selection tabs"""
    return rx.tabs(
        rx.tab_list(
            rx.tab(
                "LinkedIn",
                on_click=lambda: rx.State.set_platform("linkedin"),
                _selected={"color": "primary", "font_weight": "bold", "border_bottom": "2px solid"},
            ),
            rx.tab(
                "Twitter",
                on_click=lambda: rx.State.set_platform("twitter"),
                _selected={"color": "primary", "font_weight": "bold", "border_bottom": "2px solid"},
            ),
            padding_y="2",
        ),
        rx.tab_panels(
            rx.tab_panel(
                form_panel("linkedin"),
                padding="4",
            ),
            rx.tab_panel(
                form_panel("twitter"),
                padding="4",
            ),
        ),
        variant="unstyled",
        width="100%",
    )

def form_panel(platform):
    """Create a form panel for the specified platform"""
    return rx.box(
        rx.vstack(
            rx.cond(
                rx.State.error_message != "",
                rx.alert(
                    rx.alert_icon(),
                    rx.alert_title(rx.State.error_message),
                    status="error",
                    variant="subtle",
                ),
                rx.box(),  # Empty box when no error
            ),
            
            rx.form_control(
                rx.form_label("Scenario/Context"),
                rx.text_area(
                    placeholder=f"e.g., {'Announcing our new AI-powered analytics platform' if platform == 'linkedin' else 'Sharing our A/B testing tool results'}",
                    height="100px",
                    value=rx.State.scenario,
                    on_change=lambda value: setattr(rx.State, "scenario", value),
                ),
                is_required=True,
            ),
            
            rx.form_control(
                rx.form_label("Content Requirements"),
                rx.text_area(
                    placeholder=f"e.g., {'Include key features, add CTA for free trial' if platform == 'linkedin' else 'Include handle @CompanyName and link'}",
                    height="80px",
                    value=rx.State.requirements,
                    on_change=lambda value: setattr(rx.State, "requirements", value),
                ),
            ),
            
            rx.hstack(
                rx.form_control(
                    rx.form_label("Viral Strategy"),
                    rx.select(
                        ["Storytelling", "Controversial Statement", "Practical Advice", "Data-Driven Insights", 
                         "Industry Trends", "Question Hook", "Inspirational Quote"] 
                        if platform == "linkedin" else 
                        ["Controversial Take", "Surprising Statistic", "Hot Take", "Engaging Question", 
                         "Bold Prediction", "Industry Secret"],
                        placeholder="Select a strategy",
                        value=rx.State.viral_strategy,
                        on_change=lambda value: setattr(rx.State, "viral_strategy", value),
                    ),
                    width="100%",
                ),
                rx.spacer(),
                width="100%",
            ),
            
            rx.hstack(
                rx.form_control(
                    rx.form_label("Target Audience"),
                    rx.input(
                        placeholder=f"e.g., {'Marketing professionals, Data analysts' if platform == 'linkedin' else 'Growth marketers, Startup founders'}",
                        value=rx.State.target_audience,
                        on_change=lambda value: setattr(rx.State, "target_audience", value),
                    ),
                ),
                rx.form_control(
                    rx.form_label("Industry/Niche"),
                    rx.input(
                        placeholder="e.g., Technology, Healthcare, Finance",
                        value=rx.State.industry,
                        on_change=lambda value: setattr(rx.State, "industry", value),
                    ),
                ),
                width="100%",
            ),
            
            rx.divider(),
            
            rx.heading("Generator Options", size="sm"),
            rx.hstack(
                rx.checkbox(
                    "Use Google ADK",
                    is_checked=rx.State.use_adk,
                    on_change=lambda value: setattr(rx.State, "use_adk", value),
                ),
                rx.checkbox(
                    "Use LangChain-Groq",
                    is_checked=rx.State.use_langchain,
                    on_change=lambda value: setattr(rx.State, "use_langchain", value),
                ),
            ),
            
            rx.button(
                "Generate Post",
                on_click=rx.State.generate_post,
                width="100%",
                color_scheme="blue",
                is_loading=rx.State.loading,
                is_disabled=rx.State.loading,
            ),
            
            # Show generated content if available
            rx.cond(
                rx.State.current_post != {},
                display_post_result(),
                rx.box(),  # Empty box when no post is generated
            ),
            
            spacing="4",
            width="100%",
        )
    )

def display_post_result():
    """Display the generated post with insights"""
    return rx.box(
        rx.vstack(
            rx.heading("Generated Post", size="md"),
            rx.divider(),
            
            rx.hstack(
                # Left column - Post content
                rx.box(
                    rx.form_control(
                        rx.text_area(
                            value=rx.State.current_post.post_content,
                            height="200px",
                        ),
                        width="100%",
                    ),
                    rx.text(
                        f"Character count: {rx.len(rx.State.current_post.post_content)}/{'3000' if rx.State.platform == 'linkedin' else '280'}",
                        font_size="xs",
                        color="gray.500",
                    ),
                    rx.button(
                        "📋 Copy to Clipboard",
                        on_click=lambda: rx.utils.copy_to_clipboard(rx.State.current_post.post_content),
                        size="sm",
                    ),
                    rx.cond(
                        rx.len(rx.State.current_post.hashtags) > 0,
                        rx.box(
                            rx.heading("Recommended Hashtags", size="xs"),
                            rx.wrap(
                                rx.foreach(
                                    rx.State.current_post.hashtags,
                                    lambda tag: rx.badge(f"#{tag}" if not tag.startswith('#') else tag, variant="subtle"),
                                ),
                                spacing="1",
                            ),
                        ),
                        rx.box(),  # Empty box when no hashtags
                    ),
                    width="60%",
                ),
                
                # Right column - Post insights
                rx.box(
                    rx.heading("Post Insights", size="sm"),
                    rx.divider(),
                    
                    rx.vstack(
                        rx.hstack(
                            rx.text("Best Posting Time:", font_weight="bold"),
                            rx.text(rx.State.current_post.posting_time),
                        ),
                        rx.hstack(
                            rx.text("Target Audience:", font_weight="bold"),
                            rx.text(rx.State.current_post.target_audience),
                        ),
                        rx.box(
                            rx.text("Engagement Strategy:", font_weight="bold"),
                            rx.text(rx.State.current_post.engagement_strategy),
                        ),
                        
                        # Sentiment analysis if available
                        rx.cond(
                            "sentiment_analysis" in rx.State.current_post,
                            rx.box(
                                rx.heading("Sentiment Analysis", size="xs"),
                                rx.hstack(
                                    rx.text("Sentiment:", font_weight="bold"),
                                    rx.text(rx.State.current_post.sentiment_analysis.sentiment),
                                ),
                                rx.hstack(
                                    rx.text("Tone:", font_weight="bold"),
                                    rx.text(rx.State.current_post.sentiment_analysis.tone),
                                ),
                                rx.hstack(
                                    rx.text("Engagement Prediction:", font_weight="bold"),
                                    rx.text(rx.State.current_post.sentiment_analysis.engagement_prediction),
                                ),
                            ),
                            rx.box(),  # Empty box when no sentiment analysis
                        ),
                        
                        # LangChain enhancements if available
                        rx.cond(
                            "emotional_triggers" in rx.State.current_post and rx.len(rx.State.current_post.emotional_triggers) > 0,
                            rx.box(
                                rx.heading("Emotional Triggers", size="xs"),
                                rx.text(rx.join(", ", rx.State.current_post.emotional_triggers)),
                            ),
                            rx.box(),  # Empty box when no emotional triggers
                        ),
                        
                        rx.cond(
                            "virality_score" in rx.State.current_post,
                            rx.box(
                                rx.heading("Virality Score", size="xs"),
                                rx.progress(
                                    value=rx.State.current_post.virality_score,
                                    max_=100,
                                    height="8px",
                                ),
                                rx.text(f"{rx.State.current_post.virality_score}/100", font_size="xs"),
                            ),
                            rx.box(),  # Empty box when no virality score
                        ),
                        
                        rx.cond(
                            "optimization_notes" in rx.State.current_post,
                            rx.box(
                                rx.heading("Optimization Notes", size="xs"),
                                rx.text(rx.State.current_post.optimization_notes),
                            ),
                            rx.box(),  # Empty box when no optimization notes
                        ),
                        
                        rx.cond(
                            "headline_options" in rx.State.current_post and rx.len(rx.State.current_post.headline_options) > 0,
                            rx.box(
                                rx.heading("Alternative Headlines", size="xs"),
                                rx.foreach(
                                    rx.enumerated(rx.State.current_post.headline_options),
                                    lambda item: rx.text(f"{item[0] + 1}. {item[1]}"),
                                ),
                            ),
                            rx.box(),  # Empty box when no headline options
                        ),
                        
                        width="100%",
                        align_items="flex-start",
                        spacing="3",
                    ),
                    width="40%",
                ),
                width="100%",
            ),
            
            rx.divider(),
            
            rx.hstack(
                rx.button(
                    "Reset Form",
                    on_click=rx.State.reset_form,
                    variant="outline",
                ),
                rx.spacer(),
                rx.button(
                    "Save to History",
                    variant="solid",
                ),
                rx.button(
                    "Generate Another",
                    on_click=[rx.State.reset_form, rx.focus("#scenario-input")],
                    color_scheme="blue",
                ),
                width="100%",
            ),
            
            width="100%",
            spacing="4",
            padding="4",
            border="1px solid #eaeaea",
            border_radius="md",
        ),
        margin_top="6",
    )

def main_layout():
    """Create the main layout"""
    return rx.box(
        navbar(),
        rx.hstack(
            sidebar(),
            rx.box(
                rx.vstack(
                    rx.heading("LinkX - AI Social Media Generator", size="lg"),
                    rx.text(
                        "Create viral LinkedIn and Twitter posts powered by Google ADK and LangChain-Groq",
                        color="gray.600",
                    ),
                    
                    platform_tabs(),
                    
                    width="100%",
                    spacing="6",
                    padding="6",
                ),
                margin_left="250px",
                width="calc(100% - 250px)",
            ),
            width="100%",
        ),
    )

# Create the app
app = rx.App(theme=rx.theme.light)
app.add_page(main_layout, title="LinkX - AI Social Media Post Generator")

# Server configuration
server = rx.Server(app)

if __name__ == "__main__":
    server.run()
