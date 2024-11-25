import uvicorn
import joblib
import yaml
import pandas as pd
import os
from datetime import datetime, timedelta
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from loguru import logger
import sys

# Crear la carpeta logs si no existe
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar el logger con loguru
logger.add(f"{log_dir}/app.log", rotation="1 week", level="INFO", format="{time} - {level} - {message}", encoding="utf-8")
logger.add(sys.stdout, level="INFO", format="{time} - {level} - {message}")

# Cargar el modelo guardado con joblib
modelo = joblib.load("mejor_modelo.pkl")

# Función para leer el archivo YAML de configuración
def leer_config():
    with open("config.yml", "r") as file:
        config = yaml.safe_load(file)  # Cargar el contenido del archivo YAML
    return config

# Leer el año y mes mínimo desde el archivo de configuración
config = leer_config()

# Definir la estructura de los datos de entrada con Pydantic
class InputData(BaseModel):
    meses_a_proyectar: int  # El número de meses a proyectar
    Uen: str
    Regional: str
    Canal_Comercial: str
    Marquilla: str
    Codigo_Producto: str
    Producto: str

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="API de predicción de Ventas Empresa XYZ DSA Grupo 5",  # Título personalizado
    description="API para realizar predicciones de Ventas a partir de la selección de variables del usuario de la Empresa XYZ",  # Descripción personalizada
    version=config.get("version", "x.x.x")  # Versión personalizada
)



#Cargar el CSV con las mínimas fechas para las predicciones por cada combinación de variables predictoras, este archivo solo cambia, si la base de entrenamiento cambia
min_fechas_df = pd.read_csv('./min_fechas_predicciones.csv')


# Función para encontrar la fecha inicial para realizar las predicciones de acuerdo a la combinación de variables seleccionada por el usuario 
def obtener_fecha_inicio(data: InputData):
    data_filtrada = min_fechas_df[
        (min_fechas_df['Uen'] == data.Uen) &
        (min_fechas_df['Regional'] == data.Regional) &
        (min_fechas_df['Canal Comercial'] == data.Canal_Comercial) &
        (min_fechas_df['Marquilla'] == data.Marquilla) &
        (min_fechas_df['Código Producto'] == int(data.Codigo_Producto)) &
        (min_fechas_df['Producto'] == data.Producto) 
    ]

    # Verificar si hay resultados e insertar la validación en los logs
    if data_filtrada.empty:
        logger.error("No se encontraron datos para la combinación proporcionada")
        logger.error(str(data.Uen) +' '+ str(data.Regional) +' '+ str(data.Canal_Comercial) +' '+ str(data.Marquilla) +' '+ str(data.Codigo_Producto) +' '+ str(data.Producto) )
        raise ValueError("Combinación de variables no encontrada en el CSV")
    
    min_anio = data_filtrada['min_Anio'].values[0]
    min_mes = data_filtrada['min_Mes'].values[0]
    
    fecha_inicio = datetime(min_anio, min_mes, 1)

    return fecha_inicio


# Función para calcular las combinaciones de Año y Mes
def calcular_fechas_inicio(meses_a_proyectar: int , data):
    fechas = []

    fecha_inicial = obtener_fecha_inicio(data)
    logger.info(print(type(fecha_inicial)))
    logger.info(print(fecha_inicial))
    # Calcular las combinaciones de Año y Mes a partir de la fecha mínima de predicción
    for i in range(meses_a_proyectar):
        nueva_fecha = fecha_inicial + timedelta(days=30 * i)  # Aproximación de 30 días por mes
        fechas.append((nueva_fecha.year, nueva_fecha.month))

    return fechas


# Redirigir la ruta raíz (/) a /docs automáticamente
@app.get("/")
async def redirect_to_docs():
    return RedirectResponse(url="/docs")


# Endpoint POST para realizar predicciones
@app.post("/predict/")
async def predict(data: InputData):
    # Calcular las combinaciones de Año y Mes para los meses a proyectar
    fechas = calcular_fechas_inicio(data.meses_a_proyectar,data)

    resultados = []

    # Realizar la predicción para cada combinación de Año y Mes
    for año, mes in fechas:
        # Crear un DataFrame para pasar al modelo
        input_df = pd.DataFrame([{
            "Año": año,
            "Mes": mes,
            "Uen": data.Uen,
            "Regional": data.Regional,
            "Canal Comercial": data.Canal_Comercial,
            "Marquilla": data.Marquilla,
            "Código Producto": data.Codigo_Producto,
            "Producto": data.Producto
        }])

        # Realizar la predicción
        try:
            prediccion = modelo.predict(input_df)
            prediccion_float = float(prediccion[0])

            resultados.append({
                "Año": año,
                "Mes": mes,
                "Ventas": prediccion_float
            })
            # Log del intento y resultado de la predicción
            logger.info(f"Predicción realizada para Año: {año}, Mes: {mes} | Resultado: {prediccion_float}")
        except Exception as e:
            # Log del error si ocurre alguna excepción durante la predicción
            logger.error(f"Error durante la predicción para Año: {año}, Mes: {mes} | Error: {str(e)}")

    # Log del final de la solicitud con los resultados completos
    logger.info(f"Resultado de la predicción: {resultados}")
    
    return {"result": resultados}

# Ejecutar el servidor FastAPI con Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
