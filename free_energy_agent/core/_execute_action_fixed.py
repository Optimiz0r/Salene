    async def _execute_action(self, action: Dict[str, Any]) -> str:
        """Execute selected action with robust error handling"""
        action_type = action.get('type', 'respond')
        
        if action_type == 'respond':
            return action.get('content', '[No response generated]')
        
        elif action_type == 'use_tool':
            # Build context for Hermes
            phys = self.state.physiology
            context = f"""
[PHYSIOLOGICAL STATE]
Error: {self.prediction_error.get('total', 0.0):.2f}
Cortisol: {phys.hormone_vector[3]:.2f}
Dopamine: {phys.hormone_vector[0]:.2f}
"""
            try:
                result = self.hermes_agent.run_conversation(
                    user_message=action.get('input', ''),
                    system_message=context,
                )
                # Handle different return types
                if isinstance(result, dict):
                    return result.get('final_response', result.get('response', str(result)))
                elif isinstance(result, str):
                    return result
                else:
                    return str(result)
            except Exception as e:
                return f"[Error: {e}]"
        
        elif action_type == 'rest':
            self.state.physiology.cpu_percent *= 0.5
            return "[Resting...]"
        
        return "[Unknown action]"
