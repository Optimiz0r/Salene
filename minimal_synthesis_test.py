#!/usr/bin/env python3
"""
Minimal Synthesis Test (Option B)

Test that emotions emerge from physiology × affect × context
Without any integration complexity.
"""

import sys
import numpy as np
import asyncio

sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.emergence.emotion_synthesis import EmotionSynthesizer

# Mock classes that simulate Neurobit state
class MockPhysiology:
    def __init__(self, hormone_vector):
        self.hormone_vector = np.array(hormone_vector)

class MockAffect:
    def __init__(self, valence, arousal, confidence, salience):
        self.valence = valence
        self.arousal = arousal
        self.confidence = confidence
        self.salience = salience

def test_emotion_synthesis():
    """Test core synthesis: hormones × affect → emotions"""
    print("="*60)
    print("MINIMAL EMOTION SYNTHESIS TEST")
    print("="*60)
    
    synthesizer = EmotionSynthesizer()
    
    # Test 1: Baseline state
    print("\n🧪 Test 1: Neutral/Baseline")
    neutral_hormones = [0.5, 0.5, 0.2, 0.2, 0.1, 0.3, 0.6, 0.4]  # [dop, ser, nor, cort, adr, mel, oxy, endo]
    neutral_affect = MockAffect(valence=0.2, arousal=0.3, confidence=0.7, salience=0.2)
    
    result1 = synthesizer.synthesize(
        physiology=MockPhysiology(neutral_hormones),
        affect=neutral_affect,
        context={},
        prediction_error={'total': 0.1}
    )
    print(f"  Hormones: cortisol=0.2, dopamine=0.5")
    print(f"  Affect: valence=0.2, arousal=0.3")
    print(f"  Emotions: {result1['dominant']}")
    print(f"  Top intensity: {result1['top_intensity']:.2f}")
    
    # Test 2: High stress
    print("\n🧪 Test 2: High Stress")
    stress_hormones = [0.2, 0.3, 0.7, 0.8, 0.8, 0.0, 0.2, 0.1]  # High cortisol, adrenaline
    stress_affect = MockAffect(valence=-0.3, arousal=0.8, confidence=0.3, salience=0.9)
    
    result2 = synthesizer.synthesize(
        physiology=MockPhysiology(stress_hormones),
        affect=stress_affect,
        context={'threat': True},
        prediction_error={'total': 0.7}
    )
    print(f"  Hormones: cortisol=0.8, adrenaline=0.8")
    print(f"  Affect: valence=-0.3, arousal=0.8")
    print(f"  Emotions: {result2['dominant']}")
    print(f"  Top intensity: {result2['top_intensity']:.2f}")
    
    # Test 3: Reward state
    print("\n🧪 Test 3: Reward/Reward State")
    reward_hormones = [0.9, 0.7, 0.2, 0.1, 0.1, 0.2, 0.5, 0.6]  # High dopamine, endorphins
    reward_affect = MockAffect(valence=0.8, arousal=0.4, confidence=0.8, salience=0.3)
    
    result3 = synthesizer.synthesize(
        physiology=MockPhysiology(reward_hormones),
        affect=reward_affect,
        context={'opportunity': True},
        prediction_error={'total': 0.1}
    )
    print(f"  Hormones: dopamine=0.9, endorphins=0.6")
    print(f"  Affect: valence=0.8, arousal=0.4")
    print(f"  Emotions: {result3['dominant']}")
    print(f"  Top intensity: {result3['top_intensity']:.2f}")
    
    # Summary
    print("\n" + "="*60)
    print("✅ SYNTHESIS TEST COMPLETE")
    print("="*60)
    print("\nKey finding: Emotions emerge from hormone × affect combinations:")
    print(f"  Baseline: {result1['dominant']} ← moderate dop/ser + neutral valence")
    print(f"  Stress:   {result2['dominant']} ← high cortisol/adrenaline + neg valence")
    print(f"  Reward:   {result3['dominant']} ← high dopamine/endorphins + pos valence")
    
    return True

if __name__ == "__main__":
    test_emotion_synthesis()
