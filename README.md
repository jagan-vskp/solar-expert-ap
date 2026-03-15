# Interactive Solar Plant Agent - India Edition �🇳�🌞

An intelligent, conversational AI agent specifically designed for the Indian solar market. It combines Wikipedia research, OpenAI GPT-4, and mathematical calculations to provide comprehensive, India-specific guidance on setting up solar power plants.

## Features

✅ **Interactive Conversations** - Chat naturally with the agent about solar energy
✅ **India-Specific Calculations** - Uses Indian costs, subsidies, and solar radiation data
✅ **State-wise Solar Data** - Customized for different Indian states (Rajasthan, Gujarat, Maharashtra, etc.)
✅ **Government Subsidy Calculator** - Includes MNRE 40% subsidy calculations
✅ **Multiple System Types** - On-grid, Off-grid, and Hybrid systems
✅ **Wikipedia Research** - Gathers information on Indian solar policies and technology
✅ **AI-Powered Guidance** - GPT-4 generates detailed, India-specific installation guides
✅ **ROI Analysis** - Calculates payback period with Indian electricity rates
✅ **Environmental Impact** - Shows CO₂ savings and tree equivalents
✅ **Complete Reports** - Generates comprehensive installation reports

## India-Specific Features

### 🇮🇳 Indian Market Parameters
- **Cost**: ₹45/watt (current market rate)
- **Subsidy**: 40% government subsidy (up to 10kW)
- **Electricity Rate**: ₹8/kWh (average residential)
- **Panel Size**: 540W high-efficiency panels (common in India)
- **State-wise Solar Radiation**: Customized for 10+ Indian states

### 📍 Supported States with Sun Hours
- Rajasthan: 6.0 hrs/day
- Gujarat: 5.8 hrs/day
- Maharashtra: 5.5 hrs/day
- Karnataka: 5.5 hrs/day
- Tamil Nadu: 5.3 hrs/day
- Andhra Pradesh: 5.4 hrs/day
- Delhi: 5.2 hrs/day
- Kerala: 4.8 hrs/day
- West Bengal: 4.5 hrs/day
- And more...

## Installation

1. Install required packages (already done):
```bash
pip install openai wikipedia python-dotenv
```

2. Create a `.env` file with your OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

## Usage

Run the interactive agent:
```bash
python main.py
```

### Interactive Menu Options:

1. **Calculate Solar Requirements**
   - Enter daily consumption
   - Select your state
   - Choose system type (on-grid/off-grid/hybrid)
   - Get instant calculations with Indian costs

2. **Ask Questions**
   - Chat naturally about solar energy
   - Ask about subsidies, policies, installation
   - Get India-specific answers

3. **Generate Complete Report**
   - Creates detailed installation guide
   - Includes all calculations and AI guidance
   - Saves to file for reference

4. **State-Specific Incentives**
   - Learn about state schemes
   - DISCOM policies
   - Net metering details

### Example Interaction:

```
💬 How can I help you?

Options:
  1. Calculate solar requirements
  2. Ask a question about solar energy in India
  3. Generate complete installation report
  4. Learn about state-specific incentives
  5. Exit

👉 Your choice: 1

🔌 Enter your daily electricity consumption (kWh): 25

📍 Select your state:
   1. Rajasthan (6.0 hrs/day)
   2. Gujarat (5.8 hrs/day)
   ...

👉 Enter state number: 1

⚡ Select system type:
   1. On-grid (Grid-tied, with net metering)
   2. Off-grid (Standalone with batteries)
   3. Hybrid (Grid + Battery backup)

👉 Enter system type: 1

💰 Cost Analysis (Indian Rupees):
   • Total System Cost: ₹2,25,000.00
   • Government Subsidy (40%): -₹90,000.00
   • Net Cost After Subsidy: ₹1,35,000.00

📊 System Specifications:
   • Required Capacity: 5.0 kW
   • Solar Panels: 10 panels (540W each)
   • Installation Area: 26.0 m² (280.0 ft²)

⚡ Energy & Savings:
   • Annual Production: 8,979.00 kWh
   • Annual Savings: ₹71,832.00
   • Payback Period: 1.88 years

🌱 Environmental Impact:
   • CO₂ Offset: 7,362.78 kg/year
   • Equivalent to: 368 trees planted
```

## What the Agent Does

1. **Interactive Chat**: Natural conversations about solar energy in India
   - Ask any questions about solar power
   - Get context-aware, India-specific answers
   - Learn about MNRE policies and state schemes

2. **Research Phase**: Searches Wikipedia for:
   - Solar power in India
   - National Solar Mission
   - MNRE (Ministry of New and Renewable Energy)
   - Net metering policies
   - Renewable energy in India

3. **Calculation Phase**: Computes (India-specific):
   - Required system capacity (kW)
   - Number of 540W panels needed
   - Total installation area
   - Costs in Indian Rupees (₹)
   - Government subsidy (40% for residential)
   - Net cost after subsidy
   - Battery costs (for off-grid/hybrid)
   - Annual energy production
   - Payback period
   - Environmental impact (CO₂ offset)

4. **AI Analysis Phase**: Generates India-specific guidance on:
   - Step-by-step installation process
   - Government subsidies and MNRE schemes
   - DISCOM approvals and permits
   - Net metering application process
   - Indian suppliers and installers
   - State-specific incentives
   - Monsoon and weather considerations
   - Maintenance in Indian climate
   - Indian quality standards (MNRE approved)
   - Tax benefits and depreciation

5. **Report Generation**: Creates detailed reports with all findings in Indian context

## Example Output

### System Requirements:
```
LOCATION & SYSTEM DETAILS:
  • State: Rajasthan
  • System Type: ON-GRID
  • Daily Consumption: 25 kWh
  • Peak Sun Hours: 6.0 hours/day

SYSTEM SPECIFICATIONS:
  • Required Capacity: 5.0 kW
  • Solar Panels: 10 panels (540W each)
  • Installation Area: 26.0 m² (280.0 ft²)

COST BREAKDOWN (INR):
  • Total System Cost: ₹2,25,000.00
  • Govt Subsidy (40%): -₹90,000.00
  • NET COST: ₹1,35,000.00

ENERGY & FINANCIAL RETURNS:
  • Annual Production: 8,979.00 kWh
  • Annual Savings: ₹71,832.00
  • Payback Period: 1.88 years

ENVIRONMENTAL IMPACT:
  • CO₂ Offset: 7,362.78 kg/year
  • Equivalent to: 368 trees planted
```

### Conversation Examples:

**Q: "What subsidies are available for solar in Maharashtra?"**
> A: In Maharashtra, you can avail the MNRE's central subsidy of 40% for residential rooftop solar systems up to 10kW. The state also offers additional incentives through MSEDCL's net metering policy...

**Q: "How does monsoon affect solar panels?"**
> A: During monsoon, solar panel output reduces by 20-30%, but modern panels are designed to handle heavy rain. In fact, rain helps clean panels naturally. In India, annual production calculations already account for monsoon seasons...

**Q: "Which are good Indian solar panel manufacturers?"**
> A: Top Indian manufacturers include Adani Solar, Tata Power Solar, Waaree Energies, and Vikram Solar. These are MNRE-approved and offer good warranties...

## Customization

You can modify India-specific parameters in the code:

```python
self.india_params = {
    "avg_sun_hours": 5.5,          # India average
    "electricity_rate_inr": 8.0,   # ₹8 per kWh (adjust to your state)
    "cost_per_watt_inr": 45.0,     # ₹45 per watt (current market rate)
    "panel_wattage": 540,           # Modern panel size
    "govt_subsidy_percent": 40,     # Central govt subsidy
    "system_efficiency": 0.82,      # Indian conditions
}
```

Add more states:
```python
"states": {
    "Your State": 5.5,  # Average sun hours
    # ... more states
}
```

## Technologies Used

- **Python 3.7+**
- **OpenAI GPT-4** - Conversational AI and guidance generation
- **Wikipedia API** - Research on Indian solar market
- **India-specific Solar Data** - State-wise irradiation, costs, subsidies

## Indian Solar Resources

- **MNRE**: https://mnre.gov.in/ (Ministry of New and Renewable Energy)
- **National Solar Mission**: Solar rooftop schemes and subsidies
- **State DISCOMs**: For net metering applications
- **PM-KUSUM**: Solar schemes for farmers and agriculture

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection (for Wikipedia and OpenAI API)

## Notes

- All costs are in Indian Rupees (₹)
- Calculations include 40% MNRE subsidy for residential systems up to 10kW
- State-specific sun hours based on actual Indian solar radiation data
- Electricity rates based on average Indian residential tariffs
- Includes monsoon and seasonal variations in calculations
- Battery costs included for off-grid and hybrid systems
- Consult with MNRE-approved installers for precise quotes
- Check your state DISCOM's net metering policies
- Environmental impact calculated based on Indian coal grid emissions

## Disclaimer

This tool provides estimates based on typical Indian market conditions. Actual costs, subsidies, and performance may vary by:
- Specific location and state
- Current market prices
- Available government schemes
- DISCOM policies
- Installation quality
- Weather patterns

Always consult with certified solar installers and your local DISCOM for accurate information.

## License

MIT License - Feel free to modify for your needs!

---

**Made with ☀️ for India's solar revolution!** 🇮🇳
# solar-expert-ap
