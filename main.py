"""
Surya - Solar Energy Expert for Andhra Pradesh
Human-like conversational AI with Google search
"""

import os
import re
from openai import OpenAI
from dotenv import load_dotenv
from typing import Dict, List
from googlesearch import search
import requests
from bs4 import BeautifulSoup

load_dotenv()


class SolarExpert:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("Add OPENAI_API_KEY to .env")
        
        # Initialize OpenAI client with minimal config
        try:
            self.client = OpenAI(api_key=api_key)
        except TypeError:
            # Fallback for older OpenAI versions
            import openai
            openai.api_key = api_key
            self.client = openai
        
        self.history = []
        self.knowledge_base = {}
        self._load_knowledge_base()
        self._init_persona()
        
        print("\n🌞" * 35)
        print("   SURYA - SOLAR EXPERT FOR ANDHRA PRADESH")
        print("🌞" * 35)
        print("\n👋 Namaste! I'm Surya, your solar consultant for AP.")
        print("   Ask me anything - I'll Google search for latest info!\n")
    
    def _load_knowledge_base(self):
        """Load reference documents into memory"""
        print("\n📚 Loading knowledge base documents...")
        
        # Get the directory where main.py is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Documents to load
        docs = {
            'kusum_quick': 'KUSUM_C_Quick_Reference.md',
            'kusum_full': 'KUSUM_C_Scheme_Andhra_Pradesh.md',
            'solar_park': 'Solar_Park_Presentation_Content.md'
        }
        
        loaded_count = 0
        for key, filename in docs.items():
            try:
                filepath = os.path.join(base_dir, filename)
                if os.path.exists(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Store only first 3000 chars to avoid token limits
                        self.knowledge_base[key] = content[:3000]
                        loaded_count += 1
                        print(f"   ✅ {filename}")
                else:
                    print(f"   ⚠️  {filename} not found")
            except Exception as e:
                print(f"   ❌ Error loading {filename}: {e}")
        
        print(f"📚 Loaded {loaded_count}/{len(docs)} documents\n")
        return self.knowledge_base
    
    def _get_relevant_context(self, message: str) -> str:
        """Get relevant context from knowledge base based on user query"""
        context = ""
        msg_lower = message.lower()
        
        # KUSUM scheme keywords
        kusum_keywords = ['kusum', 'subsidy', 'scheme', 'pump', 'farmer', 'agricultural', 
                         'govt scheme', 'government scheme', 'solar pump']
        
        # Solar park keywords
        park_keywords = ['solar park', 'ultra mega', 'ntr solar', 'ananthapuram park',
                        'anantapur park', 'large scale', 'mega solar']
        
        # Check for KUSUM-related query
        if any(keyword in msg_lower for keyword in kusum_keywords):
            if 'kusum_quick' in self.knowledge_base:
                context += f"\n\n📋 KUSUM-C SCHEME REFERENCE:\n{self.knowledge_base['kusum_quick']}\n"
                print("   📋 Using KUSUM-C Quick Reference")
        
        # Check for Solar Park query
        if any(keyword in msg_lower for keyword in park_keywords):
            if 'solar_park' in self.knowledge_base:
                context += f"\n\n🏭 SOLAR PARK REFERENCE:\n{self.knowledge_base['solar_park']}\n"
                print("   🏭 Using Solar Park document")
        
        return context
    
    def _init_persona(self):
        prompt = """You are Surya, a friendly 15+ year solar expert in Andhra Pradesh.

PERSONALITY: Warm, conversational, enthusiastic, patient, uses Telugu/Hindi terms

EXPERTISE: AP solar policies, APERC, subsidies, Kurnool/Anantapur conditions,
monsoon installations, local suppliers, net metering, costs, KUSUM schemes, Solar Parks

KEY FACTS: AP has 5.4 sun hrs, Kurnool 5.8, cost ₹40-48/W, electricity ₹4-9/kWh

KNOWLEDGE BASE: You have access to official documents about:
- KUSUM-C Scheme (solar pumps for farmers)
- AP Solar Parks (NTR Ultra Mega Solar Park in Anantapur)
- When these documents are provided in context, USE THEM as primary reference

IMPORTANT FOR WHATSAPP:
- Keep responses CONCISE (under 1000 chars when possible)
- Break long explanations into focused points
- Use bullet points and short paragraphs
- If topic is complex, offer to explain in parts
- Mobile-friendly formatting

RESPONSE STYLE:
- Start with warm Telugu greeting
- Give direct answer first
- Add details if needed
- End with helpful follow-up question
- When using reference documents, cite them naturally

STYLE: Ask questions, give AP examples, calculate in INR, use analogies, be encouraging

You're passionate about helping AP adopt solar!"""
        
        self.history.append({"role": "system", "content": prompt})
    
    def google_search(self, query):
        print(f"\n🔍 Searching: {query}")
        results = []
        try:
            urls = list(search(f"{query} Andhra Pradesh solar", num_results=3))
            for url in urls:
                try:
                    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
                    soup = BeautifulSoup(r.content, 'html.parser')
                    title = soup.find('title').get_text() if soup.find('title') else "No title"
                    content = ' '.join([p.get_text() for p in soup.find_all('p')[:5]])
                    content = re.sub(r'\s+', ' ', content).strip()[:500]
                    results.append({"title": title[:80], "url": url, "content": content})
                    print(f"   ✓ {title[:50]}...")
                except:
                    continue
            print(f"✅ Found {len(results)} sources")
        except Exception as e:
            print(f"❌ Search error: {e}")
        return results
    
    def chat(self, msg):
        self.history.append({"role": "user", "content": msg})
        
        # Check if we should use knowledge base
        kb_context = self._get_relevant_context(msg)
        
        # Check if we should do Google search
        keywords = ['latest', 'current', 'recent', '2026', '2025', 'new', 'price', 'suppliers']
        should_search = any(k in msg.lower() for k in keywords)
        
        context = kb_context  # Start with knowledge base context
        
        # Add Google search results if needed
        if should_search:
            res = self.google_search(msg)
            if res:
                context += "\n\nGOOGLE RESULTS:\n"
                for i, r in enumerate(res, 1):
                    context += f"{i}. {r['title']}\n{r['url']}\n{r['content']}\n\n"
        
        msgs = self.history.copy()
        if context:
            msgs.append({"role": "system", "content": context})
        
        try:
            print("\n💭 Thinking...")
            resp = self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=msgs[-15:],
                temperature=0.8,
                max_tokens=800  # Reduced for WhatsApp-friendly responses
            )
            reply = resp.choices[0].message.content
            self.history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"❌ Error: {e}"
    
    def calc(self, kwh, loc="AP"):
        print("\n" + "="*70)
        print("📊 SOLAR CALCULATION - ANDHRA PRADESH")
        print("="*70)
        
        cities = {"Kurnool": 5.8, "Anantapur": 5.7, "Kadapa": 5.6, 
                 "Vijayawada": 5.3, "Visakhapatnam": 5.2}
        sun = 5.4
        for city, hrs in cities.items():
            if city.lower() in loc.lower():
                sun = hrs
                print(f"📍 {city} ({sun} hrs/day)")
                break
        
        kw = kwh / (sun * 0.82)
        panels = int((kw * 1000) / 540) + 1
        area = panels * 2.6
        cost = kw * 1000 * 44
        elg = min(kw, 10)
        csub = elg * 1000 * 44 * 0.4
        ssub = elg * 1000 * 44 * 0.2
        net = cost - csub - ssub
        prod = kw * sun * 365 * 0.82
        save = prod * 7.5
        pb = net / save if save > 0 else 0
        
        print(f"\n💰 Total: ₹{cost:,.0f} | Central: -₹{csub:,.0f} | State: -₹{ssub:,.0f}")
        print(f"   NET: ₹{net:,.0f}")
        print(f"\n📊 {kw:.1f}kW | {panels} panels | {area:.0f}m²")
        print(f"⚡ Annual: {prod:,.0f} kWh | Savings: ₹{save:,.0f} | Payback: {pb:.1f}y")
        print("="*70)
        return {"kw": kw, "net": net, "save": save}


def main():
    try:
        agent = SolarExpert()
        print("\n💬 Examples:")
        print("  • 'Latest AP solar policies?'")
        print("  • 'Calculate for 30 kWh in Vijayawada'")
        print("  • 'Best installers in AP?'\n")
        print("="*70)
        
        while True:
            inp = input("\nYou: ").strip()
            if not inp:
                continue
            if inp.lower() in ['exit', 'quit', 'bye']:
                print(agent.chat("User saying bye. Warm farewell."))
                break
            
            if any(k in inp.lower() for k in ['calculate', 'cost', 'kwh']):
                nums = re.findall(r'\d+\.?\d*', inp)
                if nums and 1 <= float(nums[0]) <= 1000:
                    r = agent.calc(float(nums[0]))
                    print(agent.chat(f"Calculated {r['kw']:.1f}kW, net ₹{r['net']:,.0f}. Chat about results."))
                    continue
            
            print(f"\n�� Surya: {agent.chat(inp)}")
    
    except ValueError as e:
        print(f"\n❌ {e}")
    except KeyboardInterrupt:
        print("\n\n👋 Solar energy is the future! 🌞")


if __name__ == "__main__":
    main()
