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
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements-deploy.txt`
- **Start Command**: `python main.py`

**Environment Variables:**
Add these environment variables in Render dashboard:

```
OPENROUTER_API_KEY=your-openrouter-api-key-here
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

1. **Rust/Cargo Errors**: Fixed by using pre-compiled packages in `requirements-deploy.txt`
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

## Package Differences

### Development vs Deployment
- **Development**: Uses `requirements.txt` with all packages
- **Deployment**: Uses `requirements-deploy.txt` with pre-compiled packages

### Pre-compiled Deployment Packages
```
fastapi==0.88.0
uvicorn==0.20.0
python-multipart==0.0.6
sqlalchemy==1.4.46
requests==2.28.1
aiohttp==3.8.4
python-dotenv==0.21.1
pydantic==1.10.2
jinja2==3.1.2
PyYAML==6.0
```

### Key Changes for Deployment
- **Pydantic v1**: Uses older version that doesn't require Rust compilation
- **Pre-compiled wheels**: All packages are pre-compiled, no compilation needed
- **Older but stable versions**: Uses proven versions that work on Render

This configuration uses only pre-compiled packages that don't require any Rust compilation, ensuring successful deployment on Render. 