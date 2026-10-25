# Notebook_Completo_Evaluacion_Diabetes

## Descripción

Notebook para realizar la evaluación de los 3 modelos de ML a implementar para identificar los casos de diabetes
dependiendo los datos clínicos proporcionados. 

## Flujo del Notebook:

- Definición de la clase de apoyo `ModelEvaluator` para realizar la evaluación de cada modelo de ML
- Definición de la clase de apoyo `DiabetesEvaluatorModels` para realizar la evaluación completa de todos los modelos de ML
- Cargar datasets desde CSV.
- Preparación de los datos de prueba y definición de los modelos a probar.
  - LogisticRegression
  - RandomForest
  - SVM
- Ejecutar el entrenamiento de cada uno de los modelos con el Dataset proporcionado en donde se calculará:
  - Threshold a utilizar para cada modelo.
  - Cálculo de métricas
  - Presentación en forma de tabla comparativa entre modelos.
- Presentación de Matriz de Confusión de cada modelo.
- Presentación de gráfica ROC-AUC comparativa para cada modelo.
- Preparación y ejecución de pruebas A/B entre cada uno de los modelos.
  - RandomForest vs SVM
  - RandomForest vs LogisticRegression
  - LogisticRegression vs SVM
- Presentación de tablero con la información recopilada para la comparación entre modelos.
- Selección del mejor modelo e interpretación de Negocio.

## Algoritmos soportados

* ### SVM
  Una Máquina de Vectores de Soporte (SVM, por sus siglas en inglés Support Vector Machine) es un algoritmo de
  aprendizaje automático supervisado que se utiliza principalmente para problemas de clasificación y, en menor medida,
  de regresión (SVR).

* ### Logistic Regression
  La regresión logística es un algoritmo de aprendizaje supervisado y un método estadístico que se utiliza para predecir
  la probabilidad de que ocurra un evento categórico (por ejemplo, sí o no, enfermo o sano, aprobación o rechazo) a
  partir de una o más variables independientes.

* ### Random Forest
  Random Forest (o Bosque Aleatorio) es un algoritmo de Machine Learning (aprendizaje automático) que combina múltiples
  árboles de decisión para obtener predicciones más precisas, estables y resistentes al sobreajuste (overfitting) que un
  solo árbol.

## Dependencias

```bash
pip install pandas numpy scikit-learn matplotlib seaborn scipy
```

## Métricas a evaluar

- Accuracy
- Precision
- Recall
- F1
- ROC_AUC
- Specificity
- CV_ROC_AUC_MEAN
- CV_ROC_AUC_STD

## Estructura esperada del dataset

```text
gender,age,hypertension,heart_disease,smoking_history,bmi,HbA1c_level,blood_glucose_level,diabetes
Female,80.0,0,1,never,25.19,6.6,140,0
Female,54.0,0,0,No Info,27.32,6.6,80,0
```
