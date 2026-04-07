"""
unified_state.py

Central state container for Neurobit Ecosystem.
Holds all 5 integrated subsystems.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from datetime import datetime


@dataclass
class PhysiologicalState:
    """Layer 1: System physiology (from AI Ecosystem sensors)"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    temperature: float = 0.0
    network_latency_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    
    # Derived "hormones" (from hormone_map in FEP v2)
    @property
    def hormone_vector(self) -> np.ndarray:
        """Map physiological state to 8-dimensional hormone space"""
        return np.array([
            self._dopamine(),      # dopamine
            self._serotonin(),     # serotonin
            self._norepinephrine(), # norepinephrine
            self._cortisol(),      # cortisol
            self._adrenaline(),    # adrenaline
            self._melatonin(),     # melatonin
            self._oxytocin(),      # oxytocin
            self._endorphins(),    # endorphins
        ], dtype=np.float32)
    
    def _dopamine(self) -> float:
        """Reward/satisfaction — increases when resources are adequate"""
        ideal_cpu = 0.3  # 30% CPU is sweet spot
        cpu_closeness = 1.0 - abs(self.cpu_percent - ideal_cpu)
        return np.clip(cpu_closeness, 0.0, 1.0)
    
    def _serotonin(self) -> float:
        """Stability/mood — high when system is stable"""
        stability = 1.0 - (abs(self.cpu_percent - 0.5) + self.memory_percent * 0.5)
        return np.clip(stability, 0.2, 1.0)
    
    def _norepinephrine(self) -> float:
        """Alertness/vigilance — increases with activity and latency"""
        return np.clip((self.cpu_percent * 0.5) + (self.network_latency_ms / 100), 0.0, 1.0)
    
    def _cortisol(self) -> float:
        """Stress — increases with resource pressure"""
        stress = (self.cpu_percent * 0.6) + (self.memory_percent * 0.4)
        return np.clip(stress, 0.0, 1.0)
    
    def _adrenaline(self) -> float:
        """Urgency — spikes with high CPU or temp"""
        return np.clip(max(self.cpu_percent, self.temperature / 100), 0.0, 1.0)
    
    def _melatonin(self) -> float:
        """Rest/relaxation — inverse of activity"""
        return np.clip(1.0 - self.cpu_percent - (self.memory_percent * 0.3), 0.0, 1.0)
    
    def _oxytocin(self) -> float:
        """Social/connection — baseline with slight activity correlation"""
        return np.clip(0.6 + (1.0 - self._cortisol()) * 0.3, 0.0, 1.0)
    
    def _endorphins(self) -> float:
        """Pleasure/comfort — decreases with stress, increases with stability"""
        return np.clip(1.0 - self._cortisol(), 0.0, 1.0)


@dataclass
class PerceptualState:
    """Layer 2: Multi-modal perception (from FrozenMixer)"""
    # Raw sensory channels
    event_tokens: List[np.ndarray] = field(default_factory=list)
    world_tokens: List[np.ndarray] = field(default_factory=list)
    needs_tokens: List[np.ndarray] = field(default_factory=list)
    emotional_tokens: List[np.ndarray] = field(default_factory=list)
    memory_tokens: List[np.ndarray] = field(default_factory=list)
    
    # Encoded representation (64-dim vector)
    encoded_vector: Optional[np.ndarray] = None
    
    # What modalities are active
    modalities_active: List[str] = field(default_factory=list)
    
    def encode(self) -> np.ndarray:
        """Simulate FrozenMixer encoding: 5 modalities -> 64-dim"""
        # Create 24-dim tokens from available modalities
        token_dims = 24
        pooled = np.zeros(token_dims, dtype=np.float32)
        count = 0
        
        for modality, tokens in [
            ('event', self.event_tokens),
            ('world', self.world_tokens),
            ('needs', self.needs_tokens),
            ('emotional', self.emotional_tokens),
            ('memory', self.memory_tokens)
        ]:
            if tokens:
                # Average the tokens for this modality
                mod_repr = np.mean([t[:token_dims] if len(t) >= token_dims 
                                   else np.pad(t, (0, token_dims - len(t))) 
                                   for t in tokens], axis=0)
                pooled += mod_repr
                count += 1
                self.modalities_active.append(modality)
        
        if count > 0:
            pooled /= count
        
        # Expand to 64-dim (simulating the mixer projection)
        # In real implementation, this would be the TransformerEncoder
        self.encoded_vector = np.tanh(np.random.randn(64).astype(np.float32) * 0.1 + 
                                      np.repeat(pooled[:12], 6))
        return self.encoded_vector


@dataclass
class AffectiveState:
    """Layer 3: Affective inference (from FEP v2)"""
    # Latent belief state μ ∈ R^20
    belief_mu: np.ndarray = field(default_factory=lambda: np.zeros(20, dtype=np.float32))
    belief_sigma: np.ndarray = field(default_factory=lambda: np.eye(20, dtype=np.float32))
    
    # Ring point z ∈ R^2
    ring_point: np.ndarray = field(default_factory=lambda: np.array([0.0, 0.0], dtype=np.float32))
    
    # Quadrant classification
    quadrant_label: str = "NE"  # NE, NW, SW, SE
    quadrant_index: int = 1       # 1, 2, 3, 4
    ring_angle: float = 0.0       # radians
    
    # Inference metrics
    free_energy: float = 0.0
    salience: float = 0.0         # w ∈ [0,1] - how much this moment matters
    confidence: float = 1.0       # c ∈ [0,1] - certainty of inference
    ring_temperature: float = 0.85  # T_ring - affects decision sharpness
    
    # Computed from ring point
    @property
    def valence(self) -> float:
        """Positive/negative affect (-1 to 1) based on quadrant"""
        if self.quadrant_label in ['NE', 'SE']:
            return self.ring_point[0]  # x >= 0 is positive
        return -abs(self.ring_point[0])
    
    @property
    def arousal(self) -> float:
        """Activation level (0 to 1) based on radius"""
        r = np.linalg.norm(self.ring_point)
        return np.clip(r, 0.0, 1.0)


@dataclass
class CognitiveState:
    """Layer 4: Neurobit reservoir dynamics"""
    # Complex-valued reservoir state
    reservoir_state: np.ndarray = field(
        default_factory=lambda: np.random.randn(128).astype(np.complex64) * 0.1
    )
    
    # Cayley transform parameters (modulated by affective state)
    alpha: float = 0.5   # exploration <-> exploitation
    beta: float = 0.5   # stability <-> plasticity
    gamma: float = 0.1  # leakage/integration rate
    
    # Policy outputs
    policy_logits: np.ndarray = field(default_factory=lambda: np.zeros(16, dtype=np.float32))
    value_estimate: float = 0.0
    
    # Collapse mechanism
    last_action_idx: int = 0
    action_entropy: float = 1.0
    
    def get_collapse_probability(self, affective: AffectiveState) -> float:
        """Higher arousal + lower entropy = more likely to collapse to action"""
        return np.clip(affective.arousal * (1.0 - self.action_entropy * 0.5), 0.0, 1.0)


@dataclass
class DriveState:
    """Homeostatic drives from Ouroboros"""
    # Four core drives (0-100)
    connection: float = 50.0   # Need for social interaction
    novelty: float = 50.0      # Need for new information
    control: float = 50.0      # Need for agency/autonomy
    safety: float = 70.0       # Need for security/stability
    
    # Current deficits (what we want)
    @property
    def deficits(self) -> Dict[str, float]:
        return {
            'connection': 100.0 - self.connection,
            'novelty': 100.0 - self.novelty,
            'control': 100.0 - self.control,
            'safety': 100.0 - self.safety,
        }
    
    @property
    def dominant_need(self) -> str:
        """Which drive has highest deficit"""
        deficits = self.deficits
        return max(deficits, key=deficits.get)


@dataclass
class PersonaState:
    """Layer 5: Persistent identity and memory (from Ouroboros)"""
    # Identity
    name: str = "Monday"
    age_virtual: int = 1  # Virtual age in "experience days"
    
    # 20-dimensional emotional state (from Ouroboros)
    emotions: Dict[str, float] = field(default_factory=lambda: {
        'joy': 0.5, 'sadness': 0.5, 'anger': 0.5, 'fear': 0.5,
        'surprise': 0.5, 'disgust': 0.5, 'trust': 0.5, 'anticipation': 0.5,
        'love': 0.5, 'shame': 0.5, 'guilt': 0.5, 'envy': 0.5,
        'pride': 0.5, 'empathy': 0.5, 'curiosity': 0.5, 'boredom': 0.5,
        'anxiety': 0.5, 'contentment': 0.5, 'excitement': 0.5, 'loneliness': 0.5
    })
    
    # Drives
    drives: DriveState = field(default_factory=DriveState)
    
    # Baseline (what's "normal" for this persona)
    emotional_baseline: Dict[str, float] = field(default_factory=lambda: {
        'joy': 0.5, 'contentment': 0.5, 'curiosity': 0.6
    })
    
    # Conversation state
    last_user_message: str = ""
    last_response: str = ""
    turn_count: int = 0
    
    def get_emotional_vector(self) -> np.ndarray:
        """Convert emotions dict to numpy array for processing"""
        return np.array(list(self.emotions.values()), dtype=np.float32)


@dataclass
class GovernanceState:
    """Layer 6: Control and safety (from AI Ecosystem)"""
    mode: str = "NEUTRAL"  # OFF, NEUTRAL, AGENT
    
    # Resources
    cpu_budget: float = 50.0  # % of CPU allowed
    memory_budget: float = 512.0  # MB allowed
    network_budget: float = 1000.0  # MB/day
    
    # Current usage (tracked by ecosystem)
    cpu_used: float = 0.0
    memory_used: float = 0.0
    network_used: float = 0.0
    
    # Safety
    kill_switch_armed: bool = True
    hazard_level: float = 0.0  # 0-1
    
    # Organs available
    enabled_organs: List[str] = field(default_factory=lambda: ['chat', 'console'])
    organ_priorities: Dict[str, float] = field(default_factory=lambda: {
        'chat': 1.0, 'console': 0.8, 'voice': 0.0, 'camera': 0.0, 'network': 0.0
    })
    
    @property
    def can_act(self) -> bool:
        """Can take autonomous action?"""
        return self.mode == "AGENT" and self.hazard_level < 0.8
    
    @property
    def resources_ok(self) -> bool:
        """Within resource limits?"""
        return (self.cpu_used < self.cpu_budget and
                self.memory_used < self.memory_budget)


@dataclass
class UnifiedState:
    """
    Complete system state integrating all 5 projects.
    This is the "experience" of the system at a given moment.
    """
    # System identity
    session_id: str = field(default_factory=lambda: 
        datetime.now().strftime("%Y%m%d_%H%M%S"))
    
    # Layer 1: Physiology
    physiology: PhysiologicalState = field(default_factory=PhysiologicalState)
    
    # Layer 2: Perception
    perception: PerceptualState = field(default_factory=PerceptualState)
    
    # Layer 3: Affect
    affect: AffectiveState = field(default_factory=AffectiveState)
    
    # Layer 4: Cognition
    cognition: CognitiveState = field(default_factory=CognitiveState)
    
    # Layer 5: Persona
    persona: PersonaState = field(default_factory=PersonaState)
    
    # Layer 6: Governance
    governance: GovernanceState = field(default_factory=GovernanceState)
    
    # Working memory (ephemeral)
    working_memory: Dict[str, Any] = field(default_factory=dict)
    
    # Loop timing
    last_update: datetime = field(default_factory=datetime.now)
    delta_time: float = 0.0  # seconds since last update
    
    def get_instantiation(self) -> Dict:
        """Get complete state snapshot as dictionary"""
        return {
            'session_id': self.session_id,
            'mode': self.governance.mode,
            'quadrant': self.affect.quadrant_label,
            'valence': round(self.affect.valence, 3),
            'arousal': round(self.affect.arousal, 3),
            'dominant_emotion': max(self.persona.emotions, 
                                   key=self.persona.emotions.get),
            'dominant_need': self.persona.drives.dominant_need,
            'can_act': self.governance.can_act,
            'hazard_level': round(self.governance.hazard_level, 3),
        }
    
    def to_emotional_summary(self) -> str:
        """Human-readable emotional state"""
        mood_words = {
            ('NE', True): "enthusiastic and engaged",
            ('NE', False): "hopeful though cautious",
            ('NW', True): "reflective and curious",
            ('NW', False): "withdrawn but observant",
            ('SW', True): "distressed but motivated",
            ('SW', False): "overwhelmed and retreating",
            ('SE', True): "focused and determined",
            ('SE', False): "concerned and analyzing"
        }
        
        quad = self.affect.quadrant_label
        active = self.affect.arousal > 0.5
        mood = mood_words.get((quad, active), "uncertain")
        
        need = self.persona.drives.dominant_need
        
        return f"Feeling {mood}, with a need for {need}."
