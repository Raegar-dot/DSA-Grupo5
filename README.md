# DSA-Grupo5
Repositorio del proyecto de DSA grupo 5 para la predicción de ventas y rentabilidad de la empresa XYZ, utilizando aprendizaje supervisado y visualización de datos.

## Pipeline de Procesamiento de Datos

En este proyecto, hemos implementado un pipeline de procesamiento de datos dividido en tres niveles: **Bronze**, **Silver** y **Gold**. Cada nivel representa una etapa en el flujo de procesamiento de los datos, de modo que cada paso posterior utiliza la versión más refinada y estructurada de los datos.

### Niveles del Pipeline

1. **Bronze**: Contiene los datos crudos o sin procesar. Estos son los datos originales tal como fueron adquiridos, sin ningún tipo de transformación o limpieza.
   - Ubicación: `data/bronze/`
   - Archivo de ejemplo: `ExporteCOL2022_2023_2024conRegional.csv`

2. **Silver**: En este nivel, los datos han sido preprocesados y limpiados. Las transformaciones incluyen la conversión de tipos de datos, eliminación de valores atípicos y ajuste de los campos necesarios para garantizar consistencia.
   - Ubicación: `data/silver/`
   - Archivo de ejemplo: `ExporteCOL2022_2023_2024_clean.csv`

3. **Gold**: Este nivel contiene los datos filtrados y listos para el modelado. Aquí, solo están presentes los productos que representan el 80% de las ventas acumuladas, y cualquier otra limpieza o ajuste específico para los modelos de predicción ha sido aplicado.
   - Ubicación: `data/gold/`
   - Archivo de ejemplo: `ExporteCOL2022_2023_2024_top_products.csv`

### Proceso de Generación de Datos

Para generar los archivos en cada nivel, sigue estos pasos:

1. **Bronze**: Cargar el archivo crudo en `data/bronze/`.
2. **Silver**: Ejecutar el script `data_process.py` en la carpeta `src` para crear el archivo limpio en `data/silver/`.
3. **Gold**: Ejecutar el script `filter_top_products.py` en la carpeta `src` para seleccionar los productos principales y crear el archivo listo para modelado en `data/gold/`.

