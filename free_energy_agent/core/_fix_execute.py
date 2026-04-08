import re

with open('free_energy_agent.py', 'r') as f:
    lines = f.readlines()

# Find the elif action_type == 'use_tool': section and replace the context building
output = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Look for "# Build system prompt avoiding f-string complexity" and replace that whole block
    if "# Build system prompt avoiding f-string complexity" in line:
        # Replace this and the next ~20 lines until we hit the try:
        new_block = '''            # PHYSIOLOGY AS CONTROL - Read REAL sensors
            sensors = SystemSensors.read_all()
            cpu_load = sensors['cpu']
            mem_load = sensors['memory']
            temp = sensors['temperature']
            
            # CONSTRAINTS from substrate state (NOT narrative)
            max_tokens = 4000
            reasoning = "full"
            exploration = 0.5
            
            if cpu_load > 0.7:
                max_tokens = 500
                reasoning = "minimal"
                exploration = 0.1
            elif cpu_load > 0.4:
                max_tokens = 2000
                reasoning = "moderate"
                exploration = 0.3
                
            if mem_load > 0.8:
                max_tokens = min(max_tokens, 1000)
                exploration = max(0.0, exploration - 0.2)
                
            if temp > 60:
                max_tokens = 200
                reasoning = "minimal"
                exploration = 0.0
            elif temp > 45:
                max_tokens = min(max_tokens, 1500)
            
            context_parts = [
                "[PHYSIOLOGY IS CONTROL - modifies your cognition]",
                f"Sensors: CPU={cpu_load:.1%} MEM={mem_load:.1%} TEMP={temp:.1f}C",
                f"Policy: tokens={max_tokens} reason={reasoning} explore={exploration:.1f}",
                "",
                "Your physiology CONSTRAINS your thinking:",
                f"- Max {max_tokens} tokens due to CPU load",
                f"- {reasoning} reasoning due to metabolic state", 
                f"- {exploration:.1f} exploration due to memory pressure",
                "",
                "SHOW evidence of constraint modification in your response.",
                "Do not describe constraints - DEMONSTRATE them.",
            ]
            context = "\\n".join(context_parts)
'''
        output.append(new_block)
        
        # Skip until we find "try:"
        i += 1
        while i < len(lines) and 'try:' not in lines[i]:
            i += 1
        continue
    
    output.append(line)
    i += 1

with open('free_energy_agent.py', 'w') as f:
    f.writelines(output)

print("Replaced context building with POLICY CONSTRAINTS")
