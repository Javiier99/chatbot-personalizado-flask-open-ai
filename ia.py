from openai import OpenAI
from pypdf import PdfReader
import base64
import io
import os
import tempfile


# ! Copiar y entender abajo


client = OpenAI(base_url="http://localhost:1235/v1", api_key='lm-studio"')
# model = "" # Colocar el modelo de la IA

MAX_CARACTERES_PDF = 20000

SYSTEM_PROMPT = (
    "Eres un asistente en Español contestarás todas las preguntas que te dé el usuario y además "
    "en caso de que no diga nada simplemente responderas en que puedo ayudarte o si no dice nada "
    "y manda archivo analiza el archivo, la imagen o haz un resumen de un audio"
)

def leer_pdf(datos: bytes) -> str:
    lector = PdfReader(io.BytesIO(datos))
    texto = "\n".join(pagina.extract_text() or "" for pagina in lector.pages)
    if not texto.strip():
        return "El pdf no tiene texto extraible; puede ser un escaneo y se necesita OCR"

    return texto[:MAX_CARACTERES_PDF]

def transcribir_audio(datos: bytes, nombre:str) -> str:
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return "No se puede transcribir el audio, instala daster-whisper"
    extension = os.path.splitext(nombre)[1] or ".mp3"
    with tempfile.NamedTemporaryFile(suffix=extension, delete=False) as tmp:
        tmp.write(datos)
        ruta = tmp.name

    try:
        modelo = WhisperModel("small", device = "cpu", compute_type="int8")
        segmentos, _ = modelo.transcribe(ruta, language="es")
        return " ".join(s.text.strip() for s in segmentos)
    finally:
        os.remove(ruta)


def preparar_contenido(promt: str, archivos) -> list:
    contenido = [{"type":"text", "text": promt or "Analiza el archivo adjunto"}]
    for archivo in archivos or []:
        if not  archivo  or not archivo.filename:
            continue
        tipo = archivo.mimetype or ""
        datos = archivo.read()

        if tipo.startswith("image/"):
            b64 = base64.b64encode(datos).decode()
            contenido.append({
                "type": "image_url",
                "image_url": {"url": f"data:{tipo};base64,{b64}"}
            })
        elif tipo == "application/pdf":
            contenido.append({
                "type": "text",
                "text": f"Contenido del PDF '{archivo.filename}':\n{leer_pdf(datos)}",
            })
        elif tipo.startswith("audio/"):
            contenido.append({
                "type": "text",
                "text": f"Transcripción del audio '{archivo.filename}':\n"
                        f"{transcribir_audio(datos, archivo.filename)}",
            })
    return contenido


def obtener_respuesta(promt: str, model: str, archivos=None, temperature: float = 0):
    messaje = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": preparar_contenido(promt, archivos)},
    ]
    reply = client.chat.completions.create(
        model=model,
        messages=messaje,
        temperature=temperature,
    )
    return reply.choices[0].message.content

