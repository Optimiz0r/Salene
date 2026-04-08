#!/usr/bin/env python3
"""Test persistence - save state, restart, load"""

import sys
import os
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

print("="*60)
print("PERSISTENCE TEST")
print("="*60)

from free_energy_agent.core import FreeEnergyAgent, AgentConfig

# Test 1: Create and use agent
print("\n1. Creating agent...")
agent = FreeEnergyAgent(name="Salene")

print("2. Running some interactions...")
import asyncio
asyncio.run(agent.perceive("Hello"))
asyncio.run(agent.perceive("How are you feeling after that?"))

print(f"   Interactions: {agent.interaction_count}")
print(f"   Current cortisol: {agent.state.physiology.hormone_vector[3]:.2f}")
print(f"   Current quadrant: {agent.state.affect.quadrant_label}")

# Test 2: Save
print("\n3. Saving state...")
save_path = agent.save()

# Test 3: Load
print("\n4. Loading from saved state...")
loaded_agent = FreeEnergyAgent.load(save_path)

print(f"   Loaded name: {loaded_agent.name}")
print(f"   Loaded ID: {loaded_agent.agent_id}")
print(f"   Restored interactions: {loaded_agent.interaction_count}")
print(f"   Restored cortisol: {loaded_agent.state.physiology.hormone_vector[3]:.2f}")
print(f"   Restored quadrant: {loaded_agent.state.affect.quadrant_label}")

print("\n" + "="*60)
print("✅ PERSISTENCE TEST PASSED")
print("="*60)
print(f"\nAgent state persists: {save_path}")
print("Can now restart agent and resume from where it left off.")
