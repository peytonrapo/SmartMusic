# IMPORT
# imports from utils.py, etc.
import optuna

def objective(trial):
    lr = trial.suggest_float('learning_rate', 1e-5, 0.1)
    model = SomeModel(learning_rate = lr)

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