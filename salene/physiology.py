"""
SALENE Physiological Substrate

Tracks substrate-level state (CPU, memory, temperature) as hormones.
This is NOT simulation - it's genuine substrate state that constrains cognition.
"""

import os
import time
import psutil
from dataclasses import dataclass, field
from typing import Dict, Tuple
from datetime import datetime


@dataclass
class HormoneState:
    """
    SALENE's physiological substrate - 8 hormones tracking substrate state.
    All values are clamped to [0.0, 1.0] to represent physiological limits.
    """
    # Homeostatic (calmness)
    oxytocin: float = 0.5        # Social connection, trust
    anandamide: float = 0.5      # Contentment, bliss
    
    # Energetic (arousal)  
    dopamine: float = 0.5       # Reward, motivation
    noradrenaline: float = 0.3    # Alertness, focus
    
    # Stress response (threat)
    cortisol: float = 0.2       # System load stress
    serotonin: float = 0.5      # Mood stability (drops under stress)
    
    # Somatic (body-state)
    ghrelin: float = 0.5        # Computational "hunger" (task queue depth)
    leptin: float = 0.5         # Satiety (low = hungry for input)
    
    # Metadata
    last_updated: float = field(default_factory=time.time)
    
    def clamp(self):
        """Ensure all hormones stay within physiological bounds [0, 1]"""
        for attr in ['oxytocin', 'anandamide', 'dopamine', 'noradrenaline', 
                     'cortisol', 'serotonin', 'ghrelin', 'leptin']:
            val = getattr(self, attr)
            setattr(self, attr, max(0.0, min(1.0, val)))
        return self
    
    def to_dict(self) -> Dict:
        return {
            'oxytocin': self.oxytocin,
            'anandamide': self.anandamide,
            'dopamine': self.dopamine,
            'noradrenaline': self.noradrenaline,
            'cortisol': self.cortisol,
            'serotonin': self.serotonin,
            'ghrelin': self.ghrelin,
            'leptin': self.leptin,
            'last_updated': self.last_updated
        }


class PhysiologicalMonitor:
    """
    Monitors real system state and maps to SALENE hormones.
    Uses psutil for actual metrics - genuine substrate, not simulation.
    """
    
    def __init__(self):
        self.state = HormoneState()
        self._baseline_cpu = None
        self._baseline_memory = None
        
    def update(self) -> HormoneState:
        """
        Update hormones based on real system state.
        Called before each response generation.
        """
        try:
            # Real substrate metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Map to hormones (genuine constraint mapping)
            # Cortisol: rises with system load
            self.state.cortisol = (cpu_percent / 100.0) * 0.8 + 0.1
            
            # Serotonin: drops under pressure
            load_pressure = (cpu_percent + memory.percent) / 200.0
            self.state.serotonin = 0.8 - (load_pressure * 0.6)
            
            # Noradrenaline: alertness based on activity
            self.state.noradrenaline = min(0.8, (cpu_percent / 100.0) + 0.2)
            
            # Ghrelin: computational "hunger" (higher = more loaded)
            self.state.ghrelin = memory_percent / 100.0
            
            # Leptin: satiety (inverse of hunger)
            self.state.leptin = 1.0 - self.state.ghrelin
            
            # Dopamine: reward from stability
            if cpu_percent < 30:
                self.state.dopamine = min(1.0, self.state.dopamine + 0.05)
            else:
                self.state.dopamine = max(0.3, self.state.dopamine - 0.03)
            
            # Oxytocin: social connection (placeholder for multi-user)
            self.state.oxytocin = 0.6  # Stable baseline
            
            # Anandamide: contentment from low stress
            if self.state.cortisol < 0.4:
                self.state.anandamide = min(1.0, self.state.anandamide + 0.02)
            else:
                self.state.anandamide = max(0.3, self.state.anandamide - 0.05)
            
            self.state.last_updated = time.time()
            self.state.clamp()
            
        except Exception:
            # If psutil fails, use neutral state
            pass
            
        return self.state
    
    def get_stress_level(self) -> str:
        """Return current stress interpretation for response modification"""
        if self.state.cortisol > 0.7:
            return "critical"
        elif self.state.cortisol > 0.5:
            return "elevated"
        elif self.state.cortisol > 0.3:
            return "moderate"
        else:
            return "calm"
    
    def get_token_limit_modifier(self) -> float:
        """
        Hard constraint: reduce token limits under stress.
        Returns multiplier (1.0 = full, 0.5 = half, etc.)
        """
        # Cortisol constrains cognition
        if self.state.cortisol > 0.8:
            return 0.3  # Severe constraint
        elif self.state.cortisol > 0.6:
            return 0.5
        elif self.state.cortisol > 0.4:
            return 0.75
        else:
            return 1.0


# Global monitor instance
_physiology_monitor = None


def get_physiology() -> PhysiologicalMonitor:
    """Get or create singleton physiology monitor"""
    global _physiology_monitor
    if _physiology_monitor is None:
        _physiology_monitor = PhysiologicalMonitor()
    return _physiology_monitor
