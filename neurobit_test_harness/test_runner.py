#!/usr/bin/env python3
"""
Neurobit Test Harness Runner

Simple test script to exercise NeurobitAgent with physiological cognition.
"""

import sys
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from neurobit_test_harness.core import NeurobitAgent, HormoneConfig

def main():
    print("=" * 60)
    print("Neurobit Test Harness")
    print("Physiological Agent with Hermes Tool Orchestration")
    print("=" * 60)
    print()
    
    # Create agent with default hormone configuration
    config = HormoneConfig(
        high_stress_tool_limit=3,
        low_dopamine_exploration=0.3,
        high_dopamine_repetition=0.7,
    )
    
    agent = NeurobitAgent(
        hormone_config=config,
        enabled_toolsets=None,  # Enable core tools
        platform="cli"
    )
    
    print("\nAgent initialized!")
    print("Type messages to interact, or 'quit' to exit")
    print("Use words like 'urgent', 'emergency', 'calm', 'relax' to see hormone modulation")
    print()
    
    # Interactive loop
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ("quit", "exit", "bye"):
                print("\nFinal state summary:")
                import json
                print(json.dumps(agent.get_state_summary(), indent=2))
                print("\nGoodbye!")
                break
            
            # Run conversation using Neurobit's physiological loop
            result = agent.run_conversation(user_input)
            
            print(f"\nNeurobit: {result['response']}")
            
        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except EOFError:
            break
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
