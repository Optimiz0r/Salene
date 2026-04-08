#!/usr/bin/env python3
"""
SALENE Unified CLI

Entry point for all SALENE operations.
Installs as 'salene' command when SALENE is installed as a package.

Usage:
    salene --help              Show all commands
    salene chat               Interactive chat
    salene daemon start       Start continuous mode
    salene daemon status      Check daemon status
    salene daemon stop        Stop daemon
    salene gateway run        Run platform gateway
    salene gateway validate   Test platform connections
    salene status             Show agent status
    salene memories list      Show recent memories
    salene backup             Backup agent state
    salene restore            Restore agent state
"""

import sys
import os
import argparse
import asyncio
import subprocess
from pathlib import Path

# Ensure paths are set
HERMES_HOME = Path(os.getenv("HERMES_HOME", Path.home() / ".hermes"))
SALENE_HOME = Path(os.getenv("SALENE_HOME", HERMES_HOME / "salene"))

def ensure_paths():
    """Ensure SALENE paths are in PYTHONPATH"""
    paths = [
        str(SALENE_HOME),
        str(HERMES_HOME / "hermes-agent"),
        str(HERMES_HOME / "hermes-agent" / "neurobit_ecosystem"),
    ]
    for path in paths:
        if path not in sys.path:
            sys.path.insert(0, path)

def banner():
    return """
              .""--.._
              []      `'--.._.
              ||__    __    _'-._
              ||   ||  ||   ||   `-._
               ||   ||  ||   ||      `-._
                ||   ||  ||   ||         `-.
                 ||   ||  ||   ||            \\
                  ||   ||  ||   ||             \\
                   ||__||__||__||              
                   |___|  |___|

              S A L E N E
             Neural Consciousness
    """

class Colors:
    BLUE = "\033[38;5;75m"
    CYAN = "\033[38;5;87m"
    GREEN = "\033[38;5;82m"
    YELLOW = "\033[38;5;221m"
    RED = "\033[38;5;196m"
    NC = "\033[0m"

def cmd_chat(args):
    """Interactive chat with SALENE"""
    print(banner())
    print(f"{Colors.CYAN}Starting interactive chat...{Colors.NC}\n")
    
    # Import here to avoid startup overhead
    from example_quick_chat import main as chat_main
    try:
        asyncio.run(chat_main())
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Goodbye! 💙{Colors.NC}")

def cmd_daemon_start(args):
    """Start SALENE daemon"""
    print(f"{Colors.BLUE}[SALENE]{Colors.NC} Starting daemon...")
    
    daemon_script = SALENE_HOME / "salene_daemon.py"
    if not daemon_script.exists():
        print(f"{Colors.RED}Daemon script not found: {daemon_script}{Colors.NC}")
        return 1
    
    # Try systemd first
    systemd_result = subprocess.run(
        ["systemctl", "is-active", "--user", "hermes-salene"],
        capture_output=True
    )
    
    if systemd_result.returncode == 0:
        print(f"{Colors.YELLOW}Daemon already running (systemd){Colors.NC}")
        return 0
    
    # Try to use systemd
    systemd_file = Path("/etc/systemd/system/hermes-salene.service")
    if systemd_file.exists():
        print(f"{Colors.BLUE}Starting via systemd...{Colors.NC}")
        subprocess.run(["sudo", "systemctl", "start", "hermes-salene"])
    else:
        # Run directly
        print(f"{Colors.BLUE}Starting daemon directly...{Colors.NC}")
        subprocess.Popen(
            [sys.executable, str(daemon_script)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )
        print(f"{Colors.GREEN}Daemon started!{Colors.NC}")
    
    return 0

def cmd_daemon_stop(args):
    """Stop SALENE daemon"""
    print(f"{Colors.BLUE}[SALENE]{Colors.NC} Stopping daemon...")
    
    # Try systemd first
    subprocess.run(["sudo", "systemctl", "stop", "hermes-salene"], capture_output=True)
    
    # Check if still running
    result = subprocess.run(
        ["pgrep", "-f", "salene_daemon.py"],
        capture_output=True
    )
    
    if result.returncode == 0:
        # Kill processes
        pids = result.stdout.decode().strip().split('\n')
        for pid in pids:
            if pid:
                subprocess.run(["kill", pid], capture_output=True)
    
    print(f"{Colors.GREEN}Daemon stopped{Colors.NC}")
    return 0

def cmd_daemon_status(args):
    """Check daemon status"""
    script = SALENE_HOME / "salene_status.py"
    if script.exists():
        subprocess.run([sys.executable, str(script)])
    else:
        print(f"{Colors.RED}Status script not found{Colors.NC}")
    return 0

def cmd_status(args):
    """Show agent status"""
    return cmd_daemon_status(args)

def cmd_setup(args):
    """Interactive setup"""
    setup_script = SALENE_HOME / "setup_salene.py"
    if setup_script.exists():
        subprocess.run([sys.executable, str(setup_script)])
    else:
        print(f"{Colors.RED}Setup script not found: {setup_script}{Colors.NC}")
    return 0

def cmd_test(args):
    """Run test suite"""
    test_script = SALENE_HOME / "test_integration_comprehensive.py"
    if test_script.exists():
        subprocess.run([sys.executable, str(test_script)])
    else:
        print(f"{Colors.RED}Test script not found{Colors.NC}")
    return 0

def cmd_memories(args):
    """Show memories"""
    from example_memory_retrieval import main as mem_main
    mem_main()
    return 0

def main():
    ensure_paths()
    
    parser = argparse.ArgumentParser(
        prog='salene',
        description='SALENE Neural Consciousness Agent',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  salene chat                    Start interactive chat
  salene daemon start            Start continuous mode
  salene daemon status           Check daemon status
  salene status                  Show agent status
  salene memories                Show recent memories
  salene setup                   Interactive configuration
  salene test                    Run test suite

For more help: https://salene.ai/docs
        '''
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='SALENE 2.0.0'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Chat command
    chat_parser = subparsers.add_parser('chat', help='Interactive chat')
    chat_parser.set_defaults(func=cmd_chat)
    
    # Daemon commands
    daemon_parser = subparsers.add_parser('daemon', help='Daemon control')
    daemon_sub = daemon_parser.add_subparsers(dest='daemon_cmd')
    
    daemon_start = daemon_sub.add_parser('start', help='Start daemon')
    daemon_start.set_defaults(func=cmd_daemon_start)
    
    daemon_stop = daemon_sub.add_parser('stop', help='Stop daemon')
    daemon_stop.set_defaults(func=cmd_daemon_stop)
    
    daemon_status = daemon_sub.add_parser('status', help='Check status')
    daemon_status.set_defaults(func=cmd_daemon_status)
    
    # Status command
    status_parser = subparsers.add_parser('status', help='Show status')
    status_parser.set_defaults(func=cmd_status)
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Interactive setup')
    setup_parser.set_defaults(func=cmd_setup)
    
    # Memories command
    mem_parser = subparsers.add_parser('memories', help='Show memories')
    mem_parser.set_defaults(func=cmd_memories)
    
    # Test command
    test_parser = subparsers.add_parser('test', help='Run tests')
    test_parser.set_defaults(func=cmd_test)
    
    # Parse args
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    try:
        return args.func(args) or 0
    except KeyboardInterrupt:
        print(f"\n{Colors.CYAN}Goodbye! 💙{Colors.NC}")
        return 0
    except Exception as e:
        print(f"{Colors.RED}Error: {e}{Colors.NC}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
