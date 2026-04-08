    def _update_affect(self, prediction_error):
        affect = self.state.affect
        error_impact = prediction_error['total'] * 0.3
        
        if prediction_error['total'] > 0.5:
            affect.ring_point[0] = max(-1.0, affect.ring_point[0] - error_impact)
            affect.ring_point[1] = max(0.0, min(1.0, affect.ring_point[1] + 0.1))
        else:
            recover_rate = 0.05
            affect.ring_point[0] = min(1.0, affect.ring_point[0] + recover_rate)
        
        # Compute quadrant from ring_point
        x, y = affect.ring_point[0], affect.ring_point[1]
        if x >= 0 and y >= 0:
            affect.quadrant_label = "NE"
            affect.quadrant_index = 1
        elif x < 0 and y >= 0:
            affect.quadrant_label = "NW"
            affect.quadrant_index = 2
        elif x < 0 and y < 0:
            affect.quadrant_label = "SW"
            affect.quadrant_index = 3
        else:
            affect.quadrant_label = "SE"
            affect.quadrant_index = 4
        
        # Update angle
        import numpy as np
        affect.ring_angle = np.arctan2(y, x)
        
        affect.confidence = max(0.0, 1.0 - prediction_error['epistemic'])
        affect.salience = max(0.0, min(1.0, prediction_error['total'] * 2))
