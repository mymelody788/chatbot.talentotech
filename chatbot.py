import groq as gr
import streamlit as st

modelos = ['llama3-8b-8192', 'llama3-70b-8192']

st.set_page_config(page_title= "Mi primer Chatbot", page_icon= "👩‍💻")

def configurar_página():
    st.title("Bienvenidos a 'Mi primer Chatbot'")
    st.subheader("Mi chat de IA:")
    nombre = st.text_input("¿Cuál es tu nombre?")
    if st.button("Saludar"):
        st.write(f"Hola {nombre}! ¿Puedo ayudarte en algo?")

def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA favorito")
    modelo = st.sidebar.selectbox("¿Cuál elegís?", modelos, index=0)
    st.sidebar.write(f"**Elegiste el modelo** : {modelo}")
    return modelo

def crear_cliente_groq():
    groq_api_key = st.secrets["Groq_API_Key"]
    return gr.Groq(api_key=groq_api_key)

def inicialización_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

def mostrar_historial_chat():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"]):
            st.markdown(mensaje["content"])

def obtener_mensaje_usuario():
    return st.chat_input("Escribí tu mensaje por acá:")

def agregar_mensajes_historial(role, content):
    st.session_state.mensajes.append({"role": role, "content": content})

def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)

def obtener_respuestas_modelo(cliente, modelo, mensaje):
    respuesta = cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False
    )
    return respuesta.choices[0].message.content

def ejecutar_app():
    configurar_página()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    inicialización_estado_chat()
    mostrar_historial_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    if mensaje_usuario:
        agregar_mensajes_historial("user", mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
        mensaje_modelo = obtener_respuestas_modelo(cliente, modelo, st.session_state.mensajes)
        agregar_mensajes_historial("assistant", mensaje_modelo)
        mostrar_mensaje("assistant", mensaje_modelo)
        print(f"{"user", mensaje_usuario},{"assistant", mensaje_modelo}")

if __name__ == '__main__':
    ejecutar_app()



