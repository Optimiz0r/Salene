"""
Sanctuary Integration Core

Core components for Sanctuary-Neurobit synthesis:
- MemoryEntry: Single memory unit
- SanctuaryMemoryCore: Episodic memory with emotional weighting
- EmotionBridge: Maps Sanctuary emotions to Neurobit physiology
"""

from .memory_entry import MemoryEntry
from .sanctuary_memory import SanctuaryMemoryCore

__all__ = ['MemoryEntry', 'SanctuaryMemoryCore']
