# End-to-End Behavioral Cloning for Autonomous Driving
**A deep learning-based autonomous driving system running locally on embedded hardware.**

https://github.com/user-attachments/assets/520368c8-3ce6-4221-9626-adb5e0731a4e

## Project Overview

This project implements an end-to-end Behavioral Cloning system to control the steering of a scale car. Unlike traditional control methods (PID), this system uses a Deep Convolutional Neural Network (CNN) to map raw camera input directly to steering commands.

The system addresses two major challenges in embedded robotics:

1. Distribution Shift: Addressed using Expert Intervention Learning (EIL).


2. Hardware Latency: Addressed using Pruning, Clustering, and Quantization Aware Training (PCQAT)

### Key Results 

* **4.5x** increase in autonomous driving distance after a single iteration of Expert Intervention Learning.

  <img width="428" height="384" alt="Screenshot 2026-01-02 at 6 33 50 PM" src="https://github.com/user-attachments/assets/2d9834e7-4b65-4b64-90d9-19e9f67a34ef" />

* **9.4x** reduction in model size (665KB → 70KB) using PCQAT optimization.

* **86.08%** test accuracy on the embedded target.

## Hardware Platform

This project builds on a previous project — [LAYMO](
https://github.com/TrevorChartier/LAYMO). Visit this repository for a breakdown of the physical build, wiring diagrams, and the initial PID control implementation.

## Methodology

### 1.   Behavioral Cloning

We utilized behavioral cloning to imitate the driving habits of a human expert. The process involves three steps:

1. **Data Collection**: A human expert teleoperated the car around the track, collecting a dataset of camera images paired with steering commands (state-action pairs).
3. **Training**: A CNN was trained to map these raw input images to the correct steering prediction.

4. **Deployment**: The trained model runs on the car, inferring steering commands from live camera feeds at 57Hz.

### 2. Expert Intervention Learning (EIL)

Imitation learning often fails due to "distribution shift"—where the car drifts to a state it hasn't seen before and crashes. To solve this, we used EIL:

* **Process**: The model drives autonomously until it enters a dangerous state (e.g., about to hit a wall).

* **Intervention**: The human expert overrides the model to correct the trajectory and guide it back to the center.

* **Retraining**: These "correction" samples are added to the dataset, teaching the model specifically how to recover from failures.

### 3. Model Optimization (PCQAT)

To ensure low latency on the Raspberry Pi CPU, we utilized a specific optimization pipeline:


* **Pruning**: 50% sparsity to remove unnecessary connections.

* **Clustering**: Weight sharing using 8 centroids.

* **Quantization**: Converting weights to reduced precision formats.

**Result**: The model size dropped from 665KB to 70KB with a 5.5% gain in accuracy

## Visual Analysis
<img width="700" height="410" alt="saliency" src="https://github.com/user-attachments/assets/2dca013a-75bb-4b51-9029-a176c4e892e4" />

We used Grad-CAM Saliency Maps to debug the model's decision-making. As seen above, the "hot" (yellow) regions indicate places in the image that highly influence the model's prediction. They are often, but not always, found on the tape  line.

## Repository Structure

```
├── models/                     # Contains the trained model files (.tflite)
│
├── notebooks/
│   ├── model_training.ipynb    # Main notebook: Loads data, augments, trains the CNN, and performs PCQAT
│   ├── grad_cam.ipynb          # Generates Saliency Maps
│
├── src/
│   ├── autonomous_run.py      # Entry point for autonomous driving using a trained model
│   ├── rc_data_collection.py  # Entry point for manual expert data collection
│   ├── inference_driver.py    # Handles autonomous driving with expert intervention logic
│   ├── keyboard_driver.py     # Handles manual teleoperation driving logic
│   ├── base_driver.py         # Abstract base class for the control & logging loop
│   ├── model.py               # TFLite model wrapper (preprocessing & inference)
│   ├── input_handler.py       # Non-blocking terminal key reader for car control
│   ├── buffer.py              # Utility for stride-indexed steering history
│   └── run_utils.py           # Hardware initialization and directory management
│
└── README.md
```
