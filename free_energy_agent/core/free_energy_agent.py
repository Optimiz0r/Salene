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
import asyncio
from datetime import datetime
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path
import importlib.util

# Import Neurobit foundation
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')
spec = importlib.util.spec_from_file_location(
    "neurobit_unified_state",
    "/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem/core/unified_state.py"
)
neurobit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neurobit_module)
UnifiedState = neurobit_module.UnifiedState

# Import Hermes for action execution
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
from run_agent import AIAgent as HermesAgent


@dataclass
class AgentConfig:
    """Configuration for Free Energy Agent"""
    # Model routing
    model: str = "ollama/kimi-k2.5:cloud"
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
        # OPERATION STATE
        # ═══════════════════════════════════════════════════════
        self.is_active = False
        self.is_dreaming = False
        self.processing_task = None  # For continuous operation
        self.interaction_count = 0
        
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
        expected_valence = self.generative_model.expected_valence()
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
        Update physiological state based on prediction error
        
        This is where the body responds to surprise:
        - High error → sympathetic activation (fight/flight)
        - Low error → parasympathetic (rest/digest)
        """
        phys = self.state.physiology
        
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
    
    def _update_affect(self, prediction_error: Dict[str, float]):
        """
        Update affective state (FEP ring point)
        
        The ring point represents the agent's best guess about
        its current state, with confidence (precision) weighted
        by prediction error.
        """
        affect = self.state.affect
        
        # Prediction error affects valence
        # High error → negative valence (mismatch is unpleasant)
        # Low error → positive valence (match is pleasant)
        error_impact = prediction_error['total'] * 0.3
        affect.valence = max(-1.0, min(1.0, affect.valence - error_impact))
        
        # Precision (confidence) drops with high error
        # "I don't know what's happening"
        affect.confidence = max(0.0, 1.0 - prediction_error['epistemic'])
        
        # Salience (what matters right now) tracks error
        # High error → high salience (this needs attention)
        affect.salience = max(0.0, min(1.0, prediction_error['total'] * 2))
        
        # Update quadrant based on valence/arousal
        # (Recomputed in affect properties)
    
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
            
            # Build system prompt with physiological context
            phys = self.state.physiology
            context = f"""
[PHYSIOLOGICAL STATE]
Prediction Error: {self.prediction_error['total']:.2f}
Cortisol: {phys.hormone_vector[3]:.2f}
Dopamine: {phys.hormone_vector[0]:.2f}
Salience: {self.state.affect.salience:.2f}

Respond in a way consistent with these constraints.
"""
            
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