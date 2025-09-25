import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Link, useNavigate, useParams } from 'react-router-dom';
import { MessageCircle, Users, Music, Heart, Send, ArrowLeft, Plus } from 'lucide-react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Home Page Component
const HomePage = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="flex justify-center py-8">
        <div className="flex items-center space-x-3">
          <Heart className="w-8 h-8 text-red-500" />
          <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
            Mindful Mind
          </h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex flex-col items-center justify-center px-4 py-16">
        <div className="max-w-4xl w-full">
          <h2 className="text-5xl font-bold text-center mb-6 leading-tight">
            Your Mental Health
            <br />
            <span className="bg-gradient-to-r from-green-400 to-blue-400 bg-clip-text text-transparent">
              Support Platform
            </span>
          </h2>
          
          <p className="text-xl text-gray-400 text-center mb-16 max-w-2xl mx-auto">
            A safe space for students to find support, connect with others, and prioritize their wellbeing.
          </p>

          {/* Navigation Cards */}
          <div className="grid md:grid-cols-3 gap-8">
            {/* AI Chatbot Card */}
            <div 
              onClick={() => navigate('/chat')}
              className="bg-gray-900 border border-gray-700 rounded-2xl p-8 hover:border-blue-400 transition-all duration-300 cursor-pointer group hover:bg-gray-800"
            >
              <div className="flex items-center justify-center w-16 h-16 bg-blue-500 bg-opacity-20 rounded-full mb-6 group-hover:bg-opacity-30 transition-all">
                <MessageCircle className="w-8 h-8 text-blue-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-blue-400 transition-colors">AI Chatbot</h3>
              <p className="text-gray-400 mb-6">
                Talk to our empathetic AI assistant for mental health support and guidance.
              </p>
              <div className="text-blue-400 font-medium">Start Conversation →</div>
            </div>

            {/* Community Forum Card */}
            <div 
              onClick={() => navigate('/forum')}
              className="bg-gray-900 border border-gray-700 rounded-2xl p-8 hover:border-purple-400 transition-all duration-300 cursor-pointer group hover:bg-gray-800"
            >
              <div className="flex items-center justify-center w-16 h-16 bg-purple-500 bg-opacity-20 rounded-full mb-6 group-hover:bg-opacity-30 transition-all">
                <Users className="w-8 h-8 text-purple-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-purple-400 transition-colors">Community Forum</h3>
              <p className="text-gray-400 mb-6">
                Connect with peers anonymously and share experiences in a supportive community.
              </p>
              <div className="text-purple-400 font-medium">Join Community →</div>
            </div>

            {/* Music & Videos Card */}
            <div 
              onClick={() => navigate('/media')}
              className="bg-gray-900 border border-gray-700 rounded-2xl p-8 hover:border-green-400 transition-all duration-300 cursor-pointer group hover:bg-gray-800"
            >
              <div className="flex items-center justify-center w-16 h-16 bg-green-500 bg-opacity-20 rounded-full mb-6 group-hover:bg-opacity-30 transition-all">
                <Music className="w-8 h-8 text-green-400" />
              </div>
              <h3 className="text-2xl font-bold mb-4 group-hover:text-green-400 transition-colors">Music & Videos</h3>
              <p className="text-gray-400 mb-6">
                Relax and unwind with curated music playlists and calming video content.
              </p>
              <div className="text-green-400 font-medium">Explore Media →</div>
            </div>
          </div>

          {/* Crisis Support */}
          <div className="mt-16 p-6 bg-red-900 bg-opacity-20 border border-red-500 rounded-2xl text-center">
            <h3 className="text-2xl font-bold text-red-400 mb-4">Crisis Support</h3>
            <p className="text-gray-300 mb-4">
              If you're in crisis or having thoughts of self-harm, please reach out immediately:
            </p>
            <div className="space-y-2 text-lg">
              <div className="text-white font-medium">Crisis Text Line: Text HOME to 741741</div>
              <div className="text-white font-medium">National Suicide Prevention Lifeline: 988</div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

// Chat Component
const ChatPage = () => {
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => Math.random().toString(36).substr(2, 9));
  const navigate = useNavigate();

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return;

    const userMessage = inputMessage.trim();
    setInputMessage('');
    setIsLoading(true);

    // Add user message to chat
    setMessages(prev => [...prev, { role: 'user', content: userMessage, timestamp: new Date() }]);

    try {
      const response = await fetch(`${API}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage
        })
      });

      if (!response.ok) throw new Error('Failed to get response');

      const data = await response.json();
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response, 
        timestamp: new Date(),
        is_crisis: data.is_crisis 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: 'Sorry, I encountered an error. Please try again.', 
        timestamp: new Date() 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-black text-white flex flex-col">
      {/* Header */}
      <header className="flex items-center p-4 border-b border-gray-700">
        <button onClick={() => navigate('/')} className="mr-4 hover:bg-gray-800 p-2 rounded-full">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center space-x-3">
          <MessageCircle className="w-6 h-6 text-blue-400" />
          <h1 className="text-xl font-bold">AI Mental Health Support</h1>
        </div>
      </header>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 py-8">
            <MessageCircle className="w-12 h-12 mx-auto mb-4 text-blue-400" />
            <p>Hello! I'm here to provide mental health support. How are you feeling today?</p>
          </div>
        )}
        
        {messages.map((message, index) => (
          <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-xs lg:max-w-md px-4 py-3 rounded-2xl shadow-lg ${
              message.role === 'user' 
                ? 'bg-white text-black rounded-br-sm' 
                : `bg-gray-800 text-white rounded-bl-sm ${message.is_crisis ? 'border border-red-400' : ''}`
            }`}>
              <p className="whitespace-pre-wrap">{message.content}</p>
              <p className="text-xs opacity-60 mt-2">
                {message.timestamp.toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-white px-4 py-3 rounded-2xl rounded-bl-sm">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-4 border-t border-gray-700">
        <div className="flex items-center space-x-4 max-w-4xl mx-auto">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts and feelings..."
            className="flex-1 bg-gray-800 text-white border border-gray-600 rounded-xl px-4 py-3 resize-none focus:outline-none focus:border-blue-400"
            rows="1"
          />
          <button
            onClick={sendMessage}
            disabled={!inputMessage.trim() || isLoading}
            className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-600 text-white p-3 rounded-xl transition-colors"
          >
            <Send className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

// Forum Component
const ForumPage = () => {
  const [channels, setChannels] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchChannels();
  }, []);

  const fetchChannels = async () => {
    try {
      const response = await fetch(`${API}/forum/channels`);
      const data = await response.json();
      setChannels(data.channels || []);
    } catch (error) {
      console.error('Failed to fetch channels:', error);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="flex items-center p-4 border-b border-gray-700">
        <button onClick={() => navigate('/')} className="mr-4 hover:bg-gray-800 p-2 rounded-full">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center space-x-3">
          <Users className="w-6 h-6 text-purple-400" />
          <h1 className="text-xl font-bold">Community Forum</h1>
        </div>
      </header>

      <div className="p-6 max-w-4xl mx-auto">
        <h2 className="text-3xl font-bold mb-8 text-center">Choose a Channel</h2>
        
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
          {channels.map(channel => (
            <div
              key={channel}
              onClick={() => navigate(`/forum/${channel}`)}
              className="bg-gray-900 border border-gray-700 rounded-xl p-6 hover:border-purple-400 cursor-pointer transition-all hover:bg-gray-800"
            >
              <h3 className="text-xl font-bold capitalize mb-2">#{channel}</h3>
              <p className="text-gray-400 text-sm">Anonymous discussions about {channel}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Channel Component
const ChannelPage = () => {
  const { channel } = useParams();
  const [posts, setPosts] = useState([]);
  const [showNewPost, setShowNewPost] = useState(false);
  const [newPost, setNewPost] = useState({ title: '', content: '' });
  const navigate = useNavigate();

  useEffect(() => {
    fetchPosts();
  }, [channel]);

  const fetchPosts = async () => {
    try {
      const response = await fetch(`${API}/forum/${channel}`);
      const data = await response.json();
      setPosts(data || []);
    } catch (error) {
      console.error('Failed to fetch posts:', error);
    }
  };

  const createPost = async () => {
    if (!newPost.title.trim() || !newPost.content.trim()) return;

    try {
      const response = await fetch(`${API}/forum/${channel}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newPost)
      });

      if (response.ok) {
        setNewPost({ title: '', content: '' });
        setShowNewPost(false);
        fetchPosts();
      }
    } catch (error) {
      console.error('Failed to create post:', error);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="flex items-center justify-between p-4 border-b border-gray-700">
        <div className="flex items-center">
          <button onClick={() => navigate('/forum')} className="mr-4 hover:bg-gray-800 p-2 rounded-full">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <div className="flex items-center space-x-3">
            <Users className="w-6 h-6 text-purple-400" />
            <h1 className="text-xl font-bold capitalize">#{channel}</h1>
          </div>
        </div>
        <button
          onClick={() => setShowNewPost(!showNewPost)}
          className="bg-purple-500 hover:bg-purple-600 text-white px-4 py-2 rounded-xl flex items-center space-x-2"
        >
          <Plus className="w-4 h-4" />
          <span>New Post</span>
        </button>
      </header>

      <div className="p-6 max-w-4xl mx-auto">
        {/* New Post Form */}
        {showNewPost && (
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6 mb-6">
            <h3 className="text-lg font-bold mb-4">Create New Post</h3>
            <input
              type="text"
              placeholder="Post title..."
              value={newPost.title}
              onChange={(e) => setNewPost({ ...newPost, title: e.target.value })}
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 mb-4 focus:outline-none focus:border-purple-400"
            />
            <textarea
              placeholder="Share your thoughts..."
              value={newPost.content}
              onChange={(e) => setNewPost({ ...newPost, content: e.target.value })}
              className="w-full bg-gray-800 border border-gray-600 rounded-lg px-4 py-3 mb-4 h-32 resize-none focus:outline-none focus:border-purple-400"
            />
            <div className="flex space-x-4">
              <button
                onClick={createPost}
                className="bg-purple-500 hover:bg-purple-600 text-white px-6 py-2 rounded-lg"
              >
                Post
              </button>
              <button
                onClick={() => setShowNewPost(false)}
                className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Posts List */}
        <div className="space-y-4">
          {posts.length === 0 ? (
            <div className="text-center text-gray-400 py-12">
              <Users className="w-12 h-12 mx-auto mb-4 text-purple-400" />
              <p>No posts yet in #{channel}. Be the first to share!</p>
            </div>
          ) : (
            posts.map(post => (
              <div key={post.id} className="bg-gray-900 border border-gray-700 rounded-xl p-6">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="text-lg font-bold">{post.title}</h3>
                  <span className="text-sm text-gray-400">
                    {new Date(post.timestamp).toLocaleDateString()}
                  </span>
                </div>
                <p className="text-gray-300 mb-4 whitespace-pre-wrap">{post.content}</p>
                <div className="flex items-center justify-between text-sm text-gray-400">
                  <span>by {post.author}</span>
                  <span>{post.replies?.length || 0} replies</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

// Media Component
const MediaPage = () => {
  const navigate = useNavigate();

  const musicPlaylists = [
    { title: "Relaxing Study Music", embed: "https://www.youtube.com/embed/jfKfPfyJRdk" },
    { title: "Meditation Sounds", embed: "https://www.youtube.com/embed/1ZYbU82GVz4" },
    { title: "Nature Sounds for Anxiety", embed: "https://www.youtube.com/embed/eKFTSSKCzWA" },
    { title: "Calming Rain Sounds", embed: "https://www.youtube.com/embed/mPZkdNFkNps" }
  ];

  return (
    <div className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="flex items-center p-4 border-b border-gray-700">
        <button onClick={() => navigate('/')} className="mr-4 hover:bg-gray-800 p-2 rounded-full">
          <ArrowLeft className="w-6 h-6" />
        </button>
        <div className="flex items-center space-x-3">
          <Music className="w-6 h-6 text-green-400" />
          <h1 className="text-xl font-bold">Music & Videos</h1>
        </div>
      </header>

      <div className="p-6 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold mb-8 text-center">Relaxing Content for Wellbeing</h2>
        
        <div className="grid md:grid-cols-2 gap-6">
          {musicPlaylists.map((playlist, index) => (
            <div key={index} className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden hover:border-green-400 transition-all">
              <div className="aspect-video">
                <iframe
                  src={playlist.embed}
                  title={playlist.title}
                  className="w-full h-full"
                  frameBorder="0"
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  allowFullScreen
                />
              </div>
              <div className="p-4">
                <h3 className="text-lg font-bold">{playlist.title}</h3>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/chat" element={<ChatPage />} />
        <Route path="/forum" element={<ForumPage />} />
        <Route path="/forum/:channel" element={<ChannelPage />} />
        <Route path="/media" element={<MediaPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;