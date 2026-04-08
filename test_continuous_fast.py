#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
from free_energy_agent.continuous_mode import ContinuousAgentMode

print("="*50)
print("CONTINUOUS MODE + REAL SENSORS")
print("="*50)

agent = FreeEnergyAgent(name="Salene", config=AgentConfig())
continuous = ContinuousAgentMode(agent)

import asyncio
asyncio.run(continuous.run(duration_sec=10))

print("\n✅ Continuous mode works!")
print("Real sensors updating agent physiology every second")
