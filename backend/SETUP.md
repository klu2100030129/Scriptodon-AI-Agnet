# Scriptodon Setup Guide

## Fixing Script Generation Issues

If you're getting a 500 error when trying to generate scripts after creating input sources, follow these steps:

### 1. Configure OpenRouter API Key

The script generation feature requires an OpenRouter API key. Here's how to set it up:

1. **Get an API Key:**
   - Go to https://openrouter.ai/keys
   - Sign up for a free account
   - Create a new API key

2. **Create Environment File:**
   Create a `.env` file in the `backend` directory with the following content:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=your_actual_api_key_here

# Site Configuration
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_SITE_NAME=Scriptodon Test Automation Platform

# Jira Configuration (optional)
JIRA_SERVER_URL=
JIRA_USERNAME=
JIRA_API_TOKEN=

# Database Configuration
DATABASE_URL=sqlite:///./scritodon.db

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
```

3. **Replace the API Key:**
   - Replace `your_actual_api_key_here` with your actual OpenRouter API key

### 2. Restart the Backend

After creating the `.env` file, restart your backend server:

```bash
cd Scritodon/backend
python run.py
```

### 3. Test Script Generation

1. Create an input source (Swagger, Jira, or User Prompt)
2. Generate test cases for the input source
3. Try generating a script - it should now work without the 500 error

### Troubleshooting

- **Still getting 500 errors?** Make sure the API key is correctly set in the `.env` file
- **API key not working?** Check that your OpenRouter account has sufficient credits
- **Other issues?** Check the backend logs for more detailed error messages

### Alternative: Use a Different AI Provider

If you prefer to use a different AI provider, you can modify the `ai_service.py` file to use other APIs like:
- OpenAI API
- Anthropic Claude API
- Local models via Ollama

The current implementation uses OpenRouter which provides access to multiple AI models through a single API. 