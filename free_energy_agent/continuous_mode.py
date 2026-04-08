"""Continuous Mode - Agent Never Sleeps"""

import asyncio
import os
from datetime import datetime
import random

# Simple sensor reader without psutil
def read_sensors():
    """Read system sensors from /proc"""
    try:
        # CPU from /proc/stat
        with open('/proc/stat', 'r') as f:
            fields = f.readline().split()
            user, system, idle = float(fields[1]), float(fields[3]), float(fields[4])
            total = user + system + idle
            cpu = (user + system) / total if total > 0 else 0
        
        # Memory from /proc/meminfo  
        with open('/proc/meminfo', 'r') as f:
            total = available = None
            for line in f:
                if line.startswith('MemTotal:'): total = float(line.split()[1])
                elif line.startswith('MemAvailable:'): available = float(line.split()[1])
            mem = (total - available) / total if total else 0
        
        # Temperature
        temp = 35.0
        for zone in range(5):
            path = f'/sys/class/thermal/thermal_zone{zone}/temp'
            if os.path.exists(path):
                with open(path, 'r') as f:
                    temp = int(f.read().strip()) / 1000
                    break
        
        return {'cpu': cpu, 'memory': mem, 'temperature': temp}
    except Exception as e:
        return {'cpu': 0.3, 'memory': 0.5, 'temperature': 35.0}

class ContinuousAgentMode:
    """Run agent continuously with real sensors"""
    
    def __init__(self, agent):
        self.agent = agent
        self.running = False
        self.idle_cycles = 0
    
    def update_physiology(self, sensors):
        """Map real sensors to hormones"""
        p = self.agent.state.physiology
        
        # High CPU → stress hormones
        if sensors['cpu'] > 0.5:
            p.hormone_vector[3] = min(1.0, p.hormone_vector[3] + 0.1)  # cortisol
        else:
            p.hormone_vector[3] *= 0.95  # decay
        
        p.cpu_percent = sensors['cpu']
        p.memory_percent = sensors['memory']
        p.temperature = sensors['temperature']
    
    async def run(self, duration_sec=60):
        """Run continuous loop"""
        print(f"[{self.agent.name}] Starting continuous mode...")
        print(f"Real sensors active: CPU, Memory, Temperature")
        self.running = True
        
        start = datetime.now()
        while self.running and (datetime.now() - start).seconds < duration_sec:
            sensors = read_sensors()
            self.update_physiology(sensors)
            
            self.idle_cycles += 1
            if self.idle_cycles % 10 == 0:  # Every 10 cycles
                print(f"[{self.idle_cycles}] CPU={sensors['cpu']:.0%}, "
                      f"Cortisol={self.agent.state.physiology.hormone_vector[3]:.2f}, "
                      f"Temp={sensors['temperature']:.1f}°C")
            
            await asyncio.sleep(1)
        
        self.running = False
        print(f"\nContinuous mode: {self.idle_cycles} cycles complete")
