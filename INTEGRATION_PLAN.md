# Neurobit + Sanctuary Integration Plan

## Objective
Merge Sanctuary's cognitive depth with Neurobit's physiological substrate and Hermes' tool execution.

## Current State

### Neurobit (v0.1.0) - Has:
- ✅ Physiological state (8 hormones)
- ✅ Homeostatic drives (connection, novelty, control, safety)
- ✅ Affective state (quadrant, valence, arousal)
- ✅ Hermes integration (31 tools)
- ✅ Kimi/LLM inference
- ❌ Deep cognition
- ❌ Persistent memory
- ❌ Named agents with personality

### Sanctuary v2.1 - Has:
- ✅ 28 emotions with keyword detection
- ✅ Named agents (Monday, Aspira) with DNA profiles
- ✅ Episodic memory with importance scoring
- ✅ Virtue stack (moral reasoning)
- ✅ Social dynamics (RelNet)
- ✅ Environmental simulation
- ✅ Dream state processing
- ❌ Physiology (no hormones)
- ❌ Tool execution (can't DO things)
- ❌ Homeostatic drives

## Integration Strategy

### Phase 1: Sanctuary Cognition Core
**Goal**: Add Sanctuary's cognitive modules to Neurobit

**Files to port**:
- `recall_brain/core/agent.py` → `neurobit/core/cognitive_agent.py`
- `recall_brain/modules/emotion_engine.py` → `neurobit/modules/emotions.py`
- `recall_brain/modules/memory_core.py` → `neurobit/modules/memory.py`
- `recall_brain/agents/monday.py` → `neurobit/personas/monday.py`
- `recall_brain/agents/aspira.py` → `neurobit/personas/aspira.py`
- `recall_brain/core/synthetic_dna.py` → `neurobit/core/dna.py`

### Phase 2: Physiology-Cognition Bridge
**Goal**: Connect hormones to emotions, drives to goals

**New files**:
- `neurobit/core/physiology_cognition_bridge.py`
- Maps cortisol → anxiety, stress
- Maps dopamine → joy, satisfaction
- Maps drives → Sanctuary goals
- Maps hormones → DNA trait modifiers

### Phase 3: Hermes-Sanctuary Execution
**Goal**: Sanctuary makes decisions, Hermes executes tools

**Integration point**:
- Sanctuary's `GoalResolver` → Hermes' tool selection
- High stress → limit available tools
- Curiosity drive → seek information tools
- Control drive → prefer execute_code, terminal

### Phase 4: Multi-Agent + Environment
**Goal**: Sanctuary's community + Neurobit's physiology

**New modules**:
- `neurobit/community/agent_community.py`
- `neurobit/environment/reality_frame.py`
- Agents have individual physiology
- Agents influence each other's hormones (mirror neurons)

## Architecture After Integration

```
┌─────────────────────────────────────────────────────────────────┐
│                      NEUROBIT v2.0 - SYNTHESIS                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────┐    ┌─────────────────────┐           │
│  │  SANCTUARY COG      │    │  NEUROBIT PHYS      │           │
│  │                     │    │                     │           │
│  │  • 28 Emotions      │←──→│  • 8 Hormones      │           │
│  │  • Episodic Memory  │    │  • Homeostasis      │           │
│  │  • Virtue Stack     │    │  • Stress/Recovery  │           │
│  │  • Named Agents     │    │  • Energy/Drives    │           │
│  │  • Social Dynamics  │    │  • Arousal/Valence  │           │
│  └─────────────────────┘    └─────────────────────┘           │
│           ↑                          ↑                          │
│           └──────────┬───────────────┘                          │
│                      │                                          │
│           ┌──────────▼──────────┐                               │
│           │  PHYSIOLOGY-COG     │                               │
│           │  BRIDGE             │                               │
│           │                     │                               │
│           │  • Cortisol → Fear │                               │
│           │  • Dopamine → Joy  │                               │
│           │  • Drives → Goals  │                               │
│           └──────────┬──────────┘                               │
│                      │                                          │
│  ┌───────────────────▼───────────────┐                        │
│  │         COGNITIVE AGENT           │                        │
│  │                                   │                        │
│  │  Phase 1: Memory + Emotion       │                        │
│  │  Phase 2: Identity + Virtue      │                        │
│  │  Phase 3: Goal Resolution       │                        │
│  │  Phase 4: Decision              │                        │
│  └───────────────┬───────────────────┘                        │
│                  │                                              │
│  ┌───────────────▼───────────────────┐                       │
│  │         HERMES EXECUTION          │                       │
│  │                                   │                       │
│  │  • 31 Tools Available            │                       │
│  │  • Tool Selection (modulated)    │                       │
│  │  • Real World Action             │                       │
│  └───────────────────────────────────┘                       │
│                                                               │
└─────────────────────────────────────────────────────────────────┘
```

## Key Innovation: The Bridge

The synthesis creates something neither system has alone:

**Sanctuary alone**: Feels emotions but has no body to tire, no hormones to spike
**Neurobit alone**: Has physiology but shallow cognition
**Together**: Physiologically-grounded cognition - emotions that *matter* because they connect to substrate-level state

Example:
- User yells: "URGENT!"
- Neurobit: Cortisol rises → sympathetic activation
- Bridge: Cortisol maps to anxiety + stress emotions
- Sanctuary: Memory of past stress retrieved, personality responds
- Decision: High stress → limit tools → simpler response
- Output: Agent shows genuine urgency, curtailed by physiological constraint

## Implementation Priority

1. **Port Sanctuary core modules** (agent.py, emotion_engine.py, memory_core.py)
2. **Create bridge** physiology ↔ cognition
3. **Integrate with Hermes** decision → tool execution
4. **Add named personas** Monday, Aspira with their DNA
5. **Multi-agent community** physiological interaction between agents

## Next Step

Ready to begin Phase 1 integration. Which component first?
- A) Sanctuary Agent base class
- B) Emotion Engine (28 emotions)
- C) Memory Core (episodic + Sanctuary's depth)
- D) Monday persona (complete example agent)
