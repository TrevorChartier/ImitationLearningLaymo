from run_utils import run_driver, print_inference_instructions
from inference_driver import InferenceDriver
from model import Model

if __name__ == "__main__":
    model = Model("/home/trevorchartier/Projects/ImitationLearningLaymo/model/bc_car_model_pqcat.keras")
    run_driver(InferenceDriver, [model], print_inference_instructions)
