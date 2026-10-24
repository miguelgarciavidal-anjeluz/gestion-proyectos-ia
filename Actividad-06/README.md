# Actividad 6
## Objetivo: 
Evaluar y validar modelos mediante métricas y pruebas.
## Descripción:
Se define el problema y el objetivo de evaluación, construye e interpreta la matriz de confusión, calcula métricas clave (exactitud, precisión, recall y F1-score), y ajusta el umbral de decisión, además valida la capacidad de generalización del modelo mediante técnicas estadísticas.

Asimismo, genera e interpreta la curva ROC y el valor AUC, valida el modelo mediante validación cruzada y compara su desempeño con un baseline. Adicionalmente, implementa o describe un escenario de prueba A/B, analiza la significancia estadística de los resultados y registra los experimentos.

Finalmente, organiza los resultados en formato visual y justifica las decisiones técnicas en función del impacto en el contexto seleccionado.
## Contexto
Se necesita crear un modelo de Machine Learning para realizar un proceso de clasificación de pacientes con probabilidad de tener diabetes de acuerdo a sus hábitos, historial clínico y estudios de laboratorio.
Para ello es necesario ejecutar algunos experimientos para verificar que modelo de ML es más apto para apoyar a los médicos en identificar los posibles casos de diabetes.

## Características del Dataset
El conjunto de datos para la predicción de la diabetes es una recopilación de información médica y demográfica de pacientes, junto con su estado respecto a la diabetes (positivo o negativo). Los datos incluyen variables como la edad, el sexo, el índice de masa corporal (IMC), la presencia de hipertensión o enfermedades cardíacas, el historial de tabaquismo, el nivel de HbA1c y el nivel de glucosa en sangre.([Diabetes prediction dataset](https://www.kaggle.com/datasets/iammustafatz/diabetes-prediction-dataset))

## Estructura del proyecto
El proyecto está estructurada en 2 carpetas. Cada una con una función diferente
* **_data_** - Contiene el dataset que se descarga directamente de la página de Kaggle. (Por limitaciones en Github no es posible cargar el dataset.csv)
* **_src_** - Contiene el Notebook con el cual se realizarán los experimentos. Dentro de esa carpeta se encuentra un **README.md** donde explica más a detalle el funcionamiento del Notebook.

## Proceso del experimento .
1. Cargar el dataset dentro del entorno. Para ello se debe de ejecutar el archivo python `load_dataset.py` de la Actividad-05 cambiando el path para dejar el Dataset en la carpeta de data de la Actividad-06
2. Se ejecuta el Notebook para mostrar los resultados.
   