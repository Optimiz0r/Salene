#!/usr/bin/env python3
"""Test FreeEnergyAgent with Ollama (properly configured)"""

import sys
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

print("="*60)
print("FREE ENERGY AGENT + OLLAMA TEST")
print("="*60)

from free_energy_agent.core import FreeEnergyAgent, AgentConfig

# Create agent with correct Ollama config
config = AgentConfig(
    model="kimi-k2.5:cloud",  # Just the model name, not ollama/ prefix
    base_url="http://localhost:11434/v1",  # Ollama API endpoint
)

agent = FreeEnergyAgent(name="Salene", config=config)
print(f"✅ Agent created with Ollama config")
print(f"   Model: {config.model}")
print(f"   Base URL: {config.base_url}")
print()

# Test
import asyncio
result = asyncio.run(agent.perceive("Hello! Tell me about yourself briefly."))

print("RESULT:")
print(f"  Prediction error: {result['prediction_error']['total']:.2f}")
print(f"  Emotions: {result['emotions']['dominant']}")
print(f"  Action: {result['action']['type']}")
print()
print(f"RESPONSE:")
print(f"  {result['result']}")
print()
print("="*60)
print("✅ Full integration test complete!")
print("="*60)
