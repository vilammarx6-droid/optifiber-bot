# Proyecto OptiBot - Lura Agente (Challenge Oracle ONE)

> ⚠️ **Aviso Importante / Disclaimer Académico:** 
> Este proyecto fue desarrollado exclusivamente con fines educativos como parte del *Challenge Agente* del programa Oracle Next Education (ONE) en colaboración con Alura Latam. **OptiBot NO es un canal de comunicación oficial de Optifiber**. Los datos presentados, aunque inspirados en el sector real de telecomunicaciones, son simulados para demostrar las capacidades técnicas de la Inteligencia Artificial.

## 📖 Descripción general del proyecto
OptiBot es un agente inteligente (Chatbot B2B) diseñado específicamente para el sector de las telecomunicaciones y la infraestructura de redes. Su propósito es simular un asistente técnico y comercial capaz de atender a proveedores de Internet (ISPs), ingenieros y técnicos instaladores. 

El principal desafío que resuelve esta aplicación es la **automatización de cotizaciones complejas y consultas de inventario**. En lugar de que un vendedor humano deba buscar manualmente en hojas de cálculo extensas, el agente es capaz de leer un archivo CSV masivo en tiempo real, comprender las necesidades técnicas del cliente (a través de lenguaje natural y sinónimos), y proporcionar respuestas precisas, cotizaciones formateadas y detalles de logística, todo en cuestión de segundos.

## 🏗️ La arquitectura de la solución implementada
La solución se ha construido bajo una arquitectura moderna dividida en dos capas principales, empleando el patrón **RAG (Retrieval-Augmented Generation)** para garantizar que la IA solo responda con información verídica del negocio:

1. **Frontend Interactivo (Streamlit):** 
   - Proporciona una interfaz web limpia, responsive y fácil de usar.
   - Cuenta con una barra lateral para subir dinámicamente archivos CSV, permitiendo actualizar la base de conocimientos "en caliente" sin tener que modificar el código fuente.
   - Mantiene el estado de la sesión (`Session State`) para asegurar que el historial del chat persista durante la navegación.

2. **Backend e IA (Python + LangChain + Cohere):** 
   - **Ingesta de Datos:** A través de la librería `Pandas`, el archivo CSV se lee, se limpia (manejando diferentes codificaciones como UTF-8 y Latin-1) y se transforma a un formato Markdown para optimizar la lectura por parte del LLM (Large Language Model).
   - **Ingeniería de Prompts (Prompt Engineering):** Se diseñó un *System Prompt* robusto que dota al agente de una "personalidad" corporativa, memoria institucional, y reglas estrictas de cotización (obligando a dar precios en Soles peruanos y respetando el stock).
   - **Memoria Contextual:** Se emplean las clases `SystemMessage`, `HumanMessage` y `AIMessage` de LangChain para empaquetar el historial de la conversación, permitiendo al bot recordar preguntas anteriores y mantener un hilo lógico.

## 🛠️ Las tecnologías y herramientas utilizadas
Para lograr un equilibrio entre rapidez de desarrollo, potencia computacional y facilidad de despliegue, se eligieron las siguientes herramientas:
- **Python 3.10+:** Lenguaje núcleo para la lógica de negocio y manipulación de datos.
- **Streamlit:** Framework ágil utilizado para crear la interfaz de usuario web y gestionar los eventos de carga de archivos y estados conversacionales.
- **Cohere API (Command-R):** Modelo de lenguaje de gran escala (LLM) seleccionado por su inmensa ventana de contexto (hasta 128k tokens) y su excelente capacidad para seguir instrucciones complejas (Chat API).
- **LangChain Core:** Framework utilizado como orquestador para estructurar correctamente los mensajes enviados al modelo de IA, evitando errores de formato y estandarizando la comunicación.
- **Pandas:** La herramienta estándar de la industria para el análisis y manipulación de los dataframes extraídos de los archivos CSV.
- **Dotenv (`python-dotenv`):** Fundamental para la ciberseguridad del proyecto, aislando las claves de las APIs en archivos locales para evitar filtraciones en repositorios públicos.

## 🚀 Instrucciones para ejecutar el proyecto
Si deseas ejecutar este proyecto en tu entorno local para modificar su comportamiento o adaptarlo a otra empresa, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/vilammarx6-droid/optifiber-bot.git
   cd optifiber-bot
   ```
2. **Instalar dependencias:**
   Se recomienda usar un entorno virtual (venv).
   ```bash
   pip install -r requirements.txt
   ```
3. **Configurar llaves de acceso:**
   Crea un archivo llamado `.env` en la raíz del proyecto e ingresa tu API Key de Cohere:
   ```env
   COHERE_API_KEY="tu_llave_de_cohere_aqui"
   ```
4. **Desplegar servidor local:**
   ```bash
   streamlit run streamlit_app.py
   ```
   La aplicación se abrirá automáticamente en tu navegador por defecto en el puerto `8501`.

## ❓ Ejemplos de preguntas que el agente puede responder
- **Conocimiento Institucional:** *"¿Qué es Optifiber, cuál es su misión y cómo los contacto?"*
- **Logística:** *"¿Tienen una sede física para ir a comprar o hacen envíos a provincia?"*
- **Consulta de Stock Avanzada:** *"Me recomendaron usar cajas NAP para un tendido, ¿tienes alguna de 16 puertos en stock y cuánto cuesta?"*
- **Cotizaciones Complejas:** *"Hazme una cotización formal de 5 cajas NAP y 2 bobinas de cable de fibra ADSS. Dime el precio total."*

## 🤖 Ejemplos de respuestas generadas por el agente
**Pregunta:** *"Cotízame 5 cajas NAP y dime dónde puedo recogerlas y en cuánto tiempo llegan a provincia"*

**Respuesta del Agente:**
> ¡Hola! Soy OptiBot, el asistente corporativo de Optifiber. Estaré encantado de ayudarte con tu cotización y tus dudas de logística. A continuación, te presento la información detallada para las cajas NAP.
>
> ### Cotización de Equipos
> De acuerdo con nuestro inventario en tiempo real, la opción más económica que tenemos en stock es la **Caja NAP Exterior/Interior Huawei 8 Puertos IP65/IP67**, con un valor unitario de **S/ 73.07**.
>
> | Producto | Precio Unitario (S/) | Cantidad | Subtotal (S/) |
> |----------|----------------------|-----------|---------------|
> | Caja NAP Exterior Huawei 8 Puertos | 73.07 | 5 | 365.35 |
>
> **Monto Total a Pagar: S/ 365.35**
>
> ### Logística y Entregas
> - **Recogida en Tienda Física**: Por supuesto, puedes acercarte a recoger los equipos en nuestra sede central ubicada en **Av. Tomasa Tito Condemayta Nro. 1614**. ¡Te esperamos!
> - **Envíos a Provincia**: Realizamos despachos a nivel nacional. Los tiempos de entrega a provincia son de **48 a 72 horas** y trabajamos con agencias de carga seguras como Shalom o Marvisur.
> 
> ¿Hay algún otro componente de fibra óptica que desees agregar a tu cotización?

## ☁️ Evidencia del Deploy en la Nube
El proyecto está desplegado de forma pública y es 100% interactivo. Puedes hablar con la IA en tiempo real haciendo clic en el siguiente enlace oficial:

👉 **[https://optifiber-bot-nansjpmb8nw9bdpqk52nsb.streamlit.app](https://optifiber-bot-nansjpmb8nw9bdpqk52nsb.streamlit.app)**

*(El despliegue fue realizado exitosamente utilizando Streamlit Community Cloud).*
