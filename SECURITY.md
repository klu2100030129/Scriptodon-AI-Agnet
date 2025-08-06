# Security Guide for Scriptodon

## API Key Security

### OpenRouter API Key Protection

The OpenRouter API key is properly secured using the following measures:

#### 1. Environment Variable Storage
- ✅ API key is stored in `.env` file (not tracked in Git)
- ✅ Loaded via `pydantic-settings` from environment variables
- ✅ Never hardcoded in source code

#### 2. Validation and Error Handling
- ✅ API key format validation (must start with `sk-or-v1-`)
- ✅ Secure error messages that don't expose the key
- ✅ Logging configured to avoid sensitive data exposure

#### 3. Deployment Security
- ✅ `.env` file excluded from Git tracking
- ✅ Environment variables set securely in Render dashboard
- ✅ No API key in logs or error messages

## Security Best Practices Implemented

### 1. API Key Validation
```python
def _validate_api_key(self):
    """Validate API key without exposing it in error messages"""
    if not self.api_key or self.api_key == "your_openrouter_api_key_here":
        raise Exception("OpenRouter API key not configured. Please set OPENROUTER_API_KEY in your .env file.")
    
    # Validate API key format (should start with sk-or-v1-)
    if not self.api_key.startswith("sk-or-v1-"):
        raise Exception("Invalid OpenRouter API key format. API key should start with 'sk-or-v1-'")
```

### 2. Secure Logging
```python
# Don't log the full error response to avoid exposing sensitive data
logger.error(f"OpenRouter API request failed with status {response.status}")
raise Exception(f"OpenRouter API request failed with status {response.status}")
```

### 3. Environment Configuration
```python
# In config.py
OPENROUTER_API_KEY: Optional[str] = None

# In .env file (not tracked in Git)
OPENROUTER_API_KEY=sk-or-v1-your-actual-api-key-here
```

## Deployment Security Checklist

### ✅ Before Deployment
- [ ] API key is in `.env` file (not in source code)
- [ ] `.env` file is in `.gitignore`
- [ ] No API key in commit history
- [ ] Environment variables set in Render dashboard

### ✅ After Deployment
- [ ] Test API endpoints work correctly
- [ ] Check logs don't contain API key
- [ ] Verify error messages don't expose sensitive data
- [ ] Update `OPENROUTER_SITE_URL` to actual deployment URL

## API Key Management

### Getting Your API Key
1. Go to https://openrouter.ai/keys
2. Create a new API key
3. Copy the key (starts with `sk-or-v1-`)
4. Add to your `.env` file locally
5. Add to Render environment variables for deployment

### Rotating API Keys
1. Generate new key at https://openrouter.ai/keys
2. Update `.env` file locally
3. Update Render environment variables
4. Test the application
5. Delete old key from OpenRouter dashboard

## Security Monitoring

### What to Monitor
- API key usage in OpenRouter dashboard
- Unusual request patterns
- Error logs for potential exposure
- Rate limiting alerts

### Emergency Response
If API key is compromised:
1. Immediately rotate the key
2. Check logs for exposure
3. Review recent commits
4. Update all deployment environments
5. Monitor for unauthorized usage

## Compliance

This implementation follows security best practices:
- ✅ No hardcoded secrets
- ✅ Environment variable usage
- ✅ Secure error handling
- ✅ Proper logging configuration
- ✅ Git ignore for sensitive files 