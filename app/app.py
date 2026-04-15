# Importamos las librerías necesarias
import streamlit as st
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

#Cargamos el modelo entrenado y el codificador de barrios
with open("E:/Archivos vscode/predictor-alquiler-madrid/models/model.pkl", "rb") as f:
    modelo = pickle.load(f)

with open("E:/Archivos vscode/predictor-alquiler-madrid/models/label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

#Título de la aplicación
st.title("Predictor de Alquiler en Madrid")
st.write("Introduce las características del piso para predecir su precio de alquiler.")

# Cargamos los barrios disponibles en el despegable
barrios = list(le.classes_)

#Inputs del usuario
st.subheader("Características del Piso")

#Desplegable para seleccionar el barrio
barrio = st.selectbox("Selecciona el barrio", barrios)

#Slider para seleccionar los metros cuadrados
metros_cuadrados = st.slider("Metros cuadrados", min_value=20, max_value=500, value=80)

#Slider para seleccionar el número de habitaciones
habitaciones = st.slider("Número de habitaciones", min_value=1, max_value=10, value=2)

#Botón para calcular el precio
if st.button("Predecir Precio de Alquiler"):
    #Codificamos el barrio seleccionado por el usuario
    barrio_encoded = le.transform([barrio])[0]
    
    #Creamos un DataFrame con las características del piso
    piso = pd.DataFrame({
        'metros_cuadrados': [metros_cuadrados],
        'habitaciones': [habitaciones],
        'barrio_encoded': [barrio_encoded]
    })
    
    #Realizamos la predicción utilizando el modelo cargado
    precio = modelo.predict(piso)[0]    

    # Mostramos el resultado con más detalle
    st.success(f'El precio estimado de alquiler es: {precio:.0f}€/mes')

    # Mostramos métricas adicionales
    col1, col2 = st.columns(2)
    col1.metric('Precio por metro cuadrado', f'{precio/metros_cuadrados:.0f}€/m²')
    col2.metric('Precio por habitación', f'{precio/habitaciones:.0f}€/hab')


#Sección informativa sobre barrios más caros y baratos
st.subheader("Contexto del Mercado de Alquiler en Madrid")

#Cargamos el dataset para mostrar las estadísticas 
df = pd.read_csv("E:/Archivos vscode/predictor-alquiler-madrid/data/processed/alquiler_madrid_limpio.csv")

#Añadimos dos columnas para mostrar los barrios más caros y más baratos
col1, col2 = st.columns(2)

#Añadimos los 5 barrios más caros
with col1:
    st.markdown("### Barrios más caros")
    top_caros = df.groupby("barrio")["precio_alquiler"].mean().round(0).sort_values(ascending=False).head(5)
    st.dataframe(top_caros)

#Añadimos los 5 barrios más baratos
with col2:
    st.markdown("### Barrios más baratos")
    top_baratos = df.groupby("barrio")["precio_alquiler"].mean().round(0).sort_values(ascending=True).head(5)
    st.dataframe(top_baratos)    


#Creamos gráficos para mostrar la distribución de precios por barrio, la relación entre metros cuadrados y precio, y la relación entre habitaciones y precio
fig, ax = plt.subplots(figsize=(10, 5))

# Boxplot de precio por barrio con seaborn de 10 barrios más representativos   
# Seleccionamos los 10 barrios más representativos por número de registros
top_barrios = df['barrio'].value_counts().head(10).index
df_top_barrios = df[df['barrio'].isin(top_barrios)]

sns.boxplot(x="barrio", y="precio_alquiler", data=df_top_barrios, ax=ax, palette="Set2")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_title("Distribución de precios por barrio más caros")
ax.set_xlabel("Barrio")
ax.set_ylabel("Precio de alquiler (€)")

# Mostramos el gráfico
st.pyplot(fig)

# Creamos un gráfico de los barrios con precio medio mas bajo 
fig0, ax = plt.subplots(figsize=(10, 5))

#Creamos un boxplot de precio por barrio con seaborn de 10 barrios más baratos
low_barrios = df['barrio'].value_counts().tail(10).index
df_low_barrios = df[df['barrio'].isin(low_barrios)]
sns.boxplot(x="barrio", y="precio_alquiler", data=df_low_barrios, ax=ax, palette="Set2")

# Rotamos las etiquetas del eje x para que se vean mejor
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# Asignamos títulos a los ejes y al gráfico
ax.set_title("Distribución de precios por barrio más baratos")
ax.set_xlabel("Barrio")
ax.set_ylabel("Precio de alquiler (€)")

# Mostramos el gráfico
st.pyplot(fig0)

# Dispersión metros cuadrados vs precio
fig1, ax = plt.subplots(figsize=(10, 5))

#Creamos un gráfico de dispersión de metros cuadrados vs precio utilizando seaborn
sns.scatterplot(x="metros_cuadrados", y="precio_alquiler", data=df, ax= ax, alpha=0.3)

# Rotamos las etiquetas del eje x para que se vean mejor
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# Asignamos títulos a los ejes y al gráfico
ax.set_title("Metros cuadrados vs precio")
ax.set_xlabel("Metros cuadrados")
ax.set_ylabel("Precio de alquiler (€)")

# Mostramos el gráfico
st.pyplot(fig1)

# Dispersión habitaciones vs precio
fig2, ax = plt.subplots(figsize=(10, 5))

#Creamos un gráfico de dispersión de habitaciones vs precio utilizando seaborn
sns.scatterplot(x="habitaciones", y="precio_alquiler", data=df, ax=ax, alpha=0.3)
# Rotamos las etiquetas del eje x para que se vean mejor
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_title("Habitaciones vs precio")
ax.set_xlabel("Número de habitaciones")
ax.set_ylabel("Precio de alquiler (€)")
st.pyplot(fig2)

# Histograma de precios
fig3, ax = plt.subplots(figsize=(10, 5))

#Creamos un histograma de precios utilizando seaborn
sns.histplot(df['precio_alquiler'], bins=50, color='#1D9E75', ax=ax)
# Rotamos las etiquetas del eje x para que se vean mejor
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

# Asignamos títulos a los ejes y al gráfico
ax.set_title("Distribución del precio de alquiler")
ax.set_xlabel("Precio de alquiler (€)")
ax.set_ylabel("Frecuencia")

# Mostramos el gráfico
st.pyplot(fig3)

#Dispersión de metros cuadrados y precio coloreada por número de habitaciones
fig4, ax = plt.subplots(figsize=(12, 6))

#Creamos el gráfico de dispersión coloreado por número de habitaciones
scatter = ax.scatter(df['metros_cuadrados'], df['precio_alquiler'], c=df['habitaciones'], cmap='viridis', alpha=0.3, s=10)

# Añadimos una barra de color para indicar el número de habitaciones
plt.colorbar(scatter, ax=ax , label='Número de Habitaciones')

# Asignamos títulos a los ejes y al gráfico
ax.set_title("Relación entre metros cuadrados y precio según número de habitaciones")
ax.set_xlabel("Metros Cuadrados")
ax.set_ylabel("Precio de Alquiler (€)")

# Ajustamos el diseño para que no se solapen los elementos del gráfico
plt.tight_layout()  

# Mostramos el gráfico
st.pyplot(fig4)

#Hacemos la app más visual 
st.set_page_config(
    page_title="Predictor Alquiler Madrid",
    page_icon="🏠",
    layout="wide"
)

#Creamos filtros y una barra lateral para mejorar la experiencia del usuario
st.sidebar.header("🔧 Configuración del piso")

barrio = st.sidebar.selectbox("Barrio", barrios)

metros_cuadrados = st.sidebar.slider(
    "Metros cuadrados", 20, 500, 80
)

habitaciones = st.sidebar.slider(
    "Habitaciones", 1, 10, 2
)

predecir = st.sidebar.button("💰 Predecir")

#Asignamos el dataframe filtrado a una variable para usarlo en las gráficas y métricas posteriores
if predecir:
    barrio_encoded = le.transform([barrio])[0]

    piso = pd.DataFrame({
        'metros_cuadrados': [metros_cuadrados],
        'habitaciones': [habitaciones],
        'barrio_encoded': [barrio_encoded]
    })

    precio = modelo.predict(piso)[0]

    st.subheader("💸 Resultado de la predicción")

    col1, col2, col3 = st.columns(3)

    col1.metric("Precio estimado", f"{precio:.0f} €")
    col2.metric("€/m²", f"{precio/metros_cuadrados:.0f} €")
    col3.metric("€/habitación", f"{precio/habitaciones:.0f} €")




