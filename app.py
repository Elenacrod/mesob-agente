import streamlit as st
import subprocess
import sys

st.set_page_config(page_title="MESOB - Asistente del Máster", page_icon="🎓", layout="centered")

st.title("🎓 MESOB — Asistente del Máster")
st.caption("Haz preguntas sobre la documentación del máster")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Escribe tu pregunta..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Consultando MESOB..."):
            result = subprocess.run(
                [sys.executable, "-m", "notebooklm", "ask", prompt],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            response = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
