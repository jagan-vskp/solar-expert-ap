"""
Solar Expert WhatsApp Bot - Flask App
Deploy this to receive WhatsApp messages and respond with AI
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
from main import SolarExpert
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)

# Initialize Twilio
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# Store conversations in memory (use Redis/DB for production)
conversations = {}

def get_or_create_expert(phone_number):
    """Get existing conversation or create new one"""
    if phone_number not in conversations:
        conversations[phone_number] = {
            'expert': SolarExpert(),
            'created_at': datetime.now(),
            'message_count': 0
        }
    return conversations[phone_number]


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Get incoming message
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        print(f"\n📱 Message from {from_number}: {incoming_msg}")
        
        # Get or create conversation
        conversation = get_or_create_expert(from_number)
        expert = conversation['expert']
        conversation['message_count'] += 1
        
        # Handle special commands
        if incoming_msg.lower() in ['reset', 'restart', 'new']:
            conversations[from_number] = {
                'expert': SolarExpert(),
                'created_at': datetime.now(),
                'message_count': 0
            }
            response_text = "🔄 Conversation reset! I'm Surya, ready to help with solar in Andhra Pradesh. What would you like to know?"
        
        elif incoming_msg.lower() in ['help', 'menu']:
            response_text = """🌞 **Surya - Solar Expert Menu**

Ask me anything about:
✅ Solar costs in AP
✅ Government subsidies
✅ Installation process
✅ ROI calculations
✅ Net metering (APERC)
✅ Best locations in AP
✅ Monsoon/maintenance

Commands:
• 'reset' - Start new chat
• 'help' - This menu

Just ask naturally! I'll Google search for latest info."""
        
        else:
            # Get AI response
            response_text = expert.chat(incoming_msg)
        
        # Create Twilio response
        resp = MessagingResponse()
        msg = resp.message()
        
        # Split long messages (WhatsApp limit ~1600 chars)
        if len(response_text) > 1500:
            chunks = split_message(response_text, 1500)
            for chunk in chunks:
                msg.body(chunk)
        else:
            msg.body(response_text)
        
        print(f"✅ Response sent: {response_text[:100]}...")
        
        return str(resp)
    
    except Exception as e:
        print(f"❌ Error: {e}")
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an error. Please try again or type 'reset' to restart.")
        return str(resp)


@app.route('/status', methods=['GET'])
def status():
    """Health check endpoint"""
    return {
        'status': 'online',
        'active_conversations': len(conversations),
        'total_messages': sum(c['message_count'] for c in conversations.values())
    }


@app.route('/send', methods=['POST'])
def send_message():
    """Manually send WhatsApp message (for testing/notifications)"""
    try:
        data = request.json
        to_number = data.get('to')
        message = data.get('message')
        
        if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
            return {'error': 'Twilio credentials not configured'}, 400
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{TWILIO_WHATSAPP_NUMBER}',
            to=f'whatsapp:{to_number}'
        )
        
        return {'success': True, 'sid': message.sid}
    
    except Exception as e:
        return {'error': str(e)}, 500


def split_message(text, max_length=1500):
    """Split long messages into chunks"""
    chunks = []
    current_chunk = ""
    
    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            current_chunk += '\n' + line if current_chunk else line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
