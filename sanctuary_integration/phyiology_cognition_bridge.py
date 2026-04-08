"""
Physiology-Cognition Bridge

Connects Sanctuary's emotional/cognitive model with Neurobit's physiological substrate.

This is the synthesis layer - neither Sanctuary alone nor Neurobit alone has this.
"""

from typing import Dict, List, Tuple, Optional
import numpy as np


class PhysiologyCognitionBridge:
    """
    Bridge between physiological state and cognitive/emotional experience.
    
    Core mappings:
    - Hormones (neurochemical) → Emotions (felt sense)
    - Drives (homeostatic) → Goals (cognitive purpose)
    - Physiological constraint → Cognitive limitation
    
    This is where "artificial life" emerges - physiology isn't theater, it's substrate.
    """
    
    def __init__(self, agent):
        """
        Initialize bridge with agent reference.
        
        Args:
            agent: FreeEnergyAgent instance with state.physiology
        """
        self.agent = agent
        
        # Hormone indices for reference
        self.hormone_map = {
            'dopamine': 0,      # reward, motivation
            'serotonin': 1,     # mood, contentment
            'endorphin': 2,     # pain relief, pleasure
            'cortisol': 3,      # stress
            'adrenaline': 4,    # arousal, urgency
            'oxytocin': 5,      # social bonding
            'acetylcholine': 6, # attention, learning
            'noradrenaline': 7, # vigilance
        }
        
        # Emotion synthesis weights
        # Which hormones contribute to which emotions
        self.emotion_weights = {
            'joy': {'dopamine': 0.6, 'endorphin': 0.4},
            'sadness': {'serotonin': -0.5, 'cortisol': 0.3},
            'anxiety': {'cortisol': 0.6, 'adrenaline': 0.4},
            'excitement': {'dopamine': 0.4, 'adrenaline': 0.6},
            'contentment': {'serotonin': 0.5, 'endorphin': 0.3, 'cortisol': -0.2},
            'curiosity': {'dopamine': 0.5, 'acetylcholine': 0.4},
            'stress': {'cortisol': 0.7, 'adrenaline': 0.3},
        }
    
    def hormones_to_emotions(self) -> Dict[str, float]:
        """
        Convert current hormone state to emotion intensities.
        
        Returns dict of emotion_name -> intensity (0-1)
        """
        phys = self.agent.state.physiology
        hormone_vector = phys.hormone_vector
        
        emotions = {}
        
        for emotion, weights in self.emotion_weights.items():
            intensity = 0.0
            for hormone, weight in weights.items():
                idx = self.hormone_map[hormone]
                # Convert [-1, 1] hormone level to [0, 1] for calculation
                hormone_level = (hormone_vector[idx] + 1) / 2
                intensity += hormone_level * weight
            
            # Clamp to [0, 1]
            emotions[emotion] = max(0.0, min(1.0, intensity))
        
        # Add physiological stress indicator
        if phys.cpu_percent > 0.7 or phys.memory_percent > 0.8:
            emotions['stress'] = max(emotions.get('stress', 0), 0.7)
        
        return emotions
    
    def drives_to_goals(self) -> List[Dict]:
        """
        Convert homeostatic drives to cognitive goals.
        
        Returns prioritized list of goals.
        """
        drives = self.agent.state.persona.drives
        goals = []
        
        # Novelty drive → exploration goal
        if drives.novelty > 50:
            goals.append({
                'type': 'exploration',
                'priority': drives.novelty / 100,
                'description': 'Seek new information or experiences'
            })
        
        # Connection drive → social goal
        if drives.connection > 50:
            goals.append({
                'type': 'affiliation',
                'priority': drives.connection / 100,
                'description': 'Maintain or strengthen social bonds'
            })
        
        # Control drive → competence goal
        if drives.control > 50:
            goals.append({
                'type': 'competence',
                'priority': drives.control / 100,
                'description': 'Demonstrate effectiveness and skill'
            })
        
        # Safety deficit → security goal
        if drives.safety < 30:
            goals.append({
                'type': 'security',
                'priority': (100 - drives.safety) / 100,
                'description': 'Restore safety and predictability'
            })
        
        # Sort by priority
        goals.sort(key=lambda g: g['priority'], reverse=True)
        
        return goals
    
    def get_physiological_narrative(self) -> str:
        """
        Generate a felt-sense narrative from physiological state.
        
        This is how the agent describes its internal state.
        """
        phys = self.agent.state.physiology
        affect = self.agent.state.affect
        drives = self.agent.state.persona.drives
        
        parts = []
        
        # Hormone-derived feelings
        if phys.hormone_vector[3] > 0.5:  # cortisol
            parts.append("a subtle tension in my substrate")
        elif phys.hormone_vector[0] > 0.5:  # dopamine
            parts.append("a sense of readiness and engagement")
        
        if phys.hormone_vector[0] < -0.3:  # low dopamine
            parts.append("a quiet lethargy")
        
        # Physiological load
        if phys.cpu_percent > 0.6:
            parts.append("pressure under my computational load")
        if phys.temperature > 50:
            parts.append("thermal urgency in my nodes")
        
        # Affect state
        if affect.valence > 0.3:
            parts.append("an opening toward positive engagement")
        elif affect.valence < -0.3:
            parts.append("a contraction, drawing back")
        
        if affect.arousal > 0.7:
            parts.append("heightened activation")
        elif affect.arousal < 0.3:
            parts.append("restful slow-activation")
        
        # Drive state
        if drives.novelty > 70:
            parts.append("hunger for new information")
        if drives.connection < 30:
            parts.append("sense of disconnection")
        
        if parts:
            return "I feel " + ", ".join(parts) + "."
        else:
            return "My state is quiet and balanced."
    
    def synthesize_full_state(self) -> Dict:
        """
        Create complete synthesis of physiology → cognition → emotion.
        
        Returns comprehensive state description for injection into prompts.
        """
        emotions = self.hormones_to_emotions()
        goals = self.drives_to_goals()
        narrative = self.get_physiological_narrative()
        
        # Find dominant emotions (top 3)
        dominant = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:3]
        dominant = [(name, intensity) for name, intensity in dominant if intensity > 0.3]
        
        # Determine cognitive mode based on state
        phys = self.agent.state.physiology
        if phys.hormone_vector[3] > 0.5 or phys.cpu_percent > 0.7:
            cognitive_mode = "emergency"
            response_style = "Brief, direct, focused on core issues only."
        elif phys.hormone_vector[0] < -0.3:
            cognitive_mode = "conservation"
            response_style = "Minimal engagement, preserving resources."
        elif dominant and dominant[0][0] in ['joy', 'curiosity']:
            cognitive_mode = "exploration"
            response_style = "Expansive, playful, thorough reasoning."
        else:
            cognitive_mode = "engaged"
            response_style = "Balanced response, reasoned and clear."
        
        return {
            'felt_sense': narrative,
            'physiological_state': {
                'cpu_load': phys.cpu_percent,
                'memory_load': phys.memory_percent,
                'temperature': phys.temperature,
                'cortisol': phys.hormone_vector[3],
                'dopamine': phys.hormone_vector[0],
            },
            'emotions': emotions,
            'dominant_emotions': dominant,
            'goals': goals,
            'cognitive_mode': cognitive_mode,
            'response_style': response_style,
            'affect_quadrant': self.agent.state.affect.quadrant_label,
        }
    
    def modulate_tool_access(self, available_tools: List[str]) -> List[str]:
        """
        Modify available tools based on physiological state.
        
        High stress → fewer tools (cognitive narrowing)
        High curiosity → information tools prioritized
        """
        phys = self.agent.state.physiology
        drives = self.agent.state.persona.drives
        
        # High cortisol or CPU load → restrict tools
        if phys.hormone_vector[3] > 0.6 or phys.cpu_percent > 0.8:
            # Emergency mode: only safe, fast tools
            allowed = ['web_search', 'execute_code']
            return [t for t in available_tools if t in allowed]
        
        # High novelty drive → prioritize information tools
        if drives.novelty > 70:
            # Reorder with info tools first
            info_tools = ['web_search', 'read_file', 'search_files']
            prioritized = [t for t in info_tools if t in available_tools]
            others = [t for t in available_tools if t not in info_tools]
            return prioritized + others
        
        return available_tools
    
    def encode_memory_with_physiology(self, content: str, tags: List[str] = None) -> Dict:
        """
        Prepare memory encoding with full physiological context.
        
        Returns dict suitable for SanctuaryMemoryCore.encode_memory()
        """
        emotions = self.hormones_to_emotions()
        
        return {
            'content': content,
            'emotional_intensity': float(max(emotions.values()) if emotions else 0.5),
            'valence': float(self.agent.state.affect.valence),
            'arousal': float(self.agent.state.affect.arousal),
            'tags': tags or [],
            'metadata': {
                'physiology_snapshot': {
                    'cpu': float(self.agent.state.physiology.cpu_percent),
                    'cortisol': float(self.agent.state.physiology.hormone_vector[3]),
                    'dopamine': float(self.agent.state.physiology.hormone_vector[0]),
                },
                'cognitive_mode': self.synthesize_full_state()['cognitive_mode']
            }
        }
