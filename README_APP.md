# 🌞 Surya - Solar Expert WhatsApp Bot for Andhra Pradesh

A human-like AI solar energy consultant that responds to WhatsApp messages 24/7. Specializes in Andhra Pradesh solar installations with real-time Google search capabilities.

---

## 🎯 **What This Bot Does**

- ✅ **WhatsApp Integration** - Works in personal chats and groups
- ✅ **Human-like Conversations** - Chats naturally like an expert
- ✅ **AP-Specific Knowledge** - Andhra Pradesh solar policies, costs, weather
- ✅ **Google Search** - Finds latest information in real-time
- ✅ **Cost Calculations** - Instant solar system quotes
- ✅ **24/7 Available** - Never sleeps, always ready to help
- ✅ **Remembers Context** - Continues conversations naturally

---

## 💬 **Example Conversations**

```
You: Hi
Bot: 🌞 Namaste! I'm Surya, your solar consultant for Andhra Pradesh. 
     I've been helping people go solar for 15+ years. What brings you here today?

You: How much for 5kW in Vijayawada?
Bot: Great question! For a 5kW rooftop system in Vijayawada:

     💰 Investment: ₹2,00,000 - ₹2,40,000
     (After 40% central subsidy: ₹1,20,000 - ₹1,44,000)
     
     ⚡ You'll generate ~23-24 units daily
     💵 Save ₹6,000-7,000 monthly
     ⏱️ ROI in 2-3 years!
     
     Vijayawada gets great sun (5.4 hrs/day). Want me to calculate 
     exact savings based on your current bill?

You: Yes, my bill is ₹5000
Bot: Perfect! Let me calculate... [detailed analysis]

You: What about monsoon?
Bot: [Explains AP monsoon patterns and solar performance]
```

---

## 🚀 **Quick Start**

### **1. Clone & Setup**
```bash
cd /Users/jaganreddy/python_projects/cowork

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.template .env

# Edit .env with your keys
nano .env
```

### **2. Get API Keys**

#### **OpenAI** (Required)
- Go to: https://platform.openai.com/api-keys
- Create new key
- Add to `.env`: `OPENAI_API_KEY=sk-xxx`

#### **Twilio** (For WhatsApp)
- Sign up: https://www.twilio.com/try-twilio
- Get Account SID and Auth Token
- Join WhatsApp Sandbox
- Add credentials to `.env`

### **3. Deploy**

#### **Option A: Automated Script**
```bash
./deploy.sh
# Follow prompts to deploy to Heroku
```

#### **Option B: Manual Heroku**
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=sk-xxx
heroku config:set TWILIO_ACCOUNT_SID=ACxxx
heroku config:set TWILIO_AUTH_TOKEN=xxx
git push heroku main
```

#### **Option C: Railway/Render**
- Connect GitHub repo
- Add environment variables
- Deploy automatically

### **4. Configure Webhook**
1. Get your deployment URL (e.g., `https://your-app.herokuapp.com`)
2. Go to Twilio Console → WhatsApp Sandbox
3. Set webhook: `https://your-app.herokuapp.com/webhook`
4. Save

### **5. Test!**
- Open WhatsApp
- Message Twilio number
- Chat with Surya! 🎉

---

## 📁 **Project Structure**

```
cowork/
├── app.py                 # Flask WhatsApp webhook server
├── main.py                # Solar expert AI agent
├── requirements.txt       # Python dependencies
├── Procfile              # Heroku deployment config
├── runtime.txt           # Python version
├── deploy.sh             # Automated deployment script
├── .env                  # Your API keys (DO NOT COMMIT)
├── .env.template         # Environment variable template
├── DEPLOYMENT_GUIDE.md   # Complete deployment instructions
└── README_APP.md         # This file
```

---

## 🔧 **Configuration**

### **Environment Variables**

```bash
# Required
OPENAI_API_KEY=sk-xxx                  # From platform.openai.com
TWILIO_ACCOUNT_SID=ACxxx              # From console.twilio.com
TWILIO_AUTH_TOKEN=xxx                 # From console.twilio.com
TWILIO_WHATSAPP_NUMBER=+14155238886   # Sandbox number

# Optional
PORT=5000                             # Server port
FLASK_ENV=production                  # Environment
```

### **Customization**

Edit `main.py` to customize:

```python
# Change region/focus
prompt = """You are Surya, expert for [YOUR REGION]"""

# Modify personality
PERSONALITY: [Your desired traits]

# Update knowledge
KEY FACTS: [Your facts]
```

---

## 📱 **Using in WhatsApp Groups**

### **Sandbox (Testing)**
1. All members must join sandbox individually
2. Add Twilio number to group
3. Bot responds to all messages

### **Production (Paid)**
1. Apply for WhatsApp Business API
2. Get approved business account
3. Add verified number to groups
4. Members don't need to join sandbox

---

## 🎛️ **Bot Commands**

| Command | Description |
|---------|-------------|
| `help` or `menu` | Show available commands |
| `reset` or `restart` | Start new conversation |
| `calculate [kW]` | Quick solar calculation |
| Just chat naturally! | Bot understands context |

---

## 💰 **Cost Breakdown**

### **Free Tier (Testing)**
- ✅ Heroku Free Dyno (limited hours)
- ✅ Twilio Sandbox (free testing)
- ❌ OpenAI API: ~$0.01-0.03 per conversation

### **Production**
- **Hosting**: $7-10/month (Heroku Hobby/Railway)
- **WhatsApp**: ~$0.005 per message (Business API)
- **OpenAI**: ~$0.03 per conversation (GPT-4)
- **Total**: $10-30/month for 100-500 conversations

---

## 🔍 **Features**

### **Core**
- [x] WhatsApp messaging
- [x] Conversational AI (GPT-4)
- [x] Context memory
- [x] Google search integration
- [x] AP-specific knowledge

### **Solar Expertise**
- [x] Cost calculations
- [x] ROI analysis
- [x] Subsidy information
- [x] Installation guidance
- [x] APERC policies
- [x] Net metering help

### **Technical**
- [x] Flask webhook server
- [x] Twilio integration
- [x] Multi-user support
- [x] Message chunking (long responses)
- [x] Error handling
- [x] Health check endpoint

---

## 🐛 **Troubleshooting**

### **Bot Not Responding**

1. **Check deployment**
   ```bash
   curl https://your-app.herokuapp.com/status
   # Should return: {"status": "online"}
   ```

2. **View logs**
   ```bash
   heroku logs --tail
   # Check for errors
   ```

3. **Verify webhook**
   - Twilio Console → Sandbox settings
   - Webhook URL must match your deployment
   - Must be HTTPS

4. **Test sandbox**
   - Re-join sandbox: `join [code]`
   - Check if sandbox is active

### **Slow Responses**
- Normal on free tier (cold start)
- Upgrade to paid dyno
- Or use Railway/Render

### **API Errors**
- Check OpenAI API quota
- Verify API key is valid
- Check billing status

---

## 📊 **Monitoring**

### **Health Check**
```bash
curl https://your-app.herokuapp.com/status
```

Response:
```json
{
  "status": "online",
  "active_conversations": 12,
  "total_messages": 347
}
```

### **Logs**
```bash
# Real-time logs
heroku logs --tail

# Search logs
heroku logs --tail | grep ERROR
```

### **Usage Stats**
- Twilio Console: Message counts
- OpenAI Dashboard: Token usage
- Heroku Metrics: Dyno performance

---

## 🔐 **Security**

1. **Never commit `.env`**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Rotate keys regularly**
   - Change Twilio tokens
   - Regenerate OpenAI keys

3. **Rate limiting** (add to `app.py`)
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, default_limits=["100 per hour"])
   ```

4. **Webhook validation**
   ```python
   from twilio.request_validator import RequestValidator
   # Verify requests are from Twilio
   ```

---

## 🚀 **Advanced Features**

### **Add Redis (Persistent Storage)**
```python
import redis
r = redis.from_url(os.getenv('REDIS_URL'))
# Store conversations permanently
```

### **Add Analytics**
```python
from flask import g
# Track: messages, users, topics, conversion rate
```

### **Multi-language Support**
```python
# Detect language and respond accordingly
if language == 'telugu':
    respond_in_telugu()
```

### **Voice Messages**
```python
# Download and transcribe voice messages
# Respond with voice using OpenAI TTS
```

### **Image Analysis**
```python
# Analyze solar panel photos
# Identify issues, estimate capacity
```

---

## 📚 **API Endpoints**

### **POST /webhook**
Receives WhatsApp messages from Twilio
- Input: Twilio webhook payload
- Output: TwiML response

### **GET /status**
Health check and stats
- Returns: Server status, conversation count

### **POST /send**
Manually send WhatsApp message
```bash
curl -X POST https://your-app.herokuapp.com/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "+919876543210",
    "message": "Hello from Surya!"
  }'
```

---

## 🎓 **Learning Resources**

- **Twilio WhatsApp**: https://www.twilio.com/docs/whatsapp
- **Flask**: https://flask.palletsprojects.com/
- **OpenAI API**: https://platform.openai.com/docs
- **Heroku Python**: https://devcenter.heroku.com/categories/python-support

---

## 🤝 **Contributing**

Improvements welcome!

1. Fork the repo
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit PR

---

## 📄 **License**

MIT License - Use freely!

---

## 🆘 **Support**

**Issues?**
- Check `DEPLOYMENT_GUIDE.md`
- View logs: `heroku logs --tail`
- Test locally with ngrok
- Contact Twilio/OpenAI support

**Questions?**
- Read full deployment guide
- Check Twilio documentation
- Test with example conversations

---

## ✅ **Deployment Checklist**

- [ ] OpenAI API key obtained
- [ ] Twilio account created
- [ ] WhatsApp sandbox joined
- [ ] Environment variables configured
- [ ] App deployed to Heroku/Railway
- [ ] Webhook URL configured
- [ ] Test message sent
- [ ] Bot responds correctly
- [ ] Added to test group
- [ ] Monitoring set up
- [ ] Logs checked
- [ ] Production plan decided

---

**Your Solar Expert is now live on WhatsApp!** 🌞📱

Start helping people go solar in Andhra Pradesh! 🇮🇳
