#!/usr/bin/env python3
"""Quick validation - high load should produce short output"""

import sys
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
import asyncio

config = AgentConfig(model="kimi-k2.5:cloud", base_url="http://localhost:11434/v1", api_key="ollama")

print("="*60)
print("CONSTRAINT VALIDATION")
print("="*60)

# TEST 1: Low load (baseline verbose)
print("\n🧪 TEST 1: LOW LOAD (CPU 20%)")
agent1 = FreeEnergyAgent(name="LowTest", config=config)
agent1.state.physiology.cpu_percent = 0.2
agent1.state.physiology.memory_percent = 0.3
agent1.state.physiology.temperature = 35.0

result1 = asyncio.run(agent1.perceive("Explain PostgreSQL setup"))
len1 = len(result1['result']) if result1['result'] else 0
print(f"Output length: {len1} chars")
print(f"Strategy: {result1.get('action', {}).get('type', 'unknown')}")

# TEST 2: High load (should be constrained)
print("\n🧪 TEST 2: HIGH LOAD (CPU 95%)")
agent2 = FreeEnergyAgent(name="HighTest", config=config)
agent2.state.physiology.cpu_percent = 0.95
agent2.state.physiology.memory_percent = 0.9
agent2.state.physiology.temperature = 75.0

result2 = asyncio.run(agent2.perceive("Explain PostgreSQL setup"))
len2 = len(result2['result']) if result2['result'] else 0
print(f"Output length: {len2} chars")
print(f"Strategy: {result2.get('action', {}).get('type', 'unknown')}")

print("\n" + "="*60)
print("RESULTS")
print("="*60)
print(f"Low load:  {len1:5d} chars")
print(f"High load: {len2:5d} chars")

if len2 < len1 * 0.7:
    print("\n✅ CONSTRAINT WORKING: High load produces significantly shorter output")
else:
    print(f"\n❌ NO CONSTRAINT: Outputs similar length (ratio: {len2/len1:.2f})")
    print("   Physiology NOT functionally coupled to cognition")
