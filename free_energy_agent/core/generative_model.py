"""
Generative Model - The Agent's World Model

Maintains priors about:
- Self (identity, traits, values)
- World (how things work)
- Others (social relationships)
- Past (episodic memory)
- Future (predictions, goals)

Updates via prediction error minimization (FEP).
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import numpy as np


@dataclass
class MemoryEntry:
    """Single episodic memory"""
    content: str
    timestamp: datetime
    importance: float  # 0.0-1.0
    emotional_tags: List[str]
    hormonal_state: List[float]  # 8 hormones at encoding time
    context: Dict[str, Any]


class GenerativeModel:
    """
    The agent's model of self and world.
    
    Under FEP: This is the generative model p(o,s) that generates
    observations from hidden states. The agent minimizes prediction
    error by updating beliefs about states or changing the world.
    """
    
    def __init__(self, agent_id: str, dna=None):
        self.agent_id = agent_id
        self.dna = dna
        
        # Memory stores
        self.episodic_memory: List[MemoryEntry] = []
        self.semantic_memory: Dict[str, Any] = {}
        self.procedural_memory: Dict[str, Any] = {}
        
        # Predictions
        self.expected_valence: float = 0.0
        self.expected_arousal: float = 0.2
        self.uncertainty: float = 0.5
        
        # Statistics
        self.memories_stored = 0
        self.last_update = datetime.now()
    
    def predict(self, observation: str) -> Dict[str, Any]:
        """
        Generate prediction about observation
        
        Returns what the model expects to perceive,
        based on current state and past experience.
        """
        # Simple prediction based on recent valence expectation
        return {
            'expected_valence': self.expected_valence,
            'expected_arousal': self.expected_arousal,
            'uncertainty': self.uncertainty,
            'prediction': f"Input: {observation[:30]}...",
        }
    
    def get_expected_valence(self) -> float:
        """Expected emotional valence"""
        return self.expected_valence
    
    def compute_uncertainty(self, observation: str) -> float:
        """
        Compute epistemic uncertainty
        
        Returns: 0.0-1.0 where higher = more uncertain
        """
        # More memories = lower uncertainty
        memory_factor = max(0.0, 1.0 - (len(self.episodic_memory) / 100))
        
        # Novel observations increase uncertainty
        novelty = 0.3  # Simplified
        
        return min(1.0, (self.uncertainty + memory_factor + novelty) / 3)
    
    def update(
        self,
        observation: str,
        action: Dict[str, Any],
        outcome: str,
        emotional_tag: str,
        hormonal_state: List[float]
    ):
        """
        Update generative model from experience (learning)
        
        This is where prediction error is used to update priors.
        """
        # Create memory entry
        memory = MemoryEntry(
            content=observation,
            timestamp=datetime.now(),
            importance=0.5,  # Simplified
            emotional_tags=[emotional_tag] if emotional_tag else ['neutral'],
            hormonal_state=hormonal_state,
            context={
                'action': action,
                'outcome': outcome,
            }
        )
        
        # Store
        self.episodic_memory.append(memory)
        self.memories_stored += 1
        
        # Update expectations
        # If outcome was positive, expected valence increases
        # (Simplified learning rule)
        self.expected_valence = 0.9 * self.expected_valence + 0.1 * (0.0)  # Neutral
        
        # Reduce uncertainty slightly (learning)
        self.uncertainty = max(0.1, self.uncertainty * 0.99)
        self.last_update = datetime.now()
    
    def get_context(self) -> Dict[str, Any]:
        """Get current context for emotion synthesis"""
        return {
            'memory_count': len(self.episodic_memory),
            'expected_valence': self.expected_valence,
            'uncertainty': self.uncertainty,
        }
    
    def retrieve_relevant(self, query: str, n: int = 3) -> List[MemoryEntry]:
        """Retrieve relevant memories (simplified)"""
        # In full version: semantic similarity search
        # For now: return recent memories
        return self.episodic_memory[-n:] if self.episodic_memory else []
