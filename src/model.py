"""Wrapper around a ML model steering predictor."""
import os
import numpy as np
from tflite_runtime.interpreter import Interpreter
from PIL import Image

class Model:
    """Dummy Policy for Now, later will use ML model to predict"""
    def __init__(self, model_path):
        self._model_id =  os.path.basename(os.path.dirname(model_path))
        self._interpreter = Interpreter(model_path=model_path)
        self._interpreter.allocate_tensors()
        self._input_details = self._interpreter.get_input_details()
        self._output_details = self._interpreter.get_output_details()
    
    def predict(self, img: np.ndarray) -> float:
        """Produce a steering prediction from camera image"""
        img_input = self._preprocess(img)
        self._interpreter.set_tensor(self._input_details[0]['index'], img_input)
        
        self._interpreter.invoke()
        pred = self._interpreter.get_tensor(self._output_details[0]['index'])[0] 

        return np.argmax(pred) - 1 # Predictions are [0-2] we need to shift back to steering angles
    
    def get_info(self):
        return self._model_id
        
    def _preprocess(self, img: np.ndarray) -> np.ndarray:
        # Scale down from 640 x 480 pixels to 6x smaller.
        TARGET_SIZE = (80, 60)

        PIL_image = Image.fromarray(img)
        PIL_image_resized = PIL_image.resize(TARGET_SIZE, resample=Image.LANCZOS)
        image_arr = np.array(PIL_image_resized)
        normalized_arr = image_arr / 255.0
        
        img_input = normalized_arr.reshape((1, 60, 80, 3)).astype(np.float32)
        return img_input.astype(np.float32)
        
        