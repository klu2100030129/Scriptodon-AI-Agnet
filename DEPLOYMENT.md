# Deployment Guide for Scriptodon on Render

## Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be pushed to GitHub
3. **Environment Variables**: Set up your API keys

## Deployment Steps

### 1. Connect to Render

1. Go to your Render dashboard
2. Click "New +" and select "Web Service"
3. Connect your GitHub repository
4. Select the repository: `klu2100030129/Scriptodon-AI-Agnet`

### 2. Configure the Service

**Build Settings:**
- **Build Command**: `cd backend && pip install -r requirements.txt && playwright install --with-deps`
- **Start Command**: `cd backend && python main.py`

**Environment Variables:**
Add these environment variables in Render dashboard:

```
OPENROUTER_API_KEY=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
OPENROUTER_SITE_URL=https://your-app-name.onrender.com
OPENROUTER_SITE_NAME=Scriptodon Test Automation Platform
JIRA_SERVER_URL=https://2100030129cse.atlassian.net/
JIRA_USERNAME=your-jira-username
JIRA_API_TOKEN=your-jira-token
```

### 3. Deploy

1. Click "Create Web Service"
2. Wait for the build to complete
3. Your app will be available at `https://your-app-name.onrender.com`

## Troubleshooting

### Common Issues:

1. **Rust/Cargo Errors**: Fixed by removing `[cryptography]` and `[bcrypt]` from requirements
2. **Port Issues**: Fixed by using environment variables for host/port
3. **Database Issues**: SQLite database will be created automatically

### Build Logs:

If deployment fails, check the build logs in Render dashboard for specific error messages.

## Environment Variables Explained

- `OPENROUTER_API_KEY`: Your OpenRouter API key for AI functionality
- `OPENROUTER_SITE_URL`: Your Render app URL (update after deployment)
- `OPENROUTER_SITE_NAME`: Your app name for OpenRouter analytics
- `JIRA_*`: Jira integration settings (optional)

## Post-Deployment

1. Update the `OPENROUTER_SITE_URL` to your actual Render URL
2. Test the API endpoints at `/health`
3. Configure your frontend to use the new backend URL

## API Endpoints

- `GET /`: Root endpoint
- `GET /health`: Health check
- `POST /api/input-sources/`: Upload input sources
- `POST /api/test-generation/generate`: Generate test cases
- `POST /api/script-output/generate`: Generate scripts
- `POST /api/manual-testing/execute`: Execute manual tests 