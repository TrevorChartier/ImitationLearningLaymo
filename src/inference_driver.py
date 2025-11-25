import os

from base_driver import BaseDriver
from model import Model

from laymo.car import Car
from laymo.camera_manager import CameraManager

class InferenceDriver(BaseDriver):
    def __init__(self, car: Car, camera: CameraManager, model: Model, data_dir: str):
        super().__init__(car, camera, data_dir)
        self._model = model
        self._expert_override = False
        
        policy_dir = os.path.join(data_dir, "policy")
        self._policy_paths = {
            "labels": os.path.join(policy_dir, "labels.csv"),
            "images": os.path.join(policy_dir, "images")
        }
        self._model_info_filepath = os.path.join(data_dir, "model_id.txt")
        self._setup_policy_data_dir()
    
    def _get_steering(self) -> float:
        key, new_press = self._input_handler.get_key()
        if new_press or self._expert_override:
            # Expert is in control
            self._expert_override = True
            if key == "w":
                self.force_stop()
            elif key == "f":
                # Expert gives back control to policy
                self._expert_override = False
            else:
                return self._get_keyboard_steering_input(key)
            
        # If nothing is returned already, policy is in control
        return self._model.predict(self._latest_camera_frame, float(self._throttle_cmd))
    
    def _log_data(self):
        """Write the current camera frame and steering command."""
        if self._expert_override:
            output_paths = self._expert_paths
        else:
            output_paths = self._policy_paths
        super()._log_data(output_paths)

    def _setup_policy_data_dir(self):
        """Create empty directory and labels file for data collected during policy control"""
        os.makedirs(self._policy_paths["images"], exist_ok=False)
        with open(self._policy_paths["labels"], "a", encoding="utf-8") as f:
            f.write("timestamp, throttle_on, steering_command\n")
            
        with open(self._model_info_filepath, "a", encoding="utf-8") as f:
            f.write(self._model.get_info())
