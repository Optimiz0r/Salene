# Sanctuary Architecture Analysis

## Executive Summary

Sanctuary v2.1 is a **modular cognitive architecture** with clear separation of concerns:
- **Agent**: Container/identity coordinator
- **ProcessingLoop**: 10-phase cognitive pipeline
- **Cognitive Modules**: Swappable units (Memory, Emotion, Identity, etc.)
- **DNA**: Trait system (15 core + custom) 0.0-1.0 range
- **LLM**: Pluggable generation backend

## Core Components

### 1. Agent Class (`core/agent.py`)
**Role**: Identity container + module coordinator

**State**:
```python
agent_id: str              # UUID
name: str                  # Human-readable
dna: SyntheticDNA          # Personality
created_at: datetime
emotional_state: EmotionalState
interaction_count: int
is_active: bool
is_dreaming: bool
current_goals: List
core_values: Dict
```

**Modules Initialized**:
- MemoryCore - episodic storage
- EmotionEngine - 28 emotion processing
- ProcessingLoop - cognitive pipeline
- LLM (OllamaLLM or CognitiveLLM)

**Key Methods**:
- `process_input(text, source, other_agent_id) -> str` - main entry
- `_initialize_emotional_baselines()` - maps DNA → emotion baselines
- `save_to_file() / load_from_file()` - persistence

**Design Pattern**: This is a **module container**—not the cognitive engine itself. Smart separation.

---

### 2. ProcessingLoop (`core/processing_loop.py`)
**Role**: Cognitive pipeline orchestrator

**10 Phases** (sequential, each transforms ProcessingContext):

| Phase | Module | Purpose | Neurobit Equivalent |
|-------|--------|---------|-------------------|
| 1. Memory Scan | MemoryCore | Retrieve relevant memories | Memory (planned) |
| 2. Emotional Processing | EmotionEngine | Update affect from input | Affect + Physiology |
| 3. Identity Processing | IdentityEngine | Check self-consistency | Persona |
| 4. Social Processing | SocialMemory | Update relationships | N/A (future) |
| 5. Goal Processing | GoalConflictResolver | Resolve priorities | DriveState deficits |
| 6. Virtue Processing | VirtueStack | Apply moral reasoning | Governance |
| 7. Output Shaping | PromptEngine | Prepare LLM context | Context building |
| 8. LLM Generation | BaseLLM | Generate text | Hermes via Kimi |
| 9. Language Refinement | LexEcho | Style adjustment | TBD |
| 10. Memory Encoding | MemoryCore | Store interaction | Memory (planned) |

**Key Insight**: Each phase is **pure**—takes context, returns context. Easy to:
- Add/remove phases
- Modify single phase without affecting others
- Skip phases conditionally

**Timing**: Tracks per-phase and total processing time

---

### 3. SyntheticDNA (`core/synthetic_dna.py`)
**Role**: Personality trait container

**15 Core Traits** (0.0 - 1.0, all clamped):
```python
empathy: float                # Capacity for understanding others
emotional_volatility: float   # How quickly emotions change
emotional_intensity: float    # Strength of emotional responses
memory_fidelity: float        # Accuracy of memory recall
risk_tolerance: float         # Comfort with uncertainty
curiosity: float              # Desire to explore/learn
analytical_thinking: float    # Logical processing strength
trust_baseline: float         # Default trust level
social_dominance: float       # Assertiveness in social settings
conflict_avoidance: float     # Tendency to avoid confrontation
moral_rigidity: float         # Flexibility in moral reasoning
self_preservation: float      # Self-protection priority
altruism: float               # Concern for others' welfare
identity_stability: float     # How stable self-concept is
introspection_frequency: float # How often self-reflects

# Plus custom traits dict for extensibility
custom_traits: Dict[str, float]
```

**Templates**:
- analytical (high analytical_thinking, curiosity)
- empathetic (high empathy, altruism)
- leader (high social_dominance, risk_tolerance)
- creative (high curiosity, risk_tolerance)

**Neurobit Mapping**:
```
Sanctuary DNA           Neurobit Equivalent
----------------       -------------------
empathy                →  Persona empathy baseline
emotional_volatility   →  Physiology hormone volatility
risk_tolerance         →  Governance hazard tolerance
altruism               →  Drives connection weight
self_preservation      →  Drives safety weight
curiosity              →  Drives novelty weight
analytical_thinking    →  Cognitive state reasoning
```

---

### 4. EmotionalState (`core/emotional_state.py`)
**Role**: Affective state container

**State**:
```python
valence: float (-1.0 to 1.0)      # Overall tone
arousal: float (0.0 to 1.0)       # Activation level
emotions: Dict[str, float]         # Named emotions → intensities
emotion_timestamps: Dict[str, datetime]  # For decay
decay_rate: float                 # How fast emotions fade
baseline_valence: float           # Default valence
baseline_arousal: float          # Default arousal
```

**28 Basic Emotions** (from EmotionEngine):
joy, sadness, anger, fear, surprise, disgust, trust, anticipation, 
pride, shame, guilt, love, curiosity, confusion, excitement, anxiety, 
contentment, gratitude, hope, envy, compassion, loneliness, frustration,
satisfaction, determination, wonder, nostalgia, betrayal

**Decay**: Emotions fade over time (configurable rate). Can be reinforced.

**Neurobit Mapping**:
```
Sanctuary               Neurobit
----------------       -------------------
valence                →  Affect.valence
arousal                →  Affect.arousal / Physiology.adrenaline-specific
emotions (28)          →  Physiology.hormone_vector + Persona.emotions
decay_rate             →  Physiology delta_time
```

**Key Difference**: 
- Sanctuary has **28 named emotions** (categorical)
- Neurobit has **8 hormones** that map to affect (dimensional)

**Synthesis Opportunity**: 28 emotions ←→ 8 hormones bidirectional mapping

---

### 5. ProcessingContext
**Role**: State container passed through pipeline

**Contents**:
```python
input_text: str
input_source: str
agent_id: str
other_agent_id: Optional[str]
current_emotional_state: EmotionalState
retrieved_memories: List[MemoryEntry]
emotional_changes: Dict[str, float]
goal_conflicts: List[GoalConflict]
virtue_analysis: VirtueAnalysis
prompt_context: Dict[str, Any]
final_response: str
response_confidence: float
module_timings: Dict[str, float]
context_tags: List[str]
```

**Purpose**: Each phase reads from context, writes back. Immutable-ish pattern (functional)

---

## Module Catalog

### Core Modules (Required)

**MemoryCore** (`modules/memory_core.py`)
- Episodic memory with importance scoring
- Semantic similarity search
- Forgetting curves
- Tags and embeddings
- **Status**: Needs port

**EmotionEngine** (`modules/emotion_engine.py`)
- 28 emotion detection
- Emotional baselines
- History tracking
- **Status**: Can map to Neurobit hormones + Persona emotions

**IdentityEngine** (`modules/identity_engine.py`)
- Self-reflection
- Trait evolution
- Identity consistency checking
- **Status**: Similar to Neurobit PersonaState

**SocialMemory** (`modules/social_memory.py`)
- Relationship tracking (RelNet)
- Trust/familiarity/tone
- Multi-agent community
- **Status**: New capability

**GoalConflictResolver** (`modules/goal_resolver.py`)
- Priority management
- Conflict detection
- **Status**: Similar to DriveState deficits

### Phase 2 Modules (Advanced)

**VirtueStack** (`modules/virtue_stack.py`)
- Moral reasoning
- Ethical templates
- **Status**: New capability

**LexEcho** (`modules/lex_echo.py`)
- Language style refinement
- Personality-aware output
- **Status**: Could integrate with LLM prompt

**DreamEngine** (`modules/dream_engine.py`)
- Idle processing
- Memory consolidation
- **Status**: New capability

**SystemGovernor** (`modules/system_governor.py`)
- Resource monitoring
- Dynamic throttling
- **Status**: Partially exists in Neurobit GovernanceState

---

## Architecture Strengths

1. **Modularity**: Clean interfaces, swappable components
2. **Pipelining**: Sequential phases, easy to extend
3. **Pure Functions**: Context transforms, testable
4. **Persistence**: Complete state save/load
5. **Multi-Agent**: Social dynamics built-in
6. **DNA System**: Trait-based personality definition

## Architecture Gaps

1. **No Physiology**: Emotions not grounded in substrate state
2. **No Real Tools**: Can't execute in world (unlike Hermes integration)
3. **No Homeostasis**: Drives are goals, not felt deficits
4. **No Continuous Operation**: Turn-based, not autonomous
5. **Complex Dependency Graph**: Many modules, hard initialization

## Integration Strategy

### Port These (High Value)

1. **Agent** class - container pattern ✅
2. **ProcessingLoop** - 10-phase pipeline ✅
3. **SyntheticDNA** - trait system ✅ (maps to Neurobit DNA)
4. **EmotionalState** - 28 emotions (maps to hormones)
5. **MemoryCore** - episodic memory ✅
6. **ProcessingContext** - pipeline state ✅

### Mapping Strategy

```
Sanctuary → Neurobit Synthesis
----------------------------------
Agent (container) → Agent (Neurobit container)
ProcessingLoop → Cognitive Pipeline + Physiology Bridge
DNA (15 traits) → DNA + Physiological drives
Emotion (28) → Emotion + Hormone vector
MemoryCore → Unified State episodic
ProcessingLoop → Decision interface
```

### Bridge Concept

The Physiology-Cognition Bridge:
```python
class PhysiologyCognitionBridge:
    def hormones_to_emotions(self, hormone_vector) -> Dict[str, float]:
        # cortisol → anxiety, fear
        # dopamine → joy, satisfaction
        # adrenaline → excitement, urgency
        # etc.
    
    def drives_to_goals(self, drive_deficits) -> List[Goal]:
        # connection deficit → social goals
        # novelty deficit → exploration goals
        # etc.
    
    def affect_to_valence_arousal(self, affect_state) -> Tuple[float, float]:
        # quadrant → valence/arousal
```

## Recommendation

**Port Architecture, Synthesize Implementation**:

1. Port `Agent` base class - clean container pattern
2. Port `ProcessingLoop` - proven pipeline
3. Port `SyntheticDNA` - trait system is excellent
4. Port `MemoryCore` - Sanctuary's is more mature
5. **Keep Neurobit**: Physiology, drives, hormones (unique contribution)
6. **Synthesize**: Emotion system (hormones + Sanctuary emotions)
7. **Synthesize**: Decision system (drives + Sanctuary goals)
8. **New**: Physiology-Cognition Bridge

This preserves Sanctuary's cognitive architecture while grounding it in Neurobit's physiological substrate—the synthesis both projects need.

## Next Steps

Ready to begin porting:
1. Base `Agent` class
2. `ProcessingContext`
3. `ProcessingLoop` skeleton
4. DNA trait system
5. Bridge to Neurobit physiology

Your call on sequence.
