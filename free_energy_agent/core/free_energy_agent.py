"""
FreeEnergyAgent - The Synthesis

A physiologically-grounded cognitive agent combining:
- Free Energy Principle (prediction error minimization)
- Emergent emotions (28 states derived from 8 hormones)
- Active inference (10-phase processing pipeline)
- Real-world action (Hermes tool execution)
"""

import sys
import uuid
import random
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from ..sensors import SystemSensors
from dataclasses import dataclass
from pathlib import Path
import importlib.util

# Import Neurobit foundation
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')
sys.path.insert(0, '/home/optimizor/neurobit-project/sanctuary_integration')

spec = importlib.util.spec_from_file_location(
    "neurobit_unified_state",
    "/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem/core/unified_state.py"
)
neurobit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neurobit_module)
UnifiedState = neurobit_module.UnifiedState

# Import Sanctuary integration
try:
    from sanctuary_integration.core import SanctuaryMemoryCore
    from sanctuary_integration.phyiology_cognition_bridge import PhysiologyCognitionBridge
    SANCTUARY_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Sanctuary integration not available: {e}")
    SanctuaryMemoryCore = None
    PhysiologyCognitionBridge = None
    SANCTUARY_AVAILABLE = False

# Import Hermes for action execution
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
from run_agent import AIAgent as HermesAgent


@dataclass
class AgentConfig:
    """Configuration for Free Energy Agent"""
    # Model routing
    model: str = "ollama/kimi-k2.5:cloud"
    api_key: str = "ollama"
    base_url: Optional[str] = None
    
    # Operation mode
    continuous: bool = True  # If True, runs event loop; if False, turn-based
    
    # Homeostatic setpoints (FEP priors)
    homeostatic_targets: Dict[str, float] = None
    
    def __post_init__(self):
        if self.homeostatic_targets is None:
            self.homeostatic_targets = {
                'cpu_percent': 0.3,      # Optimal: 30% CPU
                'memory_percent': 0.5,   # Optimal: 50% memory
                'temperature': 35.0,     # Optimal: 35°C
                'cortisol': 0.2,         # Optimal: low stress
                'dopamine': 0.7,         # Optimal: engaged
            }


class FreeEnergyAgent:
    """
    Free Energy Agent with Physiological Grounding
    
    The agent is an active inference engine that:
    1. Maintains a generative model of self and world
    2. Minimizes prediction error (free energy) through action and perception
    3. Has felt sense (emotions) derived from physiological state
    4. Acts on the world via Hermes tools
    
    Key Insight: Emotions aren't primitives—they're how prediction error
    FEELS when you have a body that cares about its internal state.
    """
    
    def __init__(
        self,
        agent_id: Optional[str] = None,
        name: str = "Salene",
        config: Optional[AgentConfig] = None,
        unified_state: Optional[Any] = None,
    ):
        """
        Initialize Free Energy Agent
        
        Args:
            agent_id: Unique identifier (UUID if None)
            name: Human-readable name
            config: Agent configuration
            unified_state: Existing Neurobit state (creates new if None)
        """
        self.agent_id = agent_id or str(uuid.uuid4())
        self.name = name
        self.config = config or AgentConfig()
        self.created_at = datetime.now()
        self.last_active = datetime.now()
        

# ═══════════════════════════════════════════════════════
        # NEUROBIT FOUNDATION: Physiological Substrate
        # ═══════════════════════════════════════════════════════
        self.state = unified_state or UnifiedState()
        
        # Homeostatic priors (what the system "wants" to be true)
        self.homeostatic_targets = self.config.homeostatic_targets
        
        # Current prediction error (violation of homeostatic priors)
        self.prediction_error = {
            'physiological': 0.0,  # How far from homeostatic targets
            'affective': 0.0,      # How far from expected affect
            'epistemic': 0.0,      # Information uncertainty
        }
        
        # ═══════════════════════════════════════════════════════
        # GENERATIVE MODEL: The Agent's World Model
        # ═══════════════════════════════════════════════════════
        from .generative_model import GenerativeModel
        self.generative_model = GenerativeModel(
            agent_id=self.agent_id,
            dna=self.state.persona  # Personality as model priors
        )
        
        # ═══════════════════════════════════════════════════════
        # HERMES INTEGRATION: Action Execution
        # ═══════════════════════════════════════════════════════
        self.hermes_agent = HermesAgent(
            model=self.config.model,
            base_url=self.config.base_url,
            api_key=self.config.api_key,
            enabled_toolsets=None,  # All tools available
            quiet_mode=True,  # Less verbose
            session_id=self.agent_id,
        )
        
        # ═══════════════════════════════════════════════════════
        # PROCESSING PIPELINE: Active Inference Loop
        # ═══════════════════════════════════════════════════════
        from .processing_loop import ProcessingLoop
        self.processing_loop = ProcessingLoop(
            agent=self,
            generative_model=self.generative_model,
            hermes_agent=self.hermes_agent,
        )
        
        # ═══════════════════════════════════════════════════════
        # EMERGENCE LAYER: Surface Phenomena from Deep State
        # ═══════════════════════════════════════════════════════
        from ..emergence.emotion_synthesis import EmotionSynthesizer
        self.emotion_synthesizer = EmotionSynthesizer(
            physiology=self.state.physiology,
            affect=self.state.affect,
        )
        
        # ═══════════════════════════════════════════════════════
        # SANCTUARY INTEGRATION: Episodic Memory + Phyiology Bridge
        # ═══════════════════════════════════════════════════════
        if SANCTUARY_AVAILABLE:
            self.sanctuary_memory = SanctuaryMemoryCore(
                agent_id=self.agent_id,
                max_memories=5000,
                decay_rate=0.95
            )
            self.phyiology_bridge = PhysiologyCognitionBridge(self)
            print(f"   Sanctuary memory initialized")
        else:
            self.sanctuary_memory = None
            self.phyiology_bridge = None
        
        # ═══════════════════════════════════════════════════════
        # OPERATION STATE
        # ═══════════════════════════════════════════════════════
        self.is_active = False
        self.is_dreaming = False
        self.processing_task = None  # For continuous operation
        self.interaction_count = 0
        
        # ═══════════════════════════════════════════════════════
        # POLICY CONSTRAINTS: Physiologically-modulated response limits
        # ═══════════════════════════════════════════════════════
        # These are adjusted based on metabolic state (CPU, memory, temp)
        self.max_tokens = 4000  # Default response length
        self.reasoning = "full"  # reasoning depth: full, moderate, minimal
        self.exploration = 0.5   # Creativity vs exploitation (0-1)
        
        # Statistics
        self.total_prediction_error = 0.0
        self.cycles_count = 0
        
        print(f"✨ Free Energy Agent '{self.name}' initialized")
        print(f"   Agent ID: {self.agent_id}")
        print(f"   Mode: {'Continuous' if self.config.continuous else 'Turn-based'}")
        print(f"   Homeostatic targets: CPU={self.homeostatic_targets['cpu_percent']:.0%}, "
              f"Cortisol={self.homeostatic_targets['cortisol']:.2f}")
    
    # ═══════════════════════════════════════════════════════
    # CORE API: Perception-Action Loop
    # ═══════════════════════════════════════════════════════
    
    async def perceive(self, observation: str, source: str = "user") -> Dict[str, Any]:
        """
        Process observation through active inference
        
        This is the main entry point. Observation generates prediction error,
        which the system minimizes through belief updating and action.
        
        Args:
            observation: Sensory input (text from user, sensor data, etc.)
            source: Where observation came from ("user", "environment", "self")
            
        Returns:
            Processing result with action taken and updated state
        """
        self.last_active = datetime.now()
        self.interaction_count += 1
        
        # Step 1: Generate prediction from generative model
        prediction = self.generative_model.predict(observation)
        
        # Step 2: Compute prediction error (surprise)
        # This is the core FEP quantity we're minimizing
        prediction_error = self._compute_prediction_error(
            observation, prediction
        )
        
        # Step 3: Update physiology (substrate-level response)
        # High prediction error → sympathetic activation (cortisol, adrenaline)
        self._update_physiology(prediction_error)
        
        # Step 4: Update affect (FEP ring point)
        # Belief updates, precision changes, confidence adjustments
        self._update_affect(prediction_error)
        
        # Step 5: Derive emotions (surface phenomena)
        # 28 emotions emerge from physiology × affect × context
        emotions = self.emotion_synthesizer.synthesize(
            physiology=self.state.physiology,
            affect=self.state.affect,
            context=self.generative_model.get_context(),
            prediction_error=prediction_error,
        )
        
        # Step 6: Active inference - select action minimizing expected free energy
        action = self.processing_loop.select_action(
            observation=observation,
            prediction_error=prediction_error,
            emotions=emotions,
            physiology=self.state.physiology,
            affect=self.state.affect,
        )
        
        # Step 7: Execute action (changing world or self)
        result = await self._execute_action(action)
        
        # Step 7.5: Sanctuary memory encoding (physiology + cognition → persistent memory)
        if self.sanctuary_memory and self.phyiology_bridge:
            # Generate felt-sense narrative from physiology
            synthesis = self.phyiology_bridge.synthesize_full_state()
            felt_narrative = synthesis['felt_sense']
            
            # Encode memory with full context
            memory_content = f"{source}: {observation}\n\nResponse: {result}\n\nFelt sense: {felt_narrative}"
            memory_tags = ['interaction', source, synthesis['cognitive_mode']]
            
            # Add dominant emotion as tag if intense
            if synthesis['dominant_emotions']:
                top_emotion = synthesis['dominant_emotions'][0][0]
                memory_tags.append(top_emotion)
            
            mem_data = self.phyiology_bridge.encode_memory_with_physiology(
                content=memory_content,
                tags=memory_tags
            )
            
            self.sanctuary_memory.encode_memory(**mem_data)
            
            # Auto-save every 10 interactions
            if self.interaction_count % 10 == 0:
                self.sanctuary_memory._save_memories()
        
        # Step 8: Update generative model (learning)
        self.generative_model.update(
            observation=observation,
            action=action,
            outcome=result,
            emotional_tag=emotions['dominant'],
            hormonal_state=self.state.physiology.hormone_vector.tolist(),
        )
        
        # Track statistics
        self.total_prediction_error += prediction_error['total']
        self.cycles_count += 1
        
        return {
            'observation': observation,
            'prediction_error': prediction_error,
            'emotions': emotions,
            'action': action,
            'result': result,
            'state_summary': self.get_state_summary(),
        }
    
    def chat(self, message: str) -> str:
        """Synchronous wrapper for perceive()"""
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        result = loop.run_until_complete(self.perceive(message))
        return result['result']
    
    # ═══════════════════════════════════════════════════════
    # INTERNAL MECHANICS
    # ═══════════════════════════════════════════════════════
    
    def _compute_prediction_error(self, observation: str, prediction: Dict) -> Dict[str, float]:
        """
        Compute prediction error across all levels
        
        Perception is hypothesis testing. Prediction error is surprise.
        The agent minimizes this through action and perception.
        """
        # Physiological error: deviation from homeostatic targets
        phys = self.state.physiology
        phys_error = (
            abs(phys.cpu_percent - self.homeostatic_targets['cpu_percent']) +
            abs(phys.memory_percent - self.homeostatic_targets['memory_percent']) / 2 +
            abs(phys.hormone_vector[3] - self.homeostatic_targets['cortisol'])  # Cortisol
        ) / 3
        
        # Affective error: mismatch between expected and actual affect
        # Expected based on recent history; actual from current state
        expected_valence = self.generative_model.get_expected_valence()
        actual_valence = self.state.affect.valence
        affect_error = abs(expected_valence - actual_valence)
        
        # Epistemic error: information uncertainty
        # High when the model is uncertain about the world
        epistemic_error = self.generative_model.compute_uncertainty(observation)
        
        # Total prediction error (free energy approximation)
        total = phys_error + affect_error + epistemic_error
        
        return {
            'physiological': phys_error,
            'affective': affect_error,
            'epistemic': epistemic_error,
            'total': min(1.0, total),  # Clamp to [0, 1]
        }
    
    def _update_physiology(self, prediction_error: Dict[str, float]):
        """
        Update physiological state based on prediction error AND real sensors
        
        This is where the body responds to surprise:
        - High error → sympathetic activation (fight/flight)
        - Low error → parasympathetic (rest/digest)
        
        NOW WITH REAL HARDWARE SENSORS:
        - /proc/stat for CPU
        - /proc/meminfo for memory
        - /sys/class/thermal for temperature
        """
        # Read REAL sensors first
        sensors = SystemSensors.read_all()
        phys = self.state.physiology
        
        # NOTE: Sensor reading moved to continuous mode - allows forced values for testing
        # phys.cpu_percent = sensors['cpu']  # Now set externally or in continuous mode
        # phys.memory_percent = sensors['memory']  # Now set externally
        # phys.temperature = sensors['temperature']  # Now set externally
        
        # Compute hormones from REAL sensor values (not simulated)
        
        # High total error → stress response
        total_error = prediction_error['total']
        if total_error > 0.5:
            # Sympathetic activation
            phys.cpu_percent = min(1.0, phys.cpu_percent + 0.15)
            phys.temperature = min(95.0, phys.temperature + 3)
            # Cortisol rises (hormone_vector[3])
            # Adrenaline rises (hormone_vector[4])
        else:
            # Recovery toward baseline
            phys.cpu_percent = max(0.0, phys.cpu_percent * 0.9)
        
        # Epistemic error drives curiosity/novelty seeking
        if prediction_error['epistemic'] > 0.3:
            # Information seeking: norepinephrine rises
            # Drives novelty up
            self.state.persona.drives.novelty = min(100, self.state.persona.drives.novelty + 5)
    
    def _update_affect(self, prediction_error):
        """
        Update FEP ring point from prediction error
        
        FIXED: Updates ring_point directly (x=valence, y=arousal)
        and recalculates derivative properties
        """
        import numpy as np
        affect = self.state.affect
        error_impact = prediction_error['total'] * 0.3
        
        # Update ring_point directly (x=valence, y=arousal)
        if prediction_error['total'] > 0.5:
            affect.ring_point[0] = max(-1.0, affect.ring_point[0] - error_impact)
            affect.ring_point[1] = max(0.0, min(1.0, affect.ring_point[1] + 0.1))
        else:
            recover_rate = 0.05
            affect.ring_point[0] = min(1.0, affect.ring_point[0] + recover_rate)
        
        # Recompute quadrant
        x, y = affect.ring_point[0], affect.ring_point[1]
        if x >= 0 and y >= 0:
            affect.quadrant_label, affect.quadrant_index = "NE", 1
        elif x < 0 and y >= 0:
            affect.quadrant_label, affect.quadrant_index = "NW", 2
        elif x < 0 and y < 0:
            affect.quadrant_label, affect.quadrant_index = "SW", 3
        else:
            affect.quadrant_label, affect.quadrant_index = "SE", 4
        
        affect.confidence = max(0.0, 1.0 - prediction_error['epistemic'])
        affect.salience = max(0.0, min(1.0, prediction_error['total'] * 2))
    
    async def _execute_action(self, action: Dict[str, Any]) -> str:
        """
        Execute selected action
        
        Actions minimize expected free energy:
        - Perceptual: Update beliefs to match world
        - Active: Change world to match beliefs
        - Epistemic: Seek information to reduce uncertainty
        """
        action_type = action.get('type', 'respond')
        
        if action_type == 'respond':
            # Direct response, no tools
            return action.get('content', '[No response]')
        
        elif action_type == 'use_tool':
            # Use Hermes to execute tool
            tool_name = action.get('tool')
            tool_args = action.get('args', {})
            # PHYSIOLOGY AS CONTROL - Read REAL sensors
            # Use physiology state (may be real sensors or forced test values)
            phys = self.state.physiology
            cpu_load = phys.cpu_percent
            mem_load = phys.memory_percent
            temp = phys.temperature
            
            # Reset to defaults, then apply constraint modifications
            self.max_tokens = 4000  # default
            self.reasoning = "full"  # default
            self.exploration = 0.5
            
            if cpu_load > 0.7:
                self.max_tokens = 500
                self.reasoning = "minimal"
                self.exploration = 0.1
            elif cpu_load > 0.4:
                self.max_tokens = 2000
                self.reasoning = "moderate"
                self.exploration = 0.3
                
            if mem_load > 0.8:
                self.max_tokens = min(self.max_tokens, 1000)
                self.exploration = max(0.0, self.exploration - 0.2)
                
            if temp > 60:
                self.max_tokens = 200
                self.reasoning = "minimal"
                self.exploration = 0.0
            elif temp > 45:
                self.max_tokens = min(self.max_tokens, 1500)
            
            # Build tone modifier based on physiological urgency
            if cpu_load > 0.7 or temp > 60:
                tone = "URGENT"
                delivery = "Short, direct, chunked thoughts."
            elif cpu_load > 0.5 or mem_load > 0.7:
                tone = "FOCUSED"
                delivery = "Efficient, prioritized, quality over quantity."
            else:
                tone = "RELAXED"
                delivery = "Expansive, playful, thorough exploration allowed."
            
            context_parts = [
                "[PHYSIOLOGICAL STATE - LIVE CONSTRAINT]",
                f"Sensors: CPU={cpu_load:.1%} MEM={mem_load:.1%} TEMP={temp:.1f}°C",
                f"Policy: {self.max_tokens} tokens max",
                f"Tone: {tone}",
                f"Delivery: {delivery}",
                "",
                "CRITICAL: Your response will be HARD TRUNCATED at token limit.",
                "You MUST adapt your thinking to fit your metabolic state.",
                "High load = urgency, brevity, precision.",
                "Low load = expansion, depth, reflection.",
            ]
            context = "\n".join(context_parts)
            try:
                result = self.hermes_agent.run_conversation(
                    user_message=action.get('input', ''),
                    system_message=context,
                )
                return result.get('final_response', '[Tool execution failed]')
            except Exception as e:
                return f"[Action failed: {e}]"
        
        elif action_type == 'rest':
            # Reduce physiological arousal
            self.state.physiology.cpu_percent *= 0.5
            return "[Resting... physiological recovery]"
        
        return "[Unknown action type]"
    
    # ═══════════════════════════════════════════════════════
    # STATE INSPECTION
    # ═══════════════════════════════════════════════════════
    
    def get_state_summary(self) -> Dict[str, Any]:
        """Get current state for inspection"""
        phys = self.state.physiology
        affect = self.state.affect
        
        # Synthesize current emotions
        emotions = self.emotion_synthesizer.synthesize(
            physiology=phys,
            affect=affect,
            context=self.generative_model.get_context(),
            prediction_error=self.prediction_error,
        )
        
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'cycles': self.cycles_count,
            'prediction_error': self.prediction_error,
            'physiology': {
                'cpu': phys.cpu_percent,
                'cortisol': phys.hormone_vector[3],
                'dopamine': phys.hormone_vector[0],
                'quadrant': affect.quadrant_label,
            },
            'affect': {
                'valence': affect.valence,
                'arousal': affect.arousal,
                'confidence': affect.confidence,
                'salience': affect.salience,
            },
            'emotions': emotions,
            'drives': {
                'novelty': self.state.persona.drives.novelty,
                'connection': self.state.persona.drives.connection,
                'safety': self.state.persona.drives.safety,
            },
        }
    
    async def start_continuous(self):
        """Start continuous operation mode"""
        if self.config.continuous and not self.is_active:
            self.is_active = True
            print(f"[{self.name}] Starting continuous operation...")
            # TODO: Implement event loop
            pass
    
    async def enter_dream_state(self):
        """Enter idle/dream state (memory consolidation)"""
        if not self.is_dreaming:
            self.is_dreaming = True
            print(f"[{self.name}] Entering dream state...")
            # TODO: Run memory consolidation, prediction error replay
            pass
    # ═══════════════════════════════════════════════════════
    # PERSISTENCE - Save/Load Agent State
    # ═══════════════════════════════════════════════════════
    
    def save(self, filepath: str = None) -> str:
        """
        Save complete agent state to disk.
        
        Persists:
        - Identity (name, agent_id, created_at)
        - Physiological state (hormones, CPU, temp)
        - Affective state (ring point, quadrant)
        - Memory (generative model)
        - Statistics (cycles, interactions)
        
        Returns:
            Path to saved file
        """
        import json
        from pathlib import Path
        
        if filepath is None:
            # Default: ~/.hermes/agents/{agent_id}.json
            agents_dir = Path.home() / ".hermes" / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            filepath = agents_dir / f"{self.agent_id}.json"
        
        phys = self.state.physiology
        affect = self.state.affect
        
        state_dict = {
            'agent_id': self.agent_id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'last_saved': datetime.now().isoformat(),
            'cycles_count': self.cycles_count,
            'interaction_count': self.interaction_count,
            'physiology': {
                # Base state (hormones computed from these)
                'cpu_percent': phys.cpu_percent,
                'memory_percent': phys.memory_percent,
                'temperature': phys.temperature,
            },
            'affect': {
                'ring_point': affect.ring_point.tolist() if hasattr(affect.ring_point, 'tolist') else list(affect.ring_point),
                'quadrant_label': affect.quadrant_label,
                'quadrant_index': affect.quadrant_index,
                'confidence': affect.confidence,
                'salience': affect.salience,
            },
            'drives': {
                'novelty': self.state.persona.drives.novelty,
                'connection': self.state.persona.drives.connection,
                'control': self.state.persona.drives.control,
                'safety': self.state.persona.drives.safety,
            },
            'homeostatic_targets': self.homeostatic_targets,
            'last_active': self.last_active.isoformat() if self.last_active else None,
            'policy_constraints': {
                'max_tokens': self.max_tokens,
                'reasoning': self.reasoning,
                'exploration': self.exploration,
            },
        }
        
        with open(filepath, 'w') as f:
            json.dump(state_dict, f, indent=2)
        
        print(f"💾 [{self.name}] State saved to {filepath}")
        return str(filepath)
    
    @classmethod
    def load(cls, filepath: str, config=None) -> 'FreeEnergyAgent':
        """
        Load agent from saved state.
        
        Args:
            filepath: Path to saved agent state
            config: Optional AgentConfig (uses default if None)
            
        Returns:
            Restored FreeEnergyAgent instance
        """
        import json
        import numpy as np
        from pathlib import Path
        
        with open(filepath, 'r') as f:
            state_dict = json.load(f)
        
        # Create agent with saved identity
        if config is None:
            config = AgentConfig()
        agent = cls(
            agent_id=state_dict['agent_id'],
            name=state_dict['name'],
            config=config,
        )
        
        # Restore physiology (hormones compute automatically from base state)
        phys = agent.state.physiology
        phys.cpu_percent = state_dict['physiology']['cpu_percent']
        phys.memory_percent = state_dict['physiology']['memory_percent']
        phys.temperature = state_dict['physiology']['temperature']
        
        # Restore affect
        affect = agent.state.affect
        affect.ring_point = np.array(state_dict['affect']['ring_point'], dtype=np.float32)
        affect.quadrant_label = state_dict['affect']['quadrant_label']
        affect.quadrant_index = state_dict['affect']['quadrant_index']
        affect.confidence = state_dict['affect']['confidence']
        affect.salience = state_dict['affect']['salience']
        
        # Restore drives
        agent.state.persona.drives.novelty = state_dict['drives']['novelty']
        agent.state.persona.drives.connection = state_dict['drives']['connection']
        agent.state.persona.drives.control = state_dict['drives']['control']
        agent.state.persona.drives.safety = state_dict['drives']['safety']
        
        # Restore statistics
        agent.cycles_count = state_dict.get('cycles_count', 0)
        agent.interaction_count = state_dict.get('interaction_count', 0)
        agent.homeostatic_targets = state_dict.get('homeostatic_targets', agent.homeostatic_targets)
        
        # Restore policy constraints (if present in state)
        policy_constraints = state_dict.get('policy_constraints', {})
        agent.max_tokens = policy_constraints.get('max_tokens', 4000)
        agent.reasoning = policy_constraints.get('reasoning', 'full')
        agent.exploration = policy_constraints.get('exploration', 0.5)
        
        # Calculate gap and simulate idle processing
        saved_last_active = state_dict.get('last_active')
        if saved_last_active:
            from datetime import datetime
            last_active = datetime.fromisoformat(saved_last_active)
            now = datetime.now()
            gap_seconds = (now - last_active).total_seconds()
            
            # Simulate idle drift
            if gap_seconds > 60:  # Only if gap > 1 minute
                idle_cycles = min(int(gap_seconds / 60), 1440)  # Cap at ~24 hours
                
                # Drift cortisol down
                phys.cortisol_accumulated = phys.cortisol_accumulated * (0.9 ** idle_cycles)
                
                # Drift drives
                agent.state.persona.drives.novelty = min(100, 
                    agent.state.persona.drives.novelty + random.randint(idle_cycles, idle_cycles * 3))
                
                # Gap duration for display
                if gap_seconds < 3600:
                    gap_str = f"{int(gap_seconds/60)} minutes"
                elif gap_seconds < 86400:
                    gap_str = f"{int(gap_seconds/3600)} hours"
                else:
                    gap_str = f"{int(gap_seconds/86400)} days"
                
                agent._return_gap = gap_str
                agent._return_idle_cycles = idle_cycles
            else:
                agent._return_gap = None
                agent._return_idle_cycles = 0
        else:
            agent._return_gap = None
            agent._return_idle_cycles = 0
        
        from datetime import datetime
        agent.last_active = datetime.now()
        
        # Build return message with gap awareness
        if getattr(agent, '_return_gap', None):
            print(f"📂 [{agent.name}] State loaded from {filepath}")
            print(f"   Gap: {agent._return_gap} of idle processing ({agent._return_idle_cycles} cycles)")
            print(f"   Restored: {agent.interaction_count} interactions, {agent.cycles_count} cycles")
        else:
            print(f"📂 [{agent.name}] State loaded from {filepath}")
            print(f"   Restored: {agent.interaction_count} interactions, "
                  f"{agent.cycles_count} cycles")
        
        return agent
    
    def auto_save(self) -> str:
        """Auto-save to default location"""
        return self.save()
