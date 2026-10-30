# Notebook_Evaluacion_PLD.ipynb

## Descripción

Notebook para realizar la evaluación de los 2 modelos de ML a implementar para identificar los casos de PLD
dependiendo los datos obtenidos del Dataset
de [IBM AMLSim Example Dataset](https://www.kaggle.com/datasets/anshankul/ibm-amlsim-example-dataset).

## Flujo del Notebook:

- Definición de la clase de apoyo `ModelEvaluator` para realizar la evaluación de cada modelo de ML
- Definición de la clase de apoyo `PLDEvaluatorModels` para realizar la evaluación completa de todos los modelos de
  ML, el objetivo será el campo `IS_FRAUD` del Dataset
- Cargar datasets desde CSV.
- Preparación de los datos de prueba y definición de los modelos a probar.
  - LogisticRegression
  - RandomForest
- Ejecutar el entrenamiento de cada uno de los modelos con el Dataset proporcionado en donde se calculará:
  - Threshold a utilizar para cada modelo.
  - Cálculo de métricas
  - Presentación en forma de tabla comparativa entre modelos.
- Presentación de Matriz de Confusión de cada modelo.
- Presentación de gráfica ROC-AUC comparativa para cada modelo.
- Preparación y ejecución de pruebas A/B entre cada uno de los modelos.
  - RandomForest vs LogisticRegression
- Presentación de tablero con la información recopilada para la comparación entre modelos.
- Selección del mejor modelo e interpretación de Negocio.

## Algoritmos soportados

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
	INIT_BALANCE	IS_FRAUD	TX_AMOUNT	CLIENT_INCOMES	HIST_AMOUNT	INCORPORATION
```

# Notebook DataLoader.ipynb

## Descripción:

- Notebook que cargará los archivos CSV descargados del Dataset para realizar los cruces ente archivos, limpiarlo,
  adecaurlo y completarlo; finalmente creará un nuevo archivo CSV con el compendio final de información.

## Flujo del Notebook:

1) Carga de archivos CSV a un Dataframe de Panda y analisar el contenido.
2) Eliminar las columnas que no aportan información valiosa y los resgistros vacios.
3) Completar información a partir de información random para fines educativos.
4) Eliminar columnas de apoyo y registros vacios.
5) Creación de archivo `resultados.csv` con la información completa y limpia, lista para entenar los modelos de ML.