"""
Sanctuary Integration Test

Tests the synthesis of:
- Sanctuary memory (emotional, episodic)
- Sanctuary cognition (goals, drives)
- Neurobit physiology (hormones, constraint)
- Hermes execution (real-world action)
"""

import sys
import asyncio
from datetime import datetime

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
from sanctuary_integration.core import SanctuaryMemoryCore
from sanctuary_integration.phyiology_cognition_bridge import PhysiologyCognitionBridge


class SynthesisAgentTester:
    """Test harness for Sanctuary-Neurobit synthesis"""
    
    def __init__(self):
        print("=" * 70)
        print("SALENE SYNTHESIS - Sanctuary + Neurobit Integration Test")
        print("=" * 70)
        
        # Create FreeEnergyAgent (Neurobit foundation)
        config = AgentConfig(
            model="kimi-k2.5:cloud",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            continuous=False,
        )
        
        self.agent = FreeEnergyAgent(name="Salene-Synthesis", config=config)
        print(f"✓ FreeEnergyAgent created: {self.agent.agent_id}")
        
        # Initialize Sanctuary memory
        self.sanctuary_memory = SanctuaryMemoryCore(
            agent_id=self.agent.agent_id,
            max_memories=100
        )
        print(f"✓ SanctuaryMemoryCore initialized")
        
        # Initialize bridge
        self.bridge = PhysiologyCognitionBridge(self.agent)
        print(f"✓ PhysiologyCognitionBridge connected")
        
    async def test_memory_encoding_with_physiology(self):
        """Test encoding memories with physiological context"""
        print("\n" + "-" * 70)
        print("TEST 1: Memory encoding with physiology")
        
        # Encode a memory with current physiological state
        mem_data = self.bridge.encode_memory_with_physiology(
            content="The user seemed pleased with the constraint demonstration",
            tags=['interaction', 'positive', 'constraint']
        )
        
        entry = self.sanctuary_memory.encode_memory(**mem_data)
        print(f"✓ Encoded memory: {entry.memory_id[:8]}...")
        print(f"  - Emotional intensity: {entry.emotional_intensity:.2f}")
        print(f"  - Valence: {entry.valence:.2f}")
        print(f"  - Tags: {entry.tags}")
        
        # Save
        self.sanctuary_memory._save_memories()
        print(f"✓ Memory saved to disk")
        
    async def test_retrieval_by_emotion(self):
        """Test retrieving memories by emotional profile"""
        print("\n" + "-" * 70)
        print("TEST 2: Memory retrieval by emotional profile")
        
        # Get current emotional state
        emotions = self.bridge.hormones_to_emotions()
        dominant = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        
        print(f"Current emotions: {[(e, f'{v:.2f}') for e, v in dominant]}")
        
        # Retrieve memories matching current valence
        memories = self.sanctuary_memory.retrieve_by_emotion(
            target_valence=self.agent.state.affect.valence,
            valence_tolerance=0.4,
            limit=3
        )
        
        print(f"Retrieved {len(memories)} memories matching emotional profile")
        for mem in memories:
            print(f"  - {mem.content[:50]}... (valence {mem.valence:.2f})")
    
    async def test_bridge_synthesis(self):
        """Test full physiological → cognition synthesis"""
        print("\n" + "-" * 70)
        print("TEST 3: Full synthesis - physiology → emotion → cognition")
        
        synthesis = self.bridge.synthesize_full_state()
        
        print(f"\nFelt sense:")
        print(f"  {synthesis['felt_sense']}")
        
        print(f"\nPhysiological state:")
        for key, value in synthesis['physiological_state'].items():
            if isinstance(value, float):
                print(f"  - {key}: {value:.2f}")
            else:
                print(f"  - {key}: {value}")
        
        print(f"\nDominant emotions: {synthesis['dominant_emotions']}")
        print(f"Cognitive mode: {synthesis['cognitive_mode']}")
        print(f"Response style: {synthesis['response_style']}")
        
    async def test_drives_to_goals(self):
        """Test converting homeostatic drives to cognitive goals"""
        print("\n" + "-" * 70)
        print("TEST 4: Drives → Goals conversion")
        
        # Manually boost drives to test
        self.agent.state.persona.drives.novelty = 75
        self.agent.state.persona.drives.connection = 40
        self.agent.state.persona.drives.safety = 25
        
        goals = self.bridge.drives_to_goals()
        
        print(f"Current drives:")
        print(f"  - novelty: {self.agent.state.persona.drives.novelty}")
        print(f"  - connection: {self.agent.state.persona.drives.connection}")
        print(f"  - control: {self.agent.state.persona.drives.control}")
        print(f"  - safety: {self.agent.state.persona.drives.safety}")
        
        print(f"\nGenerated goals:")
        for goal in goals:
            print(f"  - [{goal['type'].upper()}] priority={goal['priority']:.2f}: {goal['description']}")
    
    async def run_all_tests(self):
        """Run complete test suite"""
        try:
            await self.test_memory_encoding_with_physiology()
            await self.test_retrieval_by_emotion()
            await self.test_bridge_synthesis()
            await self.test_drives_to_goals()
            
            print("\n" + "=" * 70)
            print("ALL TESTS PASSED ✓")
            print("=" * 70)
            print("\nSanctuary-Neurobit synthesis is operational:")
            print("  ✓ Emotional memories with physiological context")
            print("  ✓ Retrieval by emotional profile")
            print("  ✓ Bridge synthesis (physiology → felt sense → cognition)")
            print("  ✓ Drives converted to goals")
            print("\nNext: Integrate into FreeEnergyAgent perceive() loop")
            
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True


async def main():
    tester = SynthesisAgentTester()
    success = await tester.run_all_tests()
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
