# Notebook_Completo_Evaluacion_Diabetes

## Descripción

Notebook para realizar la evaluación de los 3 modelos de ML a implementar para identificar los casos de diabetes dependiendo los datos clínicos proporcionados.

Permite:

- Definición de la clase de apoyo `ModelEvaluator` para realizar la evaluación de los modelos de ML
- Cargar datasets desde CSV.
- Preparación de los datos de prueba y entrenamiento que serán utilizados.
- Definición de los modelos a probar.
  - LogisticRegression
  - RandomForest
  - SVM
  - Baseline
- Ejecutar el entrenamiento de cada uno de los modelos con el Dataset proporcionado. 
- Cálculo de métricas y presentación en forma de tabla comparativa.
- Generación de Matriz de Confusión de cada modelo.
- Generación de gráfica ROC-AUC sobrepuesta para cada modelo.
- Preparación y ejecución de pruebas A/B entre cada uno de los modelos.
- Tablero con la información recopilada para la comparación entre modelos.
- Selección del mejor modelo e interpretación de Negocio.

## Algoritmos soportados

* ### SVM
  Una Máquina de Vectores de Soporte (SVM, por sus siglas en inglés Support Vector Machine) es un algoritmo de aprendizaje automático supervisado que se utiliza principalmente para problemas de clasificación y, en menor medida, de regresión (SVR).

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
- F1 Score
- ROC-AUC
- Specificity

## Estructura esperada del dataset

```text
gender,age,hypertension,heart_disease,smoking_history,bmi,HbA1c_level,blood_glucose_level,diabetes
Female,80.0,0,1,never,25.19,6.6,140,0
Female,54.0,0,0,No Info,27.32,6.6,80,0
```

La columna especificada en target_column será utilizada como variable objetivo. En nuestro caso será **diabetes**
