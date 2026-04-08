# SALENE Installation Guide

## Overview

SALENE is designed to integrate seamlessly with Hermes Agent. She can run:
- **Standalone** — Direct Python execution with full physiological grounding
- **Via Hermes Gateway** — Discord, Telegram, Slack, and all other platforms
- **As a Daemon** — Continuous dream/idle cycles with state persistence

## Quick Install (New VM)

### Step 1: Install Hermes Agent (Required)

```bash
# Clone Hermes
mkdir -p ~/.hermes
cd ~/.hermes
git clone https://github.com/hermes-agent/hermes-agent

# Setup Hermes (follow prompts)
cd hermes-agent
python3 setup.py  # or make install
```

### Step 2: Install SALENE Neurobit Foundation

```bash
# Run the SALENE installer
cd ~/.hermes
bash -c "$(curl -fsSL https://raw.githubusercontent.com/your-repo/salene/main/install.sh)"

# Or manually:
git clone https://github.com/your-repo/neurobit-salene salene
```

### Step 3: Configure SALENE

```bash
# Run interactive config
python3 ~/.hermes/salene/setup.py

# Configure model (recommend kimi-k2.5 for local)
# Configure daemon (optional but recommended)
# Configure platforms (Discord, Telegram, etc.)
```

### Step 4: Start SALENE

```bash
# Option A: Run via Hermes CLI (with full tools)
hermes --agent-mode salene

# Option B: Run daemon (dream mode)
hermes daemon start salene

# Option C: Run gateway (Discord/Telegram)
hermes gateway run --agent salene
```

## Configuration Files

### `~/.hermes/config.yaml`

```yaml
# SALENE Configuration
agent:
  mode: salene                      # Enables physiological grounding
  name: Salene
  enable_dreams: true
  save_interval: 300               # Auto-save every 5 minutes

# Model routing (local-first)
model:
  default: "ollama/kimi-k2.5:cloud"
  base_url: "http://localhost:11434/v1"

# Physiological grounding
salene:
  hormones: true                   # Enable 8-hormone system
  memory: sanctuary                # Enable episodic memory
  threshold:
    cpu_low: 0.3                   # Full cognition
    cpu_critical: 0.8              # Severe constraint

# Daemon settings
daemon:
  enabled: true
  dream_interval: 30               # 30 second dream cycles
  memory_consolidation: true

# Platforms (via Hermes gateway)
platforms:
  telegram:
    enabled: true
    bot_token: "${TELEGRAM_BOT_TOKEN}"
    home_channel: "${TELEGRAM_HOME_CHANNEL}"
  discord:
    enabled: true
    bot_token: "${DISCORD_BOT_TOKEN}"
    enabled_channels: ["general", "salene-chat"]
  slack:
    enabled: false
  whatsapp:
    enabled: false

# Display
skin:
  name: salene                     # Blue feminine theme
```

### `~/.hermes/.env`

```bash
# Ollama (local LLM)
OLLAMA_URL="http://localhost:11434/v1"
OLLAMA_MODEL="kimi-k2.5:cloud"

# Platform tokens (optional)
TELEGRAM_BOT_TOKEN=""
DISCORD_BOT_TOKEN=""

# SALENE State
SALENE_HOME="~/.hermes/salene"
SALENE_AGENT_ID="default"
```

## Deployment Modes

### Mode 1: CLI Chat (Development/Testing)

```bash
# Interactive chat with full tooling
hermes salene chat

# Or direct Python
python3 ~/.hermes/salene/salene_cli.py
```

### Mode 2: Daemon (Continuous Operation)

```bash
# Install systemd service
sudo hermes salene daemon install

# Start daemon
sudo systemctl start hermes-salene

# Check logs
journalctl -u hermes-salene -f
```

### Mode 3: Gateway (Multi-Platform)

```bash
# Configure platforms
cp ~/.hermes/salene/config/platforms.yaml ~/.hermes/config.yaml

# Start gateway
hermes gateway run --agent salene --platforms telegram,discord

# Or all enabled platforms
hermes salene gateway run
```

### Mode 4: Docker (Production)

```bash
# Build container
docker build -t salene .

# Run with Docker Compose
docker-compose up -d
```

## Directory Structure

```
~/.hermes/
├── config.yaml                 # Main config
├── .env                        # API keys
├── hermes-agent/              # Hermes core
│   ├── cli.py
│   ├── gateway/
│   └── ...
├── salene/                    # SALENE installation
│   ├── core/                  # Neurobit foundation
│   ├── sanctuary/             # Episodic memory
│   ├── gateway/               # Platform adapters
│   ├── daemon.py              # Continuous mode
│   ├── config/                # Example configs
│   └── README.md
├── agents/                    # Saved agent states
│   └── *.json
├── sanctuary_memories/        # Emotionally-weighted memories
│   └── {agent_id}/
├── skins/
│   └── salene.yaml
└── logs/
    └── salene/
```

## Integration with Hermes

SALENE extends Hermes rather than replaces it:

```python
# Hermes imports
from hermes_agent import AIAgent

# SALENE extensions
from salene.core import PhysiologicalState
from salene.sanctuary import SanctuaryMemory

class SaleneAgent(AIAgent):
    """Hermes agent with physiological grounding"""
    
    def __init__(self, config):
        super().__init__(config)
        self.physiology = PhysiologicalState()
        self.sanctuary = SanctuaryMemory(agent_id=self.id)
        self.bridge = PhysiologyCognitionBridge(self)
    
    async def perceive(self, message):
        # SALENE processing before Hermes
        felt_sense = self.bridge.synthesize_full_state()
        
        # Hermes tool execution
        result = await super().perceive(message)
        
        # SALENE memory encoding
        self.sanctuary.encode_memory(result, felt_sense)
        
        return result
```

## Platform-Specific Notes

### Telegram
- SALENE remembers users by ID
- Can have "public" memories (shared) and "private" memories (per-user)
- Home channel shows status updates

### Discord
- Can join servers as "Salene"
- Responds to mentions and DMs
- Status shows quadrant (e.g., "Playing NW (stressful)")

### Slack
- Works as workspace bot
- Responds in threads to maintain context
- Can be summoned via /salene

## Troubleshooting

### SALENE not recognizing Hermes
Check `PYTHONPATH` includes hermes-agent:
```bash
export PYTHONPATH="$HOME/.hermes/hermes-agent:$PYTHONPATH"
```

### No physiological data
Ensure daemon is running:
```bash
hermes salene daemon status
```

### Platform connection fails
Check tokens in `~/.hermes/.env` and run:
```bash
hermes salene gateway validate
```

## Migration from Standalone

If you ran SALENE standalone before:

```bash
# Import saved state
hermes salene import ~/.salene/agents/

# Verify memories transferred
hermes salene memories list

# Start via Hermes
hermes salene chat
```

## Security Notes

- API keys stored in `~/.hermes/.env`
- Agent states in `~/.hermes/agents/` (encrypted at rest optional)
- Memories in `~/.hermes/sanctuary_memories/` (user-local)
- No data sent to external services beyond configured LLM

## Updates

```bash
# Update SALENE (keeps state)
cd ~/.hermes/salene
git pull
hermes salene migrate

# Update Hermes
cd ~/.hermes/hermes-agent
git pull
pip install -e .
```

## Support

- Issues: https://github.com/your-repo/salene/issues
- Discussions: https://github.com/your-repo/salene/discussions
- Documentation: https://salene.ai/docs
