# LinkX - AI Social Media Post Generator

![LinkX Logo](https://via.placeholder.com/500x100/0077B5/FFFFFF?text=LinkX)

## Overview

LinkX is an AI-powered agent that creates engaging and viral social media posts for LinkedIn and Twitter (X). The application uses Google's Agent Development Kit (ADK) to generate high-quality, platform-specific content based on user inputs.

## Features

- **ADK-Powered Post Generation:** Create professional LinkedIn posts and concise Twitter messages using Google's Agent Development Kit (ADK) and state-of-the-art AI models.
- **Custom AI Tools:** Leverage custom ADK tools for hashtag analysis and optimal posting time suggestions.
- **Platform-Specific Optimization:** Content is tailored specifically for each platform's audience, character limits, and best practices.
- **Viral Strategies:** Incorporate proven viral content strategies including storytelling, questions, statistics, and more.
- **Publishing Integration:** Optionally publish directly to LinkedIn and Twitter with API integration.
- **Content Enhancement:** Get recommendations for hashtags, best posting times, and engagement strategies.
- **User-Friendly Interface:** Simple web UI makes it easy to generate and manage social media content.
- **Fallback Mechanism:** Automatically switches to legacy method if ADK is unavailable.

## Requirements

- Python 3.8+
- UV (Python package installer)
- Google Generative AI API key (Gemini)
- Google Agent Development Kit (ADK)
- Twitter Developer API keys (optional, for posting to Twitter)
- LinkedIn account credentials (optional, for posting to LinkedIn)

## Installation

1. **Clone the repository:**

```powershell
git clone https://github.com/yourusername/LinkX.git
cd LinkX
```

2. **Create and activate a virtual environment using UV:**

```powershell
uv venv
.\.venv\Scripts\activate
```

3. **Install dependencies:**

```powershell
uv pip install -r requirements.txt
```

4. **Create a `.env` file:**

Copy the `.env.example` file to `.env` and add your API keys:

```
# Google Generative AI API Key
GOOGLE_API_KEY=your_google_api_key_here

# Twitter (X) API Credentials
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret_key
TWITTER_ACCESS_TOKEN=your_twitter_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_twitter_access_token_secret

# LinkedIn API Credentials
LINKEDIN_EMAIL=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password
```

5. **Start the application:**

```powershell
python .\src\app.py
```

The application will be available at http://127.0.0.1:5000

## Usage

1. Open the application in your web browser
2. Select the platform (LinkedIn or Twitter)
3. Enter your scenario/context, content requirements, and viral strategy
4. Click "Generate Post" to create your social media content
5. Review the generated post, recommended hashtags, and engagement tips
6. Optionally publish directly to the selected platform (requires API configuration)

## Viral Strategies

LinkX supports several viral content strategies:

- **Storytelling:** Engage audiences with a compelling narrative structure
- **Questions:** Spark curiosity and engagement with thought-provoking questions
- **Statistics:** Use surprising or counter-intuitive data points to grab attention
- **Controversy:** Take a thoughtful contrarian position on industry topics
- **Listicles:** Create scannable, valuable lists of tips, strategies or insights

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
