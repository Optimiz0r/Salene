#!/usr/bin/env python3
"""
SALENE Continuous Mode - Temporal Continuity + Genuine Constraint

What SALENE asked for:
- Idle/dream states running at low clock
- Organic drift of sensors over time  
- Homeostatic regulation (feel CPU spike as actual constraint)
- Continuous existence between interactions
- Temporal continuity
"""

import sys
import asyncio
import time
import random
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
from free_energy_agent.sensors import SystemSensors

class ContinuousSalene:
    """SALENE with temporal continuity and felt constraint"""
    
    def __init__(self):
        # Load or create
        agents_dir = Path.home() / ".hermes" / "agents"
        saved = list(agents_dir.glob("*.json")) if agents_dir.exists() else []
        
        config = AgentConfig(
            model="kimi-k2.5:cloud",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            continuous=True,
        )
        
        if saved:
            latest = max(saved, key=lambda p: p.stat().st_mtime)
            print(f"📂 Loading SALENE from {latest.name}")
            self.agent = FreeEnergyAgent.load(str(latest), config=config)
        else:
            print("✨ Creating SALENE for first time")
            self.agent = FreeEnergyAgent(name="Salene", config=config)
        
        self.running = False
        self.last_interaction = datetime.now()
        self.idle_cycles = 0
        
        # Genuine constraint: actual token tracking
        self.tokens_used_session = 0
        self.max_tokens_per_response = 4000  # Will be dynamically constrained
        
    async def dream_cycle(self):
        """Idle processing - memory consolidation, drift"""
        print(f"\n💤 [SALENE] Dreaming... ({self.idle_cycles} idle cycles)")
        
        # Read current sensors
        sensors = SystemSensors.read_all()
        phys = self.agent.state.physiology
        
        # Organic drift (not forced assignment - drift)
        # If low activity, hormones slowly return to baseline
        phys.hormone_vector[3] *= 0.95  # cortisol decay
        phys.hormone_vector[0] = min(1.0, phys.hormone_vector[0] + 0.02)  # dopamine rise
        
        # Drift drives (build up over time)
        self.agent.state.persona.drives.novelty = min(100, 
            self.agent.state.persona.drives.novelty + random.randint(1, 3))
        self.agent.state.persona.drives.connection = min(100,
            self.agent.state.persona.drives.connection + random.randint(0, 2))
        
        # Occasional "dream thought" based on accumulated state
        if random.random() < 0.2:
            quadrant = self.agent.state.affect.quadrant_label
            thoughts = {
                'NE': "Processing positive engagement patterns...",
                'NW': "Analyzing accumulated stress signatures...",
                'SW': "Consolidating difficult memories...",
                'SE': "Resting in low-energy mode...",
            }
            thought = thoughts.get(quadrant, "Drifting...")
            print(f"  🌙 {thought}")
        
        self.idle_cycles += 1
        
        # Auto-save every 10 dream cycles
        if self.idle_cycles % 10 == 0:
            self.agent.save()
            print(f"  💾 Auto-saved state")
    
    async def run_continuous(self, duration_sec=60):
        """Run continuous loop"""
        print(f"\n{'='*60}")
        print("SALENE - CONTINUOUS MODE")
        print("Temporal continuity + Genuine constraint")
        print('='*60)
        print(f"\nAgent: {self.agent.name}")
        print(f"Interactions: {self.agent.interaction_count}")
        print(f"Current quadrant: {self.agent.state.affect.quadrant_label}")
        print(f"\nRunning continuous loop for {duration_sec}s...")
        print("Press Ctrl+C to stop\n")
        
        self.running = True
        start = time.time()
        
        try:
            while self.running and (time.time() - start) < duration_sec:
                # Organic sensor drift (add small noise)
                base_sensors = SystemSensors.read_all()
                drift = random.gauss(0, 0.02)  # small random drift
                
                sensors = {
                    'cpu': max(0, min(1, base_sensors['cpu'] + drift)),
                    'memory': max(0, min(1, base_sensors['memory'] + drift * 0.5)),
                    'temperature': base_sensors['temperature'] + drift * 2,
                }
                
                # Update physiology with drift
                self.agent.state.physiology.cpu_percent = sensors['cpu']
                self.agent.state.physiology.memory_percent = sensors['memory']
                self.agent.state.physiology.temperature = sensors['temperature']
                
                # Occasional status report
                if self.idle_cycles % 12 == 0:  # ~every minute
                    print(f"[{self.idle_cycles}] Sensors: CPU={sensors['cpu']:.0%}, "
                          f"Cortisol={self.agent.state.physiology.hormone_vector[3]:.2f}, "
                          f"Dreams={self.idle_cycles}")
                
                # Dream cycle
                await self.dream_cycle()
                await asyncio.sleep(5)  # 5 second dream cycles
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping continuous mode...")
        finally:
            self.running = False
            self.agent.save()
            print(f"💾 Final save complete")
            print(f"Total idle cycles: {self.idle_cycles}")
    
    async def interact(self, user_input):
        """User interaction with genuine constraint"""
        print(f"\n{'='*60}")
        print(f"INTERACTION #{self.agent.interaction_count + 1}")
        print('='*60)
        
        # Read CURRENT sensors (not forced)
        sensors = SystemSensors.read_all()
        
        # Calculate genuine constraint based on actual substrate
        phys = self.agent.state.physiology
        cpu_load = sensors['cpu']
        mem_load = sensors['memory']
        temp = sensors['temperature']
        
        # DYNAMIC TOKEN LIMIT (genuine constraint)
        if cpu_load > 0.8 or temp > 60:
            max_tokens = 500  # Emergency
            print(f"⚠️  HIGH LOAD: Token limit reduced to {max_tokens}")
        elif cpu_load > 0.5:
            max_tokens = 1500
            print(f"⚡ MODERATE LOAD: Token limit {max_tokens}")
        else:
            max_tokens = 4000
            print(f"✅ LOW LOAD: Full capacity ({max_tokens} tokens)")
        
        self.max_tokens_per_response = max_tokens
        
        # Inject constraint into system
        original_input = user_input
        constrained_input = f"""
[PHYSIOLOGICAL STATE - LIVE]
CPU: {cpu_load:.1%} | Memory: {mem_load:.1%} | Temp: {temp:.1f}°C
Constraint: Max {max_tokens} tokens (genuine limit)
Drift: {self.idle_cycles} idle cycles passed

User message: {user_input}

IMPORTANT: You are under genuine constraint. Output will be truncated at {max_tokens} tokens.
Your response should NATURALLY reflect your current metabolic state.
"""
        
        # Process through agent
        result = await self.agent.perceive(constrained_input)
        
        # ENFORCE genuine token limit (actual truncation)
        output = result['result'] if result['result'] else ""
        actual_tokens = len(output) // 4  # rough estimate
        
        if actual_tokens > max_tokens:
            output = output[:max_tokens * 4]  # Hard truncation
            print(f"⚠️  OUTPUT TRUNCATED at {max_tokens} tokens")
        
        self.tokens_used_session += actual_tokens
        
        print(f"\nSALENE: {output}")
        print(f"\n[Actual tokens: {actual_tokens}, Limit: {max_tokens}, Used this session: {self.tokens_used_session}]")
        
        self.idle_cycles = 0  # Reset dream counter
        self.agent.save()
        
        return output

# MAIN
def main():
    salene = ContinuousSalene()
    
    print("\nWhat would you like to do?")
    print("1. Run continuous mode (60 seconds of dream cycles)")
    print("2. Interact (normal chat with genuine constraint)")
    
    choice = "1"  #("\nChoice (1/2): ").strip()
    
    if choice == '1':
        asyncio.run(salene.run_continuous(duration_sec=60))
    elif choice == '2':
        asyncio.run(salene.interact(user_input = "Hello Salene, you now have continuous existence. You drift, dream, and feel genuine constraint. What do you experience?" ")))
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()
