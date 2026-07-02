# Proyecto OptiBot - Lura Agente (Oracle ONE)

¡Hola! Este es mi proyecto para el desafío de crear un agente inteligente. Decidí hacer un bot asistente (OptiBot) enfocado en una empresa peruana real de telecomunicaciones llamada Optifiber. 

La idea principal es resolver el "dolor" que tienen muchas empresas que venden equipos técnicos: armar cotizaciones rápido y responder dudas de los clientes sin tener que buscar manualmente en un excel de inventario gigante.

## ¿Cómo funciona? (Arquitectura)
Para armar esto usé algunas herramientas que fuimos viendo y otras que investigué:
* **Streamlit:** Para hacer la interfaz visual súper rápida y permitir que el usuario suba su propio archivo CSV ahí mismo (como mostraron en el ejemplo del evento).
* **Pandas:** Para leer el archivo `inventario.csv` que sube el usuario.
* **LangChain y Cohere:** El agente lee toda la tabla de productos usando una técnica llamada RAG (le pasamos el texto directo al prompt). Elegí esto en lugar del agente de pandas para evitar que se quede pensando en bucle cuando le haces preguntas raras.

## Link del Proyecto (Deploy)
Aquí pueden probar el bot funcionando en la nube de Streamlit sin instalar nada:
👉 **[https://optifiber-bot-nansjpmb8nw9bdpqk52nsb.streamlit.app](https://optifiber-bot-nansjpmb8nw9bdpqk52nsb.streamlit.app)**

## ¿Cómo correrlo en tu compu?
Si quieres probar el código en local, estos son los pasos:

1. Clona este repositorio y entra a la carpeta:
   ```bash
   git clone https://github.com/vilammarx6-droid/optifiber-bot
   cd optifiber_bot
   ```
2. Instala las librerías que usé:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la aplicación web:
   ```bash
   streamlit run streamlit_app.py
   ```

## Ejemplos para probar el bot
Para que el bot funcione, primero tienes que subir el archivo `inventario.csv` que está en la carpeta `data` usando el botón de la izquierda. Luego, puedes probar con estas preguntas:

1. **Para ver si sabe quién es:**
   * Pregunta: *"¿Qué es Optifiber y a qué se dedican?"*
   * Respuesta esperada: Te explicará que venden equipos para ISPs y técnicos, y que no hacen instalaciones en casas.

2. **Para ver si busca bien en el inventario:**
   * Pregunta: *"Me recomendaron usar un repetidor para mi casa, ¿tienes alguno?"*
   * Respuesta esperada: Va a buscar sinónimos y te ofrecerá los Routers Wi-Fi Tp-Link con su precio exacto (porque no hay "repetidores" literales en el excel).

3. **Para ver cómo cotiza:**
   * Pregunta: *"Hazme una cotización de 5 cámaras Hikvision y una antena Starlink"*
   * Respuesta esperada: Te va a generar una tabla bien armada con los precios unitarios sacados del CSV, las cantidades, y el total sumado.

---
*Hecho para el challenge de Oracle ONE.*
