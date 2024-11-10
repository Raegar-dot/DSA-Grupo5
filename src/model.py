# Importar las librerías necesarias
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd

# Configurar la URI de seguimiento de MLflow
mlflow.set_tracking_uri("http://34.235.166.100:8050")

# Configurar el nombre del experimento
mlflow.set_experiment("Proyecto_Prediccion_Ventas")

# Cargar los datos
file_path = '../data/gold/ExporteCOL2022_2023_2024_top_products_encoded.csv'
df = pd.read_csv(file_path)

# Separar las variables predictoras y la variable objetivo
X = df.drop(columns=['Ventas', 'Código Producto', 'Producto'])  # Excluye las columnas que no son predictoras
y = df['Ventas']

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Configuración del modelo
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Iniciar el experimento en MLflow
with mlflow.start_run():
    # Entrenar el modelo
    model.fit(X_train, y_train)

    # Realizar predicciones
    y_pred = model.predict(X_test)

    # Calcular métricas de rendimiento
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Registrar el modelo y las métricas en MLflow
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("MSE", mse)
    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("R2", r2)

    # Guardar el modelo en MLflow
    mlflow.sklearn.log_model(model, "RandomForestRegressor_Modelo_Ventas")

    print(f"MSE: {mse}")
    print(f"MAE: {mae}")
    print(f"R2 Score: {r2}")

print("Modelo registrado y métricas guardadas en MLflow.")
