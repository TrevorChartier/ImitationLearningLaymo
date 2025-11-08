ImitationLearningLaymo/   # Root of the project
├── data/                 # Collected dataset
│   ├── images/           # Camera frames
│   └── labels.csv        # Steering commands, timestamps, etc.
│
├── models/               # Trained models
│   └── latest_model.pth  # Example
│
├── src/                  # Python source code
│   ├── __init__.py
│   ├── car_control.py    # Script for neural network driving the car
│   ├── rc_data_collection.py  # Script for manual RC data collection
│   ├── data_collector.py # Class for encapsulating data collection
│   ├── dataset.py        # Dataset handling utilities
│   ├── model.py          # Neural network model definition
│   └── utils.py          # Misc helpers (logging, image save/load, etc.)
│
├── notebooks/            # Jupyter notebooks
│   └── train.ipynb       # Training and experimentation
│
├── requirements.txt      # Python dependencies
├── .gitignore
└── README.md
