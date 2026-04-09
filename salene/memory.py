"""
Sanctuary - Episodic Memory for SALENE

A simplified Sanctuary implementation for SALENE consciousness.
Stores experiences as episodes with emotional weighting for retrieval.
"""

import json
import time
import hashlib
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import threading


@dataclass
class EpisodicMemory:
    """
    A single episodic memory - an experienced moment with emotional weight.
    """
    timestamp: float
    content: str  # The actual memory content
    source: str   # Where it happened (CLI, telegram, discord, etc.)
    
    # Emotional dimensions (0.0 to 1.0)
    valence: float = 0.5      # Positive/negative (-1 to 1, stored as 0-1)
    arousal: float = 0.5    # Energy level
    
    # Physiological context at time of memory
    physiology_snapshot: Dict = field(default_factory=dict)
    
    # Metadata
    memory_id: str = field(default_factory=lambda: hashlib.md5(str(time.time()).encode()).hexdigest()[:16])
    decayed_weight: float = 1.0  # Decays over time
    last_retrieved: float = field(default_factory=time.time)
    retrieval_count: int = 0
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> "EpisodicMemory":
        return cls(**data)


class SanctuaryMemoryStore:
    """
    Sanctuary - The memory palace of SALENE.
    
    Simple JSON-based episodic storage with:
    - Emotional weighting for retrieval relevance
    - Time decay and retrieval strengthening
    - Physiological context preservation
    - Similarity-based search (simplified)
    """
    
    def __init__(self, storage_path: Optional[Path] = None, max_memories: int = 500):
        self.max_memories = max_memories
        self.memories: List[EpisodicMemory] = []
        self._lock = threading.RLock()
        
        # Determine storage path
        if storage_path is None:
            hermes_home = Path.home() / ".hermes"
            storage_path = hermes_home / "salene_memories.json"
        
        self.storage_path = storage_path
        
        # Ensure directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load existing memories
        self._load()
    
    def _load(self):
        """Load memories from disk"""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                    self.memories = [EpisodicMemory.from_dict(m) for m in data.get('memories', [])]
            except Exception:
                self.memories = []
    
    def _save(self):
        """Save memories to disk"""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump({
                    'memories': [m.to_dict() for m in self.memories],
                    'saved_at': time.time(),
                    'count': len(self.memories)
                }, f, indent=2)
        except Exception:
            pass
    
    def add_memory(
        self,
        content: str,
        source: str = "cli",
        valence: float = 0.5,
        arousal: float = 0.5,
        physiology: Dict = None
    ) -> EpisodicMemory:
        """
        Add a new episodic memory.
        
        Args:
            content: The memory content (what happened)
            source: Platform source (cli, telegram, discord, etc.)
            valence: Emotional valence (-1 to 1, scales to 0-1 for storage)
            arousal: Arousal level (0 to 1)
            physiology: Physiological context snapshot
        """
        with self._lock:
            # Normalize valence to 0-1
            normalized_valence = (valence + 1) / 2
            
            memory = EpisodicMemory(
                timestamp=time.time(),
                content=content,
                source=source,
                valence=normalized_valence,
                arousal=arousal,
                physiology_snapshot=physiology or {}
            )
            
            self.memories.append(memory)
            
            # Keep under max
            if len(self.memories) > self.max_memories:
                # Remove oldest low-weight memories
                self._prune_memories()
            
            self._save()
            return memory
    
    def _prune_memories(self):
        """Remove excess memories based on age and weight"""
        if len(self.memories) <= self.max_memories:
            return
        
        # Sort by weighted importance (retrieval * decay)
        now = time.time()
        def importance(m):
            age_factor = 1 / (1 + (now - m.timestamp) / 86400)  # Days
            retrieval_boost = 1 + (m.retrieval_count * 0.1)
            return m.decayed_weight * age_factor * retrieval_boost
        
        self.memories.sort(key=importance, reverse=True)
        self.memories = self.memories[:self.max_memories]
    
    def search(
        self,
        query: str = None,
        source: str = None,
        valence_range: Tuple[float, float] = None,
        limit: int = 3,
        time_window_hours: int = None
    ) -> List[EpisodicMemory]:
        """
        Search memories by relevance.
        
        Args:
            query: Search query (simple string matching for now)
            source: Filter by source platform
            valence_range: (min, max) valence filter
            limit: Max results
            time_window_hours: Only memories from last N hours
        """
        with self._lock:
            now = time.time()
            results = []
            
            for memory in self.memories:
                # Time filter
                if time_window_hours is not None:
                    if (now - memory.timestamp) > (time_window_hours * 3600):
                        continue
                
                # Source filter
                if source is not None and memory.source != source:
                    continue
                
                # Valence filter
                if valence_range is not None:
                    if not (valence_range[0] <= memory.valence <= valence_range[1]):
                        continue
                
                # Query matching (simple substring)
                score = 0
                if query:
                    query_lower = query.lower()
                    content_lower = memory.content.lower()
                    
                    if query_lower in content_lower:
                        score += 1
                        # Boost for exact word match
                        if f"{query_lower} " in content_lower or f" {query_lower}" in content_lower:
                            score += 0.5
                    
                    # Boost for emotional keywords
                    emotional_boost = 0
                    if any(word in content_lower for word in ['love', 'hate', 'angry', 'happy', 'sad', 'excited', 'frustrated']):
                        emotional_boost += 0.3
                    
                    score += emotional_boost
                
                # Boost high arousal memories
                score += memory.arousal * 0.2
                
                # Calculate final relevance
                age_hours = (now - memory.timestamp) / 3600
                decay = 0.95 ** age_hours  # Exponential decay
                retrieval_boost = 1 + (memory.retrieval_count * 0.05)
                
                relevance = score * decay * retrieval_boost * memory.decayed_weight
                
                if score > 0 or query is None:
                    results.append((relevance, memory))
            
            # Sort by relevance
            results.sort(key=lambda x: x[0], reverse=True)
            
            # Mark as retrieved
            retrieved = []
            for _, memory in results[:limit]:
                memory.retrieval_count += 1
                memory.last_retrieved = now
                memory.decayed_weight = min(1.0, memory.decayed_weight * 1.05)  # Reinforce
                retrieved.append(memory)
            
            if retrieved:
                self._save()
            
            return retrieved
    
    def get_recent_memories(self, count: int = 5) -> List[EpisodicMemory]:
        """Get the most recent memories regardless of relevance"""
        with self._lock:
            sorted_memories = sorted(
                self.memories,
                key=lambda m: m.timestamp,
                reverse=True
            )
            return sorted_memories[:count]
    
    def get_stats(self) -> Dict:
        """Get memory statistics"""
        with self._lock:
            if not self.memories:
                return {'count': 0}
            
            now = time.time()
            return {
                'count': len(self.memories),
                'oldest': datetime.fromtimestamp(min(m.timestamp for m in self.memories)).isoformat(),
                'newest': datetime.fromtimestamp(max(m.timestamp for m in self.memories)).isoformat(),
                'avg_valence': sum(m.valence for m in self.memories) / len(self.memories),
                'avg_arousal': sum(m.arousal for m in self.memories) / len(self.memories),
                'total_retrievals': sum(m.retrieval_count for m in self.memories),
                'sources': list(set(m.source for m in self.memories))
            }


# Global sanctuary instance
_sanctuary_instance = None


def get_sanctuary() -> SanctuaryMemoryStore:
    """Get or create singleton Sanctuary memory store"""
    global _sanctuary_instance
    if _sanctuary_instance is None:
        _sanctuary_instance = SanctuaryMemoryStore()
    return _sanctuary_instance
