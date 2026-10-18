from classification_trainer_mlflow_registry import (
    ClassificationTrainer
)

result_path = 'Actividad-05/results/'

trainer = ClassificationTrainer(
    csv_path="Actividad-05/data/diabetes_prediction_dataset_clean.csv",
    target_column="diabetes",
    model_name="random_forest",
    experiment_name="Diabetes Prediction",
    registered_model_name="DiabetesPredictionModel",
    tracking_uri="http://127.0.0.1:5000"
)

trainer.create_model()
trainer.load_data()

trainer.start_experiment()

trainer.register_dataset_metadata()

trainer.create_model()

print(
    trainer.cross_validation(cv=3)
)

param_grid = {
    "n_estimators": [2000],
    #"max_depth": [20],
    "max_features": ["sqrt"],  # ["sqrt", "log2"]
    "min_samples_split": [20],
    "min_samples_leaf": [2],
    "criterion": ["entropy"],  # ["gini", "entropy"]
}

trainer.hyperparameter_tuning(
    param_grid=param_grid,
    cv=3
)

trainer.train()

metrics = trainer.evaluate()

print(metrics)

trainer.log_confusion_matrix(result_path=result_path)

trainer.log_classification_report(result_path=result_path)

trainer.save_and_register_model()

trainer.promote_to_staging()

trainer.end_experiment()
