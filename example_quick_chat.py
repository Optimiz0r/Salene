#!/usr/bin/env python3
"""
SALENE Quick Chat Example

Simplest way to talk with SALENE once.
Loads from saved state if available, chats, saves back.
"""

import sys
import asyncio

# Setup paths
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig

def print_banner():
    print("""
\033[38;5;87m              .""--.._\033[0m
\033[38;5;87m              []      `'--.._.\033[0m
\033[38;5;75m              ||__    __    _'-._\033[0m

\033[1m\033[38;5;87m              S A L E N E\033[0m
\033[38;5;75m     Quick Chat Example\033[0m
    """)

async def main():
    print_banner()
    
    config = AgentConfig(
        model="kimi-k2.5:cloud",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        continuous=False,
    )
    
    # Load or create
    import os
    from pathlib import Path
    
    agents_dir = Path.home() / ".hermes" / "agents"
    agent = None
    
    if agents_dir.exists():
        saved = list(agents_dir.glob("*.json"))
        if saved:
            latest = max(saved, key=lambda p: p.stat().st_mtime)
            print(f"📂 Loading SALENE from {latest.name}")
            agent = FreeEnergyAgent.load(str(latest), config=config)
    
    if not agent:
        print("✨ Creating new SALENE instance")
        agent = FreeEnergyAgent(name="Salene", config=config)
    
    # Chat
    print(f"\n💙 SALENE is ready. Type '/quit' to exit.\n")
    
    while True:
        try:
            user_input = input("\033[38;5;87mYou:\033[0m ").strip()
            
            if user_input.lower() in ['/quit', '/exit', 'exit', 'quit']:
                break
            
            if not user_input:
                continue
            
            # Process
            result = await agent.perceive(user_input)
            
            # Show response
            response = result.get('result', '[No response]')
            print(f"\033[38;5;75mSALENE:\033[0m {response[:500]}")
            
            # Show felt sense if available
            if agent.phyiology_bridge:
                synthesis = agent.phyiology_bridge.synthesize_full_state()
                print(f"\033[2m  [Felt: {synthesis['felt_sense'][:60]}...]\033[0m")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye! 💙")
            break
        except EOFError:
            print("\n\n[EOF received, exiting] 💙")
            break
    
    # Save
    agent.save()
    print("\n💾 SALENE's state saved.")

if __name__ == "__main__":
    asyncio.run(main())
