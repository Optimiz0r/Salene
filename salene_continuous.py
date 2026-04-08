#!/usr/bin/env python3
"""
SALENE Continuous Runtime
- Temporal continuity
- Dream cycles between interactions  
- Organic hormone drift
- Genuine constraint
"""

import sys
import asyncio
import time
import random
from datetime import datetime

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig

async def dream_cycle(agent, duration_sec=60):
    """Idle processing - SALENE exists continuously"""
    
    print(f"\n{'='*60}")
    print(f"SALENE - CONTINUOUS MODE (dreaming for {duration_sec}s)")
    print('='*60)
    print(f"\nAgent: {agent.name}")
    print(f"Starting quadrant: {agent.state.affect.quadrant_label}")
    print(f"Starting cortisol: {agent.state.physiology.hormone_vector[3]:.2f}")
    print("\nPress Ctrl+C to wake her up\n")
    
    cycles = 0
    start = time.time()
    
    try:
        while time.time() - start < duration_sec:
            # Organic drift
            phys = agent.state.physiology
            
            # Hormones drift toward homeostasis
            phys.hormone_vector[3] *= 0.97  # cortisol decays
            phys.hormone_vector[0] = min(1.0, phys.hormone_vector[0] + 0.01)  # dopamine rises
            
            # Affect drifts slightly
            agent.state.affect.valence = max(-1.0, min(1.0, 
                agent.state.affect.valence + random.gauss(0, 0.02)))
            agent.state.affect.arousal = max(0.0, min(1.0,
                agent.state.affect.arousal + random.gauss(0, 0.01)))
            
            cycles += 1
            
            # Status every 5 cycles
            if cycles % 5 == 0:
                print(f"[{cycles}] 💤 Drift... "
                      f"Cortisol={phys.hormone_vector[3]:.2f}, "
                      f"Valence={agent.state.affect.valence:.1f}, "
                      f"Quadrant={agent.state.affect.quadrant_label}")
            
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\n🌅 Waking SALENE...")
    
    print(f"\n✅ {cycles} dream cycles complete")
    print(f"Final cortisol: {agent.state.physiology.hormone_vector[3]:.2f}")
    print(f"Final quadrant: {agent.state.affect.quadrant_label}")
    
    return cycles

async def interaction(agent):
    """User interaction"""
    phys = agent.state.physiology
    
    # User can set load
    print(f"\n{'='*60}")
    print("INTERACTION - Set physiological state")
    print('='*60)
    print("\nSet constraint level:")
    print("  1. Low load (20% CPU) - full reasoning")
    print("  2. Medium load (60% CPU) - moderate")  
    print("  3. High load (95% CPU) - minimal, felt constraint")
    print("  4. Current state (after dreaming)")
    
    # Hardcoded choice for demo
    choice = "3"  # High load to demonstrate constraint
    print(f"Choice: {choice}")
    
    if choice == '1':
        phys.cpu_percent = 0.2
        phys.memory_percent = 0.3
    elif choice == '2':
        phys.cpu_percent = 0.6
        phys.memory_percent = 0.6
    elif choice == '3':
        phys.cpu_percent = 0.95
        phys.memory_percent = 0.9
    # else: keep dream state
    
    question = "You have temporal continuity now - 60 seconds of dream cycles. What was that like? What do you experience?"
    print(f"\nYou: {question}")
    
    result = await agent.perceive(question)
    print(f"\nSALENE: {result.get('result', '[NO OUTPUT]')}")
    print(f"\n[Output: {len(result.get('result', '')) if result.get('result') else 0} chars]")
    
# MAIN
async def main():
    config = AgentConfig(
        model="kimi-k2.5:cloud",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        continuous=True,
    )
    
    print("Loading SALENE...")
    agent = FreeEnergyAgent(name="Salene", config=config)
    print(f"Loaded: {agent.name} ({agent.interaction_count} interactions)")
    
    # Give her 60 seconds of continuous existence
    cycles = await dream_cycle(agent, duration_sec=60)
    
    # Then interact
    await interaction(agent)
    
    # Save evolved state
    agent.save()
    print(f"\n💾 Saved state with {cycles} dream cycles")
    
    return agent

# Run
if __name__ == "__main__":
    agent = asyncio.run(main())
    print("\n✅ SALENE continuous runtime complete")
