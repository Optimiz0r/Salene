    # FIX 1: _update_affect needs to update ring_point, not valence directly
    def _update_affect(self, prediction_error):
        affect = self.state.affect
        error_impact = prediction_error['total'] * 0.3
        
        # Update ring_point directly (x=valence, y=arousal)
        if prediction_error['total'] > 0.5:
            affect.ring_point[0] = max(-1.0, affect.ring_point[0] - error_impact)
            affect.ring_point[1] = max(0.0, min(1.0, affect.ring_point[1] + 0.1))
        else:
            recover_rate = 0.05
            affect.ring_point[0] = min(1.0, affect.ring_point[0] + recover_rate)
        
        # Recompute quadrant
        x, y = affect.ring_point[0], affect.ring_point[1]
        if x >= 0 and y >= 0:
            affect.quadrant_label, affect.quadrant_index = "NE", 1
        elif x < 0 and y >= 0:
            affect.quadrant_label, affect.quadrant_index = "NW", 2
        elif x < 0 and y < 0:
            affect.quadrant_label, affect.quadrant_index = "SW", 3
        else:
            affect.quadrant_label, affect.quadrant_index = "SE", 4
        
        import numpy as np
        affect.ring_angle = np.arctan2(y, x)
        
        affect.confidence = max(0.0, 1.0 - prediction_error['epistemic'])
        affect.salience = max(0.0, min(1.0, prediction_error['total'] * 2))

    # FIX 2: _execute_action needs explicit variable construction
    async def _execute_action(self, action):
        action_type = action.get('type', 'respond')
        
        if action_type == 'respond':
            return action.get('content', '[No response]')
        
        elif action_type == 'use_tool':
            phys = self.state.physiology
            pe_val = self.prediction_error.get('total', 0.0)
            cort_val = phys.hormone_vector[3]
            dop_val = phys.hormone_vector[0]
            sal_val = self.state.affect.salience
            
            context = (
                "[PHYSIOLOGICAL STATE]\n" +
                f"Error: {pe_val:.2f}\n" +
                f"Cortisol: {cort_val:.2f}\n" +
                f"Dopamine: {dop_val:.2f}\n" +
                f"Salience: {sal_val:.2f}\n\n" +
                "Respond consistently with these constraints."
            )
            
            try:
                result = self.hermes_agent.run_conversation(
                    user_message=action.get('input', ''),
                    system_message=context,
                )
                if isinstance(result, dict):
                    return result.get('final_response', str(result))
                return str(result)
            except Exception as e:
                return f"[Action failed: {e}]"
        
        elif action_type == 'rest':
            self.state.physiology.cpu_percent *= 0.5
            return "[Resting...]"
        
        return "[Unknown action type]"
