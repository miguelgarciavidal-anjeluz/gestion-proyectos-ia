# Actividad 4
## Objetivo: Identificar e implementar el modelo preentrenado más adecuado para un caso de uso específico.

Implementa al menos tres modelos con el siguiente contenido:
* Configuración de GPU.
* Instalación de dependencias.
* Autenticación en Hugging Face Hub.
* Carga de modelos y datasets.
* Pipeline de inferencia.
* Cálculo de métricas (accuracy, precision, recall, F1-score).
* Medición de latencia.
* Tablas o resúmenes.
* Conclusiones parciales.

## Caso de Uso: Contexto de la problemática

Una firma de Diseño Gráfico está buscando implementar una herramienta de inteligencia artificial que les permita agilizar la creación de nuevos contenidos y prototipos para campañas de marketing. La idea es generar varios bocetos para ser presentados y en base al mejor comenzar a generar los diseños de las campañas haciendo los retoques que se vayan necesitando.

## Requisitos

- Python 3.11 o superior
- `pip` actualizado
- ~10 GB libres en disco para los modelos de Hugging Face.
- Contar con credenciales de Hugging Face para poder descargar los modelos.

## Generación de Token de acceso Hugging Face

1. Inicia sesión en tu cuenta en el sitio oficial de Hugging Face.
2. Haz clic en la foto de tu perfil (esquina superior derecha) y selecciona Settings (Configuración).
3. En el menú lateral izquierdo, haz clic en la pestaña Access Tokens.
4. Haz clic en el botón Create new token (o New token).
5. Configura tu credencial asignando los siguientes campos:
	* Name: Un nombre descriptivo para identificar dónde lo usarás (ej. mi_proyecto_ia).
	* Type / Role: Elige el tipo de permiso adecuado:
		* Read: Para descargar modelos públicos o privados y consultar bases de datos.
		* Write: Obligatorio si necesitas subir modelos o modificar tus repositorios.
		* Fine-grained: Permisos específicos por repositorio (recomendado para producción).
6. Haz clic en Generate a token.
7. Copia el token inmediatamente y guárdalo en un lugar seguro. No volverá a mostrarse completo por seguridad.
8. (Opcional) Crea una variable de entorno y resguarda el Token en esta.



