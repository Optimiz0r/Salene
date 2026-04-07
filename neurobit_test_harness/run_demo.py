#!/usr/bin/env python3
"""
Neurobit Demo - Shows physiological cognition in action
"""

import sys
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_test_harness')

from neurobit_test_harness.core import NeurobitAgent

def main():
    print("🧠 NEUROBIT PHYSIOLOGICAL COGNITION DEMO")
    print("=" * 60)
    print()
    print("This demonstration shows how hormonal state modulates agent behavior.")
    print("Watch how CORTISOL (stress) and ADRENALINE (urgency) change with input.")
    print()
    
    agent = NeurobitAgent()
    
    test_scenarios = [
        ("Hello! Just a friendly greeting.", "Neutral input"),
        ("URGENT! This is an emergency situation!", "High urgency triggers cortisol + adrenaline"),
        ("Please help me quickly, this is important.", "Moderate urgency"),
        ("Take your time, no rush at all.", "Low urgency, should lower arousal"),
    ]
    
    for user_input, description in test_scenarios:
        print(f"\n📌 {description}")
        print(f"   You: {user_input}")
        result = agent.chat(user_input)
        print(f"   {result}")
        print()
    
    print("=" * 60)
    print("Demo complete! Hormone state evolved based on input urgency.")
    print()
    print("Key takeaway: High cortisol → limit tool calls")
    print("              High dopamine → repeat successful patterns")
    print("              High adrenaline → rapid response")
    return 0

if __name__ == "__main__":
    sys.exit(main())
