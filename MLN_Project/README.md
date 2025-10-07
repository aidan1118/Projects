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

## Usage

1. Open either notebook in Jupyter or Google Colab
2. Run cells sequentially to:
   - Load and preprocess data
   - Build and train the model
   - Evaluate performance
   - Visualize results

## Results

- **MNIST CNN**: 98.61% test accuracy
- **Fashion-MNIST Dense**: Results vary (training showed gradient explosion issues in later epochs)

## Features

- Data visualization and exploration
- Model architecture summaries
- Training history plots
- Individual prediction examples
- Performance evaluation metrics