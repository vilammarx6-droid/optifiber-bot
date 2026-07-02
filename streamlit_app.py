import os
import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Importamos el cerebro (backend) desde nuestro archivo principal app.py
from app import build_agent

# 1. CONFIGURACIÓN VISUAL DE LA PÁGINA
# Esto le dice a Streamlit cómo se va a ver nuestra pestaña en el navegador web
st.set_page_config(page_title="OptiBot", page_icon="🤖", layout="wide")

# Pintamos el título principal
st.title("🤖 OptiBot: Asistente B2B de Telecomunicaciones")
st.caption("Consulta el inventario corporativo de Optifiber en tiempo real.")


def sync_secrets_to_env() -> None:
    """
    Truco avanzado: Si la aplicación está corriendo en la nube (Streamlit Cloud),
    tomamos la contraseña de 'st.secrets' y la inyectamos en las variables de entorno locales.
    Así nuestro backend no se da cuenta de la diferencia.
    """
    try:
        secrets_dict = dict(st.secrets)
    except Exception:
        return
    if "COHERE_API_KEY" in secrets_dict and not os.getenv("COHERE_API_KEY"):
        os.environ["COHERE_API_KEY"] = str(secrets_dict["COHERE_API_KEY"])


# Carga de seguridad dual: lee archivos .env (local) o secretos de Streamlit (nube)
load_dotenv()
sync_secrets_to_env()


def api_key_ref() -> str:
    """
    Oculta casi toda la API Key por seguridad, devolviendo solo los últimos 4 dígitos
    para que el usuario sepa que sí la detectamos correctamente.
    """
    key = os.getenv("COHERE_API_KEY")
    if not key:
        return "no-configurada"
    if len(key) <= 10:
        return "configurada"
    return f"{key[:4]}...{key[-4:]}"


def reset_chat() -> None:
    """Borra la memoria temporal de la sesión para iniciar de cero."""
    st.session_state.messages = []
    st.session_state.agent_blocked = False


@st.cache_resource
def get_agent_instance(df: pd.DataFrame):
    """
    Inicializa nuestro agente de IA. Usamos @st.cache_resource para que el "Cerebro" 
    solo se construya una vez y se quede guardado en memoria, haciendo la app rapidísima.
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("API Key no configurada.")
    return build_agent(api_key, df)


# --- BARRA LATERAL (SIDEBAR) ---
# Todo el código dentro de este bloque se dibujará en el menú de la izquierda
with st.sidebar:
    st.header("Configuración")
    st.write("Panel de control del asistente.")
    
    # Botón mágico para resetear la memoria
    if st.button("🧹 Limpiar chat"):
        reset_chat()
        st.rerun()

    st.divider()
    st.header("Gestión de Inventario")

    # Formulario para que evaluadores puedan subir su propio CSV y romper las reglas si quieren
    with st.form("upload_form", clear_on_submit=True):
        uploaded_file = st.file_uploader(
            "📂 Actualizar Inventario (Opcional)",
            type=["csv"],
            help="Límite: 200 MB por archivo • Solo CSV"
        )
        submitted = st.form_submit_button("💾 Guardar y actualizar base")
        
        # Si el usuario subió algo nuevo, lo inyectamos en la sesión activa
        if submitted and uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.df = df
                st.cache_resource.clear()  # Obligamos a reconstruir el agente con los nuevos datos
                st.success("Inventario actualizado con éxito.")
                st.rerun()
            except Exception as e:
                st.error(f"Error al cargar el CSV: {e}")

    # Mini panel que te avisa qué archivo de base de datos estamos leyendo
    st.subheader("📑 Base de Datos Actual")
    if "df" not in st.session_state:
        # Si nadie ha subido nada, leemos el original de la empresa de manera silenciosa
        try:
            st.session_state.df = pd.read_csv("data/inventario.csv")
            st.write("✅ `inventario.csv` (Original de Optifiber)")
        except:
            st.write("❌ No hay inventario cargado.")
    else:
        st.write("✅ Inventario personalizado activo")

    # Botón para borrar el archivo custom y regresar al original
    col1, col2 = st.columns([0.85, 0.20])
    col1.write("Restaurar por defecto")
    if col2.button("🗑️", key="del_custom"):
        if "df" in st.session_state:
            del st.session_state.df
        st.cache_resource.clear()
        st.rerun()


# --- CHAT PRINCIPAL (LA ZONA DE MAGIA) ---

# Preparamos las variables de la sesión (solo la primera vez que entras)
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent_blocked" not in st.session_state:
    st.session_state.agent_blocked = False

# Renderizamos todo el historial de la conversación
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# La caja de texto flotante de abajo donde escribes tus dudas
pregunta = st.chat_input("✍️ Escribe tu pregunta técnica o pide una cotización...")

# ¿El usuario apretó enter?
if pregunta:
    # 1. Chequeos de seguridad previos
    if st.session_state.agent_blocked:
        st.warning("⚠️ El agente quedó bloqueado por un error previo. Pulsa 'Limpiar chat' para reintentar.")
        st.stop()

    if "df" not in st.session_state:
        st.error("⚠️ No hay base de datos cargada. Por favor sube un archivo CSV.")
        st.stop()

    # 2. Dibujamos en pantalla lo que el usuario acaba de preguntar
    st.session_state.messages.append({"role": "user", "content": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # 3. Dibujamos la respuesta de la IA
    with st.chat_message("assistant"):
        with st.spinner("🤔 Analizando inventario..."):
            try:
                # Instanciamos a OptiBot pasándole el DataFrame
                agente = get_agent_instance(st.session_state.df)
                
                # Le pedimos la respuesta enviándole TODO el historial de la conversación
                respuesta = agente.invoke(st.session_state.messages)
                
                # Pintamos en pantalla y guardamos en memoria
                st.markdown(respuesta)
                st.session_state.messages.append(
                    {"role": "assistant", "content": respuesta}
                )
                
            except Exception as exc:
                # Si Cohere falla (se cae su servidor, o llave inválida), bloqueamos por seguridad
                error_msg = f"❌ Error conectando con la IA: {exc}\n\nReferencia API key: {api_key_ref()}"
                st.error(error_msg)
                st.session_state.agent_blocked = True
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )
