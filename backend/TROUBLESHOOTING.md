# Scriptodon Troubleshooting Guide

## 🔴 401 Unauthorized Error Fix

If you're getting a **401 Unauthorized** error when trying to generate test cases or scripts, follow these steps:

### Step 1: Verify Your API Key

Run the verification script:
```bash
cd Scritodon/backend
python check_api_key.py
```

### Step 2: Check Your OpenRouter Account

1. **Go to https://openrouter.ai/keys**
2. **Verify your account status:**
   - Make sure your account is active
   - Check if you have sufficient credits
   - Ensure your API key hasn't expired

### Step 3: Generate a New API Key

If your current key is invalid:

1. Go to https://openrouter.ai/keys
2. Click "Create Key" or "Generate New Key"
3. Copy the new API key
4. Update your `.env` file:

```env
OPENROUTER_API_KEY=your_new_api_key_here
```

### Step 4: Restart the Backend

After updating the API key:
```bash
# Stop the current server (Ctrl+C)
# Then restart:
python run.py
```

## 🔧 Common Issues and Solutions

### Issue 1: "API key is invalid or expired"

**Solution:**
- Generate a new API key from OpenRouter
- Make sure you're using the correct key format (starts with `sk-or-`)

### Issue 2: "Access denied" or "Insufficient credits"

**Solution:**
- Check your OpenRouter account balance
- Add credits to your account
- Consider using a different model (some are free)

### Issue 3: "Rate limit exceeded"

**Solution:**
- Wait a few minutes before trying again
- Consider upgrading your OpenRouter plan
- Use a different model with higher rate limits

### Issue 4: API key not being loaded

**Solution:**
1. Check your `.env` file exists in the backend directory
2. Verify the file format is correct (no spaces around `=`)
3. Restart the backend server after making changes

## 🧪 Testing Your Setup

### Test 1: API Key Verification
```bash
python check_api_key.py
```

### Test 2: Manual API Test
```bash
curl -X POST "https://openrouter.ai/api/v1/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: http://localhost:3000" \
  -H "X-Title: Scriptodon Test Automation Platform" \
  -d '{
    "model": "qwen/qwen-2.5-72b-instruct:free",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
  }'
```

## 📋 Environment File Template

Make sure your `.env` file looks like this:

```env
# OpenRouter API Configuration
OPENROUTER_API_KEY=sk-or-your-actual-api-key-here

# Site Configuration
OPENROUTER_SITE_URL=http://localhost:3000
OPENROUTER_SITE_NAME=Scriptodon Test Automation Platform

# Database Configuration
DATABASE_URL=sqlite:///./scritodon.db

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760
```

## 🚨 Emergency Fallback

If you can't get OpenRouter working, you can temporarily disable AI features:

1. Comment out the AI service calls in the routers
2. Return mock data for testing
3. Focus on the non-AI features first

## 📞 Getting Help

If you're still having issues:

1. **Check the logs:** Look at the backend console output for detailed error messages
2. **Verify network:** Make sure you can access https://openrouter.ai
3. **Try a different model:** Some models might be temporarily unavailable
4. **Contact OpenRouter support:** If the issue persists with a valid API key

## 🔄 Alternative AI Providers

If OpenRouter continues to have issues, you can modify `ai_service.py` to use:

- **OpenAI API** (requires OpenAI API key)
- **Anthropic Claude API** (requires Anthropic API key)
- **Local models** via Ollama (free, runs locally)

The current implementation uses OpenRouter for its access to multiple AI models through a single API. 