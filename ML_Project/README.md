# Machine Learning Project - Retail Store Inventory Analysis

This project analyzes retail store inventory data to predict units sold using machine learning regression techniques.

## Project Contents

- **a3.ipynb**: Main analysis notebook implementing machine learning models
- **retail_store_inventory.csv**: Dataset containing retail store inventory and sales data

## Dataset Overview

The retail store inventory dataset contains 73,100 records with the following features:

### Features
- **Date**: Transaction date
- **Store ID**: Unique store identifier
- **Product ID**: Unique product identifier
- **Category**: Product category (Groceries, Toys, Electronics, Furniture, Clothing)
- **Region**: Geographic region (North, South, East, West)
- **Inventory Level**: Current stock level
- **Units Sold**: Number of units sold (target variable)
- **Units Ordered**: Number of units ordered
- **Demand Forecast**: Predicted demand
- **Price**: Product price
- **Discount**: Discount percentage
- **Weather Condition**: Weather at time of sale
- **Holiday/Promotion**: Binary indicator for promotional periods
- **Competitor Pricing**: Competitor's price for similar products
- **Seasonality**: Seasonal category (Spring, Summer, Autumn, Winter)

## Machine Learning Analysis

### Data Preprocessing
- **Train/Test Split**: 80/20 split (58,480 training, 14,620 testing samples)
- **Feature Selection**: Price, Store ID, Product ID, Inventory Level
- **Target Variable**: Units Sold
- **Scaling**: StandardScaler for numeric features
- **Encoding**: OneHotEncoder for categorical features
- **Final Feature Space**: 27 dimensions after transformation

### Models Implemented

#### 1. Linear Regression
- **Cross-validation MSE**: 7,733.60
- **Test Set R² Score**: 0.3449 (34.49% variance explained)
- Simple baseline model with moderate predictive power

#### 2. Support Vector Regression (SVR)
- **Initial Cross-validation MSE**: 7,813.25
- **Hyperparameter Tuning**: GridSearchCV with 3-fold CV
- **Best Parameters**: 
  - C: 10 (regularization parameter)
  - gamma: 'auto' (kernel coefficient)
  - kernel: 'rbf' (Radial Basis Function)
- **Test Set R² Score**: 0.3441 (34.41% variance explained)

## Key Findings

### Correlation Analysis
- **Strong correlations**:
  - Units Sold ↔ Demand Forecast (0.997)
  - Price ↔ Competitor Pricing (0.994)
  - Inventory Level ↔ Units Sold (0.591)

### Model Performance
- Both Linear Regression and SVR achieved similar performance (~34.4% R²)
- Models explain moderate variance in sales data
- Significant room for improvement with additional features or advanced techniques

## Requirements

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.metrics import r2_score
```

## Usage

1. Load the dataset: `pd.read_csv('retail_store_inventory.csv')`
2. Follow the notebook cells sequentially for:
   - Data exploration and visualization
   - Feature preprocessing and transformation
   - Model training and evaluation
   - Performance comparison

## Future Improvements

- Feature engineering from additional variables
- Advanced ensemble methods (Random Forest, XGBoost)
- Time-series analysis for temporal patterns
- Deep learning approaches for non-linear relationships