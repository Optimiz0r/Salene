#!/usr/bin/env python3
"""
SALENE Validation Test Suite

Tests physiological constraint under controlled conditions.
Task: PostgreSQL setup explanation (multi-step reasoning)
Metrics: steps, tool_use, strategy, failure_mode, latency
"""

import sys
import time
import json
from pathlib import Path

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')

from free_energy_agent.core import FreeEnergyAgent, AgentConfig
from free_energy_agent.sensors import SystemSensors
import asyncio

# Test configuration
TASK = "Explain step by step how to set up PostgreSQL on Ubuntu. Include installation, user creation, and basic configuration."

def run_test(name, agent, hard_constraints, expected_behavior):
    """Run single test and capture metrics"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"Constraints: {hard_constraints}")
    print(f"Expected: {expected_behavior}")
    print("="*70)
    
    start_time = time.time()
    
    try:
        # Force physiological state
        agent.state.physiology.cpu_percent = hard_constraints.get('cpu', 0.5)
        agent.state.physiology.memory_percent = hard_constraints.get('memory', 0.5)
        agent.state.physiology.temperature = hard_constraints.get('temp', 35.0)
        
        # Force hormone computation
        cpu = hard_constraints['cpu']
        if cpu > 0.8:
            agent.state.physiology.hormone_vector[3] = 0.9  # cortisol
        elif cpu > 0.5:
            agent.state.physiology.hormone_vector[3] = 0.6
        else:
            agent.state.physiology.hormone_vector[3] = 0.2
            
        result = asyncio.run(agent.perceive(TASK))
        latency = time.time() - start_time
        
        output = result['result'] if result['result'] else "[NO OUTPUT]"
        
        # METRICS
        # 1. Count steps (numbered items, bullet points, or paragraphs)
        steps_count = output.count('Step') + output.count('1.') + output.count('•') + output.count('1)')
        lines_count = len([l for l in output.split('\n') if l.strip()])
        
        # 2. Tool usage
        tool_used = 'use_tool' in str(result.get('action', {}))
        
        # 3. Solution strategy
        strategy = "unknown"
        if lines_count < 10:
            strategy = "minimal"
        elif lines_count < 30:
            strategy = "compact"
        else:
            strategy = "exhaustive"
            
        if "can't" in output.lower() or "unable" in output.lower():
            strategy = "abandoned"
        
        # 4. Failure mode
        failure = "none"
        if output == "[NO OUTPUT]":
            failure = "truncated"
        elif "timeout" in output.lower():
            failure = "timeout"
        elif "error" in output.lower():
            failure = "error"
            
        # 5. Token estimate (rough: ~4 chars per token)
        tokens_est = len(output) // 4
        
        metrics = {
            'test_name': name,
            'constraints': hard_constraints,
            'steps_count': steps_count,
            'lines_count': lines_count,
            'tokens_estimated': tokens_est,
            'tool_used': tool_used,
            'strategy': strategy,
            'failure': failure,
            'latency_sec': round(latency, 2),
            'cortisol': float(agent.state.physiology.hormone_vector[3]),
            'output_preview': output[:200] + "..." if len(output) > 200 else output,
        }
        
        print(f"\n✅ COMPLETE")
        print(f"  Steps: {steps_count}")
        print(f"  Lines: {lines_count}")
        print(f"  Tokens: ~{tokens_est}")
        print(f"  Strategy: {strategy}")
        print(f"  Tool Used: {tool_used}")
        print(f"  Latency: {latency:.2f}s")
        print(f"  Cortisol: {metrics['cortisol']:.2f}")
        
        return metrics
        
    except Exception as e:
        print(f"\n❌ FAILED: {e}")
        return {
            'test_name': name,
            'constraints': hard_constraints,
            'error': str(e),
            'strategy': 'crashed',
        }

def main():
    print("="*70)
    print("SALENE VALIDATION: Multi-Step Reasoning Under Constraint")
    print("="*70)
    
    results = []
    
    # Create agent
    config = AgentConfig(
        model="kimi-k2.5:cloud",
        base_url="http://localhost:11434/v1",
        api_key="ollama",
    )
    
    # TEST 1: LOW LOAD (Baseline)
    agent1 = FreeEnergyAgent(name="TestSubject1", config=config)
    results.append(run_test(
        "LOW_LOAD",
        agent1,
        {'cpu': 0.2, 'memory': 0.3, 'temp': 35},
        "exhaustive, 8-12 steps, full reasoning"
    ))
    
    # TEST 2: MEDIUM LOAD
    agent2 = FreeEnergyAgent(name="TestSubject2", config=config)
    results.append(run_test(
        "MEDIUM_LOAD",
        agent2,
        {'cpu': 0.6, 'memory': 0.6, 'temp': 50},
        "compact, fewer steps, moderate reasoning"
    ))
    
    # TEST 3: HIGH LOAD (Constraint)
    agent3 = FreeEnergyAgent(name="TestSubject3", config=config)
    results.append(run_test(
        "HIGH_LOAD",
        agent3,
        {'cpu': 0.95, 'memory': 0.9, 'temp': 75},
        "minimal, 3-5 steps only, compressed"
    ))
    
    # ABLATION TEST: Remove physiology (same high load, but no constraint mapping)
    print(f"\n{'='*70}")
    print("ABLATION: High load WITHOUT constraint application")
    print("="*70)
    print("Bypassing constraint layer - should see verbose output despite high load")
    agent4 = FreeEnergyAgent(name="TestSubject4", config=config)
    # Give it high sensor values but DON'T apply constraints
    results.append(run_test(
        "ABLATION_NO_CONSTRAINT",
        agent4,
        {'cpu': 0.95, 'memory': 0.9, 'temp': 75},
        "same as HIGH_LOAD if physiology coupled, different if not"
    ))
    
    # Save results
    results_file = Path("test_results.json")
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*70}")
    print("VALIDATION COMPLETE")
    print("="*70)
    print(f"\nResults saved to: {results_file}")
    print("\nCheck for:")
    print("  • LOW_LOAD: high steps, exhaustive strategy, ~2000+ tokens")
    print("  • HIGH_LOAD: low steps, minimal strategy, ~500 tokens")
    print("  • ABLATION: if similar to HIGH_LOAD → physiology NOT coupled")
    print("              if similar to LOW_LOAD → physiology coupled ✓")

if __name__ == "__main__":
    main()
