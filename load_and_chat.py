#!/usr/bin/env python3
"""Load saved agent and chat"""

import sys
from pathlib import Path

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig

print("="*60)
print("SALENE - Physiologically-Grounded AI Companion")
print("="*60)

# Config for Ollama
config = AgentConfig(
    model="kimi-k2.5:cloud",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# Check for saved agents
agents_dir = Path.home() / ".hermes" / "agents"
saved_agents = list(agents_dir.glob("*.json")) if agents_dir.exists() else []

if saved_agents:
    latest = max(saved_agents, key=lambda p: p.stat().st_mtime)
    print(f"\n📂 Loading from {latest.name}...")
    agent = FreeEnergyAgent.load(str(latest), config=config)
else:
    print("\n✨ Creating new agent...")
    agent = FreeEnergyAgent(name="Salene", config=config)

print(f"\n✅ {agent.name} ready!")
print(f"   Interactions: {agent.interaction_count}")
print(f"   Cortisol: {agent.state.physiology.hormone_vector[3]:.2f}")
print(f"\nType to chat, 'quit' to save & exit")
print("-"*60)

import asyncio

while True:
    try:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit'):
            print("\n💾 Saving...")
            agent.save()
            print("👋 Goodbye!")
            break
        
        result = asyncio.run(agent.perceive(user_input))
        
        print(f"\nSalene: {result['result']}")
        print(f"   [Cortisol: {result['state_summary']['physiology']['cortisol']:.2f}, "
              f"Emotions: {', '.join(result['emotions']['dominant'][:2])}]")
        
    except KeyboardInterrupt:
        print("\n💾 Saving...")
        agent.save()
        print("👋 Goodbye!")
        break
