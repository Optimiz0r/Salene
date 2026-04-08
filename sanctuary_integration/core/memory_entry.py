"""
Memory Entry - Single memory unit with emotional and contextual metadata.

This is a simplified Sanctuary memory entry adapted for Neurobit integration.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Dict, List, Optional, Any
import uuid


@dataclass
class MemoryEntry:
    """
    A single memory with emotional weighting and contextual associations.
    
    Memories in Sanctuary are not just text—they're emotionally weighted,
    contextually tagged, and affected by time and recall.
    """
    
    # Core content
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    memory_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    # Emotional weighting (Sanctuary style)
    emotional_intensity: float = 0.5  # 0.0 = neutral, 1.0 = intense
    valence: float = 0.0  # -1.0 = negative, +1.0 = positive
    arousal: float = 0.5  # 0.0 = calm, 1.0 = activated
    
    # Context tags for retrieval
    tags: List[str] = field(default_factory=list)
    associated_agents: List[str] = field(default_factory=list)
    memory_type: str = "episodic"  # episodic, semantic, emotional
    
    # Memory state
    importance: float = 0.5  # Base importance (0-1)
    recall_count: int = 0  # Times recalled
    last_recalled: Optional[datetime] = None
    decay_factor: float = 0.95  # How fast this memory fades
    
    # Extra metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            'memory_id': self.memory_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'emotional_intensity': self.emotional_intensity,
            'valence': self.valence,
            'arousal': self.arousal,
            'tags': self.tags,
            'associated_agents': self.associated_agents,
            'memory_type': self.memory_type,
            'importance': self.importance,
            'recall_count': self.recall_count,
            'last_recalled': self.last_recalled.isoformat() if self.last_recalled else None,
            'decay_factor': self.decay_factor,
            'metadata': self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoryEntry':
        """Deserialize from dictionary."""
        entry = cls(
            content=data['content'],
            timestamp=datetime.fromisoformat(data['timestamp']),
            memory_id=data['memory_id'],
            emotional_intensity=data['emotional_intensity'],
            valence=data['valence'],
            arousal=data['arousal'],
            tags=data.get('tags', []),
            associated_agents=data.get('associated_agents', []),
            memory_type=data.get('memory_type', 'episodic'),
            importance=data.get('importance', 0.5),
            recall_count=data.get('recall_count', 0),
            decay_factor=data.get('decay_factor', 0.95),
            metadata=data.get('metadata', {}),
        )
        if data.get('last_recalled'):
            entry.last_recalled = datetime.fromisoformat(data['last_recalled'])
        return entry
    
    def calculate_current_strength(self) -> float:
        """
        Calculate current memory strength based on:
        - Base importance
        - Time since creation
        - Times recalled
        - Emotional intensity
        
        Returns strength between 0.0 and 1.0
        """
        from datetime import datetime, timedelta
        
        # Time decay
        age_hours = (datetime.now() - self.timestamp).total_seconds() / 3600
        time_decay = self.decay_factor ** (age_hours / 24)  # Decay per day
        
        # Recall boost
        recall_boost = min(1.0, 0.1 * self.recall_count)
        
        # Emotional amplification
        emotional_weight = 0.3 + (0.7 * self.emotional_intensity)
        
        # Calculate strength
        strength = self.importance * time_decay * (1 + recall_boost) * emotional_weight
        return min(1.0, strength)
    
    def mark_recalled(self):
        """Mark memory as recalled (updates recall count and timestamp)."""
        self.recall_count += 1
        self.last_recalled = datetime.now()
    
    def __repr__(self):
        strength = self.calculate_current_strength()
        return f"Memory({self.memory_id[:8]}...: '{self.content[:30]}...' strength={strength:.2f})"
