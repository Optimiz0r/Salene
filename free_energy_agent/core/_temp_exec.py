    async def _execute_action(self, action):
        action_type = action.get('type', 'respond')
        if action_type == 'respond':
            return action.get('content', '[No response]')
        elif action_type == 'use_tool':
            phys = self.state.physiology
            pe = self.prediction_error.get('total', 0.0)
            cort = phys.hormone_vector[3]
            dop = phys.hormone_vector[0]
            context = f"[Physiological] Error: {pe:.2f}, Cortisol: {cort:.2f}, Dopamine: {dop:.2f}"
            try:
                result = self.hermes_agent.run_conversation(
                    user_message=action.get('input', ''),
                    system_message=context,
                )
                return result.get('final_response', str(result)) if isinstance(result, dict) else str(result)
            except Exception as e:
                return f"[Error: {e}]"
        return "[Unknown]"
