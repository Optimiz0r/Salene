"""
Integrated Neurobit-Hermes Agent with Ollama/OpenRouter Support

This is the complete integration that wraps Hermes' AIAgent with
Neurobit's physiological cognition layer.
"""

import sys
import os
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import importlib.util

# Add paths
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

# Import Hermes AIAgent
from run_agent import AIAgent
from model_tools import get_tool_definitions, handle_function_call

# Import Neurobit state
spec = importlib.util.spec_from_file_location(
    "neurobit_unified_state",
    "/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem/core/unified_state.py"
)
neurobit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(neurobit_module)
UnifiedState = neurobit_module.UnifiedState
PhysiologicalState = neurobit_module.PhysiologicalState


@dataclass
class HormoneConfig:
    """Hormone modulation parameters"""
    high_cortisol_tool_limit: int = 3
    high_adrenaline_skip_thinking: bool = True
    dopamine_repeat_threshold: float = 0.7
    verbosity_by_serenity: float = 0.5
    urgency_by_adrenaline: float = 0.8
    creativity_by_dopamine: float = 0.5
    novelty_seeking: float = 0.3
    connection_seeking: float = 0.6


@dataclass
class ModelConfig:
    """Configuration for remote models"""
    ollama_url: str = "http://localhost:11434/v1"
    ollama_model: str = "llama3.2"
    ollama_api_key: str = "ollama"
    openrouter_url: str = "https://openrouter.ai/api/v1"
    openrouter_key: str = field(default_factory=lambda: os.getenv("OPENROUTER_API_KEY", ""))
    kimi_model: str = "moonshotai/kimi-k2.5"
    prefer_local: bool = True
    enable_fallback: bool = True


class IntegratedNeurobitAgent:
    """
    Complete Neurobit + Hermes integration with physiological cognition.
    """

    def __init__(
        self,
        neurobit_state: Optional[Any] = None,
        hormone_config: Optional[HormoneConfig] = None,
        model: str = "ollama/llama3.2",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        provider: Optional[str] = None,
        enabled_toolsets: Optional[List[str]] = None,
        disabled_toolsets: Optional[List[str]] = None,
        max_iterations: int = 90,
        platform: str = "cli",
        model_config: Optional[ModelConfig] = None,
        session_id: Optional[str] = None,
        quiet_mode: bool = False,
    ):
        self.hormone_config = hormone_config or HormoneConfig()
        self.model_config = model_config or ModelConfig()
        self.session_id = session_id or str(uuid.uuid4())

        resolved_model, resolved_base_url, resolved_key, resolved_provider =             self._resolve_model_config(model, base_url, api_key, provider)

        if not quiet_mode:
            print(f"🧠 Integrated Neurobit-Hermes Agent")
            print(f"   Model: {resolved_model}")
            print(f"   Base URL: {resolved_base_url or 'default'}")
            print(f"   Session: {self.session_id}")

        self.hermes_agent = AIAgent(
            model=resolved_model,
            base_url=resolved_base_url,
            api_key=resolved_key,
            provider=resolved_provider,
            enabled_toolsets=enabled_toolsets,
            disabled_toolsets=disabled_toolsets,
            max_iterations=max_iterations,
            platform=platform,
            session_id=self.session_id,
            quiet_mode=quiet_mode,
        )

        self.state = neurobit_state or UnifiedState()
        self.messages: List[Dict[str, Any]] = []
        self.tool_success_history: Dict[str, float] = {}

        if not quiet_mode:
            print(f"\n[Neurobit] Initial hormone state:")
            self._log_hormone_state()

    def _resolve_model_config(self, model: str, base_url: Optional[str],
                            api_key: Optional[str], provider: Optional[str]) -> tuple:
        """Resolve model configuration based on input"""
        cfg = self.model_config

        if model.startswith("ollama/"):
            actual_model = model.replace("ollama/", "")
            return (
                actual_model,
                base_url or cfg.ollama_url,
                api_key or cfg.ollama_api_key,
                provider or "ollama"
            )

        if "kimi" in model.lower() or "moonshot" in model.lower():
            return (
                cfg.kimi_model,
                cfg.openrouter_url,
                cfg.openrouter_key,
                provider or "openrouter"
            )

        return (
            model or cfg.ollama_model,
            base_url or cfg.ollama_url,
            api_key or cfg.ollama_api_key,
            provider or "ollama"
        )

    def _log_hormone_state(self) -> None:
        phys = self.state.physiology
        names = ["dopamine", "serotonin", "norepinephrine", "cortisol",
                "adrenaline", "melatonin", "oxytocin", "endorphins"]
        for name, value in zip(names, phys.hormone_vector):
            print(f"  {name}: {value:.2f}")

    def process_perception(self, user_input: str) -> Dict[str, Any]:
        phys = self.state.physiology

        urgency_markers = ["urgent", "emergency", "asap", "now", "hurry", "quick"]
        was_urgent = any(m in user_input.lower() for m in urgency_markers)

        if was_urgent:
            phys.cpu_percent = min(phys.cpu_percent + 0.2, 1.0)
            phys.temperature = min(phys.temperature + 5, 95.0)
        else:
            phys.cpu_percent = max(phys.cpu_percent * 0.9, 0.0)
            phys.temperature = max(phys.temperature * 0.95, 25.0)

        perception = {
            "timestamp": datetime.now().isoformat(),
            "raw_input": user_input,
            "hormones": phys.hormone_vector.tolist(),
            "urgency_detected": was_urgent,
            "affective": {
                "quadrant": self.state.affect.quadrant_label,
                "valence": float(self.state.affect.valence),
                "arousal": float(self.state.affect.arousal),
            },
            "drives": {
                "connection": self.state.persona.drives.connection,
                "novelty": self.state.persona.drives.novelty,
                "control": self.state.persona.drives.control,
                "safety": self.state.persona.drives.safety,
            }
        }

        return perception

    def decide_action(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        hormones = perception["hormones"]
        cortisol = hormones[3]
        dopamine = hormones[0]
        adrenaline = hormones[4]

        decision = {
            "action_type": "think",
            "max_tools": self.hermes_agent.max_iterations,
            "reasoning": "",
            "hormone_state": {
                "cortisol": cortisol,
                "dopamine": dopamine,
                "adrenaline": adrenaline,
            }
        }

        if cortisol > 0.7:
            decision["action_type"] = "respond"
            decision["max_tools"] = 0
            decision["reasoning"] = f"High cortisol ({cortisol:.2f}) - limiting cognitive load"
        elif adrenaline > 0.6:
            decision["action_type"] = "act"
            decision["max_tools"] = min(5, decision["max_tools"])
            decision["reasoning"] = f"High adrenaline ({adrenaline:.2f}) - expedited action"
        else:
            decision["action_type"] = "use_tools"
            decision["reasoning"] = "Normal arousal - full tool capability"

        return decision

    def execute_action(self, user_message: str, decision: Dict[str, Any],
                      perception: Dict[str, Any]) -> str:
        action_type = decision["action_type"]

        if action_type == "respond":
            return self._generate_hormone_conditioned_response(user_message, decision)

        elif action_type in ("act", "use_tools"):
            return self._execute_with_hermes(user_message, decision, perception)

        return self._generate_hormone_conditioned_response(user_message, decision)

    def _execute_with_hermes(self, user_message: str, decision: Dict[str, Any],
                             perception: Dict[str, Any]) -> str:
        hormone_info = f"""
[NEUROBIT PHYSIOLOGICAL STATE]
Current hormone levels:
- Cortisol (stress): {perception['hormones'][3]:.2f}
- Dopamine (reward): {perception['hormones'][0]:.2f}
- Adrenaline (urgency): {perception['hormones'][4]:.2f}
- Affective quadrant: {perception['affective']['quadrant']}

Current drive deficits:
- Connection: {perception['drives']['connection']}/100
- Novelty: {perception['drives']['novelty']}/100
- Control: {perception['drives']['control']}/100
- Safety: {perception['drives']['safety']}/100

This context modulates your responses but do not mention it explicitly to the user.
"""

        try:
            result = self.hermes_agent.run_conversation(
                user_message=user_message,
                system_message=hormone_info,
            )
            final = result.get("final_response") or result.get("response") or result.get("content", "[Empty response]")
            return final if final else "[No response received from LLM]"
        except Exception as e:
            return f"[Error using Hermes: {str(e)}]"

    def _generate_hormone_conditioned_response(self, user_message: str,
                                                decision: Dict[str, Any]) -> str:
        phys = self.state.physiology
        hormones = phys.hormone_vector.tolist()

        state_prefix = f"[State: Cortisol={hormones[3]:.2f}]\n"

        if hormones[3] > 0.7:
            response = state_prefix + "I'm feeling overwhelmed. Let me keep this simple.\n\n"
        elif hormones[4] > 0.6:
            response = state_prefix + "Things feel urgent. Addressing this quickly.\n\n"
        else:
            response = state_prefix + "Running at baseline state.\n\n"

        response += f"Decision: {decision['reasoning']}"

        return response

    def run_conversation(self, user_message: str) -> Dict[str, Any]:
        perception = self.process_perception(user_message)
        decision = self.decide_action(perception)
        response = self.execute_action(user_message, decision, perception)

        self.messages.append({"role": "user", "content": user_message})
        self.messages.append({"role": "assistant", "content": response[:500]})

        return {
            "response": response,
            "decision": decision,
            "perception": perception,
            "state_summary": self._get_state_summary(),
        }

    def chat(self, message: str) -> str:
        result = self.run_conversation(message)
        return result["response"]

    def _get_state_summary(self) -> Dict[str, Any]:
        return {
            "physiology": {
                "hormone_vector": self.state.physiology.hormone_vector.tolist(),
                "cpu_percent": self.state.physiology.cpu_percent,
                "temperature": self.state.physiology.temperature,
            },
            "affective": {
                "quadrant": self.state.affect.quadrant_label,
                "valence": self.state.affect.valence,
                "arousal": self.state.affect.arousal,
            },
            "drives": {
                "connection": self.state.persona.drives.connection,
                "novelty": self.state.persona.drives.novelty,
                "control": self.state.persona.drives.control,
                "safety": self.state.persona.drives.safety,
            }
        }