# ClassificationTrainer con MLflow y Model Registry

## Descripción

Framework reutilizable para entrenamiento de modelos de clasificación basado en Scikit-Learn y MLflow.

Permite:

- Cargar datasets desde CSV.
- Seleccionar el algoritmo a utilizar.
- Definir la variable objetivo (target).
- Ejecutar validación cruzada K-Fold.
- Realizar ajuste de hiperparámetros con GridSearchCV.
- Registrar experimentos en MLflow.
- Registrar modelos en MLflow Model Registry.
- Promover modelos a Staging y Production.
- Generar artefactos para auditoría y monitoreo.

## Algoritmos soportados

* ### Logistic Regression
  La regresión logística es un algoritmo de aprendizaje supervisado y un método estadístico que se utiliza para predecir
  la probabilidad de que ocurra un evento categórico (por ejemplo, sí o no, enfermo o sano, aprobación o rechazo) a
  partir de una o más variables independientes.
    * Los hyperparametros que se pueden configurar son:
        * **penalty**: Define la técnica de regularización para evitar el sobreajuste:
            * l2 (Ridge): Penaliza los pesos al cuadrado (por defecto).
            * l1 (Lasso): Penaliza el valor absoluto de los pesos y puede llevar algunos a cero (útil para selección de
              características).
            * elasticnet: Combina penalizaciones L1 y L2.
            * none: Sin regularización.
        * **C**: Fuerza inversa de regularización (por defecto 1.0). Valores más pequeños implican una regularización
          más fuerte; valores más grandes reducen o eliminan la penalización.
        * **solver**: El algoritmo matemático utilizado para optimizar la función de pérdida:
            * lbfgs: Por defecto; bueno para conjuntos de datos pequeños y medianos.
            * liblinear: Eficiente para conjuntos de datos pequeños o penalización L1.
            * sag / saga: Buenos para conjuntos de datos grandes.
            * newton-cg: Basado en el método de Newton.
        * **max_iter**: Número máximo de iteraciones permitidas para que los solvers convergentes encuentren la solución
          (por defecto 100).
        * **class_weight**: Maneja conjuntos de datos desbalanceados asignando pesos automáticos a las clases (balanced
          o personalizado).
        * **random_state**: Semilla para controlar la aleatoriedad de los datos o del solver (garantiza
          reproducibilidad).
* ### Random Forest
  Random Forest (o Bosque Aleatorio) es un algoritmo de Machine Learning (aprendizaje automático) que combina múltiples
  árboles de decisión para obtener predicciones más precisas, estables y resistentes al sobreajuste (overfitting) que un
  solo árbol.
    * Los hyperparámetros que se pueden configuirar son:
        * **n_estimators**: Define el número de árboles de decisión en el bosque. Su valor habitual: 100 o más (valores
          entre 100 y 500 suelen ser un buen punto de partida). Entre más árboles mejoran la estabilidad y reducen la
          varianza, pero aumentan el tiempo y costo de entrenamiento.
        * **max_features**: Cantidad máxima de características que se consideran al buscar la mejor división en un nodo.
          Limita el parecido entre los árboles, fomentando la diversidad.
            * sqrt (raíz cuadrada del total de características; valor común por defecto para clasificación).
            * log2 (logaritmo en base 2 del total de características; añade más aleatoriedad).
            * None (usa todas las características en cada división, lo que puede causar sobreajuste).
        * **max_depth**: La profundidad máxima permitida para cada árbol de decisión. El valor habitual es None (los
          árboles crecen hasta que las hojas son puras o tienen menos de min_samples_split muestras) o un valor entre 10
          y 30. Las profundidades muy altas permiten capturar patrones complejos pero aumentan el riesgo de overfitting
          (sobreajuste).
        * **min_samples_split**: Es el número mínimo de muestras necesarias para dividir un nodo interno. Su valor
          habitual: 2 (por defecto) o un rango entre 2 y 10. Los valores más altos hacen que el modelo sea más
          conservador y evitan divisiones en grupos muy pequeños.
        * **min_samples_leaf**: Es el número mínimo de muestras que debe tener un nodo terminal (hoja). El valor
          habitual: 1 (por defecto) o entre 1 y 5 para mejorar la generalización. Actúa como un suavizador del modelo;
          valores mayores evitan que se waislen los valores atípicos (outliers).
        * **bootstrap**: Define si se utilizan muestras de arranque (bootstrap) al construir los árboles. Si es True,
          cada árbol se entrena con un subconjunto aleatorio de los datos con reemplazo, lo que aumenta la diversidad
          del bosque.
        * **n_jobs**: Es la cantidad de núcleos del procesador que se usarán en paralelo. Normalmente se coloca en -1
          (utiliza todos los núcleos disponibles del sistema para acelerar el entrenamiento).

## Dependencias

```bash
pip install pandas numpy scikit-learn mlflow matplotlib seaborn joblib
```

## Inicialización

```python
from classification_trainer_mlflow_registry import ClassificationTrainer

trainer = ClassificationTrainer(
    csv_path='clientes.csv',
    target_column='default',
    model_name='random_forest',
    experiment_name='CreditRisk',
    registered_model_name='CreditRiskModel'
)
```

## Flujo completo

```python
trainer.load_data()

trainer.start_experiment()

trainer.register_dataset_metadata()

trainer.create_model()

trainer.cross_validation(cv=5)

param_grid = {
    'n_estimators': [100, 200, 500],
    'max_depth': [5, 10, 15]
}

trainer.hyperparameter_tuning(param_grid)

trainer.train()

metrics = trainer.evaluate()

trainer.log_confusion_matrix('/path')
trainer.log_classification_report('/path')

trainer.save_and_register_model()

trainer.promote_to_staging()

trainer.end_experiment()
```

## Métricas registradas

- Accuracy
- Precision
- Recall
- F1 Score
- ROC-AUC
- Cross Validation Metrics

## Artefactos generados

- confusion_matrix.png
- classification_report.json
- model.pkl
- Modelo registrado en MLflow Registry

## Estructura esperada del dataset

```text
gender,age,hypertension,heart_disease,smoking_history,bmi,HbA1c_level,blood_glucose_level,diabetes
Female,80.0,0,1,never,25.19,6.6,140,0
Female,54.0,0,0,No Info,27.32,6.6,80,0
```

La columna especificada en target_column será utilizada como variable objetivo. En nuestro caso será **diabetes**

## Recomendaciones futuras

- Pipeline de preprocesamiento
- XGBoost, LightGBM y CatBoost
- Data Drift Monitoring
- MLflow Model Serving
- Integración CI/CD
