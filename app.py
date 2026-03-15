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
        
        # Empty message check
        if not incoming_msg:
            resp = MessagingResponse()
            resp.message("I didn't receive any message. Please try again!")
            return str(resp)
        
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
            response_text = """🌞 Surya - Solar Expert Menu

Ask me anything about:
✅ Solar costs in AP
✅ Government subsidies
✅ Installation process
✅ ROI calculations
✅ Net metering (APERC)
✅ Best locations in AP
✅ Monsoon/maintenance

Commands:
• reset - Start new chat
• help - This menu

Just ask naturally! I'll Google search for latest info."""
        
        else:
            # Get AI response with timeout handling
            print(f"🤖 Getting AI response...")
            try:
                response_text = expert.chat(incoming_msg)
                print(f"✅ AI response received: {len(response_text)} chars")
            except Exception as ai_error:
                print(f"❌ AI Error: {ai_error}")
                response_text = "I'm having trouble connecting to my knowledge base. Please try again in a moment or type 'help' for options."
        
        # Create Twilio response
        resp = MessagingResponse()
        
        # Split long messages (WhatsApp sandbox limit ~1600, using 1200 to be safe)
        if len(response_text) > 1200:
            chunks = split_message(response_text, 1200)
            print(f"✅ Splitting response into {len(chunks)} parts")
            
            # Add part numbers if more than 2 chunks
            if len(chunks) > 2:
                for i, chunk in enumerate(chunks, 1):
                    resp.message(f"[Part {i}/{len(chunks)}]\n\n{chunk}")
            else:
                for chunk in chunks:
                    resp.message(chunk)
        else:
            resp.message(response_text)
            print(f"✅ Response sent: {len(response_text)} chars")
        
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


def split_message(text, max_length=1200):
    """
    Split long messages into WhatsApp-safe chunks
    WhatsApp sandbox limit: ~1600 chars, using 1200 to be safe
    """
    # If message is short enough, return as-is
    if len(text) <= max_length:
        return [text]
    
    chunks = []
    current_chunk = ""
    
    # Split by paragraphs first (double newline)
    paragraphs = text.split('\n\n')
    
    for para in paragraphs:
        # If adding this paragraph exceeds limit, save current chunk
        if current_chunk and len(current_chunk) + len(para) + 2 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = para
        # If single paragraph is too long, split by sentences
        elif len(para) > max_length:
            sentences = para.split('. ')
            for sentence in sentences:
                if len(current_chunk) + len(sentence) + 2 > max_length:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk += '. ' + sentence if current_chunk else sentence
        else:
            current_chunk += '\n\n' + para if current_chunk else para
    
    # Add remaining chunk
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    # Safety check: if any chunk is still too long, hard split it
    final_chunks = []
    for chunk in chunks:
        if len(chunk) <= max_length:
            final_chunks.append(chunk)
        else:
            # Hard split at max_length
            for i in range(0, len(chunk), max_length):
                final_chunks.append(chunk[i:i+max_length])
    
    return final_chunks


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
