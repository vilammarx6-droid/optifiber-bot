# Proyecto OptiBot - Lura Agente (Challenge Oracle ONE)

## 📖 Descripción general del proyecto
OptiBot es un agente inteligente diseñado específicamente para el sector B2B de las telecomunicaciones. Su propósito es actuar como el asistente técnico y comercial oficial de **Optifiber** (https://www.optifiber.pe/), una empresa peruana especializada en soluciones de conectividad. 
El bot ayuda a clientes, ISPs y técnicos instaladores a consultar el inventario de la empresa, cotizar productos en Soles (PEN) y resolver dudas sobre la logística de envíos y sedes, automatizando una tarea que usualmente consume mucho tiempo de forma manual.

## 🏗️ La arquitectura de la solución implementada
La solución se construyó separando claramente el "Cerebro" (lógica de IA y memoria) de la "Interfaz Visual":
1. **Frontend (Streamlit):** Proporciona una interfaz web interactiva donde el usuario puede hablar en un chat en tiempo real y subir dinámicamente un archivo CSV con el inventario actualizado, el cual alimenta directamente al agente.
2. **Backend (Python + LangChain):** Actúa como el controlador. Recibe la base de datos CSV, la convierte a texto plano (Markdown) y la inyecta como contexto junto a un poderoso *System Prompt* que define las reglas de negocio, logística, personalidad y memoria de la conversación.
3. **Motor LLM (Cohere):** Procesa el contexto (historial + inventario + reglas) mediante la arquitectura RAG (Retrieval-Augmented Generation) para responder las consultas de los usuarios sin "alucinar" datos.

## 🛠️ Las tecnologías y herramientas utilizadas
- **Lenguaje Base:** Python 3
- **Framework Web:** Streamlit (para la interfaz UI y despliegue rápido).
- **Inteligencia Artificial:** LangChain (orquestación) y Cohere API (`ChatCohere` con baja temperatura para respuestas precisas).
- **Procesamiento de Datos:** Pandas (para lectura, manipulación y conversión del archivo `.csv`).
- **Variables de Entorno:** `python-dotenv` para proteger las llaves de la API (API Keys).

## 🚀 Instrucciones para ejecutar el proyecto
1. Clona este repositorio en tu computadora:
   ```bash
   git clone https://github.com/vilammarx6-droid/optifiber-bot.git
   cd optifiber-bot
   ```
2. Crea un entorno virtual e instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Crea un archivo llamado exactamente `.env` en la raíz del proyecto y agrega tu llave secreta de Cohere:
   ```env
   COHERE_API_KEY="tu_llave_de_cohere_aqui"
   ```
4. Inicia la aplicación en tu navegador:
   ```bash
   streamlit run streamlit_app.py
   ```

## ❓ Ejemplos de preguntas que el agente puede responder
- **Conocimiento Institucional:** *"¿Qué es Optifiber y cómo los contacto?"* o *"¿Tienen una sede física para ir a comprar?"*
- **Consulta de Stock:** *"Me recomendaron usar cajas NAP, ¿tienes alguna de 16 puertos en stock?"*
- **Cotizaciones y Lógica de Negocio:** *"Cotízame 5 cajas NAP y 2 bobinas de cable de fibra. Dime en qué moneda está el precio y en cuánto tiempo llegan a provincia."*

## 🤖 Ejemplos de respuestas generadas por el agente
**Pregunta:** *"Cotízame 5 cajas NAP y dime dónde puedo recogerlas y en cuánto tiempo llegan a provincia"*
**Respuesta del Agente:**
> ¡Hola! Soy OptiBot, el asistente de Optifiber. A continuación, te proporciono la cotización para 5 cajas NAP y la información sobre cómo recogerlas y los tiempos de envío a provincia.
>
> ### Cotización de 5 Cajas NAP
> En nuestro inventario, tenemos varias opciones. Te cotizaré la más económica, que es la **Caja NAP Exterior/Interior Huawei 8 Puertos IP65/IP67**, con un precio de **S/ 73.07** por unidad.
>
> | Producto | Precio Unitario (S/) | Cantidad | Subtotal (S/) |
> |----------|----------------------|-----------|---------------|
> | Caja NAP Exterior Huawei 8 Puertos | 73.07 | 5 | 365.35 |
>
> **Total: S/ 365.35**
>
> ### Recogida y Envío
> - **Recogida en Tienda**: Puedes recoger tu pedido en nuestra tienda principal ubicada en **Av. Tomasa Tito Condemayta Nro. 1614**.
> - **Envío a Provincia**: Si prefieres que te lo enviemos, los tiempos de entrega a provincia son de **48 a 72 horas** mediante agencias como **Shalom** o **Marvisur**.
> 
> ¿Te gustaría que te proporcione más detalles sobre algún otro producto?

## ☁️ Evidencia del Deploy en la Nube
El proyecto está desplegado de forma pública y 100% funcional. Puedes interactuar con la IA haciendo clic en el siguiente enlace:
👉 **[https://optifiber-bot-nansjpmb8nw9bdpqk52nsb.streamlit.app](https://optifiber-bot-nansjpmb8nw9bdpqk52nsb.streamlit.app)**
*(La aplicación se encuentra hospedada en Streamlit Community Cloud).*
