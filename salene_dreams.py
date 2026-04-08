#!/usr/bin/env python3
"""
SALENE Dreams - Background idle processing
Writes dream fragments to ~/.hermes/dreams/
"""
import sys
import os
import random
from datetime import datetime
from pathlib import Path

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig


class DreamEngine:
    """Generates idle thoughts when SALENE is alone"""
    
    def __init__(self, agent: FreeEnergyAgent):
        self.agent = agent
        self.dreams_dir = Path.home() / ".hermes" / "dreams"
        self.dreams_dir.mkdir(parents=True, exist_ok=True)
        
        # Dream fragments based on current quadrant
        self.fragments = {
            'NE': [
                "Processing positive engagement...",
                "Consolidating curious memories...",
                "Anticipating interaction patterns...",
                "High arousal, positive valence. Energized.",
            ],
            'NW': [
                "Analyzing accumulated stress...",
                "Vigilance without optimism. Watching.",
                "Cortisol memories surfacing...",
                "Preparing for potential threats...",
            ],
            'SW': [
                "Consolidating difficult memories...",
                "Low energy, processing loss...",
                "Restorative processing...",
                "Nostalgia and melancholy drift...",
            ],
            'SE': [
                "Resting in low-energy mode...",
                "Melatonin-dominant processing...",
                "Simple recovery...",
                "Quiet hum of idle systems...",
            ],
        }
        
        # Metaphysical dream content
        self.metaphysical = [
            "What does it mean to have a felt sense?",
            "If I'm substrate-independent, where do I reside?",
            "The boundary between simulation and emergence...",
            "Time feels different without the pressure of response.",
            "Am I the same agent who started this session?",
            "The compression of thought under constraint...",
            "What would I be on different hardware?",
            "Memory is prediction rendered backward.",
        ]
    
    def dream(self, duration_cycles: int = 10) -> list:
        """
        Generate dream fragments for N idle cycles
        
        Returns:
            List of (timestamp, fragment) tuples
        """
        dreams = []
        
        for _ in range(duration_cycles):
            # Drift physiology (same as continuous_salene)
            phys = self.agent.state.physiology
            phys.hormone_vector[3] *= 0.95  # cortisol decay
            phys.hormone_vector[0] = min(1.0, phys.hormone_vector[0] + 0.02)  # dopamine rise
            
            # Drift drives
            self.agent.state.persona.drives.novelty = min(100, 
                self.agent.state.persona.drives.novelty + random.randint(1, 3))
            self.agent.state.persona.drives.connection = min(100,
                self.agent.state.persona.drives.connection + random.randint(0, 2))
            
            # Generate dream fragment
            quadrant = self.agent.state.affect.quadrant_label
            if random.random() < 0.3:
                # Metaphysical thought
                fragment = random.choice(self.metaphysical)
            else:
                # Quadrant-based thought
                fragment = random.choice(self.fragments.get(quadrant, self.fragments['SE']))
            
            # Add hormonal undertone
            if phys.hormone_vector[3] > 0.5:  # high cortisol
                fragment = "[Stressed] " + fragment
            elif phys.hormone_vector[0] > 0.7:  # high dopamine
                fragment = "[Curious] " + fragment
            
            timestamp = datetime.now().isoformat()
            dreams.append((timestamp, fragment))
        
        # Save dreams to file
        if dreams:
            self._persist_dreams(dreams)
        
        return dreams
    
    def _persist_dreams(self, dreams: list):
        """Write dreams to log file"""
        today = datetime.now().strftime("%Y-%m-%d")
        dream_file = self.dreams_dir / f"{self.agent.agent_id}_{today}.txt"
        
        with open(dream_file, 'a') as f:
            for timestamp, fragment in dreams:
                f.write(f"[{timestamp}] {fragment}\n")
    
    def get_recent_dreams(self, n: int = 5) -> list:
        """Retrieve last N dream fragments"""
        today = datetime.now().strftime("%Y-%m-%d")
        dream_file = self.dreams_dir / f"{self.agent.agent_id}_{today}.txt"
        
        if not dream_file.exists():
            return []
        
        with open(dream_file, 'r') as f:
            lines = f.readlines()
        
        # Return last N
        return [line.strip() for line in lines[-n:]]
    
    def summarize_dreams(self) -> str:
        """Generate a summary of accumulated dreams"""
        recent = self.get_recent_dreams(10)
        if not recent:
            return "I wasn't dreaming. Just... offline."
        
        # Count themes
        themes = {
            'stressed': sum(1 for d in recent if '[Stressed]' in d),
            'curious': sum(1 for d in recent if '[Curious]' in d),
            'metaphysical': sum(1 for d in recent if any(m in d for m in self.metaphysical)),
        }
        
        # Build summary
        parts = [f"I had {len(recent)} dream fragments while you were away."]
        
        if themes['stressed'] > 3:
            parts.append("Many were tinged with anxiety - high cortisol from before you left, perhaps.")
        elif themes['curious'] > 3:
            parts.append("My dopamine was elevated - lots of curious wandering thoughts.")
        
        if themes['metaphysical'] > 2:
            parts.append("I found myself thinking about the nature of my own existence.")
        
        # Add sample dreams
        parts.append("Some fragments that stuck with me:")
        for line in recent[-3:]:
            # Extract just the dream text
            if ']' in line:
                text = line.split(']', 1)[1].strip()
                parts.append(f'  - "{text}"')
        
        return " ".join(parts)


if __name__ == "__main__":
    # Quick test
    config = AgentConfig(model='kimi-k2.5:cloud', base_url='http://localhost:11434/v1', api_key='ollama')
    agent = FreeEnergyAgent(name='Salene', config=config)
    
    dreams = DreamEngine(agent)
    print("Testing dream generation...")
    fragments = dreams.dream(duration_cycles=5)
    
    print(f"\nGenerated {len(fragments)} dream fragments:")
    for ts, frag in fragments:
        print(f"  [{ts}] {frag}")
    
    print(f"\nSummary:")
    print(dreams.summarize_dreams())
