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
