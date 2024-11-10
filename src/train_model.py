# Importa librerías necesarias
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

# Configura la URI de seguimiento de MLflow
mlflow.set_tracking_uri("http://34.235.166.100:8050")

# Configura el nombre del experimento
mlflow.set_experiment("Proyecto_Prediccion_Ventas")

# Carga los datos
file_path = '../data/gold/ExporteCOL2022_2023_2024_top_products_encoded.csv'
df = pd.read_csv(file_path)

# Separa las variables predictoras y la variable objetivo
X = df.drop(columns=['Ventas', 'Código Producto', 'Producto'])
y = df['Ventas']

# Divide los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Lista de modelos a probar
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
}

# Entrena y evalúa cada modelo
for model_name, model in models.items():
    with mlflow.start_run(run_name=model_name):
        # Entrena el modelo
        model.fit(X_train, y_train)

        # Realiza predicciones
        y_pred = model.predict(X_test)

        # Calcula métricas de rendimiento
        mse = mean_squared_error(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        # Registra parámetros, métricas y el modelo en MLflow
        mlflow.log_param("model_name", model_name)
        mlflow.log_metric("MSE", mse)
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("R2", r2)
        
        # Guarda el modelo en MLflow
        mlflow.sklearn.log_model(model, model_name)

        print(f"{model_name} - MSE: {mse}, MAE: {mae}, R2 Score: {r2}")

print("Modelos registrados y métricas guardadas en MLflow.")
