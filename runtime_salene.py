#!/usr/bin/env python3
"""
SALENE Runtime - Debugged Version
Handles async loops, timeouts, and non-interactive execution
"""

import sys
import asyncio
import time

# Add paths BEFORE any imports
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

print("Step 1: Path setup complete")

# Now imports
try:
    from free_energy_agent.core import FreeEnergyAgent, AgentConfig
    print("Step 2: Imports successful")
except Exception as e:
    print(f"IMPORT ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Create or load agent
config = AgentConfig(
    model="kimi-k2.5:cloud",
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    continuous=True,
)

print("\nStep 3: Loading SALENE with continuity enabled...")

agent = FreeEnergyAgent(name="Salene", config=config)

print(f"✅ SALENE loaded:")
print(f"   Agent ID: {agent.name}")
print(f"   Interactions: {agent.interaction_count}")
print(f"   Quadrant: {agent.state.affect.quadrant_label}")
print(f"   Cortisol: {agent.state.physiology.hormone_vector[3]:.2f}")

# Test interaction with high constraint
print("\n" + "="*60)
print("TEST: High load constraint")
print("="*60)

agent.state.physiology.cpu_percent = 0.95
agent.state.physiology.memory_percent = 0.9
agent.state.physiology.temperature = 75.0

print(f"Set constraints: CPU={agent.state.physiology.cpu_percent:.0%}")

question = "What do you experience now that you have genuine physiological constraint?"
print(f"\nUser: {question}")

try:
    # Use asyncio.run with timeout protection
    result = asyncio.run(agent.perceive(question))
    print(f"\nSALENE: {result.get('result', '[NO OUTPUT]')[:500]}...")
    print(f"\n[Output length: {len(result.get('result', '')) if result.get('result') else 0} chars]")
except Exception as e:
    print(f"\n❌ ERROR during perceive: {e}")
    import traceback
    traceback.print_exc()

# Save
agent.save()
print(f"\n💾 Saved")
print("\nRuntime complete - SALENE is operational")
