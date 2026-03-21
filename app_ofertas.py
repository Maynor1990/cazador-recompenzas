import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
from PIL import Image
import pytesseract

# --- CONFIGURACIÓN ---
# Asegúrate de haber instalado Tesseract en esta ruta de Windows:
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.set_page_config(page_title="Cazador de Ofertas", page_icon="🛒")
ARCHIVO_DB = "mis_precios.json"

def cargar_datos():
    if os.path.exists(ARCHIVO_DB):
        with open(ARCHIVO_DB, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def guardar_datos(datos):
    with open(ARCHIVO_DB, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

datos = cargar_datos()

# --- MENÚ ---
st.sidebar.header("Menú Principal")
menu = st.sidebar.radio("Ir a:", ["🔍 Comparar Oferta", "➕ Registrar Producto", "📸 Escanear Ticket", "📊 Mi Inventario"])

# --- SECCIÓN NUEVA: ESCANEAR ---
if menu == "📸 Escanear Ticket":
    st.header("📸 Escanear Ticket")
    archivo = st.file_uploader("Sube la foto del ticket", type=["jpg", "png", "jpeg"])
    
    if archivo:
        img = Image.open(archivo)
        st.image(img, caption="Ticket cargado", use_container_width=True)
        
        if st.button("🔍 Leer Texto del Ticket"):
            try:
                texto = pytesseract.image_to_string(img, lang='spa')
                st.subheader("Texto detectado:")
                st.text_area("Resultado:", texto, height=300)
                st.success("¡Lectura completa! Ahora puedes copiar los precios detectados.")
            except Exception as e:
                st.error("Error: No se encontró el motor Tesseract. ¿Lo instalaste en C:\\Program Files\\Tesseract-OCR?")

# --- LAS OTRAS SECCIONES (IGUAL QUE ANTES) ---
elif menu == "➕ Registrar Producto":
    st.header("Registrar Producto")
    nombre = st.text_input("Nombre")
    precio = st.number_input("Precio Ideal", min_value=0.0)
    if st.button("Guardar"):
        datos[nombre.lower()] = {"precio_ideal": precio, "fecha": datetime.now().strftime("%Y-%m-%d")}
        guardar_datos(datos)
        st.success("Guardado.")

elif menu == "🔍 Comparar Oferta":
    st.header("Comparar")
    if datos:
        prod = st.selectbox("Producto", list(datos.keys()))
        precio_t = st.number_input("Precio Tienda", min_value=0.0)
        if st.button("Verificar"):
            p_i = datos[prod]["precio_ideal"]
            if precio_t <= p_i:
                st.balloons()
                st.success(f"¡Oferta! Ahorras ${p_i - precio_t:.2f}")
            else:
                st.error(f"Caro. Pagas ${precio_t - p_i:.2f} de más.")

elif menu == "📊 Mi Inventario":
    st.header("Inventario")
    if datos:
        st.table(pd.DataFrame([{"Producto": k, "Precio": v["precio_ideal"]} for k, v in datos.items()]))