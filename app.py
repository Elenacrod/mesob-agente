import streamlit as st
import subprocess
import sys
import os
import tempfile
import base64

st.set_page_config(page_title="MESOB - Asistente del Máster", page_icon="🎓", layout="centered")

st.title("🎓 MESOB — Asistente del Máster")
st.caption("Haz preguntas sobre la documentación del máster")

# En la nube: decodifica el auth desde base64
auth_path = None
auth_b64 = os.environ.get("NOTEBOOKLM_AUTH_B64")
if auth_b64:
    auth_bytes = base64.b64decode(auth_b64)
    tmp = tempfile.NamedTemporaryFile(mode="wb", suffix=".json", delete=False)
    tmp.write(auth_bytes)
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
                encoding="utf-8",
                errors="replace"
            )
            response = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
