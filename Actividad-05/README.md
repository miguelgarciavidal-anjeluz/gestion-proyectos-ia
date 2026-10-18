# Actividad 5 - Design thinking, definiendo e ideando
## Objetivo: 
Realizar la preparación de los datos, el entrenamiento de un modelo y el registro de los resultados.
## Descripción:
El estudiante desarrolla un proyecto aplicado en el que selecciona un dataset público, ya sea de clasificación o regresión, realiza su preparación y versionamiento, entrena un modelo de aprendizaje automático, ajusta hiperparámetros y registra los experimentos utilizando MLflow.

La actividad integra prácticas de gestión de datos para el entrenamiento, así como el entrenamiento y ajuste de modelos, lo que garantiza trazabilidad, reproducibilidad y análisis comparativo de resultados.

## Contexto
Se necesita crear un modelo de Machine Learning para realizar un proceso de clasificación de pacientes con probabilidad de tener diabetes de acuerdo a sus hábitos, historial clínico y estudios de laboratorio.
Para ello es necesario ejecutar algunos experimientos para verificar que modelo de ML es más apto para apoyar a los médicos en identificar los posibles casos de diabetes.
Se realizarán varios experimentos con la ayuda de MLflow con diferentes algoritmos de ML así como de diferentes configuraciones de hiperparámetros.

## Características del Dataset
El conjunto de datos para la predicción de la diabetes es una recopilación de información médica y demográfica de pacientes, junto con su estado respecto a la diabetes (positivo o negativo). Los datos incluyen variables como la edad, el sexo, el índice de masa corporal (IMC), la presencia de hipertensión o enfermedades cardíacas, el historial de tabaquismo, el nivel de HbA1c y el nivel de glucosa en sangre.([Diabetes prediction dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset))

## Estructura del proyecto
El proyecto está estructurada en 3 carpetas. Cada una con una función diferente
* **_data_** - Contiene el dataset que se descarga directamente de la página de Kaggle. (Por limitaciones en Github no es posible cargar el dataset.csv)
* **_src_** - Contiene los programas python con los cuales se realizarán los experimentos. Dentro de esa carpeta se encuentra un **README.md** donde explica más a detalle el funcionamiento de los programas.
* **_results_** - Contiene el resultado del experimento con el reporte de clasificaciones y la matriz de confusión, así como un Reporte Técnico con los hallazgos.

## Proceso del experimento.
1. Cargar el dataset dentro del entorno. Para ello se debe de ejecutar el archivo python `load_dataset.py`
2. Se debe realizar el preprocesamiento del Dataset, para ello se debe de ejecutar el Notebook `preprocess-data.ipynb`. Una vez ejecutado el Notebook se generará un nuevo archivo en la carpeta data con la información limpia y lista para el experimento.
3. Configuración de experimentos. Para ello se cuenta con dos archivos python:
   1. El programa `execute_experiment_logistic_regression.py` tiene la configuración para ejecutar un modelo de regresión logística.
   2. El programa `execute_experiment_random_forest.py` tiene la configuración para ejecutar un modelo de Random Forest.
   
   A cada uno de estos archivos se puede ir adecuando los hiperparámetros de acuerdo a la necesidad o conforme se vaya viendo los resultados. Para ello solo se debe de cambiar el código:
            
        param_grid = {
            "n_estimators": [2000],
            "max_depth": [10],
            "max_features": ["sqrt"],  # ["auto", "sqrt", "log2"]
            "min_samples_split": [10],
            "min_samples_leaf": [10],
            "criterion": ["entropy"],  # ["gini", "entropy"]
        }
        
    Para mayor detalle revisar el archivo **_README_** de la carpeta **src** 
4. Levantar el servidor de **_MLflow_**. Para ello se debe ejecutar en una terminal el comando ` python -m mlflow ui `
5. Una vez levantado el servidor se podrá comenzar la ejecución de los experimentos. Para ello se debera de ejcuetar el comando:

    `python Actividad-05/src/execute_experiment_random_forest.py`

    o

    `python Actividad-05/src/execute_experiment_logistic_regression.py`
6. Para revisar los resultados solo tenemos que entrar a la consola de **_MLflow_**. Para ello solo se debe de entrar a la liga: [http://127.0.0.1:5000/](http://127.0.0.1:5000/) y seleccionar el experimento de _**Diabetes Prediction**_

