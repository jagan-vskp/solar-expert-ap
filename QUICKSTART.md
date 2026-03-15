# 🚀 Quick Start Guide - Interactive Solar Agent for India

## Step 1: Add Your OpenAI API Key

Edit the `.env` file:
```bash
nano .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

Save and exit (Ctrl+X, then Y, then Enter)

## Step 2: Run the Agent

```bash
python main.py
```

## Step 3: Interact!

### Example 1: Calculate Solar Requirements

```
👉 Your choice: 1
🔌 Enter your daily electricity consumption (kWh): 25
📍 Select your state: 1 (Rajasthan)
⚡ Select system type: 1 (On-grid)
```

You'll get:
- Complete cost breakdown in ₹
- Government subsidy calculation
- Number of panels needed
- Payback period
- Environmental impact

### Example 2: Ask Questions

```
👉 Your choice: 2
❓ Ask your question: What are the benefits of on-grid vs off-grid systems in India?
```

The AI will explain in detail with India-specific context!

### Example 3: Generate Full Report

```
👉 Your choice: 3
```

Creates a comprehensive report file with:
- All calculations
- Installation guide
- Government schemes
- State-specific incentives
- Maintenance tips

### Example 4: State Incentives

```
👉 Your choice: 4
📍 Which state: Karnataka
```

Get detailed info about subsidies, net metering, and schemes!

## Common Questions to Ask

Try asking the agent:
- "How much does a 5kW solar system cost in India after subsidy?"
- "What is the net metering process in my state?"
- "Which Indian solar panel brands are best?"
- "How does monsoon affect solar production?"
- "What are the MNRE requirements?"
- "Can I get a loan for solar installation?"
- "What maintenance is needed for rooftop solar?"
- "How to apply for government subsidy?"

## System Types Explained

1. **On-Grid (Grid-tied)**
   - Connected to electricity grid
   - Net metering available
   - No batteries needed
   - Lowest cost
   - Sell excess to DISCOM

2. **Off-Grid (Standalone)**
   - Independent system
   - Batteries required
   - Higher cost
   - Good for remote areas
   - No grid dependency

3. **Hybrid**
   - Grid + Battery backup
   - Best of both worlds
   - Power during outages
   - Medium to high cost
   - Maximum flexibility

## Tips for Best Results

✅ **Know your monthly bill**: Daily consumption = Monthly bill ÷ 30 ÷ ₹8
✅ **Select correct state**: Different states have different sun hours
✅ **Consider future expansion**: Plan for increased usage
✅ **Check roof space**: Ensure you have enough area
✅ **Verify subsidy eligibility**: Check current MNRE schemes

## Troubleshooting

**Problem**: "OPENAI_API_KEY not found"
- **Solution**: Make sure .env file exists and contains valid API key

**Problem**: "Invalid number"
- **Solution**: Enter only numeric values for consumption

**Problem**: Agent responses are slow
- **Solution**: Normal - AI processing takes 10-30 seconds

## Need Help?

The agent is conversational! Just ask:
- "I don't understand payback period, explain simply"
- "What should I do first to install solar?"
- "Is solar worth it for a ₹3000/month bill?"

---

**Happy Solar Planning!** 🌞🇮🇳
