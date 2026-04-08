#!/usr/bin/env python3
"""Test Ollama connection directly"""

import openai

client = openai.OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",  # Ollama doesn't check this, but needs something
)

print("Testing Ollama connection...")
try:
    response = client.chat.completions.create(
        model="kimi-k2.5:cloud",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say 'Hello from Ollama' in 5 words or less."},
        ],
    )
    print(f"✅ SUCCESS!")
    print(f"Response: {response.choices[0].message.content}")
except Exception as e:
    print(f"❌ FAILED: {e}")
