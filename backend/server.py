from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from emergentintegrations.llm.chat import LlmChat, UserMessage

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

# Crisis keywords for detection
CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "self harm", 
    "cut myself", "hurt myself", "no point living", "better off dead",
    "ending it all", "take my own life", "not worth living"
]

# Define Models
class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    message: str
    response: str
    is_crisis: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    id: str
    response: str
    is_crisis: bool
    timestamp: datetime

class ForumPost(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    channel: str
    title: str
    content: str
    author: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    replies: List[dict] = Field(default_factory=list)

class ForumPostCreate(BaseModel):
    channel: str
    title: str
    content: str
    author: Optional[str] = None

class ForumReply(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    content: str
    author: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ForumReplyCreate(BaseModel):
    content: str
    author: Optional[str] = None

class CrisisAlert(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str
    message: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: str = "open"

# Helper functions
def detect_crisis(message: str) -> bool:
    """Detect crisis keywords in message"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in CRISIS_KEYWORDS)

def generate_anonymous_username() -> str:
    """Generate anonymous username"""
    prefixes = ["Anonymous", "Student", "Mindful", "Helper", "Seeker"]
    import random
    return f"{random.choice(prefixes)}_{random.randint(100, 999)}"

async def log_crisis_alert(session_id: str, message: str):
    """Log crisis alert to database"""
    alert = CrisisAlert(session_id=session_id, message=message)
    await db.crisis_alerts.insert_one(alert.dict())
    logging.warning(f"Crisis alert logged for session {session_id}: {message}")

# API Routes
@api_router.get("/")
async def root():
    return {"message": "Mindful Mind API is running"}

@api_router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize LLM chat with mental health system message
        system_message = """You are a compassionate mental health support assistant for students. 
        Provide empathetic, supportive responses while maintaining appropriate boundaries. 
        Encourage professional help when needed. Be warm, understanding, and non-judgmental.
        Keep responses concise but meaningful."""
        
        chat = LlmChat(
            api_key=os.environ['EMERGENT_LLM_KEY'],
            session_id=request.session_id,
            system_message=system_message
        ).with_model("openai", "gpt-4o")
        
        # Create user message
        user_message = UserMessage(text=request.message)
        
        # Check for crisis keywords
        is_crisis = detect_crisis(request.message)
        
        # Get AI response
        ai_response = await chat.send_message(user_message)
        
        # If crisis detected, log alert and modify response
        if is_crisis:
            await log_crisis_alert(request.session_id, request.message)
            crisis_addendum = "\n\n🚨 I'm concerned about you. Please reach out to a counselor or call the crisis helpline: 988 (US) or your local emergency number. You're not alone."
            ai_response = ai_response + crisis_addendum
        
        # Save chat message to database
        chat_msg = ChatMessage(
            session_id=request.session_id,
            message=request.message,
            response=ai_response,
            is_crisis=is_crisis
        )
        
        # Prepare for MongoDB
        chat_dict = chat_msg.dict()
        chat_dict['timestamp'] = chat_dict['timestamp'].isoformat()
        await db.chat_messages.insert_one(chat_dict)
        
        return ChatResponse(
            id=chat_msg.id,
            response=ai_response,
            is_crisis=is_crisis,
            timestamp=chat_msg.timestamp
        )
        
    except Exception as e:
        logging.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat service error: {str(e)}")

@api_router.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        messages = await db.chat_messages.find(
            {"session_id": session_id}
        ).sort("timestamp", 1).to_list(1000)
        
        # Parse timestamps back from ISO string
        for msg in messages:
            if isinstance(msg['timestamp'], str):
                msg['timestamp'] = datetime.fromisoformat(msg['timestamp'])
        
        return [ChatMessage(**msg) for msg in messages]
    except Exception as e:
        logging.error(f"Chat history error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve chat history")

@api_router.get("/forum/channels")
async def get_channels():
    try:
        # Get distinct channels
        channels = await db.forum_posts.distinct("channel")
        default_channels = ["general", "anxiety", "depression", "study-stress", "relationships"]
        all_channels = list(set(channels + default_channels))
        return {"channels": all_channels}
    except Exception as e:
        logging.error(f"Channels error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve channels")

@api_router.get("/forum/{channel}")
async def get_forum_posts(channel: str):
    try:
        posts = await db.forum_posts.find(
            {"channel": channel}
        ).sort("timestamp", -1).to_list(100)
        
        # Parse timestamps
        for post in posts:
            if isinstance(post['timestamp'], str):
                post['timestamp'] = datetime.fromisoformat(post['timestamp'])
        
        return [ForumPost(**post) for post in posts]
    except Exception as e:
        logging.error(f"Forum posts error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve forum posts")

@api_router.post("/forum/{channel}", response_model=ForumPost)
async def create_forum_post(channel: str, post_data: ForumPostCreate):
    try:
        # Generate username if not provided
        author = post_data.author or generate_anonymous_username()
        
        post = ForumPost(
            channel=channel,
            title=post_data.title,
            content=post_data.content,
            author=author
        )
        
        # Prepare for MongoDB
        post_dict = post.dict()
        post_dict['timestamp'] = post_dict['timestamp'].isoformat()
        await db.forum_posts.insert_one(post_dict)
        
        return post
    except Exception as e:
        logging.error(f"Create post error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create forum post")

@api_router.post("/forum/{channel}/{post_id}/reply")
async def add_reply(channel: str, post_id: str, reply_data: ForumReplyCreate):
    try:
        # Generate username if not provided
        author = reply_data.author or generate_anonymous_username()
        
        reply = ForumReply(
            content=reply_data.content,
            author=author
        )
        
        # Add reply to post
        reply_dict = reply.dict()
        reply_dict['timestamp'] = reply_dict['timestamp'].isoformat()
        
        result = await db.forum_posts.update_one(
            {"id": post_id, "channel": channel},
            {"$push": {"replies": reply_dict}}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Post not found")
            
        return reply
    except Exception as e:
        logging.error(f"Add reply error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to add reply")

@api_router.get("/admin/crisis-alerts")
async def get_crisis_alerts():
    try:
        alerts = await db.crisis_alerts.find(
            {"status": "open"}
        ).sort("timestamp", -1).to_list(100)
        
        # Parse timestamps
        for alert in alerts:
            if isinstance(alert['timestamp'], str):
                alert['timestamp'] = datetime.fromisoformat(alert['timestamp'])
        
        return [CrisisAlert(**alert) for alert in alerts]
    except Exception as e:
        logging.error(f"Crisis alerts error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve crisis alerts")

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()