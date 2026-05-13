import streamlit as st
import subprocess
import sys
import os
import tempfile

st.set_page_config(page_title="MESOB - Asistente del Máster", page_icon="🎓", layout="centered")

st.title("🎓 MESOB — Asistente del Máster")
st.caption("Haz preguntas sobre la documentación del máster")

# En la nube: lee la autenticación desde variable de entorno
auth_path = None
auth_json = os.environ.get("NOTEBOOKLM_AUTH_JSON")
if auth_json:
    tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
    tmp.write(auth_json)
    tmp.close()
    auth_path = tmp.name

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
            cmd = [sys.executable, "-m", "notebooklm"]
            if auth_path:
                cmd += ["--storage", auth_path]
            cmd += ["ask", prompt]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            response = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
