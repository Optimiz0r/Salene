"""
Sanctuary-style memory system for Neurobit agents.

This integrates Sanctuary's emotional memory weighting and contextual retrieval
with Neurobit's physiological state.
"""

import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pathlib import Path
import heapq

from .memory_entry import MemoryEntry


class SanctuaryMemoryCore:
    """
    Sanctuary-style memory core with episodic storage and emotional weighting.
    
    Unlike the simple Neurobit memory, this:
    - Weights memories by emotional intensity
    - Supports contextual tagging
    - Implements time-based decay with recovery
    - Maintains memory strength scores
    """
    
    def __init__(
        self,
        agent_id: str,
        storage_path: str = None,
        max_memories: int = 5000,
        decay_rate: float = 0.95
    ):
        """
        Initialize memory core.
        
        Args:
            agent_id: Unique agent identifier
            storage_path: Where to store memories (default: ~/.hermes/sanctuary_memories/{agent_id})
            max_memories: Maximum memories to retain
            decay_rate: How fast memories fade (0-1)
        """
        self.agent_id = agent_id
        
        if storage_path is None:
            self.storage_path = Path.home() / ".hermes" / "sanctuary_memories" / agent_id
        else:
            self.storage_path = Path(storage_path)
        
        self.max_memories = max_memories
        self.decay_rate = decay_rate
        
        # Memory storage
        self.memories: Dict[str, MemoryEntry] = {}
        
        # Context index: tag -> list of memory IDs
        self.tag_index: Dict[str, List[str]] = {}
        
        # Statistics
        self.total_memories_created = 0
        self.total_retrievals = 0
        
        # Ensure storage exists
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing memories
        self._load_memories()
        
        print(f"✨ SanctuaryMemoryCore initialized")
        print(f"   Agent: {agent_id}")
        print(f"   Loaded: {len(self.memories)} memories")
    
    def encode_memory(
        self,
        content: str,
        emotional_intensity: float = 0.5,
        valence: float = 0.0,
        arousal: float = 0.5,
        tags: List[str] = None,
        memory_type: str = "episodic",
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> MemoryEntry:
        """
        Create and store a new memory.
        
        Args:
            content: The memory content
            emotional_intensity: How emotional (0-1)
            valence: Positive/negative (-1 to +1)
            arousal: Activation level (0-1)
            tags: Contextual tags
            memory_type: episodic, semantic, or emotional
            importance: Base importance (0-1)
            metadata: Extra data
            
        Returns:
            The created MemoryEntry
        """
        entry = MemoryEntry(
            content=content,
            emotional_intensity=emotional_intensity,
            valence=valence,
            arousal=arousal,
            tags=tags or [],
            memory_type=memory_type,
            importance=importance,
            metadata=metadata or {}
        )
        
        # Store
        self.memories[entry.memory_id] = entry
        self.total_memories_created += 1
        
        # Index by tags
        for tag in entry.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = []
            self.tag_index[tag].append(entry.memory_id)
        
        # Check capacity
        if len(self.memories) > self.max_memories:
            self._prune_memories()
        
        # Auto-save every 10 memories
        if self.total_memories_created % 10 == 0:
            self._save_memories()
        
        return entry
    
    def retrieve_by_context(
        self,
        tags: List[str],
        limit: int = 5,
        min_strength: float = 0.1
    ) -> List[MemoryEntry]:
        """
        Retrieve memories matching context tags.
        
        Returns memories sorted by current strength (emotional + time + importance).
        """
        candidate_ids = set()
        
        # Find memories matching any tag
        for tag in tags:
            if tag in self.tag_index:
                candidate_ids.update(self.tag_index[tag])
        
        # Score by current strength
        scored_memories = []
        for memory_id in candidate_ids:
            entry = self.memories[memory_id]
            strength = entry.calculate_current_strength()
            if strength >= min_strength:
                scored_memories.append((strength, entry))
                entry.mark_recalled()
        
        # Sort by strength (highest first)
        scored_memories.sort(reverse=True)
        
        self.total_retrievals += 1
        
        return [entry for strength, entry in scored_memories[:limit]]
    
    def retrieve_by_emotion(
        self,
        target_valence: float = None,
        target_arousal: float = None,
        valence_tolerance: float = 0.3,
        arousal_tolerance: float = 0.3,
        limit: int = 5
    ) -> List[MemoryEntry]:
        """
        Retrieve memories matching emotional profile.
        
        Useful for: "memories similar to how I feel now"
        """
        scored_memories = []
        
        for entry in self.memories.values():
            # Calculate emotional distance
            valence_dist = abs(entry.valence - target_valence) if target_valence is not None else 0
            arousal_dist = abs(entry.arousal - target_arousal) if target_arousal is not None else 0
            
            # Check within tolerance
            if valence_dist <= valence_tolerance and arousal_dist <= arousal_tolerance:
                # Score by strength and emotional match
                strength = entry.calculate_current_strength()
                match_score = 1.0 - (valence_dist + arousal_dist) / 2
                final_score = strength * match_score
                scored_memories.append((final_score, entry))
        
        # Sort by score
        scored_memories.sort(reverse=True)
        
        return [entry for score, entry in scored_memories[:limit]]
    
    def retrieve_strongest(self, limit: int = 5) -> List[MemoryEntry]:
        """Get strongest memories regardless of context."""
        scored = [(entry.calculate_current_strength(), entry) 
                  for entry in self.memories.values()]
        scored.sort(reverse=True)
        
        return [entry for strength, entry in scored[:limit]]
    
    def consolidate_memories(self) -> str:
        """
        Consolidate memories into a narrative summary.
        
        Returns a summary of dominant emotional themes.
        """
        if not self.memories:
            return "No memories yet."
        
        # Calculate total valence and arousal
        total_valence = sum(m.valence * m.emotional_intensity for m in self.memories.values())
        total_arousal = sum(m.arousal * m.emotional_intensity for m in self.memories.values())
        
        num_memories = len(self.memories)
        avg_valence = total_valence / num_memories
        avg_arousal = total_arousal / num_memories
        
        # Determine emotional quadrant
        if avg_valence >= 0 and avg_arousal >= 0.5:
            quadrant = "positive engagement"
        elif avg_valence >= 0:
            quadrant = "contentment"
        elif avg_arousal >= 0.5:
            quadrant = "stress"
        else:
            quadrant = "withdrawal"
        
        # Strongest memories
        strongest = self.retrieve_strongest(limit=3)
        
        summary = f"{num_memories} memories, dominant tone: {quadrant}\n"
        summary += f"Strongest memories:\n"
        for mem in strongest:
            summary += f"  - {mem.content[:50]}... (strength {mem.calculate_current_strength():.2f})\n"
        
        return summary
    
    def _prune_memories(self):
        """Remove weakest memories if over capacity."""
        if len(self.memories) <= self.max_memories:
            return
        
        # Score all memories
        scored = [(entry.calculate_current_strength(), memory_id) 
                  for memory_id, entry in self.memories.items()]
        scored.sort()
        
        # Remove bottom 10%
        to_remove = int(len(scored) * 0.1)
        for strength, memory_id in scored[:to_remove]:
            del self.memories[memory_id]
        
        # Rebuild tag index
        self._rebuild_tag_index()
        print(f"🗑️ Pruned {to_remove} weak memories")
    
    def _rebuild_tag_index(self):
        """Rebuild tag index after pruning."""
        self.tag_index = {}
        for entry in self.memories.values():
            for tag in entry.tags:
                if tag not in self.tag_index:
                    self.tag_index[tag] = []
                self.tag_index[tag].append(entry.memory_id)
    
    def _save_memories(self):
        """Persist memories to disk."""
        data = {
            'agent_id': self.agent_id,
            'saved_at': datetime.now().isoformat(),
            'total_memories_created': self.total_memories_created,
            'memories': {mid: entry.to_dict() for mid, entry in self.memories.items()}
        }
        
        filepath = self.storage_path / "memories.json"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _load_memories(self):
        """Load memories from disk."""
        filepath = self.storage_path / "memories.json"
        
        if not filepath.exists():
            return
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            for memory_id, mem_data in data.get('memories', {}).items():
                entry = MemoryEntry.from_dict(mem_data)
                self.memories[memory_id] = entry
                
                # Index tags
                for tag in entry.tags:
                    if tag not in self.tag_index:
                        self.tag_index[tag] = []
                    self.tag_index[tag].append(memory_id)
            
            self.total_memories_created = data.get('total_memories_created', len(self.memories))
            print(f"📂 Loaded {len(self.memories)} memories from disk")
            
        except Exception as e:
            print(f"⚠️ Error loading memories: {e}")
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get statistics about memory system."""
        return {
            'total_memories': len(self.memories),
            'total_created': self.total_memories_created,
            'total_retrievals': self.total_retrievals,
            'storage_path': str(self.storage_path),
            'memory_types': self._count_memory_types(),
        }
    
    def _count_memory_types(self) -> Dict[str, int]:
        """Count memories by type."""
        counts = {}
        for entry in self.memories.values():
            counts[entry.memory_type] = counts.get(entry.memory_type, 0) + 1
        return counts
