#!/usr/bin/env python3
"""
SALENE Memory Retrieval Example

Demonstrates Sanctuary-style memory retrieval:
- By emotional profile
- By context tags
- Strongest memories
"""

import sys
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
from pathlib import Path

def print_banner():
    print("""
\033[38;5;87m              .""--.._\033[0m
\033[38;5;87m              []      `'--.._.\033[0m
\033[38;5;75m              ||__    __    _'-._\033[0m

\033[1m\033[38;5;87m         M E M O R I E S\033[0m
\033[38;5;75m     Episodic Retrieval Demo\033[0m
    """)

def main():
    print_banner()
    
    # Load agent (we need the Sanctuary memory)
    config = AgentConfig(
        model="kimi-k2.5:cloud",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
        continuous=False,
    )
    
    agents_dir = Path.home() / ".hermes" / "agents"
    agent = None
    
    if agents_dir.exists():
        saved = list(agents_dir.glob("*.json"))
        if saved:
            latest = max(saved, key=lambda p: p.stat().st_mtime)
            print(f"📂 Loading SALENE from {latest.name}\n")
            agent = FreeEnergyAgent.load(str(latest), config=config)
    
    if not agent or not agent.sanctuary_memory:
        print("❌ No SALENE with Sanctuary memory found")
        print("Run example_quick_chat.py first to create memories")
        return
    
    # Get stats
    stats = agent.sanctuary_memory.get_memory_stats()
    print(f"📊 Memory Statistics:")
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Total created: {stats['total_created']}")
    print(f"  Storage: {stats['storage_path']}")
    print()
    
    if stats['total_memories'] == 0:
        print("ℹ️  No memories yet. Interact with SALENE first.")
        return
    
    # Retrieve by current emotional state
    print("\033[38;5;87m=== Memories Matching Current Emotional Profile ===\033[0m\n")
    memories = agent.sanctuary_memory.retrieve_by_emotion(
        target_valence=agent.state.affect.valence,
        valence_tolerance=0.5,
        limit=3
    )
    
    for i, mem in enumerate(memories, 1):
        print(f"\033[38;5;75m[{i}]\033[0m Strength: {mem.calculate_current_strength():.2f}")
        print(f"    Valence: {mem.valence:.2f}, Arousal: {mem.arousal:.2f}")
        print(f"    Content: {mem.content[:100]}...")
        print(f"    Tags: {', '.join(mem.tags)}")
        print()
    
    # Retrieve strongest memories
    print("\033[38;5;87m=== Strongest Memories ===\033[0m\n")
    strongest = agent.sanctuary_memory.retrieve_strongest(limit=3)
    
    for i, mem in enumerate(strongest, 1):
        print(f"\033[38;5;75m[{i}]\033[0m Strength: {mem.calculate_current_strength():.2f}")
        print(f"    {mem.content[:100]}...")
        print()
    
    # Memory consolidation
    print("\033[38;5;87m=== Memory Consolidation ===\033[0m\n")
    summary = agent.sanctuary_memory.consolidate_memories()
    print(summary)

if __name__ == "__main__":
    main()
