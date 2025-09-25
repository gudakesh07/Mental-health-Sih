# OpenRouter API Setup for Mindful Mind Platform

## Overview
Your mental health platform now uses OpenRouter API, which gives you access to multiple AI models through a single API key, including:

- **OpenAI Models**: GPT-4o, GPT-4, GPT-3.5-turbo, etc.
- **Anthropic Models**: Claude-3.5-sonnet, Claude-3-haiku, etc.
- **Google Models**: Gemini Pro, Gemini Flash, etc.
- **Meta Models**: Llama-3, CodeLlama, etc.
- **Mistral Models**: Mistral-7B, Mixtral, etc.

## Setup Instructions

### 1. Get OpenRouter API Key
1. Visit [OpenRouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Go to "Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-...`)

### 2. Configure Your App
Update `/app/backend/.env` file:
```env
OPENROUTER_API_KEY=sk-or-your-actual-openrouter-key-here
```

### 3. Available Models
The app is currently configured to use `openai/gpt-4o`, but you can easily change it in `/app/backend/server.py`:

```python
# Current model (line ~95)
model="openai/gpt-4o"

# Other options you can use:
model="anthropic/claude-3.5-sonnet"     # Anthropic's Claude
model="google/gemini-pro"               # Google's Gemini
model="meta-llama/llama-3-8b-instruct" # Meta's Llama
model="mistralai/mistral-7b-instruct"   # Mistral's 7B model
```

### 4. Model Pricing
OpenRouter uses pay-per-use pricing:
- **GPT-4o**: ~$0.005 per 1K tokens
- **Claude-3.5-Sonnet**: ~$0.003 per 1K tokens  
- **Gemini Pro**: ~$0.001 per 1K tokens
- **Mistral-7B**: ~$0.0002 per 1K tokens

### 5. Benefits of OpenRouter
✅ **Multiple Providers**: Access to 20+ AI models
✅ **Cost Effective**: Often cheaper than direct API calls
✅ **Unified Interface**: Single API key for all models
✅ **Reliability**: Built-in failover and load balancing
✅ **Easy Migration**: Switch models without code changes

### 6. Testing
After setting up your API key:
1. Restart the backend: `sudo supervisorctl restart backend`
2. Test the chatbot on your app
3. Check logs: `tail -f /var/log/supervisor/backend*.log`

### 7. Production Deployment
When deploying your app independently:
1. Set `OPENROUTER_API_KEY` in your hosting environment
2. Update `HTTP-Referer` header in the code to your domain
3. Consider rate limiting for production use

## Support
- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Model Pricing](https://openrouter.ai/models)
- [API Status](https://status.openrouter.ai)

Your mental health platform is now ready to run independently with OpenRouter! 🚀