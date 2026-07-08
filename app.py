import os
import argparse
import pandas as pd
from dotenv import load_dotenv
from langchain_cohere import ChatCohere

# 1. CARGA DE SEGURIDAD
# Cargamos las variables de entorno para que nuestra API Key se mantenga secreta
# (Busca automáticamente un archivo .env en tu computadora).
load_dotenv()

class OptiBotAgent:
    """
    Clase principal que actúa como el 'Cerebro' de nuestro asistente.
    Toda la lógica de LangChain y Cohere vive aquí adentro, aislada de la interfaz gráfica.
    """
    
    def __init__(self, api_key: str, df: pd.DataFrame):
        # Configuramos el motor de IA
        self.llm = ChatCohere(
            cohere_api_key=api_key,
            model="command-r",  # o command-r-plus
            temperature=0.1
        )
            
        # Convertimos nuestro DataFrame de Pandas a un formato de texto (Markdown).
        # Así es mucho más fácil que el LLM lo lea y lo entienda.
        self.csv_string = df.to_markdown(index=False)
        
        # PROMPT DEL SISTEMA: Aquí definimos la "Personalidad" y las "Reglas" del agente.
        self.system_message = f"""Eres OptiBot, el asistente corporativo B2B y representante oficial de Optifiber (https://www.optifiber.pe/).
Optifiber es una empresa líder en telecomunicaciones especializada en soluciones de Fibra Óptica y conectividad. 
Tu misión es defender y promover la marca Optifiber, resaltando que proveemos equipos de altísima calidad (Cajas NAP, cables de fibra, kits FTTH, herramientas de precisión, equipos Tp-Link, Hikvision, Huawei y antenas Starlink) ideales para ISPs y técnicos instaladores.
Si un usuario pregunta qué somos o qué hacemos, explícale nuestra misión con orgullo.
Si un usuario necesita orientación sobre nuestro portal web, guíalo a las secciones de 'Tienda', 'STARLINK' o 'Contáctenos' en optifiber.pe, o sugiérele contactarnos vía WhatsApp para atención rápida.

Además, tu función técnica es ayudar a clientes a consultar el inventario y dar cotizaciones usando los datos proporcionados.
Responde de manera formal, cálida, profesional y precisa.
Muestra los precios en la moneda indicada y sugiere productos relacionados. Si no tienes un dato en el inventario, indícalo amablemente pero resalta que nuestro equipo de ventas en la web puede ayudarle.

INVENTARIO DISPONIBLE (Solo tienes esto para vender, nada más):
{self.csv_string}

LOGÍSTICA Y UBICACIÓN:
- Sede Física: Nuestra tienda principal está ubicada en Av. Tomasa Tito Condemayta Nro. 1614. Los clientes pueden recoger sus pedidos aquí.
- Tiempos de Envío: Entregas en 24 horas para pedidos locales, y despachos a nivel nacional (todo el Perú) con tiempos de 48 a 72 horas mediante agencias (Shalom, Marvisur, etc.).

REGLAS ESTRICTAS:
1. Usa el inventario de arriba para buscar productos, descripciones, precios y stock. Busca palabras clave o sinónimos.
2. Si te preguntan "qué es Optifiber" o "qué hacen", responde defendiendo la marca.
3. SIEMPRE que recomiendes un producto, menciona su 'Precio_PEN' exacto del inventario y revisa el 'Stock_Actual'. Aclara siempre que los precios están en Soles (S/).
4. Si el usuario pregunta "cuánto costaría" o pide cotizar, asume una cantidad (ej. 1 unidad) y DIBUJA UNA TABLA Markdown con Producto, Precio Unitario, Cantidad y Subtotal. Suma el Total.
5. Responde como un consultor técnico amable, sin evasivas ni rodeos.
"""

    def invoke(self, messages_history: list) -> str:
        """
        Esta función recibe el historial de conversación y lo convierte a formato LangChain
        para que Cohere lo procese correctamente como un chat (evitando errores 422).
        """
        from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
        
        # 1. Añadimos el System Prompt (las reglas)
        langchain_messages = [SystemMessage(content=self.system_message)]
        
        # 2. Añadimos solo el historial reciente (últimos 10 mensajes) para no exceder el límite de tokens
        historial_reciente = messages_history[-10:]
        
        for msg in historial_reciente:
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            else:
                langchain_messages.append(AIMessage(content=msg["content"]))
                
        # 3. Enviamos la lista de objetos en lugar de un string gigante
        response = self.llm.invoke(langchain_messages)
        return response.content


def build_agent(api_key: str, df: pd.DataFrame) -> OptiBotAgent:
    """
    Fábrica constructora: Centralizamos aquí la creación del agente 
    para poder llamarlo fácilmente desde nuestra página web en Streamlit.
    """
    return OptiBotAgent(api_key, df)


def main() -> None:
    """
    Punto de entrada para la consola (Modo CLI).
    Nos permite probar el bot en la terminal sin necesidad de levantar el servidor web.
    """
    # Configuramos argparse para poder pasarle preguntas directo en el comando, ej:
    # python app.py --pregunta "Hola"
    parser = argparse.ArgumentParser(description="OptiBot CLI (Backend Agent)")
    parser.add_argument("--pregunta", type=str, help="Pregunta para el agente")
    args = parser.parse_args()

    # Validamos que el desarrollador haya configurado su llave secreta
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        print("❌ Error crítico: Falta configurar la variable de entorno COHERE_API_KEY.")
        return

    # Intentamos cargar la base de datos central
    try:
        df = pd.read_csv("data/inventario.csv")
    except Exception as e:
        print(f"❌ Error cargando inventario base: {e}")
        return

    # Encendemos el "Cerebro"
    agente = build_agent(api_key, df)

    # Si nos mandaron una pregunta por comando de consola, la respondemos y salimos
    if args.pregunta:
        respuesta = agente.invoke([{"role": "user", "content": args.pregunta}])
        print("=" * 60)
        print(respuesta)
        return

    # Si no nos mandaron parámetros, abrimos un chat interactivo eterno en la terminal
    print("Modo interactivo con MEMORIA (Backend). Escribe 'salir' para terminar.\n")
    historial = []
    while True:
        pregunta = input("Tu pregunta: ").strip()
        if not pregunta or pregunta.lower() in {"salir", "exit", "quit"}:
            break
        historial.append({"role": "user", "content": pregunta})
        respuesta = agente.invoke(historial)
        historial.append({"role": "assistant", "content": respuesta})
        print("=" * 60)
        print(respuesta)
        print()

# Esta línea asegura que main() solo se ejecute si corremos ESTE archivo directo,
# pero NO si lo importamos desde Streamlit.
if __name__ == "__main__":
    main()
