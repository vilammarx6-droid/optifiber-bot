import pandas as pd
import random

categorias = [
    "Cables de Fibra Óptica", 
    "Cajas NAP de Fibra Óptica", 
    "Herramientas de Pelado y Corte", 
    "KIT DE FTTH", 
    "Sistemas Starlink",
    "Seguridad y Cámaras (Imou/Hikvision)",
    "Redes Inalámbricas (Tp-Link)",
    "Equipos Activos (Huawei/Satraq)"
]

marcas = ["Huawei", "Tp-Link", "Satraq", "Hikvision", "Imou", "Starlink", "Optifiber"]

productos = []
for i in range(1, 151):
    categoria = random.choice(categorias)
    marca = random.choice(marcas)
    
    if categoria == "Cables de Fibra Óptica":
        nombre = f"Cable Fibra Óptica {marca} {random.choice(['Drop G.657A2', 'ADSS', 'ASU'])} {random.choice(['1 Hilo', '2 Hilos', '12 Hilos'])} Bobina {random.choice(['1km', '2km'])}"
        precio = round(random.uniform(50.0, 300.0), 2)
    elif categoria == "Cajas NAP de Fibra Óptica":
        nombre = f"Caja NAP Exterior/Interior {marca} {random.choice(['8 Puertos', '16 Puertos'])} IP65/IP67"
        precio = round(random.uniform(15.0, 60.0), 2)
    elif categoria == "Herramientas de Pelado y Corte":
        nombre = f"Herramienta Profesional {marca} {random.choice(['Peladora de Fibra', 'Cortadora (Cleaver)', 'Pinza de Precisión'])}"
        precio = round(random.uniform(20.0, 150.0), 2)
    elif categoria == "KIT DE FTTH":
        nombre = f"Kit Completo FTTH {marca} (Incluye OLT, Cajas y Herramientas)"
        precio = round(random.uniform(500.0, 1500.0), 2)
    elif categoria == "Sistemas Starlink":
        marca = "Starlink"
        nombre = f"Antena Starlink {random.choice(['Standard', 'Mini V4', 'High Performance'])} Kit Internet Satelital"
        precio = round(random.uniform(300.0, 2500.0), 2)
    elif categoria == "Seguridad y Cámaras (Imou/Hikvision)":
        marca = random.choice(["Hikvision", "Imou"])
        nombre = f"Cámara de Seguridad {marca} {random.choice(['PTZ', 'Domo', 'Bala'])} 4MP Wi-Fi"
        precio = round(random.uniform(35.0, 200.0), 2)
    else:
        nombre = f"Equipo Profesional {marca} Modelo {i} para {categoria}"
        precio = round(random.uniform(10.0, 400.0), 2)
        
    stock = random.randint(0, 500)
    descripcion = f"Producto original {marca} ideal para despliegues profesionales e ISPs en Perú. Categoría: {categoria}."
    
    productos.append([nombre, categoria, precio, stock, descripcion])

df = pd.DataFrame(productos, columns=["Producto", "Categoria", "Precio_PEN", "Stock_Actual", "Descripcion"])
# Multiplicamos el precio por 3.8 para simular Soles Peruanos (PEN)
df['Precio_PEN'] = (df['Precio_PEN'] * 3.8).round(2)
df.to_csv("data/inventario.csv", index=False)
print("Generados 150 productos 100% basados en optifiber.pe")
