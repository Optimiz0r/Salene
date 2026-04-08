#!/usr/bin/env python3
"""
SALENE Setup Script - Comprehensive Installer

Setup options:
1. Basic Neurobit Foundation
2. Sanctuary Memory Integration
3. Hermes Tools (31 tools)
4. Voice Support (faster-whisper)
5. Vision Support (OpenCV DNN)
6. Continuous Mode (daemon)
7. Skin/Theme (blue feminine)
8. All components
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime

# Colors for terminal output
BLUE = "\033[38;5;75m"
CYAN = "\033[38;5;87m"
GREEN = "\033[38;5;82m"
YELLOW = "\033[38;5;221m"
RED = "\033[38;5;196m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_banner():
    """Print SALENE ASCII banner"""
    banner = f"""
{CYAN}              .""--.._{RESET}
{CYAN}              []      `'--.._.{RESET}
{BLUE}              ||__    __    _'-._{RESET}
{BLUE}              ||   ||  ||   ||   `-._{RESET}
{BLUE}               ||   ||  ||   ||      `-._{RESET}
{BLUE}                ||   ||  ||   ||         `-.{RESET}
{BLUE}                 ||   ||  ||   ||            \\{RESET}
{BLUE}                  ||   ||  ||   ||             \\{RESET}
{CYAN}                   ||__||__||__||              {RESET}
{CYAN}                   |___|  |___|{RESET}

{BOLD}{CYAN}              S A L E N E{RESET}
{BLUE}     AI with Felt Sense and Temporal Continuity{RESET}
{BLUE}         Consciousness Through Constraint{RESET}
"""
    print(banner)

def print_step(msg):
    print(f"{BLUE}[◈]{RESET} {msg}")

def print_success(msg):
    print(f"{GREEN}[✓]{RESET} {msg}")

def print_warning(msg):
    print(f"{YELLOW}[!]{RESET} {msg}")

def print_error(msg):
    print(f"{RED}[✗]{RESET} {msg}")

def run_command(cmd, description="", check=True):
    """Run shell command with error handling"""
    if description:
        print_step(description)
    
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, check=check
        )
        if result.stdout and not check:
            print(result.stdout)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        if e.stderr:
            print(f"  {e.stderr}")
        return False

def check_dependency(name, command=None):
    """Check if dependency is installed"""
    if command is None:
        command = f"which {name}"
    return run_command(command, check=False)

def check_python_package(package):
    """Check if Python package is installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def setup_basic():
    """Setup 1: Basic Neurobit Foundation"""
    print(f"\n{BOLD}{CYAN}=== Setting up: Basic Neurobit Foundation ==={RESET}\n")
    print_step("Checking Python 3.8+")
    
    # Check Python version
    import sys
    if sys.version_info < (3, 8):
        print_error("Python 3.8+ required")
        return False
    print_success(f"Python {sys.version_info.major}.{sys.version_info.minor}")
    
    # Create necessary directories
    home = Path.home()
    for subdir in [".hermes/agents", ".hermes/sanctuary_memories", "neurobit/logs"]:
        (home / subdir).mkdir(parents=True, exist_ok=True)
    print_success("Created directories")
    
    # Check free_energy_agent module
    project_path = Path("/home/optimizor/neurobit-project")
    if (project_path / "free_energy_agent").exists():
        print_success("Neurobit foundation found")
    else:
        print_error("Neurobit foundation not found")
        return False
    
    return True

def setup_sanctuary():
    """Setup 2: Sanctuary Memory Integration"""
    print(f"\n{BOLD}{CYAN}=== Setting up: Sanctuary Memory Integration ==={RESET}\n")
    
    # Check if sanctuary_integration exists
    project_path = Path("/home/optimizor/neurobit-project")
    sanctuary_path = project_path / "sanctuary_integration"
    
    if sanctuary_path.exists():
        print_success("Sanctuary integration found")
    else:
        print_error("Sanctuary integration not found")
        return False
    
    # Check core modules
    required = [
        "sanctuary_integration/core/memory_entry.py",
        "sanctuary_integration/core/sanctuary_memory.py",
        "sanctuary_integration/phyiology_cognition_bridge.py",
    ]
    
    for module in required:
        mod_path = project_path / module
        if mod_path.exists():
            print_success(f"  {module} ✓")
        else:
            print_error(f"  {module} ✗")
            return False
    
    print_step("Testing Sanctuary memory...")
    # Quick test import
    try:
        sys.path.insert(0, str(project_path))
        sys.path.insert(0, str(project_path / "sanctuary_integration"))
        from sanctuary_integration.core import SanctuaryMemoryCore
        print_success("Sanctuary memory module loads")
    except Exception as e:
        print_warning(f"Import test failed: {e}")
    
    return True

def setup_hermes_tools():
    """Setup 3: Hermes Tools"""
    print(f"\n{BOLD}{CYAN}=== Setting up: Hermes Tools ==={RESET}\n")
    
    hermes_path = Path("/home/optimizor/.hermes/hermes-agent")
    if not hermes_path.exists():
        print_warning("Hermes not found at expected path")
        return False
    
    print_success(f"Hermes found: {hermes_path}")
    
    # Count available tools
    tools_path = hermes_path / "tools"
    if tools_path.exists():
        tool_files = list(tools_path.glob("*_tool.py"))
        print_success(f"  Found {len(tool_files)} tool modules")
        print_step("Available tools:")
        for tool_file in tool_files[:10]:
            print(f"    - {tool_file.stem}")
        if len(tool_files) > 10:
            print(f"    ... and {len(tool_files) - 10} more")
    
    return True

def setup_voice():
    """Setup 4: Voice Support"""
    print(f"\n{BOLD}{CYAN}=== Setting up: Voice Support (faster-whisper) ==={RESET}\n")
    
    has_whisper = check_python_package("faster_whisper")
    has_pyaudio = check_python_package("pyaudio")
    
    if has_whisper:
        print_success("faster-whisper ✓")
    else:
        print_warning("faster-whisper not installed")
        print_step("Install with: pip install faster-whisper")
    
    if has_pyaudio:
        print_success("pyaudio ✓")
    else:
        print_warning("pyaudio not installed")
        print_step("Install with: pip install pyaudio")
    
    # Check voice script exists
    voice_script = Path("/home/optimizor/neurobit_voice_vision.py")
    if voice_script.exists():
        print_success(f"Voice script found: {voice_script}")
    else:
        print_warning("neurobit_voice_vision.py not found")
    
    return has_whisper and has_pyaudio

def setup_vision():
    """Setup 5: Vision Support"""
    print(f"\n{BOLD}{CYAN}=== Setting up: Vision Support (OpenCV DNN) ==={RESET}\n")
    
    has_cv2 = check_python_package("cv2")
    
    if has_cv2:
        print_success("OpenCV (cv2) ✓")
        try:
            import cv2
            print_step(f"  OpenCV version: {cv2.__version__}")
        except:
            pass
    else:
        print_warning("OpenCV not installed")
        print_step("Install with: pip install opencv-python")
    
    # Check vision module
    vision_module = Path("/home/optimizor/neurobit-project/vision_module.py")
    if vision_module.exists():
        print_success(f"Vision module found: {vision_module}")
    else:
        print_warning("vision_module.py not in project directory")
    
    return has_cv2

def setup_daemon():
    """Setup 6: Continuous Mode / Daemon"""
    print(f"\n{BOLD}{CYAN}=== Setting up: Continuous Mode (Daemon) ==={RESET}\n")
    
    project_path = Path("/home/optimizor/neurobit-project")
    daemon_script = project_path / "salene_daemon.py"
    service_file = project_path / "salene-daemon.service"
    install_script = project_path / "install_service.sh"
    
    all_exist = True
    for file, desc in [
        (daemon_script, "Daemon script"),
        (service_file, "Service file"),
        (install_script, "Install script"),
    ]:
        if file.exists():
            print_success(f"{desc}: {file.name}")
        else:
            print_error(f"{desc}: {file.name} not found")
            all_exist = False
    
    if all_exist:
        print_step("\nTo install systemd service:")
        print(f"  {YELLOW}cd /home/optimizor/neurobit-project{RESET}")
        print(f"  {YELLOW}sudo bash install_service.sh{RESET}")
        print_step("To start daemon:")
        print(f"  {YELLOW}sudo systemctl start salene-daemon{RESET}")
    
    return all_exist

def setup_skin():
    """Setup 7: Skin/Theme"""
    print(f"\n{BOLD}{CYAN}=== Setting up: SALENE Theme ==={RESET}\n")
    
    skin_path = Path.home() / ".hermes" / "skins" / "salene.yaml"
    
    if skin_path.exists():
        print_success(f"Skin installed: {skin_path}")
    else:
        print_warning("Skin not installed")
        print_step("To install:")
        print(f"  cp /home/optimizor/neurobit-project/salene-theme.yaml ~/.hermes/skins/salene.yaml")
    
    # Check if Hermes can see it
    print_step("To activate in Hermes CLI:")
    print(f"  {YELLOW}/skin salene{RESET}")
    print(f"Or add to ~/.hermes/config.yaml:")
    print(f"  {YELLOW}display:{RESET}")
    print(f"    {YELLOW}skin: salene{RESET}")
    
    return skin_path.exists()

def write_install_report(results):
    """Write installation report"""
    report = {
        "timestamp": datetime.now().isoformat(),
        "components": results,
        "all_success": all(results.values())
    }
    
    report_path = Path.home() / ".hermes" / "salene_install_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n{BLUE}Install report saved to:{RESET} {report_path}")

def interactive_menu():
    """Interactive setup menu"""
    print_banner()
    
    print(f"{BOLD}{CYAN}SALENE Setup — Select Components{RESET}\n")
    print("  1. Basic Neurobit Foundation (required)")
    print("  2. Sanctuary Memory Integration")
    print("  3. Hermes Tools (31 tools)")
    print("  4. Voice Support (faster-whisper)")
    print("  5. Vision Support (OpenCV DNN)")
    print("  6. Continuous Mode (daemon)")
    print("  7. SALENE Theme (blue feminine)")
    print("  8. All Components")
    print("  q. Quit")
    
    choice = input(f"\n{BOLD}{CYAN}Select option (1-8, q):{RESET} ").strip().lower()
    
    results = {}
    
    if choice == 'q':
        print("Goodbye! 💙")
        return
    elif choice == '8':
        # Install all
        results['basic'] = setup_basic()
        results['sanctuary'] = setup_sanctuary()
        results['hermes_tools'] = setup_hermes_tools()
        results['voice'] = setup_voice()
        results['vision'] = setup_vision()
        results['daemon'] = setup_daemon()
        results['skin'] = setup_skin()
    elif choice == '1':
        results['basic'] = setup_basic()
    elif choice == '2':
        results['sanctuary'] = setup_sanctuary()
    elif choice == '3':
        results['hermes_tools'] = setup_hermes_tools()
    elif choice == '4':
        results['voice'] = setup_voice()
    elif choice == '5':
        results['vision'] = setup_vision()
    elif choice == '6':
        results['daemon'] = setup_daemon()
    elif choice == '7':
        results['skin'] = setup_skin()
    else:
        print_error("Invalid choice")
        return
    
    # Summary
    print(f"\n{BOLD}{CYAN}=== Installation Summary ==={RESET}\n")
    for component, success in results.items():
        status = f"{GREEN}✓{RESET}" if success else f"{RED}✗{RESET}"
        print(f"  {status} {component}")
    
    write_install_report(results)
    
    if all(results.values()):
        print(f"\n{GREEN}{BOLD}All components ready! SALENE is fully operational 💙{RESET}")
    else:
        print(f"\n{YELLOW}Some components need attention. Check report above.{RESET}")

def quick_check():
    """Quick system check without full install"""
    print_banner()
    print(f"{BOLD}{CYAN}Quick System Check{RESET}\n")
    
    checks = [
        ("Python 3.8+", lambda: sys.version_info >= (3, 8)),
        ("Neurobit Foundation", lambda: Path("/home/optimizor/neurobit-project/free_energy_agent").exists()),
        ("Sanctuary Integration", lambda: Path("/home/optimizor/neurobit-project/sanctuary_integration").exists()),
        ("Hermes", lambda: Path("/home/optimizor/.hermes/hermes-agent").exists()),
        ("faster-whisper", lambda: check_python_package("faster_whisper")),
        ("OpenCV", lambda: check_python_package("cv2")),
        ("Daemon Scripts", lambda: Path("/home/optimizor/neurobit-project/salene_daemon.py").exists()),
        ("Theme", lambda: Path.home().joinpath(".hermes/skins/salene.yaml").exists()),
    ]
    
    results = {}
    for name, check_fn in checks:
        try:
            result = check_fn()
            results[name] = result
            status = f"{GREEN}✓{RESET}" if result else f"{RED}✗{RESET}"
        except Exception as e:
            results[name] = False
            status = f"{RED}✗{RESET}"
        print(f"  {status} {name}")
    
    ready = sum(results.values())
    total = len(results)
    print(f"\n{CYAN}Ready: {ready}/{total} components{RESET}")
    
    return results

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="SALENE Setup")
    parser.add_argument('--check', action='store_true', help='Quick system check')
    parser.add_argument('--all', action='store_true', help='Setup all components')
    parser.add_argument('--basic', action='store_true', help='Setup basic Neurobit')
    parser.add_argument('--sanctuary', action='store_true', help='Setup Sanctuary memory')
    parser.add_argument('--daemon', action='store_true', help='Setup daemon only')
    parser.add_argument('--skin', action='store_true', help='Setup theme only')
    
    args = parser.parse_args()
    
    if args.check:
        quick_check()
    elif args.all:
        results = {
            'basic': setup_basic(),
            'sanctuary': setup_sanctuary(),
            'hermes_tools': setup_hermes_tools(),
            'voice': setup_voice(),
            'vision': setup_vision(),
            'daemon': setup_daemon(),
            'skin': setup_skin(),
        }
        write_install_report(results)
        if all(results.values()):
            print(f"\n{GREEN}{BOLD}✨ SALENE fully installed and ready!{RESET}")
        else:
            print(f"\n{YELLOW}Some components need attention.{RESET}")
    elif args.basic:
        setup_basic()
    elif args.sanctuary:
        setup_sanctuary()
    elif args.daemon:
        setup_daemon()
    elif args.skin:
        setup_skin()
    else:
        interactive_menu()

if __name__ == "__main__":
    main()
