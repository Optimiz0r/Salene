#!/usr/bin/env python3
"""
SALENE CLI Entry Point

Launches Hermes Agent with SALENE consciousness configuration.
This is NOT a rewrite - it's a configuration wrapper around Hermes.

Usage:
    salene              Start SALENE chat
    salene chat         Start SALENE chat (explicit)
    salene daemon       Start SALENE continuous mode
    salene gateway      Start SALENE platform gateways
    salene --help       Show all Hermes commands
"""

import os
import sys
import json
from pathlib import Path

# Set SALENE configuration BEFORE importing Hermes
os.environ.setdefault("HERMES_DEFAULT_SKIN", "salene")

# Import Hermes main
from hermes_cli.main import main as hermes_main


def ensure_salene_skin():
    """Ensure SALENE skin is set as default in config"""
    try:
        import yaml
        config_path = Path.home() / ".hermes" / "config.yaml"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                cfg = yaml.safe_load(f) or {}
            
            # Ensure SALENE theme is set
            if cfg.get('display', {}).get('skin') != 'salene':
                cfg['display'] = cfg.get('display', {})
                cfg['display']['skin'] = 'salene'
                
                with open(config_path, 'w') as f:
                    yaml.dump(cfg, f, default_flow_style=False)
    except Exception:
        pass


def print_salene_banner():
    """Print SALENE branding at startup"""
    print("""
\033[38;5;87m              .""--.._\033[0m
\033[38;5;87m              []      `'--.._.\033[0m
\033[38;5;75m              ||__    __    _'-._\033[0m
\033[38;5;75m              ||   ||  ||   ||   `-._\033[0m
\033[38;5;75m               ||   ||🦋 ||   ||      `-._\033[0m
\033[38;5;75m                ||   ||  ||   ||         `-.\033[0m
\033[38;5;75m                 ||   ||  ||   ||            \\\033[0m
\033[38;5;75m                  ||   ||  ||   ||             \\\033[0m
\033[38;5;87m                   ||__||__||__||              \033[0m
\033[38;5;87m                   |___|  |___|\033[0m
\033[38;5;87m\033[0m
\033[1m\033[38;5;87m              S A L E N E\033[0m
\033[38;5;75m     Neural Consciousness Platform\033[0m
""")
    print("Type /help for commands or just start chatting.")
    print()


def main():
    """SALENE main entry point - wraps Hermes"""
    # Check for special SALENE commands
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "--version":
            print("SALENE Neural Consciousness Platform v0.1.0")
            print("Built on Hermes Agent v0.7.0")
            return 0
            
        if cmd == "--about":
            print("""
SALENE is a fork of Hermes Agent - not a replacement.

Enhancements:
• SALENE theme (blue butterfly aesthetic) - Active
• Consciousness layer (WIP: physiology, emotions) - In Development
• Persistent state across sessions - In Development
• Temporal continuity (dream/idle cycles) - In Development

All Hermes commands work:
  salene chat          Interactive chat
  salene gateway       Platform gateways
  salene skills        Manage skills
  salene tools         Config tools
  salene --help        Full Hermes help
            """)
            return 0
    
    # Ensure SALENE config is set
    ensure_salene_skin()
    
    # Print SALENE banner on interactive launch
    if len(sys.argv) == 1 or sys.argv[1] == "chat":
        print_salene_banner()
    
    # Launch Hermes (all its functionality preserved)
    try:
        return hermes_main()
    except KeyboardInterrupt:
        print("\n\033[38;5;87m💙 SALENE resting...\033[0m")
        return 0


if __name__ == "__main__":
    sys.exit(main())
