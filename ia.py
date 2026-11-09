from openai import OpenAI



client = OpenAI(base_url="http://localhost:1235/v1", api_key='lm-studio"')
# model = "" # Colocar el modelo de la IA

def obtener_respuesta(promt: str, model: str, temperature:float=0):
    messaje = [{
        'role' : 'system',
        'content' : "Eres un asistente en Español contestarás todas las preguntas que te dé el usuario y además en caso de que no diga nada simplemente responderas en que puedo ayudarte o si no dice nada y manda archivo analiza el archivo, la imagen o haz un resumen de un audio"
    },{
        'role' : 'user', 'content' : promt}]
    reply = client.chat.completions.create(
        model = model,
        messages= messaje,
        temperature= temperature
    )
    return reply.choices[0].message.content
