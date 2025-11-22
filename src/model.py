"""Wrapper around a ML model steering predictor."""
import time
class Model:
    """Dummy Policy for Now, later will use ML model to predict"""
    
    def __init__(self):
        self._last_pred = 0
        self._curr_sign = 1
    
    def predict(self, img) -> float:
        """Produce a steering prediction from camera image"""
        
        if(abs(self._last_pred) > 1):
            self._curr_sign *= -1
        time.sleep(0.1) # Simulate model latency
        curr_pred = self._last_pred + self._curr_sign * 0.1
        self._last_pred = curr_pred
        return curr_pred
        
        