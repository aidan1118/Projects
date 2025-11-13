# Machine Learning Neural Network Project

This project contains implementations of multilayer neural networks for image classification using two different datasets: Fashion-MNIST and MNIST.

## Project Contents

- **FNist.ipynb**: Fashion-MNIST classification using a dense neural network
- **MNist.ipynb**: MNIST digit classification using a convolutional neural network (CNN)
- **A4.pdf**, **A4P1.pdf**: Project documentation and assignment instructions

## Datasets

### Fashion-MNIST (FNist.ipynb)
- 70,000 grayscale images of 28x28 pixels
- 10 fashion item classes: T-shirt/top, Trouser, Pullover, Dress, Coat, Sandal, Shirt, Sneaker, Bag, Ankle boot
- Dense neural network with 2 hidden layers (300 and 100 neurons)

### MNIST (MNist.ipynb) 
- 70,000 grayscale images of handwritten digits (0-9)
- 28x28 pixel resolution
- Convolutional neural network with Conv2D, MaxPooling, and Dense layers
- Achieved 98.61% test accuracy

## Models

### Fashion-MNIST Model
- **Architecture**: Sequential dense network
- **Layers**: Flatten → Dense(300, ReLU) → Dense(100, ReLU) → Dense(10, Softmax)
- **Optimizer**: SGD with learning rate 0.01
- **Loss**: Sparse categorical crossentropy

### MNIST Model
- **Architecture**: Convolutional neural network
- **Layers**: 
  - Conv2D(32) → MaxPooling2D → Dropout(0.25)
  - Conv2D(64) → MaxPooling2D → Dropout(0.25)
  - Flatten → Dense(128, ReLU) → Dropout(0.5) → Dense(10, Softmax)
- **Optimizer**: Adam
- **Loss**: Categorical crossentropy

## Requirements

```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
```

## Setup and Installation

### Step 1: Check Your Environment
First, verify you have Python 3.13+ installed:
```bash
python3 --version
```

### Step 2: Install Required Packages
If you encounter import errors in VS Code, install the required packages:

```bash
# Option 1: Install to user directory
pip3 install --user --break-system-packages tensorflow numpy matplotlib pandas

# Option 2: If you have a virtual environment in your Projects directory
source /path/to/your/.venv/bin/activate
pip install tensorflow numpy matplotlib pandas
```

### Step 3: Configure VS Code Python Interpreter
If you see import errors like "ModuleNotFoundError: No module named 'tensorflow'":

1. **Open your notebook** (FNist.ipynb or MNist.ipynb)
2. **Look at the top-right corner** - you'll see something like "Python 3.x.x" or ".venv (Python 3.x.x)"
3. **Click on the Python version**
4. **Select the correct interpreter**:
   - If you installed with `--user`: Choose `/opt/homebrew/bin/python3` or `/usr/bin/python3`
   - If you have a `.venv`: Choose the one that shows `.venv` or the path to your virtual environment

### Step 4: Verify Installation
Test that all packages work:
```python
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
print("TensorFlow version:", tf.__version__)
print("All packages imported successfully!")
```

## Usage

1. **Click "Run All"** at the top of the notebook, or run cells sequentially to:
   - Load and preprocess data
   - Build and train the model
   - Evaluate performance
   - Visualize results

## Troubleshooting

### Common Issues

#### "ModuleNotFoundError" for tensorflow, numpy, or matplotlib
- **Cause**: VS Code is using the wrong Python interpreter
- **Solution**: Follow Step 3 above to set the correct Python interpreter

#### VS Code shows ".venv (Python 3.x.x)" but packages are missing
- **Cause**: Virtual environment exists but doesn't have required packages
- **Solution**: Install packages in the virtual environment:
  ```bash
  source /path/to/.venv/bin/activate
  pip install tensorflow numpy matplotlib pandas
  ```

#### TensorFlow import warnings about CPU optimizations
- **Cause**: TensorFlow not compiled with specific CPU optimizations
- **Impact**: None - just informational warnings, models will still train correctly

#### Model training takes a long time
- **Cause**: Neural networks are computationally intensive
- **Solution**: 
  - Reduce epochs or batch size for faster training
  - Or let it run - both models should complete training reasonably quickly

## Results

- **MNIST CNN**: 98.61% test accuracy
- **Fashion-MNIST Dense**: Results vary (training showed gradient explosion issues in later epochs)

## Features

- Data visualization and exploration
- Model architecture summaries
- Training history plots
- Individual prediction examples
- Performance evaluation metrics