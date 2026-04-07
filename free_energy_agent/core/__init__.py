"""Free Energy Agent - Physiologically-Grounded Cognitive Architecture

Core module providing the foundation for an agent that:
- Minimizes prediction error (FEP)
- Has felt sense (28 emotions derived from 8 hormones)
- Acts through tools (Hermes integration)
- Maintains continuous operation (not turn-based)

Architecture:
    Neurobit Foundation (FEP)
    ├── PhysiologicalState (8 hormones, homeostasis)
    ├── AffectiveState (FEP ring point: belief μ, salience w, confidence c)
    └── DriveState (homeostatic deficits)
    
    Sanctuary Richness (Emergent)
    └── Emotions (28 derived states from physiology × affect × context)
    
    Processing (Active Inference)
    └── 10-phase pipeline minimizing expected free energy
    
    Action (Real World)
    └── Hermes tool execution
"""

from .free_energy_agent import FreeEnergyAgent
from .processing_loop import ProcessingLoop
from .processing_context import ProcessingContext
from .generative_model import GenerativeModel

__all__ = [
    "FreeEnergyAgent",
    "ProcessingLoop", 
    "ProcessingContext",
    "GenerativeModel",
]