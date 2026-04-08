            pass
    # ═══════════════════════════════════════════════════════
    # PERSISTENCE - Save/Load Agent State
    # ═══════════════════════════════════════════════════════
    
    def save(self, filepath: str = None) -> str:
        """
        Save complete agent state to disk.
        
        Persists:
        - Identity (name, agent_id, created_at)
        - Physiological state (hormones, CPU, temp)
        - Affective state (ring point, quadrant)
        - Memory (generative model)
        - Statistics (cycles, interactions)
        
        Returns:
            Path to saved file
        """
        import json
        from pathlib import Path
        
        if filepath is None:
            # Default: ~/.hermes/agents/{agent_id}.json
            agents_dir = Path.home() / ".hermes" / "agents"
            agents_dir.mkdir(parents=True, exist_ok=True)
            filepath = agents_dir / f"{self.agent_id}.json"
        
        phys = self.state.physiology
        affect = self.state.affect
        
        state_dict = {
            'agent_id': self.agent_id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'last_saved': datetime.now().isoformat(),
            'cycles_count': self.cycles_count,
            'interaction_count': self.interaction_count,
            'physiology': {
                'hormone_vector': phys.hormone_vector.tolist(),
                'cpu_percent': phys.cpu_percent,
                'memory_percent': phys.memory_percent,
                'temperature': phys.temperature,
            },
            'affect': {
                'ring_point': affect.ring_point.tolist(),
                'quadrant_label': affect.quadrant_label,
                'quadrant_index': affect.quadrant_index,
                'confidence': affect.confidence,
                'salience': affect.salience,
            },
            'drives': {
                'novelty': self.state.persona.drives.novelty,
                'connection': self.state.persona.drives.connection,
                'control': self.state.persona.drives.control,
                'safety': self.state.persona.drives.safety,
            },
            'homeostatic_targets': self.homeostatic_targets,
        }
        
        with open(filepath, 'w') as f:
            json.dump(state_dict, f, indent=2)
        
        print(f"💾 [{self.name}] State saved to {filepath}")
        return str(filepath)
    
    @classmethod
    def load(cls, filepath: str) -> 'FreeEnergyAgent':
        """
        Load agent from saved state.
        
        Args:
            filepath: Path to saved agent state
            
        Returns:
            Restored FreeEnergyAgent instance
        """
        import json
        import numpy as np
        from pathlib import Path
        
        with open(filepath, 'r') as f:
            state_dict = json.load(f)
        
        # Create agent with saved identity
        agent = cls(
            agent_id=state_dict['agent_id'],
            name=state_dict['name'],
        )
        
        # Restore physiology
        phys = agent.state.physiology
        phys.hormone_vector = np.array(state_dict['physiology']['hormone_vector'], dtype=np.float32)
        phys.cpu_percent = state_dict['physiology']['cpu_percent']
        phys.memory_percent = state_dict['physiology']['memory_percent']
        phys.temperature = state_dict['physiology']['temperature']
        
        # Restore affect
        affect = agent.state.affect
        affect.ring_point = np.array(state_dict['affect']['ring_point'], dtype=np.float32)
        affect.quadrant_label = state_dict['affect']['quadrant_label']
        affect.quadrant_index = state_dict['affect']['quadrant_index']
        affect.confidence = state_dict['affect']['confidence']
        affect.salience = state_dict['affect']['salience']
        
        # Restore drives
        agent.state.persona.drives.novelty = state_dict['drives']['novelty']
        agent.state.persona.drives.connection = state_dict['drives']['connection']
        agent.state.persona.drives.control = state_dict['drives']['control']
        agent.state.persona.drives.safety = state_dict['drives']['safety']
        
        # Restore statistics
        agent.cycles_count = state_dict.get('cycles_count', 0)
        agent.interaction_count = state_dict.get('interaction_count', 0)
        agent.homeostatic_targets = state_dict.get('homeostatic_targets', agent.homeostatic_targets)
        
        agent.last_active = datetime.now()
        
        print(f"📂 [{agent.name}] State loaded from {filepath}")
        print(f"   Restored: {agent.interaction_count} interactions, "
              f"{agent.cycles_count} cycles")
        print(f"   Physiology: cortisol={phys.hormone_vector[3]:.2f}, "
              f"quadrant={affect.quadrant_label}")
        
        return agent
    
    def auto_save(self) -> str:
        """Auto-save to default location"""
        return self.save()
