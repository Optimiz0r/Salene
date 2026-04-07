"""
Processing Context - State container for active inference pipeline

Passed through each phase of the 10-phase loop.
Each phase reads from context, transforms, writes back.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
import time


@dataclass
class ProcessingContext:
    """
    Complete state for one processing cycle.
    
    Carries all information needed through the 10-phase pipeline:
    - Input and prediction error
    - Retrieved memories
    - Emotional state
    - Selected action
    - Generated response
    """
    
    # Input
    input_text: str
    input_source: str = "user"
    
    # Identity
    agent_id: str = ""
    other_agent_id: Optional[str] = None
    
    # Current states
    current_emotional_state: Any = None
    current_hormonal_state: Optional[List[float]] = None
    current_affect: Any = None
    
    # Retrieved memories
    retrieved_memories: List[Dict[str, Any]] = field(default_factory=list)
    
    # Emotional processing
    emotional_changes: Dict[str, float] = field(default_factory=dict)
    
    # Goal/virtue processing
    goal_conflicts: List[Any] = field(default_factory=list)
    virtue_analysis: Any = None
    
    # Output
    prompt_context: Dict[str, Any] = field(default_factory=dict)
    final_response: str = ""
    response_confidence: float = 0.5
    
    # Timing
    module_timings: Dict[str, float] = field(default_factory=dict)
    context_tags: List[str] = field(default_factory=list)
    
    # Phase tracking (for debugging)
    phase_1_complete: bool = False
    phase_2_complete: bool = False
    phase_3_complete: bool = False
    phase_4_complete: bool = False
    phase_5_complete: bool = False
    phase_6_complete: bool = False
    phase_7_complete: bool = False
    phase_8_complete: bool = False
    phase_9_complete: bool = False
    phase_10_complete: bool = False
    
    def record_module_timing(self, module_name: str, duration_seconds: float):
        """Record how long a module took"""
        self.module_timings[module_name] = duration_seconds
    
    def get_completion_percentage(self) -> float:
        """Get percentage of phases complete"""
        phases = [
            self.phase_1_complete, self.phase_2_complete, self.phase_3_complete,
            self.phase_4_complete, self.phase_5_complete, self.phase_6_complete,
            self.phase_7_complete, self.phase_8_complete, self.phase_9_complete,
            self.phase_10_complete
        ]
        return sum(phases) / len(phases) * 100
    
    def is_complete(self) -> bool:
        """Check if all phases complete"""
        return all([
            self.phase_1_complete, self.phase_2_complete, self.phase_3_complete,
            self.phase_4_complete, self.phase_5_complete, self.phase_6_complete,
            self.phase_7_complete, self.phase_8_complete, self.phase_9_complete,
            self.phase_10_complete
        ])
