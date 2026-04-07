"""
NeurobitAgent - Integrates Hermes with Neurobit physiological cognition.

This agent maintains hormonal state that modulates tool selection and responses.
Uses Hermes for MCP tool orchestration while running Neurobit's decision loop.
"""

import asyncio
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass
import sys
import os

# Add paths for imports
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

# Import Neurobit state directly from file to avoid module name collision
import importlib.util
spec = importlib.util.spec_from_file_location(
    "neurobit_unified_state", 
    "/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem/core/unified_state.py"
)
neurobit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neurobit_module)

UnifiedState = neurobit_module.UnifiedState
PhysiologicalState = neurobit_module.PhysiologicalState

# Hermes imports
from model_tools import get_tool_definitions


@dataclass
class HormoneConfig:
    """Configuration for hormone-based decision modulation"""
    high_stress_tool_limit: int = 3
    low_dopamine_exploration: float = 0.3
    high_dopamine_repetition: float = 0.7
    verbosity_by_serenity: float = 0.5
    urgency_by_adrenaline: float = 0.8
    memory_by_oxytocin: float = 0.6


class NeurobitAgent:
    """
    Agent using Neurobit's physiological model for cognition.
    
    Hermes provides:
    - MCP tool orchestration
    - Session persistence
    - Platform integration
    
    Neurobit provides:
    - Physiological/hormonal state
    - Hormone-modulated decisions
    """
    
    def __init__(
        self,
        state=None,
        hormone_config=None,
        enabled_toolsets=None,
        disabled_toolsets=None,
        session_id=None,
        platform="cli",
        mcp_servers=None,
    ):
        # Core state
        self.state = state or UnifiedState()
        self.hormone_config = hormone_config or HormoneConfig()
        self.session_id = session_id or str(uuid.uuid4())
        self.platform = platform
        
        # Tool discovery via Hermes
        try:
            self.tools = get_tool_definitions(
                enabled_toolsets=enabled_toolsets,
                disabled_toolsets=disabled_toolsets,
                quiet_mode=False,
            )
        except Exception as e:
            print(f"Note: Could not load Hermes tools: {e}")
            self.tools = []
        
        if mcp_servers:
            self._register_mcp_servers(mcp_servers)
        
        # Conversation
        self.messages = []
        self._iteration_count = 0
        
        print(f"[Neurobit] Agent initialized")
        print(f"[Neurobit] Session: {self.session_id}")
        print(f"[Neurobit] Initial hormone state:")
        self._log_hormone_state()
    
    def _register_mcp_servers(self, mcp_servers: dict) -> None:
        print(f"[Neurobit] Registering {len(mcp_servers)} MCP servers")
        for name, config in mcp_servers.items():
            print(f"  - {name}: {config.get('command', 'docker')}")
    
    def process_perception(self, user_input: str) -> dict:
        """Process input with hormonal awareness"""
        perception = {
            "timestamp": datetime.now().isoformat(),
            "raw_input": user_input,
            "hormone_vector": self.state.physiology.hormone_vector.tolist(),
            "affective_state": {
                "quadrant": self.state.affect.quadrant_label,
                "valence": float(self.state.affect.valence),
                "arousal": float(self.state.affect.arousal),
            },
            "drives": {
                "connect": float(self.state.persona.drives.connection),
                "novelty": float(self.state.persona.drives.novelty),
                "control": float(self.state.persona.drives.control),
                "safety": float(self.state.persona.drives.safety),
            }
        }
        
        # Update physiology
        self._update_physiology_from_input(user_input)
        
        return perception
    
    def _update_physiology_from_input(self, user_input: str) -> None:
        """Update state based on input"""
        phys = self.state.physiology
        
        urgency_markers = ["urgent", "quick", "asap", "now", "hurry", "emergency"]
        if any(marker in user_input.lower() for marker in urgency_markers):
            phys.cpu_percent = min(phys.cpu_percent + 0.2, 1.0)
            phys.temperature = min(phys.temperature + 5, 95)
        
        if phys.cpu_percent > 0.5:
            phys.memory_percent = min(phys.memory_percent + 0.1, 1.0)
    
    def decide_action(self, perception: dict) -> dict:
        """Hormone-modulated decision making"""
        hormones = self.state.physiology.hormone_vector
        cortisol = hormones[3]  # Stress
        dopamine = hormones[0]  # Reward
        adrenaline = hormones[4]  # Urgency
        
        decision = {
            "action": None,
            "reasoning": ""
        }
        
        if cortisol > 0.7:
            decision["action"] = {"type": "respond", "tools": False}
            decision["reasoning"] = "High cortisol (stress) - limiting tool calls"
        elif adrenaline > 0.6:
            decision["action"] = {"type": "act", "urgent": True}
            decision["reasoning"] = "High adrenaline - prioritizing action"
        else:
            decision["action"] = {"type": "think", "tools": True}
            decision["reasoning"] = "Normal arousal - standard reasoning"
        
        return decision
    
    def execute_action(self, decision: dict) -> str:
        """Execute action, generate hormone-conditioned response"""
        hormones = self.state.physiology.hormone_vector
        cortisol, dopamine, serotonin = hormones[3], hormones[0], hormones[1]
        
        response = f"[State: C:{cortisol:.2f} D:{dopamine:.2f} S:{serotonin:.2f}]\n\n"
        
        if cortisol > 0.7:
            response += "I'm feeling pressured. "
        elif dopamine > 0.7:
            response += "I'm engaged! "
        elif serotonin > 0.8:
            response += "Feeling calm. "
        
        response += f"\nDecision: {decision['reasoning']}"
        return response
    
    def run_conversation(self, user_message: str) -> dict:
        """Main conversation loop with physiological cognition"""
        print(f"\n[Neurobit] Processing: '{user_message[:50]}...'")
        
        perception = self.process_perception(user_message)
        decision = self.decide_action(perception)
        response = self.execute_action(decision)
        
        self.messages.append({"role": "user", "content": user_message})
        self.messages.append({"role": "assistant", "content": response})
        self._iteration_count += 1
        
        print(f"[Neurobit] Response complete")
        self._log_hormone_state()
        
        return {
            "response": response,
            "state_snapshot": {
                "hormones": self.state.physiology.hormone_vector.tolist(),
                "quadrant": self.state.affect.quadrant_label,
            },
            "messages": list(self.messages)
        }
    
    def _log_hormone_state(self) -> None:
        """Log hormone levels"""
        hormones = self.state.physiology.hormone_vector
        names = ["dopamine", "serotonin", "norepinephrine", "cortisol",
                "adrenaline", "melatonin", "oxytocin", "endorphins"]
        for name, value in zip(names, hormones):
            print(f"  {name}: {value:.2f}")
    
    def chat(self, message: str) -> str:
        """Simple interface"""
        return self.run_conversation(message)["response"]
    
    def get_state_summary(self) -> dict:
        """Export current state"""
        return {
            "physiological": {
                "cpu_percent": self.state.physiology.cpu_percent,
                "memory_percent": self.state.physiology.memory_percent,
                "temperature": self.state.physiology.temperature,
                "hormone_vector": self.state.physiology.hormone_vector.tolist(),
            },
            "affective": {
                "quadrant": self.state.affect.quadrant_label,
                "valence": float(self.state.affect.valence),
                "arousal": float(self.state.affect.arousal),
            },
            "drives": {
                "connect": float(self.state.persona.drives.connection),
                "novelty": float(self.state.persona.drives.novelty),
                "control": float(self.state.persona.drives.control),
                "safety": float(self.state.persona.drives.safety),
            }
        }
