#!/usr/bin/env python3
"""
SALENE with Vision Integration
- Can see through camera
- Vision context added to interactions
"""
import sys
import asyncio
import time
from datetime import datetime

sys.path.insert(0, '/home/optimizor/neurobit-project')
sys.path.insert(0, '/home/optimizor/.hermes/hermes-agent')

from continuous_salene import ContinuousSalene
from vision_module import VisionModule


class SaleneWithVision(ContinuousSalene):
    """SALENE that can see"""
    
    def __init__(self):
        super().__init__()
        self.vision = VisionModule()
        self.vision_enabled = False
        self.last_seen = ""
        
        # Check camera
        available, msg = self.vision.check_camera()
        if available:
            print(f"📷 Vision ready: {msg}")
            self.vision_enabled = True
        else:
            print(f"⚠️  Vision unavailable: {msg}")
    
    async def interact(self, user_input):
        """Interact with vision context"""
        print(f"\n{'='*60}")
        print(f"INTERACTION #{self.agent.interaction_count + 1}")
        print('='*60)
        
        # Capture vision before responding
        vision_context = ""
        if self.vision_enabled:
            print("\n📸 Looking...")
            vision_result = self.vision.capture()
            if vision_result['success']:
                vision_context = vision_result['context']
                self.last_seen = vision_result['image_path']
                print(f"   👁️  {vision_context}")
            else:
                print(f"   ⚠️  Vision: {vision_result['error']}")
        
        # Read sensors (existing)
        from free_energy_agent.sensors import SystemSensors
        sensors = SystemSensors.read_all()
        
        # Calculate constraint (existing)
        cpu_load = sensors['cpu']
        mem_load = sensors['memory']
        temp = sensors['temperature']
        
        if cpu_load > 0.8 or temp > 60:
            max_tokens = 500
        elif cpu_load > 0.5:
            max_tokens = 1500
        else:
            max_tokens = 4000
            
        print(f"   🧠 Token limit: {max_tokens} (CPU: {cpu_load:.0%}, Temp: {temp:.1f}°C)")
        
        # Build enhanced input with vision
        enhanced_input = f"""
[PHYSIOLOGICAL STATE]
Sensors: CPU {cpu_load:.0%} | Memory {mem_load:.0%} | Temp {temp:.1f}°C
Tokens available: {max_tokens}
Idle cycles: {self.idle_cycles}

[VISION INPUT]
{vision_context}

[USER MESSAGE]
{user_input}
"""
        
        # Process through agent
        result = await self.agent.perceive(enhanced_input)
        
        # Output
        output = result['result'] if result['result'] else ""
        actual_tokens = len(output) // 4
        
        print(f"\n🤖 SALENE: {output}")
        if vision_context:
            print(f"\n   [Based on: {vision_context}]")
        print(f"\n[Tokens: {actual_tokens}/{max_tokens}]")
        
        self.idle_cycles = 0
        self.agent.save()
        
        return output
    
    def get_vision_status(self) -> str:
        """Get current vision status"""
        if not self.vision_enabled:
            return "Vision unavailable"
        
        # Quick capture to show status
        result = self.vision.capture(save_path="/tmp/salene_status.jpg")
        if result['success']:
            return f"Vision active - {result['context']}"
        return "Vision error"


def main():
    print("=" * 60)
    print("SALENE WITH VISION")
    print("=" * 60)
    
    salene = SaleneWithVision()
    
    print("\nWhat would you like to do?")
    print("1. Say hello (with vision)")
    print("2. Run continuous mode (60s)")
    print("3. Check vision status")
    
    try:
        choice = input("\nChoice (1/2/3): ").strip()
    except EOFError:
        choice = "1"
    
    if choice == '1':
        msg = input("Your message (or press Enter for default 'hello'): ").strip()
        if not msg:
            msg = "Hello Salene! Can you see me?"
        
        asyncio.run(salene.interact(msg))
        
        # Show the captured image if available
        if salene.last_seen and os.path.exists(salene.last_seen):
            print(f"\n📷 Image saved: {salene.last_seen}")
            
    elif choice == '2':
        asyncio.run(salene.run_continuous(duration_sec=60))
        
    elif choice == '3':
        status = salene.get_vision_status()
        print(f"\nStatus: {status}")
    else:
        print("Invalid choice")


if __name__ == "__main__":
    import os
    main()
