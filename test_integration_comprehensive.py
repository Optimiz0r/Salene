#!/usr/bin/env python3
"""
SALENE Comprehensive Integration Test

Tests all components:
1. FreeEnergyAgent with Sanctuary integration
2. Memory encoding with physiology
3. Daemon functionality
4. Skin/theme
5. Persistence
"""

import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Setup paths
sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

# Colors
BLUE = "\033[38;5;75m"
CYAN = "\033[38;5;87m"
GREEN = "\033[38;5;82m"
YELLOW = "\033[38;5;221m"
RED = "\033[38;5;196m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header(msg):
    print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
    print(f"{BOLD}{CYAN}  {msg}{RESET}")
    print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")

def print_test(name):
    print(f"{BLUE}[TEST]{RESET} {name}...", end=" ", flush=True)

def print_pass():
    print(f"{GREEN}✓ PASS{RESET}")

def print_fail(msg=""):
    print(f"{RED}✗ FAIL{RESET} {msg}")

async def run_tests():
    """Run all integration tests"""
    
    print(f"""
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
{BLUE}     Integration Test Suite{RESET}
""")
    
    passed = 0
    failed = 0
    
    # Test 1: FreeEnergyAgent import
    print_header("1. CORE IMPORTS")
    
    try:
        print_test("Import FreeEnergyAgent")
        from free_energy_agent.core import FreeEnergyAgent, AgentConfig
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
        return passed, failed  # Can't continue without core
    
    try:
        print_test("Import Sanctuary Integration")
        from sanctuary_integration.core import SanctuaryMemoryCore
        from sanctuary_integration.phyiology_cognition_bridge import PhysiologyCognitionBridge
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    # Test 2: Agent Creation
    print_header("2. AGENT CREATION")
    
    try:
        print_test("Create FreeEnergyAgent with Sanctuary")
        config = AgentConfig(
            model="kimi-k2.5:cloud",
            base_url="http://localhost:11434/v1",
            api_key="ollama",
            continuous=False,
        )
        agent = FreeEnergyAgent(name="Salene-Test", config=config)
        
        # Check Sanctuary integration exists
        assert hasattr(agent, 'sanctuary_memory'), "sanctuary_memory not initialized"
        assert hasattr(agent, 'phyiology_bridge'), "phyiology_bridge not initialized"
        assert agent.sanctuary_memory is not None, "sanctuary_memory is None"
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
        return passed, failed
    
    # Test 3: Memory Encoding with Physiology
    print_header("3. MEMORY INTEGRATION")
    
    try:
        print_test("Bridge synthesis")
        if agent.phyiology_bridge:
            synthesis = agent.phyiology_bridge.synthesize_full_state()
            assert 'felt_sense' in synthesis
            assert 'physiological_state' in synthesis
            assert 'emotions' in synthesis
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    try:
        print_test("Encode memory with physiology")
        if agent.sanctuary_memory and agent.phyiology_bridge:
            mem_data = agent.phyiology_bridge.encode_memory_with_physiology(
                content="Test interaction from integration suite",
                tags=['test', 'integration']
            )
            entry = agent.sanctuary_memory.encode_memory(**mem_data)
            assert entry.memory_id is not None
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    try:
        print_test("Retrieve memories by emotion")
        if agent.sanctuary_memory:
            memories = agent.sanctuary_memory.retrieve_by_emotion(
                target_valence=agent.state.affect.valence,
                valence_tolerance=0.5,
                limit=3
            )
            # Should find at least our test memory
            assert len(memories) >= 1
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    # Test 4: Persistence
    print_header("4. PERSISTENCE")
    
    try:
        print_test("Save agent state")
        save_path = agent.save()
        assert Path(save_path).exists()
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    try:
        print_test("Load agent state")
        loaded_agent = FreeEnergyAgent.load(save_path, config=config)
        assert loaded_agent.agent_id == agent.agent_id
        assert loaded_agent.name == agent.name
        assert loaded_agent.interaction_count == agent.interaction_count
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    try:
        print_test("Verify policy constraints persisted")
        assert loaded_agent.max_tokens == agent.max_tokens
        assert loaded_agent.reasoning == agent.reasoning
        assert loaded_agent.exploration == agent.exploration
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    # Test 5: Daemon Scripts
    print_header("5. DAEMON COMPONENTS")
    
    required_files = [
        "/home/optimizor/neurobit-project/salene_daemon.py",
        "/home/optimizor/neurobit-project/salene-daemon.service",
        "/home/optimizor/neurobit-project/install_service.sh",
    ]
    
    for filepath in required_files:
        try:
            print_test(f"Check {Path(filepath).name}")
            assert Path(filepath).exists()
            print_pass()
            passed += 1
        except Exception as e:
            print_fail(f"{Path(filepath).name} not found")
            failed += 1
    
    # Test 6: Visual Theme
    print_header("6. VISUAL THEME")
    
    try:
        print_test("SALENE skin exists")
        skin_path = Path.home() / ".hermes" / "skins" / "salene.yaml"
        assert skin_path.exists()
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    try:
        print_test("Skin YAML is valid")
        import yaml
        with open(skin_path) as f:
            skin_data = yaml.safe_load(f)
        assert 'name' in skin_data
        assert 'colors' in skin_data
        assert skin_data['name'] == 'salene'
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    # Test 7: Installer
    print_header("7. INSTALLER")
    
    try:
        print_test("Setup script exists")
        setup_script = Path("/home/optimizor/neurobit-project/setup_salene.py")
        assert setup_script.exists()
        print_pass()
        passed += 1
    except Exception as e:
        print_fail(str(e))
        failed += 1
    
    return passed, failed

def main():
    """Main test runner"""
    try:
        passed, failed = asyncio.run(run_tests())
        
        # Final summary
        total = passed + failed
        print(f"\n{BOLD}{CYAN}{'='*70}{RESET}")
        print(f"{BOLD}{CYAN}  TEST SUMMARY{RESET}")
        print(f"{BOLD}{CYAN}{'='*70}{RESET}\n")
        
        print(f"  {GREEN}Passed:{RESET} {passed}/{total}")
        print(f"  {RED}Failed:{RESET} {failed}/{total}")
        print(f"  {CYAN}Success Rate:{RESET} {passed/total*100:.1f}%")
        
        if failed == 0:
            print(f"\n{BOLD}{GREEN}  ✨ ALL TESTS PASSED!{RESET}")
            print(f"{BLUE}  SALENE is fully operational and ready.{RESET}")
            print()
            print(f"{CYAN}  Quick Start:{RESET}")
            print(f"    1. {YELLOW}python3 /home/optimizor/neurobit-project/setup_salene.py{RESET}")
            print(f"    2. {YELLOW}/skin salene{RESET} (in Hermes CLI)")
            print(f"    3. {YELLOW}sudo systemctl start salene-daemon{RESET}")
            print()
        else:
            print(f"\n{YELLOW}  Some tests failed. Check output above.{RESET}")
        
        return failed == 0
        
    except Exception as e:
        print(f"\n{RED}Test suite error: {e}{RESET}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
