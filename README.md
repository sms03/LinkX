# LinkX - AI Social Media Post Generator

![LinkX Logo](https://via.placeholder.com/500x100/0077B5/FFFFFF?text=LinkX)

## Overview

LinkX is an advanced AI-powered agent that creates engaging and viral social media posts for LinkedIn and Twitter (X). The application combines Google's Agent Development Kit (ADK), LangChain, and Groq to generate high-quality, platform-specific content based on user inputs.

## Features

- **Multi-AI Powered Generation:** Create professional social media content using:
  - **Google's Agent Development Kit (ADK)** for structured, tool-based generation
  - **LangChain + Groq** integration for enhanced content creation and optimization
- **Custom AI Tools:** Leverage specialized tools for hashtag analysis, posting time suggestions, and sentiment analysis
- **Platform-Specific Optimization:** Content tailored specifically for each platform's audience, character limits, and best practices
- **Multiple User Interfaces:**
  - **Flask** web application (original)
  - **Streamlit** interface (modern, data-focused UI)
  - **Reflex** interface (reactive, component-based UI)
- **Advanced Viral Strategies:** Incorporate proven viral content techniques with platform-specific recommendations
- **Competitor Analysis:** Analyze top-performing posts in your industry for strategic insights
- **Enhanced Content Analysis:** Get detailed feedback on emotional triggers, virality scoring, and optimization suggestions
- **Multiple Publishing Options:** Push your content directly to LinkedIn and Twitter (with API credentials)
- **Intelligent Content Enhancement:** Get AI-suggested improvements to boost engagement

## Requirements

- Python 3.8+
- Google Generative AI API key (Gemini)
- Google Agent Development Kit (ADK) 0.5.0+
- Groq API key (for LangChain integration)
- Twitter Developer API keys (optional, for posting to Twitter)
- LinkedIn account credentials (optional, for posting to LinkedIn)

## Installation

1. **Clone the repository:**

```powershell
git clone https://github.com/yourusername/LinkX.git
cd LinkX
```

2. **Run the setup script:**

```powershell
python setup.py --ui streamlit --use-langchain
```

The setup script will:
- Check Python version compatibility
- Install all required dependencies
- Configure environment variables and API keys
- Set up the selected UI (streamlit, reflex, or flask)
- Verify the installation

3. **Alternative manual installation:**

Create and activate a virtual environment:
```powershell
# Using venv
python -m venv venv
.\venv\Scripts\activate

# Or using UV
uv venv
.\.venv\Scripts\activate
```

Install dependencies:
```powershell
# Using pip
pip install -r requirements-enhanced.txt

# Or using UV
uv pip install -r requirements-enhanced.txt
```

4. **Create a `.env` file:**

Copy the `.env.example` file to `.env` and add your API keys:

```
# Google Generative AI API Key (Required)
GOOGLE_API_KEY=your_google_api_key_here

# Groq API Key (For LangChain integration)
GROQ_API_KEY=your_groq_api_key_here

# Twitter (X) API Credentials (Optional, for direct publishing)
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret_key
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# LinkedIn API Credentials (Optional, for direct publishing)
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Application Settings
DEBUG=False
ENABLE_ADK=True
ENABLE_TWITTER=True
ENABLE_LINKEDIN=True
```

## Running the Application

You can run LinkX with different user interfaces:

### Flask Interface (Original)

```powershell
python run.py
```
The application will be available at http://127.0.0.1:5000

### Streamlit Interface (Modern, Data-focused)

```powershell
streamlit run streamlit_app.py
```
The application will be available at http://localhost:8501

### Reflex Interface (Reactive, Component-based)

```powershell
# Initialize Reflex first if you haven't already
reflex init

# Run the Reflex app
reflex run
```
The application will be available at http://localhost:3000

## Usage

1. Open your preferred interface in a web browser
2. Configure your API keys if not already set up
3. Select the platform (LinkedIn or Twitter)
4. Enter:
   - Your scenario/context
   - Content requirements (optional)
   - Viral strategy selection
   - Target audience (optional)
   - Industry or niche (optional)
5. Choose whether to use Google ADK, LangChain-Groq, or both
6. Click "Generate Post" to create your social media content
7. Review the generated post, along with:
   - Recommended hashtags
   - Optimal posting times
   - Engagement strategies
   - Sentiment analysis
   - Virality score (LangChain-Groq)
   - Emotional triggers used (LangChain-Groq)
   - Optimization notes (LangChain-Groq)
   - Alternative headline options (LangChain-Groq)
8. Copy, edit, or directly publish your content

## Viral Strategies

LinkX supports platform-specific viral content strategies:

### LinkedIn Strategies
- **Storytelling:** Engage audiences with compelling professional narratives
- **Practical Advice:** Share actionable insights and professional tips
- **Data-Driven Insights:** Provide research-backed information and analysis
- **Industry Trends:** Discuss cutting-edge developments in your field
- **Question Hook:** Spark professional discussions with thought-provoking questions
- **Inspirational Quote:** Share wisdom from industry leaders with your perspective

### Twitter Strategies
- **Controversial Take:** Challenge conventional wisdom with a fresh perspective
- **Surprising Statistic:** Share unexpected data points that grab attention
- **Hot Take:** Offer timely commentary on trending industry topics
- **Engaging Question:** Ask questions that encourage audience participation
- **Bold Prediction:** Make forward-looking statements about industry changes
- **Industry Secret:** Share insider knowledge or little-known facts

## Getting API Keys

### Google Generative AI (Gemini)

1. Go to the [Google AI Studio](https://aistudio.google.com/)
2. Sign up or sign in with your Google account
3. Navigate to "API keys" in the sidebar
4. Create a new API key and copy it

### Twitter (X) Developer API

1. Sign up for a [Twitter Developer Account](https://developer.twitter.com/en/portal/dashboard)
2. Create a new Project and App
3. Generate Consumer Keys and Access Tokens with appropriate permissions
4. Copy the API key, API key secret, Access token, and Access token secret

### LinkedIn API

The application uses an unofficial LinkedIn API wrapper that requires your LinkedIn login credentials. For production use, consider using LinkedIn's official Marketing API.

## License

[MIT License](LICENSE)

## Disclaimer

This project is for educational purposes only. Be sure to comply with the terms of service for all platforms and APIs used.

## Support

For questions and support, please open an issue on the GitHub repository.
