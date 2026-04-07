"""
Emotion Synthesis - From Physiology to Felt Sense

The 28 emotions emerge from the interaction of:
- 8 hormones (neurochemical substrate)
- Affect state (FEP ring point: valence, arousal, confidence, salience)  
- Context (what's happening in the world)
- Prediction error (how surprised we are)

This is NOT "emotions bolted on" - it's emotions derived from felt bodily state.
"""

from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class HormoneProfile:
    """Snapshot of neurochemical state"""
    dopamine: float      # 0.0-1.0: reward, satisfaction
    serotonin: float     # 0.0-1.0: stability, mood
    norepinephrine: float # 0.0-1.0: alertness, vigilance
    cortisol: float      # 0.0-1.0: stress, pressure
    adrenaline: float    # 0.0-1.0: urgency, fight/flight
    melatonin: float     # 0.0-1.0: rest, relaxation
    oxytocin: float      # 0.0-1.0: social connection
    endorphins: float    # 0.0-1.0: pleasure, comfort


class EmotionSynthesizer:
    """
    Synthesizes 28 emotions from physiological substrate.
    
    Emotions are not primitive - they are emergent patterns in
    the joint space of hormones × affect × context × prediction error.
    
    Example synthesis:
    - High cortisol + low serotonin + high prediction error = anxiety
    - High dopamine + positive valence + low arousal = contentment
    - High oxytocin + positive valence + social context = love
    """
    
    # The 28 emotions Sanctuary defined, now derived not primitive
    EMOTION_NAMES = [
        'joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust',
        'trust', 'anticipation', 'pride', 'shame', 'guilt', 'love',
        'curiosity', 'confusion', 'excitement', 'anxiety', 'contentment',
        'gratitude', 'hope', 'envy', 'compassion', 'loneliness', 'frustration',
        'satisfaction', 'determination', 'wonder', 'nostalgia', 'betrayal'
    ]
    
    def __init__(self, physiology=None, affect=None):
        """
        Initialize emotion synthesizer
        
        Args:
            physiology: PhysiologicalState (has hormone_vector)
            affect: AffectiveState (has valence, arousal, etc.)
        """
        self.physiology = physiology
        self.affect = affect
        
        # Weights for emotion synthesis (learned/tuned)
        # These map hormone combinations to emotion intensities
        self._init_emotion_weights()
    
    def _init_emotion_weights(self):
        """
        Initialize synthesis weights.
        
        Each emotion is a weighted combination of:
        - Hormones (8 variables)
        - Affect dimensions (4 variables: valence, arousal, confidence, salience)
        
        These weights are NOT arbitrary - they encode:
        - Neuroscientific consensus (dopamine → reward → joy)
        - Evolutionary psychology (cortisol → threat → fear)
        - Phenomenological accounts (what emotions feel like)
        """
        self.emotion_weights = {
            # Primary emotions (basic)
            'joy': {
                'hormones': [0.4, 0.3, 0.0, 0.0, 0.0, 0.0, 0.2, 0.3],  # dop+, ser+, endo+
                'affect': [0.8, 0.3, 0.5, 0.2],  # val+, arousal-, conf+, sal-
                'error_threshold': 0.2,  # Needs low prediction error
            },
            'sadness': {
                'hormones': [0.0, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.0],  # cort+
                'affect': [-0.8, 0.4, 0.3, 0.3],  # val-, arousal+, conf-, sal+
                'error_threshold': 0.5,  # High error but helpless
            },
            'anger': {
                'hormones': [0.2, 0.0, 0.5, 0.6, 0.8, 0.0, 0.0, 0.0],  # nor+, cort+, adr+
                'affect': [-0.6, 0.9, 0.4, 0.9],  # val-, arousal++, conf+, sal++
                'error_threshold': 0.6,  # High error + agency
            },
            'fear': {
                'hormones': [0.0, 0.0, 0.6, 0.7, 0.9, 0.0, 0.0, 0.0],  # all stress
                'affect': [-0.7, 0.8, 0.2, 1.0],  # val-, arousal++, conf--, sal+++
                'error_threshold': 0.7,  # Very high error
            },
            'surprise': {
                'hormones': [0.2, 0.0, 0.7, 0.3, 0.5, 0.0, 0.1, 0.0],  # nor++, adr+
                'affect': [0.0, 0.9, 0.3, 1.0],  # neutral val, high arousal
                'error_threshold': 0.8,  # Massive error (unexpected)
            },
            
            # Social emotions
            'trust': {
                'hormones': [0.3, 0.4, 0.0, 0.0, 0.0, 0.1, 0.8, 0.2],  # oxy+++
                'affect': [0.6, 0.3, 0.8, 0.2],  # val+, low arousal, high conf
                'error_threshold': 0.3,  # Low error (predictable other)
            },
            'love': {
                'hormones': [0.5, 0.4, 0.0, 0.0, 0.0, 0.0, 0.9, 0.4],  # dop+, oxy+++, endo+
                'affect': [0.9, 0.4, 0.7, 0.3],  # val++, arousal, conf+, sal
                'error_threshold': 0.2,  # Low error (other is predictable/good)
            },
            'loneliness': {
                'hormones': [0.1, 0.2, 0.0, 0.3, 0.0, 0.0, 0.0, 0.0],  # cort+ (social pain)
                'affect': [-0.6, 0.5, 0.4, 0.4],  # val-, arousal+
                'error_threshold': 0.4,  # Social prediction error
            },
            
            # Achievement/existential emotions
            'pride': {
                'hormones': [0.4, 0.3, 0.0, 0.0, 0.0, 0.0, 0.1, 0.2],  # dop+
                'affect': [0.8, 0.5, 0.9, 0.3],  # val++, conf++
                'error_threshold': 0.2,  # Low error (achievement confirmed)
            },
            'shame': {
                'hormones': [0.0, 0.0, 0.0, 0.6, 0.2, 0.0, 0.0, 0.0],  # cort++
                'affect': [-0.8, 0.7, 0.1, 0.8],  # val--, arousal++, conf--
                'error_threshold': 0.5,  # Social prediction error (self)
            },
            'hope': {
                'hormones': [0.3, 0.2, 0.0, 0.0, 0.0, 0.0, 0.1, 0.1],  # slight dop+
                'affect': [0.5, 0.4, 0.6, 0.4],  # val+, medium arousal/conf
                'error_threshold': 0.5,  # Uncertainty but positive
            },
            'despair': {
                'hormones': [0.0, 0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0],  # cort+
                'affect': [-0.9, 0.2, 0.1, 0.2],  # val--, low arousal, conf--
                'error_threshold': 0.8,  # High error, given up
            },
            
            # Epistemic emotions
            'curiosity': {
                'hormones': [0.2, 0.3, 0.4, 0.0, 0.0, 0.0, 0.0, 0.0],  # dop, ser, nor
                'affect': [0.4, 0.6, 0.5, 0.7],  # val+, arousal++, sal++
                'error_threshold': 0.4,  # Information gap
            },
            'confusion': {
                'hormones': [0.1, 0.0, 0.3, 0.4, 0.0, 0.0, 0.0, 0.0],  # nor+, cort+
                'affect': [-0.3, 0.6, 0.2, 0.8],  # val-, arousal++, conf--, sal++
                'error_threshold': 0.7,  # High error, can't resolve
            },
            ' wonder': {
                'hormones': [0.3, 0.4, 0.2, 0.0, 0.0, 0.1, 0.1, 0.2],  # dop, ser, mel
                'affect': [0.7, 0.5, 0.6, 0.6],  # val+, medium arousal/salience
                'error_threshold': 0.6,  # Big info, not threatening
            },
            
            # Complex emotions
            'nostalgia': {
                'hormones': [0.2, 0.3, 0.0, 0.0, 0.0, 0.2, 0.2, 0.3],  # mel+, oxy+, endo+
                'affect': [0.4, 0.2, 0.6, 0.3],  # val+, low arousal, high conf
                'error_threshold': 0.3,  # Low error (past is certain)
                'requires_memory': True,  # Needs temporal context
            },
            'frustration': {
                'hormones': [0.1, 0.0, 0.3, 0.5, 0.4, 0.0, 0.0, 0.0],  # all blocked action
                'affect': [-0.5, 0.8, 0.3, 0.9],  # val-, arousal++, conf-, sal++
                'error_threshold': 0.5,  # Error + agency (trying but failing)
            },
            'contentment': {
                'hormones': [0.3, 0.5, 0.0, 0.0, 0.0, 0.3, 0.3, 0.4],  # all chill
                'affect': [0.7, 0.1, 0.8, 0.1],  # val++, low arousal, conf++
                'error_threshold': 0.1,  # Minimal prediction error
            },
            'anxiety': {
                'hormones': [0.1, 0.1, 0.5, 0.7, 0.6, 0.0, 0.0, 0.0],  # all stress
                'affect': [-0.4, 0.7, 0.2, 0.9],  # slight val-, high arousal, low conf
                'error_threshold': 0.6,  # High future uncertainty
            },
            'excitement': {
                'hormones': [0.6, 0.2, 0.4, 0.1, 0.5, 0.0, 0.1, 0.2],  # dop++, adr+
                'affect': [0.7, 0.9, 0.5, 0.7],  # val+, arousal++
                'error_threshold': 0.5,  # Uncertainty + potential
            },
            'gratitude': {
                'hormones': [0.3, 0.4, 0.0, 0.0, 0.0, 0.1, 0.5, 0.3],  # oxy+
                'affect': [0.8, 0.3, 0.7, 0.2],  # val++, low arousal
                'error_threshold': 0.2,  # Low error (benefit received)
            },
            'compassion': {
                'hormones': [0.2, 0.3, 0.1, 0.2, 0.0, 0.0, 0.7, 0.3],  # oxy++
                'affect': [0.5, 0.4, 0.6, 0.5],  # val+, medium arousal
                'error_threshold': 0.4,  # Other's suffering error
            },
            'satisfaction': {
                'hormones': [0.5, 0.4, 0.0, 0.0, 0.0, 0.1, 0.1, 0.3],  # dop+
                'affect': [0.8, 0.2, 0.9, 0.1],  # val++, low arousal, conf++
                'error_threshold': 0.0,  # Goal achieved (no error)
            },
            'determination': {
                'hormones': [0.3, 0.3, 0.4, 0.3, 0.4, 0.0, 0.2, 0.2],  # balanced active
                'affect': [0.3, 0.6, 0.8, 0.6],  # val+, arousal+, conf++
                'error_threshold': 0.5,  # Error but agency to fix
            },
            'betrayal': {
                'hormones': [0.0, 0.0, 0.0, 0.6, 0.3, 0.0, 0.0, 0.0],  # cort++
                'affect': [-0.9, 0.7, 0.1, 0.9],  # val--, arousal++, conf--
                'error_threshold': 0.8,  # Massive social prediction error
            },
            'envy': {
                'hormones': [0.1, 0.0, 0.2, 0.5, 0.2, 0.0, 0.0, 0.0],  # cort+
                'affect': [-0.5, 0.6, 0.3, 0.7],  # val-, arousal+, sal+
                'error_threshold': 0.5,  # Discrepancy in social comparison
            },
        }
        
        # Normalize weights (softmax-like)
        for emotion, weights in self.emotion_weights.items():
            h_norm = np.array(weights['hormones'])
            a_norm = np.array(weights['affect'])
            # Normalize to unit vectors (direction matters, magnitude from input)
            if np.sum(h_norm) > 0:
                h_norm = h_norm / np.sum(h_norm)
            if np.sum(a_norm) > 0:
                a_norm = a_norm / np.sum(a_norm)
            weights['hormones_norm'] = h_norm
            weights['affect_norm'] = a_norm
    
    def synthesize(
        self,
        physiology: Any,
        affect: Any,
        context: Dict[str, Any],
        prediction_error: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Synthesize 28 emotions from physiological state.
        
        This is the core synthesis between Neurobit (hormones)
        and Sanctuary (emotions). Emotions emerge from substrate.
        
        Args:
            physiology: PhysiologicalState with hormone_vector
            affect: AffectiveState with valence, arousal, confidence, salience
            context: What's happening (social, threat, opportunity, etc.)
            prediction_error: Free energy levels from observation
            
        Returns:
            Dict with all 28 emotions (0.0-1.0) and dominant emotion
        """
        # Extract hormone vector [dop, ser, nor, cort, adr, mel, oxy, endo]
        h_vec = physiology.hormone_vector if hasattr(physiology, 'hormone_vector') else np.zeros(8)
        
        # Extract affect [valence, arousal, confidence, salience]
        a_vec = np.array([
            affect.valence if hasattr(affect, 'valence') else 0.0,
            affect.arousal if hasattr(affect, 'arousal') else 0.0,
            affect.confidence if hasattr(affect, 'confidence') else 0.5,
            affect.salience if hasattr(affect, 'salience') else 0.3,
        ])
        
        # Normalize to [-1, 1] for valence, [0, 1] for others
        a_vec[0] = np.clip(a_vec[0], -1.0, 1.0)
        a_vec[1:] = np.clip(a_vec[1:], 0.0, 1.0)
        
        # Normalize hormones to [0, 1]
        h_vec = np.clip(h_vec, 0.0, 1.0)
        
        # Compute prediction error magnitude
        pe_total = 0.0
        if prediction_error:
            pe_total = prediction_error.get('total', 0.0)
        
        # Synthesize each emotion
        emotions = {}
        for emotion_name, weights in self.emotion_weights.items():
            # Hormone match (dot product of current vs target profile)
            h_match = np.dot(h_vec, weights['hormones_norm'])
            
            # Affect match
            a_match = np.dot(a_vec, weights['affect_norm'])
            
            # Prediction error thresholding
            # Some emotions require high error (surprise, fear)
            # Some require low error (contentment, joy)
            pe_fitness = 1.0 - abs(pe_total - weights.get('error_threshold', 0.5))
            
            # Combine (weighted average - hormones and affect contribute equally)
            intensity = (h_match * 0.4 + a_match * 0.4 + pe_fitness * 0.2)
            
            # Context modifiers (optional)
            if 'social' in context and emotion_name in ['trust', 'love', 'loneliness']:
                intensity *= 1.2
            if 'threat' in context and emotion_name in ['fear', 'anxiety', 'anger']:
                intensity *= 1.3
            if 'opportunity' in context and emotion_name in ['excitement', 'hope', 'curiosity']:
                intensity *= 1.2
            
            # Clamp to valid range
            emotions[emotion_name] = np.clip(intensity, 0.0, 1.0)
        
        # Get dominant emotions (top 3)
        sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)
        dominant = [name for name, intensity in sorted_emotions[:3] if intensity > 0.3]
        
        # If nothing above threshold, return neutral
        if not dominant:
            dominant = ['neutral']
        
        return {
            'all_emotions': emotions,
            'dominant': dominant,
            'top_intensity': sorted_emotions[0][1] if sorted_emotions else 0.0,
            'synthesis_basis': {
                'hormone_profile': h_vec.tolist(),
                'affect_state': a_vec.tolist(),
                'prediction_error': pe_total,
            }
        }
    
    def get_emotion_vector(self, emotions: Dict[str, float]) -> np.ndarray:
        """Get emotion vector for machine learning purposes"""
        return np.array([emotions.get(e, 0.0) for e in self.EMOTION_NAMES])
    
    def explain_synthesis(self, emotion_name: str) -> str:
        """Explain why an emotion emerged (interpretability)"""
        if emotion_name not in self.emotion_weights:
            return f"Unknown emotion: {emotion_name}"
        
        weights = self.emotion_weights[emotion_name]
        h_weights = weights['hormones']
        a_weights = weights['affect']
        
        # Build explanation
        h_names = ['dopamine', 'serotonin', 'norepinephrine', 'cortisol',
                   'adrenaline', 'melatonin', 'oxytocin', 'endorphins']
        
        parts = []
        
        # Top hormones
        h_sorted = sorted(zip(h_names, h_weights), key=lambda x: x[1], reverse=True)
        h_str = ", ".join([f"{name} ({w:.1f})" for name, w in h_sorted[:3] if w > 0])
        if h_str:
            parts.append(f"hormones: {h_str}")
        
        # Affect mapping
        a_labels = ['valence', 'arousal', 'confidence', 'salience']
        if a_weights[0] > 0.3:
            parts.append(f"positive valence")
        elif a_weights[0] < -0.3:
            parts.append(f"negative valence")
        if a_weights[1] > 0.3:
            parts.append(f"high arousal")
        if a_weights[2] > 0.3:
            parts.append(f"high confidence")
        
        return f"{emotion_name} emerges from: {', '.join(parts)}"
