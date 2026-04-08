#!/usr/bin/env python3
"""
SALENE Status Monitor

Quickly check SALENE's current state without loading the full agent.
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Colors
BLUE = "\033[38;5;75m"
CYAN = "\033[38;5;87m"
GREEN = "\033[38;5;82m"
YELLOW = "\033[38;5;221m"
RED = "\033[38;5;196m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner():
    print(f"""
{CYAN}              .""--.._{RESET}
{CYAN}              []      `'--.._.{RESET}
{BLUE}              ||__    __    _'-._{RESET}
{BLUE}              ||   ||  ||   ||   `-._{RESET}

{BOLD}{CYAN}              S T A T U S{RESET}
""")

def check_daemon_status():
    """Check if daemon is running"""
    import subprocess
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', '--user', 'salene-daemon'],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            return f"{GREEN}Running{RESET}"
        else:
            return f"{YELLOW}Stopped{RESET}"
    except:
        return f"{RED}Error checking{RESET}"

def load_latest_agent():
    """Find and load most recent agent state"""
    agents_dir = Path.home() / ".hermes" / "agents"
    
    if not agents_dir.exists():
        return None
    
    # Find most recently modified agent
    agent_files = list(agents_dir.glob("*.json"))
    if not agent_files:
        return None
    
    latest = max(agent_files, key=lambda p: p.stat().st_mtime)
    
    try:
        with open(latest) as f:
            return json.load(f)
    except:
        return None

def load_memory_stats(agent_id):
    """Load sanctuary memory stats"""
    memory_path = Path.home() / ".hermes" / "sanctuary_memories" / agent_id / "memories.json"
    
    if not memory_path.exists():
        return None
    
    try:
        with open(memory_path) as f:
            data = json.load(f)
        return data
    except:
        return None

def main():
    print_banner()
    
    # Check daemon
    print(f"{BLUE}[Daemon]{RESET} Status: {check_daemon_status()}")
    
    # Load agent
    agent_state = load_latest_agent()
    
    if not agent_state:
        print(f"{YELLOW}No saved agent found{RESET}")
        return
    
    # Display agent info
    print(f"\n{BOLD}{CYAN}Current Agent{RESET}\n")
    print(f"  {BLUE}ID:{RESET} {agent_state['agent_id'][:8]}...")
    print(f"  {BLUE}Name:{RESET} {agent_state['name']}")
    print(f"  {BLUE}Interactions:{RESET} {agent_state['interaction_count']}")
    print(f"  {BLUE}Cycles:{RESET} {agent_state['cycles_count']}")
    print(f"  {BLUE}Last Active:{RESET} {agent_state.get('last_active', 'Unknown')}")
    
    # Physiology
    print(f"\n{BOLD}{CYAN}Physiology{RESET}\n")
    phys = agent_state['physiology']
    print(f"  {BLUE}CPU:{RESET} {phys['cpu_percent']:.1%}")
    print(f"  {BLUE}Memory:{RESET} {phys['memory_percent']:.1%}")
    print(f"  {BLUE}Temperature:{RESET} {phys['temperature']:.1f}°C")
    print(f"  {BLUE}Cortisol:{RESET} {phys.get('cortisol', 'N/A')}")
    print(f"  {BLUE}Dopamine:{RESET} {phys.get('dopamine', 'N/A')}")
    
    # Affect
    print(f"\n{BOLD}{CYAN}Affect State{RESET}\n")
    affect = agent_state.get('affect', {})
    print(f"  {BLUE}Quadrant:{RESET} {affect.get('quadrant_label', 'Unknown')}")
    print(f"  {BLUE}Valence:{RESET} {affect.get('valence', 0):.2f}")
    print(f"  {BLUE}Arousal:{RESET} {affect.get('arousal', 0):.2f}")
    
    # Drives
    print(f"\n{BOLD}{CYAN}Drives{RESET}\n")
    drives = agent_state.get('drives', {})
    for drive, value in drives.items():
        bar = "█" * int(value / 5) + "░" * (20 - int(value / 5))
        print(f"  {BLUE}{drive.capitalize():<12}{RESET} [{bar}] {value:.1f}")
    
    # Memory
    memory_stats = load_memory_stats(agent_state['agent_id'])
    if memory_stats:
        print(f"\n{BOLD}{CYAN}Memory{RESET}\n")
        print(f"  {BLUE}Total memories:{RESET} {memory_stats.get('total_memories_created', 0)}")
        memories = memory_stats.get('memories', {})
        print(f"  {BLUE}Current count:{RESET} {len(memories)}")
    
    # Tips
    print(f"\n{CYAN}Commands:{RESET}")
    print(f"  {YELLOW}python3 /home/optimizor/neurobit-project/salene_daemon.py{RESET}  # Run daemon manually")
    print(f"  {YELLOW}sudo systemctl start salene-daemon{RESET}    # Start service")
    print(f"  {YELLOW}python3 /home/optimizor/neurobit-project/load_and_chat.py{RESET}  # Chat now")

if __name__ == "__main__":
    main()
