from run_utils import run_driver, print_inference_instructions
from inference_driver import InferenceDriver
from model import Model

if __name__ == "__main__":
    model_path = "/home/trevorchartier/Projects/ImitationLearningLaymo/models/005/model.tflite"
    model = Model(model_path)
    run_driver(InferenceDriver, [model], print_inference_instructions)
