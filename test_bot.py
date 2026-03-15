"""
Local Testing Script - Test your bot before deploying
Run this to simulate WhatsApp messages without needing Twilio
"""

from main import SolarExpert
import sys

def test_bot():
    """Interactive local testing"""
    print("\n" + "="*70)
    print("🧪 LOCAL BOT TESTING MODE")
    print("="*70)
    print("\nThis simulates WhatsApp conversations without needing deployment.")
    print("Type 'quit' to exit, 'reset' to restart conversation.\n")
    
    try:
        # Initialize expert
        expert = SolarExpert()
        
        # Chat loop
        while True:
            print("\n" + "-"*70)
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye! Test complete.")
                break
            
            if user_input.lower() == 'reset':
                expert = SolarExpert()
                print("\n🔄 Conversation reset!")
                continue
            
            # Get response
            print("\n🤖 Surya: ", end="", flush=True)
            response = expert.chat(user_input)
            print(response)
    
    except KeyboardInterrupt:
        print("\n\n👋 Testing interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nMake sure:")
        print("1. OPENAI_API_KEY is set in .env")
        print("2. All dependencies are installed: pip install -r requirements.txt")


def test_single_message(message):
    """Test single message (for automation)"""
    try:
        expert = SolarExpert()
        response = expert.chat(message)
        print(f"\n📤 Input: {message}")
        print(f"📥 Output: {response}\n")
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def run_test_suite():
    """Run predefined test cases"""
    print("\n" + "="*70)
    print("🧪 RUNNING TEST SUITE")
    print("="*70 + "\n")
    
    test_cases = [
        "Hello!",
        "How much does 5kW solar cost in Vijayawada?",
        "What subsidies are available?",
        "Should I install during monsoon?",
        "Calculate ROI for ₹3000 monthly bill",
        "Best solar companies in AP?",
    ]
    
    expert = SolarExpert()
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"Test {i}/{len(test_cases)}")
        print(f"{'='*70}")
        print(f"\n👤 User: {test}")
        print(f"\n🤖 Surya: ", end="", flush=True)
        
        try:
            response = expert.chat(test)
            print(response)
            print(f"\n✅ Test {i} passed")
        except Exception as e:
            print(f"\n❌ Test {i} failed: {e}")
    
    print(f"\n{'='*70}")
    print("✅ Test suite complete!")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--suite":
            run_test_suite()
        elif sys.argv[1] == "--message":
            if len(sys.argv) > 2:
                test_single_message(" ".join(sys.argv[2:]))
            else:
                print("Usage: python test_bot.py --message 'Your message here'")
        else:
            print("Usage:")
            print("  python test_bot.py              # Interactive mode")
            print("  python test_bot.py --suite      # Run test suite")
            print("  python test_bot.py --message 'Hi'  # Test single message")
    else:
        test_bot()
