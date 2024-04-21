# IMPORT
# imports from utils.py, etc.
import optuna

# Some Model
# takes in an aggregate -> 

# rfc
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import os


strat_shuff_split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

for train_index, test_index in strat_shuff_split.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

clf = RandomForestClassifier(max_depth=2, random_state=0)
clf.fit(X, y)
print(clf.predict([[0, 0, 0, 0]]))

# lda


def objective(trial):
    lr = trial.suggest_float('learning_rate', 1e-5, 0.1)
    model = clf(learning_rate = lr)

study = optuna.create_study(direction='minimize')

# optimize over objective function
study.optimize(objective, n_trials=100)

# results
best_params = study.best_params
best_score = study.best_value

print(f"Best Hyperparameters: {best_params}")
print(f"Best Score: {best_score}")

fig1 = optuna.visualization.plot_slice(study)
fig1.write_image("plot_slice.png")

fig2 = optuna.visualization.plot_param_importances(study)
fig2.write_image("param_importances.png")