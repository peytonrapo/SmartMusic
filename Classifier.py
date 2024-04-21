import numpy as np
from xgboost import XGBClassifier, XGBRegressor

class EEGEnjoymentRegressor:
  """
  A class for predicting enjoyment levels using XGBoost regression based on EEG features.
  """
  def __init__(self):
    # Define model parameters (adjust as needed)
    #self.model = XGBRegressor(n_estimators = 2, learning_rate = 0.3, max_depth = 5, objective = 'reg:squarederror')
    self.model = XGBClassifier(n_estimators = 2, learning_rate = 0.3, max_depth = 5, objective = 'binary:logistic')
    self.X_train_history = None
    self.y_train_history = None 
    
  def fit(self, X_train, y_train = None):
    """
    Train the XGBoost model on EEG data (X) and enjoyment levels (y).

    Args:
      X: A numpy array of shape (n_samples, 5) where each row represents an EEG sample
        with features (delta, theta, alpha, sigma, beta).
      y: A numpy array of shape (n_samples,) containing enjoyment levels (continuous values 0-1).
    """
    # If y_train is not provided, use classifyData to generate labels
    # Implicitly assumes 1 datapoint
    if y_train is None:
      y_train = np.array(self.classifyData(X_train))
    
    if self.X_train_history is None:
      self.X_train_history = X_train
    else: 
      self.X_train_history = np.vstack([self.X_train_history, X_train])
      
    if self.y_train_history is None:
      self.y_train_history = y_train
    else:
      self.y_train_history = np.hstack([self.y_train_history, y_train])
      
    # Train the model
    self.model.fit(self.X_train_history, self.y_train_history)
    
  def classifyData(self, brainData):
    """
    Classify brain data (single sample) and return the predicted enjoyment level.

    Args:
      brainData: A numpy array of shape (5,) representing an EEG sample
        with features (delta, theta, alpha, sigma, beta).

    Returns:
      A float representing the predicted enjoyment level.
    """
    return self.model.predict(brainData)

if __name__ == "__main__":
  pass
