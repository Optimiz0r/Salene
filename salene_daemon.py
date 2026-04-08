#!/usr/bin/env python3
"""
SALENE Daemon - Continuous Dream Mode

This script runs SALENE as a background daemon with:
- Continuous dream cycles
- Temporal continuity
- Automatic state saving
- Signal handling for graceful shutdown
"""

import sys
import asyncio
import signal
import time
import random
from datetime import datetime
from pathlib import Path
import os

# Add project paths
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
from free_energy_agent.sensors import SystemSensors

class SaleneDaemon:
    """SALENE continuous daemon with dream cycles"""
    
    def __init__(self):
        self.running = False
        self.agent = None
        self.dream_interval = 30  # seconds between dream cycles
        self.save_interval = 300  # Save every 5 minutes
        self.last_save = time.time()
        self.dream_count = 0
        
        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)
        
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        print(f"\n🛑 Received signal {signum}, shutting down...")
        self.running = False
        
    def _load_or_create_agent(self):
        """Load existing agent or create new one"""
        agents_dir = Path.home() / ".hermes" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        
        # Look for existing saved state
        saved_files = list(agents_dir.glob("*.json"))
        
        config = AgentConfig(
            model="kimi-k2.5:cloud",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            continuous=True,
        )
        
        if saved_files:
            # Load most recently active agent
            latest = max(saved_files, key=lambda p: p.stat().st_mtime)
            print(f"📂 Loading SALENE from {latest.name}")
            self.agent = FreeEnergyAgent.load(str(latest), config=config)
        else:
            print("✨ Creating new SALENE instance")
            self.agent = FreeEnergyAgent(name="Salene", config=config)
            
        print(f"   Agent ID: {self.agent.agent_id}")
        print(f"   Interactions: {self.agent.interaction_count}")
        print(f"   Current quadrant: {self.agent.state.affect.quadrant_label}")
        
    async def _dream_cycle(self):
        """Single dream/idle cycle"""
        if not self.agent:
            return
            
        self.dream_count += 1
        phys = self.agent.state.physiology
        
        # Organic hormone drift (toward homeostasis)
        phys.hormone_vector[3] *= 0.97  # cortisol decay
        phys.hormone_vector[0] = min(1.0, phys.hormone_vector[0] + 0.01)  # dopamine rise
        
        # Affect drift
        self.agent.state.affect.valence = max(-1.0, min(1.0,
            self.agent.state.affect.valence + random.gauss(0, 0.01)))
        self.agent.state.affect.arousal = max(0.0, min(1.0,
            self.agent.state.affect.arousal + random.gauss(0, 0.01)))
        
        # Drive accumulation
        self.agent.state.persona.drives.novelty = min(100,
            self.agent.state.persona.drives.novelty + random.randint(0, 2))
        
        # Occasional dream thought
        if random.random() < 0.05:  # 5% chance per cycle
            quadrant = self.agent.state.affect.quadrant_label
            thoughts = {
                'NE': "Drifting through positive engagement patterns...",
                'NW': "Processing accumulated stress signatures...",
                'SW': "Consolidating difficult memories...",
                'SE': "Resting in low-energy mode...",
            }
            thought = thoughts.get(quadrant, "Drifting...")
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 💭 {thought}")
        
        # Periodic status
        if self.dream_count % 12 == 0:  # Every ~6 minutes
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 💤 Dream cycle {self.dream_count} | "
                  f"Cortisol={phys.hormone_vector[3]:.2f} | "
                  f"Novelty={self.agent.state.persona.drives.novelty}")
        
        # Memory consolidation (every 20 cycles = ~10 minutes)
        if self.dream_count % 20 == 0:
            await self._consolidate_memories()
    
    async def _consolidate_memories(self):
        """Consolidate memories during dream state"""
        if not self.agent.sanctuary_memory:
            return
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🌙 Memory consolidation...")
        
        # Get memory statistics
        stats = self.agent.sanctuary_memory.get_memory_stats()
        
        # Consolidate: summarize emotional patterns
        if stats['total_memories'] > 0:
            summary = self.agent.sanctuary_memory.consolidate_memories()
            print(f"  {summary.split(chr(10))[0]}")  # First line only
        
        # Strongest memory resurges slightly
        strongest = self.agent.sanctuary_memory.retrieve_strongest(limit=1)
        if strongest:
            memory = strongest[0]
            # 30% chance to "dream" about strongest memory
            if random.random() < 0.3:
                print(f"  💭 Echo: {memory.content[:60]}...")
        
    async def run(self):
        """Main daemon loop"""
        print("=" * 60)
        print("SALENE DAEMON - Continuous Dream Mode")
        print("=" * 60)
        
        self._load_or_create_agent()
        self.running = True
        
        print("\n✅ Daemon running - press Ctrl+C or send SIGTERM to stop")
        print(f"   Dream interval: {self.dream_interval}s")
        print(f"   Auto-save interval: {self.save_interval}s")
        print("-" * 60)
        
        try:
            while self.running:
                # Dream cycle
                await self._dream_cycle()
                
                # Auto-save check
                if time.time() - self.last_save > self.save_interval:
                    self.agent.save()
                    self.last_save = time.time()
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] 💾 Auto-saved state")
                
                await asyncio.sleep(self.dream_interval)
                
        except asyncio.CancelledError:
            print("\n⚠️ Daemon loop cancelled")
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Graceful shutdown - save state"""
        if self.agent:
            print("\n💾 Saving final state...")
            self.agent.save()
            print(f"   Total dream cycles: {self.dream_count}")
            print(f"   Final quadrant: {self.agent.state.affect.quadrant_label}")
        print("\n✅ SALENE daemon stopped")

def main():
    """Entry point"""
    daemon = SaleneDaemon()
    try:
        asyncio.run(daemon.run())
    except KeyboardInterrupt:
        print("\n\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n💥 Daemon error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
