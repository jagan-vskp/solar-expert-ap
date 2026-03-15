"""
Solar Energy Expert - Andhra Pradesh Specialist
A human-like conversational AI agent with complete knowledge on solar park installation
in Andhra Pradesh. Can search Google and answer any solar-related questions naturally.
"""

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List, Any, Optional
import time
from googlesearch import search
import requests
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()

class SolarPlantAgent:
    """Interactive AI Agent for researching and calculating solar plant setup requirements in India"""
    
    def __init__(self):
        """Initialize the agent with OpenAI client and India-specific parameters"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Create a .env file with your API key.")
        
        self.client = OpenAI(api_key=api_key)
        self.research_data = {}
        self.conversation_history = []
        
        # India-specific parameters
        self.india_params = {
            "avg_sun_hours": 5.5,  # India average
            "electricity_rate_inr": 8.0,  # ₹8 per kWh (average residential)
            "cost_per_watt_inr": 45.0,  # ₹45 per watt installed (current Indian market)
            "panel_wattage": 540,  # Modern high-efficiency panels common in India
            "panel_area_sqm": 2.6,  # Area for 540W panel
            "govt_subsidy_percent": 40,  # Central govt subsidy for residential (up to 40%)
            "system_efficiency": 0.82,  # Slightly higher due to good solar conditions
            "states": {
                "Rajasthan": 6.0,
                "Gujarat": 5.8,
                "Maharashtra": 5.5,
                "Karnataka": 5.5,
                "Tamil Nadu": 5.3,
                "Andhra Pradesh": 5.4,
                "Delhi": 5.2,
                "Kerala": 4.8,
                "West Bengal": 4.5,
                "Other": 5.2
            }
        }
        
        print("\n🇮🇳 Solar Plant Agent initialized for India!")
        print(f"📍 Using India-specific parameters:")
        print(f"   • Average electricity rate: ₹{self.india_params['electricity_rate_inr']}/kWh")
        print(f"   • Installation cost: ₹{self.india_params['cost_per_watt_inr']}/watt")
        print(f"   • Government subsidy: Up to {self.india_params['govt_subsidy_percent']}%")
        print(f"   • Panel capacity: {self.india_params['panel_wattage']}W")
    
    def chat(self, user_message: str, include_context: bool = True) -> str:
        """
        Interactive chat with the agent using OpenAI
        
        Args:
            user_message: User's message/question
            include_context: Whether to include research context
        """
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare system message
        system_message = """You are an expert solar energy consultant specializing in the Indian solar market. 
You have deep knowledge of:
- Indian solar policies, subsidies, and regulations
- State-wise solar potential and incentives
- MNRE (Ministry of New and Renewable Energy) guidelines
- Indian solar panel manufacturers and suppliers
- Net metering policies in different Indian states
- PM-KUSUM and other government schemes
- Indian weather patterns and solar irradiation
- Local installation practices and costs

You should be conversational, helpful, and provide India-specific advice. 
Always mention Indian Rupees (₹) for costs and reference Indian states, policies, and suppliers when relevant.
Be encouraging and explain technical concepts in simple terms."""

        # Add research context if available
        if include_context and self.research_data:
            wiki_context = "\n".join([f"{topic}: {content[:200]}..." 
                                     for topic, content in list(self.research_data.items())[:3]])
            system_message += f"\n\nRecent research context:\n{wiki_context}"
        
        try:
            messages = [{"role": "system", "content": system_message}] + self.conversation_history[-10:]  # Keep last 10 messages
            
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
                temperature=0.8,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"❌ Error in chat: {e}"
    
    def get_state_sun_hours(self, state: str = None) -> float:
        """Get average sun hours for an Indian state"""
        if state and state in self.india_params["states"]:
            return self.india_params["states"][state]
        return self.india_params["avg_sun_hours"]
        
    def search_wikipedia(self, topic: str, sentences: int = 5) -> str:
        """Search Wikipedia for information on a topic"""
        try:
            print(f"\n🔍 Searching Wikipedia for: {topic}")
            summary = wikipedia.summary(topic, sentences=sentences)
            print(f"✅ Found information on Wikipedia")
            return summary
        except wikipedia.exceptions.DisambiguationError as e:
            print(f"⚠️  Multiple results found. Using first option: {e.options[0]}")
            return wikipedia.summary(e.options[0], sentences=sentences)
        except wikipedia.exceptions.PageError:
            print(f"❌ No Wikipedia page found for: {topic}")
            return f"No information found for {topic}"
    
    def gather_solar_research(self) -> Dict[str, str]:
        """Gather comprehensive research from Wikipedia on solar energy topics"""
        topics = [
            "Solar power in India",
            "Photovoltaic system",
            "Solar panel",
            "National Solar Mission",
            "Ministry of New and Renewable Energy",
            "Net metering",
            "Renewable energy in India"
        ]
        
        print("\n" + "="*60)
        print("📚 GATHERING SOLAR RESEARCH (India-focused)")
        print("="*60)
        
        research = {}
        for topic in topics:
            research[topic] = self.search_wikipedia(topic, sentences=3)
        
        self.research_data = research
        return research
    
    def calculate_solar_requirements(self, 
                                     daily_consumption_kwh: float,
                                     state: str = None,
                                     system_type: str = "on-grid") -> Dict[str, Any]:
        """
        Calculate solar plant requirements for India
        
        Args:
            daily_consumption_kwh: Daily energy consumption in kWh
            state: Indian state for sun hours calculation
            system_type: "on-grid", "off-grid", or "hybrid"
        
        Returns:
            Dictionary with calculated requirements in Indian context
        """
        print("\n" + "="*60)
        print("🔢 CALCULATING SOLAR REQUIREMENTS FOR INDIA")
        print("="*60)
        
        # Get state-specific sun hours
        avg_sun_hours = self.get_state_sun_hours(state)
        if state:
            print(f"📍 State: {state} (Avg sun hours: {avg_sun_hours} hrs/day)")
        
        # India-specific parameters
        panel_wattage = self.india_params["panel_wattage"]
        panel_area_sqm = self.india_params["panel_area_sqm"]
        system_efficiency = self.india_params["system_efficiency"]
        cost_per_watt_inr = self.india_params["cost_per_watt_inr"]
        electricity_rate_inr = self.india_params["electricity_rate_inr"]
        govt_subsidy_percent = self.india_params["govt_subsidy_percent"]
        
        # Calculate required system size
        required_capacity_kw = daily_consumption_kwh / (avg_sun_hours * system_efficiency)
        
        # Calculate number of panels needed
        num_panels = int((required_capacity_kw * 1000) / panel_wattage) + 1
        
        # Calculate total area needed
        total_area_sqm = num_panels * panel_area_sqm
        
        # Calculate costs in INR
        total_cost_inr = required_capacity_kw * 1000 * cost_per_watt_inr
        
        # Calculate subsidy (for systems up to 10kW, 40% subsidy)
        subsidy_eligible = min(required_capacity_kw, 10.0)
        subsidy_amount_inr = subsidy_eligible * 1000 * cost_per_watt_inr * (govt_subsidy_percent / 100)
        net_cost_inr = total_cost_inr - subsidy_amount_inr
        
        # Calculate annual production
        annual_production_kwh = required_capacity_kw * avg_sun_hours * 365 * system_efficiency
        
        # Calculate savings and payback
        annual_savings_inr = annual_production_kwh * electricity_rate_inr
        payback_years = net_cost_inr / annual_savings_inr if annual_savings_inr > 0 else 0
        
        # Additional costs for off-grid/hybrid
        battery_cost_inr = 0
        if system_type in ["off-grid", "hybrid"]:
            # Estimate battery cost (₹15,000 per kWh of storage)
            battery_capacity_kwh = daily_consumption_kwh * 2  # 2 days backup
            battery_cost_inr = battery_capacity_kwh * 15000
            total_cost_inr += battery_cost_inr
            net_cost_inr += battery_cost_inr
            payback_years = net_cost_inr / annual_savings_inr if annual_savings_inr > 0 else 0
        
        # Calculate environmental impact
        co2_offset_kg_year = annual_production_kwh * 0.82  # 0.82 kg CO2 per kWh in India
        trees_equivalent = co2_offset_kg_year / 20  # Average tree absorbs 20kg CO2/year
        
        results = {
            "daily_consumption_kwh": daily_consumption_kwh,
            "state": state or "India (Average)",
            "avg_sun_hours": avg_sun_hours,
            "system_type": system_type,
            "system_efficiency": system_efficiency,
            "required_capacity_kw": round(required_capacity_kw, 2),
            "number_of_panels": num_panels,
            "panel_wattage": panel_wattage,
            "total_area_sqm": round(total_area_sqm, 2),
            "total_area_sqft": round(total_area_sqm * 10.764, 2),
            "total_cost_inr": round(total_cost_inr, 2),
            "subsidy_amount_inr": round(subsidy_amount_inr, 2),
            "net_cost_inr": round(net_cost_inr, 2),
            "battery_cost_inr": round(battery_cost_inr, 2) if battery_cost_inr > 0 else 0,
            "annual_production_kwh": round(annual_production_kwh, 2),
            "annual_savings_inr": round(annual_savings_inr, 2),
            "payback_period_years": round(payback_years, 2),
            "co2_offset_kg_year": round(co2_offset_kg_year, 2),
            "trees_equivalent": round(trees_equivalent, 0)
        }
        
        print(f"\n� Cost Analysis (Indian Rupees):")
        print(f"   • Total System Cost: ₹{results['total_cost_inr']:,.2f}")
        print(f"   • Government Subsidy (40%): -₹{results['subsidy_amount_inr']:,.2f}")
        if battery_cost_inr > 0:
            print(f"   • Battery Cost ({system_type}): +₹{results['battery_cost_inr']:,.2f}")
        print(f"   • Net Cost After Subsidy: ₹{results['net_cost_inr']:,.2f}")
        print(f"\n📊 System Specifications:")
        print(f"   • Required Capacity: {results['required_capacity_kw']} kW")
        print(f"   • Solar Panels: {results['number_of_panels']} panels ({panel_wattage}W each)")
        print(f"   • Installation Area: {results['total_area_sqm']} m² ({results['total_area_sqft']} ft²)")
        print(f"\n⚡ Energy & Savings:")
        print(f"   • Annual Production: {results['annual_production_kwh']:,.2f} kWh")
        print(f"   • Annual Savings: ₹{results['annual_savings_inr']:,.2f}")
        print(f"   • Payback Period: {results['payback_period_years']} years")
        print(f"\n🌱 Environmental Impact:")
        print(f"   • CO₂ Offset: {results['co2_offset_kg_year']:,.2f} kg/year")
        print(f"   • Equivalent to: {results['trees_equivalent']} trees planted")
        
        return results
    
    def generate_ai_guidance(self, calculations: Dict[str, Any]) -> str:
        """Use OpenAI to generate comprehensive setup guidance for India"""
        print("\n" + "="*60)
        print("🤖 GENERATING AI-POWERED SETUP GUIDANCE (India)")
        print("="*60)
        
        # Prepare context with Wikipedia research
        wiki_context = "\n\n".join([f"{topic}:\n{content}" 
                                     for topic, content in self.research_data.items()])
        
        prompt = f"""Based on the following solar energy research and calculations, provide a comprehensive step-by-step guide for setting up a solar power plant IN INDIA.

SOLAR ENERGY RESEARCH:
{wiki_context}

CALCULATED REQUIREMENTS FOR INDIA:
- Location: {calculations['state']}
- System Type: {calculations['system_type']}
- System Capacity: {calculations['required_capacity_kw']} kW
- Number of Panels: {calculations['number_of_panels']} panels
- Total Cost: ₹{calculations['total_cost_inr']:,.2f}
- Government Subsidy: ₹{calculations['subsidy_amount_inr']:,.2f}
- Net Cost: ₹{calculations['net_cost_inr']:,.2f}
- Annual Production: {calculations['annual_production_kwh']:,.2f} kWh
- Payback Period: {calculations['payback_period_years']} years

Please provide INDIA-SPECIFIC guidance including:
1. Step-by-step installation process in Indian context
2. Government subsidies and schemes (MNRE, state schemes)
3. Required permits and approvals from DISCOMs
4. Net metering application process
5. Recommended Indian suppliers and installers
6. State-specific incentives for {calculations['state']}
7. Monsoon and weather considerations
8. Maintenance in Indian climate
9. Indian quality standards and certifications (MNRE approved)
10. Tax benefits and depreciation (for commercial)

Use Indian Rupees (₹) for all costs and reference Indian regulations."""

        try:
            print("⏳ Generating India-specific comprehensive guide...")
            response = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": "You are an expert solar energy consultant specializing in the Indian market with deep knowledge of Indian solar policies, MNRE guidelines, state-wise incentives, and local installation practices."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2500
            )
            
            guidance = response.choices[0].message.content
            print("✅ AI guidance generated successfully")
            return guidance
            
        except Exception as e:
            print(f"❌ Error generating AI guidance: {e}")
            return "Error generating guidance. Please check your OpenAI API key and connection."


def main():
    """Main function to run the interactive solar plant agent"""
    print("\n" + "🌞"*35)
    print("   INTERACTIVE SOLAR PLANT AGENT - INDIA EDITION 🇮🇳")
    print("🌞"*35 + "\n")
    
    try:
        # Initialize agent
        agent = SolarPlantAgent()
        
        # Welcome message
        print("\n👋 Namaste! I'm your Solar Energy Assistant for India!")
        print("   I can help you with:")
        print("   • Solar plant calculations and cost estimates")
        print("   • Government subsidies and schemes")
        print("   • Installation guidance and best practices")
        print("   • State-specific solar information")
        print("   • Answering your solar energy questions")
        print("\n" + "="*70)
        
        # Gather initial research
        print("\n🔍 Let me first gather some solar energy research...")
        agent.gather_solar_research()
        
        # Interactive conversation loop
        calculations = None
        
        while True:
            print("\n" + "="*70)
            print("\n💬 How can I help you? (or type 'quit' to exit)")
            print("\nOptions:")
            print("  1. Calculate solar requirements")
            print("  2. Ask a question about solar energy in India")
            print("  3. Generate complete installation report")
            print("  4. Learn about state-specific incentives")
            print("  5. Exit")
            
            choice = input("\n👉 Your choice (1-5 or ask anything): ").strip()
            
            if choice.lower() in ['quit', 'exit', '5']:
                print("\n👋 Thank you for using Solar Plant Agent! Stay solar-powered! 🌞")
                break
            
            elif choice == '1':
                # Calculate solar requirements
                print("\n" + "="*70)
                print("📊 SOLAR REQUIREMENTS CALCULATOR")
                print("="*70)
                
                daily_consumption = float(input("\n🔌 Enter your daily electricity consumption (kWh): "))
                
                print("\n📍 Select your state:")
                states_list = list(agent.india_params["states"].keys())
                for idx, state in enumerate(states_list, 1):
                    sun_hrs = agent.india_params["states"][state]
                    print(f"   {idx}. {state} ({sun_hrs} hrs/day)")
                
                state_idx = input("\n👉 Enter state number (or press Enter for average): ").strip()
                state = None
                if state_idx.isdigit() and 1 <= int(state_idx) <= len(states_list):
                    state = states_list[int(state_idx) - 1]
                
                print("\n⚡ Select system type:")
                print("   1. On-grid (Grid-tied, with net metering)")
                print("   2. Off-grid (Standalone with batteries)")
                print("   3. Hybrid (Grid + Battery backup)")
                
                system_idx = input("\n👉 Enter system type (1-3): ").strip()
                system_types = {
                    '1': 'on-grid',
                    '2': 'off-grid',
                    '3': 'hybrid'
                }
                system_type = system_types.get(system_idx, 'on-grid')
                
                # Calculate
                calculations = agent.calculate_solar_requirements(
                    daily_consumption, 
                    state=state,
                    system_type=system_type
                )
                
                print("\n✅ Calculations complete! Ask me anything about these results.")
                
            elif choice == '2':
                # Free-form question
                question = input("\n❓ Ask your question: ").strip()
                if question:
                    print("\n🤔 Let me think about that...\n")
                    response = agent.chat(question)
                    print(f"\n💡 {response}")
                
            elif choice == '3':
                # Generate report
                if calculations:
                    print("\n📄 Generating comprehensive installation report...")
                    guidance = agent.generate_ai_guidance(calculations)
                    
                    # Create report
                    report = f"""
{'='*70}
SOLAR PLANT INSTALLATION REPORT - INDIA
{'='*70}

LOCATION & SYSTEM DETAILS:
  • State: {calculations['state']}
  • System Type: {calculations['system_type'].upper()}
  • Daily Consumption: {calculations['daily_consumption_kwh']} kWh
  • Peak Sun Hours: {calculations['avg_sun_hours']} hours/day

SYSTEM SPECIFICATIONS:
  • Required Capacity: {calculations['required_capacity_kw']} kW
  • Solar Panels: {calculations['number_of_panels']} panels ({calculations['panel_wattage']}W each)
  • Installation Area: {calculations['total_area_sqm']} m² ({calculations['total_area_sqft']} ft²)

COST BREAKDOWN (INR):
  • Total System Cost: ₹{calculations['total_cost_inr']:,.2f}
  • Govt Subsidy (40%): -₹{calculations['subsidy_amount_inr']:,.2f}"""
                    
                    if calculations['battery_cost_inr'] > 0:
                        report += f"\n  • Battery Cost: +₹{calculations['battery_cost_inr']:,.2f}"
                    
                    report += f"""
  • NET COST: ₹{calculations['net_cost_inr']:,.2f}

ENERGY & FINANCIAL RETURNS:
  • Annual Production: {calculations['annual_production_kwh']:,.2f} kWh
  • Annual Savings: ₹{calculations['annual_savings_inr']:,.2f}
  • Payback Period: {calculations['payback_period_years']} years

ENVIRONMENTAL IMPACT:
  • CO₂ Offset: {calculations['co2_offset_kg_year']:,.2f} kg/year
  • Equivalent to: {calculations['trees_equivalent']} trees planted

{'='*70}
INSTALLATION GUIDANCE FOR INDIA
{'='*70}

{guidance}

{'='*70}
END OF REPORT - Generated by Solar Plant Agent 🇮🇳
{'='*70}
"""
                    
                    # Save report
                    filename = f"solar_report_{calculations['state'].replace(' ', '_')}_{calculations['required_capacity_kw']}kW.txt"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(report)
                    
                    print(f"\n✅ Report generated and saved to: {filename}")
                    print("\n" + report)
                else:
                    print("\n⚠️  Please calculate solar requirements first (Option 1)")
            
            elif choice == '4':
                # State incentives
                state_q = input("\n📍 Which state are you interested in? ").strip()
                question = f"Tell me about solar incentives, subsidies, and net metering policies in {state_q}, India. Include MNRE schemes and state-specific programs."
                print(f"\n🤔 Looking up incentives for {state_q}...\n")
                response = agent.chat(question)
                print(f"\n💡 {response}")
            
            else:
                # Treat as free-form question
                print(f"\n🤔 Let me help you with that...\n")
                response = agent.chat(choice)
                print(f"\n💡 {response}")
        
    except ValueError as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease make sure to:")
        print("1. Create a .env file with your OPENAI_API_KEY")
        print("2. Enter valid numeric values")
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye! Have a solar-powered day! 🌞")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
