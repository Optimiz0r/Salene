#!/usr/bin/env python3
"""
Test Integrated Neurobit-Hermes with Kimi k2.5 via Ollama
"""

import sys
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_ecosystem')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent/neurobit_test_harness')

from neurobit_test_harness.core import IntegratedNeurobitAgent

print("=" * 80)
print("🧠 TEST: Neurobit + Hermes + Kimi k2.5 (via Ollama)")
print("=" * 80)
print()

# Use kimi-k2.5 from your Ollama
print("Creating agent with kimi-k2.5:cloud...")
agent = IntegratedNeurobitAgent(
    model="ollama/kimi-k2.5:cloud",  # Your locally running Kimi
    quiet_mode=False,
)
print()
print("✅ Agent initialized with Kimi!")
print()

# Test 1: Neutral
print("-" * 80)
print("Test 1: Simple greeting")
print("-" * 80)
result1 = agent.chat("Hello! Say something brief about yourself.")
print(f"\nResponse: {result1}")
print()

# Test 2: Tool request (Hermes should use terminal or search)
print("-" * 80)  
print("Test 2: Request that should trigger tool usage")
print("-" * 80)
result2 = agent.chat("What files are in the current directory? Use terminal to list them.")
print(f"\nResponse: {result2}")
print()

# Test 3: Urgent (should modulate hormones)
print("-" * 80)
print("Test 3: Urgent request (hormone modulation)")
print("-" * 80)
result3 = agent.run_conversation("URGENT search for all Python files ASAP!")
print(f"\nCortisol: {result3['perception']['hormones'][3]:.2f}")
print(f"Decision: {result3['decision']['action_type']}")
print(f"Response: {result3['response'][:200]}...")
print()

print("=" * 80)
print("✅ Tests complete!")
print("=" * 80)
