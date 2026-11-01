# Fase II. Ejecución
Desarrollar una solución técnica completa y desplegable basada en un modelo de ML para la identificación de transacciones Fraudulentas. La solución se contenerizará mediante Docker, validar su funcionamiento en un entorno local y preparar su despliegue en la nube.

La solución contempla la integración entre componentes (frontend y backend) mediante API, asegurando la comunicación funcional del sistema. Asimismo, documenta todo el proceso técnico, incluyendo la construcción del contenedor, la ejecución local, las pruebas realizadas y las estrategias de despliegue en la nube.

## Contexto

Validar mediante un piloto controlado si una solución híbrida de IA puede aumentar la cobertura de monitoreo y reducir el esfuerzo PLD manual manteniendo trazabilidad, capacidad operativa y desempeño de detección dentro de umbrales aprobados.
- Objetivo operativo vigente: liberar 90% del trabajo PLD manual, sujeto a validación en piloto.
- Las metas FP ≤2% y FN ≤1% quedan como hipótesis iniciales hasta definir denominadores y capacidad de alertas.
- Las métricas go/no-go incluirán precisión, recall, FPR, FNR, volumen de alertas y SLA.


## Requisitos

- Python 3.11 o superior
- `pip` actualizado
- ~5 GB libres en disco (modelos entrenados y contenedores)
- Librerías:
 
`````
# Núcleo de notebooks
jupyter
ipykernel
notebook

# Manipulación de datos y visualización
pandas
numpy
matplotlib
scipy
seaborn

# Apificación
fastapi
uvicorn
python-multipart
pickle

# Modelos ML
sklearn
sklearn.ensemble.RandomForestClassifier
sklearn.linear_model.LogisticRegression

`````

## Instalación

### Anaconda / Miniconda

1. Instala [Anaconda](https://www.anaconda.com/download) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

2. Clona o abre el repositorio y abre una terminal en la carpeta elegida.

3. Crea el entorno conda con Python 3.10 y actívalo:

   ```bash
   conda create -n <<nombre>> python=3.10 -y
   conda activate <<nombre>>
   ```
Para salir del entorno cuando termines: `conda deactivate`.

## Generación y pruebas del modelo de ML para PLD

1) Creación del modelo que servirá para la predicción de las transacciones a alertar. Para la creación del modelo se cuentan con dos opciones; ambas opciones crearán sobre la carpeta `models` los modelos con extensión pkl.:
   1) Ejecutar el notebook `Notebook_Evaluacion_PLD.ipynb`.
   2) Ejecutar directamente el archivo python `src/randomForestModelAML.py` mediante el comando: `python randomForestModelAML.py` 
2) Probar el modelo generado. Para ello se deberá de ejecutar el comando: 
   1) `python simulador.py`.
   2) **Importante**: La ejecución de los comandos se deben de realizar desde la raiz del proyecto. La alternativa es adecuar el programa python para recuperar el modelo de ML de la ruta indicada.

## Levantar servicio en local y probar

1) Ejecutar el comando: `uvicorn service:app --reload`, se visualizará algo del siguiente modo:

``
INFO:     Will watch for changes in these directories: ['/xxxx/xxxxx/']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [22089] using WatchFiles
INFO:     Started server process [22091]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
``

   Una vez levantado el servicio se podrá llamar a la API:

- `GET`: http://localhost:8000/
- `POST`: http://localhost:8000/predict
2) Ejecutar el comando: `python src/simuladorClienteAPI.py`


## Generación de contenedor Docker

### Prerequisitos

1) Instalar y levantar el servicio Docker. La forma sensilla para desarrolladores es descargar el software [Docker Desktop](https://www.docker.com/products/docker-desktop/). 

### Creación de contenedor

Para la creación del contenedor se utilizará el archivo `Dockerfile` el cual está configurado para recuperar los elementos a contenizar conforme a la estructura del proyecto. Para ello se deberá de ejecutar el comando:
- `docker build -t modelo_fraude .` 
- **Nota**: El nombre del modelo se puede ajustar.

### Levantar servicio contenerizado.

Para levantar la API que se podrá utilizar para realizar las predicciones se hará uso del comando:

-  `docker run -p 8000:8000 modelo_fraude`
