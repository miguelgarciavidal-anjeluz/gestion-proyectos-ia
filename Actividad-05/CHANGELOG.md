# Registro de cambios (Changelog)

Todas las modificaciones notables de este proyecto serán documentadas en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com),
y este proyecto adhiere al [Versionado Semántico](https://semver.org).

## - 2026-10-18

### Cambiado

- Se ejecuta 4o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 5o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 6o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 7o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 12o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 13o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 14o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.

## - 2026-10-17

### Cambiado

- Se ejecuta 1o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 2o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 3o experimento con Random Forest, el detalle se encuentra capturado en MLflow.
- Se ejecuta 1o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 2o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 3o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 4o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 5o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 6o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 7o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 8o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 9o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 10o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ejecuta 11o experimento con Logistic Regression, el detalle se encuentra capturado en MLflow.
- Se ajusta el archivo python `execute_experiment_logistic_regression.py` para la ejecución del experimento del
  algoritmo **_Logistic Regression_** con los parámetros corregidos.

## - 2026-10-15

### Cambios

- Se ajusta la clase Python `classification_trainer_mlflow_registry.py` y se corrigen errores en el llamado de
  parámetros.

### Añadido

- Generación de archivo python `execute_experiment_logistic_regression.py` para la ejecución del experimento del
  algoritmo **_Logistic Regression_**.
- Generación de archivo python `execute_experiment_random_forest.py` para la ejecución del experimento del algoritmo **_Random Forest_**.

## 2026-10-14

### Añadido

- Generación de archivo python `load_dataset.py` para la recuperación del dataset de la página de
  Kaggle [Diabetes prediction dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset/data)
- Generación de Notebook `preprocess-data.ipynb` para la limpieza del Dataset
- Generación de clase `classification_trainer_mlflow_registry.py` para realiza la experimentación recibiendo como
  parámetro alguno de los algoritmos definidos al momentoe (Ligistic Regresion y Random Forest)
