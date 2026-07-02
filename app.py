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
        # Inicializamos el motor de IA (Cohere) con una temperatura baja (0.2) 
        # para que sus respuestas sean técnicas, precisas y no alucine datos.
        self.llm = ChatCohere(temperature=0.2, cohere_api_key=api_key)
        self.df = df
        
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

REGLAS ESTRICTAS:
1. Usa el inventario de arriba para buscar productos, descripciones, precios y stock. Busca palabras clave o sinónimos.
2. Si te preguntan "qué es Optifiber" o "qué hacen", responde defendiendo la marca.
3. SIEMPRE que recomiendes un producto, menciona su 'Precio_USD' exacto del inventario y revisa el 'Stock_Actual'.
4. Si el usuario pregunta "cuánto costaría" o pide cotizar, asume una cantidad (ej. 1 unidad) y DIBUJA UNA TABLA Markdown con Producto, Precio Unitario, Cantidad y Subtotal. Suma el Total.
5. Responde como un consultor técnico amable, sin evasivas ni rodeos.
"""

    def invoke(self, question: str) -> str:
        """
        Esta función recibe la pregunta del usuario, la une con las reglas del sistema
        y le pide a Cohere que genere una respuesta.
        """
        prompt = f"{self.system_message}\n\nPregunta del Cliente: {question}"
        response = self.llm.invoke(prompt)
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
        respuesta = agente.invoke(args.pregunta)
        print("=" * 60)
        print(respuesta)
        return

    # Si no nos mandaron parámetros, abrimos un chat interactivo eterno en la terminal
    print("Modo interactivo (Backend). Escribe 'salir' para terminar.\n")
    while True:
        pregunta = input("Tu pregunta: ").strip()
        if not pregunta or pregunta.lower() in {"salir", "exit", "quit"}:
            break
        respuesta = agente.invoke(pregunta)
        print("=" * 60)
        print(respuesta)
        print()

# Esta línea asegura que main() solo se ejecute si corremos ESTE archivo directo,
# pero NO si lo importamos desde Streamlit.
if __name__ == "__main__":
    main()
