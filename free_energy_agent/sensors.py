"""
System Sensors - Read real hardware without psutil dependency

Uses /proc filesystem on Linux for CPU, memory, temperature.
"""

import os
import time

class SystemSensors:
    """Read real system sensors via /proc filesystem"""
    
    @staticmethod
    def get_cpu_percent():
        """Get CPU usage percentage from /proc/stat"""
        try:
            with open('/proc/stat', 'r') as f:
                fields = f.readline().split()
                # fields[0] is 'cpu', fields[1-4] are user, nice, system, idle
                user = float(fields[1])
                nice = float(fields[2])
                system = float(fields[3])
                idle = float(fields[4])
                total = user + nice + system + idle
                return (user + nice + system) / total if total > 0 else 0
        except:
            return 0.0
    
    @staticmethod
    def get_memory_percent():
        """Get memory usage from /proc/meminfo"""
        try:
            with open('/proc/meminfo', 'r') as f:
                mem_total = None
                mem_available = None
                for line in f:
                    if line.startswith('MemTotal:'):
                        mem_total = float(line.split()[1]) * 1024  # convert to bytes
                    elif line.startswith('MemAvailable:'):
                        mem_available = float(line.split()[1]) * 1024
                        break
                
                if mem_total and mem_available:
                    used = mem_total - mem_available
                    return used / mem_total
        except:
            return 0.0
        return 0.0
    
    @staticmethod
    def get_temperature():
        """Get CPU temperature from /sys/class/thermal"""
        try:
            # Try different thermal zone files
            for zone in range(10):
                path = f'/sys/class/thermal/thermal_zone{zone}/temp'
                if os.path.exists(path):
                    with open(path, 'r') as f:
                        temp_millidegrees = int(f.read().strip())
                        return temp_millidegrees / 1000.0  # convert to Celsius
        except:
            pass
        return 35.0  # Default fallback
    
    @classmethod
    def read_all(cls):
        """Read all sensors at once"""
        return {
            'cpu': cls.get_cpu_percent(),
            'memory': cls.get_memory_percent(),
            'temperature': cls.get_temperature(),
        }

# Quick test
if __name__ == "__main__":
    sensors = SystemSensors.read_all()
    print(f"CPU: {sensors['cpu']:.1%}")
    print(f"Memory: {sensors['memory']:.1%}")
    print(f"Temperature: {sensors['temperature']:.1f}°C")
