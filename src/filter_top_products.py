import pandas as pd
from pathlib import Path
from sklearn.preprocessing import LabelEncoder

# Cargar datos limpios desde el nivel silver
file_path = '../data/silver/ExporteCOL2022_2023_2024_clean.csv'
df = pd.read_csv(file_path)

# Calcular las ventas totales por producto
ventas_por_producto = df.groupby('Código Producto')['Ventas'].sum().reset_index()

# Ordenar productos por ventas en orden descendente
ventas_por_producto = ventas_por_producto.sort_values(by='Ventas', ascending=False)

# Calcular el porcentaje acumulado de ventas
ventas_por_producto['Porcentaje Acumulado'] = ventas_por_producto['Ventas'].cumsum() / ventas_por_producto['Ventas'].sum()

# Definir el umbral de contribución, en este caso, el 80%
umbral_contribucion = 0.80

# Seleccionar solo los productos que representan el 80% de las ventas
productos_principales = ventas_por_producto[ventas_por_producto['Porcentaje Acumulado'] <= umbral_contribucion]

# Filtrar el DataFrame original para incluir solo los productos principales
df_principales = df[df['Código Producto'].isin(productos_principales['Código Producto'])]

# Verificar el tamaño del nuevo conjunto de datos
print("Dimensiones del conjunto de datos filtrado:", df_principales.shape)

# Codificación de variables categóricas
# One-Hot Encoding para variables con pocos valores únicos
df_encoded_principales = pd.get_dummies(df_principales, columns=['Uen', 'Regional', 'Canal Comercial'], drop_first=True)

# Codificación de 'Marquilla' con LabelEncoder
label_encoder = LabelEncoder()
df_encoded_principales['Marquilla'] = label_encoder.fit_transform(df_encoded_principales['Marquilla'])

# Definir el path de salida para el archivo en el nivel gold
clean_file_path = Path('../data/gold/ExporteCOL2022_2023_2024_top_products_encoded.csv')

# Guardar el DataFrame filtrado en el archivo CSV
df_encoded_principales.to_csv(clean_file_path, index=False)
print(f"Archivo guardado en {clean_file_path}")
