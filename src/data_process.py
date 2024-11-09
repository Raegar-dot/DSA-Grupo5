import pandas as pd
from pathlib import Path

# Crear el path al archivo de datos en la carpeta bronze
file_path = Path('../data/bronze/ExporteCOL2022_2023_2024conRegional.csv')

# Cargar el archivo CSV en un DataFrame de pandas
df = pd.read_csv(file_path, on_bad_lines='skip', sep=';')

# Mostrar las primeras filas del DataFrame para revisar la estructura
print(df.head())

# Crear una copia del DataFrame original
df_copy = df.copy()

# Realizar las transformaciones en la copia
# Convertir 'Código Producto' a tipo string
df_copy['Código Producto'] = df_copy['Código Producto'].astype(str)

for column in ['Ventas Galones', 'Ventas', 'Utilidad Bruta', 'Costos', 'Margen']:
    if column in df_copy.columns:
        # Convertir la columna a string, gestionando NaN
        df_copy[column] = df_copy[column].astype(str)
        # Reemplazar comas por puntos y eliminar espacios en blanco
        df_copy[column] = df_copy[column].str.replace(',', '.').str.strip()
        # Convertir a tipo float después de limpiar
        df_copy[column] = pd.to_numeric(df_copy[column], errors='coerce')
    else:
        print(f"Advertencia: La columna '{column}' no existe en los datos.")

# Verificar que las conversiones sean correctas
print(df_copy.info())
print(df_copy.describe())

# Excluir filas con margen negativo
df_copy = df_copy[df_copy['Margen'] >= 0]

# Excluir filas que contienen "#DIV/0!" en cualquier columna
df_copy = df_copy.replace("#DIV/0!", float('nan')).dropna()

# Excluir filas donde la columna "Producto" contiene la palabra "KIT"
df_copy = df_copy[~df_copy['Producto'].str.contains('KIT', case=False, na=False)]

# Excluir filas con ventas en galones, ventas en dinero, costos y utilidad brutas negativas
df_copy = df_copy[df_copy['Ventas Galones'] >= 0]
df_copy = df_copy[df_copy['Ventas'] >= 0]
df_copy = df_copy[df_copy['Utilidad Bruta'] >= 0]
df_copy = df_copy[df_copy['Costos'] >= 0]

# Contar cuántas ventas tiene cada producto
ventas_por_producto = df_copy.groupby('Código Producto')['Ventas Galones'].count()

# Identificar los productos con solo una venta
productos_una_venta = ventas_por_producto[ventas_por_producto == 1].index

# Eliminar productos con una única venta de la base de datos
df_copy = df_copy[~df_copy['Código Producto'].isin(productos_una_venta)]

# Verificar que las exclusiones se han realizado correctamente
print(df_copy.info())
print(df_copy.describe())

# Guardar el DataFrame limpio en un nuevo archivo CSV
clean_file_path = Path('../data/silver/ExporteCOL2022_2023_2024_clean.csv')


df_copy.to_csv(clean_file_path, index=False)