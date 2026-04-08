#!/usr/bin/env python3
"""
Step C: Neurobit + Synthesis Test

Connect real Neurobit physiology → EmotionSynthesizer
"""

import sys
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')
sys.path.insert(0, '/home/optimizor/neurobit-project')

print("="*60)
print("NEUROBIT + SYNTHESIS INTEGRATION")
print("="*60)

# 1. Import Neurobit
from core.unified_state import UnifiedState
print("\n🧬 Phase 1: Create Neurobit state")
state = UnifiedState()
phys = state.physiology
affect = state.affect

print(f"   Initial hormones: dop={phys.hormone_vector[0]:.2f}, cort={phys.hormone_vector[3]:.2f}")
print(f"   Initial affect: quadrant={affect.quadrant_label}, valence={affect.valence:.2f}")

# 2. Import synthesis
from free_energy_agent.emergence.emotion_synthesis import EmotionSynthesizer
synthesizer = EmotionSynthesizer()
print("   ✓ EmotionSynthesizer created")

# 3. Create "observation"
observation = "Something unexpected happened!"
print(f"\n🧬 Phase 2: Observation '{observation}'")

# 4. Manually simulate prediction error → physiology update
# High error → sympathetic activation
phys.cpu_percent = 0.6
phys.temperature = 42.0
phys.hormone_vector[3] = 0.7  # cortisol rise
phys.hormone_vector[4] = 0.6  # adrenaline rise

print(f"   Physiology: CPU={phys.cpu_percent:.0%}, cortisol={phys.hormone_vector[3]:.2f}")

# 5. Affect update from prediction error
affect.ring_point[0] = -0.3  # valence drop
affect.ring_point[1] = 0.7   # arousal rise
affect.confidence = 0.4       # confidence drops
affect.salience = 0.8         # high salience

print(f"   Affect: valence={affect.valence:.2f}, arousal={affect.arousal:.2f}, conf={affect.confidence:.2f}")

# 6. SYNTHESIS
print("\n🧬 Phase 3: SYNTHESIS → Emotions")
emotions = synthesizer.synthesize(
    physiology=phys,
    affect=affect,
    context={'unexpected': True},
    prediction_error={'total': 0.7}
)

print(f"   DOMINANT EMOTIONS: {emotions['dominant']}")
print(f"   Top intensity: {emotions['top_intensity']:.2f}")

# Show all emotions > 0.5
top_emotions = [(k, v) for k, v in emotions['all_emotions'].items() if v > 0.5]
top_emotions.sort(key=lambda x: x[1], reverse=True)
print(f"\n   All strong emotions (>0.5):")
for name, intensity in top_emotions[:5]:
    print(f"     {name}: {intensity:.2f}")

print("\n" + "="*60)
print("✅ INTEGRATION SUCCESS")
print("="*60)
print("\nNeurobit → Synthesis works!")
print("Physiology updates → Emotions emerge from substrate")
print("Next: Connect this to action selection (Hermes)")
