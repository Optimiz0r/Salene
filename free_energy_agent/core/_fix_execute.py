import sys

with open('free_energy_agent.py', 'r') as f:
    lines = f.readlines()

# Find the problematic lines (375-390 approximately)
output = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Look for the problematic context = f""" line
    if 'context = f"""' in line and i > 370:
        # Replace with simpler version using explicit variables
        output.append('            # Build context avoiding f-string nesting issues\n')
        output.append('            phys = self.state.physiology\n')
        output.append('            pe_val = self.prediction_error.get("total", 0.0)\n')
        output.append('            cort_val = phys.hormone_vector[3]\n')
        output.append('            dop_val = phys.hormone_vector[0]\n')
        output.append('            sal_val = self.state.affect.salience\n')
        output.append('            context = "[PHYSIOLOGICAL STATE]\\n" + \\n')
        output.append('                f"Error: {pe_val:.2f}\\n" + \\n')
        output.append('                f"Cortisol: {cort_val:.2f}\\n" + \\n')
        output.append('                f"Dopamine: {dop_val:.2f}\\n" + \\n')
        output.append('                f"Salience: {sal_val:.2d}\\n\\n" + \\n')
        output.append('                "Respond consistently with these constraints."\n')
        
        # Skip the old lines until we reach the try:
        while i < len(lines) and 'try:' not in lines[i]:
            i += 1
        continue
    
    output.append(line)
    i += 1

with open('free_energy_agent.py', 'w') as f:
    f.writelines(output)

print("Fixed f-string issues")
