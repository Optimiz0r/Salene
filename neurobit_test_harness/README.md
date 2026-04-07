# Neurobit Test Harness

**A testbed for experimenting with humanistic AI traits using Hermes infrastructure + Neurobit physiological cognition.**

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    NEUROBIT TEST HARNESS                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌─────────────┐ │
│  │   Hermes     │────>│ MCP Client   │────>│ Docker MCP  │ │
│  │ Infrastructure│     │ (Tools)      │     │ Plugins     │ │
│  └──────────────┘     └──────────────┘     └─────────────┘ │
│         │                                                  │
│         │   ┌────────────────────────────────────┐      │
│         └──>│         Neurobit Core               │      │
│             │                                      │      │
│             │  • PhysiologicalState (hormones)    │      │
│             │  • AffectiveState (emotions)         │      │
│             │  • PerceptualState (tokens)          │      │
│             │  • DriveState (homeostatic needs)    │      │
│             │                                      │      │
│             │  Decision loop modulated by:        │      │
│             │    → Cortisol (stress limiting)       │      │
│             │    → Dopamine (reward/repetition)     │      │
│             │    → Adrenaline (urgency/action)      │      │
│             └────────────────────────────────────┘      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Hormone Modulation

High cortisol limits tool calling. High dopamine prefers successful patterns. High adrenaline triggers rapid response.

## Usage

```bash
# Run interactive test
cd ~/.hermes/hermes-agent
source venv/bin/activate
python neurobit_test_harness/test_runner.py
```

Type messages. Use "urgent" or "emergency" to see hormone modulation.

## Docker MCP Modules

- voice_input: Speech-to-text via faster-whisper
- vision_organ: OpenCV face/object detection  
- memory_organ: Episodic/semantic memory storage

Add to ~/.hermes/config.yaml under mcp_servers: key.

## Files

- core/neurobit_agent.py: Main agent with physiological cognition
- config/mcp_servers.yaml: Docker plugin configuration
- docker_examples/: Template MCP servers

## Integration Points

### NeurobitAgent wraps Hermes AIAgent:

| Layer | Hermes | Neurobit |
|-------|--------|----------|
| Tools | MCP client | Hormone-modulated selection |
| Session | SQLite persistence | Physiological state snapshots |
| Platform | CLI/Telegram/Discord | Emotional continuity |

### Key Methods:

- **process_perception()**: Maps input → hormone-aware tokens
- **decide_action()**: Modulates tool choice by cortisol/dopamine/adrenaline
- **execute_action()**: Generates state-conditioned responses
