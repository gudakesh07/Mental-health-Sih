# Mindful Mind - Mental Health Support Platform

A comprehensive full-stack web application providing AI-powered mental health support for students with crisis detection, community forums, and wellness resources.

## 🌟 Features

- **AI Chatbot**: Empathetic mental health support with GPT-4o via OpenRouter
- **Crisis Detection**: Automatic detection of crisis keywords with emergency resources
- **Community Forum**: Anonymous discussion channels for peer support
- **Media Library**: Curated relaxing music and videos for wellbeing
- **Beautiful UI**: Clean black & white design with colorful accents

## 🚀 Complete Setup Instructions

### Prerequisites

Make sure you have the following installed:
- **Node.js** (v16 or higher) - [Download here](https://nodejs.org/)
- **Python** (v3.8 or higher) - [Download here](https://python.org/)
- **MongoDB** - [MongoDB Atlas (cloud)](https://mongodb.com/atlas) or [Local MongoDB](https://mongodb.com/try/download/community)
- **Git** - [Download here](https://git-scm.com/)

### Step 1: Clone/Download the Project

```bash
# If you have the code on GitHub
git clone your-repo-url
cd mindful-mind

# Or if you downloaded as ZIP
unzip mindful-mind.zip
cd mindful-mind
```

### Step 2: Backend Setup

#### 2.1 Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### 2.2 Set Up Environment Variables
Create a `.env` file in the `backend/` folder:
```bash
# backend/.env
MONGO_URL="your-mongodb-connection-string"
DB_NAME="mindful_mind_db"
CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
OPENROUTER_API_KEY="your-openrouter-api-key"
```

**Getting MongoDB Connection String:**

**Option A: MongoDB Atlas (Recommended - Free)**
1. Go to [MongoDB Atlas](https://mongodb.com/atlas)
2. Create a free account
3. Create a new cluster (free tier)
4. Click "Connect" → "Connect your application"
5. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)
6. Replace `<password>` with your actual password

**Option B: Local MongoDB**
```bash
# Install MongoDB locally, then use:
MONGO_URL="mongodb://localhost:27017"
```

**Getting OpenRouter API Key:**
1. Go to [OpenRouter.ai](https://openrouter.ai)
2. Sign up for a free account
3. Go to "Keys" section
4. Create a new API key
5. Copy the key (starts with `sk-or-...`)

### Step 3: Frontend Setup

#### 3.1 Install Node.js Dependencies
```bash
cd ../frontend
npm install
# OR if you prefer yarn:
yarn install
```

#### 3.2 Set Up Frontend Environment
Create a `.env` file in the `frontend/` folder:
```bash
# frontend/.env
REACT_APP_BACKEND_URL=http://localhost:8000
```

### Step 4: Running the Application

#### 4.1 Start the Backend Server
```bash
cd backend
python -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

#### 4.2 Start the Frontend (New Terminal)
```bash
cd frontend
npm start
# OR
yarn start
```

### Step 5: Access Your Application

Open your browser and go to:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (API documentation)

## 🔧 Configuration Options

### Available AI Models (OpenRouter)

You can change the AI model in `backend/server.py` (line ~95):

```python
# Current: OpenAI GPT-4o
model="openai/gpt-4o"

# Other options:
model="anthropic/claude-3.5-sonnet"     # Anthropic Claude (great for empathy)
model="google/gemini-pro"               # Google Gemini (cost-effective)
model="meta-llama/llama-3-8b-instruct" # Meta Llama (good performance)
model="mistralai/mistral-7b-instruct"   # Mistral (lightweight)
```

### Crisis Detection Keywords

You can modify crisis keywords in `backend/server.py` (line ~30):

```python
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "self harm",
    # Add more keywords as needed
]
```

## 🚀 Deployment Options

### Option 1: Vercel + Railway (Recommended)

**Frontend (Vercel):**
1. Push your code to GitHub
2. Go to [Vercel.com](https://vercel.com)
3. Import your GitHub repository
4. Set build command: `cd frontend && npm run build`
5. Set environment variable: `REACT_APP_BACKEND_URL=your-backend-url`

**Backend (Railway):**
1. Go to [Railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add MongoDB service
4. Set environment variables:
   - `MONGO_URL` (from Railway MongoDB service)
   - `OPENROUTER_API_KEY`
   - `CORS_ORIGINS=your-frontend-url`

### Option 2: Netlify + Render

**Frontend (Netlify):**
1. Go to [Netlify.com](https://netlify.com)
2. Drag and drop your `frontend/build` folder
3. Set environment variables in site settings

**Backend (Render):**
1. Go to [Render.com](https://render.com)
2. Create new web service from GitHub
3. Set build command: `cd backend && pip install -r requirements.txt`
4. Set start command: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`

### Option 3: Docker Deployment

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_BACKEND_URL=http://localhost:8000

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGO_URL=mongodb://mongo:27017
      - OPENROUTER_API_KEY=your-key
    depends_on:
      - mongo

  mongo:
    image: mongo:latest
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

volumes:
  mongo_data:
```

Run with: `docker-compose up`

## 🛠️ Troubleshooting

### Common Issues

**1. "OpenRouter API key not configured"**
```bash
# Check your backend/.env file has:
OPENROUTER_API_KEY=sk-or-your-actual-key
# Restart backend after adding
```

**2. "Connection refused" errors**
```bash
# Make sure MongoDB is running
# Check MONGO_URL in backend/.env
# For Atlas: ensure IP whitelist includes your IP
```

**3. "CORS errors"**
```bash
# Update CORS_ORIGINS in backend/.env:
CORS_ORIGINS="http://localhost:3000,https://yourdomain.com"
```

**4. Frontend can't reach backend**
```bash
# Check REACT_APP_BACKEND_URL in frontend/.env
# Make sure backend is running on the specified port
```

### Testing the Setup

**Test Backend API:**
```bash
curl http://localhost:8000/api/
# Should return: {"message": "Mindful Mind API is running"}
```

**Test AI Chat:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"session_id": "test", "message": "Hello, I need help"}'
```

## 📁 Project Structure

```
mindful-mind/
├── backend/
│   ├── server.py          # Main FastAPI application
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
├── frontend/
│   ├── src/
│   │   ├── App.js        # Main React component
│   │   ├── App.css       # Styles
│   │   └── index.js      # Entry point
│   ├── package.json      # Node.js dependencies
│   └── .env             # Frontend environment
├── README.md            # This file
└── OPENROUTER_SETUP.md  # OpenRouter specific guide
```

## 🔐 Security Notes

**For Production:**
1. Use strong environment variables
2. Enable MongoDB authentication
3. Set up proper CORS origins
4. Use HTTPS for all domains
5. Implement rate limiting
6. Monitor API usage and costs

## 💰 Cost Estimation

**OpenRouter Pricing (approximate per 1000 users/month):**
- GPT-4o: $15-30/month
- Claude-3.5-Sonnet: $10-20/month
- Gemini Pro: $3-8/month
- Mistral-7B: $1-3/month

**Hosting (free tiers available):**
- Vercel: Free for personal projects
- Railway: $5/month for backend + DB
- MongoDB Atlas: Free tier (512MB)

## 📞 Support & Contact

**Crisis Resources Built Into App:**
- National Suicide Prevention Lifeline: 988
- Crisis Text Line: Text HOME to 741741

**Technical Support:**
- Check logs: `tail -f backend/logs/app.log`
- OpenRouter Status: [status.openrouter.ai](https://status.openrouter.ai)
- MongoDB Atlas Support: [support.mongodb.com](https://support.mongodb.com)

## 📄 License

This project is for educational and mental health support purposes. Please ensure compliance with local healthcare regulations when deploying.

---

**🎉 Your mental health platform is now ready to help students worldwide!**

For any questions or issues, refer to the troubleshooting section or check the logs for specific error messages.
