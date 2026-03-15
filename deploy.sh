#!/bin/bash
# Quick Deployment Script for Solar Expert WhatsApp Bot

echo "🌞 Solar Expert WhatsApp Bot - Quick Deploy"
echo "==========================================="
echo ""

# Check if required tools are installed
command -v heroku >/dev/null 2>&1 || { 
    echo "❌ Heroku CLI not installed. Install from: https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
}

command -v git >/dev/null 2>&1 || { 
    echo "❌ Git not installed. Please install git first."
    exit 1
}

# Get app name
read -p "Enter your Heroku app name (e.g., solar-expert-ap): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "❌ App name is required"
    exit 1
fi

echo ""
echo "📋 You'll need these credentials:"
echo "1. OpenAI API Key (from platform.openai.com)"
echo "2. Twilio Account SID (from twilio.com/console)"
echo "3. Twilio Auth Token (from twilio.com/console)"
echo ""

read -p "Enter your OpenAI API Key: " OPENAI_KEY
read -p "Enter your Twilio Account SID: " TWILIO_SID
read -p "Enter your Twilio Auth Token: " TWILIO_TOKEN

if [ -z "$OPENAI_KEY" ] || [ -z "$TWILIO_SID" ] || [ -z "$TWILIO_TOKEN" ]; then
    echo "❌ All credentials are required"
    exit 1
fi

echo ""
echo "🚀 Starting deployment..."
echo ""

# Login to Heroku
echo "Step 1: Logging in to Heroku..."
heroku login

# Create Heroku app
echo ""
echo "Step 2: Creating Heroku app..."
heroku create $APP_NAME

# Set environment variables
echo ""
echo "Step 3: Setting environment variables..."
heroku config:set OPENAI_API_KEY=$OPENAI_KEY -a $APP_NAME
heroku config:set TWILIO_ACCOUNT_SID=$TWILIO_SID -a $APP_NAME
heroku config:set TWILIO_AUTH_TOKEN=$TWILIO_TOKEN -a $APP_NAME
heroku config:set TWILIO_WHATSAPP_NUMBER=+14155238886 -a $APP_NAME

# Initialize git if needed
if [ ! -d .git ]; then
    echo ""
    echo "Step 4: Initializing git..."
    git init
    git add .
    git commit -m "Initial deployment of Solar Expert Bot"
fi

# Add heroku remote
git remote add heroku https://git.heroku.com/$APP_NAME.git 2>/dev/null || true

# Deploy
echo ""
echo "Step 5: Deploying to Heroku..."
git push heroku main || git push heroku master

# Check status
echo ""
echo "Step 6: Checking deployment..."
sleep 5
heroku open -a $APP_NAME

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📱 Next steps:"
echo "1. Your app is running at: https://$APP_NAME.herokuapp.com"
echo "2. Check status: https://$APP_NAME.herokuapp.com/status"
echo "3. Configure Twilio webhook:"
echo "   → Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn"
echo "   → Set webhook to: https://$APP_NAME.herokuapp.com/webhook"
echo "4. Test in WhatsApp by messaging the Twilio number!"
echo ""
echo "View logs: heroku logs --tail -a $APP_NAME"
echo ""
