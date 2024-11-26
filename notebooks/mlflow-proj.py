#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Importar librerías necesarias
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# Cargar datos limpios
file_path = '../data/silver/ExporteCOL2022_2023_2024_clean.csv'
df = pd.read_csv(file_path)

# Calcular las ventas totales por producto
ventas_por_producto = df.groupby('Código Producto')['Ventas'].sum().reset_index()

# Ordenar productos por ventas descendente
ventas_por_producto = ventas_por_producto.sort_values(by='Ventas', ascending=False)

# Calcular el porcentaje acumulado de ventas
ventas_por_producto['Porcentaje Acumulado'] = ventas_por_producto['Ventas'].cumsum() / ventas_por_producto['Ventas'].sum()

# Definir el umbral de contribución, por ejemplo, el 80% de las ventas
umbral_contribucion = 0.80

# Seleccionar solo los productos que representan el 80% de las ventas
productos_principales = ventas_por_producto[ventas_por_producto['Porcentaje Acumulado'] <= umbral_contribucion]

# Filtrar el DataFrame original para incluir solo los productos principales
df_principales = df[df['Código Producto'].isin(productos_principales['Código Producto'])]

# Verificar el tamaño del nuevo conjunto de datos
print(df_principales.shape)

# Selección de las variables predictoras y la variable objetivo
# X = df_principales[['Año', 'Mes', 'Uen', 'Regional', 'Canal Comercial', 'Marquilla', 'Numérica Clientes', 'Numérica Documentos']]
X = df_principales[['Año', 'Mes', 'Uen', 'Regional', 'Canal Comercial', 'Marquilla', 'Código Producto', 'Producto']]
y = df_principales['Ventas']

# Dividir los datos en entrenamiento y prueba (80%-20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definir columnas categóricas
categorical_features = ['Uen', 'Regional', 'Canal Comercial', 'Marquilla','Código Producto', 'Producto']

# Configurar el preprocesador para las columnas categóricas
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ],
    remainder='passthrough'  # Deja las columnas numéricas sin cambiar
)

xgbmodelo = XGBRegressor(objective='reg:squarederror', random_state=42)

#Importe MLFlow para registrar los experimentos, el regresor de bosques aleatorios y la métrica de error cuadrático medio
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# defina el servidor para llevar el registro de modelos y artefactos
mlflow.set_tracking_uri("http://3.88.216.97:8050")
# registre el experimento
experiment = mlflow.set_experiment("Proyecto_Prediccion_Ventas_3")

# Aquí se ejecuta MLflow sin especificar un nombre o id del experimento. MLflow los crea un experimento para este cuaderno por defecto y guarda las características del experimento y las métricas definidas. 
# Para ver el resultado de las corridas haga click en Experimentos en el menú izquierdo. 
with mlflow.start_run(experiment_id=experiment.experiment_id):
    # defina los parámetros del modelo
    n_estimators = 100
    max_depth = 10
    learning_rate = 0.1
    subsample = 1.0
    colsample_bytree = 1.0

    # Cree el modelo con los parámetros definidos y entrénelo
    model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', XGBRegressor(n_estimators = n_estimators, max_depth = max_depth, learning_rate = learning_rate, subsample = subsample, colsample_bytree=colsample_bytree, objective='reg:squarederror', random_state=42))
    ])
    model.fit(X_train, y_train)

    # Realice predicciones de prueba
    predictions = model.predict(X_test)
  
    # Registre los parámetros
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("maxdepth", max_depth)
    mlflow.log_param("learning_rate", learning_rate)
    mlflow.log_param("subsample", subsample)
    mlflow.log_param("colsample_bytree", colsample_bytree)
  
    # Registre el modelo
    mlflow.sklearn.log_model(model, "xgboost-model")
  
    # Cree y registre la métrica de interés
    r2 = r2_score(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    mlflow.log_metric("r2", r2)
    mlflow.log_metric("mse", mse)
    mlflow.log_metric("mae", mae)
    print(r2)